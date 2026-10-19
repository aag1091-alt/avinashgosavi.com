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
- [ ] Paper TL;DR candidates (read before writing): ~~MemGPT~~ (done Oct 19), Generative Agents memory stream (Park et al., 2023), RAG (Lewis et
      al., 2020), HNSW (Malkov & Yashunin, 2016), ColBERT (Khattab & Zaharia,
      2020), Lost in the Middle (Liu et al., 2023)
- [ ] Explainer: how VaultMem's three retrieval tiers work (from its README/posts)
- [ ] Explainer: how Drafting Desk keeps drafts private (from its README)
- [ ] Keep the agent memory glossary growing (/post/agent-memory-glossary/)

Designer:
- [ ] Project cards: consistent visual header (icon or tinted band per category)
- [ ] About page layout on mobile; 404 illustration

Engineer:
- [x] CI internal link check (done Oct 19, 6:35am PT — see below)
- [ ] CI link check: consider `--strict` (blocks deploy) after a week of zero-warning runs
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

## Done (Oct 18, 2026, 10:35pm PT)

- Glossary cross-links: VaultMem Part 1 & 3, Attractor and the Paper TL;DR hub now link to /post/agent-memory-glossary/ (it had zero inbound post links)
- Note: Oct 18 already has 8 PT-dated posts (manual session) — over the 4/day cap, so no new posts until Oct 19 PT.

Editor backlog additions:
- [ ] Glossary: add entries for RAG, MemGPT-style paging, re-ranking cross-encoder examples as their Paper TL;DRs land, and link back from each TL;DR

## Done (Oct 18, 2026, 11:35pm PT)

- Each of the 6 Paper TL;DR posts now ends with a line linking to the matching glossary section (#storing-and-finding-memories, #how-memories-change-over-time, #privacy, #measuring-it). Internal-link audit of all posts: no broken permalinks. Events/now checked: nothing past-dated yet (OSA Con Nov 2, HackUMass Nov 15).

Editor backlog additions:
- [ ] Glossary: give each bold term its own anchor id (e.g. `{: #recall-at-k}` or HTML spans) so TL;DRs can deep-link to a single term

## Done (Oct 19, 2026, 12:35am PT)

- CLS Paper TL;DR: inline SVG diagram (experience → hippocampus → replay → neocortex, with agent equivalents) via `_includes/diagrams/cls-two-learners.html`; styled by `.diagram` classes in style.css using theme tokens, so it follows sepia/dark. Contrast checked: text ≥10:1, muted ≥5.2:1 on box fill in sepia + dark; checked at 375px.

Designer backlog additions:
- [ ] Reuse `.diagram` for more posts: VaultMem retrieval tiers (from README), LoCoMo eval flow, Hopfield store/recall
- [ ] Old Attractor SVGs are hard-coded dark (#0f1117) — convert to theme-aware inline diagrams

## Done (Oct 19, 2026, 1:35am PT)

- Table of contents: posts with >= 1,200 words get a collapsible "On this page" box (h2 sections, needs >= 3) above the content; open by default at >= 700px, collapsed on phones. Opt out per post with `toc: false` in front matter. Markup in `_layouts/post.html`, built by JS in `_includes/post-tools.html`, styles `.post-toc` in style.css (theme tokens).

Engineer backlog additions:
- [ ] TOC: highlight the current section while scrolling (IntersectionObserver), if it stays tiny

## Done (Oct 19, 2026, 2:35am PT)

- Site-wide search: /search/ page (search.md, vanilla JS, ~120 lines) over /search.json (posts with first 8k chars of text, pages with titles, projects, papers, events). Weighted scoring (title > tags > description > text), all terms must match, highlighted snippets, ?q= shareable URLs. Header magnifier icon (`.header-search`), `/` shortcut on every page (focuses the page's search box, else opens /search/). Blog no-results and 404 link to it; llms.txt lists /search.json. CI step validates _site/search.json is JSON (fails build before deploy if broken). Contrast: mark text 9.0:1 sepia / 7.8:1 dark.

Engineer backlog additions:
- [ ] Search: include page body text (pages render after the index today, so only title+description are indexed) — maybe via a `search_text` front-matter field
- [ ] CI: Node 20 action deprecation warnings — bump actions/checkout, upload-pages-artifact, deploy-pages to current majors when available

## Done (Oct 19, 2026, 3:35am PT)

- Paper TL;DR #8: MemGPT (Packer et al., 2023) at /post/paper-tldr-memgpt/ — read from the arXiv PDF; neutral voice (no repo source ties it to his projects). Added to `_data/papers.yml` (no `why`). Glossary: new "Virtual context (paging)" entry under Kinds of memory linking to it. Post count Oct 19 PT: 1.
- Note: today is Monday — the weekly "This week in agent memory" roundup (beat c) is still open for a later editor shift today. arXiv abs pages needed a permission prompt in this unattended run; the arXiv PDF URL from a WebSearch result worked.

Editor backlog additions:
- [ ] Waiting on Avinash: has he used MemGPT/Letta or compared it to VaultMem? If so, a "what I took from it" line for the MemGPT TL;DR and a `why` in papers.yml

## Done (Oct 19, 2026, 4:35am PT)

- First weekly roundup (beat c): /post/this-week-in-agent-memory-2026-10-19/ — 7 arXiv papers submitted Oct 13–16 (Bemula unlearning benchmark, MemCut, QEMem, JointCore, TEM, multimodal memory survey, memory-centric compression survey), grouped by theme, each read from its arXiv abs page, neutral voice, links to glossary/LoCoMo/MemGPT posts. Tags Agent memory, Roundup, Research. Post count Oct 19 PT: 2.
- Source tip: WebSearch "arxiv.org/abs/2610 agent memory" surfaces this month's IDs; abs pages fetched fine this run. Check submission dates — many 2610.* hits were Oct 7–10 (outside the 7-day window).

Editor backlog additions:
- [ ] Paper TL;DR candidates from the roundup: Bemula (2610.18052) or MemCut (2610.21405) — ties to VaultMem's privacy theme only if his own posts support it; otherwise neutral
- [ ] Glossary: add "memory unlearning / forget requests" and "sufficient evidence" entries, linking the roundup
- [ ] Next roundup: Monday Oct 26 (cover Oct 19–25)

## Done (Oct 19, 2026, 5:35am PT)

- MemGPT Paper TL;DR: inline SVG diagram of main context (system instructions / working context / FIFO queue) vs external context (recall / archival), with eviction and function-call arrows — `_includes/diagrams/memgpt-virtual-context.html`, content taken only from the post. New `.dg-group` (dashed container) and `.dg-label` (small caps label) classes in style.css. Contrast: muted text 5.7:1 sepia / 5.2:1 dark on box fill; checked at 375px in both themes (Playwright needs `executablePath: '/opt/pw-browsers/chromium'`).

Designer backlog additions:
- [ ] Diagram for the weekly roundup? (probably not — keep roundups text-only); LoCoMo eval flow diagram next

## Done (Oct 19, 2026, 6:35am PT)

- CI internal link checker: `scripts/check_links.py` (stdlib only, offline) scans every href/src in `_site`, verifies on-site targets exist and that `#fragments` match a real id (or a `data-tag`, for `/blog/#tag` filter links). Runs in the workflow with `continue-on-error: true`, so it never blocks deploys; problems appear as ::warning annotations (`gh run view <id>` shows them) and as a full list in the job summary. Run locally: `python3 scripts/check_links.py _site [--strict]`. First run: 0 broken after allowing tag-filter hashes.
- Tip: `gh run view --log` and artifact downloads are Forbidden from the sandbox, but `gh run view <id>` (annotations) works.

## Run history

- 2026-10-18 — manual session: everything under "Done".
- 2026-10-18 evening — manual session: descriptions, computed read times, contrast fix.
- 2026-10-18 7:45pm PT — manual — changelog page + homepage strip; agent memory glossary post; team model set up.
- 2026-10-18 20:34 PT — ENGINEER — related posts by shared tags at the end of every post (live site not fetchable from sandbox; Actions deploy green).
- 2026-10-18 21:35 PT — ENGINEER — copy buttons on code blocks and heading anchor links in all posts (Actions deploy green).
- 2026-10-18 22:35 PT — EDITOR — glossary cross-links added to 4 posts (daily post cap already reached; Actions deploy green).
- 2026-10-18 23:35 PT — EDITOR — Paper TL;DRs link back to glossary sections; internal-link audit clean (post cap reached; Actions deploy green).
- 2026-10-19 00:35 PT — DESIGNER — theme-aware SVG diagram on /post/paper-tldr-complementary-learning-systems/ (Actions deploy green).
- 2026-10-19 01:35 PT — ENGINEER — "On this page" table of contents on posts over 1,200 words (Actions deploy green).
- 2026-10-19 02:35 PT — ENGINEER — site-wide search at /search/ with header icon and / shortcut (Actions deploy green).
- 2026-10-19 03:35 PT — EDITOR — Paper TL;DR on MemGPT (/post/paper-tldr-memgpt/) + glossary virtual-context entry (Actions deploy green).
- 2026-10-19 04:35 PT — EDITOR — weekly roundup "This week in agent memory" (/post/this-week-in-agent-memory-2026-10-19/) (Actions deploy green).
- 2026-10-19 05:35 PT — DESIGNER — theme-aware MemGPT memory-tiers diagram on /post/paper-tldr-memgpt/ (Actions deploy green).
- 2026-10-19 06:35 PT — ENGINEER — CI internal link + #fragment checker (warnings only; 0 broken links found; Actions deploy green).
