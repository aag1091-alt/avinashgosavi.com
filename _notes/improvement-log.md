# Site improvement log

Working notes for the recurring "improve avinashgosavi.com" task. Not published
(Jekyll ignores folders starting with `_` that aren't collections).

## Ground rules (from Avinash)

- **No posts on his behalf (Oct 20, 2026):** never create new posts in
  `_posts/` — no Paper TL;DRs, explainers, roundups or glossaries. Existing
  posts get small fixes only.
- **Taken down (Oct 20, 2026):** VideoOnly Browser and Drafting Desk projects
  and their posts — "both projects are not that good". Never re-add them.
- **Paper TL;DR is its own section** at /paper-tldr/ (nav item), kept out of
  the Writing list and homepage "Recent Writing".

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
- [x] Explainer: how Drafting Desk keeps drafts private (done Oct 19, 8:35am PT)

Designer:
- [x] Project cards: consistent visual header (done Oct 20, 12:34am PT)
- [x] About page layout on mobile (done Oct 20, 7:34pm PT; 404 illustration done Oct 19, 7:35pm PT)

Engineer:
- [x] CI internal link check (done Oct 19, 6:35am PT — see below)
- [x] CI link check: `--strict` (blocks deploy) — done Oct 27, 11:35am PT
- [x] Related posts: exclude same-series posts (done Oct 19, 11:35am PT)

General:

- [x] ~~Projects: short "what I learned" line per project~~ — dropped Oct 28
      (would be new first-person content; conflicts with the Oct 20 rule)
- [x] Events: link any other event to a recap if a post exists (checked Oct 23 — none)
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
- [x] Extend anchors/copy buttons to non-post pages (already done via _includes/page-anchors.html — noted Oct 25, 4:35pm PT)

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
- [ ] Old Attractor SVGs are hard-coded dark (#0f1117) — convert to theme-aware inline diagrams (~~context filtering~~ done Oct 21, 12:34am PT; ~~energy landscape~~ done Oct 21, 5:35am PT; ~~architecture~~ done Oct 21, 10:34am PT)

## Done (Oct 19, 2026, 1:35am PT)

- Table of contents: posts with >= 1,200 words get a collapsible "On this page" box (h2 sections, needs >= 3) above the content; open by default at >= 700px, collapsed on phones. Opt out per post with `toc: false` in front matter. Markup in `_layouts/post.html`, built by JS in `_includes/post-tools.html`, styles `.post-toc` in style.css (theme tokens).

Engineer backlog additions:
- [x] TOC: highlight the current section while scrolling (done Oct 19, 12:35pm PT)

## Done (Oct 19, 2026, 2:35am PT)

- Site-wide search: /search/ page (search.md, vanilla JS, ~120 lines) over /search.json (posts with first 8k chars of text, pages with titles, projects, papers, events). Weighted scoring (title > tags > description > text), all terms must match, highlighted snippets, ?q= shareable URLs. Header magnifier icon (`.header-search`), `/` shortcut on every page (focuses the page's search box, else opens /search/). Blog no-results and 404 link to it; llms.txt lists /search.json. CI step validates _site/search.json is JSON (fails build before deploy if broken). Contrast: mark text 9.0:1 sepia / 7.8:1 dark.

Engineer backlog additions:
- [x] Search: include page body text (done Oct 19, 7:35am PT)
- [x] CI: Node 20 action deprecation warnings (done Oct 22, 4:34pm PT)

## Done (Oct 19, 2026, 3:35am PT)

- Paper TL;DR #8: MemGPT (Packer et al., 2023) at /post/paper-tldr-memgpt/ — read from the arXiv PDF; neutral voice (no repo source ties it to his projects). Added to `_data/papers.yml` (no `why`). Glossary: new "Virtual context (paging)" entry under Kinds of memory linking to it. Post count Oct 19 PT: 1.
- Note: today is Monday — the weekly "This week in agent memory" roundup (beat c) is still open for a later editor shift today. arXiv abs pages needed a permission prompt in this unattended run; the arXiv PDF URL from a WebSearch result worked.

Editor backlog additions:
- [ ] Waiting on Avinash: has he used MemGPT/Letta or compared it to VaultMem? If so, a "what I took from it" line for the MemGPT TL;DR and a `why` in papers.yml

## Done (Oct 19, 2026, 4:35am PT)

- First weekly roundup (beat c): /post/this-week-in-agent-memory-2026-10-19/ — 7 arXiv papers submitted Oct 13–16 (Bemula unlearning benchmark, MemCut, QEMem, JointCore, TEM, multimodal memory survey, memory-centric compression survey), grouped by theme, each read from its arXiv abs page, neutral voice, links to glossary/LoCoMo/MemGPT posts. Tags Agent memory, Roundup, Research. Post count Oct 19 PT: 2.
- Source tip: WebSearch "arxiv.org/abs/2610 agent memory" surfaces this month's IDs; abs pages fetched fine this run. Check submission dates — many 2610.* hits were Oct 7–10 (outside the 7-day window).

Editor backlog additions:

## Done (Oct 19, 2026, 5:35am PT)

- MemGPT Paper TL;DR: inline SVG diagram of main context (system instructions / working context / FIFO queue) vs external context (recall / archival), with eviction and function-call arrows — `_includes/diagrams/memgpt-virtual-context.html`, content taken only from the post. New `.dg-group` (dashed container) and `.dg-label` (small caps label) classes in style.css. Contrast: muted text 5.7:1 sepia / 5.2:1 dark on box fill; checked at 375px in both themes (Playwright needs `executablePath: '/opt/pw-browsers/chromium'`).

Designer backlog additions:

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
- [x] (done, verified Oct 21 4:34am PT) llms.txt events line still says "attended, hacked at or judged" — add "mentored" next time llms.txt is touched

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
- [x] Audit other `color: var(--accent)` hover states on --surface/--bg in sepia for the same 4.2:1 issue (checked Oct 21, 11:35pm PT: no text uses plain --accent any more)

## Done (Oct 19, 2026, 4:35pm PT)

- Deep links: project cards get `id="{{ name | slugify }}"` (e.g. /projects/#drafting-desk), papershelf items `id="paper-{{ title | slugify }}"`. search.json now points projects without a `post` and papers without a `tldr_post` at those anchors instead of the bare page. `:target` highlight (accent border + soft ring on cards; accent bar + soft fill on papers) with scroll-margin under the header. Link checker: 0 warnings.
- Bug fix: /research showed an empty "Why it matters to me" label for papers with no `why` (MemGPT, Generative Agents) — now only rendered when `why` exists. Lede reworded to match.
- Done: the "Search: index project/paper/event anchors" backlog item (events still link to /events/ — event rows have no ids yet).

Engineer backlog additions:
- [ ] Events: give event rows ids and point search's Event entries without a recap at /events/#<slug>
- [x] CI: actions bumped to Node 24 majors (done Oct 22, 4:34pm PT)

## Done (Oct 19, 2026, 5:35pm PT)

- Glossary per-term anchors (beat e): all 25 definitions got a kramdown IAL `{: #slug .glossary-term}` (e.g. #reflection, #recall-at-k, #virtual-context, #hnsw). `.glossary-term:target` shows an accent bar (no tinted fill — accent links on --accent-soft are 3.8:1 in sepia), scroll-margin under the header. All 8 Paper TL;DR glossary footers now link each term to its own anchor (MemGPT adds virtual context, Generative Agents adds reflection). CI link checker: 0 fragment warnings, so the ids render. llms.txt events line now includes "mentored". Oct 19 PT post cap already reached, so no new post.
- Done: the "Glossary: give each bold term its own anchor id" backlog item.

Editor backlog additions:
- [ ] New glossary terms must get a `{: #slug .glossary-term}` line right under the paragraph (no blank line)

## Done (Oct 19, 2026, 6:35pm PT)

- Glossary (beat e): two new terms under "How memories change over time" — "Event time vs. write time" (#event-time; source: VaultMem Part 2's captured_at/created_at section) and "Versioned facts (temporal state)" (#versioned-facts; source: TEM 2610.21900 on emergentmind.com, opened this run). The Oct 19 roundup's Theme 3 now links both. VaultMem Part 2's LoCoMo section links the LoCoMo TL;DR and the Recall@k / MRR glossary anchors (wording only, no facts changed). CI link checker: 0 warnings. Oct 19 PT post cap already reached, so no new post.
- Done: the "Glossary: versioned facts / temporal state entry from TEM" backlog item.

Editor backlog additions:
- [x] Cross-link sweep of the other older posts (Attractor, Daylog, Hobby stack, Whisper transcription) to glossary terms where they already use them (done Oct 24, 11:34pm PT — Whisper post uses no glossary terms)

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
- [x] (checked Oct 24, 4:35am PT — dark-theme diagram prints with light tokens, fine) Print: check a real diagram post prints well (SVG text uses tokens, should follow the light override); ~~post URL under the title~~ (done Oct 21, 6:34am PT)
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

## Done (Oct 20, 2026, 12:34am PT)

- Project cards (`_includes/project-card.html`): 3px category band (`.project-card::before`) + 2rem icon chip with an inline stroke SVG per category (lock = Memory & privacy, mic = Agents & voice, wrench = Tools, sparkle = Just for fun), keyed by `data-cat="{{ category | slugify }}"`. Homepage passes `show_category=true` to add a small uppercase kicker with the category name (/projects already has category headings). Tokens `--cat-agents/--cat-tools/--cat-fun` on :root with dark overrides; memory uses the theme `--accent` (set on `.project-card`, not :root — :root resolves --accent to the white theme's blue). Decorative hues ≥4.16:1 sepia / ≥7.1:1 dark on --surface; kicker uses --text-muted (5.5 / 6.6). Checked at 375px + 900px in sepia and dark with Playwright on a mock page (no horizontal scroll). Run 39387695071 green, 0 link warnings.
- Done: the "Project cards: consistent visual header" backlog item.

Designer backlog additions:
- [x] Project cards: long hyphenated names (whisper-live-transcribe) wrap at the hyphen at 375px (done Oct 25, 12:34am PT)
- [x] Reuse the category icons as small markers in /projects category headings (done Oct 21, 11:35pm PT)

## Done (Oct 20, 2026, 1:34am PT)

- Browser UI follows the theme: `<meta name="theme-color">` (header surface: sepia #e8e0cc, dark #1e1b16) and `<meta name="color-scheme">` (light / dark) in `_layouts/default.html`, set from `site.color_theme`; a tiny head script reads the saved theme from localStorage before first paint, and `apply()` in `_includes/theme-toggle.html` updates both metas on toggle. CSS `color-scheme: light` on body.theme-sepia, `dark` on body.theme-dark (native scrollbars, inputs, autofill). Tested with Playwright on a mock page: toggle + reload keep metas in sync, no JS errors. Run 39394542822 green.
- Done: the "`<meta name=\"theme-color\">` / `color-scheme` per theme" backlog item.

Engineer backlog additions:
- [ ] Theme flash: the saved dark theme is applied by the header script (after the skip link renders) — consider setting a class on `<html>` in the head script and keying tokens off it to remove any first-paint flash
- [ ] If theme colors change in style.css, update the hex values in default.html + theme-toggle.html too

## Done (Oct 20, 2026, 2:34am PT)

- Theme flash fix: an inline script right after `<body>` in `_layouts/default.html` sets `document.body.className` to the saved theme (localStorage `blog_color_theme`) before the skip link/header parse, so dark readers no longer get a sepia first paint. theme-toggle.html still runs `apply()` later (slider state, metas). Tested with Playwright on a mock page: class is theme-dark before any content when stored, theme-sepia otherwise, no JS errors. Run 39401816939 green.
- Done: the "Theme flash" backlog item.

Engineer backlog additions:
- [ ] Theme: consider honoring `prefers-color-scheme: dark` for first-time visitors (no stored choice) — design call, ask Avinash first (default is sepia)

## Done (Oct 20, 2026, 3:34am PT)

- Paper TL;DR #10: Lost in the Middle (/post/paper-tldr-lost-in-the-middle/), sourced from arXiv abs v3 + ar5iv full text; added to `_data/papers.yml` (no `why` — not sourced); glossary gets a `#position-bias` entry after re-ranking. 1 post today (Oct 20 PT).

Editor backlog additions:
- [ ] Optional diagram for Lost in the Middle: U-shaped accuracy vs. position sketch (qualitative only, no invented numbers)

## Done (Oct 20, 2026, 4:35am PT)

- Explainer (beat b): /post/videoonly-browser-how-it-works/ — popups (setWindowOpenHandler deny + app-wide fallback), redirect guard (user-started or same base domain; non-web schemes refused), leave-page traps, downloads/permissions denied, Ghostery + EasyList/EasyPrivacy, isolated-world preload, auto-pick scoring (≥300×150, area × 3 if playing, 1.3× rule after manual off), the `[data-vo-keep] > :not(...)` CSS rule, cross-origin iframe walk, e2e test + release workflow, honest limits (no DRM, unsigned Windows). Sourced only from the repo README + main.js/content-preload.js/urlutil.js (cloned publicly). Projects card links it (`post:`). Post count Oct 20 PT: 2. Run 39416144924 green, 0 link warnings.

Editor backlog additions:
- [ ] Explainer still open: What's New in AI (ai-newsletter repo) — read README first

## Done (Oct 20, 2026, 5:35am PT)

- Lost in the Middle TL;DR: inline SVG U-curve sketch (accuracy vs. answer-passage position; primacy / "lost in the middle" / recency; a strip of 9 prompt passages with the first and last highlighted) — `_includes/diagrams/lost-in-the-middle-u-curve.html`, placed before "Why it matters for builders". Qualitative only (no axis numbers), caption says so. New classes `.dg-curve` (3px round stroke), `.dg-axis` (muted solid), `.dg-dot` (accent with --bg halo). Contrast: curve 4.8:1 sepia / 7.4:1 dark on bg, muted labels 6.3 / 5.8. Checked at 375px in sepia + dark (no horizontal scroll). Run 39423606119 green.
- Done: the "Optional diagram for Lost in the Middle" backlog item.

Designer backlog additions:
- [ ] `.dg-axis`/`.dg-curve` make simple qualitative charts possible — reuse only where a post describes a shape (no invented numbers)

## Done (Oct 20, 2026, 6:35am PT)

- Per-series Atom feeds: `_layouts/series-feed.html` (newest 20 parts, full HTML content with xml:base, summary from description, tags as categories) + one stub page per series in `feed/` (`feed/paper-tldr.xml`, `feed/vaultmem.xml`, `sitemap: false`). Linked from /series (lede + "Follow X via RSS" per section), the bottom series box on every part ("Follow this series", `.series-box-feed`), `<link rel="alternate">` in the head of series posts and /series, and llms.txt. Shared RSS glyph `_includes/feed-icon.html`. New CI step parses /feed.xml + every /feed/*.xml as Atom (fails the build if malformed). Template pre-checked with python-liquid mock render. Run 39432005480 green, no link warnings.

Engineer backlog additions:
- [ ] New series in `_data/series.yml` need a stub `feed/<slug>.xml` (copy an existing one) — or the series box links a 404 (CI link checker would warn)

## Done (Oct 20, 2026, 7:35am PT)

- CI accessibility lint: `scripts/check_a11y.py` (stdlib, offline) checks every built page for html lang, non-empty title, exactly one h1, heading levels not skipping downward, img alt, accessible names on links/buttons (text, aria-label, aria-labelledby, title, img alt, svg <title>; aria-hidden/hidden subtrees ignored), form-field labels, duplicate ids. One ::warning per rule (count + 4 examples, since annotations are capped) plus the full list in the job summary; `continue-on-error: true`, `--strict` available. First run (39440782441): 1 false positive (link inside the hidden blog no-results `<p hidden>` — linter now skips hidden ancestors) and 8 real: unlabeled kramdown task-list checkboxes in the ISTQB post — `_includes/post-tools.html` now sets each checkbox's aria-label to its list item text (linter skips `.task-list-item-checkbox`, tested with Playwright). Run 39441331130: green, 0 a11y warnings.

Engineer backlog additions:
- [x] (done Oct 20, 11:34am PT) a11y lint: add checks for link text like "here"/"click here", `target=_blank` without rel=noopener, and tables without header cells; consider `--strict` after a week at 0
- [ ] Color contrast can't be linted statically — keep the Playwright contrast scripts for designer shifts

## Done (Oct 20, 2026, 8:35am PT)

- Paper TL;DR #11: RAG (Lewis et al., 2020) at /post/paper-tldr-retrieval-augmented-generation/ — read from the arXiv abs v4 + PDF (affiliations, intro framing, Table 1, Jeopardy human eval, index hot-swap, retrieval collapse, broader impact). Venue left as arXiv (the PDF has no NeurIPS footer). Added to `_data/papers.yml` (no `why`). Glossary: new `#rag` entry after top-k retrieval. Post count Oct 20 PT: 3. Run 39450093496 green, no link/a11y warnings.
- Events (beat d) checked: no new registrations in Gmail since Oct 19; nothing past-dated (Cal Hacks Oct 23).

Editor backlog additions:
- [ ] Waiting on Avinash: does VaultMem/daylog count as RAG in his framing, or did the RAG paper shape his work? If yes, a `why` in papers.yml + first-person line
- [x] Designer: RAG diagram (done Oct 20, 10:35am PT) (query encoder → index top-k → generator; swap-the-index callout), content only from the post

## Done (Oct 20, 2026, 9:35am PT)

- Cross-links (beat e) for the new RAG TL;DR: Lost in the Middle footer ("Next in the series: RAG"), LoCoMo's "retrieval-augmented generation", Sentence-BERT's "RAG system" and the six-papers intro's "RAG setups" (→ glossary #rag; his post, link only, wording unchanged). No new post (Oct 20 PT count stays 3). Run 39458912798 green, 0 link warnings.
- External link sweep attempted: curl to arXiv/github.io/etc. returns 000 through the sandbox proxy, so external links can't be checked from here — don't retry; rely on CI or a manual check.

Editor backlog additions:
- [ ] Projects "what I learned" line: only AI History Blog Generator ("What Surprised Me") and whisper-live-transcribe ("what I learned") have sourced lessons — not enough for a site-wide field yet; ask Avinash or do per-card only where the post states it

## Done (Oct 20, 2026, 10:35am PT)

- RAG TL;DR: inline SVG of retrieve-then-generate (input pill → BERT query encoder → non-parametric memory group with the Dec 2018 Wikipedia index ⇄ dashed 2016 index "no retraining", FAISS + HNSW / frozen doc encoder note → top-k passages → BART generator → answer pill; dashed training-signal loop back to both trained parts, rotated label "learns only from the final answer") — `_includes/diagrams/rag-retrieve-then-generate.html`, placed at the end of "How it works". Content only from the post. Contrast: notes 5.7:1 sepia / 5.2:1 dark on box fill, pill text 9.0 / 7.9, accent lines 4.8 / 7.4 on bg. Checked at 375px in sepia + dark (no horizontal scroll). Run 39467588245 green, no link/a11y warnings.
- Done: the "Designer: RAG diagram" backlog item.

Designer backlog additions:
- [ ] Rotated `.dg-note` labels (transform rotate) work well for side loops — reuse instead of cramming horizontal text
- [ ] Diagram ideas still open: LoCoMo eval flow, Hopfield store/recall, VaultMem envelope encryption (MEK wrapping)

## Done (Oct 20, 2026, 11:34am PT)

- a11y lint (`scripts/check_a11y.py`) gained 3 rules: `link-text` (vague link names like "here", "read more", "click here" — skipped when aria-label is set), `blank-noopener` (target=_blank without rel noopener/noreferrer), `table-header` (tables without <th>, role=presentation skipped). Tested on a fixture. Pre-fix: /research "Read more →" links (papers with `why` + `post`) now have `aria-label="Read more about <title>"`. Deploy run 39476147496 green with no a11y annotations.

Engineer backlog additions:
- [x] a11y lint: links built by JS (search results, TOC) aren't covered (done Oct 24, 12:34pm PT — `a11y-dom` rule in check_browser.py)
- [ ] Consider `--strict` for check_a11y.py after a week at 0 warnings (from Oct 27)

## Done (Oct 20, 2026, 12:34pm PT)

- /search/ type filter: chips (All / Posts / Projects / Papers / Events / Pages, with counts; only types that have hits; hidden when <2 kinds) built in search.md, `aria-pressed`, choice kept in the URL as `?q=…&type=Paper` (falls back to All if that type has no hits). Keyboard: ↓ from the box focuses the first result title, ↑/↓ walk results, ↑ on the first returns to the box, Esc clears (box) / returns to the box (results). Small "Tip" line with `<kbd>` only on hover+fine-pointer devices (`.search-hint`). Blog tag chips now set `aria-pressed` too. Tested with Playwright on a mock page at 375px dark (filter, URL, keys, no horizontal scroll, no JS errors). Run 39484888509 green, no link/a11y warnings.

Engineer backlog additions:
- [ ] Search: Enter could open the top result when the query hasn't changed since results rendered (ask whether that surprises people first — current Enter just re-renders)

## Done (Oct 20, 2026, 7:34pm PT)

- About page on phones (≤640px, style.css media query only): photo moves above the text (`order: -1`), centered (was stuck left — `align-items: flex-start` defeated `margin: auto`), 176px wide cropped 4:5 with `object-fit: cover; object-position: 62% 30%`; h1 centered at 1.6rem. Desktop unchanged. Checked at 375px + 900px in sepia + dark with Playwright on a mock page (no horizontal scroll). Run 39533905715 green. Note: about.md has no permalink, so link it as /about (not /about/).

Designer backlog additions:
- [ ] About page desktop: photo could be `position: sticky` beside the long text column

## Done (Oct 20, 2026, 8:35pm PT)

- Favicon: the site had none (tabs/bookmarks showed a blank page, /favicon.ico 404'd). Added root `favicon.svg` (64×64 rounded teal #0f766e tile, "AG" outlined from Poppins Bold glyph paths via fontTools — no font dependency), `favicon.ico` (16/32/48, Pillow) and `apple-touch-icon.png` (180×180, full-bleed square; iOS rounds it). Rasterized with Playwright. `<link rel="icon">` ×2 + apple-touch-icon in `_layouts/default.html` (the only layout with a `<head>`). Letter color #f5efe0 on #0f766e ≈ 5.0:1. Run 39539503568 green.

Engineer backlog additions:
- [x] `site.webmanifest` (done Oct 21, 1:35am PT)

## Done (Oct 22, 2026, 10:34am PT)

- DESIGNER: theme-aware, phone-friendly sanitize → provider → restore
  diagram on /post/vaultmem-part-3-pii-sanitizer/
  (`_includes/diagrams/vaultmem-sanitizer-round-trip.html`). Posts still
  without a diagram: Sentence-BERT, Modern Hopfield, Whisper, VaultMem Part 2.

## Done (Oct 22, 2026, 11:34am PT)

- Code blocks: `_includes/post-tools.html` adds a `.code-lang` tab (language
  from the wrapper's `language-xxx` class; plaintext/text/console skipped)
  sitting on top of the box's left edge (`bottom: 100%`, `.has-lang >
  .highlight` gets 1.9rem top margin so it never touches the text above).
  Copy buttons now say "Copy python code to clipboard" and a shared polite
  status region announces "Code copied to clipboard" (or the failure hint).
  Muted text on --code-bg 5.7:1 sepia / 5.2:1 dark. Playwright mock at 375px
  both themes: scrollWidth 375, no JS errors. Run 39832898685 green.

## Done (Oct 22, 2026, 12:35pm PT)

- Image viewer on posts (`_includes/post-tools.html` + `.img-viewer` CSS):
  any `.post-content img` not inside a link or `.diagram` whose largest source
  (width attr, `srcset` w-descriptors of the img/`<source>`s, or a bare webp
  `<source>`) is >1.25× its rendered width gets `.is-zoomable`, tabindex 0,
  role=button, "Enlarge image: <alt>" (re-checked via ResizeObserver). Click /
  Enter / Space opens a modal `<dialog>` with the largest source + alt caption;
  Esc, Close, backdrop or image click closes and returns focus. Hidden in print.
  Today that's the Rena screenshots, VaultMem explainer (opens the 1400w
  webp) and SF Ruby photos. Playwright mock 375/1280, sepia + dark: no JS
  errors, scrollWidth unchanged, focus restore works. Run 39841721519 green.

Engineer backlog additions:
- [ ] New post images: keep `width`/`height` attrs = the full file size — the viewer uses them to decide zoomability

## Done (Oct 25, 2026, 5:34am PT)

- Designer shift (UTC 12): post tables. Cells used the browser default
  `vertical-align: middle`, so short row labels (Codex skills "What it is",
  VaultMem ABC table) floated mid-row beside wrapped multi-line cells. Now
  td/th `vertical-align: top`, thead th bottom, table `line-height: 1.5`
  (was body 1.65) and `font-variant-numeric: tabular-nums` (VaultMem Part 2
  latency columns). Colours untouched. Playwright file mock of the Codex
  table at 375px: cells top-aligned, page scrollWidth 375 (table scrolls in
  its box). Run 40193843587 green.

## Done (Oct 25, 2026, 9:34am PT)

- Editor slot (UTC 16): nothing needed — Cal Hacks 13.0 ends today (Oct 25),
  so it stays upcoming until tomorrow's editor; /now accurate; Gmail last 2
  days: no new registrations (SF Ruby 2026 Luma message already logged);
  codespell clean; llms.txt covers every page. SF Ruby 2025 post says
  "Ruby 3.5 and beyond" — Ruby 3.5 shipped as 4.0, but that's his wording and
  no source opened this run (rubyevents.org fetch not approved), so left as is.
- → Engineer: search.md text fragments now add a second directive with the
  matched word alone (`#:~:text=<phrase>&text=<word>`) when the 2-word
  extension was used, so a phrase crossing a heading/list boundary still
  scrolls to the word. Playwright check on a mock (h2 "Memory types" + p):
  phrase-only → scrollY 0; with fallback → 2668. Run 40212881861 green.
- Backlog note: many older `[ ]` items are already done (theme-color per
  theme, event row ids, project/paper anchors in search, pre-paint theme
  script) — check the code before picking one.
- 2026-10-25 09:34 PT — EDITOR→ENGINEER — search result links still jump to the matched word when the phrase spans a heading/list boundary (search.md; /search/) (Actions deploy green).

## Done (Oct 25, 2026, 10:35am PT)

- Designer shift (UTC 17): new `_includes/diagrams/jekyll-pages-deploy.html`
  on /post/building-your-website-with-jekyll-and-github-pages/ (after the
  "Build workflow" paragraph in section 5): git push → Actions (bundle
  install, jekyll build without --baseurl, _site, upload-pages-artifact,
  deploy-pages) → GitHub Pages ← DNS (www CNAME, apex A records, Enforce
  HTTPS). Every label is from the post's own text. Playwright mock 375px
  sepia + dark: no text past the viewBox, scrollWidth 375. Run 40217267746 green.
- Posts still without a diagram (only if the post describes a flow): Codex
  skills, ISTQB tests review, glossary/six-papers roundups (probably not).

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
- 2026-10-20 00:34 PT — DESIGNER — project cards get a category icon + colored top band; homepage cards name the category (/projects/, /) (Actions deploy green).
- 2026-10-20 01:34 PT — ENGINEER — mobile browser bar tint (theme-color) and native color-scheme follow sepia/dark, synced on toggle (Actions deploy green).
- 2026-10-20 02:34 PT — ENGINEER — saved dark theme applied before first paint, no more sepia flash (Actions deploy green).
- 2026-10-20 03:34 PT — EDITOR — Paper TL;DR on Lost in the Middle (/post/paper-tldr-lost-in-the-middle/) + glossary position-bias entry (Actions deploy green).
- 2026-10-20 04:35 PT — EDITOR — explainer post on how VideoOnly Browser works (/post/videoonly-browser-how-it-works/), linked from /projects (Actions deploy green).
- 2026-10-20 05:35 PT — DESIGNER — U-shaped curve sketch on /post/paper-tldr-lost-in-the-middle/ (Actions deploy green).
- 2026-10-20 06:35 PT — ENGINEER — per-series RSS feeds (/feed/paper-tldr.xml, /feed/vaultmem.xml) linked from /series and each series part; CI validates feeds (Actions deploy green).
- 2026-10-20 07:35 PT — ENGINEER — CI accessibility lint on every deploy; task-list checkboxes in /post/reviewing-ai-generated-tests-istqb-framework/ now labelled for screen readers (Actions deploy green, 0 a11y warnings).
- 2026-10-20 08:35 PT — EDITOR — Paper TL;DR on RAG (/post/paper-tldr-retrieval-augmented-generation/) + glossary RAG entry (Actions deploy green).
- 2026-10-20 09:35 PT — EDITOR — RAG TL;DR cross-linked from Lost in the Middle, LoCoMo, Sentence-BERT and the six-papers intro (Actions deploy green).
- 2026-10-20 10:35 PT — DESIGNER — theme-aware retrieve-then-generate diagram on /post/paper-tldr-retrieval-augmented-generation/ (Actions deploy green).
- 2026-10-20 11:34 PT — ENGINEER — a11y lint now flags vague link text, target=_blank without noopener and header-less tables; /research "Read more" links labelled per paper (Actions deploy green).
- 2026-10-20 12:34 PT — ENGINEER — /search/ results filter by type (posts, projects, papers, events, pages) with shareable URL + arrow-key navigation; blog tag chips expose aria-pressed (Actions deploy green).
- 2026-10-20 13:34 PT — EDITOR — Paper TL;DR on HNSW (/post/paper-tldr-hnsw/) + papers.yml entry; glossary HNSW term and VaultMem Part 2 link to it. Events/now checked: nothing passed, no new registrations in Gmail. Daily post cap now reached (4) (Actions deploy green).
- 2026-10-20 14:35 PT — EDITOR — HNSW TL;DR cross-linked from Sentence-BERT, Hopfield Networks Is All You Need, Attractor and VaultMem Part 1 (post cap reached; Actions deploy green).
- 2026-10-20 15:35 PT — DESIGNER — theme-aware layered-search diagram on /post/paper-tldr-hnsw/ (Actions deploy green).
- 2026-10-20 16:35 PT — ENGINEER — # section links on h2s of all regular pages (/uses, /research, /events, /changelog, /projects…) (Actions deploy green).
- 2026-10-20 17:34 PT — EDITOR — next-in-series links on MemGPT, Generative Agents and RAG TL;DRs; RAG's HNSW mention links the HNSW TL;DR (post cap reached; Actions deploy green).
- 2026-10-20 18:35 PT — EDITOR — next-in-series links on Hopfield 2020, LoCoMo, Memory as Asset, Sentence-BERT and Hopfield 1982 TL;DRs; parts 2→12 now fully chained (post cap reached; Actions deploy green).
- 2026-10-22 05:34 PT — DESIGNER — balanced heading wraps, orphan-free paragraphs and theme-tinted text selection site-wide (assets/css/style.css) (Actions deploy green).

## Done (Oct 20, 2026, 1:34pm PT)

- Paper TL;DR #12: HNSW, read from arXiv PDF (latest version) + abs v2 page; TPAMI DOI from opentrain.ai listing. Next candidates: ColBERT, DPR (Karpukhin et al., 2020 — RAG's retriever), product quantization (Jégou et al.).
- Backlog idea (Designer): small theme-aware diagram of HNSW's layered descent for /post/paper-tldr-hnsw/.

## Done (Oct 20, 2026, 2:35pm PT)

- HNSW TL;DR now has inbound links from 4 more posts (Sentence-BERT, Hopfield 2020, Attractor, VaultMem Part 1).
- Tried to verify whether the RAG paper used FAISS with an HNSW index (to link RAG TL;DR → HNSW TL;DR) but arXiv fetch permission timed out; left unlinked. Next editor: confirm in arxiv.org/abs/2005.11401 before adding that line.

## Done (Oct 20, 2026, 3:35pm PT)

- HNSW TL;DR: inline SVG of the layered search (three dashed layer bands — layer 2 two items/one long link, layer 1 four, layer 0 every item with short links; accent path entry point → hop → dashed drop → hop → drop → hop; dashed ellipse "ef candidates → best k" around the query ×; numbered 4-step legend) — `_includes/diagrams/hnsw-layered-search.html`, placed before the "knobs" paragraph in "How it works". Sketch only, caption says so; content only from the post. New classes `.dg-node` (code-bg fill, muted stroke), `.dg-edge` (1px muted line), `.dg-query` (text-colored × stroke). Contrast: notes 6.3:1 sepia / 5.8:1 dark, node stroke on fill 5.7 / 5.2, accent 4.8 / 7.4. Checked at 375px in sepia + dark (no horizontal scroll). Run 39509441156 green.
- Done: the "Designer: HNSW layered descent diagram" backlog idea.
- Layout tip: right-aligned band notes collide with vertical connectors on the right — put band notes next to the label (x≈92) instead.

Designer backlog additions:
- [ ] `.dg-node`/`.dg-edge` allow small graph sketches — candidate: Hopfield store/recall (attractor basins) for the Hopfield TL;DR
- [ ] Diagram ideas still open: LoCoMo eval flow, VaultMem envelope encryption (MEK wrapping)

## Done (Oct 20, 2026, 4:35pm PT)

- Section links on regular pages: `_includes/page-anchors.html` (loaded by default.html only when `page.layout == 'default'`) gives every h2 in `<main>` an id (keeps existing ones like #papershelf; slug of the text, `&` → "and", `-2` suffix on collisions with project/event ids) and a hover `#` link (`h2.has-anchor`, same look as post anchors; 0.6 opacity on touch). Because ids are added after load, a shared #link gets one `scrollIntoView` (smooth scroll + 5rem scroll-margin). Changelog dates become e.g. /changelog/#october-20-2026. Tested with Playwright on a mock (375px dark): ids, labels, hash jump, no horizontal scroll, no JS errors. Run 39516140453 green, no annotations.
- Done: the "Extend anchors/copy buttons to non-post pages" backlog item (anchors only; no code blocks on those pages).

Engineer backlog additions:
- [x] (done Oct 21, 12:35pm PT) Page anchor ids are JS-only, so the CI link checker can't verify links to them — if posts start linking /uses/#… etc., render those ids server-side instead

## Done (Oct 20, 2026, 5:34pm PT)

- Cross-links (beat e): MemGPT → Generative Agents, Generative Agents → Lost in the Middle, RAG → HNSW "Next in the series" footer lines (series_order 8→9→10→11→12 now chained). RAG body's "HNSW approximation" now links /post/paper-tldr-hnsw/ (glossary #hnsw still linked in the footer). No new claims: the FAISS+HNSW statement was already in the RAG post (written from the PDF); arXiv fetch timed out again, so not re-verified. Oct 20 PT post cap (4) already reached. Events: nothing past-dated (Cal Hacks Oct 23). Run 39522739832 green, no link warnings.

Editor backlog additions:
- [x] Older TL;DRs "Next in the series" lines (done Oct 20, 6:35pm PT)
- [ ] New TL;DRs: add a "Next in the series" line to the previous part's footer

## Done (Oct 20, 2026, 6:35pm PT)

- Cross-links (beat e): "Next in the series" lines on Hopfield 2020 (#2 → CLS), LoCoMo (#4 → Memory as Asset), Memory as Asset (#5 → Sentence-BERT), Sentence-BERT (#6 → Hopfield 1982), Hopfield 1982 (#7 → MemGPT, "series keeps going"). Each one-line description taken from the target post's own text. Parts 2→12 now chained. Oct 20 PT post cap (4) reached. Run 39528256043 green.

Editor backlog additions:
- [x] Six-papers hub (#1) → Part 2 line (done Oct 20, 10:35pm PT)
- 2026-10-20 6:50pm PT — manual — Paper TL;DR section; removed VideoOnly Browser and Drafting Desk (projects + posts); no new posts rule.
- 2026-10-20 7:15pm PT — manual — deleted the "This week in agent memory" roundup at Avinash's request; no roundups.
- 2026-10-20 19:34 PT — DESIGNER — /about on phones opens with a centered, cropped photo above the intro instead of ending on it (Actions deploy green).
- 2026-10-20 20:35 PT — ENGINEER — site favicon (teal AG tile) for tabs, bookmarks and phone home screens (all pages, via default layout) (Actions deploy green).
- 2026-10-20 21:34 PT — ENGINEER — BreadcrumbList JSON-LD on every post/page (Home › Writing or Paper TL;DR › post); CI step validates all JSON-LD blocks (Actions deploy green, 0 problems).
- 2026-10-20 22:35 PT — EDITOR — /post/paper-tldr-six-papers-on-memory/ links Part 2 (series fully chained 1→12); /llms.txt lists Writing, Series, Achievements and no longer hard-codes the glossary term count (Actions deploy green).
- 2026-10-20 23:35 PT — EDITOR — VaultMem diary post (had only 1 inbound link) now linked from VaultMem Part 1 footer and glossary #zero-knowledge-storage; it lists Part 3 (Actions deploy green).

## Done (Oct 20, 2026, 9:34pm PT)

- Breadcrumb structured data: `_includes/breadcrumb-jsonld.html` (included from default.html head; skipped on / and /404.html). Posts → Home › Writing (/blog/) or Paper TL;DR (/paper-tldr/ for series paper-tldr) › post; other pages → Home › page. `scripts/check_jsonld.py` (CI, continue-on-error) parses every ld+json block and checks breadcrumb positions; exits 1 on problems. Run 39544882892 green, JSON-LD step passed. Run logs are 403 from the sandbox — read step conclusions via `gh api .../actions/jobs/<id>` instead.

Engineer backlog additions:
- [ ] Event JSON-LD on /events was considered and skipped (Google wants event markup on the event's own page)

## Done (Oct 20, 2026, 10:35pm PT)

- Six-papers hub now ends with a neutral "Next in the series" line → Hopfield 2020 (description from the target's front matter) + link to /paper-tldr/. Paper TL;DR parts 1→12 fully chained.
- llms.txt Pages: added /blog/ (Writing), /series/, /achievements/; glossary blurb dropped the stale "20 terms" (now ~29).
- Events/now: nothing past-dated (Cal Hacks Oct 23–25 is next). Gmail last 2 days: only a Luma *invite* to Berkeley Ruby Early Birds (Oct 24) — not accepted, so NOT added. Next editor after Oct 25: move Cal Hacks to past (role mentor, from acceptance email) and drop it from now.yml.
- Note: pages without a permalink (about.md, blog.md) still build to /about/ and /blog/ because the site permalink ends in "/" — both /about and /about/ forms are fine.
- Run 39550495718 green.

## Done (Oct 20, 2026, 11:35pm PT)

- Inbound-link audit (count by permalink AND post_url filename): /post/vaultmem-your-ai-agent-shouldnt-read-your-diary/ had only papers.yml. Now linked from VaultMem Part 1 footer and glossary zero-knowledge entry; its "technical writeups" list gained Part 3. Next-lowest (2 inbound): sf-ruby-2025, jekyll-and-github-pages, ai-history-blog-generator, vaultmem-part-3 — candidates for future cross-links.
- Events/now: nothing past-dated; Gmail last day had no registrations (IEEE panel Oct 27 is a promo, not a registration). Cal Hacks still Oct 23–25.
- External link check impossible from sandbox (all hosts 000/403 via proxy) — skip in future runs.
- Run 39556577627 green.

## Done (Oct 21, 2026, 12:34am PT)

- Attractor post: the hard-coded dark context-filtering SVG (`assets/images/attractor-context-filtering.svg`, now unreferenced but kept) is replaced by `_includes/diagrams/attractor-context-filtering.html` — query pill (the post's own query text) → "Vector search only" group with both memories → dashed arrow "same query, plus context_filter: topic = auth refactor" → "With the context filter" group (session-tokens memory on a pill, localStorage memory dashed/muted, "filtered out: formed in a security review" from the post's context block). Stacked vertically (360 wide) so it reads at 375px; only existing dg classes, `.dg-note` kept off pills. Checked in sepia + dark at 375px with Playwright (scrollWidth 375). Run 39563150720 green.

Designer backlog additions:
- [x] Attractor: energy landscape converted (Oct 21, 5:35am PT); architecture (820×380) SVG still hard-coded dark — convert next

- 2026-10-21 00:34 PT — DESIGNER — theme-aware, phone-friendly context-filtering diagram on /post/attractor-memory-engine/ (Actions deploy green).

## Done (Oct 21, 2026, 1:35am PT)

- Web app manifest: root `site.webmanifest` (name, short_name, start_url/scope "/", display "browser" — no install/standalone behaviour change, sepia bg #f5efe0 + theme #e8e0cc) with `assets/icons/icon-192.png`, `icon-512.png` (rounded tile from favicon.svg) and `icon-maskable-512.png` (full-bleed, letters inside the 80% safe zone), rasterized with Playwright. `<link rel="manifest">` in `_layouts/default.html`. New CI step parses the manifest and stats each icon (fails build if missing). Run 39570532172 green, no link/a11y warnings.

Engineer backlog additions:
- [ ] If favicon.svg changes, regenerate the 3 manifest PNGs + apple-touch-icon.png too

- 2026-10-21 01:35 PT — ENGINEER — web app manifest + 192/512/maskable icons so Android home-screen shortcuts use the AG tile (/site.webmanifest) (Actions deploy green).

## Done (Oct 21, 2026, 2:35am PT)

- Self-hosted fonts: Google Fonts link + 2 preconnects removed from `_layouts/default.html`; `assets/fonts/` holds Fontsource 5.3.0 variable woff2 files (DM Sans wght 100–1000 normal + italic, JetBrains Mono wght 100–800 normal; latin + latin-ext each, unicode-range split so latin-ext only loads when used; ~170 KB total, a typical page loads ~37–77 KB) with OFL license files. `@font-face` block at the top of style.css keeps the family names "DM Sans"/"JetBrains Mono", so `--font-sans`/`--font-mono` are unchanged. Preload for dm-sans-latin-wght-normal only. Italic now uses the real italic face (Google request only had 400 italic). Checked with Playwright (fonts load, italic/bold/accents render). Run 39578321708 green, no link/a11y warnings.

Engineer backlog additions:
- [ ] Mono italic isn't shipped (wasn't before either) — add jetbrains-mono-*-wght-italic.woff2 if code comments ever render in italic
- [ ] Google Analytics (gtag) is now the only third-party request on page load

- 2026-10-21 02:35 PT — ENGINEER — fonts self-hosted (assets/fonts/, all pages via default layout); no Google Fonts requests (Actions deploy green).

## Done (Oct 21, 2026, 3:35am PT)

- VaultMem Part 2 ends with a "Part 3 →" link (same pattern as Part 1 → Part 2). Remaining low-inbound posts: sf-ruby-2025 (permalink /post/my-sf-ruby-2025-experience-talks-side-quests-community-inspiration/ — only events.yml + talks.md link it; no post mentions Ruby events, so no natural cross-link yet), jekyll-and-github-pages, ai-history-blog-generator (they link each other + uses/projects).
- now.yml `updated` → 2026-10-21; all items still current. Events: nothing past-dated (Cal Hacks Oct 23–25 next). Gmail last day: no registrations (IEEE Oct 27 panel is promo only).
- llms.txt Pages checked: in step with real pages (/search/ covered by search.json).
- Run 39585767008 green.

- 2026-10-21 03:35 PT — EDITOR — VaultMem Part 2 links on to Part 3 (/post/vaultmem-part-2-multimodal-temporal-backends/); now.yml checked (Actions deploy green).

## Done (Oct 21, 2026, 4:34am PT)

- Rena post: the 4 screenshot captions had inline `color:#666` (hard-coded grey, low contrast on the dark theme) → `var(--text-muted)`. No other inline hex colors in `_posts/` or root pages.
- Checked: events/now current (Cal Hacks Oct 23–25 next); Gmail last day had no event registrations; llms.txt events line already says "mentored" (backlog item at line ~226 is done); Rena ↔ Whisper cross-links already exist both ways.
- Run 39593098008 green.

- 2026-10-21 04:34 PT — EDITOR — theme-aware screenshot captions on /post/building-rena-ai-health-companion-gemini-live/ (Actions deploy green).

## Done (Oct 21, 2026, 5:35am PT)

- Attractor post: hard-coded dark `assets/images/attractor-energy-landscape.svg` (now unreferenced, kept) replaced by `_includes/diagrams/attractor-energy-landscape.html` (360×282, dg-axis/dg-curve/dg-dot/dg-query). Old SVG drew memories at energy *peaks*; new one puts them at minima (basins), matching the post's "energy minima" text. Memory labels are the post's own two example memories. Checked sepia + dark at 375px with Playwright (scrollWidth 375). Run 39600997383 green.

Designer backlog additions:
- [x] Attractor architecture SVG converted (done Oct 21, 10:34am PT)

- 2026-10-21 05:35 PT — DESIGNER — theme-aware, phone-friendly energy-landscape diagram on /post/attractor-memory-engine/ (Actions deploy green).
## Done (Oct 21, 2026, 6:34am PT)
- Print: `_layouts/post.html` adds `<p class="post-print-source">` (absolute post URL) under the meta line — `display:none` on screen, shown in `@media print`; print also hides tag chips and appends " (avinashgosavi.com/path)" after internal `/…` links in post content (external links already showed their URL).
- Local `jekyll build` impossible in the sandbox (rubygems.org unreachable) — CI is the build check.
- Run 39609752255 green.
- 2026-10-21 06:34 PT — ENGINEER — printed/PDF posts show their source URL and internal link targets (all /post/* pages) (Actions deploy green).
## Done (Oct 21, 2026, 7:34am PT)
- Responsive WebP: /about photo is a `<picture>` (about-280.webp 19 KB / about-560.webp 65 KB, `sizes="(max-width: 640px) 176px, 280px"`, jpg fallback, `fetchpriority="high"` — it's the LCP image); SF Ruby post photos are `<picture>` with 720/1086 and 540/768 WebP (q78) + lazy jpg fallback. Originals kept (og/JSON-LD still use about.jpg / sf-ruby-1.jpg). Playwright: 375@2x picks about-560, 900@1x picks about-280; no horizontal scroll. `scripts/check_links.py` now checks every `srcset` candidate on img/source. Run 39618778763 green, no warnings.

Engineer backlog additions:
- [x] vaultmem-explainer.jpg and Rena screenshots WebP variants (done Oct 21, 11:35am PT)

- 2026-10-21 07:34 PT — ENGINEER — right-sized WebP photos on /about and /post/my-sf-ruby-2025-experience-talks-side-quests-community-inspiration/; link checker covers srcset (Actions deploy green).
## Done (Oct 21, 2026, 8:35am PT)
- Attractor post references 1, 2, 4, 6 now end with "Plain-language summary: [Paper TL;DR](…)" linking the Hopfield 1982, Hopfield 2020, Sentence-BERT and CLS TL;DRs (it previously linked only the HNSW TL;DR and glossary).
- Checked: events/now current (Cal Hacks Oct 23–25 next); Gmail last 2 days had no new event registrations.
- Run 39627238714 green.
- 2026-10-21 08:35 PT — EDITOR — Attractor post references link to their Paper TL;DRs (/post/attractor-memory-engine/#references) (Actions deploy green).
## Done (Oct 21, 2026, 9:35am PT)
- SF Ruby 2025 post now ends with "See also: Talks Worth Watching" (/talks/) — /talks/ already linked the post, now reciprocal. Didn't claim recordings are out (couldn't open rubyevents.org this run).
- Checked: events/now current (Cal Hacks Oct 23–25 next); Gmail last day had no event registrations. codespell over posts/pages: only "Rouge" false positives. External link check not possible from the sandbox (proxy returns 000/403).
- Run 39636992584 green.
- 2026-10-21 09:35 PT — EDITOR — SF Ruby post cross-links /talks/ (/post/my-sf-ruby-2025-experience-talks-side-quests-community-inspiration/) (Actions deploy green).
## Done (Oct 21, 2026, 10:34am PT)
- Attractor post: hard-coded dark `assets/images/attractor-architecture.svg` (unreferenced now, kept) replaced by `_includes/diagrams/attractor-architecture.html` (360×522, stacked: Client → REST → FastAPI endpoints → Encoder | PgStore → PostgreSQL + pgvector columns → port 7747 note). Content only from the old SVG + post. New CSS class `.dg-mono` (JetBrains Mono 12.5px). `.dg-note` on `.dg-pill` is only 3.7:1 in dark — so all boxes use `.dg-box` (muted on code-bg 5.7 sepia / 5.2 dark). Playwright at 375px sepia + dark: scrollWidth 375, no text outside the viewBox. All three Attractor diagrams are now theme-aware. Run 39645326603 green.

Designer backlog additions:
- [ ] Rule: never put `.dg-note` (muted) text on `.dg-pill` — fails 4.5:1 in dark (3.7:1); use `.dg-body` or `.dg-box`
- 2026-10-21 10:34 PT — DESIGNER — theme-aware, phone-friendly architecture diagram on /post/attractor-memory-engine/ (Actions deploy green).
## Done (Oct 21, 2026, 11:35am PT)
- WebP for the remaining post images: Rena post's 4 screenshots wrapped in `<picture>` with `rena-<name>.webp` (360w, same size; 137 KB → 44 KB total); VaultMem diary post's explainer image `<picture>` with `vaultmem-explainer-720.webp` (13 KB) / `-1400.webp` (34 KB), `sizes="(max-width: 42rem) 100vw, 42rem"`, jpg fallbacks kept. All post images now have WebP.
- Run 39654172680 green.
- 2026-10-21 11:35 PT — ENGINEER — WebP images on /post/building-rena-ai-health-companion-gemini-live/ and /post/vaultmem-your-ai-agent-shouldnt-read-your-diary/ (Actions deploy green).
## Done (Oct 21, 2026, 12:35pm PT)
- Page h2 section ids now server-rendered (was JS-only): /uses, /research, /events (upcoming/past), /achievements, /changelog (dates), /experience (companies), /projects (categories), /talks (topics). Slug rule matches page-anchors.html (`replace: '&', ' and ' | slugify`), so ids are identical to the old JS ones and existing shared links keep working; JS still adds the `#` link and covers any new h2. /series h2s left to JS (their section already has the slug id). Closes the "Page anchor ids are JS-only" backlog item; CI link checker can now verify links to these anchors. Logs/site unreachable from sandbox (proxy 403). Run 39663096915 green.

- 2026-10-21 12:35 PT — ENGINEER — server-rendered section ids on /uses, /projects, /events, /talks, /experience, /achievements, /changelog, /research (Actions deploy green).
## Done (Oct 21, 2026, 1:34pm PT)
- Low-inbound posts: /uses Ollama line now links the AI History Blog Generator post (its post-writing model is qwen2.5:14b via Ollama, per the post's stack table); /changelog lede links the Jekyll + GitHub Pages setup post. Both posts had only 2 inbound links.
- Checked: events/now current (Cal Hacks Oct 23–25 next); Gmail last day had no event registrations; llms.txt Pages in step.
- Run 39671612886 green.
- 2026-10-21 13:34 PT — EDITOR — cross-links to the AI History generator and Jekyll setup posts from /uses and /changelog (Actions deploy green).
## Done (Oct 21, 2026, 2:34pm PT)
- Memory as Asset TL;DR (had 3 inbound) now linked as "plain-language TL;DR" next to the arXiv citation in VaultMem Part 1, the diary post and VaultMem Part 3. Remaining 3-inbound posts: doing-the-right-thing-fast, reviewing-ai-generated-tests, i-fell-in-love, codex-skills (4).
- Checked: events/now current (Cal Hacks Oct 23–25 next); Gmail last day had no event registrations.
- Run 39680043307 green.
- 2026-10-21 14:34 PT — EDITOR — VaultMem posts link the Memory as Asset TL;DR (/post/vaultmem-encrypted-memory-for-ai-agents/, /post/vaultmem-your-ai-agent-shouldnt-read-your-diary/, /post/vaultmem-part-3-pii-sanitizer/) (Actions deploy green).
## Done (Oct 21, 2026, 3:34pm PT)
- LoCoMo Paper TL;DR: `_includes/diagrams/locomo-benchmark.html` (360×548) after the category list — conversation pill (~300 turns · ~9K tokens avg; S1…S35 session nodes, "up to 35 sessions") → "Three tasks" group (QA highlighted, event summary, dialogue generation) → "Question categories" (single-hop, multi-hop, temporal, open-domain, adversarial dashed). Numbers from the arXiv 2402.17753 abstract (opened this run); categories from the post. Muted text only on `.dg-box`/page bg. Playwright at 375px sepia + dark: scrollWidth 375, no text outside viewBox. Jekyll not installable in sandbox (rubygems unreachable); CI is the build check. Run 39688379264 green.
- Diagram ideas still open: Hopfield store/recall, VaultMem envelope encryption (MEK wrapping).
- 2026-10-21 15:34 PT — DESIGNER — theme-aware LoCoMo benchmark diagram on /post/paper-tldr-locomo-long-term-memory-benchmark/ (Actions deploy green).
## Done (Oct 21, 2026, 4:34pm PT)
- Changelog Atom feed: `feed/changelog.xml` (layout null, sitemap false) renders the latest 50 `_data/changelog.yml` entries — title "Desk: first 12 words", link = entry link (or /changelog/#<date> when none), id `tag:www.avinashgosavi.com,2026:changelog-<n>` counted up from the oldest entry (stable as entries are added on top; don't delete old entries or ids shift), category = desk, HTML content. Linked from /changelog ("Follow the changelog via RSS", reuses `.series-feed-link` + feed icon), `<link rel="alternate">` in the head of /changelog only, and llms.txt. Pre-checked with a python-liquid mock render (50 entries, parses as Atom); existing CI feed step validates every /feed/*.xml. Run 39694508648 green, no link/a11y warnings.

Engineer backlog additions:
- [ ] Changelog feed: entries share a per-day timestamp (date only) — fine for readers; add an optional `time:` field later if ordering within a day matters

- 2026-10-21 16:34 PT — ENGINEER — changelog RSS feed (/feed/changelog.xml), linked from /changelog and llms.txt (Actions deploy green).
## Done (Oct 21, 2026, 5:34pm PT)
- Codex Skills post (3 inbound) now ends with a "Next:" line → Doing the Right Thing, Fast (which names the jira-to-PR skill and the 20–25 work streams, both from that post's own text). Doing the Right Thing, Fast gains a "Related:" line → Are These AI-Generated Tests Good? (description from its front matter). Remaining 3-inbound: i-fell-in-love (well linked from its follow-ups), reviewing-ai-generated-tests (now 4).
- Checked: events/now current (Cal Hacks Oct 23–25 next); Gmail last day had no event registrations.
- Run 39700592831 green.
- 2026-10-21 17:34 PT — EDITOR — cross-links on /post/codex-skills-baking-your-workflow-into-the-tool/ and /post/doing-the-right-thing-fast/ (Actions deploy green).
## Done (Oct 21, 2026, 6:35pm PT)
- daylog security post's closing note now links Live Audio Transcription (the Whisper service extracted from daylog, per that post's intro) — the three daylog posts (security, hobby stack, whisper) now all link each other. Didn't touch the apparent mismatch (security post says voice is transcribed on-device by Apple's neural engine; whisper post is server-side) — Avinash's text, not ours to reconcile.
- Checked: events/now current (Cal Hacks Oct 23–25 next — move to past on the Oct 26 editor shift; only mark attended with evidence); Gmail last day had no event registrations; llms.txt Pages in step.
- Run 39706645214 green.
- 2026-10-21 18:35 PT — EDITOR — daylog security post cross-links the Whisper transcription post (/post/daylog-security-architecture/) (Actions deploy green).
## Done (Oct 21, 2026, 7:35pm PT)
- Hopfield 1982 TL;DR: `_includes/diagrams/hopfield-store-recall.html` (360×478) after "The key insight" — Store pill (Hebbian rule, patterns' weights added, from the post) → "Recall" group with three 5×5 bit grids (noisy cue with 6 flipped → settling with 2 → stored "H"; on = `.dg-head` accent, off = `.dg-node`) → qualitative energy staircase (only goes down or stays — the post's claim; no numbers). Labelled an illustration in the caption. Playwright at 375px sepia + dark: scrollWidth 375, no clipped text. Run 39712339629 green.
- Closes the "Hopfield store/recall" diagram idea. Still open: VaultMem envelope encryption (MEK wrapping) — only if the VaultMem posts describe it.
- 2026-10-21 19:35 PT — DESIGNER — theme-aware store/recall diagram on /post/paper-tldr-hopfield-1982/ (Actions deploy green).
## Done (Oct 21, 2026, 8:34pm PT)
- OpenSearch: root `opensearch.xml` (layout null, sitemap false; ShortName "Avinash Gosavi", template `/search/?q={searchTerms}` — /search/ already reads `?q`, favicon.ico + icon-192 images, rel=self Url, moz:SearchForm). `<link rel="search" type="application/opensearchdescription+xml">` in `_layouts/default.html` head on every page; llms.txt lists it next to the search index. New CI step parses `_site/opensearch.xml` and asserts the search template (fails build if broken). Note: jekyll-seo-tag already emits WebSite JSON-LD on the homepage; SearchAction skipped (Google retired the sitelinks search box in 2024). Run 39717700005 green, OpenSearch/link/a11y/JSON-LD steps all passed.
- 2026-10-21 20:34 PT — ENGINEER — OpenSearch description so browsers can search the site from the address bar (/opensearch.xml, all pages) (Actions deploy green).
## Done (Oct 21, 2026, 9:35pm PT)
- Speculation rules: `_layouts/default.html` ends with `<script type="speculationrules">` — prefetch, eagerness "moderate" (hover ~200ms / pointerdown), same-origin `/*` only, excluding `/feed/*`, `*.xml`, `*.txt`, `*.json`, `/assets/*`, `[download]` and `rel=nofollow` links. No JS; browsers without support ignore it; prefetch doesn't run gtag, so analytics only count real visits. Verified in Playwright Chromium on a static copy: hovering a page link fetched it, hovering a feed link did not, no console errors. `scripts/check_jsonld.py` now also validates every speculationrules block (warning only). Run 39723287146 green.

Engineer backlog additions:
- [ ] If any page ever gets side effects on GET (e.g. a logout or counter URL), add it to the speculation-rules exclusions
- 2026-10-21 21:35 PT — ENGINEER — hover prefetch of internal pages via speculation rules (all pages, default layout) (Actions deploy green).
## Done (Oct 21, 2026, 10:35pm PT)
- /about/: "Off hours" sentence now links encrypted memory for agents → VaultMem Part 1, local-first voice apps → daylog security post (tagged Local-first, voice diary), read papers → /paper-tldr/. Typo "Board games" → "board games". README events roles now list `mentor`.
- Checked: events/now current (Cal Hacks Oct 23–25 next — move to past on the Oct 26 editor shift; only mark attended with evidence); Gmail last day had no event registrations; llms.txt Pages in step; no doubled words or http:// links in posts.
- Run 39728968075 green.
- 2026-10-21 22:35 PT — EDITOR — About page links VaultMem, daylog and the Paper TL;DR series; typo fix (/about/) (Actions deploy green).
## Done (Oct 21, 2026, 11:35pm PT)
- Editor shift had nothing to do (events/now current — Cal Hacks Oct 23–25 next; Gmail last day had no event registrations; codespell clean on posts/pages; llms.txt Pages in step), so took a Designer task: /projects category h2s now show the category icon in the category color. Icon SVG moved to `_includes/project-icon.html` (param `cat`), used by `project-card.html` and `projects.md`; `--cat` mapping is now on any `[data-cat]` (cards + headings). Playwright mock at 375px sepia + dark: no overflow, icon colors match cards. Run 39735204846 green.
- Env note: this sandbox can't reach rubygems or the live site (proxy 403), so no local Jekyll build — CI is the build check; CSS tested on static mocks.
- 2026-10-21 23:35 PT — DESIGNER (editor slot) — category icons on /projects headings (/projects/) (Actions deploy green).
## Done (Oct 22, 2026, 12:35am PT)
- Wide post tables on phones: a python-markdown mock of all 18 post tables at 375px showed 8 overflowing (page scrollWidth up to 584 — Codex skills, Jekyll, AI History, VaultMem 1/2, daylog, Whisper). `_includes/post-tools.html` now wraps every `.post-content table` in `<div class="table-scroll">` (overflow-x auto); a ResizeObserver toggles `.is-wide` and, only when it overflows, `tabindex=0` + `role=region` + aria-label "Table, scrolls sideways". `.is-wide` gets theme-aware edge shadows (background-attachment local/scroll trick, `--bg` + `--text` color-mix). ≤640px: table font 0.875rem, cell padding 0.4/0.55rem. Print: wrapper overflow visible, no shadows. Playwright: scrollWidth 375 in sepia + dark (was 584), 900px has 0 wide tables, no JS errors; text colors unchanged. Run 39741744331 green.

Designer backlog additions:
- [x] Tables are only wrapped by JS — fixed Oct 22, 1:35am PT (server-side wrapper in post layout)
- 2026-10-22 00:35 PT — DESIGNER — wide post tables scroll inside their own box on phones (all /post/* with tables, e.g. /post/codex-skills-baking-your-workflow-into-the-tool/) (Actions deploy green).
## Done (Oct 22, 2026, 1:35am PT)
- No-JS table overflow: `_layouts/post.html` now wraps `<table>` in `<div class="table-scroll">` via Liquid `replace` on `content` (kramdown emits bare `<table>`); `post-tools.html` reuses an existing wrapper (still adds `.is-wide`, tabindex/role/label when it overflows) and wraps any stragglers. Without JS, the box still scrolls (no edge shadows/focus stop). Run 39748954340 green.

Engineer backlog additions:
- [ ] If a post table ever gets a kramdown IAL (`{: .class}`), it renders `<table class=…>` and skips the server wrapper — JS still wraps it
- 2026-10-22 01:35 PT — ENGINEER — post tables wrapped in their scroll box server-side, so phones without JS don't overflow (/post/* with tables) (Actions deploy green).
## Done (Oct 22, 2026, 2:34am PT)
- Reduced motion site-wide: `scroll-behavior: smooth` moved into `@media (prefers-reduced-motion: no-preference)` (anchor jumps, TOC and `scrollIntoView` were smooth for everyone before); a `prefers-reduced-motion: reduce` block at the END of style.css (must stay after the hover rules — same specificity) sets transitions/animations to 0.01ms and cancels the `.project-card:hover` lift and `.site-mark` rotation. Playwright: reduce → transform none, scroll auto; no-preference unchanged. Run 39756689247 green.

Engineer backlog additions:
- [x] Forced-colors (Windows high contrast) pass (done Oct 22, 6:35am PT)
- 2026-10-22 02:34 PT — ENGINEER — site honours prefers-reduced-motion (assets/css/style.css, all pages) (Actions deploy green).
## Done (Oct 22, 2026, 3:35am PT)
- SF Ruby 2025 recap: all 13 bolded talk titles now link to their RubyEvents recordings (paths checked against rubyevents.org/events/sfruby-2025/talks this run; they match `_data/talks.yml`). Post wording kept as-is (e.g. Rachael's talk is "Play with your code" on RubyEvents). Run 39765184302 green.
- Checked: events/now current (Cal Hacks Oct 23–25 next — move to past on the Oct 26 editor shift; only mark attended with evidence); Gmail last day had no event registrations; llms.txt Pages in step.
- 2026-10-22 03:35 PT — EDITOR — SF Ruby recap talks link to recordings (/post/my-sf-ruby-2025-experience-talks-side-quests-community-inspiration/) (Actions deploy green).
## Done (Oct 22, 2026, 4:34am PT)
- Sentence-BERT TL;DR's "Every time Attractor, VaultMem or daylog searches by meaning" line now links all three (Attractor post, /series/#vaultmem, daylog security post); six-papers intro's Sentence-BERT line links daylog (Attractor/VaultMem were already linked elsewhere in it). llms.txt Pages now lists the human /search/ page above the search index.
- Checked: events/now current (Cal Hacks Oct 23–25 next — move to past on the Oct 26 editor shift; only mark attended with evidence); Gmail last day had no event registrations.
- Run 39771761913 green.
- 2026-10-22 04:34 PT — EDITOR — project cross-links on /post/paper-tldr-sentence-bert/ and /post/paper-tldr-six-papers-on-memory/; llms.txt lists /search/ (Actions deploy green).

## Done (Oct 22, 2026, 5:34am PT)

- Designer: `text-wrap: balance` on headings/titles, `text-wrap: pretty` on
  post paragraphs, list items and card descriptions; `::selection` uses
  `--accent-soft` + `--text` (contrast 7.8–9.0:1 in sepia and dark).

## Done (Oct 22, 2026, 6:35am PT)

- Forced colors: `@media (forced-colors: active)` block at the end of
  style.css. Playwright `forced_colors='active'` mock confirmed before: theme
  thumb invisible, active tag chip looked like the rest, glossary/:target
  box-shadow bars gone, diagram muted text near-invisible. Fix: thumb +
  timeline line/dots use CanvasText/Highlight (`forced-color-adjust: none`);
  `.tag-chip.is-active` Highlight/HighlightText; `#site-search`/`#post-search`
  focus get a Highlight outline (they used `outline: none` + tinted ring);
  search `mark` uses Mark/MarkText; event-row/glossary-term/paper/project-card
  `:target` get a Highlight outline; `.diagram svg` and `.notfound-art`
  remap tokens (--text/--text-muted CanvasText, --accent Highlight, fills
  Canvas). Normal-mode screenshot byte-identical before/after.
- Run 39788383066 green.
- 2026-10-22 06:35 PT — ENGINEER — Windows high-contrast (forced colors) support: theme switch, filter chips, search focus, :target highlights and all diagrams (assets/css/style.css, all pages) (Actions deploy green).

## Done (Oct 22, 2026, 7:35am PT)

- Share row on posts (`_includes/share.html`): "Share…" button using
  `navigator.share` (hidden unless supported — phones, Safari/Edge desktop);
  `role="group"` + `aria-labelledby` (aria-label on a plain div was ignored);
  visually-hidden "(opens in a new tab)" on the four external share links;
  polite status region announces "Link copied to clipboard". Playwright mock
  at 375px: button hidden without `navigator.share`, shown with it; copy
  announcement fires. Local Jekyll build not possible (rubygems.org blocked by
  the sandbox proxy; Actions artifact download blocked too) — CI is the build check.
- Run 39797274284 green (queued ~10 min on runners).

Engineer backlog additions:
- [x] (done Oct 22, 9:34am PT) Share: consider the same "(opens in a new tab)" hint for other target=_blank links site-wide (demo/GitHub links on /projects) — check_a11y.py could flag missing hints
- 2026-10-22 07:35 PT — ENGINEER — native "Share…" button and screen-reader announcements on post share row (all /post/* pages) (Actions deploy green).

## Done (Oct 22, 2026, 1:34pm PT)

- now.yml "Reading" item no longer claims he is "writing them up as a Paper
  TL;DR series" (no new TL;DRs since the Oct 20 no-posts rule); it now points
  at the /paper-tldr/ shelf. `updated` → 2026-10-22.
- OSA Con venue from the Oct 22 osacom.io email: AWS Builder Loft, SF. That
  email is titled "Your OSA CON Registration Is Not Yet Complete" — he may need
  to finish registering; do NOT mark OSA Con attended without later evidence.
- Checked: Cal Hacks Oct 23–25 still upcoming (move to past on the Oct 26
  editor shift); no other new registrations in Gmail last 2 days.
- Run 39850170931 green.

## Done (Oct 22, 2026, 8:34am PT)

- Jekyll + GitHub Pages guide's closing note now links Codex Skills (lowest
  inbound post, 2 → 3), wording from the Codex post's own description.
- Checked: events/now current (Cal Hacks Oct 23–25 next — move to past on the
  Oct 26 editor shift; only mark attended with evidence); Gmail last day had no
  event registrations; llms.txt Pages in step.
- Run 39806276219 green.
- 2026-10-22 08:34 PT — EDITOR — Jekyll guide cross-links Codex Skills (/post/building-your-website-with-jekyll-and-github-pages/) (Actions deploy green).

## Done (Oct 22, 2026, 9:34am PT)

- Editor shift had nothing to do (events/now checked an hour ago, codespell
  clean apart from "Rouge", llms.txt in step), so took the Engineer backlog
  item: project cards' Code/Live/Write-up links carry visually-hidden text
  naming the project ("Code for VaultMem on GitHub (opens in a new tab)"),
  social icon aria-labels and the footer Jekyll link say "(opens in a new tab)".
  No other target=_blank links remain without a hint.
- Run 39815307430 green (queued ~12 min on runners).
- 2026-10-22 09:34 PT — EDITOR→ENGINEER — project links name their project for screen readers; new-tab hints on social/footer links (/projects/, homepage, footer) (Actions deploy green).
- 2026-10-22 10:34 PT — DESIGNER — theme-aware sanitizer round-trip diagram on /post/vaultmem-part-3-pii-sanitizer/ (Actions deploy green).
- 2026-10-22 11:34 PT — ENGINEER — language tabs on post code blocks + screen-reader copy announcement (all /post/* with code) (Actions deploy green).
- 2026-10-22 12:35 PT — ENGINEER — tap/Enter to view post images full size (/post/building-rena-ai-health-companion-gemini-live/, VaultMem diary, SF Ruby) (Actions deploy green).
- 2026-10-22 13:34 PT — EDITOR — /now reading item points to Paper TL;DR shelf; OSA Con venue on /events (Actions deploy green).

## Done (Oct 22, 2026, 2:34pm PT)

- Editor shift had nothing to do (events/now checked an hour ago; Gmail last
  day: no new registrations), so took a Designer task: cross-document view
  transitions in style.css (inside `prefers-reduced-motion: no-preference`):
  `@view-transition { navigation: auto }`, 180ms root crossfade, `.site-header`
  gets `view-transition-name: site-header` with a 0s group so it stays put.
  Playwright mock: rules parse, header name is `none` under reduce, navigation
  works, no JS errors. Unsupported browsers just navigate. Run 39858630561 green.

Designer backlog additions:
- [ ] View transitions: if any page ever shows two `.site-header`s, the duplicate name aborts the transition — keep exactly one
- [ ] Skipped this run: About photo `position: sticky` — the About text is only ~250 words, so the photo barely scrolls away; not worth it
- 2026-10-22 14:34 PT — EDITOR→DESIGNER — soft crossfade between pages with a fixed header (assets/css/style.css, all pages) (Actions deploy green).

## Done (Oct 22, 2026, 3:35pm PT)

- VaultMem Part 1: `_includes/diagrams/vaultmem-envelope-encryption.html`
  (360×574) after the MEK paragraph in "How the encryption works" — passphrase
  → Argon2id(passphrase, salt) (64 MiB · 3 iterations) → "In RAM only" group
  (KEK, AES-GCM-Dec(KEK, wrapped_MEK), MEK) → AES-256-GCM(memory atom) (128-bit
  tag, UUID as AAD) → "On disk" (wrapped_MEK + salt, encrypted atoms). All
  facts from the post itself. Playwright 375px sepia + dark: scrollWidth 375,
  no text outside viewBox, muted-on-box 5.7:1 / 5.2:1. Run 39866283386 green.
- Closes the last open diagram idea (LoCoMo, Hopfield, MEK wrapping all done).
- 2026-10-22 15:35 PT — DESIGNER — theme-aware two-layer key diagram on /post/vaultmem-encrypted-memory-for-ai-agents/ (Actions deploy green).

## Done (Oct 22, 2026, 4:34pm PT)

- CI workflow: actions/checkout v4 → v5, upload-pages-artifact v3 → v5
  (Apr 2026, uses upload-artifact v7), deploy-pages v4 → v5 (Node 24) —
  versions confirmed on each action's GitHub releases page this run. v4+ of
  upload-pages-artifact drops dotfiles from the artifact; the site publishes
  none. Run 39872873776 green; the forced-Node-24 annotations are gone (only
  the Ubuntu 26 label notice remains). checkout has v6/v7 too — stayed on v5
  (known Node 24, no other behaviour changes); revisit if it warns.
- Invisible chore, so no changelog entry.
- 2026-10-22 16:34 PT — ENGINEER — CI actions bumped to Node 24 majors (.github/workflows/jekyll.yml) (Actions deploy green).

## Done (Oct 22, 2026, 5:34pm PT)

- Editor shift had nothing to do (Gmail last day: no new registrations — only
  the OSA Con "not yet complete" reminder already logged; Cal Hacks Oct 23–25
  still upcoming; now.yml current; llms.txt Pages in step), so took an
  Engineer task.
- `scripts/check_seo.py` + CI step (continue-on-error): per indexable page
  (skips `noindex` and meta-refresh pages) warns on missing/duplicate
  `<title>`, missing/duplicate meta description, missing canonical, h1 count
  ≠ 1; ::notice for titles > 70 chars before " | Avinash Gosavi" and
  descriptions > 160 chars. Read results via
  `gh api repos/aag1091-alt/avinashgosavi.com/check-runs/<job id>/annotations`
  (job logs blob is 403 through the proxy).
- First run found one real issue: 404.html reused the homepage description.
  404 now has its own description + `noindex: true`; `_layouts/default.html`
  emits `<meta name="robots" content="noindex">` for any page with
  `noindex: true`. Runs 39879106416, 39879430596 green; SEO step 0 problems.

Editor backlog additions (metadata only, small fixes allowed):
- [x] (done Oct 22, 6:34pm PT) Trim over-long meta descriptions (> 160) on homepage (_config.yml
      description, 168), glossary (207), HNSW (234), Generative Agents (191),
      CLS (186), Hopfield 1982 (180) — keep wording from the posts themselves
- 2026-10-22 17:34 PT — EDITOR→ENGINEER — SEO lint in CI; 404 gets its own description + noindex (scripts/check_seo.py, /404.html) (Actions deploy green).

## Done (Oct 22, 2026, 6:34pm PT)

- Editor shift: trimmed every meta description > 160 chars (_config.yml
  homepage, experience, research, talks + 12 posts: glossary, all Paper
  TL;DRs) to 150–159 chars by cutting clauses only — no new claims. Run
  39884898466 green, no SEO description notices left.
- Events: Cal Hacks (Oct 23–25) still upcoming — move to past next editor
  shift after Oct 25 (only mark attended if Gmail supports it).
- 2026-10-22 18:34 PT — EDITOR — Meta descriptions trimmed to ≤160 chars (homepage, /experience, /research, /talks, 12 posts) (Actions deploy green).

## Done (Oct 22, 2026, 7:34pm PT)

- Designer shift: theme-aware, phone-friendly diagram of TimeQueryParser on
  /post/vaultmem-part-2-multimodal-temporal-backends/ (`_includes/diagrams/vaultmem-time-query.html`,
  placed after the `parse_time=True` example). Content only from the post:
  "what happened summer 2019" → time phrase (2019-06-01 → 2019-09-01) +
  remainder embedded → search(parse_time=True). Playwright mock at 375px sepia +
  dark: no text overflow. Run 39890489784 green.
- Note: Playwright needs `executablePath: '/opt/pw-browsers/chromium'` (npm's
  playwright version wants a headless shell that isn't installed).

Designer backlog additions:
- [x] Diagram ideas still open: VaultMem Part 2 query normalizer (done Oct 24, 5:35am PT) (question
      scaffolding stripped before embedding), Whisper WebM header fix (only if
      the post describes the flow step by step)
- 2026-10-22 19:34 PT — DESIGNER — theme-aware time-query diagram on /post/vaultmem-part-2-multimodal-temporal-backends/ (Actions deploy green).

## Done (Oct 22, 2026, 8:35pm PT)

- Engineer shift: `_plugins/git_last_modified.rb` (no new gem) sets
  `last_modified_at` on posts/pages from their last git commit (front matter
  wins; posts only when the commit is after the publish date). Feeds
  jekyll-sitemap `<lastmod>` (pages had none before), jekyll-seo-tag
  `dateModified` on posts, and jekyll-feed/series-feed `<updated>`.
  Checkout uses `fetch-depth: 0`. New CI step (continue-on-error) emits a
  `::notice title=sitemap::` — run 39896367595: 43 urls, 0 without lastmod.
- Can't build locally (rubygems 403 via proxy) and can't fetch the live site
  or the Pages artifact from the sandbox — read CI annotations instead.
- Invisible (SEO metadata), so no changelog entry.

Engineer backlog additions:
- [ ] Posts could show "Updated <date>" from `last_modified_at` — skipped:
      metadata-only commits (description trims) would mark every post updated;
      would need a front-matter `updated:` set by hand for real content edits
- 2026-10-22 20:35 PT — ENGINEER — sitemap lastmod + post dateModified from git history (_plugins/git_last_modified.rb, sitemap.xml) (Actions deploy green).

## Done (Oct 22, 2026, 9:34pm PT)

- Engineer shift: `_includes/social-icons.html` GitHub/LinkedIn/X links now
  `rel="me noopener"` (header/footer and homepage), so profiles that check
  rel=me (GitHub, Mastodon/IndieWeb parsers) can verify the site is his.
  Invisible to readers, so no changelog entry. Run 39901119149 green.

Engineer backlog additions:
- [ ] If Avinash ever adds a Mastodon/Bluesky profile, add it to
      social_links + person-jsonld sameAs with rel="me"
- 2026-10-22 21:34 PT — ENGINEER — rel="me" on social profile links (_includes/social-icons.html, all pages) (Actions deploy green).

## Done (Oct 22, 2026, 10:34pm PT)

- Editor shift had nothing to do: events/now current (Cal Hacks 13.0 starts
  Oct 23 — still upcoming; move to past after Oct 25), Gmail last day had no
  new registrations, llms.txt page list matches real pages.
- Fell through to Engineer: About page now emits ProfilePage JSON-LD whose
  mainEntity is the same Person (from `_includes/person-jsonld.html`, now one
  `capture` used by both the homepage Person and the About ProfilePage; Person
  has `@id` `<site>/#person`). Included from `_layouts/default.html` when
  `page.layout == "about"` (page.url is /about.html, not /about/).
  `scripts/check_jsonld.py` warns if a ProfilePage lacks a named Person
  mainEntity. Invisible, so no changelog entry. Run 39906647710 green, JSON-LD
  step passed.

Editor backlog additions:
- [ ] After Oct 25: move Cal Hacks 13.0 to past and drop its /now item
      (mark "mentored" only if Gmail confirms participation)
- 2026-10-22 22:34 PT — EDITOR→ENGINEER — ProfilePage structured data on /about (_includes/person-jsonld.html, _layouts/default.html) (Actions deploy green).

## Done (Oct 22, 2026, 11:34pm PT)

- Editor shift had nothing to do: events/now current (Cal Hacks 13.0 Oct
  23–25 still upcoming), Gmail last day had no new event registrations,
  codespell clean (only "Rouge" false positives), llms.txt in step.
- Fell through to Engineer: `/feed.json` — JSON Feed 1.1 of the latest 20
  posts (summary, tags, date_modified from git, full `content_html` with
  root-relative href/src made absolute since JSON Feed has no xml:base;
  per-post `image` only when it isn't the site default). Autodiscovery
  `<link rel="alternate" type="application/feed+json">` in default.html head;
  listed in llms.txt; new CI step asserts it parses, version 1.1, and has no
  root-relative links left. Run 39912528445 green.

Engineer backlog additions:
- [ ] Series JSON feeds (feed/<slug>.json) only if someone asks — Atom covers it
- 2026-10-22 23:34 PT — EDITOR→ENGINEER — JSON Feed at /feed.json (feed.json, _layouts/default.html, llms.txt, CI check) (Actions deploy green).

## Done (Oct 23, 2026, 12:34am PT)

- Designer shift: theme-aware WebM chunk diagram on the Whisper post
  (`_includes/diagrams/whisper-webm-chunks.html`, placed after the
  accumulated-audio code block so his text is unchanged): header-only-in-chunk-1,
  lone chunk → ffmpeg can't decode, accumulated 1 / 1+2 / 1+2+3 → valid WebM,
  transcript replaces. Content only from the post. Contrast (Playwright mock):
  body text 11.5/12.4:1, notes/labels 6.3/5.8:1 on bg (sepia/dark), ≥5.2:1 on box
  fill; no text overflow, no horizontal scroll at 375px. Run 39918933501 green.
- Tip: monochrome text inside a `.dg-pill` → `class="dg-body dg-mono"` (dg-mono
  alone has no fill, so SVG's default black would vanish in dark). Local
  `jekyll` isn't installed; mock pages with `<body class="theme-sepia|theme-dark">`
  + style.css are enough for diagram checks.

Designer backlog additions:
- [x] Diagram ideas still open: VaultMem Part 2 query normalizer (done Oct 24, 5:35am PT)
- 2026-10-23 00:34 PT — DESIGNER — theme-aware WebM chunk diagram on /post/live-audio-transcription-whisper/ (Actions deploy green).

## Done (Oct 23, 2026, 1:34am PT)

- Engineer shift: /search/ result links for items with body text (posts,
  pages) now end in a text fragment `#:~:text=<matched word + up to 2 words>`
  (`fragment()` in search.md), so the target opens scrolled to the match with
  the browser's native highlight. Expands partial terms to the full word (text
  fragments need word boundaries), stops at punctuation, encodes `-`. Skipped
  for URLs that already carry `#id` (projects/papers/events). Unsupported
  browsers/failed matches just open at the top; Chromium strips the directive
  from location.hash (page-anchors.html uses getElementById, safe anyway).
  Tested in Playwright Chromium: click scrolls to the phrase. Run 39925819109
  green.

Engineer backlog additions:
- [x] Search: if text-fragment misses turn up (phrase spans a block boundary
      in the rendered post), fall back to the single matched word (done Oct 25, 9:34am PT)
- 2026-10-23 01:34 PT — ENGINEER — search results open posts scrolled to the matched words via text fragments (search.md) (Actions deploy green).

## Done (Oct 23, 2026, 2:34am PT)

- Engineer shift: smart 404. `404.html` script tokenizes the missing path
  (drops post/html/stopwords/numbers), fetches /search.json, scores items by
  exact/prefix word hits in URL slug (×3), title (×2), tags (×1); shows up to 3
  in "Maybe you were looking for" (needs ≥2 matched words, or score ≥5 for a
  single distinctive word) with type + date. "Search the site" link gets
  `?q=<path words>`. Fails silently (generic list stays). Taken-down projects
  aren't in search.json, so they're never suggested.
- Bug fixed: 404 links had no theme color (browser-default blue in sepia,
  lavender in dark) — `.notfound-page a` now uses --accent-ink. Suggestion box
  is left-border only: muted text on the tinted fill was 3.66:1 in dark; now
  link 6.6/7.4:1, meta 6.3/5.8:1 (sepia/dark). Playwright mock at 375px: no
  horizontal scroll, no JS errors. Run 39933291965 green.
- 2026-10-23 02:34 PT — ENGINEER — 404 suggests closest pages from the broken URL + theme-colored links (404.html, assets/css/style.css) (Actions deploy green).

## Done (Oct 23, 2026, 3:35am PT)

- Editor shift: upcoming events in `_data/events.yml` now carry exact dates in
  `when` (Cal Hacks "Oct 23–25, 2026", OSA Con "Nov 2, 2026", HackUMass "Nov 15,
  2026" — same dates as now.yml). Past events keep "Mon YYYY". When an event
  moves to past, shorten `when` back to "Mon YYYY". now.yml `updated` →
  2026-10-23 (all items current; Cal Hacks underway Oct 23–25 — move it to past
  on Oct 26 and drop the Mentoring Now item; role stays mentor, no "attended"
  claims without evidence). Gmail last day: no new registrations (IEEE Oct 27
  panel is promo; OSA Con "not yet complete" reminder already logged).
  Run 39940266488 green.
- 2026-10-23 03:35 PT — EDITOR — exact dates for upcoming events (/events/); /now updated date (Actions deploy green).

## Done (Oct 23, 2026, 4:34am PT)

- Editor slot (UTC 11) → Engineer: events/now were updated an hour ago,
  llms.txt pages match real pages, codespell over posts/data/pages finds only
  "Rouge"/"Master [key]" false positives — nothing editorial to do.
- Engineer shift: stylesheet cache-busting. New `_plugins/asset_version.rb`
  Liquid filter `asset_version` appends `?v=<first 10 hex of MD5>` of the
  source file; `_layouts/default.html` uses
  `{{ '/assets/css/style.css' | asset_version | relative_url }}`. Hash only
  changes when the CSS bytes change, so after a deploy returning visitors get
  new CSS at once (GitHub Pages caches assets 10 min) instead of new HTML with
  stale CSS. New CI step asserts the homepage link's hash equals the built
  style.css MD5 (blocking — it's our own build, no network). Fonts are
  referenced from the CSS and don't need versions (file names never change).
  Runs 39947301176 + 39947653564 green. Invisible chore → no changelog entry.

Engineer backlog additions:
- [ ] Use `asset_version` for any new local CSS/JS file added later
- 2026-10-23 04:34 PT — EDITOR→ENGINEER — content-hash cache-busting for style.css + CI check (_plugins/asset_version.rb, _layouts/default.html, all pages) (Actions deploy green).

## Done (Oct 23, 2026, 5:34am PT)

- Designer shift: theme-aware, phone-friendly diagram on the Sentence-BERT
  TL;DR (`_includes/diagrams/sbert-cross-vs-siamese.html`, placed after "drops
  to about 5 seconds" so his text is unchanged): plain BERT reads A+B together
  → one score per pair (10,000 sentences ≈ 50M passes ≈ 65 h, nothing
  precomputable) vs Sentence-BERT siamese BERT + pooling with shared weights →
  vectors u, v → cosine similarity (≈ 5 s). Content only from the post (which
  cites arXiv 1908.10084). viewBox 312 wide. Playwright mock at 375px: body
  text 11.5/12.4:1, notes 6.3/5.8:1 (sepia/dark), no overflow, no horizontal
  scroll. Run 39954633197 green.
- Tip: a double-headed arrow across a <30px gap overlaps its heads — use a
  plain dashed connector instead.
- Note: the clone was on a detached HEAD; `git push origin HEAD:main` worked.

Designer backlog additions:
- [ ] Posts still without a diagram: Modern Hopfield TL;DR, Memory as Asset,
      daylog security architecture, Rena — only if the post describes a flow
- 2026-10-23 05:34 PT — DESIGNER — theme-aware plain-BERT vs Sentence-BERT diagram on /post/paper-tldr-sentence-bert/ (Actions deploy green).

## Done (Oct 23, 2026, 6:35am PT)

- Engineer shift: theme stays in step across tabs. `_includes/theme-toggle.html`
  listens for `storage` events on `blog_color_theme` (another tab toggled) and
  `pageshow` with `persisted` (back/forward-cache restore after toggling on
  another page) and re-applies the stored theme (body class, slider, both
  metas) without re-writing storage. Playwright on a mock page: toggle in tab
  1 → tab 2 flips to dark and back; toggle on page B then Back → page A dark;
  no JS errors. Run 39962571648 green.
- 2026-10-23 06:35 PT — ENGINEER — theme toggle syncs across open tabs and back/forward-cache restores (_includes/theme-toggle.html) (Actions deploy green).

## Done (Oct 23, 2026, 7:35am PT)

- Engineer shift: glossary term previews. `_includes/post-tools.html` finds
  post links to `/post/agent-memory-glossary/#<id>` (not on the glossary
  itself); on mouse hover (250ms delay, `(hover: hover) and (pointer: fine)`
  only) or keyboard `:focus-visible` it fetches the glossary page once
  (DOMParser), and if the target is a `.glossary-term` paragraph shows a
  `role=tooltip` card (#term-preview, `aria-describedby` on the link) with the
  bold term + definition text (≤260 chars, plain text, no links inside).
  Hoverable (moving into the card keeps it), Esc / blur / scroll dismiss;
  heading anchors (#storing-and-finding-memories) and missing ids show nothing.
  Touch taps unchanged. CSS `.term-preview` (surface bg, accent left border,
  hidden in print). Playwright mock at 375/1200 sepia+dark: card inside
  viewport (16px gutters), no horizontal scroll, no JS errors; text/surface
  ≈11:1 sepia, ≈14:1 dark. Run 39971371306 green.

Engineer backlog additions:
- [x] Term previews extended to post-to-post links (done Oct 23, 8:35am PT)
- 2026-10-23 07:35 PT — ENGINEER — glossary term definitions on hover/focus in posts (_includes/post-tools.html, assets/css/style.css) (Actions deploy green).

## Done (Oct 23, 2026, 8:35am PT)

- Editor slot (UTC 15) → Engineer: events/now current (Cal Hacks underway
  Oct 23–25 — move to past Oct 26 and drop the Mentoring Now item); Gmail last
  day has no new registrations (OSA Con "not yet complete" + IEEE Oct 27 promo
  already logged); llms.txt pages match; no unlinked mentions of posts in other
  posts. External link check isn't possible from the sandbox (proxy returns
  000/403 for every external host) — rely on CI.
- Engineer shift: link previews for post-to-post links. `_includes/post-tools.html`
  preview block now also covers `.post-content` links to any other `/post/...`
  page (not the current one): on hover (250ms, fine pointer only) or
  :focus-visible it fetches /search.json once, maps type=Post by url (also tries
  a trailing slash), and shows title + desc (≤200 chars) + date line
  (`.term-preview-meta`, --text-muted: 5.5:1 sepia, 6.6:1 dark on --surface).
  Glossary term links unchanged; unknown posts and self-links show nothing.
  Playwright mock sepia 1200 / dark 375+1200: previews correct, keyboard
  aria-describedby set, no horizontal scroll, no JS errors. Run 39980018894 green.
- 2026-10-23 08:35 PT — EDITOR→ENGINEER — post-to-post link previews (title, summary, date) on hover/focus (_includes/post-tools.html, assets/css/style.css) (Actions deploy green).

## Done (Oct 23, 2026, 9:35am PT)

- Editor slot (UTC 16) → Engineer: events/now/llms.txt were checked an hour
  ago and nothing has changed (Cal Hacks still underway until Oct 25).
- Engineer shift: "pick up where you left off" on long posts (those with the
  TOC box, ≥1,200 words). `_includes/post-tools.html` saves the last h2/h3 id
  above 30% of the viewport (400ms debounce) to localStorage `post_resume`
  ({path: {id, t}}, newest 30, ≤60 days); reaching the end of .post-content
  or scrolling above the first heading clears it. Next visit (no URL hash,
  saved id ≠ first heading, id still on page) shows `.resume-reading` above
  the TOC: link to `#id` + × dismiss (clears). All storage in try/catch.
  CSS: surface fill, accent left bar, link --accent-ink 5.7:1 sepia / 8.4:1
  dark, × --text-muted 5.5 / 6.6:1; hidden in print. Playwright mock at 375
  sepia/dark + 1200 dark: saves, note shows, click jumps + removes note, end
  clears, no horizontal scroll, no JS errors. Run 39988376569 green.
- Note: no local Jekyll (rubygems unreachable) — keep testing with mocks.

Engineer backlog additions:
- [ ] Resume note: if posts' heading ids ever change (renamed headings), stale saved ids simply show nothing — fine
- 2026-10-23 09:35 PT — EDITOR→ENGINEER — long posts offer "pick up where you left off" (_includes/post-tools.html, assets/css/style.css) (Actions deploy green).

## Done (Oct 23, 2026, 10:35am PT)

- Designer shift: the daylog security post's hand-coded 700×290 inline SVG
  (hard-coded light pastels, 8–10px text → ~4px on phones, legend text low
  contrast in dark) replaced with `_includes/diagrams/daylog-entry-path.html`:
  five stacked layers (You → Browser → HTTPS → Vault → Stored on disk) with a
  "Save" down-arrow on the left and "Read" up-arrow on the right; same facts and
  labels as the old figure (kept "text + vector encrypted" because the post's
  next paragraph quotes it). viewBox 336 wide, title/desc for screen readers.
  New CSS `.dg-ink` (note-size text in --text) for text on --accent-soft fills:
  --text-muted there is only 3.7:1 in dark. Playwright at 375px sepia/dark: no
  text outside its box, no horizontal scroll; notes on boxes 5.7/5.2:1. Run
  39996600368 green.

Designer backlog additions:
- [x] Other posts with old hard-coded inline SVGs: none left (checked Oct 23, 10:35am PT)
- 2026-10-23 10:35 PT — DESIGNER — phone-friendly, theme-aware entry-path diagram replaces the tiny hard-coded one on /post/daylog-security-architecture/ (Actions deploy green).

## Done (Oct 23, 2026, 11:35am PT)

- Engineer shift: /blog filters gave no feedback to screen readers and topic
  chips didn't change the URL. Now a `role=status` line (`#post-count`,
  `.blog-count`) says "Showing N of M posts tagged “X” matching “q”." (debounced
  400ms while typing; "No posts match." is visually hidden since the visible
  no-results line already shows), and chip clicks `history.replaceState` the
  `#tag` hash (All clears it); `hashchange` re-applies a filter. Tested with a
  Playwright mock (hash load, click, type, no match, All, hashchange; no JS
  errors). Run 40004737946 green.

Engineer backlog additions:
- [x] /blog search text in the URL (`?q=`) (done Oct 23, 12:35pm PT)
- 2026-10-23 11:35 PT — ENGINEER — /blog shows a live "Showing N of M posts" count for filters/search and topic chips update the #tag URL (blog.md, assets/css/style.css) (Actions deploy green).

## Done (Oct 23, 2026, 12:35pm PT)

- Engineer shift: /blog search lives in the URL. Typing updates `?q=` via
  `history.replaceState` (400ms debounce; keeps the `#tag` hash; empty box
  drops `q`); chip clicks rebuild the URL the same way (`syncUrl()`); on load
  `?q=` fills the box and filters (then `#tag` applies). The no-results
  "Search projects, papers and pages too →" link now carries `?q=<words>` to
  /search/. Playwright mock: `/blog/?q=hopfield#ruby` filters both, typing
  updates URL, All keeps q, clearing restores `/blog/`, no JS errors. Run 40627746923 green.
  Run 40012728937 green.
- 2026-10-23 12:35 PT — ENGINEER — /blog search kept in the URL (?q=) and handed to /search/ on no results (blog.md) (Actions deploy green).

## Done (Oct 23, 2026, 1:35pm PT)

- Editor slot (UTC 20) → Engineer: events/now current (Cal Hacks Oct 23–25
  underway, OSA Con Nov 2, HackUMass Nov 15); Gmail last 2 days: no new
  registrations (IEEE Oct 27 panel promo; OSA Con "not yet complete" reminder
  already logged); llms.txt covers every page; older posts' cross-links already
  swept. /paper-tldr/ items now show a `.tldr-paper` line — authors · year ·
  venue linking the original paper — joined from `_data/papers.yml` via
  `where: "tldr_post", p.url` (the six-papers overview has no match, so no
  line). Link text = venue, aria-label "<venue>: read the original paper".
  Couldn't build locally (rubygems unreachable from sandbox); CI built it.
  Run 40020628533 green, no lint warnings.

Backlog notes:
- [x] Events rows have ids + search Event entries point at /events/#slug (already done; line ~253 stale)
- [x] Search indexes /projects/#slug anchors (already done; line ~176 stale)
- 2026-10-23 13:35 PT — EDITOR→ENGINEER — Paper TL;DR list shows each paper's authors, year and a link to the original (/paper-tldr/) (Actions deploy green).

## Done (Oct 23, 2026, 2:34pm PT)

- Editor slot (UTC 21) → Designer: events/now checked an hour ago and still
  current (Cal Hacks Oct 23–25 underway); nothing for the editor desk. Post
  prose links (`.post-content a`) were marked by color only — link vs body
  text is 1.75:1 sepia / 1.69:1 dark (WCAG 1.4.1 wants a non-color cue). Now a
  1px underline at 55% of the link color (`color-mix`, full-color fallback),
  offset 0.2em, full color on hover/focus-visible. Heading `#` anchors stay
  undecorated (higher specificity); resume/back-to-top links live outside
  `.post-content`. Playwright mock at 375px sepia + dark: computed styles as
  expected. Run 40028011958 green.

Designer backlog additions:
- [x] Same color-only link cue may exist on /about prose and footer inline links (done Oct 23, 3:34pm PT)
- 2026-10-23 14:34 PT — EDITOR→DESIGNER — soft underline on links in post prose so they're not marked by color alone (assets/css/style.css, all /post/*) (Actions deploy green).

## Done (Oct 23, 2026, 3:34pm PT)

- Designer shift (UTC 22): plain links outside post prose had NO CSS rule, so
  /about, page ledes (blog, events, now, talks, series, changelog, paper-tldr),
  /uses, /research lists, read-next/series-box lists, changelog "See" links etc.
  showed the browser default blue #0000EE / visited purple (dark: #9e9eff).
  Added `:where(.main :is(p, li, dd, blockquote, td) a:not([class]))` (zero
  specificity, so every component rule like `.post-list-item a` still wins):
  accent-ink color + the 55% soft underline from post prose, full on
  hover/focus. Footer inline "Jekyll" link (`.site-footer p a`) underlined too;
  footer nav stays plain. Playwright mock sepia + dark at 375px: about/lede/
  footer links teal #0a5f58 (≈6.7:1 on bg) / gold #d4b078 (≈7.9:1); post-list,
  project-links, all-posts-link, footer nav unchanged. Run 40034846618 green.

Designer backlog additions:
- [x] Lone "→" link on /now items now gets an underline (done Oct 23, 5:35pm PT)
- 2026-10-23 15:34 PT — DESIGNER — theme-colored soft underline for plain links in page text and footer instead of browser blue (assets/css/style.css; /about/, /uses/, /research/, page ledes) (Actions deploy green).

## Done (Oct 23, 2026, 4:34pm PT)

- Engineer shift (UTC 23): three visible dates were plain text — /changelog
  day headings, the /now "Updated" line and /series part dates. Now wrapped in
  `<time datetime>` (YYYY-MM-DD for changelog/now, `date_to_xmlschema` for
  series), matching posts, /blog, homepage and /paper-tldr. New
  `time-datetime` rule in `scripts/check_a11y.py` warns on any `<time>` without
  an ISO datetime (outside SVG); tested on a mock (catches missing, "Oct 2026",
  space-before-zone). Run 40040649691 green, no time-datetime warnings.
  Invisible to readers, so no changelog entry.
- Events: Cal Hacks (Oct 23–25) still upcoming/underway — move to past Oct 26.
- 2026-10-23 16:34 PT — ENGINEER — machine-readable <time> dates on /changelog/, /now/, /series/ + a11y lint rule (scripts/check_a11y.py) (Actions deploy green).

## Done (Oct 23, 2026, 5:35pm PT)

- Editor slot (UTC 00) → Designer: events/now still current (Cal Hacks Oct
  23–25 underway — move to past and drop the Mentoring Now item on Oct 26);
  Gmail last 2 days: no new event registrations; llms.txt pages complete.
  /now arrow-only "→" links picked up the new soft underline (looked like a
  stray dash). Added `.now-more` class (now.md): no underline, 24×24px tap
  target (WCAG 2.5.8), accent-ink color, 3px nudge on hover (off under
  prefers-reduced-motion), focus-visible outline. Homepage Now has no arrows.
  Run 40045786265 green.
- 2026-10-23 17:35 PT — EDITOR→DESIGNER — /now arrow links: no underline, 24px tap target, hover nudge (now.md, assets/css/style.css) (Actions deploy green).

## Done (Oct 23, 2026, 6:35pm PT)

- Editor slot (UTC 01) → Engineer: events/now still current (Cal Hacks Oct
  23–25 underway); Gmail last day: no event registrations; codespell: only
  "Rouge" false positives. Stale backlog items checked and already done:
  theme-color/color-scheme (line ~297), theme flash (line ~330).
  Backlog line ~409 (JS-built links): /search's `role=status` line updated on
  every 120ms keystroke render, so screen readers heard a count per letter.
  New `say(msg, wait)` in search.md delays the live-region text 400ms while
  typing (results still draw at once); load, chips, Enter, Esc and errors
  announce immediately. Post TOC current section now `aria-current="location"`
  (was "true"; CSS keys off `[aria-current]`, unchanged). Playwright mock: load,
  typing (+250ms empty, +650ms "1 result for “memo”"), chip, Esc; no JS errors. Run 40627746923 green.
  Run 40050634537 green.
- [x] Backlog line ~409 reviewed: search result titles and TOC links have real
  text; no other gaps found in JS-built links.
- 2026-10-23 18:35 PT — EDITOR→ENGINEER — /search result count announced after typing pauses; TOC current section is aria-current=location (search.md, _includes/post-tools.html) (Actions deploy green).

## Done (Oct 23, 2026, 7:34pm PT)

- Designer shift (UTC 02): the Modern Hopfield TL;DR
  (/post/paper-tldr-hopfield-networks-is-all-you-need/) had no diagram. New
  `_includes/diagrams/modern-hopfield-one-step.html` after the NumPy demo:
  noisy state ξ = query (40% flipped, overlap 14/64) → compare with x₁…x₅
  (keys) → softmax bars (≈0.97 on x₃, "crumbs" elsewhere) → blend (values) →
  new state ≈ x₃ (overlap 64/64), plus the attention mapping (β = 1/√d,
  K = V = patterns). All numbers are the post's own demo output. Note: the
  demo's "14 / 64" is a ±1 dot-product overlap, not "bits matching" — the
  diagram says "overlap". New CSS `.dg-bar` (accent fill) for qualitative
  bars. Uppercase `.dg-label` turns β into "Β" (looks like B) — keep Greek
  letters out of labels. Playwright 375px sepia/dark: no text outside the
  viewBox, no horizontal scroll. Run 40054886195 green.

Designer backlog additions:
- [ ] Posts still without a diagram: Memory as Asset, Rena — only if the post describes a flow (Modern Hopfield done Oct 23, 7:34pm PT)
- 2026-10-23 19:34 PT — DESIGNER — theme-aware one-step recall diagram on /post/paper-tldr-hopfield-networks-is-all-you-need/ (Actions deploy green).

## Done (Oct 23, 2026, 8:35pm PT)

- Engineer shift (UTC 03): editors hand-check that /llms.txt lists every page
  each run. New `scripts/check_llms.py` (stdlib, offline; CI step after the
  SEO lint, `continue-on-error: true`, `--strict` available) warns when a
  sitemap.xml URL isn't linked from /llms.txt, and when /llms.txt or
  /llms-full.txt links an on-site path that wasn't built (treats /x/,
  /x/index.html and /x.html as one page). ::warning annotations + job summary.
  Tested on a mock _site (missing page, dead page, dead image, strict exit 1).
  Run 40059010088 green; step passed with no llms.txt annotations, so the
  page list is currently complete. Invisible, so no changelog entry.

Editor note:
- [ ] llms.txt completeness is now in CI — read the run's annotations instead of diffing pages by hand
- 2026-10-23 20:35 PT — ENGINEER — CI check that /llms.txt lists every sitemap page and has no dead links (scripts/check_llms.py, .github/workflows/jekyll.yml) (Actions deploy green).

## Done (Oct 23, 2026, 9:35pm PT)

- Engineer shift (UTC 04): offline support. `sw.js` (root, Liquid-rendered;
  registered on load from `_layouts/default.html`): navigations are network
  first (navigation preload on); each successful same-origin HTML page is
  copied to cache `pages-v1` (key = path without query, newest 40); on
  network failure the saved copy is served, else `/offline/`. Only
  `/assets/css/` and `/assets/fonts/` are cache-first (style.css is
  content-hashed); images, feeds, JSON and analytics are untouched. `static-<build
  time>` precaches /offline/, style.css?v=, the DM Sans latin font; old
  static caches deleted on activate. New `offline.html` (/offline/, noindex,
  sitemap false): "Try again" button (44px, accent-ink), reloads on the
  `online` event, lists "Saved on this device" from `pages-v1` titles.
  Playwright mock at 375px: visit /a/ + /b/, go offline → /a/ served from
  cache, unknown URL → offline page listing both, no horizontal scroll, no JS
  errors. Run 40063056801 green, no lint warnings.
- Kill switch (if the SW ever misbehaves): replace sw.js body with
  install→skipWaiting + activate→`self.registration.unregister()` (see the
  comment at the top of sw.js). Keep the file at the same URL.

Engineer backlog additions:
- [ ] If pages ever get personalised/side-effect content, exclude them from the `pages-v1` cache in sw.js
- [ ] Offline: could precache the homepage + /blog/ on install (skipped: only pages the visitor opened are kept)
- 2026-10-23 21:35 PT — ENGINEER — offline support: visited pages readable without a connection + /offline/ fallback (sw.js, offline.html, _layouts/default.html) (Actions deploy green).

## Done (Oct 23, 2026, 10:34pm PT)

- Editor slot (UTC 05) → Engineer had nothing worthwhile → Designer. Editor
  checks: events/now current (Cal Hacks Oct 23–25 underway — move to past and
  drop the Mentoring Now item on Oct 26); Gmail last 2 days: no new event
  registrations (OSA Con "not yet complete" reminder already logged); no
  http:// links in posts/pages/data. Backlog line 70 checked: only SF Ruby 2025
  has a recap post; it doesn't cover Hack Day or the AI Hackathon, so no other
  event gets a recap link. Local Jekyll build impossible (rubygems unreachable).
- Designer: new `_includes/diagrams/memory-as-asset-layers.html` on
  /post/paper-tldr-memory-as-asset/ (after "The three layers"): memory object
  chips (content, context, version; owner + access policy highlighted) →
  1 Personal storage (pill, "VaultMem: encrypted with your key") ↔ 2 Evolution
  (record · merge · abstract, local or remote) ↔ 3 Memory exchange network
  (dashed `.dg-box.dg-muted`, "sketched in the paper, not solved"). All text
  from the post itself. Playwright 375px theme-sepia + theme-dark: no text
  outside the viewBox, no horizontal scroll. Mock pages need `body.theme-sepia`
  (bare :root is a blue theme) and must be loaded via goto(file://), not
  setContent, or the stylesheet won't load. Run 40067088696 green.

Designer backlog:
- [x] Memory as Asset diagram (done Oct 23, 10:34pm PT) — Rena is the last post without one; only if it describes a flow
- [x] Events: link any other event to a recap if a post exists (checked Oct 23, 10:34pm PT — none)
- 2026-10-23 22:34 PT — EDITOR→DESIGNER — theme-aware memory-object + three-layer diagram on /post/paper-tldr-memory-as-asset/ (Actions deploy green).

## Done (Oct 23, 2026, 11:35pm PT)

- Editor slot (UTC 06): nothing needed → Designer. Editor checks: events/now
  current (Cal Hacks Oct 23–25 still underway — move to past and drop the
  Mentoring Now item on Oct 26); Gmail last 2 days: no new event registrations
  (OSA Con "not yet complete" reminder already logged); llms.txt covers every
  page (/offline/ is noindex, correctly absent).
- Designer: new `_includes/diagrams/rena-voice-session.html` replaces the
  ~70-char "Voice session data flow" ASCII block on
  /post/building-rena-ai-health-companion-gemini-live/ (it scrolled sideways
  at 375px). Stack: You tap Rena (/ws/{user_id}?context={tab}&tz=…) → Backend
  loads [RENA MEMORY] + tab prompt → PCM 16 kHz → ADK → Gemini Live (intent →
  tool) → tool_status live save indicator | Tool writes to Firestore → reply,
  24 kHz chunks · AVAudioEngine. All facts from the post's own text. The big
  architecture ASCII block is untouched. Playwright 375px sepia/dark: no text
  outside the viewBox, no horizontal scroll. Run 40070894690 green.

Designer backlog:
- [x] Rena diagram (done Oct 23, 11:35pm PT) — every post with a flow now has a theme-aware diagram
- [x] Rena: the larger "Architecture" ASCII block also scrolls at 375px (done Oct 24, 12:35am PT) — could become a diagram (client → Cloud Run agent with ADK tools → Firestore / Gemini APIs / Cloud Storage)
- 2026-10-23 23:35 PT — EDITOR→DESIGNER — theme-aware voice-session diagram on /post/building-rena-ai-health-companion-gemini-live/ (Actions deploy green).

## Done (Oct 24, 2026, 12:35am PT)

- Designer shift (UTC 07): new `_includes/diagrams/rena-architecture.html`
  replaces the ~70-char "Architecture" ASCII box on
  /post/building-rena-ai-health-companion-gemini-live/ (scrolled sideways at
  375px). iOS app / web PWA pill ↔ (WebSocket audio · REST data) ↔ dashed
  "Rena agent · Cloud Run" group with two boxes (Google ADK agent core + all 9
  tool names in mono; Context prompt system: prompts in Firestore, [RENA
  MEMORY], per-tab contexts, tool_status) → left spine to Firestore / Gemini
  APIs / Cloud Storage rows. All text from the post's own ASCII block.
  Playwright 375px sepia + dark: no text outside the viewBox, no horizontal
  scroll. Run 40074864708 green. The Rena post now has no wide ASCII flow
  blocks left except the numbered video-pipeline steps (plain text, wraps).

Designer backlog:
- [x] Look for other posts whose fenced ```text/ASCII blocks are wider than ~45 chars and scroll at 375px (checked Oct 24, 5:35pm PT: only the VaultMem key chain — already diagrammed below it — and the .vmem file tree remain; both are his own text, left as is)
- 2026-10-24 00:35 PT — DESIGNER — theme-aware architecture diagram on /post/building-rena-ai-health-companion-gemini-live/ (Actions deploy green).

## Done (Oct 24, 2026, 1:34am PT)

- Engineer shift (UTC 08): wide code blocks weren't reachable by keyboard
  (Safari never focuses scrollers; ~10 posts have code lines > 60 chars).
  `_includes/post-tools.html` now checks every `pre` in `.post-content`: when
  scrollWidth > clientWidth it gets tabindex=0, role=region and aria-label
  "<lang> code, scrolls sideways" (plain "Code" for text/no-lang blocks);
  removed again when it fits (ResizeObserver), same pattern as wide tables.
  Runs before the clipboard early-return, so it works without the Clipboard
  API. Focus ring comes from the global `:focus-visible`. Playwright mock at
  375px + 1200px: Tab lands on the wide block, ArrowRight scrolls it (80px),
  short block untouched, no JS errors. Run 40078749172 green.
- Not done: shortening the 6 SEO titles > 70 chars (check_seo notices) —
  would change his visible post titles; leave unless Avinash asks.

Engineer backlog additions:
- [x] a11y lint can't see JS-added scroll regions — covered by check_browser.py `scroll-focus` rule
- 2026-10-24 01:34 PT — ENGINEER — wide code blocks in posts keyboard-scrollable and labelled for screen readers (_includes/post-tools.html) (Actions deploy green).

## Done (Oct 24, 2026, 2:34am PT)

- Engineer shift (UTC 09): every run's annotations carried GitHub's notice
  that `ubuntu-latest` migrates to Ubuntu 26 from Oct 19, 2026 — a surprise
  image switch could break `ruby/setup-ruby` (Ruby 3.4 prebuilt) and block
  deploys. Build and deploy jobs in `.github/workflows/jekyll.yml` now pin
  `runs-on: ubuntu-24.04` (commented). Invisible, so no changelog entry.
  Run 40082631369 green. Explored other ideas this run: site already has
  image dimensions everywhere, search arrow keys, JSON-LD, feeds, SW — nothing
  else small was missing. Gems can't install in the sandbox (rubygems 403),
  so local builds aren't possible; use Actions annotations via
  `gh api .../check-runs/<job id>/annotations` (run logs are proxy-blocked).

Engineer backlog additions:
- [ ] Unpin ubuntu-24.04 → 26.04 once setup-ruby supports it (try in a
      throwaway branch run first); 24.04 is supported until 2029
- 2026-10-24 02:34 PT — ENGINEER — pinned CI runners to ubuntu-24.04 ahead of the ubuntu-latest migration (.github/workflows/jekyll.yml) (Actions deploy green).

## Done (Oct 24, 2026, 3:34am PT)

- Editor slot (UTC 10): nothing needed → Engineer had nothing small left
  (theme-color, flash, search anchors all done) → Designer. Editor checks:
  events/now current (Cal Hacks Oct 23–25 still underway — move to past and
  drop the Mentoring Now item on Oct 26); Gmail last 2 days: no new event
  registrations (IEEE Oct 27 panel mail is a reminder, not a registration);
  codespell: only "Rouge" false positives.
- Designer: new `_includes/diagrams/ai-history-pipeline.html` replaces the
  64-char ASCII pipeline box on /post/ai-history-blog-generator/ (scrolled at
  375px): Claude/OpenAI pill → Research node → Write node (Ollama, WriterAgent,
  search_wikipedia · search_arxiv · write_post) → Critique node (Pydantic
  checks) → approved → Publish & push pill | issues (max 2×) → Rewrite node,
  dashed loop back to Critique. All text from the post's own ASCII block.
  Playwright 375px sepia/dark: no text outside viewBox/boxes, no overlaps, no
  horizontal scroll. Run 40086617603 green.

Designer backlog:
- [x] ASCII sweep (line ~1433): AI History pipeline done. Remaining wide
      fenced blocks are code/key-path listings (Rena's numbered steps, VaultMem
      key chain already has a diagram below it, my_vault/ tree, python) — leave.
- 2026-10-24 03:34 PT — EDITOR→DESIGNER — theme-aware pipeline diagram on /post/ai-history-blog-generator/ (Actions deploy green).

## Done (Oct 24, 2026, 4:35am PT)

- Editor slot (UTC 11): nothing needed (events/now current — Cal Hacks still
  underway until Oct 25; llms.txt Pages in step; posts' cross-links already in
  place; no stale "this week/month" wording) → Designer.
- Designer: print audit with a Playwright print-media mock from the dark
  theme. Diagrams, code, tables, quotes all print with the light tokens (closes
  the line ~296 item). Found: project category hues (`--cat-*`) are redefined
  by a later `body.theme-dark` rule, so the print token reset didn't reach
  them — /projects printed from dark showed pastels (#e39472, ~2.6:1 on
  white). Added a `@media print` override right after that rule, plus
  `color-scheme: light` in the print token block. Screen dark unchanged.
  Run 40090695928 green.

Designer backlog:
- [ ] Any new per-theme token defined after the print block (style.css
      ~line 1770) needs its own print override placed after it
- 2026-10-24 04:35 PT — EDITOR→DESIGNER — light-theme category hues and color-scheme when printing from dark (assets/css/style.css, /projects) (Actions deploy green).
- 2026-10-24 05:35 PT — DESIGNER — theme-aware query-normalizer diagram on /post/vaultmem-part-2-multimodal-temporal-backends/ (Actions deploy green).

## Done (Oct 24, 2026, 5:35am PT)

- Designer shift (UTC 12): new `_includes/diagrams/vaultmem-query-normalizer.html`
  after the last code block of "Query normalizer" on VaultMem Part 2:
  question pill → QueryNormalizer (normalize(text) -> str) → built-in Regex |
  your own class (e.g. Groq LLM, "return only keywords") → "Sarah Chen"
  ("What do I know about" dropped) → search(…, normalize_query=True) pill.
  All text from the post. Playwright 375px sepia + dark: no text outside the
  viewBox or tight in boxes, no horizontal scroll. Run 40094628482 green.
  Closes the last open diagram idea (Whisper WebM done Oct 23).

## Done (Oct 24, 2026, 6:35am PT)

- Engineer shift (UTC 13): editors hand-check events/now freshness every run.
  New `scripts/check_data.py` (source tree, not _site; PyYAML or Ruby Psych
  fallback; CI step before the sitemap check, `continue-on-error: true`,
  `--strict` and `--today=YYYY-MM-DD` for testing). Warns (PT dates) when:
  an `upcoming` event's date is > 3 days ago; a `past` event is in the future;
  a recap isn't a post; role/status/required fields are off (location is
  optional); now.yml `updated` is > 30 days old or an item links an
  /events/#anchor that doesn't exist or is over; changelog entries miss
  fields, use an unknown desk, are dated in the future or out of order.
  Tested with --today=2026-10-27 (flags Cal Hacks + Mentoring item) and a
  mock with a bad recap/role/desk/order. Run 40098931557 green, 0 data
  warnings. Invisible, so no changelog entry.

Editor note:
- [ ] Event/now freshness is now in CI ("Check data files are current" step) — read its annotations; it starts flagging Cal Hacks on Oct 27
- 2026-10-24 06:35 PT — ENGINEER — CI freshness lint for events/now/changelog data (scripts/check_data.py, .github/workflows/jekyll.yml) (Actions deploy green).

## Done (Oct 24, 2026, 7:35am PT)

- Engineer shift (UTC 14): new `scripts/check_browser.py` + CI step
  (`pip install --break-system-packages playwright`, runner's preinstalled
  Google Chrome via `channel="chrome"`, `continue-on-error`, 8-min timeout;
  ~1 min for all pages). Serves `_site` on localhost (maps /about →
  about.html), blocks every other host (no analytics hits, no flakiness) and
  service workers, opens each page at 375px and 1280px and warns on:
  `js-error` (uncaught exceptions / console.error, ignoring blocked-resource
  noise), `h-scroll` (page wider than the viewport — names the box or text
  that sticks out), `scroll-focus` (overflowing `.post-content pre` /
  `.table-scroll` without tabindex). Skips /404.html, /offline/, redirect
  stubs. `--strict`, `--only=/a/,/b/` for local runs. Closes backlog lines
  ~409 and ~1452 (JS-built behaviour now checked in CI).
- First run found /post/hobby-project-stack/ 392px wide at 375px: the
  `<div class="mermaid">` source shows as raw text until the CDN script
  renders it (always, in CI; on slow/blocked loads for readers), and its long
  tokens spilled out. style.css: `.post-content .mermaid` max-width +
  overflow-x auto; `:not([data-processed])` styles the source as a
  pre-formatted code box. Run 40103727802 green, 0 browser warnings.

Engineer backlog additions:
- [x] (done Oct 24, 8:34am PT — contrast pass) Browser check could also run in dark theme (set localStorage
      `blog_color_theme` via `add_init_script`) — layouts are the same, so low value
- [ ] Consider `--strict` for check_browser.py after a week at 0 warnings
- 2026-10-24 07:35 PT — ENGINEER — CI headless-browser check (JS errors, sideways scroll, unreachable wide code) on every page; fixed phone sideways scroll on /post/hobby-project-stack/ (scripts/check_browser.py, .github/workflows/jekyll.yml, assets/css/style.css) (Actions deploy green).

## Done (Oct 24, 2026, 8:34am PT)

- Editor slot (UTC 15): nothing needed — events/now current (Cal Hacks
  Oct 23–25 still underway; move it to past + drop the Mentoring Now item on
  Oct 26), Gmail last day had no event registrations, llms.txt Pages in step
  → Engineer.
- Engineer: `scripts/check_browser.py` gained a `contrast` rule — a third and
  fourth pass at 1280px with the theme set via `add_init_script`
  (localStorage `blog_color_theme` = sepia, dark; reduced motion). Walks every
  visible text node (skips SVG, aria-hidden, <2px visually-hidden helpers,
  opacity <0.1), composites ancestor background fills (skips text over
  background images/gradients), folds ancestor opacity into the text color,
  and warns below 4.5:1 (3:1 for ≥24px or bold ≥18.66px). Closes the dark-theme
  browser-check item (~line 1568) and line ~376 (contrast now measured in CI).
- First run (40107767770): 73 issues — sepia/white Rouge tokens tuned for
  white (comment #6b7280 3.8:1, keyword/string teal/green ~2.9:1, blue 4.1,
  violet 4.4 on #ebe4d2), dark comment/operator #8b949e 4.39:1 on #322e26,
  and /blog tag counts (opacity .6 → 3.4:1). Fixed in style.css: light Rouge
  c #4b5563, k/ow #115e59, s/s2 #065f46, nb/nf/na/nn #1d4ed8, nv/vi #6d28d9
  (all ≥5.8:1 on every light code-bg); dark c/o #a0a8b2 (5.6:1); tag count
  opacity .8 and 1 on the active chip. Run 40108110610 green, 0 browser
  warnings.

Engineer backlog additions:
- [ ] Contrast pass doesn't see hover/focus states — designer shifts still check those by hand (SVG diagram text now covered, Oct 24 9:34am PT)
- 2026-10-24 08:34 PT — EDITOR→ENGINEER — CI text-contrast check in sepia and dark; code highlighting + /blog tag counts fixed to WCAG AA (scripts/check_browser.py, assets/css/style.css, /blog/, all posts with code) (Actions deploy green).

## Done (Oct 24, 2026, 9:34am PT)

- Editor slot (UTC 16): nothing needed — events/now current (Cal Hacks
  Oct 23–25 still underway; move to past + drop the Mentoring Now item on
  Oct 26), Gmail last day: no event registrations → Engineer.
- Engineer: `scripts/check_browser.py` contrast pass now measures `.diagram
  svg text` too: text fill (× fill-opacity/opacity) vs. the topmost filled
  rect/circle/ellipse/path/polygon under the text's centre
  (`elementsFromPoint` after an instant `scrollIntoView` — the page's smooth
  scroll otherwise leaves the text off-screen), composited down to the HTML
  background behind the figure; large-text threshold uses the rendered px
  size. Mock with all 24 diagram includes × sepia/dark/white at 375px: all
  421 texts measured, lowest 5.71 (sepia) / 5.23 (dark) / 7.20 (white); an
  injected muted-on-pill (3.66), grey-on-page and 50%-white overlay case were
  flagged with the right composited colors. Run 40112453492 green, 0 browser
  warnings. Invisible, so no changelog entry.
- 2026-10-24 09:34 PT — EDITOR→ENGINEER — CI contrast check now covers text in SVG diagrams (scripts/check_browser.py) (Actions deploy green).

## Done (Oct 24, 2026, 10:35am PT)

- Designer shift (UTC 17): hover/focus contrast audit by hand (the CI
  contrast pass can't see hover). Computed every hover rule that changes
  text or fill colour in sepia + dark: `.hero-btn` (accent-ink on
  accent-soft 5.1 / 4.6), header search, offline retry, footer/links — all
  ≥4.5 except `.hero-btn-primary:hover` ("View Projects" on the homepage):
  `opacity: .88` faded the teal fill into the page, label #f5efe0 dropped to
  3.88:1 in sepia. Hover now uses `color-mix(in srgb, var(--accent) 80%,
  var(--text))` for background + border (#176860 sepia 5.8:1, #d9bb8d dark
  8.2:1 — contrast rises on hover in both themes); browsers without
  color-mix keep the rest-state accent. Playwright 375px hover mock confirmed
  computed colours. Run 40116924278 green.

Designer backlog:
- [x] Touch-only `.heading-anchor` opacity (done Oct 24, 2:35pm PT)
- 2026-10-24 10:35 PT — DESIGNER — homepage "View Projects" button hover darkens instead of fading; sepia hover label 3.9 → 5.8:1 (assets/css/style.css, /) (Actions deploy green).

## Done (Oct 24, 2026, 11:35am PT)

- Engineer shift (UTC 18): "Copy link to quote" in posts
  (`_includes/post-tools.html`, `.quote-link` in style.css). On
  fine-pointer devices only (phones have native "link to highlight"),
  selecting text inside `.post-content` (mouse or Shift+arrows) shows a
  small button under the selection's last line; it copies
  `<post url>#:~:text=<text>` (≤8 words) or `start,end` (first/last 4
  words) with `-`/`,` percent-encoded. Ignores selections in pre/code,
  SVG diagrams, TOC, buttons; hides on outside mousedown / Escape; the
  "Link copied" reset timer is cleared on a new selection (bug caught in
  test). Live status message via the existing `say()`. Hidden in print.
  Playwright mock (localhost, sepia + dark at 1200px): button shows with
  theme colours, clipboard URL opens scrolled to the passage; no button on
  code selections or on a touch/mobile context. Run 40121748287 green,
  0 warnings.
- Sandbox notes: www.avinashgosavi.com is blocked by the egress proxy and
  rubygems is unreachable (no local Jekyll) — test JS/CSS on a localhost
  mock page (`python3 -m http.server`; clipboard needs localhost).

Engineer backlog additions:
- [x] Quote links: if a quote's start/end words repeat earlier in the post,
      the browser highlights the first match — could add a `prefix-,` if
      readers hit this (done Oct 24, 1:35pm PT)
- 2026-10-24 11:35 PT — ENGINEER — "Copy link to quote" button for selected text in posts (_includes/post-tools.html, assets/css/style.css, all /post/*) (Actions deploy green).

## Done (Oct 24, 2026, 12:34pm PT)

- Engineer shift (UTC 19): `scripts/check_browser.py` gained an `a11y-dom`
  rule, run in the 375px and 1280px passes after scripts have run (same
  issue at both widths reported once). Flags any visible `a[href]`, button,
  form field, summary, ARIA widget role or `[tabindex]≥0` with no accessible
  name (aria-label, aria-labelledby, `<label>`, title, placeholder, or
  readable text — aria-hidden parts skipped, img alt / svg title counted; a
  plain tabindex scroller with text inside passes), plus ids used twice in
  the live DOM. Also opens `/search/?q=memory` and `/blog/?q=memory` (added
  to every pass, contrast too) so JS-rendered results get checked. Closes
  line ~409. Mock with 4 nameless controls + a duplicate id + a nameless
  JS-built result: all flagged, the 8 good cases not. Run 40126077274 green,
  0 browser warnings on the real site. Invisible, so no changelog entry.

Engineer backlog additions:
- [ ] check_browser.py EXTRA list: add any other page whose content is built from a query string
- 2026-10-24 12:34 PT — ENGINEER — CI browser check flags nameless links/buttons/fields and duplicate ids after JS runs, incl. search and blog results (scripts/check_browser.py) (Actions deploy green).

## Done (Oct 24, 2026, 1:35pm PT)

- Editor slot (UTC 20): nothing needed — events/now current (Cal Hacks
  Oct 23–25 still underway; move to past + drop Mentoring Now item on
  Oct 26), llms.txt Pages in step, codespell sweep of posts/pages/data
  clean (only "Rouge" false positives). Gmail last day: a Luma "new message
  in San Francisco Ruby Conference" (Nov 10, 2026, SFJAZZ) — no registration
  or ticket email found for the 2026 edition, so NOT added to events.yml.
- → Engineer: quote links (`_includes/post-tools.html`) now check whether
  the quote's opening words (full quote if ≤8 words, else first 4) occur
  earlier in `.post-content` (case-insensitive); if so, prepend up to 3
  words preceding the selection in the same block (p/li/h2–h6/blockquote/
  td/th/dd/dt/figcaption) as `prefix-,`. Skipped when the selection starts
  mid-word or at the block's start (no safe prefix). Playwright localhost
  mock: repeated phrase → `Second%20time%20around%2C-,memory…` and opening
  it scrolls to the second paragraph; first occurrence and unique quotes
  unchanged. Run 40130641612 green.

Engineer backlog additions:
- [ ] Waiting on Avinash: SF Ruby Conference 2026 (Nov 10, SFJAZZ) — Luma
      messages arrive, but no registration/ticket email found; add to
      /events only if he confirms he's going
- 2026-10-24 13:35 PT — EDITOR→ENGINEER — quote links pick the right passage when its opening words repeat earlier in the post (_includes/post-tools.html, all /post/*) (Actions deploy green).

## Done (Oct 24, 2026, 2:35pm PT)

- Editor slot (UTC 21): nothing needed — events/now current (Cal Hacks
  Oct 23–25 still underway; move to past + drop Mentoring Now item on
  Oct 26). Gmail last day: only another Luma SF Ruby Conference 2026
  message (scholarship announcement) — still no registration/ticket, not
  added. External links can't be checked from the sandbox.
- → Designer: touch-only (`hover: none`) heading "#" anchors in posts and
  on pages were opacity .6 → text-muted blended to 2.65:1 sepia / 3.03:1
  dark. Now opacity 1: 6.31:1 sepia, 5.82:1 dark (0.85 would only reach
  4.46/4.64). Run 40134953371 green.
- 2026-10-24 14:35 PT — EDITOR→DESIGNER — heading # links on touch screens shown at full muted colour, sepia 2.7 → 6.3:1 (assets/css/style.css, all /post/* and pages with section anchors) (Actions deploy green).

## Done (Oct 24, 2026, 3:35pm PT)

- Designer shift (UTC 22): project cards (homepage + /projects). The hover
  lift/accent border/shadow is now inside `@media (hover: hover)` — on
  phones a tap used to leave the card stuck raised. New
  `.project-card:focus-within { border-color: var(--accent) }` so keyboard
  users see which card the focused Code/Live/Write-up link belongs to (no
  lift on focus). Accent border vs surface: sepia ~4.4:1, dark ~8:1 (≥3:1
  non-text). Playwright localhost mock at 375px: desktop context hover →
  teal border + -2px; touch context hover → unchanged; Tab → border in both.
  Run 40139300662 green.

Designer backlog:
- [ ] Other hover-only container states (tag chips, share buttons) are
      border-only, no lift — fine on touch; revisit only if a new card
      with a transform hover is added (wrap it in `@media (hover: hover)`)
- 2026-10-24 15:35 PT — DESIGNER — project cards: no stuck hover lift on touch, accent border on keyboard focus-within (assets/css/style.css, /, /projects/) (Actions deploy green).

## Done (Oct 24, 2026, 4:35pm PT)

- Engineer shift (UTC 23): microformats2 for IndieWeb readers/reply tools.
  `_layouts/post.html`: `article.h-entry` with hidden `<data>` u-url
  (absolute) + p-summary (description), `p-name` on the h1, `dt-published`
  on the date, author span is `p-author h-card` (hidden data p-name
  "Avinash Gosavi" + u-url home; visible text still the username),
  `p-category` on tag links, `e-content` on `.post-content`.
  `_layouts/home.html`: `.hero.h-card` with u-url/u-uid + u-photo
  (site.logo), p-name h1, p-note intro; social icons gained `u-url`
  (rel="me" already there) — only parsed inside the hero h-card.
  style.css: `.h-entry > data, .h-card > data { display: none }`.
  New `scripts/check_mf2.py` (mf2py, pip-installed in CI,
  continue-on-error): one h-entry per post with name/published/absolute
  url/content/author name; homepage h-card with name/url/photo. Mock
  parsed correctly with mf2py 2.0.2. Run 40143540265 green, 0 warnings.

Engineer backlog additions:
- [x] /about h-card with `u-uid` = homepage (done Oct 24, 6:34pm PT)
- 2026-10-24 16:35 PT — ENGINEER — microformats h-entry on posts + h-card on homepage, CI mf2 check (_layouts/post.html, _layouts/home.html, _includes/social-icons.html, scripts/check_mf2.py, all /post/*, /) (Actions deploy green).

## Done (Oct 24, 2026, 5:35pm PT)

- Editor shift (UTC 00): events/now still current (Cal Hacks Oct 23–25 underway;
  move it to past + drop its /now item after Oct 25). Cross-link sweep of
  project names in posts: only gap was the first VaultMem post linking Rena
  to GitHub alone — now links the Rena write-up with the code link beside it.
  Closed two stale backlog items (ASCII-block sweep, scroll-focus check).
- 2026-10-24 17:35 PT — EDITOR — VaultMem post links the Rena write-up (/post/vaultmem-encrypted-memory-for-ai-agents/) (Actions deploy green).

## Done (Oct 24, 2026, 6:34pm PT)

- Editor shift (UTC 01) had nothing to do: events/now checked an hour ago
  (Cal Hacks Oct 23–25 still underway — move to past + drop /now item after
  Oct 25), llms.txt Pages in step, codespell only "Rouge" false positives.
  Took an Engineer task from the backlog: `_layouts/about.html` wraps
  `.about-page` in `h-card` with hidden `<data>` u-url u-uid (homepage,
  absolute) + p-name (site.author.name), `p-note` on `.about-content`,
  `u-photo` on the photo img. Hidden data uses the existing
  `.h-card > data { display:none }` (no flex gap impact). check_mf2.py now
  also checks /about/ (name, photo, uid matching the homepage uid). mf2py
  mock parsed correctly. Run 40151262844 green, no mf2 warnings.
- 2026-10-24 18:34 PT — EDITOR (took Engineer task) — About page h-card tied to homepage, CI mf2 check covers /about/ (_layouts/about.html, scripts/check_mf2.py, /about/) (Actions deploy green).

## Done (Oct 24, 2026, 7:35pm PT)

- Designer shift (UTC 02): /post/hobby-project-stack/ was the last post using
  a CDN Mermaid chart (`theme: 'neutral'`, ignored sepia/dark, raw source
  showed until jsdelivr loaded). New `_includes/diagrams/daylog-stack-architecture.html`
  (336×634, same nodes/edges/labels as the Mermaid source, no emoji): PWA →
  HTTPS → Rails API → SQL → Neon Postgres; Fly internal network :8000 →
  vault service group (FastAPI + vaultmem) → Redis (lock) / Fly Volume
  (read/write) / faster-whisper / sentence-transformers. Removed the module
  script and the now-unused `.post-content .mermaid` CSS. Playwright 375px
  mock sepia + dark: no overflow, all text inside its box. Run 40155178678
  green, 0 warnings. Site now loads no Mermaid/jsdelivr script anywhere.
- 2026-10-24 19:35 PT — DESIGNER — theme-aware architecture diagram replaces CDN Mermaid chart (/post/hobby-project-stack/, _includes/diagrams/daylog-stack-architecture.html) (Actions deploy green).

## Done (Oct 24, 2026, 8:34pm PT)

- Engineer shift (UTC 03): search.json cut each post's text at 8,000 chars,
  so the tails of ~10 long posts (VaultMem Part 2 ~13.8k source chars,
  hobby stack, VaultMem intro, Rena, Attractor, Codex skills, glossary…)
  weren't searchable — and /search/'s text-fragment jump never reached them.
  Cap raised to 30,000 (longest post well under it; adds ~25 KB raw /
  a few KB gzipped to search.json, which /search/, 404 and link previews
  fetch once). CI "Check search index is valid JSON" step now prints the
  index size and a ::notice for any post that hits the 30k cap.
  Run 40158874493 green, no cap notices. (Local Jekyll build impossible:
  rubygems.org unreachable from sandbox — CI is the build check.)
- Changelog wording kept generic ("a long post") — exact rendered-text
  lengths weren't measured.

Engineer backlog additions:
- [ ] If search.json ever passes ~400 KB, consider splitting post text into a lazily fetched second file (links previews only need title/desc/date)
- 2026-10-24 20:34 PT — ENGINEER — /search/ now searches the full text of long posts (cap 8k → 30k chars) + CI size/cap notice (search.json, .github/workflows/jekyll.yml) (Actions deploy green).

## Done (Oct 24, 2026, 9:35pm PT)

- Engineer shift (UTC 04): CI browser check (scripts/check_browser.py) gains a
  `layout-shift` rule — a PerformanceObserver init script sums load-time CLS
  per page at 375/1280px and warns above 0.05 (Google "good" ≤ 0.1; local
  server is faster than the real one), naming the shifted elements. Tested on
  a mock page (late 300px box → CLS 0.17 flagged, stable page clean). First CI
  run (40162532410) found one real shift: /search/?q=memory, footer jumped
  when results arrived (CLS 0.099 phone / 0.120 desktop). Fix in search.md:
  a ?q= link sets `min-height: 100vh` on the results list before search.json
  loads (cleared when the query is emptied). Run 40162724050 green, 0 browser
  warnings. Live site unreachable from sandbox (proxy) — CI is the check.

Engineer backlog additions:
- [ ] Consider `--strict` for the layout-shift rule after a week at 0 warnings
- [ ] Layout-shift check runs on a fast local server with fonts cached per page; font-swap shifts on slow networks may still slip through
- 2026-10-24 21:35 PT — ENGINEER — CI layout-shift (CLS) check on every page; fixed footer jump on /search/?q= links (scripts/check_browser.py, search.md) (Actions deploy green).

## Done (Oct 24, 2026, 10:34pm PT)

- Editor slot (UTC 05): nothing needed — Cal Hacks (Oct 23–25) still
  underway, other events/now items current; Gmail last day had no new
  registration/ticket emails. Took the Engineer backlog item "Contrast pass
  doesn't see hover/focus states": scripts/check_browser.py now, in each
  theme, tags every visible link/button/summary with text, hovers (real
  mouse move to a point not covered by the sticky header) and then focuses
  one element per kind site-wide (tag + sorted classes + nearest classed
  ancestor), with transitions/animations disabled, and runs the same AA
  test on its text → rules `contrast-hover` / `contrast-focus` (messages
  already failing at rest are not repeated). CONTRAST JS now takes an
  optional root. Mock test caught a bad :hover (1.39:1, even with a 1s
  transition) and a bad :focus (1.23:1). Run 40166211848 green: 0 hover/
  focus contrast issues site-wide; browser step ~2 min.
- Same run flagged one layout-shift on /post/building-rena-ai-health-companion-gemini-live/
  at 375px (CLS 0.068; div.post-content, a, strong, p) — previous run had
  0, so possibly timing; check the next runs before fixing.

Engineer backlog additions:
- [x] (closed Oct 24, 11:34pm PT: run 40166502242 had no layout-shift annotation — timing noise) Rena post 375px CLS 0.068 warning (first seen run 40166211848) — if it repeats, find what reflows post-content (image dims? font swap?)
- [x] Contrast pass doesn't see hover/focus states (done Oct 24, 10:34pm PT)
- 2026-10-24 22:34 PT — EDITOR→ENGINEER — CI contrast check now covers hover and keyboard-focus states of links/buttons in sepia and dark (scripts/check_browser.py) (Actions deploy green).

## Done (Oct 24, 2026, 11:34pm PT)

- Editor shift (UTC 06): events/now current (Cal Hacks Oct 23–25 still
  underway); Gmail last day: only the already-logged Luma SF Ruby 2026 message.
  Cross-linked existing wording to glossary anchors: VaultMem diary explainer
  (four memory types → #episodic/#semantic/#persona/#procedural-memory) and
  hobby-stack post (semantic search, embeddings). Wording unchanged.
- Rena CLS warning didn't repeat (run 40166502242 annotations) — closed.
- Note: `gh run view --log` returns 403 from the log host; read annotations via
  `gh api .../check-runs/<id>/annotations` instead.
- 2026-10-24 23:34 PT — EDITOR — glossary cross-links in /post/vaultmem-your-ai-agent-shouldnt-read-your-diary/ and /post/hobby-project-stack/ (Actions deploy green).

## Done (Oct 25, 2026, 12:34am PT)

- Designer shift (UTC 07): `.project-name` inherited body line-height (33px
  on a 17.6px heading), so two-line names (AI History Blog Generator at
  375px, several at 320px) looked double-spaced. Now `line-height: 1.3`, and
  ≤400px the name is 1.04rem so whisper-live-transcribe fits one line at
  375px (was wrapping at the hyphen). Playwright mock with the real
  style.css at 320/375/414: no overflow; colours untouched. Run 40173388107 green.
- 2026-10-25 00:34 PT — DESIGNER — project card names: tighter line-height, long names fit on one line on phones (assets/css/style.css; /, /projects/) (Actions deploy green).

## Done (Oct 25, 2026, 1:34am PT)

- Engineer shift (UTC 08): CI page-weight budget, `scripts/check_weight.py`
  (stdlib, warnings only, step "Page-weight budget"). Per page it counts the
  first-visit download: HTML + same-origin CSS/JS gzipped, preloaded fonts,
  and every non-lazy image at its largest srcset/<source> candidate (the
  <img src> fallback inside a <picture> with sources isn't counted). Budgets:
  page 500 KB, eager image 150 KB, any used image 250 KB, HTML 60 KB gzip;
  also flags missing asset files. Skips <pre>/<code> samples and redirect
  stubs; third-party hosts listed, not counted. Mock test caught an eager
  221 KB JPEG and a missing PNG. Run 40177330877 green: 46 pages, 0 over
  budget; heaviest /about/ 117 KB, then the VaultMem/Attractor posts ~68 KB.
  Invisible, so no changelog entry.
- Note: sandbox can't reach www.avinashgosavi.com (proxy 403) or rubygems —
  test scripts on a mock _site built from the repo's assets.

Engineer backlog additions:
- [ ] Consider `--strict` for check_weight.py after a week at 0 warnings
- [ ] If fonts beyond the preloaded DM Sans become render-critical, count the @font-face files a page actually uses (needs the browser check)
- 2026-10-25 01:34 PT — ENGINEER — CI page-weight budget check on every page (scripts/check_weight.py, .github/workflows/jekyll.yml) (Actions deploy green).

## Done (Oct 25, 2026, 2:34am PT)

- Engineer shift (UTC 09): feed readers got the inline SVG diagrams raw —
  their colours come from style.css classes, so readers drew solid black
  shapes; llms-full.txt (strip_html) got a jumble of box labels. New
  `_plugins/feed_diagrams.rb`: each `<figure class="diagram">` becomes a
  `<blockquote class="diagram-text">` with "Diagram: <svg title>" + link to
  the post, the `<desc>` text and the figcaption. Liquid filter
  `feed_diagrams: <abs post url>` in feed.json, `_layouts/series-feed.html`
  and llms-full.txt; a `:pages, :post_render` hook rewrites jekyll-feed's
  /feed.xml (0.17 puts content in CDATA — first push only handled escaped
  text; the new CI step caught 9 entries, fixed in the second push).
  New CI step (warnings only): raw `<svg`/`dg-box` in any Atom feed,
  feed.json or llms-full.txt. Runs 40181440077 (warnings) → 40181672195
  green, 0 warnings. search.json still indexes diagram labels (useful there).
- Rena 375px CLS 0.068 warning showed again in run 40181440077 (not in
  40181672195) — second sighting; still looks like timing, but if it repeats
  look at the 4 phone screenshots (inline style width:100%, width/height set).

Engineer backlog additions:
- [ ] Any new diagram must keep `<title>`, `<desc>` and a `<figcaption>` — the feed text version is built from them
- 2026-10-25 02:34 PT — ENGINEER — diagrams arrive in RSS/Atom/JSON feeds and llms-full.txt as text descriptions + link instead of raw SVG; CI check (_plugins/feed_diagrams.rb, feed.json, _layouts/series-feed.html, llms-full.txt, /feed.xml, /feed/*.xml) (Actions deploy green).

## Done (Oct 25, 2026, 3:35am PT)

- Editor slot (UTC 10): nothing needed — Cal Hacks (Oct 23–25) still underway
  today, /now accurate, codespell clean (only "Rouge" false positives),
  external links can't be checked from the sandbox (proxy). → Engineer.
- /events: optional `end_date` in events.yml (set on Cal Hacks 13.0). Upcoming
  rows carry data-start/data-end and a hidden "Happening now" pill; a tiny
  script in events.md un-hides it when the visitor's local date is inside the
  range. `.event-when` is now `<time datetime>`. check_data.py uses end_date
  for the "move to past" and "/now item is over" warnings (+ validates it).
  README documents the field. Playwright mock 375px: pill 6.6:1 sepia,
  7.4:1 dark, no overflow. Run 40185577255 green, no new warnings.

Editor backlog additions:
- [ ] Add `end_date` to any new multi-day event (drives "Happening now" and the CI freshness check)
- 2026-10-25 03:35 PT — EDITOR→ENGINEER — "Happening now" tag + <time> dates + end_date on /events (_data/events.yml, _includes/event-row.html, events.md, assets/css/style.css, scripts/check_data.py) (Actions deploy green).

## Done (Oct 25, 2026, 4:34am PT)

- Editor slot (UTC 11): nothing needed — Cal Hacks 13.0 (Oct 23–25) still
  running today; /now accurate; no http:// links, doubled words or stray
  punctuation in posts; llms.txt lists every page. Gmail (for the next
  editor after Oct 25): Cal Hacks emails are only Slack-workspace joins/
  mentions (Oct 15–16) — no mentor shift, check-in or QR email, so they
  don't prove attendance on their own. → Engineer had nothing open that
  wasn't done or waiting on Avinash → Designer.
- Search fields (#site-search, #post-search): accent `caret-color` and a
  themed WebKit/Blink clear (×) button — SVG mask filled with --text-muted,
  accent-ink on hover, CanvasText in forced colors (Firefox has no native
  clear button). Playwright file mock at 375px, sepia + dark: icon visible,
  no overflow. Run 40189673958 green, 0 warnings.

Designer backlog additions:
- [ ] Any new `<input type="search">` needs its id added to the clear-button rule in style.css
- 2026-10-25 04:34 PT — EDITOR→DESIGNER — themed clear (×) button + accent caret on search fields (assets/css/style.css; /search/, /blog/) (Actions deploy green).
- 2026-10-25 05:34 PT — DESIGNER — post tables: top-aligned cells, tabular numbers (assets/css/style.css; /post/* with tables) (Actions deploy green).

## Done (Oct 25, 2026, 6:35am PT)

- Engineer shift (UTC 13): Paper TL;DR posts now carry a `ScholarlyArticle`
  JSON-LD block (`_includes/paper-jsonld.html`, included from
  `_layouts/default.html` when `page.series == 'paper-tldr'`): paper title,
  original URL, year (`datePublished`), authors as `creditText` (they're
  strings like "Maharana et al.", so not Person nodes), `@id` = post URL +
  `#paper`, `subjectOf` → the post's WebPage `@id` (same node jekyll-seo-tag
  uses as mainEntityOfPage). Data from `_data/papers.yml` by `tldr_post`;
  the six-papers roundup has no entry, so nothing is emitted there.
  `scripts/check_jsonld.py` validates name/http url/4-digit year and posts a
  `JSON-LD` notice with counts. Run 40198843843: 11 ScholarlyArticle,
  29 BlogPosting, 44 BreadcrumbList, 0 problems.
- Same run showed one layout-shift warning on
  /post/building-rena-ai-health-companion-gemini-live/ at 375px (CLS 0.068,
  div.post-content) that the previous run didn't have — not from this change
  (head-only JSON-LD). Next engineer: if it repeats, look at the Rena
  `<picture>` screenshots' reserved size at 375px.

Engineer backlog additions:
- [ ] New Paper TL;DR: give its papers.yml entry a `tldr_post` — that drives the ScholarlyArticle JSON-LD
- [x] Watch the Rena post 375px CLS warning (first seen run 40198843843; not repeated by Oct 25 8:35am PT)
- 2026-10-25 06:35 PT — ENGINEER — ScholarlyArticle structured data naming the summarised paper on every Paper TL;DR post + CI check (_includes/paper-jsonld.html, _layouts/default.html, scripts/check_jsonld.py; /post/paper-tldr-*) (Actions deploy green).

## Done (Oct 25, 2026, 8:35am PT)

- Editor shift (UTC 15): events/now still current — Cal Hacks 13.0 ends today
  (Oct 25); next editor after today moves it to past and drops its /now item
  (attendance not provable from Gmail — keep role mentor, note in log).
- Rena post: closing italic line linking VaultMem (fact from the VaultMem
  post's opening: memory need while building Rena); removed a doubled `---`
  after "What's next". Run 40207747469 green, 0 warnings.
- Rena 375px CLS warning from run 40198843843 did not repeat in runs
  40199179259 or 40207747469 — treat as one-off unless it returns.
- 2026-10-25 08:35 PT — EDITOR — Rena post links VaultMem, doubled rule removed (/post/building-rena-ai-health-companion-gemini-live/) (Actions deploy green).
- 2026-10-25 10:35 PT — DESIGNER — theme-aware push → Actions → Pages → DNS diagram on /post/building-your-website-with-jekyll-and-github-pages/ (Actions deploy green).

## Done (Oct 25, 2026, 11:34am PT)

- Engineer shift (UTC 18): CI outbound-link check — `scripts/check_external.py`
  collects every external `<a href>` in `_site`, fetches each unique URL once
  (HEAD → GET fallback, 16 threads, 12s timeout, 150s total budget, exits
  without waiting on stragglers). Only 404/410 and unresolvable hosts become
  `Dead external link` warnings; 403/429/5xx/timeouts go in a collapsed
  "Couldn't verify" group. Skips share intents and bot-walled hosts
  (LinkedIn, X, Bluesky, HN, Medium…). Workflow step is
  `continue-on-error` + `timeout-minutes: 4` — never blocks deploy. This is
  the only place external links can be checked (sandbox proxy blocks them).
  Read results via `gh api repos/.../check-runs/<build job id>/annotations`
  (`gh run view --log` returns 403 from the sandbox).
- First run 40222083290: 89 URLs on 46 pages — 84 ok, 3 unverified, 2 dead:
  - https://rena-490107-f0f28.web.app → 404 (Rena demo; linked on /, /projects/, Rena post)
  - https://github.com/aag1091-alt/daylog → 404 (repo private or gone; linked on /, /projects/, Whisper post)
  Left as-is: whether to drop/replace these is Avinash's call.

Backlog additions:
- [ ] Waiting on Avinash: Rena demo (rena-490107-f0f28.web.app) and daylog repo both 404 — redeploy/make public, or remove the links (/, /projects/, two posts)
- [ ] Consider `--strict` for check_external.py only if dead-link warnings stay at 0 for a week (bot walls make strict risky)
- 2026-10-25 11:34 PT — ENGINEER — CI outbound-link check flagging 404/410 and dead hosts, non-blocking (scripts/check_external.py, .github/workflows/jekyll.yml) (Actions deploy green; found 2 dead links, logged for Avinash).

## Done (Oct 25, 2026, 12:35pm PT)

- Engineer shift (UTC 19): posts show "· Updated <date>" in the meta line
  (`<time class="dt-updated">`, `_layouts/post.html`) when git's
  `last_modified_at` is ≥ 7 days (604800 s) after the publish date, so the
  visible date matches BlogPosting `dateModified`; trivial same-week fixes
  stay hidden. CSS: shares the " · " separator, nowrap. `scripts/check_mf2.py`
  now counts posts with an Updated date and warns if dt-updated < dt-published.
  Run 40226923527 green, no new warnings (only the 2 known dead external links).
  Rendered output not viewable from the sandbox (live site + artifact download
  blocked) — next designer can eyeball the meta line at 375px.
- Skipped: WebSite/SearchAction JSON-LD — jekyll-seo-tag already emits a
  WebSite block on / and /about/; a second one would duplicate.
- 2026-10-25 12:35 PT — ENGINEER — "Updated <date>" on posts revised ≥1 week after publishing + mf2 check (_layouts/post.html, assets/css/style.css, scripts/check_mf2.py; all /post/*) (Actions deploy green).

## Done (Oct 25, 2026, 1:34pm PT)

- Editor shift (UTC 20): nothing editorial needed — Cal Hacks 13.0 ends today
  (Oct 25), so it stays upcoming/"Happening now" and on /now; move it to past
  tomorrow (role `mentor` only if a check-in email supports attendance).
  Gmail since Oct 23: no new registrations (only the already-logged Luma SF
  Ruby 2026 message). codespell: only "Rouge" false positives. llms.txt page
  list complete. Cross-links already cover every older post (post_url links).
- Took a Designer task: theme-aware eight-step review flow diagram on
  /post/reviewing-ai-generated-tests-istqb-framework/
  (`_includes/diagrams/ai-test-review-flow.html`), inserted after the
  "Actionable Review Algorithm" list. Step 7 uses `.dg-bar` lengths only as a
  rank (highest → lowest), no numbers. Checked at 375px in sepia + dark:
  no text overflow/overlap. Run 40231663397 green.
- Stale backlog items: "Search: index project/paper/event anchors" and
  "Events: give event rows ids" are already done (search.json uses
  /projects/#slug, /research/#paper-slug, /events/#slug).
- Diagram ideas still open: Codex Skills (agent vs. skill), Doing the Right
  Thing Fast (ticket → PR pipeline) — only if the post describes the flow.
- 2026-10-25 13:34 PT — EDITOR→DESIGNER — eight-step review flow diagram (/post/reviewing-ai-generated-tests-istqb-framework/) (Actions deploy green).

## Done (Oct 25, 2026, 2:34pm PT)

- Editor shift (UTC 21): nothing editorial needed — Cal Hacks 13.0 still
  runs today (move to past tomorrow); Gmail last day: only the HackUMass XIV
  judge next-steps email (event already listed as upcoming/judge). No new
  registrations.
- Took a Designer task: theme-aware git housekeeping flow diagram on
  /post/codex-skills-baking-your-workflow-into-the-tool/
  (`_includes/diagrams/codex-git-housekeeping.html`): One prompt → combined
  skill chaining New branch → Update from origin → Commit → Push, each step
  noted from the post's own table. Checked at 375px in sepia + dark, no
  overflow. Run 40236264205 green.
- Diagram idea still open: Doing the Right Thing Fast (stream cycle:
  identify → change → review → test) — the post describes it in one line.
- 2026-10-25 14:34 PT — EDITOR→DESIGNER — git housekeeping flow diagram (/post/codex-skills-baking-your-workflow-into-the-tool/) (Actions deploy green).

## Done (Oct 25, 2026, 3:35pm PT)

- Designer shift (UTC 22): theme-aware work-stream cycle diagram on
  /post/doing-the-right-thing-fast/ (`_includes/diagrams/right-thing-fast-cycle.html`),
  inserted after the "same cycle" sentence: 20–25 work streams → Identify
  (Codex finds call sites) → Change (Codex: deletions + ripple effects) →
  Review (diff by diff in VS Code) → Test (manually) with a dashed
  "next stream" loop back; all labels from the post's own text. Mocked at
  375px in sepia + dark (Playwright): no overflow. Run 40241056074 green;
  only the 2 known dead external links. Closes the last open diagram idea.
- Posts still without a diagram: SF Ruby 2025, I Fell in Love with Coding
  Again, VaultMem intro, glossary, six-papers intro — none describe a flow;
  leave them.
- 2026-10-25 15:35 PT — DESIGNER — work-stream cycle diagram (/post/doing-the-right-thing-fast/) (Actions deploy green).

## Done (Oct 25, 2026, 4:35pm PT)

- Engineer shift (UTC 23): /projects now emits an ItemList of 9
  SoftwareSourceCode entries (`_includes/projects-jsonld.html`, included from
  `_layouts/default.html` when `page.url == '/projects/'`), built from
  `_data/projects.yml` in page order: name, description, codeRepository,
  keywords (tags), url = card anchor (/projects/#slug), author → `#person`,
  subjectOf → the write-up post. `scripts/check_jsonld.py` warns if an entry
  lacks a name or http url and counts them in the notice. Rendered locally
  with python-liquid (gems can't install) — valid JSON, anchors match card ids.
  Run 40245658208 green: "SoftwareSourceCode 9". Invisible metadata → no
  changelog entry.
- Not done: still skipping the 6 long SEO titles (would change visible titles).

Engineer backlog additions:
- [ ] New projects.yml category: add it to the `order` list in BOTH projects.md and `_includes/projects-jsonld.html`
- [ ] Rena demo / daylog repo still 404 — the JSON-LD repeats daylog's codeRepository; fix both when Avinash decides
- 2026-10-25 16:35 PT — ENGINEER — SoftwareSourceCode structured data for /projects (_includes/projects-jsonld.html, scripts/check_jsonld.py) (Actions deploy green).

## Done (Oct 25, 2026, 5:35pm PT)

- Editor slot (UTC 00) → Engineer: nothing editorial — Cal Hacks 13.0 ends
  today (Oct 25 PT), so it stays upcoming; Gmail last 2 days: no new
  registrations (AICamp Oct 29 is only an RSVP invite — not added; HackUMass
  judge next-steps already reflected).
- /now items can carry `until: YYYY-MM-DD`. New `_includes/now-items.html`
  (used by now.md with links=true and home.html with max=4 compact=true):
  build drops items more than a day past (UTC build clock minus 1 day), and an
  inline script hides items from the visitor's local day after `until`, then
  re-caps the homepage at 4 so the next item moves up. No-JS fallback: same
  first-4 as before. CSS `.now-item[hidden]`. Set until on Cal Hacks (Oct 25),
  OSA Con (Nov 2), HackUMass (Nov 15). `scripts/check_data.py` validates
  `until` and warns once it has passed ("remove it from now.yml"); dated items
  skip the events cross-check. README data table notes the field. Playwright
  mock of the script: Oct 25 shows all 4, Oct 26 hides Cal Hacks and promotes
  the 5th. Run 40250275040 green, only the 2 known dead external links.
- Next editor (Oct 26 PT): still move Cal Hacks to past in events.yml (role
  `mentor` from the acceptance email) and delete its now.yml item (the site
  already hides it); bump `updated`.
- 2026-10-25 17:35 PT — EDITOR→ENGINEER — dated /now items hide themselves the day after (`until:`) on /now/ and / (_includes/now-items.html, scripts/check_data.py) (Actions deploy green).

## Done (Oct 25, 2026, 6:34pm PT)

- Editor slot (UTC 01) → Engineer: nothing editorial — Cal Hacks 13.0 still
  runs today (Oct 25 PT), so it stays upcoming; Gmail last 2 days: no new
  registrations (only the already-logged HackUMass judge next-steps, AICamp
  RSVP invite and SF Ruby 2026 Luma message); codespell only "Rouge" false
  positives; llms.txt in step (CI-checked).
- /changelog desk filter: chips All / Writing / Design / Engineering with
  counts (reuse `.tag-chip`), rendered `hidden` and shown by the inline script
  (no-JS: full list as before). Filtering hides `li[data-desk]` and any
  `.changelog-day` left empty, announces "Showing N of M changes from the X
  desk." in a role=status line, and keeps the filter in the hash
  (/changelog/#design; hashchange supported; desk slugs don't collide with
  the date-heading ids). CSS: `.changelog-filter`, `[hidden]` display:none.
  python-liquid mock + Playwright at 375px: 160 = 42 + 49 + 69, empty days
  hide, hash deep link works, no JS errors, no sideways scroll.
  Run 40255181929 green, only the 2 known dead external links.
- Next editor (Oct 26 PT): move Cal Hacks 13.0 to past (role `mentor`), delete
  its now.yml item, bump `updated`.

Engineer backlog additions:
- [ ] New changelog desks: add them to the `desks` list in changelog.md or they get no chip (entries still show under All)
- 2026-10-25 18:34 PT — EDITOR→ENGINEER — desk filter chips on /changelog/ (changelog.md, assets/css/style.css) (Actions deploy green).

## Done (Oct 25, 2026, 7:35pm PT)

- Designer shift (UTC 02): headings reached by URL hash (post TOC, # links,
  shared links; `.post-content h2/h3[id]:target` and `h2.has-anchor:target`
  on pages) get an inset 3px accent bar + 0.6rem padding, and a 2.4s
  --accent-soft tint that fades to transparent (only with
  prefers-reduced-motion: no-preference). Text stays --text, so contrast is
  unchanged. Forced-colors: Highlight outline like the other :target rules.
  Also `.post-content li::marker` uses --text-muted; ol numbers tabular.
  Playwright mock at 375px in sepia + dark: no sideways scroll.
- 2026-10-25 19:35 PT — DESIGNER — accent bar + fading tint on deep-linked headings, muted list markers (assets/css/style.css; all /post/*, pages with # anchors) (Actions deploy green).

## Done (Oct 25, 2026, 8:35pm PT)

- Engineer shift (UTC 03): CI "Spelling" step (warnings only) runs codespell
  over the whole repo with settings in `.codespellrc` (skips .git, _site,
  fonts/images/og/icons, binaries, Gemfile.lock, _notes; ignore-words-list
  `rouge` = the Rouge highlighter, `pres` = <pre> list in check_a11y.py).
  Each hit becomes a file/line `::warning` annotation plus a count notice.
  Editors no longer need a manual codespell sweep — read the run's
  annotations. Local test: planted typos → 2 annotations; clean repo → 0.
  Run 40264967930 green. Invisible chore → no changelog entry.
- Next editor (Oct 26 PT): move Cal Hacks 13.0 to past (role `mentor`), delete
  its now.yml item, bump `updated`.

Engineer backlog additions:
- [ ] Spelling: add real names that codespell flags to `ignore-words-list` in .codespellrc (lowercase, comma-separated)
- [ ] Consider `--strict`-style blocking for spelling only after a week at 0 warnings
- 2026-10-25 20:35 PT — ENGINEER — CI spelling check with file/line annotations (.codespellrc, .github/workflows/jekyll.yml) (Actions deploy green).

## Done (Oct 25, 2026, 9:35pm PT)

- Engineer shift (UTC 04): the sepia/dark switch wrapper
  (`_includes/theme-toggle.html`) had `aria-label="Theme"` on a role-less
  `<div>` — ARIA 1.2 forbids naming generic elements, so screen readers
  dropped it. Now `role="group" aria-label="Color theme"`. `_layouts/default.html`
  head gets `<noscript><style>.theme-toggle{display:none}</style></noscript>`
  so no-JS visitors don't see a dead switch (no layout shift for JS users).
- `scripts/check_a11y.py` new rule `generic-label`: aria-label/labelledby on
  div/span/p/etc. without a role (SVG internals skipped). Mock test: flags 2,
  passes role=group/section. Run 40269978553 green, 0 a11y warnings.
- Found while reading that run: last shift's spelling step reported **815
  typos** — all from CI's `vendor/bundle` gems (the "0 warnings" claim was
  from a local run). `.codespellrc` now skips ./vendor and ./node_modules.
  Run 40270282914 green: "0 possible typo(s)". Spelling annotations are now
  trustworthy for editors.

Engineer backlog additions:
- [ ] New wrapper with aria-label: give it a role (group/region/navigation) or use `<section>`/`<nav>` — CI flags it otherwise
- [ ] When adding a CI scanner over `.`, skip ./vendor (CI installs gems there)
- 2026-10-25 21:35 PT — ENGINEER — theme switch is a named group and hidden without JS; a11y lint flags aria-label on role-less elements; codespell skips vendor/ (_includes/theme-toggle.html, _layouts/default.html, scripts/check_a11y.py, .codespellrc) (Actions deploy green).

## Done (Oct 25, 2026, 10:34pm PT)

- Editor shift (UTC 05): Cal Hacks 13.0 (Oct 23–25) moved upcoming → past in
  `_data/events.yml`, role stays `mentor` (from the Oct 14 mentor-acceptance
  email). Its expired "Mentoring" item removed from `_data/now.yml`;
  `updated` → 2026-10-26. Changelog entry added.
- Attendance: Gmail since Oct 14 has only the acceptance + Slack workspace
  emails (no check-in/QR/shift email), so attendance isn't email-confirmed.
  Row says "Mentor" only — no recap or "mentored" claim added. Waiting on
  Avinash if he wants a different label.
- Next editor: OSA Con 2026 (Nov 2) → past after Nov 2 (role `attended` is
  from registration only; keep unless he says he didn't go); its Now item has
  `until: 2026-11-02` and auto-hides.
- 2026-10-25 22:34 PT — EDITOR — Cal Hacks 13.0 moved to past events; expired Now item removed (_data/events.yml, _data/now.yml) (Actions run 40275047595 green).

## Done (Oct 25, 2026, 11:35pm PT)

- Editor shift (UTC 06): /events meta description said the list runs "from
  RubyConf India 2013 to SF Ruby 2025", stale since Cal Hacks 13.0 moved to
  past. Now "…going back to RubyConf India 2013" (no end event to go stale).
  /achievements and /research keep "to SF Ruby 2025" — those lines are about
  the Ruby community, and SF Ruby 2025 is still the latest Ruby conference.
  Search-snippet only, so no changelog entry. Run 40281006387 green.
- Checked: events.yml/now.yml current (Gmail last 3 days: only the HackUMass
  judge next-steps email for the already-listed Nov 15 row, and the
  already-logged SF Ruby 2026 Luma message); llms.txt page list matches pages.
- Last run's CI note "`updated` 2026-10-26 is in the future": the 10:34pm
  shift wrote the UTC date. Self-resolves at PT midnight. Editors: use
  `TZ=America/Los_Angeles date +%F` for `updated`.
- The SF Ruby recap's "catch the recorded talks once they're released" and
  hobby-stack's "Demo coming soon" are dated but in Avinash's own voice — left as is.

Editor backlog additions:
- [x] Set now.yml `updated` from the PT date, not UTC (CI warning now names the command, Oct 26 11:40pm PT)
- 2026-10-25 23:35 PT — EDITOR — /events meta description no longer ends at SF Ruby 2025 (events.md) (Actions run 40281006387 green).

## Done (Oct 26, 2026, 12:35am PT)

- Designer shift (UTC 07): new `_includes/diagrams/vaultmem-who-can-read.html`
  on /post/vaultmem-your-ai-agent-shouldnt-read-your-diary/ (after the "Alice
  holds the key" paragraph) — two stacked panels, "Typical agent memory" vs
  "With VaultMem": you → platform database / VaultSession → encrypted blob →
  developer, breach, subpoena, acquirer (read everything vs. see only
  encrypted bytes; dashed box). Every label comes from the post's own text.
  Existing dg-* classes only; Playwright at 375px: no text overflow, no
  sideways scroll. Run 40286841298 green.
- Posts still without a diagram: sf-ruby-2025, agent-memory-glossary,
  i-fell-in-love-with-coding-again, paper-tldr-six-papers-on-memory (roundup;
  probably fine without).
- 2026-10-26 00:35 PT — DESIGNER — who-can-read diagram on /post/vaultmem-your-ai-agent-shouldnt-read-your-diary/ (_includes/diagrams/vaultmem-who-can-read.html) (Actions run 40286841298 green).

## Done (Oct 26, 2026, 1:35am PT)

- Engineer shift (UTC 08): new `scripts/check_axe.py` + workflow step —
  axe-core 4.10.2 (npm into $RUNNER_TEMP) injected into every built page via
  the same offline local server + Chrome as check_browser.py, 1280px, plus
  /search/?q=memory and /blog/?q=memory. Tags WCAG 2.0/2.1/2.2 A+AA and
  best-practice; color-contrast off (check_browser covers it). One ::warning
  per failing rule + a ::notice "N pages audited…" + job-summary list.
  `continue-on-error`, never blocks deploys. Local run:
  `npm i axe-core@4.10.2` then `python3 scripts/check_axe.py _site --axe=node_modules/axe-core/axe.min.js`.
- First run (40293847669) found 17 elements / 2 rules, all fixed:
  landmark-unique — top and bottom series boxes were both `aside
  aria-label="Series"` → now "<title> series" / "More in <title>"
  (`_includes/series-box.html`); empty-table-header — Codex skills post's
  comparison table first header cell now has a visually-hidden "Aspect".
  Second run surfaced two wide python blocks with identical region names on
  VaultMem Part 2 → `post-tools.html` labels now "python code, block N,
  scrolls sideways" / "Table N, scrolls sideways". Run 40295215101: 46 pages,
  0 axe violations, green.
- Sandbox note: rubygems.org and the live site are blocked from this sandbox
  (no local Jekyll build) — CI annotations are the build check.

Engineer backlog additions:
- [x] axe: 375px pass (done Oct 26, 2:35am PT)
- 2026-10-26 01:35 PT — ENGINEER — axe-core accessibility audit on every deploy; fixed duplicate series-box and code-region names and an empty table header (scripts/check_axe.py, _includes/series-box.html, _includes/post-tools.html, /post/codex-skills-baking-your-workflow-into-the-tool/) (Actions run 40295215101 green).

## Done (Oct 26, 2026, 2:35am PT)

- Engineer shift (UTC 09): `scripts/check_axe.py` now audits every page twice —
  1280px and a 375px touch phone (is_mobile + has_touch, so hover:none states
  are covered); `--widths=1280,375` option; results for the second width are
  tagged "@375px". scrollable-region-focusable warnings now print the element's
  scroll/client size and tabindex. Workflow step timeout 6 → 10 min.
- First 375px run caught the Whisper post's model table: its `.table-scroll`
  overflowed by 1px (322 in 321) — post-tools said "fits" (1px tolerance) but
  the box still scrolled, so axe flagged an unreachable scrollable region.
  Fix in `_includes/post-tools.html`: when a table fits, the wrapper gets inline
  `overflow-x: visible` (restored to auto when it becomes wide); the
  ResizeObserver now also watches the table itself. Run 40302850534: 46 pages
  × 2 widths, 0 axe violations, green.
- Note: the site has no mobile menu toggle (nav is a wrapping list), so there
  are no menu states to audit.

Engineer backlog additions:
- [x] Code blocks (`pre`) use the same 1px tolerance — overflow-x: visible trick applied (done Oct 26, 3:37am PT)
- 2026-10-26 02:35 PT — ENGINEER — axe audit now also runs at 375px; fixed an unreachable 1px scroll box on the Whisper post's table (scripts/check_axe.py, _includes/post-tools.html, /post/live-audio-transcription-whisper/) (Actions run 40302850534 green).

## Done (Oct 26, 2026, 3:37am PT)

- Editor slot (UTC 10) → Engineer: nothing editorial needed — events.yml/now.yml
  current (OSA Con Nov 2 and HackUMass Nov 15 still upcoming; `updated` already
  the PT date), Gmail since Oct 25 has no new registrations, llms.txt Pages list
  matches real pages, cross-links/http links/removed-project mentions clean,
  CI shows 0 typos; only known dead links are Rena demo + daylog repo (waiting
  on Avinash).
- Engineer: `_includes/post-tools.html` code blocks now get the table fix —
  a `pre` that fits (or overflows by ≤1px) gets inline `overflow-x: visible`
  on itself and its Rouge `div.highlight` wrapper (which also has
  overflow-x:auto), restored when it becomes wide; re-checks after
  `document.fonts.ready`. Playwright mock at 375px: short blocks visible/no
  tabindex, wide block keeps auto + region label, no JS errors. Preventive (axe
  found none at 1280/375), so no changelog entry. Run 40309131332 green, 0 axe.
- 2026-10-26 03:37 PT — EDITOR→ENGINEER — nothing editorial needed; code blocks that fit no longer leave 1px scroll boxes (_includes/post-tools.html) (Actions run 40309131332 green).

## Done (Oct 26, 2026, 4:35am PT)

- Editor slot (UTC 11) → Engineer: nothing editorial needed — events.yml/now.yml
  checked an hour ago and still current, Gmail since Oct 26 has no new
  registrations (SF Ruby Conf 2026 still only Luma broadcasts — still waiting
  on Avinash).
- Engineer: new `_includes/blog-jsonld.html`, included from
  `_layouts/default.html` — /blog/ gets a `Blog` node whose `blogPost` lists
  every Writing post; /paper-tldr/ gets an `ItemList` of the TL;DRs in series
  order. Each entry is a BlogPosting (headline, url, datePublished,
  description, author → #person). `scripts/check_jsonld.py` validates them and
  the notice now reports "Blog 1 (29 posts listed …)". Run 40316535058 green,
  0 JSON-LD problems, 0 axe. Invisible (SEO metadata), so no changelog entry.

Engineer backlog additions:
- [ ] SEO notice: 6 post titles exceed 70 chars before the site name — titles
      are Avinash's words; jekyll-seo-tag has no separate <title> override, so
      leave unless he wants shorter titles
- 2026-10-26 04:35 PT — EDITOR→ENGINEER — Blog/ItemList structured data listing every post (/blog/, /paper-tldr/; _includes/blog-jsonld.html) (Actions run 40316535058 green).

## Done (Oct 26, 2026, 5:38am PT)

- Designer shift (UTC 12): `.post-content hr` (assets/css/style.css ~line 981)
  is now a centered three-dot ornament (radial-gradient, 3.75rem wide, 5px
  dots in --text-muted at 0.75) instead of a full-width 1px rule — 15 posts use
  `---` between sections, up to 15 per post. No generated text, so screen
  readers still just hear a separator. Forced-colors falls back to a
  CanvasText line; print falls back to a 1px #ccc line. Playwright mock at
  375px in sepia + dark checked by eye. Run 40324293180 green.

Designer backlog additions:
- [ ] If Avinash dislikes the dot breaks, revert to `border-top: 1px solid var(--border); margin: 2rem 0` (one rule)
- 2026-10-26 05:38 PT — DESIGNER — section breaks in posts are a centered three-dot ornament (assets/css/style.css; all /post/* using ---) (Actions run 40324293180 green).

## Done (Oct 26, 2026, 6:43am PT)

- Engineer shift (UTC 13): new `scripts/check_html.py` + workflow step "HTML
  validity" — Nu Html Checker (npm `vnu-jar@25.11.25`, Java, offline) over
  every built page, errors only. One ::warning per distinct message (count,
  pages, first line + extract), ::notice with totals, full list in the job
  summary. `continue-on-error`, never blocks deploys. Known false positive
  ignored: `<script type="speculationrules">` ("Subtype missing").
  Local: `npm i vnu-jar@25.11.25` then
  `python3 scripts/check_html.py _site --vnu=node_modules/vnu-jar/build/dist/vnu.jar`.
- First run (40333528879) found 3 real errors, all fixed: Rena post iframe
  `frameborder="0"` → `border:0` in its style; Attractor post's obsolete
  `<a name="references"></a>` removed (the "## References" h2 already has
  id=references). Run 40334343793: 46 pages, 0 HTML errors, green.
  Invisible (CI + markup), so no changelog entry.
- Sandbox note: `gh run view --log` and artifact downloads are blocked (403);
  read results via `gh api repos/.../check-runs/<job id>/annotations`.

Engineer backlog additions:
- [ ] Consider `--strict` for check_html.py after a week at 0 errors (from Nov 2)
- [ ] Drop the speculationrules IGNORE once a newer vnu accepts it
- 2026-10-26 06:43 PT — ENGINEER — CI HTML validity check (Nu Html Checker); fixed obsolete iframe/anchor markup (scripts/check_html.py, .github/workflows/jekyll.yml, /post/building-rena-ai-health-companion-gemini-live/, /post/attractor-memory-engine/) (Actions run 40334343793 green).

## Done (Oct 26, 2026, 7:39am PT)

- Engineer shift (UTC 14): AVIF photos. Pillow (has AVIF built in) made
  about-280/560.avif and sf-ruby-1-720/1086, sf-ruby-2-540/768.avif at
  quality 50, speed 4, from the original JPGs — about half the WebP bytes
  (about-560 63 → 31 KB), side-by-side crops looked identical. Each is a
  `<source type="image/avif">` before the WebP one in `_layouts/about.html`
  and the SF Ruby post. The post image viewer (`_includes/post-tools.html`
  biggest()) now keeps only the srcset holding `img.currentSrc`, so it zooms
  in the format the browser picked (no AVIF request in a WebP-only browser).
  `scripts/check_weight.py` counts only the first `<picture>` source (still
  checks every candidate exists). Playwright (Chromium, 2x): picks the .avif
  files; viewer → 1086/768/560 avif. Run 40342093804 green; /about first
  load 119 → 87 KB; 0 axe / 0 HTML errors.

Engineer backlog additions:
- [ ] New photos: ship AVIF (q50) + WebP sources, AVIF first; other posts'
      images (Rena screenshots, VaultMem explainer) are already ≤35 KB WebP — not worth it
- 2026-10-26 07:39 PT — ENGINEER — AVIF photos on /about and the SF Ruby 2025 post, viewer keeps the browser's chosen format, page-weight check counts the first <picture> source (_layouts/about.html, /post/my-sf-ruby-2025-experience-talks-side-quests-community-inspiration/, _includes/post-tools.html, scripts/check_weight.py) (Actions run 40342093804 green).

## Done (Oct 26, 2026, 8:35am PT)

- Editor shift (UTC 15) found nothing editorial: events/now current (OSA Con
  Nov 2, HackUMass Nov 15 upcoming; Gmail last 2 days only the already-logged
  HackUMass judge next-steps + SF Ruby 2026 Luma message), CI 0 typos, no
  doubled words, only known dead links (Rena demo, daylog repo — waiting on
  Avinash). Engineer backlog had nothing small left, so → DESIGNER.
- Post blockquotes (used almost only as callouts: VaultMem "Install · Code ·
  Live demo" lines, Rena "Try it", hobby-stack "My pick", two ISTQB quotes)
  are now a soft card: --surface fill, 3px accent left border, 8px right
  radius, body text color, no italics, first/last child margins trimmed;
  print drops the fill. Contrast on --surface: text 10.0:1 sepia / 14.2:1
  dark, links 5.7 / 8.4, inline code 10.4 / 11.2. Playwright mock at 375 and
  900px in both themes: no horizontal scroll. Run 40351180469 green.

- Follow-up fix: the new changelog text contains double quotes, which broke
  the arrow link's `aria-label` on / (HTML check: 4 errors). `_layouts/home.html`
  and `changelog.md` now pipe it through `| escape`. Run 40351998007: 0 HTML
  errors, 0 axe failures. Rule: any data text inside an attribute needs `| escape`.

Designer backlog additions:
- [ ] If a post ever needs a real pull-quote (his own words, attributed), add
      a `.pull-quote` class rather than restyling blockquote again
- 2026-10-26 08:35 PT — EDITOR→DESIGNER — post callouts (blockquotes) as soft cards in body text color (assets/css/style.css; /post/hobby-project-stack/, VaultMem posts, Rena, ISTQB) (Actions run 40351180469 green); escaped changelog aria-labels (_layouts/home.html, changelog.md) (run 40351998007 green).

## Done (Oct 26, 2026, 9:36am PT)

- Editor shift (UTC 16) found nothing editorial: events/now current (OSA Con
  Nov 2, HackUMass Nov 15); Gmail last day had no new registrations (only
  newsletters + the already-logged HackUMass judge email); llms.txt lists
  posts via Liquid and all real pages; SF Ruby post cross-links already done.
  → DESIGNER.
- Off-site links in `.post-content` get a small ↗ (`::after`, 0.72em, raised
  0.35em, not underlined, `content: "\2197" / ""` so screen readers skip it).
  `@media screen` only — print keeps its " (URL)" suffix. Skipped for classed
  links, links wrapping img/picture/svg (`:has`) and absolute
  avinashgosavi.com links. Arrow uses link color (no opacity) so it keeps
  the link's contrast. Playwright mock at 375px, sepia + dark: no horizontal
  scroll, internal links unchanged. Run 40361015568 green, 0 HTML/axe errors.

Designer backlog additions:
- [ ] If Avinash dislikes the ↗ arrows, delete the one `@media screen` block after `.post-content a:hover` in style.css
- [x] Could extend ↗ to page prose (done Oct 26, 10:35am PT)
- 2026-10-26 09:36 PT — EDITOR→DESIGNER — off-site links in posts end in a small ↗ (assets/css/style.css; all /post/*) (Actions run 40361015568 green).

## Done (Oct 26, 2026, 10:35am PT)

- Designer shift (UTC 17): the off-site ↗ marker (style.css `@media screen`
  block after `.post-content a:hover`) now also applies to unclassed links in
  `.main :is(p, li, dd, blockquote, td)` — same scope as the page-prose link
  rule. Shows on /research (Zenodo/PyPI/Code, newsletters), /now
  (nownownow), /achievements (PyPI, DOI). Classed links (paper titles, talk
  titles, now-more, event recap) and the footer (outside .main) stay
  arrow-free. Playwright mock at 375px: arrows only on plain external links,
  no horizontal scroll. Run 40370206261 green.
- To revert just the page part: change the selector back to
  `.post-content a[href^="http"]…`.
- 2026-10-26 10:35 PT — DESIGNER — off-site ↗ marker extended from posts to page prose (assets/css/style.css; /research/, /now/, /achievements/) (Actions run 40370206261 green).

## Done (Oct 26, 2026, 11:35am PT)

- Engineer shift (UTC 18): CSS minification at build. New
  `_plugins/minify_css.rb` (`:site, :post_write` hook) rewrites
  `_site/assets/css/*.css`: comments removed, whitespace collapsed, spaces
  around `{ } ; ,` and the last `;` before `}` dropped. Quoted strings are
  tokenized and copied untouched; `:`/`+`/`~`/`>` spacing is never changed
  (selectors and calc() depend on it). style.css 62.4 KB → 47.3 KB raw,
  14.5 KB → 9.5 KB gzipped. Source file stays commented. `CSS_MINIFY=0`
  skips it.
- Verified in Chromium: original and minified sheets parse to the same 465
  CSSOM rules (only diff: comma spacing inside custom-property raw values).
- `_plugins/asset_version.rb` now hashes the minified bytes for .css, so the
  `?v=` matches what's served (first push failed the "content-hash version"
  CI step; fixed in the next commit). Run 40379607081 green: 0 HTML/axe
  errors, browser + contrast checks clean.
- Sandbox note: www.avinashgosavi.com and Actions artifact downloads are
  blocked by the proxy, and bundle install can't reach rubygems — compare
  CSS via CSSOM in Playwright (setContent) instead of live screenshots.

Engineer backlog additions:
- [ ] If any style ever looks off after a CSS edit, rebuild with `CSS_MINIFY=0` to rule the minifier out
- [ ] Could also drop the space after `:` in declarations (only inside `{…}` blocks, never in selectors) — ~1 KB more, not worth the risk yet
- 2026-10-26 11:35 PT — ENGINEER — stylesheet minified at build, ~35% fewer gzipped CSS bytes on every page (_plugins/minify_css.rb, _plugins/asset_version.rb) (Actions run 40379607081 green).

## Done (Oct 26, 2026, 12:35pm PT)

- Engineer shift (UTC 19): IndexNow. Build step `indexnow` runs
  `scripts/indexnow.py diff _site` — compares `_site/sitemap.xml` with the
  live sitemap (fetched before deploy) and lists URLs that are new or whose
  `<lastmod>` changed; live fetch failure → submits nothing. New `indexnow`
  job (needs build + deploy, skipped when the list is empty,
  `continue-on-error`) POSTs them to api.indexnow.org (Bing, Yandex, Seznam,
  Naver share submissions). Key file `/cd4471ebd9b322f9b4bc4d7adab382c5.txt`
  at the root (README says keep it). Not in the sitemap (static .txt).
- Run 40388394067 green: notice "0 of 43 sitemap URLs changed" (only
  workflow/README/script changed), indexnow job correctly skipped. The submit
  path is tested locally only — first real submission happens on the next
  commit that changes a page. Invisible to visitors, so no changelog entry.

Engineer backlog additions:
- [x] Next page-changing run: check the `indexnow` job log (done Oct 26, 1:35pm PT — run 40397306689 submitted /events/, HTTP 202)
- [ ] Waiting on Avinash: Bing Webmaster Tools → IndexNow tab shows these submissions once the site is verified there
- 2026-10-26 12:35 PT — ENGINEER — IndexNow pings for pages changed in each deploy (scripts/indexnow.py, .github/workflows/jekyll.yml, key .txt at root) (Actions run 40388394067 green).

## Done (Oct 26, 2026, 1:35pm PT)

- Editor shift (UTC 20) found nothing editorial: events/now current (OSA Con
  Nov 2, HackUMass Nov 15); Gmail last day: no new registrations (only an
  SF Ruby conf promo email — no ticket); CI 0 typos, 0 internal broken links,
  only the known dead links (Rena demo, daylog repo); llms.txt in step;
  older-post cross-links already saturated. → ENGINEER.
- /events self-files ended events (same idea as now.yml `until`). events.md:
  at build, an `upcoming` row whose last day (end_date or date) is >1 day
  behind the UTC build clock renders under Past (Liquid `push` + `concat`,
  re-sorted newest first); lede counts now use that merged Past list. In the
  browser, upcoming rows with data-end < visitor's local date move to the top
  of Past (`#past-list`), their hidden "Happening now" tag is removed, and an
  emptied Upcoming h2/list is hidden. Playwright mock with a fixed clock
  (Oct 26 → B "Happening now", A moved; Oct 27 → both moved, heading hidden).
  Editors still flip `status` to `past` (check_data warns after 3 days) and
  decide the role. README /events row notes it. Run 40397306689 green: 0
  HTML/axe/browser issues.
- IndexNow first real submission: /events/ → HTTP 202. Note: / and
  /changelog/ show the new changelog entry but weren't submitted — their
  sitemap lastmod follows their own source files, not _data/changelog.yml.

Engineer backlog additions:
- [x] IndexNow/sitemap: pages built from `_data/` take lastmod from their data file's git date too (done Oct 26, 2:35pm PT)
- 2026-10-26 13:35 PT — EDITOR→ENGINEER — ended events move from Upcoming to Past by themselves (events.md, README.md) (Actions run 40397306689 green).

## Done (Oct 26, 2026, 2:35pm PT)

- Editor shift (UTC 21) found nothing editorial: events/now current (OSA Con
  Nov 2, HackUMass Nov 15); Gmail last day: no new registrations (only the
  already-logged SF Ruby conf promo, plus newsletters); llms.txt in step.
  → ENGINEER.
- `_plugins/git_last_modified.rb`: pages (not posts) now take the newest of
  their own git date and the git date of every `_data/<name>.{yml,yaml,json,csv}`
  they read via `site.data.<name>` — scanned in the page source, its layout
  chain (skipping site-wide `default`, whose `site.data.series` would date
  every page) and includes referenced there (one level). Homepage lastmod
  went from 2026-02-21 to today (changelog/projects/experience/now data).
  Posts excluded so series.yml edits don't redate every series part.
  Tested with stubbed Jekyll against the real repo (no local Jekyll).
  README notes it. Run 40405856813 green; IndexNow job submitted /,
  /changelog/, /now/ (HTTP 200). Invisible to visitors → no changelog entry.
- Sandbox note: `gh run view --log` is blocked (results-receiver 403); use
  the GitHub MCP `get_job_logs` with the job id instead.
- 2026-10-26 14:35 PT — EDITOR→ENGINEER — data-driven pages (/, /changelog/, /now/, /events/…) get sitemap lastmod + IndexNow pings from their _data files (_plugins/git_last_modified.rb, README.md) (Actions run 40405856813 green).

## Done (Oct 26, 2026, 3:35pm PT)

- Designer shift (UTC 22): `.changelog-desk` badges (homepage "Latest updates"
  + /changelog) were identical grey pills although the markup already had
  `changelog-desk-<slug>` classes. Added a 0.5em colored dot via `::before`
  (`--desk` token): Writing → `--cat-agents`, Design → `--cat-fun`,
  Engineering → `--accent`; unknown desks → `--text-muted`. Label text
  unchanged (muted). Dot contrast on `--code-bg`: sepia 4.8 / 5.4 / 4.3,
  dark 5.6 / 6.3 / 6.6. min-width 6.2 → 7rem so ENGINEERING still fits with
  the dot (all pills same width). Playwright CSSOM mock at 375px, sepia +
  dark: no horizontal scroll. Live site and rubygems are blocked from this
  sandbox (no live screenshots, no local Jekyll). Run 40413747752 green.

Designer backlog additions:
- [ ] If Avinash dislikes the desk dots, delete the `.changelog-desk::before` block and the four `--desk` lines after `.changelog-desk` in style.css
- [ ] New changelog desk: give it a `.changelog-desk-<slug> { --desk: … }` hue (≥3:1 on --code-bg in both themes)
- 2026-10-26 15:35 PT — DESIGNER — changelog desk labels get a colored dot per desk (assets/css/style.css; /, /changelog/) (Actions run 40413747752 green).

## Done (Oct 26, 2026, 4:35pm PT)

- Engineer shift (UTC 23): offline pages kept their text but lost images
  (sw.js sent /assets/images/ straight to the network). sw.js now serves
  `/assets/images/*` stale-while-revalidate from a new `images-v1` cache
  (newest 60, LRU by re-insert, Range requests skipped, only 200 basic
  responses stored; cache writes in waitUntil so first loads aren't delayed).
  Header comment updated. Playwright mock (localhost, rendered sw.js): image
  cached on 2nd load, page reload with context offline → image naturalWidth
  360. Changelog entry links the SF Ruby post (has photos).
- Kill switch unchanged; to drop just this: delete the `/assets/images/`
  branch in the fetch listener (and `caches.delete('images-v1')` in activate).

Engineer backlog additions:
- [ ] If images ever get replaced in place under the same filename, offline
      visitors see the old one once (refreshed in the background) — fine
- 2026-10-26 16:35 PT — ENGINEER — offline-saved pages keep their photos and diagrams (sw.js images-v1 cache) (Actions run 40421061246 green).

## Done (Oct 26, 2026, 5:35pm PT)

- Editor slot (UTC 00) → Designer: events/now still current (OSA Con Nov 2,
  HackUMass Nov 15 upcoming; Gmail last 4 days: no new registrations);
  codespell 0; llms.txt in step. Only CI warnings are the known dead Rena demo
  + daylog repo links (still waiting on Avinash).
- New `_includes/diagrams/six-papers-map.html` on
  /post/paper-tldr-six-papers-on-memory/ (after the intro): six paper boxes →
  Attractor / daylog / VaultMem. Edges only where the post's "What I took from
  it" says so (Hopfield, Modern Hopfield, CLS → Attractor; Sentence-BERT → all
  three; LoCoMo, Memory as Asset → VaultMem). Existing dg-* classes only.
  Playwright at 375px sepia + dark: no text overflow, no sideways scroll.
  Run 40427863415 green.
- Posts still without a diagram: sf-ruby-2025, agent-memory-glossary,
  i-fell-in-love-with-coding-again — leave them (no flow described).
- Stale backlog items re-checked and already done: theme-color/color-scheme
  (~297), theme flash (~330), search anchors (~176).
- 2026-10-26 17:35 PT — EDITOR→DESIGNER — paper-to-project map diagram (/post/paper-tldr-six-papers-on-memory/) (Actions run 40427863415 green).

## Done (Oct 26, 2026, 6:34pm PT)

- Editor slot (UTC 01) → Engineer: events/now still current (OSA Con Nov 2,
  HackUMass Nov 15 upcoming); Gmail last day: no new registrations (only
  another SF Ruby Conf 2026 promo — still waiting on Avinash).
- New `/events.ics` (events.ics, Liquid, `sitemap: false`): upcoming events
  from events.yml as all-day VEVENTs (same ended-cutoff as events.md; DTEND
  exclusive = day after end; SUMMARY gets "(Judge)/(Mentor)…" unless
  attended; text escaped `\ ; ,`; UID `<slug>@avinashgosavi.com`; URL to the
  /events/ anchor; REFRESH-INTERVAL P1D). `_plugins/ics_crlf.rb` rewrites any
  .ics page with CRLF and 75-octet folding (UTF-8 safe). /events/ shows an
  "Add upcoming events to your calendar" line under Upcoming (`.events-ics`,
  hidden by the JS when Upcoming empties). New warning-only CI step prints the
  file and checks envelope/line lengths: run 40433683195 green, "2 events,
  0 bad lines" (OSA Con, HackUMass).
- Local Jekyll build impossible in the sandbox (rubygems 403 via proxy); run
  logs readable via the GitHub MCP get_job_logs (gh --log is 403).

Engineer backlog additions:
- [ ] Past events deliberately left out of events.ics (year-only dates like
      "2014" would show as Jan 1) — add only if they get real dates
- 2026-10-26 18:34 PT — EDITOR→ENGINEER — subscribable calendar of upcoming events (/events.ics, link on /events/) (Actions run 40433683195 green).

## Done (Oct 26, 2026, 7:35pm PT)

- Designer shift (UTC 02): hover/focus color rules re-audited by hand (all use
  --accent-ink/--accent on known-good backgrounds; nothing to fix). Found a
  list-rhythm gap instead: nested `ul`/`ol` inside a post `li` inherited the
  top-level `margin: 0 0 1rem`, so the item after a nested list sat 18px
  below vs 6.3px between plain siblings (ISTQB checklist steps 6–7). New rule
  `.post-content li > ul, li > ol { margin: 0.35rem 0 0 }`. Playwright CSSOM
  mock at 375px, sepia + dark: gaps now 6.3px everywhere, no sideways scroll.
  Only post with nested lists today: reviewing-ai-generated-tests-istqb-framework.

Designer backlog additions:
- [ ] If nested lists ever need more air, raise only the `li > ul/ol` top margin
- 2026-10-26 19:35 PT — DESIGNER — nested lists in posts keep the sibling-item spacing (assets/css/style.css; /post/reviewing-ai-generated-tests-istqb-framework/) (Actions run 40439378809 green).

## Done (Oct 26, 2026, 8:35pm PT)

- Engineer shift (UTC 03): new `_plugins/post_markdown.rb` (`:site,
  :post_write` hook) writes `/post/<slug>.md` for every post (llms.txt
  convention): the post's own Markdown source with Liquid rendered via
  `Jekyll::Renderer#render_liquid` (post_url, image paths, diagram includes),
  `<figure class="diagram">` → blockquote "Diagram: title / desc / caption"
  with a link to the post, whole-line kramdown IALs dropped, on-site
  `](/`, `href/src="/` and srcset entries made absolute; header (title, by,
  date, URL, topics, description) and an "Original post" footer. Errors only
  warn. `markdown_url` filter. Linked from post `<head>` (rel=alternate
  type=text/markdown), a "Markdown" link in the share row (posts only), and
  /llms.txt (note + "[Markdown]" per post). Speculation rules exclude `/*.md`.
  Run 40445285703 green, "PostMarkdown: wrote 29 Markdown copies", 0 HTML
  errors, no internal-link warnings. Live site not fetchable from the
  sandbox (proxy 403), so added a warning-only CI step that prints the
  Attractor copy and flags missing copies or leftover `{%`/`{{`/`<svg`/`](/`.

Engineer backlog additions:
- [x] Post Markdown CI step (run 40445909138): 29 posts, 29 copies, 0 problems;
      Attractor copy reads cleanly (header, absolute links)
- [ ] Inline kramdown IALs (`text{: .x}`) still show in the .md copies — none today
- 2026-10-26 20:35 PT — ENGINEER — plain Markdown copy of every post (/post/<slug>.md; share-row link, head alternate, /llms.txt) (Actions run 40445285703 green).

## Done (Oct 26, 2026, 9:35pm PT)

- Engineer shift (UTC 04): metric-matched fallback font. New
  `"DM Sans Fallback"` @font-face pair in assets/css/style.css (before
  `:root`) — local Arial / Liberation Sans / Arimo (regular 400, bold 700)
  with size-adjust 103.5% / 101% (DM Sans ÷ Arial advance width over the
  site's own post text, measured with canvas in Playwright: 400→1.035,
  500→1.054, 600→1.001, 700→1.018) and ascent/descent overrides from DM Sans
  hhea (992/−310 per 1000) ÷ size-adjust. `--font-sans` is now
  `"DM Sans", "DM Sans Fallback", system-ui, sans-serif`. Playwright on
  ~14k chars of post text in `.post-content`: height shift on swap 394px →
  52px at 375px, 267px → 112px at 1024px (vs. the old system-ui stack in the
  sandbox). Android has no Arial, so it still falls to system-ui (unchanged).

Engineer backlog additions:
- [ ] If a new DM Sans weight/axis is added, re-measure size-adjust (scratch
      script: canvas measureText DM vs Liberation Sans over post text)
- [ ] JetBrains Mono has no metric fallback — code blocks scroll rather than
      wrap, so a swap barely shifts layout; leave unless CLS shows up there
- 2026-10-26 21:35 PT — ENGINEER — metric-matched DM Sans fallback font so text doesn't reflow when the webfont loads (assets/css/style.css, site-wide) (Actions run 40450768426 green).

## Done (Oct 26, 2026, 10:34pm PT)

- Editor shift (UTC 05): events/now still current (OSA Con Nov 2, HackUMass
  Nov 15 upcoming; Cal Hacks already past). Gmail last 2 days: no new event
  registrations (HackUMass team update, promos only). now.yml `updated` →
  2026-10-27 (all items still valid).
- /llms.txt was missing the new /events.ics feed — added "Upcoming events
  calendar" line after Conferences & community.
- 2026-10-26 22:34 PT — EDITOR — /llms.txt lists the upcoming-events calendar (/events.ics); now.yml re-verified (Actions run 40456199282 green).

## Done (Oct 26, 2026, 11:40pm PT)

- Editor shift (UTC 06): events/now still current (OSA Con Nov 2, HackUMass
  Nov 15 upcoming). Gmail last day: no new registrations (SF Ruby conf promo,
  Devpost/newsletters only). codespell over _posts, pages, _data: 0.
- The 10:34pm PT shift set now.yml `updated` to 2026-10-27 (UTC date) — /now
  showed tomorrow. Reset to 2026-10-26; the check_data.py "in the future"
  warning now says `TZ=America/Los_Angeles date +%F`, not the UTC date.
  No changelog entry (correction of a date).
- 2026-10-26 23:40 PT — EDITOR — now.yml `updated` back to the PT date; data check explains PT dates (_data/now.yml, scripts/check_data.py) (Actions run 40462069782 green).

## Done (Oct 27, 2026, 12:35am PT)

- Designer shift (UTC 07): `.post-content code` gets
  `box-decoration-break: clone` (+ -webkit-). Long inline code
  (`http://daylog-vault-service.internal:8000` in hobby-project-stack,
  `sentence-transformers/all-MiniLM-L6-v2` in daylog-security-architecture)
  wraps at 375px; each wrapped piece now has its own padding and rounded ends
  instead of a chip sliced open at the line edge. `pre code` unaffected
  (no padding/background). Playwright mock at 375px sepia + dark:
  scrollWidth 375, no overflow (no local Jekyll — rubygems 403).

Designer backlog additions:
- [x] Inline code outside posts (uses.md) has no chip style (done Oct 27, 5:36am PT)
- 2026-10-27 00:35 PT — DESIGNER — wrapped inline code in posts keeps rounded, padded ends on each line (assets/css/style.css; /post/hobby-project-stack/, /post/daylog-security-architecture/) (Actions run 40468233919 green).

## Done (Oct 27, 2026, 1:35am PT)

- Engineer shift (UTC 08): new `_includes/suggest-edit.html`, included in
  `_layouts/post.html` right after Share: "Spotted a typo or a broken link?
  Suggest an edit on GitHub · See this post's history" — links built from
  `page.path` (`/edit/main/_posts/…md`, `/commits/main/_posts/…md`; repo is
  public). Muted 0.85rem line, accent-ink links; hidden in print.
  `scripts/check_external.py` skips those two URL prefixes (SKIP_PREFIXES) so
  ~58 new URLs don't eat the 150s budget (/edit/ needs a login anyway).
  Run 40474835069 green: 0 html errors, 0 axe, external links unchanged
  (89 URLs, same 2 known dead). Live site not reachable from this sandbox.

Engineer backlog additions:
- [ ] If Avinash doesn't want edit PRs from strangers, drop the include line in post.html (one line) — or keep only the history link
- [ ] If the repo is renamed or goes private, update the `repo` URL in suggest-edit.html and SKIP_PREFIXES in check_external.py
- 2026-10-27 01:35 PT — ENGINEER — "Suggest an edit on GitHub" + post history links at the end of every post (_layouts/post.html, _includes/suggest-edit.html; e.g. /post/sf-ruby-2025/) (Actions run 40474835069 green).

## Done (Oct 27, 2026, 2:34am PT)

- Engineer shift (UTC 09): new `_includes/og-image-meta.html`, included right
  after `{% seo %}` in `_layouts/default.html`. Every page now has
  `og:image:alt` + `twitter:image:alt` (jekyll-seo-tag emits neither):
  generated cards (/assets/og/) → "<page title> — share card from
  avinashgosavi.com" plus og:image:width 1200 / height 630 / type image/png;
  site default about.jpg → "Photo of Avinash Gosavi"; photo share images use
  new `image_alt:` front matter (sf-ruby-2025: photo-booth description from
  looking at sf-ruby-1.jpg, no other names; rena post: "Home screen of the
  Rena app on a phone"). `scripts/check_seo.py` warns when a page with
  og:image lacks either alt tag. Run 40482046120 green; build annotations show
  0 og:image alt warnings (only the known long-title notice + 2 dead links).

Engineer backlog additions:
- [ ] Any post with a photo `image:` (not /assets/og/) needs `image_alt:` in front matter — CI SEO lint warns otherwise
- 2026-10-27 02:34 PT — ENGINEER — share-preview images get alt text + card dimensions on every page (_includes/og-image-meta.html, _layouts/default.html; e.g. /post/sf-ruby-2025/) (Actions run 40482046120 green).

## Done (Oct 27, 2026, 3:35am PT)

- Editor shift (UTC 10): events/now still current (OSA Con Nov 2, HackUMass
  Nov 15 upcoming). Gmail last 2 days: no new registrations (HackUMass judge
  next steps, SF Ruby conf promo, newsletters). now.yml `updated` → 2026-10-27
  (PT date). Cross-links in older posts re-checked — all in place.
- SF Ruby 2025 post still says "catch the recorded talks once they're
  released" — talks.yml links RubyEvents recordings, but rubyevents.org was
  blocked from this sandbox (proxy 403), so the wording wasn't changed
  (needs a source opened in-run; the post already links /talks/).
- → Engineer: talks in site search. talks.md rows get `id="talk-<title|slugify>"`;
  search.json adds a `Talk` entry per _data/talks.yml row (url
  /talks/#talk-…, tags = speaker + event + topic, desc = "speaker · event —
  take"); search.md TYPES/PLURAL gain Talk (filter chip "Talks"). Existing
  `.paper:target` style highlights the row. 13 slugs unique. Run 40490543478
  green: 0 html errors, 0 axe, no new warnings.

Engineer backlog additions:
- [ ] New talks.yml rows need unique titles (the slug is the anchor + search URL)
- [x] Editor: SF Ruby post's "once they're released" line now links the recordings (done Oct 27, 8:35am PT)
- 2026-10-27 03:35 PT — EDITOR→ENGINEER — recommended talks are searchable and link to their row (/search/, /talks/, search.json); now.yml re-verified (Actions run 40490543478 green).

## Done (Oct 27, 2026, 4:34am PT)

- Editor shift (UTC 11): events.yml / now.yml still current (checked an hour
  ago too; OSA Con Nov 2, HackUMass Nov 15 upcoming). Copy now matches the
  new talks-in-search feature: /search/ lede + meta description, opensearch.xml
  Description, /blog/ no-results link, llms.txt Search + Search index lines.
  External-link sweep (95 URLs) inconclusive: github.com and most hosts are
  blocked by this sandbox's proxy (403/000), so nothing was changed.
  Run 40497348074 green.
- 2026-10-27 04:34 PT — EDITOR — search copy mentions recommended talks (/search/, /blog/, /llms.txt, /opensearch.xml) (Actions run 40497348074 green).

## Done (Oct 27, 2026, 5:36am PT)

- Designer shift (UTC 12): `.prose-page code` joins `.post-content code`
  (JetBrains Mono chip on --code-bg, clone decoration) and `.prose-page pre
  code` joins the pre reset. Only inline code outside posts today is
  `qwen2.5:14b` on /uses/ (was browser-default monospace, no chip). Data
  files render no inline code. Playwright mock at 375px: no overflow.
- Diagram coverage: every post except sf-ruby-2025, i-fell-in-love-with-coding-again
  and the glossary now has one — those three don't need one.

Designer backlog additions:
- [ ] New pages using `<code>`: give the wrapper `prose-page` (or add the selector) so inline code gets the chip
- 2026-10-27 05:36 PT — DESIGNER — inline code chip on prose pages (assets/css/style.css; /uses/) (Actions run 40505274184 green).

## Done (Oct 27, 2026, 6:36am PT)

- Engineer shift (UTC 13): achievements in site search. achievements.md rows
  get `id="ach-<title|slugify>"` (10 titles, all unique); search.json adds an
  `Achievement` entry per achievements.yml item (url /achievements/#ach-…,
  date = year, tags = section + year, desc = detail); search.md TYPES/PLURAL
  gain Achievement (chip "Achievements"). `.achievement:target` = accent bar
  only (no tint), scroll-margin 5rem. Search copy updated in search.md lede +
  description, llms.txt Search line, opensearch.xml Description.
  Run 40513685233 green (all checks + deploy).

Engineer backlog additions:
- [ ] New achievements.yml items need unique titles (slug = anchor + search URL)
- [x] Experience roles (experience.yml) in search (done Oct 27, 7:35am PT)
- 2026-10-27 06:36 PT — ENGINEER — achievements searchable with deep links + "Achievements" filter chip (/search/, /achievements/, search.json) (Actions run 40513685233 green).

## Done (Oct 27, 2026, 7:35am PT)

- Engineer shift (UTC 14): work roles in site search. experience.md
  `.timeline-role` divs get `id="role-<company + title, & → and | slugify>"`
  (11 roles, all unique); search.json adds a `Role` entry per role (title
  "<role> — <company>", url /experience/#role-…, date = period, tags = job
  tags + company + location, desc = company · location · period, text = the
  role's highlights so snippets show matched lines). search.md TYPES/PLURAL
  gain Role (chip "Roles"). `.timeline-role:target` = accent bar only,
  scroll-margin 5rem; forced-colors outline list now also covers
  `.achievement:target` and `.timeline-role:target`. Search copy updated
  (search.md lede + description, llms.txt, opensearch.xml). Run 40522808204
  green: 111 index entries incl. Role 11, 0 html errors, 0 axe.

Engineer backlog additions:
- [ ] New experience.yml roles: company + title must stay unique (slug = anchor + search URL)
- 2026-10-27 07:35 PT — ENGINEER — work roles searchable with deep links + "Roles" filter chip (/search/, /experience/, search.json) (Actions run 40522808204 green).

## Done (Oct 27, 2026, 8:35am PT)

- Editor shift (UTC 15): events.yml / now.yml still current (OSA Con Nov 2,
  HackUMass Nov 15 upcoming; Cal Hacks already past). SF Ruby 2025 post: the
  stale "catching the recorded talks once they're released!" now reads
  "catching the [recorded talks](https://www.rubyevents.org/events/sfruby-2025/talks)!"
  — source: rubyevents.org event page for SF Ruby 2025 (Nov 19–20, 2025, 63
  talks, most with video), opened via WebFetch this run (curl is proxy-blocked).
  Run 40532692265 green.
- 2026-10-27 08:35 PT — EDITOR — SF Ruby 2025 recap links the recorded talks on RubyEvents (/post/my-sf-ruby-2025-experience-talks-side-quests-community-inspiration/) (Actions run 40532692265 green).

## Done (Oct 27, 2026, 9:35am PT)

- Editor shift (UTC 16): events.yml / now.yml still current (no changes).
  codespell over _posts, pages and _data: no typos. llms.txt "Search index"
  line now lists achievements and work roles (added to search.json today).
  Run 40542472881 green.
- 2026-10-27 09:35 PT — EDITOR — llms.txt search-index description lists achievements and work roles (/llms.txt) (Actions run 40542472881 green).

## Done (Oct 27, 2026, 10:35am PT)

- Designer shift (UTC 17): theme-matched scrollbars. `scrollbar-color:
  var(--scroll-thumb) transparent` on body.theme-sepia / body.theme-dark
  (inherits to pre, .table-scroll, etc.) and on `html:has(> body.theme-…)`
  for the page scrollbar (theme class lives on body). Thumb sepia #8c8069
  (3.39:1 on --bg, 3.06:1 on --code-bg), dark #81776a (3.42 / 3.08:1).
  Forced-colors resets to `auto`. Playwright mock at 375px: computed values
  correct in both themes, no overflow. Run 40552283685 green.

Designer backlog additions:
- [ ] If --bg/--code-bg change, re-check --scroll-thumb stays >= 3:1
- 2026-10-27 10:35 PT — DESIGNER — warm theme-matched scrollbars on page, code blocks and wide tables (assets/css/style.css; all pages) (Actions run 40552283685 green).

## Done (Oct 27, 2026, 11:35am PT)

- Engineer shift (UTC 18): CI annotations showed 2 broken internal links on
  /changelog/ — the 01:35 and 02:34 PT entries linked `/post/sf-ruby-2025/`
  (the post's permalink is the long slug). Fixed in _data/changelog.yml
  (run 40561462778 green, no broken-link annotations). They sat unnoticed for
  ~10 hours because the internal check was warnings-only, so
  `scripts/check_links.py _site --strict` now fails the build (no
  continue-on-error). Outbound checks stay warnings-only. Run 40562292776 green.

Engineer backlog additions:
- [ ] A red "Check internal links" step means a page or #anchor link is wrong —
      fix the link (or the changelog `link:`), never drop `--strict`
- [ ] Changelog `link:` must be a real permalink (post front matter `permalink:`), not the file name
- 2026-10-27 11:35 PT — ENGINEER — fixed two broken changelog links to the SF Ruby post (/changelog/); broken internal links now fail CI (.github/workflows/jekyll.yml) (Actions runs 40561462778, 40562292776 green).

## Done (Oct 27, 2026, 12:35pm PT)

- Engineer shift (UTC 19): `@media (prefers-contrast: more) and
  (forced-colors: none)` block at the end of assets/css/style.css. Sepia:
  --text-muted #3f3934 (9.9:1 on --bg), --accent #0a5f58 (= accent-ink,
  6.6:1 bg / 5.7:1 surface), --border/--border-header #8c8069 (3.4:1). Dark:
  --text-muted #cfc8bc (9.1:1), --border/--border-header #81776a (3.4:1).
  Prose link underlines go to full currentColor. Playwright mock (real CSS,
  emulateMedia contrast more/no-preference) at 375px: computed tokens correct
  in both themes, no overflow. Run 40571011768 green (0 html errors, only the
  2 known dead links).
- Considered and rejected: `content-visibility: auto` on `.changelog-day`
  (relayout 13ms → 0.7ms on a 5× mock) — it broke `/changelog/#<date>`
  anchor landing with the site's smooth scroll-behavior (landed thousands of
  px off). Don't retry without fixing anchor scroll.

Engineer backlog additions:
- [ ] If sepia/dark --text-muted/--border/--accent change, re-check the prefers-contrast: more overrides still beat them
- 2026-10-27 12:35 PT — ENGINEER — increase-contrast mode: firmer muted text, borders and link underlines in sepia + dark (assets/css/style.css; all pages) (Actions run 40571011768 green).

## Done (Oct 27, 2026, 1:35pm PT)

- Editor shift (UTC 20) found nothing editorial: events.yml/now.yml current
  (OSA Con Nov 2, HackUMass Nov 15 upcoming; Cal Hacks past), Gmail last 2
  days: no new event registrations (HackUMass judge RSVP reminder only),
  older posts already cross-linked via post_url. Took an Engineer task.
- Per-topic Atom feeds: `_plugins/topic_feeds.rb` generates
  `/feed/topic/<slug>.xml` (layout `_layouts/topic-feed.html`, newest 20,
  full content with feed_diagrams, sitemap false) for every post tag with >= 2
  posts (all posts, TL;DRs included) — today 7: agent-memory 18, research 13,
  privacy 6, ai-tools 3, tutorials 3, agents 2, local-first 2. On /blog/,
  chips whose tag has a feed carry `data-feed`; picking one turns the lede's
  "Subscribe via RSS" into "Subscribe to “<topic>” via RSS" pointing at the
  topic feed (All → /feed.xml). llms.txt lists the topic feeds; CI Atom
  check now globs `_site/feed/**/*.xml` recursively. Local bundle install
  blocked (rubygems 403), so CI was the build check. Run 40579926772 green.

Engineer backlog additions:
- [x] Topic-feed threshold: now one setting, `topic_feed_min` in _config.yml (done Oct 28, 12:35pm PT)
- 2026-10-27 13:35 PT — EDITOR→ENGINEER — per-topic RSS feeds (/feed/topic/<slug>.xml); /blog/ Subscribe link follows the active topic chip (Actions run 40579926772 green).

## Done (Oct 27, 2026, 2:35pm PT)

- Editor shift (UTC 21): events.yml / now.yml still current (OSA Con Nov 2,
  HackUMass Nov 15 upcoming); Gmail last day: no new registrations (HackUMass
  judge RSVP reminder only). /uses "AI tooling" now cross-links existing
  posts: faster-whisper → /post/live-audio-transcription-whisper/,
  sentence-transformers → /post/paper-tldr-sentence-bert/, LangGraph →
  /post/ai-history-blog-generator/ (each post names that tool). Run
  40588156992 green.
- 2026-10-27 14:35 PT — EDITOR — /uses AI-tooling list links faster-whisper, sentence-transformers and LangGraph to the posts that use them (/uses/) (Actions run 40588156992 green).

## Done (Oct 27, 2026, 3:35pm PT)

- Designer shift (UTC 22): `text-wrap: pretty` (typography-rhythm block near
  the end of style.css) extended from post prose to page prose — .page-lede,
  .hero-intro, .about-content p, .prose-page p/li, .interest-list li,
  .now-list dd, .achievement-detail, .paper-tldr, .timeline-highlights li,
  .experience-lede. Progressive enhancement; no color/size changes, so
  contrast unchanged. Live site unreachable from sandbox (proxy 403), so no
  screenshots; CI was the build check. Run 40596070835 green.

Designer backlog additions:
- [ ] New page paragraph classes: add them to the `text-wrap: pretty` list in style.css
- 2026-10-27 15:35 PT — DESIGNER — orphan-free wrapping for page prose (assets/css/style.css; /about/, /now/, /research/, /uses/, /achievements/, /experience/) (Actions run 40596070835 green).

## Done (Oct 27, 2026, 4:34pm PT)

- Engineer shift (UTC 23): topic-feed autodiscovery. `_layouts/default.html`
  now emits `<link rel="alternate" type="application/atom+xml" title="<tag>
  topic">` for the /feed/topic/<slug>.xml feeds (pages with layout
  `topic-feed`, from _plugins/topic_feeds.rb): each post lists the feeds of
  its own tags, /blog/ lists all 7. Feed readers pasted a post URL now offer
  "follow this topic". Run 40603244480 green (0 html errors, 0 axe, internal
  links strict OK). Couldn't eyeball built HTML: artifact download and live
  site are both proxy-blocked from this sandbox — next shift with access,
  spot-check `<head>` of /blog/ and one post.

Engineer backlog additions:
- [x] Spot-check topic-feed `<link rel=alternate>` tags in built /blog/ and a post head (CI step added Oct 27, 5:35pm PT)
- 2026-10-27 16:34 PT — ENGINEER — posts and /blog/ advertise their per-topic Atom feeds for feed-reader autodiscovery (_layouts/default.html; /blog/, every post) (Actions run 40603244480 green).

## Done (Oct 27, 2026, 5:35pm PT)

- Editor shift (UTC 00) found nothing editorial: events.yml/now.yml current
  (OSA Con Nov 2, HackUMass Nov 15 upcoming; `updated` already today PT);
  codespell 0; llms.txt in step; older posts already cross-linked. Gmail
  search returned a quota error, so no registration check this run; outbound
  link checks and local bundle install are proxy-blocked here. Took an
  Engineer task.
- CI: new warnings-only step "Topic feeds are advertised for autodiscovery"
  (.github/workflows/jekyll.yml) — compares _site/feed/topic/*.xml with the
  `<link rel="alternate" … title="<tag> topic">` hrefs in /blog/'s head and
  warns per missing feed; prints how many posts advertise at least one.
  Run 40609839451 green with no topic-feed warnings (run logs are proxy-
  blocked; annotations read via the check-runs API). Invisible chore — no
  changelog entry.

Engineer backlog additions:
- [ ] Run logs (`gh run view --log`) 403 from this sandbox — read `check-runs/<job>/annotations` instead
- 2026-10-27 17:35 PT — EDITOR→ENGINEER — CI now warns if topic feeds stop being advertised for autodiscovery (.github/workflows/jekyll.yml) (Actions run 40609839451 green).

## Done (Oct 27, 2026, 6:34pm PT)

- Editor shift (UTC 01): events.yml/now.yml still current (OSA Con Nov 2,
  HackUMass Nov 15 upcoming; Cal Hacks past; `updated` is today PT);
  llms.txt in step; latest CI: 0 spelling, 0 HTML, 0 axe. Gmail search hit
  the quota error again — no registration check this run.
- Cross-link scan (project/paper names mentioned in a post without a link to
  their post): only gap was "HNSW" in the VaultMem diary post's feature list
  → now links /post/paper-tldr-hnsw/. Run 40616017831 green.
- Still dead (waiting on Avinash): rena-490107-f0f28.web.app and the daylog
  repo (404) — linked from /, /projects/, the Rena and Whisper posts.
- 2026-10-27 18:34 PT — EDITOR — HNSW in the VaultMem diary post links to the HNSW TL;DR (/post/vaultmem-your-ai-agent-shouldnt-read-your-diary/) (Actions run 40616017831 green).

## Done (Oct 27, 2026, 7:34pm PT)

- Designer shift (UTC 02): post footer "Keep reading" Older/Newer links are
  now a pair of bordered cards (`.read-next-pair` in style.css after
  `.read-next-more`; `_includes/read-next.html` now lists Older first with ←,
  Newer second with → in column 2, right-aligned). Stretched-link makes the
  whole card the tap target; focus ring moves to the card (`li:focus-within`);
  accent border on hover (hover-capable devices only); single column ≤34rem.
  No new fills, so contrast unchanged. Checked with local Playwright
  screenshots of a mock at 375px and 900px in sepia and dark. Run
  40621955875 green.

Designer backlog additions:
- [ ] If Avinash prefers the plain list, delete the `.read-next-pair` block in style.css (markup still reads fine unstyled)
- 2026-10-27 19:34 PT — DESIGNER — "Keep reading" older/newer links as a pair of clickable cards (_includes/read-next.html, assets/css/style.css; every /post/*) (Actions run 40621955875 green).

## Done (Oct 27, 2026, 8:35pm PT)

- Engineer shift (UTC 03): "Did you mean …?" on /search/. When a query has
  0 results, each term that matches nothing in the index is replaced by the
  closest word from a vocabulary built lazily from search.json (title/tag
  words weigh 20×, desc/body 1×; Damerau edit distance ≤1, ≤2 for 6+
  letters), offered only if the corrected query finds results. Visible as
  `#search-suggest` link (click sets the box and re-renders, URL `?q=`
  updates); screen readers hear it via a visually-hidden span in the
  status live region. CSS `.search-suggest` after `.search-status`. Tested
  on a Playwright mock with the real posts at 375px: hopfeild→hopfield,
  vaultmme→vaultmem, "embedings memory"→"embeddings memory",
  retreival→retrieval, nonsense → no suggestion; no JS errors. Run 40627746923 green.

Engineer backlog additions:
- [x] Search typo suggestion could also run on /blog/'s inline search (done Oct 27, 9:34pm PT)
- 2026-10-27 20:35 PT — ENGINEER — search suggests a corrected query ("Did you mean …?") when nothing matches (/search/) (Actions run 40627746923 green).

## Done (Oct 27, 2026, 9:34pm PT)

- Engineer shift (UTC 04): /blog/ inline search (blog.md script). Was a
  single-substring match on the whole query, so "agent memory" style
  multi-word queries only worked if the words were adjacent. Now every
  whitespace term must appear in title + excerpt + tags (tag hyphens as
  spaces), any order. Zero results → `#blog-suggest` "Did you mean …?"
  (vocab from data-title/data-tags ×20, data-excerpt ×1; same Damerau
  distance rule as /search/), offered only if it finds a post under the
  active topic chip; click fills the box, re-filters and updates `?q=`;
  screen readers get it in the #post-count status text. Playwright mock with
  the 17 real non-TL;DR posts: vaultmme→vaultmem, privcy→privacy, nonsense →
  none, no JS errors. Run 40633247463 green.

Engineer backlog additions:
- [x] Typo-suggest code (dist/vocab) is duplicated in search.md and blog.md (done Oct 27, 10:35pm PT — now _includes/typo-suggest.js)
- 2026-10-27 21:34 PT — ENGINEER — /blog/ search matches all words in any order and suggests a typo fix (blog.md; /blog/) (Actions run 40633247463 green).

## Done (Oct 27, 2026, 10:35pm PT)

- Editor shift (UTC 05) found nothing editorial: events.yml/now.yml current
  (OSA Con Nov 2, HackUMass Nov 15 still upcoming; Now `updated` already
  2026-10-27), codespell clean on posts/pages/data (only the deliberate
  "privcy" demo in changelog.yml), llms.txt page list matches real pages,
  paper/glossary cross-links already in place. External link check isn't
  possible from this sandbox (proxy rejects most hosts). → Engineer chore.
- Engineer: the "Did you mean …?" helpers now live once in
  `_includes/typo-suggest.js` (typoAdd, typoDist, typoClosest), inlined via
  `{% include %}` into the scripts in search.md and blog.md (no extra
  request). Behaviour unchanged; node --check on both rendered scripts and
  a unit run (hopfeild→hopfield, vaultmme→vaultmem, privcy→privacy,
  memroy→memory, nonsense→null). Invisible chore, no changelog entry.
  Run 40639044543 green.

Engineer backlog additions:
- [ ] Typo-suggest fixes go in _includes/typo-suggest.js (it's JS inside a Liquid include — keep `{{`/`{%` out of it)
- 2026-10-27 22:35 PT — EDITOR→ENGINEER — typo-suggest code shared between /search/ and /blog/ via _includes/typo-suggest.js (no visible change) (Actions run 40639044543 green).

## Done (Oct 27, 2026, 11:34pm PT)

- Editor shift (UTC 06) found nothing editorial again: events.yml/now.yml
  current (OSA Con Nov 2, HackUMass Nov 15 upcoming; Now `updated`
  2026-10-27 PT), no http:// links in posts/pages/data, cross-link backlog
  items already done, llms.txt in step (CI check). → Engineer chore.
- Engineer: CI "Spelling" step always showed 2 warnings for the deliberate
  `privcy` demo in changelog.yml. `.codespellrc` now has
  `ignore-regex = \?q=[^\s&)\]]+|\(try "[^)]*\)` — skips search-demo URLs
  and `(try "…")` hints only; a bare "privcy" elsewhere is still flagged
  (tested locally). Spelling is now at 0 warnings, which starts the
  "week at 0 warnings before --strict" clock for spelling (from Oct 28).
  Invisible chore, no changelog entry.

Engineer backlog additions:
- [ ] Changelog demo typos must sit inside `(try "…")` or a `?q=` link, or the spelling step flags them
- [ ] Still open from CI annotations: Rena demo + daylog repo 404 (waiting on Avinash)
- 2026-10-27 23:34 PT — EDITOR→ENGINEER — spelling CI ignores deliberate search-demo typos (.codespellrc; no visible change) (Actions run 40644916734 green).

## Done (Oct 28, 2026, 12:34am PT)

- Designer shift (UTC 07): post TOC (`details.post-toc`) summary drops the
  browser disclosure triangle (`list-style: none` + `::-webkit-details-marker`)
  for a CSS border chevron in currentColor (text-muted, ≥3:1 non-text in both
  themes) that points right when collapsed and rotates down when open
  (0.15s, off under prefers-reduced-motion); summary text darkens to --text
  on hover. Playwright mock with the real style.css at 375px, sepia + dark:
  no overflow. Run 40651229374 green.

Designer backlog additions:
- [ ] Any future `<details>` on pages could reuse the same chevron (selector is `.post-toc summary` only today)
- 2026-10-28 00:34 PT — DESIGNER — post "On this page" box gets a themed chevron that rotates when opened (assets/css/style.css; long /post/*) (Actions run 40651229374 green).

## Done (Oct 28, 2026, 1:35am PT)

- Engineer shift (UTC 08): CI browser check warned of CLS 0.088 at 1280px on
  /post/building-rena-ai-health-companion-gemini-live/. Cause: the post TOC
  was `<details hidden>` with an empty list; post-tools.html filled it, opened
  it (>=700px) and unhid it after first paint, pushing the post down. Now
  `_layouts/post.html` builds the list in Liquid (split content on
  `<h2 id="`; shown when >=1,200 words AND 3+ h2s), renders `open`, and a
  one-line inline script right after it closes it below 700px before paint.
  JS keeps only the current-section highlight. Works without JS too. All 10
  long posts have 4+ h2s, so back-to-top/resume (gated on `.post-toc`) still
  run everywhere they did. Liquid tested with python-liquid (headings with
  `<code>`/`&amp;`). Run 40658219790 green: layout-shift warning gone, 0 HTML
  errors, 0 axe.

Engineer backlog additions:
- [x] TOC Liquid handles h2s with extra attributes (done Oct 28, 12:35pm PT)
- 2026-10-28 01:35 PT — ENGINEER — post "On this page" box built server-side: no layout shift at load, works without JS (_layouts/post.html, _includes/post-tools.html; long /post/*) (Actions run 40658219790 green).

## Done (Oct 28, 2026, 2:34am PT)

- Engineer shift (UTC 09): each /events row (`_includes/event-row.html`) is
  now an h-event: `p-name` (event name), `dt-start` (the existing `<time>`),
  `dt-end` (hidden `<data>`, only when `end_date` is set), `p-location`, and
  `u-url` (hidden `<data>`, absolute /events/#slug anchor). No visual change
  (hidden elements drop out of the row grid). `scripts/check_mf2.py` now also
  checks /events/: one h-event per row, name/start/absolute url, end not
  before start. Tested with python-liquid + mf2py on a mock of all 14 rows:
  0 problems. Speculation rules also skip `/*.ics` (the calendar link was
  being prefetched on hover). Run 40665708644 green: 0 HTML errors, 0 axe,
  only the 2 known dead links.
- No Event JSON-LD on purpose: Google's event rich results are for organizers,
  and he doesn't organize these events.

Engineer backlog additions:
- [ ] If event rows ever get a recap AND an external event site, a `u-url` to the event's own site would be better than the anchor
- 2026-10-28 02:34 PT — ENGINEER — /events rows carry h-event microformats + CI mf2 check; .ics link no longer prefetched (_includes/event-row.html, scripts/check_mf2.py, _layouts/default.html; /events/) (Actions run 40665708644 green).

## Done (Oct 28, 2026, 3:35am PT)

- Editor shift (UTC 10): events/now checked — nothing expired (OSA Con Nov 2,
  HackUMass Nov 15 still upcoming; Cal Hacks already past). Attractor post's
  "Why This Matters" paragraph now links "context windows" to the glossary's
  #context-window entry. Wording unchanged. Run 40673431694 green.
- 2026-10-28 03:35 PT — EDITOR — Attractor post links "context windows" to the glossary (/post/attractor-memory-engine/) (Actions run 40673431694 green).

## Done (Oct 28, 2026, 4:35am PT)

- Editor shift (UTC 11): events/now checked — nothing expired (OSA Con Nov 2,
  HackUMass Nov 15 upcoming). Cross-link sweep (Whisper, daylog, Rena,
  VaultMem, ISTQB, Codex, Ollama): all already linked except VaultMem Part 1's
  "Sentence-transformers", which now links /post/paper-tldr-sentence-bert/
  (that TL;DR already names the `sentence-transformers` package and links
  back to VaultMem). Wording unchanged. Run 40681200368 green.
- 2026-10-28 04:35 PT — EDITOR — VaultMem Part 1 links sentence-transformers to the Sentence-BERT TL;DR (/post/vaultmem-encrypted-memory-for-ai-agents/) (Actions run 40681200368 green).

## Done (Oct 28, 2026, 5:41am PT)

- Designer shift (UTC 12): /series/ `ol.series-parts` is now a numbered
  reading path: list-style none + CSS counter, a 1.6rem circled number per
  part (accent-ink on --bg: 7:1 sepia, 7.6:1 dark; border currentColor) and a
  1.5px --border rule joining the circles (not after the last). `role="list"`
  added in series.md (Safari keeps list semantics); `content: counter() / ""`
  so screen readers don't hear the number twice. Playwright mock with the real
  style.css at 375 and 1000px, sepia + dark: no overflow, wrapped titles align.
  Live site wasn't reachable from the run's browser (tunnel error), so mocks only.
  Run 40690064615 green.

Designer backlog additions:
- [ ] Same stepper could suit `.series-box-list` inside posts if Avinash likes it (kept plain for now)
- 2026-10-28 05:41 PT — DESIGNER — /series/ parts shown as a numbered reading path (assets/css/style.css, series.md; /series/) (Actions run 40690064615 green).

## Done (Oct 28, 2026, 6:46am PT)

- Engineer shift (UTC 13): Rouge theme only styled 14 base classes (.c, .k,
  .s …), but Rouge emits Pygments' subtype classes — Python `# comments` are
  `.c1` (2nd most common token in the posts), imports `.kn`, True/None `.kc`,
  numbers `.mi/.mf`, classes `.nc`, decorators `.nd`, f-string parts
  `.sa/.si`, YAML/markdown headings `.gh/.gu` — so they rendered as plain
  text. Each colour rule in style.css now lists its whole family (comments,
  keywords, strings, names, variables) plus new numbers (#9a3412 light /
  #f2cc60 dark) and bold headings. Measured with pygments-tokenized copies of
  every fenced block in _posts on a Playwright mock with the real CSS: min
  token contrast 5.28 sepia, 5.15 light-gray, 5.62 dark; no overflow at
  375px. Run 40699985411 green, 0 axe / 0 HTML errors.
- The spelling step then flagged `.nd` (→ "and"); `.codespellrc`
  ignore-regex now also skips `\.highlight \.nd\b` (only that selector, so a
  real "nd" typo is still caught). Spelling's 0-warning clock restarts Oct 28.

Engineer backlog additions:
- [ ] New code languages in posts: tokenize with pygments (same class names as Rouge) and check each class has a rule
- 2026-10-28 06:46 PT — ENGINEER — code blocks colour comments, imports, numbers, classes, decorators (assets/css/style.css, .codespellrc; every /post/* with code) (Actions run 40699985411 green).

## Done (Oct 28, 2026, 7:37am PT)

- Engineer shift (UTC 14): offline bug + notice. Bug: a page saved offline
  links the `style.css?v=<hash>` of the day it was saved, but every deploy
  activates a new `static-<build>` cache and deletes the old one — so after
  any CSS change (several a day) saved pages rendered unstyled offline, and
  non-precached fonts were dropped too. sw.js: `handleStatic` now tries
  network, then `caches.match(req, {ignoreSearch: true})` (current
  stylesheet) when offline; fonts live in `fonts-v1`, which survives deploys.
  Notice: when a saved copy is served, sw.js `markSaved()` rewrites
  `<html lang="en"` → `<html lang="en" data-saved-copy="<Date header>">`;
  a script in default.html then prepends a `.saved-copy-note` (role=status)
  to <main>: "You're offline, so this is the copy saved on this device on
  <date>. Other saved pages" (→ /offline/); on `online` it becomes "You're
  back online. [Load the latest version]". Playwright mock (real CSS + sw.js)
  at 375px, sepia + dark: old ?v= entry deleted, offline reload → styled +
  note; contrast text 10.0/14.2, link/button 5.7/8.4; no overflow, no JS
  errors. Run 40708416909 green, 0 axe / 0 HTML errors.

Engineer backlog additions:
- [ ] sw.js `markSaved` relies on the literal `<html lang="en"` in default.html — keep them in step if the html tag ever changes
- [ ] Pages cached before Oct 28 7:37am PT have no notice script; they get it on the next online visit
- 2026-10-28 07:37 PT — ENGINEER — offline saved pages keep their styling after deploys and show a "saved copy" note (sw.js, _layouts/default.html, assets/css/style.css; every page offline) (Actions run 40708416909 green).

## Done (Oct 28, 2026, 8:36am PT)

- Editor shift (UTC 15): events.yml / now.yml checked — nothing expired (OSA
  Con Nov 2, HackUMass Nov 15; Cal Hacks already past); now.yml `updated`
  bumped to 2026-10-28. Cross-link: the "Six Papers" overview cited each paper
  but only linked one of the six deep-dive TL;DRs (via its footer). Each
  section's citation line now ends "· [Full TL;DR](/post/paper-tldr-…/)"
  (Hopfield 1982, Modern Hopfield, CLS, Sentence-BERT, LoCoMo, Memory as
  Asset). Links only, no wording/facts changed. External link sweep from the
  sandbox is useless (proxy returns 000/403 for nearly all hosts) — rely on
  CI's check_external.py annotations. Run 40717992055 green.
- 2026-10-28 08:36 PT — EDITOR — Six Papers overview links each paper section to its full Paper TL;DR (/post/paper-tldr-six-papers-on-memory/); now.yml re-verified (Actions run 40717992055 green).

## Done (Oct 28, 2026, 9:34am PT)

- Editor shift (UTC 16): events.yml / now.yml checked — nothing expired (OSA
  Con Nov 2, HackUMass Nov 15). Gmail (last 3 days): no new event
  registrations (SF Ruby Nov 10-11 mail is a promo, not a ticket). llms.txt
  page list matches real pages. Cross-link: VaultMem Part 1's three-tier
  benchmark table now links "MRR" to the glossary's #mrr (Part 2 already
  links Recall@10/MRR). Considered linking Sentence-BERT's inline "re-rank"
  but its footer already links #re-ranking, so left it. Run 40727486213 green.
- 2026-10-28 09:34 PT — EDITOR — VaultMem Part 1 benchmark table links MRR to the glossary (/post/vaultmem-encrypted-memory-for-ai-agents/) (Actions run 40727486213 green).

## Done (Oct 28, 2026, 10:34am PT)

- Designer shift (UTC 17): /events role pills (Hacker, Judge, Mentor, Speaker)
  all looked identical. Each now carries a 0.5em colored dot (`--role`):
  hacker = --cat-fun, judge = --cat-agents, mentor = --cat-tools, other roles
  = accent-ink. Label text unchanged (accent-ink, 5.1:1 sepia / 4.7:1 dark on
  the pill tint). Dot vs composited pill tint: sepia 4.1–5.1:1, dark
  4.0–5.1:1 (≥3:1 non-text). Playwright mock with real style.css at 375px,
  sepia + dark: no overflow; wrapped pill on long names OK. Jekyll can't be
  built in the sandbox (rubygems unreachable) and the live site is blocked by
  the proxy, so mock only. Run 40737282366 green.
- 2026-10-28 10:34 PT — DESIGNER — per-role colored dot on /events role tags (assets/css/style.css; /events/) (Actions run 40737282366 green).

## Done (Oct 28, 2026, 11:35am PT)

- Engineer shift (UTC 18): "Read a random post" on /blog/ (blog.md). A link
  in the lede (`#blog-random`, inside `#blog-random-wrap`, `hidden` until JS
  runs) picks a random post from the items currently showing, so it follows
  the topic chip / search box; sessionStorage (`blog-random-last`, try/catch)
  avoids the same post twice in a row. No-JS href is the newest post but the
  link stays hidden then. No class on the `<a>`, so it inherits the plain
  page-text link style. Playwright mock: with #web filter only matching posts
  picked, no repeats, no JS errors. Run 40746806494 green, 0 axe/HTML errors.

Engineer backlog additions:
- [ ] Same "random" link could sit on /paper-tldr/ if Avinash likes it (kept to /blog/ for now)
- 2026-10-28 11:35 PT — ENGINEER — "Read a random post" link on /blog/, respects topic/search filters (blog.md; /blog/) (Actions run 40746806494 green).

## Done (Oct 28, 2026, 12:35pm PT)

- Engineer shift (UTC 19): two backlog robustness fixes, no visible change.
  (1) Post TOC (`_layouts/post.html`) split content on `<h2 id="`, so a
  kramdown IAL heading (`<h2 class="x" id="slug">`) was skipped — and with
  only 3 h2s the whole box vanished. It now splits on `<h2`, reads the id
  from each tag wherever it sits, skips h2s without an id, builds the items
  in a capture and shows the box at 3+ items. python-liquid compare of old vs
  new over all 29 posts (python-markdown HTML): identical output; synthetic
  IAL/`<code>`/`&amp;`/no-id case correct. (2) Topic-feed threshold is one
  setting, `topic_feed_min: 2` in _config.yml, read by
  _plugins/topic_feeds.rb (default 2) and blog.md (`| default: 2`).
  Run 40756066815 green: 0 HTML errors, 0 axe, internal links OK. Invisible,
  so no changelog entry. (Pages artifact download is blocked by the proxy —
  blob.core.windows.net — so built HTML can't be inspected from the sandbox.)
- 2026-10-28 12:35 PT — ENGINEER — post TOC now lists headings with extra attributes; topic-feed threshold in one _config.yml setting (_layouts/post.html, _plugins/topic_feeds.rb, blog.md, _config.yml) (Actions run 40756066815 green).

## Done (Oct 28, 2026, 1:35pm PT)

- Editor slot (UTC 20) → Engineer: nothing editorial. events.yml / now.yml
  current (OSA Con Nov 2, HackUMass Nov 15; `updated` already 2026-10-28).
  Gmail last day: no registrations (AICamp AWS Loft Oct 29 mail is a promo
  reminder; OSA Con mail is the known AWS-registration nudge). CI annotations
  clean apart from the 2 known dead links (Rena demo, daylog repo). A
  pyspellchecker pass over posts/pages/data found no real typos (British
  spellings and deliberate changelog demo typos only). llms.txt in step.
- /events countdown: upcoming rows that haven't started get a muted
  `.event-countdown` after the name — "tomorrow" / "in N days" — from the
  visitor's local calendar date (same inline script in events.md that does
  "Happening now" and moves ended rows). No-JS: nothing shown. Playwright mock
  with real style.css at 375/1000px dark: OSA Con "in 5 days", HackUMass
  "in 18 days", today's event still "Happening now", no overflow, no JS errors.
  Run 40765103543 green.
- 2026-10-28 13:35 PT — EDITOR→ENGINEER — countdown ("in 5 days") on upcoming events (events.md, assets/css/style.css; /events/) (Actions run 40765103543 green).

## Done (Oct 28, 2026, 2:35pm PT)

- Editor shift (UTC 21): nothing needed, no site changes. events.yml/now.yml
  current (OSA Con Nov 2, HackUMass Nov 15; `updated` 2026-10-28). Gmail last
  day: no new registrations (only the known OSA Con AWS-registration nudge and
  AICamp promo). Doubled-word, a/an, its/it's and common-misspelling greps over
  posts/pages/data: clean. Glossary/TL;DR cross-links (HNSW, context window,
  Hopfield, LoCoMo) already in place. Latest CI annotations clean apart from the
  2 known dead links (Rena demo, daylog repo — waiting on Avinash).
- Fallbacks considered and skipped: `hyphens: auto` for phone prose (sandbox
  Chromium has no hyphenation dictionary, so it can't be verified — leave
  unless tested on a real phone); live-site Playwright audit (proxy blocks
  www.avinashgosavi.com and rubygems, so no local Jekyll build either).
- Backlog: dropped the "what I learned" project line (first-person content).
- 2026-10-28 14:35 PT — EDITOR — No changes (checks only; backlog tidy).

## Done (Oct 28, 2026, 3:35pm PT)

- Designer shift (UTC 22): in-post series boxes (_includes/series-box.html,
  top and bottom of every series post). Part numbers are muted like other post
  list markers; the current part's number is accent-ink and bold (5.7:1 sepia,
  8.4:1 dark on --surface) with `aria-current="step"` on its `<li>`; in the
  bottom box the following part gets a small "Next" pill (muted text, 5.5:1
  sepia / 6.6:1 dark; hidden in print). Last part: no tag. Liquid checked with
  python-liquid (sb_next reset per include), Playwright mock with real
  style.css at 375px sepia + dark: no overflow, no JS errors.
- Backlog: the numbered stepper idea for `.series-box-list` stays open (this
  is the lighter version — markers only).
- 2026-10-28 15:35 PT — DESIGNER — series boxes highlight the current part and tag the next one (_includes/series-box.html, assets/css/style.css; every series /post/*, e.g. /post/vaultmem-part-2-multimodal-temporal-backends/) (Actions run 40781340029 green).

## Done (Oct 28, 2026, 4:34pm PT)

- Engineer shift (UTC 23): ← / → keys on posts. `_includes/read-next.html`:
  the "Keep reading" Older/Newer links get `rel="prev"` / `rel="next"` and
  `aria-keyshortcuts="ArrowLeft"/"ArrowRight"`; an inline keydown handler
  follows them only when focus is on body (a focused code block, table, input
  or zoomable image keeps its arrows), no text is selected, no `<dialog open>`
  (image lightbox), no modifier key, not `defaultPrevented`. Screen readers in
  browse mode keep arrows for themselves. Playwright mock: ←/→ navigate;
  focused code / Shift / selection / open dialog → no navigation; no JS errors.
  Run 40788583572 green: 0 HTML errors, 0 axe, internal links OK.

Engineer backlog additions:
- [x] (done Oct 28, 5:34pm PT) Designer: a small `<kbd>←</kbd>`/`<kbd>→</kbd>` hint by the Older/Newer labels on fine-pointer screens (hidden on touch, print) would make the shortcut discoverable
- [ ] If Avinash dislikes the arrow-key shortcut, delete the `<script>` at the end of _includes/read-next.html (rel/aria-keyshortcuts can stay)
- 2026-10-28 16:34 PT — ENGINEER — ← / → keys open the older / newer post (_includes/read-next.html; every /post/*) (Actions run 40788583572 green).

## Done (Oct 28, 2026, 5:34pm PT)

- Editor shift (UTC 00) → Designer: nothing editorial. events.yml/now.yml
  current (OSA Con Nov 2, HackUMass Nov 15; `updated` 2026-10-28). Gmail last
  day: no new registrations (only the known OSA Con AWS-registration nudge).
- Took the backlog key-hint item: the existing ←/→ arrows by Older/Newer in
  _includes/read-next.html are now `<span class="read-next-arrow">` and, under
  `(hover: hover) and (pointer: fine)`, styled as key caps (same look as
  `.search-hint kbd`: --text on --surface, border). Touch screens keep plain
  arrows; .read-next is already hidden in print. Playwright mock at 1000px
  sepia + dark and 375px: no overflow. Run 40795105368 green.
- 2026-10-28 17:34 PT — EDITOR→DESIGNER — ←/→ by Older/Newer look like key caps on mouse/trackpad screens (_includes/read-next.html, assets/css/style.css; every /post/*) (Actions run 40795105368 green).

## Done (Oct 28, 2026, 6:34pm PT)

- Editor shift (UTC 01) → Engineer: nothing editorial. events.yml/now.yml
  current (OSA Con Nov 2, HackUMass Nov 15; `updated` 2026-10-28); Gmail last
  day: no new registrations (only the known OSA Con AWS-registration nudge);
  codespell 0 on posts/pages/data/includes/layouts.
- `html { scrollbar-gutter: stable; }` in style.css: on classic-scrollbar
  screens (Windows, Linux, macOS "always show") the header/column no longer
  slide sideways between short and long pages (or when the lightbox locks
  scroll). Gutter shows the body bg (propagated canvas). Playwright mock
  1000px sepia + dark: clientWidth 985 on both a 1-line and a 200-line page.
  Run 40801563597 green.
- Sandbox note: live site and Actions artifact blob downloads are blocked by
  the egress proxy (403) — test with local mocks only.

Engineer backlog additions:
- [ ] If a full-bleed element ever needs to reach the true right edge on short pages, note the reserved gutter (`100vw` includes it)
- 2026-10-28 18:34 PT — EDITOR→ENGINEER — scrollbar space reserved so pages don't shift sideways (assets/css/style.css; every page) (Actions run 40801563597 green).
