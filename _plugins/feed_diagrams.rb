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

  def self.inner(html, tag)
    m = html.match(%r{<#{tag}\b[^>]*>(.*?)</#{tag}>}m)
    m && m[1].strip.gsub(/\s+/, " ")
  end

  def self.replace(html, url = nil)
    return html unless html.is_a?(String) && html.include?('<figure class="diagram"')

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

  # Same swap inside jekyll-feed's Atom output, where post HTML is escaped
  # inside <content type="html">. The post URL comes from the entry's
  # rel="alternate" link.
  def self.rewrite_atom(xml)
    return xml unless xml.include?("figure class=&quot;diagram&quot;")

    xml.gsub(%r{<entry>.*?</entry>}m) do |entry|
      next entry unless entry.include?("figure class=&quot;diagram&quot;")

      url = entry[/<link href="([^"]+)" rel="alternate"/, 1]
      entry.sub(%r{(<content type="html"[^>]*>)(.*?)(</content>)}m) do
        open_tag, body, close_tag = Regexp.last_match(1), Regexp.last_match(2), Regexp.last_match(3)
        open_tag + CGI.escapeHTML(replace(CGI.unescapeHTML(body), url && CGI.unescapeHTML(url))) + close_tag
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
