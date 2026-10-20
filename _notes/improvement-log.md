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
- [ ] Paper TL;DR candidates (read before writing): ~~MemGPT~~ (done Oct 19), ~~Generative Agents~~ (done Oct 19, 2:35pm PT), RAG (Lewis et
      al., 2020), HNSW (Malkov & Yashunin, 2016), ColBERT (Khattab & Zaharia,
      2020), Lost in the Middle (Liu et al., 2023)
- [ ] Explainer: how VaultMem's three retrieval tiers work (from its README/posts)
- [x] Explainer: how Drafting Desk keeps drafts private (done Oct 19, 8:35am PT)
- [ ] Keep the agent memory glossary growing (/post/agent-memory-glossary/)

Designer:
- [ ] Project cards: consistent visual header (icon or tinted band per category)
- [ ] About page layout on mobile (404 illustration done Oct 19, 7:35pm PT)

Engineer:
- [x] CI internal link check (done Oct 19, 6:35am PT — see below)
- [ ] CI link check: consider `--strict` (blocks deploy) after a week of zero-warning runs
- [x] Related posts: exclude same-series posts (done Oct 19, 11:35am PT)

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
- [ ] Reuse `.diagram` for more posts: ~~VaultMem retrieval tiers~~ (done Oct 19, 10:35am PT), LoCoMo eval flow, Hopfield store/recall
- [ ] Old Attractor SVGs are hard-coded dark (#0f1117) — convert to theme-aware inline diagrams

## Done (Oct 19, 2026, 1:35am PT)

- Table of contents: posts with >= 1,200 words get a collapsible "On this page" box (h2 sections, needs >= 3) above the content; open by default at >= 700px, collapsed on phones. Opt out per post with `toc: false` in front matter. Markup in `_layouts/post.html`, built by JS in `_includes/post-tools.html`, styles `.post-toc` in style.css (theme tokens).

Engineer backlog additions:
- [x] TOC: highlight the current section while scrolling (done Oct 19, 12:35pm PT)

## Done (Oct 19, 2026, 2:35am PT)

- Site-wide search: /search/ page (search.md, vanilla JS, ~120 lines) over /search.json (posts with first 8k chars of text, pages with titles, projects, papers, events). Weighted scoring (title > tags > description > text), all terms must match, highlighted snippets, ?q= shareable URLs. Header magnifier icon (`.header-search`), `/` shortcut on every page (focuses the page's search box, else opens /search/). Blog no-results and 404 link to it; llms.txt lists /search.json. CI step validates _site/search.json is JSON (fails build before deploy if broken). Contrast: mark text 9.0:1 sepia / 7.8:1 dark.

Engineer backlog additions:
- [x] Search: include page body text (done Oct 19, 7:35am PT)
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

## Done (Oct 19, 2026, 7:35am PT)

- Search indexes page body text: `scripts/enrich_search_index.py` (stdlib, offline) runs in CI right after `jekyll build`, reads each Page entry's built HTML, takes the visible text inside `<main>` (skips script/style/svg/button), and writes up to 8k chars into `_site/search.json`. `continue-on-error: true` and atomic rewrite, so a failure just leaves the old title+description index. Missing pages show as ::warning annotations (none on first run). Step tip: `gh api repos/aag1091-alt/avinashgosavi.com/actions/jobs/<job id> --jq '.steps[]'` shows per-step conclusions (continue-on-error hides failures from the run summary).

Engineer backlog additions:
- [ ] Search: index project/paper/event entries' own anchors (e.g. /projects/#vaultmem) once those cards get ids
- [ ] CI: ubuntu-latest moves to Ubuntu 26 from Oct 19 — watch the next runs for python3/ruby breakage

## Done (Oct 19, 2026, 8:35am PT)

- Explainer (beat b): /post/drafting-desk-how-it-keeps-drafts-private/ — no server, localStorage posts, keys in sessionStorage unless "remember", OpenRouter PKCE, CSP, assistant sends only selected text, "never writes for you" prompt rules, honest caveats (plain-JSON storage, CSP allows any https: for custom servers). Sourced only from the drafting-desk README and source (cloned publicly; GitHub MCP can't read it, `git clone` works). Projects card now links the post; /now "Building" item links it (updated bumped). Post count Oct 19 PT: 3.
- Skipped the VaultMem tiers explainer: Part 1 already has a "Three-tier retrieval" section — a diagram (designer) would add more than a new post.

Editor backlog additions:
- [ ] Explainers for other projects without a post (VideoOnly Browser, What's New in AI) — read their READMEs first
- [ ] Waiting on Avinash: why he built Drafting Desk / how he uses it — a first-person intro paragraph for the post

## Done (Oct 19, 2026, 9:35am PT)

- Glossary (beat e): two new entries — "Sufficient evidence" (Storing and finding; source: Beyond Marginal Influence on neurips.cc) and "Memory unlearning (forget requests)" (Privacy; source: Bemula on emergentmind.com) — each deep-links the matching theme of the Oct 19 roundup (anchors verified by CI link check). Title dropped the stale "20 Terms" count (now 24) and its share card regenerated. No new post (Oct 19 PT count stays 3).
- Confirmed: previous shift's runs finished — 39282542875 green (39280359141 cancelled by concurrency; superseded).
- Source tip: arXiv abs URLs need permission in unattended runs (withdrawn). Search for the title and fetch emergentmind.com/papers/<id> or the neurips.cc virtual page instead.

Editor backlog additions:
- [ ] Glossary: "versioned facts / temporal state" entry from TEM (2610.21900) — couldn't open a source this run

## Done (Oct 19, 2026, 10:35am PT)

- VaultMem Part 1 (/post/vaultmem-encrypted-memory-for-ai-agents/): inline SVG of three-tier retrieval (query → AFFINITY/COMPOSITE/ATOM in order → global re-rank on cosine + significance → flat cosine vs three-tier top results for the coffee-habit decoy) — `_includes/diagrams/vaultmem-three-tier.html`, content only from the post's own section. New `.dg-muted` class (muted dashed stroke) for "comparison" boxes. Contrast: muted text on `.dg-pill` is only 3.7:1 in dark, so pill subtitles use `.dg-body` (7.8:1) — keep `.dg-note` off pills. Checked at 375px in sepia + dark, no horizontal scroll.

Designer backlog additions:
- [ ] Remaining diagram ideas: LoCoMo eval flow, Hopfield store/recall, VaultMem envelope encryption (MEK wrapping) from Part 1's "How the encryption works"

## Done (Oct 19, 2026, 11:35am PT)

- Related posts (`_includes/read-next.html`) now skip posts in the same `series` as the current post — the series box already lists them, so Paper TL;DRs/VaultMem parts surface glossary, roundup and other posts instead.
- Layout shift: explicit width/height on all 10 post images (SF Ruby photos via kramdown `{: width height}` IAL; Attractor SVGs from viewBox; VaultMem explainer; 4 Rena screenshots). CSS `.post-content img { height: auto }` keeps aspect ratio. Link checker: 0 warnings. Ubuntu 26 runner migration: this run (39303877522) green.

Engineer backlog additions:
- [ ] Images on non-post pages (projects, about) — check width/height if any are added
- [x] Back-to-top on long posts (done Oct 19, 12:35pm PT); reading progress bar skipped — TOC highlight covers it

## Done (Oct 19, 2026, 12:35pm PT)

- TOC scrollspy: IntersectionObserver on h2s in `_includes/post-tools.html`; current item = last h2 above 30% of the viewport, marked `aria-current` (bold + 2px accent underline — accent text on sepia surface is only 4.2:1, so the active item keeps text color).
- Back-to-top pill (`.back-to-top`, fixed bottom-right) on posts that have the TOC box (>= 1,200 words); shows after 1.5 screens, respects prefers-reduced-motion, moves focus to the h1, hidden in print. Tested at 375px with Playwright on a mock page (no horizontal scroll).

Engineer/Designer backlog additions:
- [x] Contrast: `.post-toc-list a:hover` (done Oct 19, 3:35pm PT — text color + accent underline)

## Done (Oct 19, 2026, 1:35pm PT)

- Events (beat d): Gmail shows a Cal Hacks 13.0 mentor acceptance (Oct 14; event Fri Oct 23 – Sun Oct 25, Palace of Fine Arts, SF) and he joined the event Slack. Added to `_data/events.yml` as role `mentor`, status upcoming (new role value; generic `.event-role` pill styles it). New "Mentoring" item on /now (shows on homepage). /events description mentions mentoring. Nothing past-dated yet.

Editor backlog additions:
- [ ] After Oct 25: move Cal Hacks 13.0 to past — keep role `mentor` only if a shift/QR/check-in email supports attendance; otherwise ask Avinash
- [ ] Waiting on Avinash: OSA Con (Nov 2) — a Luma email asked him to complete his registration; confirm he's still going before Nov 2
- [ ] llms.txt events line still says "attended, hacked at or judged" — add "mentored" next time llms.txt is touched

## Done (Oct 19, 2026, 2:35pm PT)

- Paper TL;DR #9: Generative Agents (Park et al., UIST 2023) at /post/paper-tldr-generative-agents/ — read from the arXiv PDF; neutral voice (no repo source ties it to his work; VaultMem link is a factual comparison to its significance re-ranking). Added to `_data/papers.yml` (no `why`). Glossary: new "Reflection" entry under How memories change over time. Post count Oct 19 PT: 4 — daily cap reached, no more new posts today.
- Note: og_cards.py skips posts that already have `image:` — don't pre-write it in front matter.

Editor backlog additions:
- [ ] Waiting on Avinash: has Generative Agents' recency/importance/relevance scoring influenced VaultMem's significance score? If yes, a `why` in papers.yml and a first-person line in the TL;DR
- [x] Designer: diagram for Generative Agents (done Oct 19, 3:35pm PT)

## Done (Oct 19, 2026, 3:35pm PT)

- Generative Agents TL;DR: inline SVG (memory stream of observations/plans/reflections → recency + importance + relevance score → top memories to the prompt / reflect when importance passes 150, dashed loop writing insights back) — `_includes/diagrams/generative-agents-memory.html`, placed before "3. Planning"; content only from the post. `.dg-line` now has `fill: none` so `<path>` connectors work (lines unaffected). Checked at 375px in sepia + dark (no horizontal scroll); only existing dg classes on `.dg-box` (audited contrast).
- TOC link hover/focus: keeps text color with a 2px-offset accent underline instead of accent text (was 4.2:1 on sepia).

Designer backlog additions:
- [ ] Diagram ideas still open: LoCoMo eval flow, Hopfield store/recall, VaultMem envelope encryption (MEK wrapping)
- [ ] Audit other `color: var(--accent)` hover states on --surface/--bg in sepia for the same 4.2:1 issue

## Done (Oct 19, 2026, 4:35pm PT)

- Deep links: project cards get `id="{{ name | slugify }}"` (e.g. /projects/#drafting-desk), papershelf items `id="paper-{{ title | slugify }}"`. search.json now points projects without a `post` and papers without a `tldr_post` at those anchors instead of the bare page. `:target` highlight (accent border + soft ring on cards; accent bar + soft fill on papers) with scroll-margin under the header. Link checker: 0 warnings.
- Bug fix: /research showed an empty "Why it matters to me" label for papers with no `why` (MemGPT, Generative Agents) — now only rendered when `why` exists. Lede reworded to match.
- Done: the "Search: index project/paper/event anchors" backlog item (events still link to /events/ — event rows have no ids yet).

Engineer backlog additions:
- [ ] Events: give event rows ids and point search's Event entries without a recap at /events/#<slug>
- [ ] CI: annotation still says actions/checkout@v4 + upload-artifact@v4 run on forced Node 24 — bump when v5/v6 majors are confirmed

## Done (Oct 19, 2026, 5:35pm PT)

- Glossary per-term anchors (beat e): all 25 definitions got a kramdown IAL `{: #slug .glossary-term}` (e.g. #reflection, #recall-at-k, #virtual-context, #hnsw). `.glossary-term:target` shows an accent bar (no tinted fill — accent links on --accent-soft are 3.8:1 in sepia), scroll-margin under the header. All 8 Paper TL;DR glossary footers now link each term to its own anchor (MemGPT adds virtual context, Generative Agents adds reflection). CI link checker: 0 fragment warnings, so the ids render. llms.txt events line now includes "mentored". Oct 19 PT post cap already reached, so no new post.
- Done: the "Glossary: give each bold term its own anchor id" backlog item.

Editor backlog additions:
- [ ] New glossary terms must get a `{: #slug .glossary-term}` line right under the paragraph (no blank line)

## Done (Oct 19, 2026, 6:35pm PT)

- Glossary (beat e): two new terms under "How memories change over time" — "Event time vs. write time" (#event-time; source: VaultMem Part 2's captured_at/created_at section) and "Versioned facts (temporal state)" (#versioned-facts; source: TEM 2610.21900 on emergentmind.com, opened this run). The Oct 19 roundup's Theme 3 now links both. VaultMem Part 2's LoCoMo section links the LoCoMo TL;DR and the Recall@k / MRR glossary anchors (wording only, no facts changed). CI link checker: 0 warnings. Oct 19 PT post cap already reached, so no new post.
- Done: the "Glossary: versioned facts / temporal state entry from TEM" backlog item.

Editor backlog additions:
- [ ] Cross-link sweep of the other older posts (Attractor, Daylog, Hobby stack, Whisper transcription) to glossary terms where they already use them

## Done (Oct 19, 2026, 7:35pm PT)

- Sepia accent-text contrast: new `--accent-ink: #0a5f58` (sepia only) and all 17 `color: var(--accent)` rules now use `var(--accent-ink, var(--accent))` (fallback evaluated per element, so other themes keep --accent). Sepia accent text was 4.16:1 on --surface / 4.32:1 on --code-bg; now 5.7 / 5.9 / 6.6 on bg, and 4.56 on --accent-soft over surface. Dark unchanged (≥4.66 everywhere). Borders/fills/diagram strokes still use --accent.
- 404 illustration: inline theme-aware SVG (sheet of paper + dotted trail + "?" ring), `.notfound-art` styles; trail dots drift only without prefers-reduced-motion. Checked at 375px in sepia + dark with Playwright (no horizontal scroll).
- Done: the "Audit other color: var(--accent) hover states" and "404 illustration" backlog items.

Designer backlog additions:
- [ ] New accent-colored TEXT should use `var(--accent-ink, var(--accent))`, not `var(--accent)`
- [ ] /papers :target note (style.css "accent links on --accent-soft drop to 3.8:1") — now 4.56:1 with --accent-ink; the tinted fill could come back

## Done (Oct 19, 2026, 8:34pm PT)

- Event deep links: each row on /events gets `id="{{ name | slugify }}"` (e.g. /events/#cal-hacks-13-0); search.json Event entries without a recap now point at that anchor; /now items (Mentoring, Judging, Going to) link their event's anchor. `.event-row:target` = accent bar only (no fill behind the role pill), scroll-margin under the header. CI link checker: 0 warnings (anchors resolve).
- Done: the "Events: give event rows ids" backlog item.
- Git tip: the persistent clone can be on a detached HEAD after a rebase — push with `git push origin HEAD:main`.

Engineer backlog additions:
- [ ] When an event moves to past and gets a recap, keep /now links pointing at the anchor or recap

## Done (Oct 19, 2026, 9:35pm PT)

- Print stylesheet (end of style.css, `@media print`): any theme prints light (tokens overridden on `body[class]`, dark Rouge spans forced to #111); hides header, footer, skip link, theme toggle, share, read-next, TOC, series boxes, heading anchors, copy buttons, back-to-top; code blocks wrap (pre-wrap); external post links print their URL; no page breaks inside code, tables, images, diagrams. Verified with Playwright `emulateMedia({media:'print'})` on a mock dark-theme post.

Engineer backlog additions:
- [ ] Print: check a real diagram post prints well (SVG text uses tokens, should follow the light override); maybe show the post URL + date under the title in print
- [ ] `<meta name="theme-color">` / `color-scheme` per theme (browser UI tint on mobile)

## Done (Oct 19, 2026, 10:35pm PT)

- Cross-link sweep (beat e) of the daylog posts: daylog security links VaultMem Part 1 (on "vaultmem"), the Sentence-BERT TL;DR (after the all-MiniLM-L6-v2 paragraph) and ends with a footer to the hobby stack + glossary anchors (episodic/semantic/procedural/persona memory, embedding, semantic search, decay). Hobby stack's Whisper and vaultmem sections link the Whisper post, daylog security and VaultMem Part 1; the Whisper post ends with links to both. Wording only — no facts changed. Skipped zero-knowledge/client-side-encryption glossary links on daylog: its vault decrypts in server RAM, so those terms don't fit exactly. Attractor already had its glossary footer. CI link checker: 0 warnings. Oct 19 PT post cap already reached.
- Done: the "Cross-link sweep of the other older posts" backlog item.

Editor backlog additions:
- [ ] Older non-memory posts (Codex skills, Jekyll site, ISTQB tests, AI history generator, Rena) — check for sensible links between them (e.g. Jekyll post ↔ /changelog, Rena ↔ Whisper/live audio) — only where the posts already discuss the topic

## Done (Oct 19, 2026, 11:34pm PT)

- Cross-link sweep (beat e) of the older non-memory posts: I Fell in Love with Coding Again → Doing the Right Thing, Fast + AI-tests post; AI-tests post → both workflow posts; Jekyll tutorial → /changelog + AI History Blog Generator; AI History generator → Jekyll tutorial + /uses (Ollama); Rena ↔ Whisper transcription (both stream live phone audio; Rena's 16 kHz PCM → backend → Gemini Live). Footer lines only, no facts changed. Events/now checked: nothing past-dated (Cal Hacks Oct 23). CI link checker: 0 warnings (run 39381310405). Oct 19 PT post cap already reached.
- Done: the "Older non-memory posts — check for sensible links" backlog item.

Editor backlog additions:
- [ ] Codex Skills post has no inbound/outbound links beyond fell-in-love/doing-right-thing — consider linking it from the AI-tests post if Avinash adds a test-review skill (waiting on him)

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
- 2026-10-19 07:35 PT — ENGINEER — search now indexes page body text (Events, Uses, Research…) via a post-build CI step (Actions deploy green).
- 2026-10-19 08:35 PT — EDITOR — explainer post on Drafting Desk's privacy design (/post/drafting-desk-how-it-keeps-drafts-private/), linked from /projects and /now. Actions runs stuck "queued" (no runner picked up ubuntu-latest jobs for 30+ min) — NEXT SHIFT: confirm runs 39279336864/39280359141 (or their successor) went green.
- 2026-10-19 09:35 PT — EDITOR — glossary entries for memory unlearning and sufficient evidence (/post/agent-memory-glossary/); title no longer hard-codes a term count (Actions deploy green).
- 2026-10-19 10:35 PT — DESIGNER — theme-aware three-tier retrieval diagram on /post/vaultmem-encrypted-memory-for-ai-agents/ (Actions deploy green).
- 2026-10-19 11:35 PT — ENGINEER — related posts skip same-series posts; width/height on post images to stop layout shift (Actions deploy green).
- 2026-10-19 12:35 PT — ENGINEER — TOC highlights the current section; back-to-top button on long posts (Actions deploy green).
- 2026-10-19 13:35 PT — EDITOR — Cal Hacks 13.0 (mentor, Oct 23–25) added to /events and /now from Gmail acceptance (Actions deploy green).
- 2026-10-19 14:35 PT — EDITOR — Paper TL;DR on Generative Agents (/post/paper-tldr-generative-agents/) + glossary reflection entry; daily post cap now reached (Actions deploy green).
- 2026-10-19 15:35 PT — DESIGNER — theme-aware memory/retrieval/reflection diagram on /post/paper-tldr-generative-agents/; TOC hover contrast fix (Actions deploy green).
- 2026-10-19 16:35 PT — ENGINEER — search deep-links to project cards (/projects/#slug) and papers (/research/#paper-slug) with :target highlight; fixed empty paper notes on /research (Actions deploy green).
- 2026-10-19 17:34 PT — EDITOR — glossary terms get their own anchors; Paper TL;DRs deep-link exact terms (/post/agent-memory-glossary/) (Actions deploy green).
- 2026-10-19 18:35 PT — EDITOR — glossary entries for versioned facts and event vs. write time (/post/agent-memory-glossary/#versioned-facts); VaultMem Part 2 links LoCoMo TL;DR + metric terms (Actions deploy green).
- 2026-10-19 19:35 PT — DESIGNER — darker sepia accent text for WCAG contrast site-wide; illustrated 404 page (Actions deploy green).
- 2026-10-19 20:34 PT — ENGINEER — per-event anchors on /events; search results and /now link straight to each event (Actions deploy green).
- 2026-10-19 21:35 PT — ENGINEER — print stylesheet: posts print/save-as-PDF as clean light pages with link URLs and wrapped code (Actions deploy green).
- 2026-10-19 22:35 PT — EDITOR — daylog security, hobby stack and Whisper posts now cross-link each other, VaultMem, Sentence-BERT and glossary terms (Actions deploy green).
- 2026-10-19 23:34 PT — EDITOR — older posts (coding again, AI tests, Jekyll, AI History generator, Rena, Whisper) cross-link each other (Actions deploy green).
