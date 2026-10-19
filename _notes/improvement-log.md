# Site improvement log

Working notes for the recurring "improve avinashgosavi.com" task. Not published
(Jekyll ignores folders starting with `_` that aren't collections).

## Ground rules (from Avinash)

- **Tone:** personal and curious, not resume-like. No resume metrics or stat
  cards ("1M+ devices", "30+ APIs") — they feel braggy on a personal site.
- **Never invent** opinions, experiences, attendance, awards or quotes. Only use
  facts from: this repo's existing posts/data, the resume in Google Drive
  (Avinash_Gosavi_Resume.pdf), Gmail ticket/registration emails, his public
  GitHub repos, and published papers/pages you actually read.
- **No current-work details:** don't describe what he is building at Cisco Meraki right now (he removed the "At work" Now item on Oct 18).
- **Privacy:** never publish health, finances, family, immigration, job-search
  or interview details, or anything from personal email beyond event tickets.
- **Small steps:** one focused change per commit, pushed to `main`; confirm the
  GitHub Actions deploy succeeds; fix immediately if it fails.
- Run `python3 scripts/og_cards.py` after adding a post (share-preview card).
- Validate YAML before pushing (`python3 -c "import yaml; yaml.safe_load(open(f))"`).
- Bigger content (new posts) must cite sources and stay factual; paper
  write-ups go in the `paper-tldr` series.

## Team model (since Oct 18, 2026, 7:40pm PT)

Avinash wants the site to feel like 10 editors, 5 designers and 10 engineers
work on it daily. The hourly scheduled task picks one role per run by UTC hour
(H mod 5: 0,1 Editor · 2 Designer · 3,4 Engineer). Every user-visible change
gets an entry at the top of `_data/changelog.yml` (shown on /changelog and the
homepage). Max 4 new posts/day, 1 per run.

## Done (Oct 18, 2026)

- New pages: /events, /achievements, /research (papershelf + newsletters),
  /talks, /now, /uses, /series, 404, robots.txt
- Blog series support; VaultMem series; Paper TL;DR series (7 posts covering
  Hopfield 1982, Modern Hopfield, CLS, LoCoMo, Memory as Asset, Sentence-BERT)
- Projects 6 → 11, grouped by theme, demo links
- Experience updated from Oct 2026 resume
- Tags + filter chips on /blog; read-next links; share cards for all posts;
  Person JSON-LD; SEO fixes (duplicate title/description); image compression,
  lazy-loading; skip link; README documents data files

## Backlog (pick from the top; move to Done with a date)

Editor:
- [ ] Paper TL;DR candidates (read before writing): MemGPT (Packer et al.,
      2023), Generative Agents memory stream (Park et al., 2023), RAG (Lewis et
      al., 2020), HNSW (Malkov & Yashunin, 2016), ColBERT (Khattab & Zaharia,
      2020), Lost in the Middle (Liu et al., 2023)
- [ ] Explainer: how VaultMem's three retrieval tiers work (from its README/posts)
- [ ] Explainer: how Drafting Desk keeps drafts private (from its README)
- [ ] Keep the agent memory glossary growing (/post/agent-memory-glossary/)

Designer:
- [ ] Simple SVG diagram for the CLS post (fast store → replay → slow store)
- [ ] Project cards: consistent visual header (icon or tinted band per category)
- [ ] About page layout on mobile; 404 illustration

Engineer:
- [ ] Table of contents for posts longer than ~1,200 words
- [ ] Site-wide search (JSON index of posts + pages)
- [ ] CI: html-proofer for internal links only (don't fail on external links)
- [ ] Related posts: tag series posts so they don't crowd out non-series matches (maybe exclude same-series posts since the series box already lists them)

General:

- [ ] Projects: short "what I learned" line per project — ONLY from facts in
      the project's own post/README
- [ ] Events: link any other event to a recap if a post exists
- [ ] Waiting on Avinash: favorite talks beyond SF Ruby, podcasts/YouTube,
      books, next papers to read (then add to /talks, a bookshelf, Paper TL;DR)
- [ ] Waiting on Avinash: LinkedIn post for the Paper TL;DR series (draft
      ready in chat; never post without his OK)

## Done (Oct 18, 2026, evening)

- Search descriptions on all 16 older posts
- Read times now computed from word count (`_includes/read-time.html`);
  front-matter `read_time` is ignored
- Alt text audit: no images missing alt
- Dark-theme contrast audit: fixed active topic chip (was 2.0:1, now 7.4:1)

## AI-agent discoverability (Oct 18, 2026)

- robots.txt explicitly allows AI search/training crawlers; /llms.txt index
  and /llms-full.txt (all post text) generated from site data — keep them
  working when adding pages (add new top-level pages to llms.txt "Pages").
- jekyll-seo-tag already emits BlogPosting JSON-LD on posts; homepage has
  Person JSON-LD.
- Waiting on Avinash: verify the site in Google Search Console and Bing
  Webmaster Tools and submit /sitemap.xml (Bing's index feeds several AI
  search products).

## Done (Oct 18, 2026, night)

- Related posts: up to 3 per post ranked by shared tags (ties → newer), shown
  above "Keep reading", skipping the newer/older links (`_includes/read-next.html`)

## Done (Oct 18, 2026, 9:35pm PT)

- Copy buttons on post code blocks + `#` anchor links on h2/h3 (`_includes/post-tools.html`, loaded only by the post layout)

Engineer backlog additions:
- [ ] Extend anchors/copy buttons to non-post pages (/uses, /research) if they get long sections or code

## Run history

- 2026-10-18 — manual session: everything under "Done".
- 2026-10-18 evening — manual session: descriptions, computed read times, contrast fix.
- 2026-10-18 7:45pm PT — manual — changelog page + homepage strip; agent memory glossary post; team model set up.
- 2026-10-18 20:34 PT — ENGINEER — related posts by shared tags at the end of every post (live site not fetchable from sandbox; Actions deploy green).
- 2026-10-18 21:35 PT — ENGINEER — copy buttons on code blocks and heading anchor links in all posts (Actions deploy green).
