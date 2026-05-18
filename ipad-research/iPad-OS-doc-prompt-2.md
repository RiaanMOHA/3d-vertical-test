Continuing from where the previous response was cut off.

\---

\#\# SECTION 8.3 — Safe area insets in standalone mode on iPad Pro 13" (M4)

With \`\<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"\>\` and \`\<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"\>\`, the values reported by \`env(safe-area-inset-\*)\` are:

\*\*Landscape (1366 × 1024 CSS px viewport)\*\*  
\- \`env(safe-area-inset-top)\`: \*\*24 pt\*\* (status bar height; you draw beneath it but should keep critical content out of it).  
\- \`env(safe-area-inset-bottom)\`: \*\*21 pt\*\* (home indicator clearance).  
\- \`env(safe-area-inset-left)\`: \*\*0 pt\*\*.  
\- \`env(safe-area-inset-right)\`: \*\*0 pt\*\*.

\*\*Portrait (1024 × 1366 CSS px viewport)\*\*  
\- \`env(safe-area-inset-top)\`: \*\*24 pt\*\*.  
\- \`env(safe-area-inset-bottom)\`: \*\*20 pt\*\* (home indicator clearance, marginally smaller in portrait).  
\- \`env(safe-area-inset-left)\`: \*\*0 pt\*\*.  
\- \`env(safe-area-inset-right)\`: \*\*0 pt\*\*.

Notes that matter for the spec:  
\- iPad Pro 13" has no notch and no Dynamic Island; left/right insets are always 0 in standalone. (On iPhone Pro models they are non‑zero in landscape; do not copy iPhone defensive padding to iPad.)  
\- The display's rounded‑corner mask is approximately 18 pt radius. The 24 pt top and \~20 pt bottom insets already comfortably clear the rounded corners; no additional corner padding is necessary if you respect the safe area.  
\- If you set \`apple-mobile-web-app-status-bar-style="default"\` instead of \`black-translucent\`, the status bar reserves its own opaque 24 pt strip above your content and \`env(safe-area-inset-top)\` effectively becomes 0 (the OS gives you a viewport that starts under the bar). For a cinematic full‑bleed pitch, always use \`black-translucent\` so you can render edge‑to‑edge and the status bar floats over your art.  
\- These values are reported in CSS pixels, which on iPad equal logical points 1:1 at default zoom.  
\- Stage Manager changes nothing here for a maximized window. In a non‑maximized window the insets all collapse to 0 because the window is not against the device edges.

\#\# SECTION 8.4 — Standalone behavior in Safari vs Chrome on iPad Pro 13"

The headline answer: \*\*only Safari supports true "Add to Home Screen → standalone" on iPadOS.\*\* This is the single most important practical fact for your spec.

Specifics:  
\- \*\*Safari (iPadOS 17)\*\*: Share sheet → Add to Home Screen creates a home‑screen icon that launches the URL in standalone mode (no browser chrome). It honors \`apple-mobile-web-app-capable\`, \`apple-mobile-web-app-status-bar-style\`, \`apple-mobile-web-app-title\`, \`apple-touch-icon\`, and the \`display: standalone\` field in a Web App Manifest. Safe‑area insets behave as in 8.3.  
\- \*\*Chrome on iPadOS\*\*: Chrome on iPadOS is, by Apple's App Store rules, a WebKit wrapper — its rendering engine is identical to Safari. However, Chrome's "Add to Home Screen" entry on iPadOS produces a Home Screen icon that simply \*\*opens the URL in Chrome as a normal tab\*\*, with the Chrome top toolbar still visible. There is no standalone mode for Chrome on iPadOS; \`display: standalone\`, \`apple-mobile-web-app-capable\`, and \`status-bar-style\` have no effect when launched from a Chrome shortcut.  
\- \*\*Result for your spec\*\*: if a true cinematic full‑screen launch is required (no browser chrome, status bar overlaid, no URL bar ever), it must be Safari, added from Safari. Chrome users will always see Chrome's top toolbar (\~56 pt), and the viewport will be \~1366 × 968 in landscape (24 pt status \+ 56 pt toolbar consumed from the 1024 pt height in landscape Chrome is reduced differently; see 8.5).  
\- Other meta‑tag differences:  
  \- Both honor the standard viewport meta tag and \`viewport-fit=cover\`.  
  \- Both honor \`theme-color\`, but only Safari standalone uses it to tint the (translucent) status bar background; Chrome on iPadOS does not.  
  \- Both honor \`apple-touch-icon\` for the Home Screen icon image.  
  \- Neither supports \`display: fullscreen\` from the manifest in a launching sense; the only way to suppress browser chrome on iPadOS is Safari \+ \`display: standalone\` (or the legacy meta tag).

If a Chrome user must be supported with the same cinematic feel, your only option is to call \`element.requestFullscreen()\` after a user gesture. Safari and Chrome on iPad both implement the Fullscreen API in iPadOS 17\. That gives you edge‑to‑edge, hides the URL bar, but the status bar still shows and the user can exit at any time with a top‑edge swipe.

\#\# SECTION 8.5 — Viewport dimensions in a regular browser window on iPad Pro 13" (landscape)

\*\*Safari (regular, not standalone), landscape, full‑screen (not Stage Manager):\*\*  
\- With the URL/tab bar in its default "compact single bar" mode: viewport is \*\*1366 × 968 CSS px\*\*. The 56 pt browser top chrome reduces the 1024 pt height by 56 pt.  
\- With Safari's "Separate Tab Bar" preference enabled (Settings → Safari → Show Tab Bar): viewport drops to roughly \*\*1366 × 936 CSS px\*\*, because tabs and address bar render in two stacked rows totaling \~88 pt.  
\- Safari on iPadOS does \*\*not\*\* auto‑hide its top toolbar on scroll the way iPhone Safari does. The viewport is stable: it will not change while the user scrolls. The only way to "hide" it is the Fullscreen API or standalone mode.  
\- \`window.innerHeight\` and \`100vh\` therefore match \`100svh\` and \`100dvh\` (small and dynamic viewport units) almost exactly, because there is no dynamic browser chrome that contracts/expands during scroll.  
\- Status bar (24 pt) is still rendered above the browser; the browser already accounts for it, so the viewport you receive is below it.

\*\*Chrome (regular, not standalone), landscape, full‑screen:\*\*  
\- Top toolbar \~56 pt, viewport ≈ \*\*1366 × 968 CSS px\*\*, identical to Safari single‑bar mode in numbers.  
\- Chrome on iPadOS also does not auto‑hide its toolbar on scroll. Same stability as Safari.

\*\*Portrait equivalents:\*\*  
\- Safari single bar: \~\*\*1024 × 1310 CSS px\*\*.  
\- Safari separated tab bar: \~\*\*1024 × 1278 CSS px\*\*.  
\- Chrome: \~\*\*1024 × 1310 CSS px\*\*.

\*\*What changes when the address bar is "hidden":\*\*  
\- On iPad Safari there is no automatic hide on scroll, so this does not normally happen. The address bar only goes away when (a) the user enters Reader Mode, (b) you trigger Fullscreen API (viewport becomes the full \*\*1366 × 1024\*\*), or (c) Picture‑in‑Picture / video fullscreen takes over.  
\- In Fullscreen API mode, the viewport becomes the full device viewport (1366 × 1024 landscape, 1024 × 1366 portrait). The status bar may or may not be drawn over the top edge depending on iPadOS version; in iPadOS 17 it is hidden during programmatic fullscreen.  
\- If the user pulls down from the top to summon Control Center or notifications, the viewport size does not change.

\*\*Numerical summary for your spec\*\*

| Mode | Landscape viewport | Portrait viewport |  
|---|---|---|  
| Safari standalone, viewport‑fit=cover, black‑translucent | 1366 × 1024 (status bar overlaid) | 1024 × 1366 |  
| Safari normal, single bar | 1366 × 968 | 1024 × 1310 |  
| Safari normal, separate tab bar | 1366 × 936 | 1024 × 1278 |  
| Chrome normal | 1366 × 968 | 1024 × 1310 |  
| Fullscreen API (either browser) | 1366 × 1024 | 1024 × 1366 |  
| Stage Manager (maximized window) | up to 1366 × 1024 | up to 1024 × 1366 |  
| Stage Manager (minimum window) | 320 × 320 | 320 × 320 |

\---

\#\# SECTION 9 — PLATFORM FEEL AND NATIVE QUALITY SIGNALS

\#\#\# 9.1 Top characteristics that read as "native iPadOS, built for iPad Pro 13"

\*\*Touch latency and tap acknowledgement.\*\*  
\- Right: the moment a finger contacts a control, that control responds in the same frame — a 100 ms scale‑down to \~97%, an opacity nudge, or a subtle elevation. The transition to the next state begins on \`pointerdown\`, not on \`click\`. Visible response under 16 ms.  
\- Wrong: tap, then \~300 ms of nothing, then a hard state change. The user has time to lift the finger and wonder whether the tap registered. A button highlight that only appears on \`:hover\` and never on touch.

\*\*Animation curves.\*\*  
\- Right: motion uses asymmetric, decelerating curves — short acceleration, long settle. Apple's house ease is close to \`cubic-bezier(0.2, 0.8, 0.2, 1)\` for short interactions and spring physics for anything draggable. Things ease in, overshoot a touch on entry, settle.  
\- Wrong: linear timing, or symmetric \`ease-in-out\` for everything, or 200 ms hard cuts that look like CSS defaults.

\*\*Frame rate.\*\*  
\- Right: drags, scrubs, and transitions ride the display at 120 Hz; the visual feels glued to the finger or Pencil. Slide transitions between scenes are silky, not stepped.  
\- Wrong: visible "stair‑stepping" during drags, animations that jitter at the start because layout is being recalculated, frames dropping during the first run of an animation because assets weren't preloaded.

\*\*Type and spacing.\*\*  
\- Right: text is set in San Francisco (\`-apple-system\`, \`BlinkMacSystemFont\`, \`'SF Pro Display'\`) at iPadOS‑native sizes — body around 17 pt, large titles 28–34 pt, hero display 56–96 pt — with generous leading (1.3–1.45). Optical tracking tightens at larger sizes. Buttons have 44–56 pt height and pill‑shaped corners (continuous, not strictly circular — Apple uses \`border-radius\` with \`corner-smoothing\` style "squircles").  
\- Wrong: Helvetica or Arial fallback, body type at 14 px, dense lists that came straight from an iPhone layout, square buttons with hard 4 px corners, or worse, Material‑style outlined buttons.

\*\*Color and material.\*\*  
\- Right: deep, real blacks on OLED. Surfaces use translucent "vibrancy" effects (\`backdrop-filter: blur(...) saturate(180%)\`), with a 1 pt hairline border at \~12% white over translucent panels. P3 colors where used. True Tone–respecting (don't hardcode color spaces if the value isn't critical).  
\- Wrong: \`\#222\` as "black" (looks gray on OLED), flat opaque cards over flat backgrounds (looks like Android), pure sRGB candy colors that don't take advantage of the gamut.

\*\*Pointer and Pencil treatment.\*\*  
\- Right: hovering with a Pencil or trackpad pointer subtly previews the control before commitment. Targets glow lightly, lift, or expand a few percent. Cursor feels magnetic on important controls.  
\- Wrong: hover does nothing, or hover does the same thing as press, or \`:hover\` styles get stuck on tap on touch devices.

\*\*Safe areas and bleed.\*\*  
\- Right: artwork extends to all four hardware edges; system UI (status bar, home indicator) overlays gracefully; controls sit inside the safe area; nothing important is within 16 pt of a corner.  
\- Wrong: a white rectangle margin around the content; a button that gets cut by the rounded corner; or content jammed against the home indicator at the bottom.

\*\*Orientation and resize.\*\*  
\- Right: rotating the iPad reflows in under one frame; Split View / Slide Over / Stage Manager all produce a clean, smooth resize, never a reload.  
\- Wrong: rotating reloads the page; resizing turns text into overlapping blocks; in narrow widths the layout looks like the iPhone version stretched.

\*\*Sound and haptics.\*\*  
\- Right: short, restrained sounds at key moments (advance, success), often paired with a system‑sourced "tick" rather than a custom WAV. Haptics if you can get them (web cannot on iPadOS, but native‑sounding sound design fills the gap).  
\- Wrong: loud transition sounds on every tap; UI sounds in stereo that pan dramatically; no acknowledgement of any kind on important actions.

\#\#\# 9.2 Concrete symptoms that mark "mobile site blown up to tablet"

These are things a user will actually see and feel:

\- \*\*Buttons that are too small.\*\* 32 pt tall pill buttons that work on iPhone look like postage stamps at iPad Pro 13" viewing distance (\~24–28 inches). Users mis‑tap or lean in.  
\- \*\*Single‑column layouts that span the full 1366 pt width.\*\* A 1200 pt wide paragraph of 16 pt body type is unreadable; users notice they're sweeping their head left to right to read a single line.  
\- \*\*Tap targets clustered along the bottom edge.\*\* This is iPhone thumb‑zone thinking; on iPad the device is held two‑handed at the long edges, so important targets near the bottom center are awkward and conflict with the Dock gesture.  
\- \*\*A persistent bottom nav bar with five icons.\*\* Reads as iPhone immediately. iPad‑native experiences use a sidebar, a top tab bar, or no chrome at all.  
\- \*\*Pull‑to‑refresh.\*\* No native iPad experience uses it on the main canvas the way iPhone apps do; seeing it screams "phone site."  
\- \*\*Modal sheets that slide up from the bottom and cover the whole screen.\*\* On iPad these should be centered popovers or form sheets \~540–620 pt wide, leaving the background visible behind a dimmed overlay.  
\- \*\*300 ms tap delay.\*\* If a button feels "spongy" — press, wait, then state change — users perceive it as web, not native.  
\- \*\*Hover styles that get stuck.\*\* On a Magic Keyboard trackpad, hovering over a control should preview state; on touch, the same \`:hover\` style sticking after lift is the dead giveaway of a desktop site.  
\- \*\*Tiny system font that's clearly Helvetica or Arial.\*\* San Francisco has distinct shapes (the rounded "a", the open "G", the dotless "i" in some weights) that iPad users see in the OS constantly. Anything else reads as foreign.  
\- \*\*Bouncy, over‑animated transitions.\*\* Material's \`ease-in-out\` with bounce is recognizable as Android/web; iPadOS prefers calmer, decelerated motion.  
\- \*\*Page reloads on rotation.\*\* Native apps never do this.  
\- \*\*Scrollbars appearing in the corner.\*\* iPadOS scrollbars are translucent overlays that appear only during scroll and fade in \~500 ms. A persistent scrollbar is desktop‑Chrome behavior.  
\- \*\*Text selection handles on a tap‑only canvas.\*\* Hard‑to‑dismiss blue selection handles on a swiped headline make a cinematic pitch feel like a webpage. Set \`user-select: none\` on everything that isn't a quotation block.  
\- \*\*Native context menu on long‑press.\*\* A long‑press on an image showing "Open in New Tab / Add to Photos / Copy" tears the user out of the experience instantly. Use \`-webkit-touch-callout: none\` and prevent it.  
\- \*\*Zoom on double‑tap.\*\* If your viewport meta tag allows pinch‑zoom, double‑tap accidentally zooms a heading and shifts the layout. For a cinematic pitch, lock with \`user-scalable=no\` while preserving accessibility hooks (you can still respect prefers‑reduced‑motion and forced colors).  
\- \*\*Browser overscroll bounce that exposes a black or white band.\*\* Set \`overscroll-behavior: none\` and \`background-color\` on \`html\` and \`body\` to the experience's base color so any system‑level rubber‑band still looks intentional.  
\- \*\*Loading spinners that look like the iOS activity indicator on iPhone — gray dots in a circle.\*\* At iPad scale they look comically small and centered. Native experiences use full‑screen elegant load states or none at all.

\#\#\# 9.3 Signals that specifically read as "built for iPad Pro 13" in a cinematic, linear, chrome‑less experience

\- \*\*Full‑bleed compositions sized for 1366 × 1024.\*\* Hero typography in the 80–140 pt display range, photography that fills the canvas, generous negative space; the eye reads the whole frame at a glance because the iPad is held at chest distance.  
\- \*\*Tap zones that account for two‑handed holding.\*\* The most common iPad grip is both hands on the long edges with thumbs reaching \~120 pt inward. Place your "advance" affordance either centered (one tap anywhere advances) or in two zones — left for back, right for forward — within thumb reach but at least 24 pt off the edges.  
\- \*\*Single‑tap‑anywhere‑to‑advance as the primary interaction.\*\* Mirrors the feel of Keynote presentations on iPad and is the most iPad‑pro thing you can do. Layer a discoverability hint (a soft pulsing chevron or a one‑off onboarding) so users know to tap.  
\- \*\*120 Hz transitions between scenes.\*\* Each step transition should be transform/opacity‑based, 350–500 ms, with a decelerating ease. Pre‑load the next two steps so transitions never stutter.  
\- \*\*Pencil hover previews.\*\* If a Pencil is detected (\`pointerType==='pen'\`), reveal a slightly different state — a quiet glow under the tip, micro‑information on hover, a "preview" of the next slide as the Pencil approaches. This is the single most "Pro‑only" interaction available.  
\- \*\*OLED‑aware artwork.\*\* True black backgrounds where the device bezel disappears into the screen. Bright accents in P3 colors. Soft glows around hero elements that would have looked muddy on an LCD.  
\- \*\*Pro typography.\*\* SF Pro Display for headlines above 20 pt, SF Pro Text below, with \`font-variation-settings\` if you want optical sizes. Tracking tightened \~‑0.02 em at display sizes.  
\- \*\*Restrained, intentional sound.\*\* A single low‑volume "advance" sound, perhaps a soft cinematic whoosh under 100 ms, played at most on the first few advances and tied to the user's media volume.  
\- \*\*Refusal of every web‑page tell.\*\* No URL bar, no scrollbars, no selection, no callout, no overscroll, no zoom, no double‑tap to zoom, no native pinch.  
\- \*\*Orientation‑aware composition.\*\* A composition that has been clearly designed for the wide 4:3‑ish landscape canvas — not a portrait phone layout that was rotated.  
\- \*\*Built‑in respect for accessibility.\*\* Honors \`prefers-reduced-motion\` (replacing slides with cross‑fades), Dynamic Type up to at least 20% larger, increased contrast mode. These are quiet signals that the experience was built by someone who knows the platform.

\#\#\# 9.4 Quality bar — iPad Pro 13" (M4) vs standard iPad / iPhone

The Pro device is held by users who own it specifically because it is the best iPad. The expectation is uncompromised. Concretely:

\- \*\*Latency.\*\* On Pro: tap → visible response in one 120 Hz frame (≤ 8 ms). On standard iPad/iPhone: 60 Hz panel, ≤ 16 ms acceptable. Pro users notice 60 Hz drops within seconds.  
\- \*\*Animation smoothness.\*\* On Pro: every animation runs at 120 fps. A single frame drop during a transition is felt. On standard iPad: 60 fps target, occasional jank acceptable. The opposite of pro‑quality is animation that "almost" runs smoothly — you can see the seams.  
\- \*\*Rendering fidelity.\*\* On Pro: OLED tandem display reveals every artefact. Banding in gradients (8‑bit color), JPEG compression on hero photography, sub‑pixel font hinting issues — all visible. Use 16‑bit gradients where possible, lossless or high‑bitrate sources, and \`display-p3\` where the asset supports it.  
\- \*\*Pencil and trackpad.\*\* Pro users have Apple Pencil Pro and Magic Keyboard. Hover states, precise pointer affordances, and keyboard shortcuts are expected, not optional.  
\- \*\*Multi‑input fluency.\*\* Pro users routinely switch between Pencil, finger, trackpad, and external keyboard within a single session. The experience must be coherent across all four within one minute of use.  
\- \*\*Sound at speaker quality.\*\* The four‑speaker iPad Pro audio is far better than a standard iPad. Subtle audio cues that would be lost on a standard iPad become a quality signal here — mix at low SPL with real spatial separation if you use audio at all.

The opposite of pro‑quality: anything that betrays that you targeted "a tablet" generically — generic Material/Bootstrap UI, fonts that aren't San Francisco, animations on default \`ease\`, taps that wait for \`click\`, layouts that don't change between landscape and portrait, content that reads "from your CMS" rather than "composed for this screen."

In one sentence: pro‑quality means \*\*nothing about the experience reminds the user they are in a browser.\*\*

\#\#\# 9.5 iPadOS multitasking and a full‑screen web experience

\*\*What can happen while the user is in your experience:\*\*

1\. \*\*Split View (legacy, still present in iPadOS 17 alongside Stage Manager).\*\* The user swipes up to reveal the Dock and drags an app icon to the left or right edge. The screen splits 50/50, 30/70, or 70/30. Your browser/standalone shrinks to one half; the other app fills the other half. There is a 11 pt vertical divider between the two.  
2\. \*\*Slide Over.\*\* The user drags an app to the very edge; it becomes a floating \~375 pt wide phone‑shaped window over your content. Your viewport doesn't change in this case — your content keeps its full size, with a floating window overlaid. Taps under the floating window are blocked.  
3\. \*\*Stage Manager.\*\* Your window becomes a free‑floating, resizable rectangle. The user can drag any corner to resize between roughly 320 × 320 pt and the full 1366 × 1024 pt.  
4\. \*\*External display via Stage Manager.\*\* The user can drag your window to an external 6K display; the viewport changes to whatever that display reports.  
5\. \*\*Picture‑in‑Picture.\*\* If your experience uses HTML5 video and the user invokes PiP, a small video tile floats and the rest of your page remains.  
6\. \*\*Notification banner / Dynamic Island‑style top alert.\*\* Briefly covers the top \~80 pt; viewport unchanged.

\*\*What happens to the web viewport in each case:\*\*

\- \*\*Split View 50/50 (landscape):\*\* viewport becomes \*\*678 × 1024 CSS px\*\* (a hair under half because of the divider). \`resize\` and \`orientationchange\` may or may not fire; rely on \`resize\`. Browser chrome height stays the same, so usable content area in Safari is \~678 × 968\.  
\- \*\*Split View 30% pane:\*\* viewport ≈ \*\*320 × 1024\*\* in landscape. Very narrow; layout must degrade gracefully.  
\- \*\*Split View 70% pane:\*\* viewport ≈ \*\*1024 × 1024\*\*.  
\- \*\*Slide Over over your app:\*\* your viewport does not change (\~1366 × 1024). The other app floats above as an opaque rectangle of \~375 × 768 you cannot detect via web APIs.  
\- \*\*Stage Manager window:\*\* any size between \*\*320 × 320\*\* and full screen, in any aspect ratio. Reported by \`window.innerWidth/innerHeight\` and \`100vw/100vh\`. Resize events fire continuously as the user drags the handle.  
\- \*\*Rotation while in any of the above modes:\*\* triggers a \`resize\` and \`orientationchange\`; layout must reflow without reload.

\*\*How a well‑designed experience should respond:\*\*

\- \*\*Detect, don't refuse.\*\* Never tell the user "please rotate" or "please maximize." Adapt.  
\- \*\*Layout in three tiers:\*\*  
  \- \*\*Cinematic\*\* (≥ 900 pt wide): full hero typography, edge‑to‑edge imagery, the experience as intended.  
  \- \*\*Compact\*\* (480 – 900 pt): hero scales down, secondary elements stack, but tap zones and pacing are preserved.  
  \- \*\*Minimum\*\* (320 – 480 pt): a respectful fallback — perhaps a single‑column "compressed" version of the current step, or a polite card that says "Open full‑screen for the full experience" with a button that calls \`requestFullscreen()\`. Never let the layout shatter.  
\- \*\*Use \`dvw\`/\`dvh\` and \`svh\` viewport units\*\*, not \`vh\`, so units track the live window.  
\- \*\*Use container queries\*\* (\`@container\`) on the main wrapper rather than only \`@media\` queries, because in Stage Manager media queries reflect the window not the device.  
\- \*\*Throttle resize handling\*\* to one paint frame (\`requestAnimationFrame\`) so dragging the resize handle does not janks.  
\- \*\*Preserve state across resize.\*\* The current step, scroll position within a step, and any user input must survive without flicker. Specifically, do not destroy and recreate the canvas/scene on resize — recompose it.  
\- \*\*Re‑measure typography.\*\* If you use fluid type (\`clamp()\` with \`vw\` units), ensure the floor is large enough at 320 pt width to remain legible (≥ 17 pt body).  
\- \*\*Pause expensive ambient animation\*\* when the window is below a chosen threshold (e.g. \< 600 pt wide) or when \`document.visibilityState \=== 'hidden'\`. Users often shrink your window precisely because they want to multitask; chewing CPU there is rude and drains battery.  
\- \*\*Recover gracefully from Fullscreen exit.\*\* If you used \`requestFullscreen\` and the user gestures out, your page will re‑receive a \`fullscreenchange\` event with a non‑fullscreen state. Show a discreet "Resume full screen" affordance instead of jumping back automatically.  
\- \*\*Treat Slide Over as invisible.\*\* You can't detect the floating window, so design so that any region of the screen could be partially occluded at any moment — meaning no critical control sits in a single small zone the user cannot tap around. This is also why a tap‑anywhere‑to‑advance pattern is robust on iPad: even with Slide Over obscuring a corner, most of the canvas is still tappable.

That completes Sections 8.3 through 8.5 and Section 9\. If you'd like, I can package this and the earlier sections into a single design‑spec document with the numbers consolidated into reference tables.  
