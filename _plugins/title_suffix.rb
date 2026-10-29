# frozen_string_literal: true

require "cgi"

# jekyll-seo-tag writes <title>Page title | Avinash Gosavi</title>. Search
# results cut titles off at roughly 60 characters, so on long post titles the
# site name only pushed the post's own words out of view ("…Temporal Search,
# and Pl…"). When the full title is longer than `title_max` (_config.yml),
# the " | site" suffix is dropped and the page's own title stands alone.
# og:title / twitter:title never had the suffix, so share cards are unchanged.
module TitleSuffix
  TITLE = %r{<title>(.*?)</title>}m

  def self.trim(html, site_title, max)
    suffix = " | #{CGI.escapeHTML(site_title)}"
    head_end = html.index("</head>") || html.length
    m = TITLE.match(html)
    return html unless m && m.begin(0) < head_end

    full = m[1]
    return html unless full.end_with?(suffix) && CGI.unescapeHTML(full).length > max

    html.sub(TITLE) { "<title>#{full.delete_suffix(suffix)}</title>" }
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  next unless doc.output_ext == ".html" && doc.output.is_a?(String)

  site = doc.site
  max = site.config["title_max"]
  next unless max && site.config["title"]

  doc.output = TitleSuffix.trim(doc.output, site.config["title"].to_s, max.to_i)
end
