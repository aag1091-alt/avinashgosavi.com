---
layout: post
title: "Building Your Website with Jekyll and GitHub Pages"
permalink: /post/building-your-website-with-jekyll-and-github-pages/
read_time: 6
---

A static site on Jekyll + GitHub Pages is fast, free to host, and works great with an AI-assisted editor. This post assumes you're using something like Cursor, Codex, or Copilot to generate most of the code—so we'll focus on **what to ask for**, **what to configure**, and **where to read more** instead of typing everything by hand.

---

## What You Need

- **Ruby** (3.1+). Check with `ruby -v`. [rbenv](https://github.com/rbenv/rbenv) or [RubyInstaller](https://rubyinstaller.org/) if you need to install.
- **Git** and a **GitHub** account.
- **Bundler**: `gem install bundler` if you don’t have it.

Official intro: [Jekyll quick start](https://jekyllrb.com/docs/).

---

## 1. Scaffold the Site (Prompts That Work)

You don’t have to run `jekyll new` and then rip out the default theme. You can have your AI generate a minimal site from a short spec.

**Example prompts:**

- *"Create a minimal Jekyll 4 site: Gemfile, _config.yml, _layouts/default.html, index.md, and one blog post in _posts. Use kramdown and Rouge for code highlighting."*
- *"Add an About page and a blog listing page to my Jekyll site. Use Liquid and keep the same default layout."*

That gives you a repo with `_config.yml`, `_layouts`, `_includes`, `_posts`, and maybe `assets/css`. From there you can iterate with more specific prompts (e.g. "add a theme toggle", "add a CNAME for custom domain in the GitHub Actions workflow").

**Off-the-shelf alternative:** Use a theme. [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes), [Just the Docs](https://just-the-docs.github.io/just-the-docs/), and [Jekyll Themes](https://jekyllthemes.io/) are good starting points. Add the theme gem to your `Gemfile` and set `theme: minimal-mistakes` (or the theme name) in `_config.yml`. Your AI can then help you override specific layouts or add features.

---

## 2. Configuration You’ll Touch

**`_config.yml`** drives the site. Key bits:

| Setting | What it does |
|--------|----------------|
| `title`, `url` | Site name and canonical URL (e.g. `https://www.yoursite.com`). |
| `baseurl` | Leave `""` if you use a **custom domain** at the root. Set to `"/repo-name"` only if you’re on `username.github.io/repo-name` and want correct asset paths. |
| `permalink` | e.g. `permalink: /post/:title/` so posts live at `/post/my-post-title/`. |
| `markdown` | `kramdown` with `input: GFM` is a solid default. |
| `highlighter` | `rouge` for syntax highlighting in code blocks. |
| `plugins` | Common: `jekyll-sitemap`, `jekyll-feed`, `jekyll-seo-tag`. |

**Prompt idea:** *"In _config.yml add jekyll-sitemap, jekyll-feed, and jekyll-seo-tag to the plugins list and set permalink to /post/:title/."*

---

## 3. Themes and Styling

**Out of the box:** Jekyll doesn’t ship a “default theme” in the same way in Jekyll 4; you use a gem-based theme or your own CSS. Gem themes (e.g. Minimal Mistakes) give you a full look and many options; your AI can help you override a single layout or add a custom CSS variable.

**Custom look:** If you’re building your own (like a simple blog with one `assets/css/style.css`), you can ask for:

- *"Add CSS variables for background, text, accent, and border. Use them in the layout and in a dark/light theme class on body."*
- *"Add a theme toggle (e.g. sepia vs dark) that saves the choice in localStorage and applies a class to body."*

Rouge (syntax highlighting) uses classes like `.highlight .k`, `.highlight .s`—your AI can generate a small “Rouge theme” block in your CSS for light and dark backgrounds.

---

## 4. Content and Front Matter

Posts go in **`_posts/`** with names like `YYYY-MM-DD-slug.md`. Front matter drives the layout and URL:

```yaml
---
layout: post
title: "Your Post Title"
permalink: /post/your-custom-slug/   # optional; else from title/slug
read_time: 4
---
```

**Prompts:** *"Create a new Jekyll post for [topic] with front matter: layout post, title, and read_time."* or *"Add an excerpt to my post front matter and show it on the blog index."*

---

## 5. GitHub Pages: Get It Online

**Enable Pages:** Repo → **Settings** → **Pages**. Under “Build and deployment”, choose **GitHub Actions** (recommended).

**Build workflow:** You need a workflow that runs `bundle install` and `bundle exec jekyll build`, then uploads `_site` with `actions/upload-pages-artifact` and deploys with `actions/deploy-pages`. GitHub’s own “Jekyll” template under Actions is a good start; if you use a **custom domain at the root**, build **without** `--baseurl` so links and assets work (e.g. `run: bundle exec jekyll build`).

**Docs (use these instead of re-explaining everything):**

- [GitHub Pages: Configuring a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [Securing your GitHub Pages site with HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
- [Troubleshooting custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages)

**Custom domain in short:** Add your domain in Settings → Pages. In your DNS (e.g. GoDaddy), point **www** to your GitHub Pages hostname with a **CNAME** (e.g. `www` → `username.github.io`). For the apex (e.g. `yoursite.com`), use **A** records to GitHub’s IPs (see the docs). After DNS and verification, enable **Enforce HTTPS**.

---

## 6. What to Ask Your AI Next

- *"Add a sitemap and RSS feed to my Jekyll site using jekyll-sitemap and jekyll-feed."*
- *"Add client-side search that filters the post list by title and excerpt."*
- *"Generate a GitHub Actions workflow that builds my Jekyll site with Ruby 3.2 and deploys to GitHub Pages."*
- *"My links on the custom domain have a double path (e.g. /repo-name/post/...). Fix the build so baseurl is empty for the production build."*

---

## Summary

Use your AI to scaffold a minimal Jekyll site, then refine with prompts about config, themes, and content. Rely on **official Jekyll and GitHub docs** for deep dives; use this post as a map to *what* to configure and *what* to ask for so you spend less time on boilerplate and more on content and design.

**Further reading:** [Jekyll docs](https://jekyllrb.com/docs/), [GitHub Pages docs](https://docs.github.com/en/pages), [Liquid](https://shopify.github.io/liquid/).
