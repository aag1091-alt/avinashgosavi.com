# frozen_string_literal: true

# Adds Google image-sitemap entries to /sitemap.xml so photos and screenshots
# in posts and pages (SF Ruby, VaultMem, Rena, the about photo, ...) can be
# found by image search. jekyll-sitemap writes the file; after the whole site
# is written, this reads each <url>'s built HTML, collects the <img src>
# inside <main> (skipping SVG, data: URIs and other hosts), and appends
# <image:image><image:loc>...</image:loc></image:image> to that <url>.
# https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps
# Any error only warns — it must never block a deploy.
module SitemapImages
  NS = 'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'
  MAX_PER_URL = 1000 # Google's limit per <url>

  def self.esc(str)
    str.gsub("&", "&amp;").gsub("<", "&lt;").gsub(">", "&gt;").gsub('"', "&quot;").gsub("'", "&apos;")
  end

  def self.unesc(str)
    str.gsub("&quot;", '"').gsub("&apos;", "'").gsub("&#39;", "'").gsub("&lt;", "<").gsub("&gt;", ">").gsub("&amp;", "&")
  end

  # Built file for a sitemap <loc> (absolute URL), or nil.
  def self.html_file(dest, root, loc)
    return nil unless loc.start_with?(root)

    path = loc[root.length..].to_s.split(/[?#]/).first.to_s
    path = "/#{path}" unless path.start_with?("/")
    path += "index.html" if path.end_with?("/")
    file = File.join(dest, path)
    file.end_with?(".html") && File.file?(file) ? file : nil
  end

  # Absolute same-site raster image URLs from <img src> inside <main>.
  def self.images(html, root, host_root)
    main = html[%r{<main\b.*?</main>}m] or return []
    main.scan(/<img\b[^>]*?\ssrc=["']([^"']+)["']/i).flatten.filter_map do |src|
      src = unesc(src.strip)
      next if src.empty? || src.start_with?("data:")
      url =
        if src.start_with?("//") then "https:#{src}"
        elsif src.start_with?("/") then host_root + src
        elsif src =~ %r{\Ahttps?://} then src
        end
      next unless url&.start_with?(root)
      next if url.split(/[?#]/).first =~ /\.svg\z/i

      url
    end.uniq.first(MAX_PER_URL)
  end

  def self.process(site)
    file = File.join(site.dest, "sitemap.xml")
    return unless File.file?(file)

    host_root = site.config["url"].to_s.chomp("/")
    root = host_root + site.config["baseurl"].to_s.chomp("/")
    return if host_root.empty?

    xml = File.read(file)
    count = 0
    pages = 0
    out = xml.gsub(%r{<url>(.*?)</url>}m) do
      body = Regexp.last_match(1)
      loc = body[%r{<loc>\s*(.*?)\s*</loc>}m, 1]
      src = loc && html_file(site.dest, root, unesc(loc))
      imgs = src ? images(File.read(src), root, host_root) : []
      next "<url>#{body}</url>" if imgs.empty? || body.include?("<image:image>")

      pages += 1
      count += imgs.size
      tags = imgs.map { |u| "<image:image><image:loc>#{esc(u)}</image:loc></image:image>" }.join("\n")
      "<url>#{body.rstrip}\n#{tags}\n</url>"
    end
    return if count.zero?

    out = out.sub(/<urlset\b([^>]*)>/) { |tag| tag.include?("xmlns:image") ? tag : "<urlset#{Regexp.last_match(1)} #{NS}>" }
    File.write(file, out)
    Jekyll.logger.info "Sitemap images:", "#{count} image(s) on #{pages} page(s)"
  rescue StandardError => e
    Jekyll.logger.warn "Sitemap images:", "skipped (#{e.class}: #{e.message})"
  end
end

Jekyll::Hooks.register :site, :post_write do |site|
  SitemapImages.process(site)
end
