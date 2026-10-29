# frozen_string_literal: true

# Feed readers and plain-text copies can't use the site's inline SVG diagrams:
# their colours come from style.css classes (dg-box, dg-line...), so in a
# reader they render as solid black shapes, and strip_html turns them into a
# jumble of box labels. For feeds and llms-full.txt each
# <figure class="diagram"> is swapped for its text alternative: the SVG's
# <title> and <desc>, the visible caption, and a link to the post.
#
#   {{ post.content | feed_diagrams: post_url }}   (feed.json, series feeds, llms-full.txt)
#   /feed.xml (made by jekyll-feed) is rewritten by the post_render hook below.

require "cgi"

module FeedDiagrams
  FIGURE = %r{<figure class="diagram"[^>]*>(.*?)</figure>}m
  # Click-to-load video facades (<div class="video-embed"><a class="video-play">
  # with a play-icon SVG) become a plain link: readers can't run the swap script
  # and would show a bare black circle.
  VIDEO = %r{<div class="video-embed">\s*(<a class="video-play"[^>]*>).*?</a>\s*</div>}m

  def self.video_link(tag)
    href = tag[/\bhref="([^"]+)"/, 1].to_s
    title = CGI.unescapeHTML(tag[/\bdata-title="([^"]*)"/, 1] || "demo")
    [href, title]
  end

  def self.videos(html)
    return html unless html.include?('class="video-play"')

    html.gsub(VIDEO) do
      href, title = video_link(Regexp.last_match(1))
      %(<p><a href="#{href}">Video: #{CGI.escapeHTML(title)} on YouTube</a></p>)
    end
  end

  def self.inner(html, tag)
    m = html.match(%r{<#{tag}\b[^>]*>(.*?)</#{tag}>}m)
    m && m[1].strip.gsub(/\s+/, " ")
  end

  def self.replace(html, url = nil)
    return html unless html.is_a?(String)

    html = videos(html)
    return html unless html.include?('<figure class="diagram"')

    html.gsub(FIGURE) do
      fig = Regexp.last_match(1)
      title = inner(fig, "title") || "Diagram"
      desc = inner(fig, "desc")
      caption = inner(fig, "figcaption")
      link = url.to_s.empty? ? "" : %( (<a href="#{CGI.escapeHTML(url.to_s)}">see it in the post</a>))
      out = +%(<blockquote class="diagram-text"><p><strong>Diagram: #{title}</strong>#{link}</p>)
      out << "<p>#{desc}</p>" if desc && !desc.empty?
      out << "<p><em>#{caption}</em></p>" if caption && !caption.empty?
      out << "</blockquote>"
    end
  end

  # Same swap inside jekyll-feed's Atom output, where post HTML sits inside
  # <content type="html"> either as CDATA (jekyll-feed 0.17) or escaped. The
  # post URL comes from the entry's rel="alternate" link.
  def self.rewrite_atom(xml)
    return xml unless %w[diagram video-play].any? { |k| xml.include?(%(class="#{k}")) || xml.include?("class=&quot;#{k}&quot;") }

    xml.gsub(%r{<entry\b[^>]*>.*?</entry>}m) do |entry|
      url = entry[/<link href="([^"]+)" rel="alternate"/, 1]
      url &&= CGI.unescapeHTML(url)
      entry.sub(%r{(<content type="html"[^>]*>)(.*?)(</content>)}m) do
        open_tag, body, close_tag = Regexp.last_match(1), Regexp.last_match(2), Regexp.last_match(3)
        cdata = body.match(/\A\s*<!\[CDATA\[(.*)\]\]>\s*\z/m)
        body =
          if cdata
            "<![CDATA[#{replace(cdata[1], url)}]]>"
          elsif body.include?("figure class=&quot;diagram&quot;") || body.include?("class=&quot;video-play&quot;")
            CGI.escapeHTML(replace(CGI.unescapeHTML(body), url))
          else
            body
          end
        open_tag + body + close_tag
      end
    end
  end

  module Filter
    def feed_diagrams(input, url = nil)
      FeedDiagrams.replace(input, url)
    end
  end
end

if defined?(Liquid::Template)
  Liquid::Template.register_filter(FeedDiagrams::Filter)
end

if defined?(Jekyll::Hooks)
  Jekyll::Hooks.register :pages, :post_render do |page|
    page.output = FeedDiagrams.rewrite_atom(page.output) if page.url == "/feed.xml"
  end
end
