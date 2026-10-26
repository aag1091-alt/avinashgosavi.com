# frozen_string_literal: true

# Sets `last_modified_at` on posts and pages from the last git commit that
# touched the file, so the sitemap gets real <lastmod> dates and post
# BlogPosting JSON-LD gets a dateModified. A value set in front matter wins.
# Does nothing when git history is unavailable (e.g. a plain download).
#
# Pages built from `_data/` (/, /now/, /events/, /changelog/, …) change when
# their data file does, not their own source, so a page takes the newest git
# date of the page file and every `_data/<name>.yml` it reads via
# `site.data.<name>` — in its own source, its layout chain (except the
# site-wide `default` layout) and the includes those reference.
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

  DATA_REF = /site\.data\.([A-Za-z0-9_]+)/
  INCLUDE_REF = /\{%-?\s*include\s+([\w.\/-]+\.html)/

  # Names of the _data files a page reads (one include level deep).
  def self.data_refs(site, page)
    texts = [page.content.to_s]
    layout = site.layouts[page.data["layout"].to_s]
    seen = {}
    while layout && !seen[layout.name]
      seen[layout.name] = true
      texts << layout.content.to_s unless layout.name == "default"
      layout = site.layouts[layout.data["layout"].to_s]
    end
    includes = texts.flat_map { |t| t.scan(INCLUDE_REF).flatten }.uniq
    includes.each do |inc|
      path = File.join(site.source, "_includes", inc)
      texts << File.read(path, encoding: "UTF-8") if File.file?(path)
    end
    texts.flat_map { |t| t.scan(DATA_REF).flatten }.uniq
  end

  def self.data_time(site, page, dates)
    data_refs(site, page).filter_map do |name|
      %w[yml yaml json csv].filter_map { |ext| dates["_data/#{name}.#{ext}"] }.max
    end.max
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
    unless item.is_a?(Jekyll::Document) # pages only: posts keep their own date
      data_time = GitLastModified.data_time(site, item, dates)
      git_time = [git_time, data_time].compact.max
    end
    next unless git_time

    # Only record a modification that happened after publishing.
    published = item.data["date"]
    next if published && git_time.to_date <= published.to_date

    item.data["last_modified_at"] = git_time
    set += 1
  end
  Jekyll.logger.info "git_last_modified:", "#{set} pages/posts dated from git"
end
