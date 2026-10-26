# frozen_string_literal: true

# Shrinks the built stylesheet(s) in _site/assets/css after every build:
# comments go, whitespace runs collapse, and spaces around { } ; , are
# dropped. Quoted strings (content: "\2197" / "", font names...) are copied
# byte-for-byte, so nothing inside quotes is ever touched. The source file in
# assets/css stays readable and commented; only the deployed copy is small
# (~35% fewer gzipped bytes of render-blocking CSS).
#
# `asset_version` hashes this minified output, so ?v= matches the served bytes. Set CSS_MINIFY=0 to skip (local debugging).

module CssMinify
  TOKEN = %r{(/\*.*?\*/)|("(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*')|([^"'/]+|.)}m

  def self.squeeze(chunk)
    chunk.gsub(/\s+/, " ").gsub(/\s*([{};,])\s*/, '\1').gsub(";}", "}")
  end

  def self.minify(css)
    out = +""
    buf = +""
    css.scan(TOKEN) do |comment, string, other|
      if comment
        buf << " "
      elsif string
        out << squeeze(buf) << string
        buf = +""
      else
        buf << other
      end
    end
    out << squeeze(buf)
    out.strip << "\n"
  end
end

Jekyll::Hooks.register :site, :post_write do |site|
  next if ENV["CSS_MINIFY"] == "0"

  Dir.glob(File.join(site.dest, "assets", "css", "*.css")).each do |path|
    css = File.read(path, encoding: "utf-8")
    min = CssMinify.minify(css)
    File.write(path, min) if min.bytesize < css.bytesize
  end
end
