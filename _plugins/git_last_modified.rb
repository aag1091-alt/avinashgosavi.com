# frozen_string_literal: true

# Sets `last_modified_at` on posts and pages from the last git commit that
# touched the file, so the sitemap gets real <lastmod> dates and post
# BlogPosting JSON-LD gets a dateModified. A value set in front matter wins.
# Does nothing when git history is unavailable (e.g. a plain download).
#
# CI needs the full history: actions/checkout uses `fetch-depth: 0`.

require "open3"
require "time"

module GitLastModified
  def self.dates(site)
    out, status = Open3.capture2(
      "git", "log", "--format=@@%cI", "--name-only", "--no-renames", "HEAD",
      chdir: site.source
    )
    return {} unless status.success?

    dates = {}
    current = nil
    out.each_line do |line|
      line = line.strip
      next if line.empty?

      if line.start_with?("@@")
        current = Time.iso8601(line.delete_prefix("@@"))
      elsif current
        dates[line] ||= current # newest commit comes first
      end
    end
    dates
  rescue StandardError => e
    Jekyll.logger.warn "git_last_modified:", e.message
    {}
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  dates = GitLastModified.dates(site)
  next if dates.empty?

  items = site.posts.docs + site.pages.select { |p| p.html? || p.ext == ".md" }
  set = 0
  items.each do |item|
    next if item.data["last_modified_at"]

    rel = item.relative_path.sub(%r{\A/}, "")
    git_time = dates[rel]
    next unless git_time

    # Only record a modification that happened after publishing.
    published = item.data["date"]
    next if published && git_time.to_date <= published.to_date

    item.data["last_modified_at"] = git_time
    set += 1
  end
  Jekyll.logger.info "git_last_modified:", "#{set} pages/posts dated from git"
end
