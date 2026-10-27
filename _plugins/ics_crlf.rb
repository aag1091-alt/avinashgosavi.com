# frozen_string_literal: true

# iCalendar (RFC 5545) wants CRLF line endings and content lines of at most 75
# octets (longer ones folded: CRLF + one space). Liquid output has neither, so
# every generated .ics page (e.g. /events.ics) is fixed up here before write.
module IcsFormat
  def self.fold(line)
    out = +""
    len = 0
    limit = 75 # first segment; continuations start with a space, so 74 more
    line.each_char do |ch|
      if len + ch.bytesize > limit && len.positive?
        out << "\r\n "
        len = 0
        limit = 74
      end
      out << ch
      len += ch.bytesize
    end
    out
  end

  def self.format(text)
    lines = text.split(/\r?\n/).reject { |l| l.strip.empty? }
    lines.map { |l| fold(l) }.join("\r\n") + "\r\n"
  end
end

Jekyll::Hooks.register :pages, :post_render do |page|
  next unless page.url.to_s.end_with?(".ics")

  page.output = IcsFormat.format(page.output)
end
