# frozen_string_literal: true

# Every post also gets a plain Markdown copy next to its page, following the
# llms.txt convention (same URL with .md): /post/<slug>/ → /post/<slug>.md.
# AI agents and "paste into a chat" readers get clean text instead of the
# site's HTML. The copy is the post's own Markdown source with Liquid
# rendered ({% post_url %}, image paths), diagrams swapped for their text
# alternative, kramdown attribute lines dropped and on-site links made
# absolute. Written after the site is built, so it never shows up in the
# sitemap or feeds. Any error only warns — it must never block a deploy.
#
# Linked from each post's <head> (rel="alternate" type="text/markdown"), the
# share row, and /llms.txt.

require "cgi"
require "fileutils"

module PostMarkdown
  FIGURE = %r{<figure class="diagram"[^>]*>(.*?)</figure>}m
  IAL_LINE = /^[ \t]*\{:[^}\n]*\}[ \t]*\n?/

  def self.inner(html, tag)
    m = html.match(%r{<#{tag}\b[^>]*>(.*?)</#{tag}>}m)
    m && m[1].strip.gsub(/\s+/, " ")
  end

  def self.md_path(url)
    url.chomp("/") + ".md"
  end

  def self.diagrams_to_text(text, post_url)
    text.gsub(FIGURE) do
      fig = Regexp.last_match(1)
      title = CGI.unescapeHTML(inner(fig, "title") || "Diagram")
      desc = inner(fig, "desc")
      caption = inner(fig, "figcaption")
      lines = ["> **Diagram: #{title}** ([see it in the post](#{post_url}))"]
      lines << ">" << "> #{CGI.unescapeHTML(desc)}" if desc && !desc.empty?
      lines << ">" << "> *#{caption}*" if caption && !caption.empty?
      lines.join("\n")
    end
  end

  def self.absolutize(text, base)
    text = text.gsub(%r{\]\(/(?!/)}) { "](#{base}/" }
    text = text.gsub(%r{\b(href|src)="/(?!/)}) { %(#{Regexp.last_match(1)}="#{base}/) }
    text.gsub(/\bsrcset="([^"]*)"/) do
      list = Regexp.last_match(1).gsub(%r{(\A|,\s*)/(?!/)}) { "#{Regexp.last_match(1)}#{base}/" }
      %(srcset="#{list}")
    end
  end

  def self.header(post, url, date)
    out = +"# #{post.data['title']}\n\n"
    out << "By #{post.site.config.dig('author', 'name') || 'Avinash Gosavi'} · #{date} · #{url}\n"
    tags = Array(post.data["tags"])
    out << "Topics: #{tags.join(', ')}\n" unless tags.empty?
    desc = post.data["description"].to_s.strip
    out << "\n> #{desc}\n" unless desc.empty?
    out << "\n---\n\n"
  end

  def self.render(site, post, payload)
    raw = File.read(post.path, encoding: "UTF-8")
    body = raw.sub(Jekyll::Document::YAML_FRONT_MATTER_REGEXP, "")
    page = post.to_liquid
    payload["page"] = page
    info = {
      registers: { site: site, page: page },
      strict_filters: site.config.dig("liquid", "strict_filters"),
      strict_variables: site.config.dig("liquid", "strict_variables"),
    }
    body = Jekyll::Renderer.new(site, post, payload).render_liquid(body, payload, info, post.path)
    base = site.config["url"].to_s.chomp("/")
    url = base + post.url
    body = diagrams_to_text(body, url)
    body = body.gsub(FeedDiagrams::VIDEO) do
      href, title = FeedDiagrams.video_link(Regexp.last_match(1))
      "Video: [#{title} on YouTube](#{href})"
    end
    body = body.gsub(IAL_LINE, "")
    body = absolutize(body, base)
    body = body.gsub(/\n{3,}/, "\n\n").strip
    header(post, url, post.date.strftime("%Y-%m-%d")) + body + "\n\n---\n\nOriginal post: #{url}\n"
  end

  def self.write_all(site)
    payload = site.site_payload
    count = 0
    site.posts.docs.each do |post|
      next unless post.write?
      begin
        dest = File.join(site.dest, md_path(post.url))
        FileUtils.mkdir_p(File.dirname(dest))
        File.write(dest, render(site, post, payload), encoding: "UTF-8")
        count += 1
      rescue StandardError => e
        Jekyll.logger.warn "PostMarkdown:", "#{post.relative_path}: #{e.class}: #{e.message}"
      end
    end
    Jekyll.logger.info "PostMarkdown:", "wrote #{count} Markdown copies"
  end

  module Filter
    # {{ page.url | markdown_url }} → /post/<slug>.md
    def markdown_url(url)
      PostMarkdown.md_path(url.to_s)
    end
  end
end

if defined?(Liquid::Template)
  Liquid::Template.register_filter(PostMarkdown::Filter)
end

if defined?(Jekyll::Hooks)
  Jekyll::Hooks.register :site, :post_write do |site|
    PostMarkdown.write_all(site)
  rescue StandardError => e
    Jekyll.logger.warn "PostMarkdown:", "skipped: #{e.class}: #{e.message}"
  end
end
