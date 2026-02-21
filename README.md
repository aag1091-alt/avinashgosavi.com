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
