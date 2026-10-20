---
layout: post
date: 2026-10-20 04:50:00 -0700
title: "How VideoOnly Browser Shows Just the Video"
permalink: /post/videoonly-browser-how-it-works/
description: "A walkthrough of VideoOnly Browser, a small Electron app: how it denies popups, stops off-site redirects, blocks downloads and permission prompts, and hides everything but the player with one CSS rule."
tags: ["Privacy", "Explainers", "Web"]
image: /assets/og/videoonly-browser-how-it-works.png
---

[VideoOnly Browser](https://github.com/aag1091-alt/videoonly-browser) is one of my side projects: a small desktop browser (Electron, so Chromium underneath) for watching a video on a page without the rest of the page getting in the way. It runs on Windows, macOS and Linux.

This post walks through how it works, using only the [README](https://github.com/aag1091-alt/videoonly-browser#readme) and the source in that repo.

## The idea in one paragraph

Pages that host video often fight the viewer: popups, popunders, surprise redirects to another site, drive-by downloads, "allow notifications?" prompts and "are you sure you want to leave?" traps. VideoOnly Browser says no to all of those at the browser level, then, once a video starts playing, hides everything on the page except the player.

## Saying no, one event at a time

Most of the blocking lives in `main.js`, the Electron main process, and each kind of annoyance maps to one Electron hook.

**Popups.** Every `window.open`, `target="_blank"` link and popunder goes through `setWindowOpenHandler`, which always answers `deny` and logs what it blocked. As a second layer, every web contents the app ever creates gets the same deny handler, so nothing can open a second window.

**Redirects.** The `will-navigate` and `will-redirect` events run through a small guard. A navigation is allowed if *you* started it (typed an address or clicked through the toolbar), or if it stays on the same site, compared by base domain. Anything else is cancelled and shows up in the toolbar with an "Open here" button, in case you did want it. The guard also refuses any scheme other than `http`, `https`, `file`, `about`, `blob` and `data`, so a page can't hand you off to an external app through a custom protocol link.

**Leave-page traps.** `will-prevent-unload` is cancelled, so "are you sure you want to leave?" never gets in the way. `alert`, `confirm` and `prompt` boxes are suppressed too.

**Downloads and permissions.** The session's `will-download` event is always cancelled (there's deliberately no toggle), and both the permission request and permission check handlers answer `false`, so notifications, camera, location and similar requests are denied without a prompt.

**Ads and trackers.** Request-level blocking uses Ghostery's ad-block engine with the EasyList and EasyPrivacy lists, cached locally after the first run. A shield in the toolbar counts blocked popups, redirects, downloads and ad requests, and lets you open any of them on purpose.

## Finding the video

A preload script, `content-preload.js`, runs in every frame of the page in an *isolated world*: the page's own JavaScript can't see or tamper with it. It reports to the main process when a video starts playing.

Small videos don't count. Anything under 300 × 150 pixels is ignored for automatic mode, which skips thumbnails and sidebar ads. When several frames have candidates, the main process scores each one by its on-screen area, and a playing video scores three times a paused one. So a big playing player wins over a small autoplaying ad.

If you switch video-only off by hand, it stays off for that page unless a clearly bigger video starts later (at least 1.3× the area). That keeps the app from fighting you.

## Hiding everything else with one CSS rule

Once the preload script has picked a target (the video, its player container, or the iframe that holds the player) it marks:

- the target with a `data-vo-target` attribute, and
- every ancestor up to the root with `data-vo-keep`.

Then it injects a single stylesheet. The key rule hides *every child of a kept ancestor that isn't itself kept or the target*:

```css
[data-vo-keep] > :not([data-vo-keep]):not([data-vo-target]) {
  display: none !important;
}
```

The target itself becomes `position: fixed` and fills the viewport. Because this is a CSS rule rather than a one-time sweep of the page, overlays the site injects *later* are hidden too: they land as siblings of something on the kept chain and match the selector automatically.

Players inside cross-origin iframes work the same way, one frame at a time: the main process walks up from the frame that holds the video through each parent frame and isolates the iframe element in each, so nested embeds end up filling the window.

There are two styles. *Player*, the default, keeps the site's own controls, quality menu and subtitle layer. *Bare video* shows just the `<video>` element with Chromium's native controls.

## Small extras

Picture-in-picture and playback speed work on whatever video you're watching, with keyboard shortcuts for both, and `Ctrl+Shift+V` (`⇧⌘V` on a Mac) toggles video-only by hand if a page's video isn't detected. The address bar takes either a URL or words to search DuckDuckGo.

Both the toolbar and the page view run with `contextIsolation` and `sandbox` on and Node integration off, which is Electron's recommended setup for loading untrusted pages.

## How it's tested and shipped

The repo has an end-to-end test, `test/e2e.js`, that launches the browser with Playwright against a deliberately hostile local page and checks that popups, redirects and downloads are blocked and that video-only isolation works across a cross-origin iframe. The same checks can run against a packaged build.

Every push to `main` runs a GitHub Actions workflow that builds installers on Windows, macOS and Linux runners and uploads them to the GitHub release for the version in `package.json`.

## Honest limits

- **No DRM.** Sites that use Widevine won't play, because plain Electron has no DRM module. Ordinary HLS, DASH and MP4 players work.
- **Downloads are always blocked.** That's by design, so it's the wrong tool for a site where you *want* to download something.
- **Unsigned on Windows.** The Windows installer is unsigned, so SmartScreen may warn on first run. Mac builds are only signed and notarized when the release workflow has Apple credentials; otherwise they're ad-hoc signed and need "Open Anyway" the first time.
- **Same-site is a heuristic.** Redirects are compared by base domain, so a hop to another page on the same site is allowed.

## Try it

Installers are on the [Releases page](https://github.com/aag1091-alt/videoonly-browser/releases/latest), and `npm install && npm start` runs it from source. It's MIT licensed.

---

*More from the same shelf:* [How Drafting Desk keeps your drafts in your browser](/post/drafting-desk-how-it-keeps-drafts-private/), another small privacy-minded tool, and the [rest of my projects](/projects/#videoonly-browser).
