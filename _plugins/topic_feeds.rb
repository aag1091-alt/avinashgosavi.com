# frozen_string_literal: true

# One Atom feed per blog topic (post tag) that has at least `topic_feed_min`
# posts (_config.yml, default 2):
# /feed/topic/<slug>.xml, rendered by _layouts/topic-feed.html. Lets a reader
# follow just "Agent memory" or "Privacy" instead of every post.
#
# The slug is Jekyll's default slugify, the same as `{{ tag | slugify }}` in
# blog.md, which links the feed from the active topic chip on /blog/.
# blog.md reads the same `site.topic_feed_min`, so chips and feeds agree.

module TopicFeeds
  DEFAULT_MIN_POSTS = 2

  class Generator < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      min_posts = (site.config["topic_feed_min"] || DEFAULT_MIN_POSTS).to_i
      counts = Hash.new(0)
      site.posts.docs.each { |p| Array(p.data["tags"]).each { |t| counts[t.to_s] += 1 } }
      counts.each do |tag, n|
        next if n < min_posts || tag.strip.empty?

        slug = Jekyll::Utils.slugify(tag)
        page = Jekyll::PageWithoutAFile.new(site, site.source, "feed/topic", "#{slug}.xml")
        page.content = ""
        page.data["layout"] = "topic-feed"
        page.data["tag"] = tag
        page.data["tag_slug"] = slug
        page.data["sitemap"] = false
        page.data["permalink"] = "/feed/topic/#{slug}.xml"
        site.pages << page
      end
    rescue StandardError => e
      Jekyll.logger.warn "TopicFeeds:", "skipped (#{e.message})"
    end
  end
end
