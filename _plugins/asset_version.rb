# frozen_string_literal: true

# Cache-busting for static assets: `{{ '/assets/css/style.css' | asset_version }}`
# returns "/assets/css/style.css?v=<first 10 hex of the file's MD5>". The
# version only changes when the file's bytes change, so returning visitors get
# fresh CSS right after a deploy instead of a stale cached copy (GitHub Pages
# serves assets with a 10-minute max-age), and keep their cache otherwise.
# Pipe through `relative_url` afterwards. Missing files are returned unchanged.

require "digest"

module AssetVersion
  CACHE = {}

  def asset_version(path)
    site = @context.registers[:site]
    file = File.join(site.source, path.to_s.sub(%r{\A/}, ""))
    return path unless File.file?(file)

    key = [file, File.mtime(file).to_f]
    CACHE[key] ||= Digest::MD5.file(file).hexdigest[0, 10]
    "#{path}?v=#{CACHE[key]}"
  end
end

Liquid::Template.register_filter(AssetVersion)
