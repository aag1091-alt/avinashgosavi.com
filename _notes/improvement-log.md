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
- [ ] Old Attractor SVGs are hard-coded dark (#0f1117) — convert to theme-aware inline diagrams (~~context filtering~~ done Oct 21, 12:34am PT; ~~energy landscape~~ done Oct 21, 5:35am PT; ~~architecture~~ done Oct 21, 10:34am PT)

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
- [ ] Print: check a real diagram post prints well (SVG text uses tokens, should follow the light override); ~~post URL under the title~~ (done Oct 21, 6:34am PT)
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
- [ ] Project cards: long hyphenated names (whisper-live-transcribe) wrap at the hyphen at 375px — fine, but consider `hyphens: none` / slightly smaller name size on phones
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
- [ ] a11y lint: links built by JS (search results, TOC) aren't covered — a Playwright pass in a designer/engineer shift could check them
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
