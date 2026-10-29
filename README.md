# Avinash Gosavi – Jekyll Blog

A Jekyll version of [avinashgosavi.com](https://www.avinashgosavi.com/) with the same structure (Home, About, More → All Posts, Search) and your existing content. UI is a new dark theme with code highlighting.

## Run locally

```bash
bundle install
bundle exec jekyll serve
```

Open <http://localhost:4000>.

## Build for production

```bash
bundle exec jekyll build
```

Output is in `_site/`. Deploy that folder to GitHub Pages, Netlify, Vercel, or any static host.

After each deploy, the workflow's `indexnow` job sends the pages whose sitemap
`<lastmod>` changed to IndexNow (Bing, Yandex, Seznam, Naver) via
`scripts/indexnow.py`. The root file `cd4471ebd9b322f9b4bc4d7adab382c5.txt` is
the IndexNow ownership key — keep it, or submissions are rejected.

## Structure

- **Home** (`/`) – Hero + recent posts
- **About** (`/about`) – About page
- **More** (dropdown) – All Posts, Search
- **All Posts** (`/blog`) – Full post list + client-side search
- **Posts** – Under `/post/:title/` with author, date, read time

Code blocks use Jekyll’s built-in Rouge highlighter (configured in `_config.yml`). Edit `assets/css/style.css` to change the look; Rouge token classes are at the bottom of the CSS file.

## Themes

**Visitor toggle:** The header has a **Theme** control (Sepia | Dark). The choice is saved in the browser (`localStorage`) so it persists across pages and visits. Default for new visitors is set in `_config.yml` (`color_theme: sepia` or `dark`). Don't use the top-level `theme:` key—that's for Jekyll gem themes.

Restart `jekyll serve` after changing `color_theme` in the config.

## Add a new post

Create a file in `_posts/` with the format `YYYY-MM-DD-slug.md` and frontmatter:

```yaml
---
layout: post
title: "Your title"
read_time: 3
---
```

Then write in Markdown. Code fences get syntax highlighting automatically.

## Content you can update without touching layouts

Most pages are driven by YAML files in `_data/`. Edit the file, push, and the page updates.

| Page | File | Notes |
| --- | --- | --- |
| `/projects` and homepage cards | `_data/projects.yml` | `category` groups cards; `featured: true` puts it on the homepage (first 4); `demo`, `post`, `github` add links |
| `/experience` and homepage list | `_data/experience.yml` | One entry per company, `roles` with `highlights` |
| `/events` | `_data/events.yml` | `role`: attended / hacker / judge / mentor / speaker; `status`: upcoming / past; optional `recap` post URL; optional `end_date` (last day) shows a "Happening now" tag while the event runs; an `upcoming` event moves under Past by itself the day after it ends (still flip `status` to `past` — CI warns after 3 days) |
| `/achievements` | `_data/achievements.yml` | Grouped by `section`; items take `title`, `year`, `detail`, `links` |
| `/research` papershelf | `_data/papers.yml` | `tldr`, `why`, `post` (related project post), `tldr_post` (full Paper TL;DR write-up) |
| `/talks` | `_data/talks.yml` | `take` is a one-line reason to watch, grouped by `topic` |
| `/now` and homepage Now | `_data/now.yml` | Bump `updated` when you edit; first 4 items show on the homepage; optional `until: YYYY-MM-DD` hides a dated item the day after |
| `/series` | `_data/series.yml` | Define a series slug, then add `series: <slug>` and `series_order: <n>` to posts |

Hand-written pages: `about.md`, `research.md` (topics + newsletters), `uses.md`.

## Posts

Front matter used by the layouts:

```yaml
title: "..."
permalink: /post/my-slug/
description: "One sentence for search results and share previews"
tags: ["Agent memory", "Research"]   # drives the filter chips on /blog
series: paper-tldr                    # optional
series_order: 3                       # optional
image: /assets/og/my-slug.png         # share-preview image
read_time: 5
```

Generate share-preview cards for any post without an `image:` (needs Pillow):

```bash
python3 scripts/og_cards.py
```

`_plugins/git_last_modified.rb` sets `last_modified_at` from each file's last
git commit (sitemap `<lastmod>`, post `dateModified`); a `last_modified_at`
in front matter overrides it. Pages that read `site.data.<name>` (in their
source, non-default layout or includes) also count the last commit to that
`_data/` file, so / and /changelog/ get a fresh `<lastmod>` (and an IndexNow
ping) when the changelog grows. CI checks out full history for this.

`_plugins/post_markdown.rb` writes a plain Markdown copy of every post at
`/post/<slug>.md` after the build (Liquid rendered, diagrams as text, links
absolute). Linked from each post's head, its share row and /llms.txt.

`_plugins/title_suffix.rb` drops the " | Avinash Gosavi" suffix from `<title>`
when the full title would be longer than `title_max` (65) in `_config.yml`,
so long post titles aren't cut off mid-word in search results.
