Below is a precise platform reference for designing a full‑screen, tap‑driven, 20‑step pitch experience for iPad Pro 13‑inch (M4) running iPadOS 17, delivered in Safari or Chrome. Numbers are taken from Apple's iPad Pro 13" (M4) technical specifications, the Human Interface Guidelines (Designing for iPadOS, Layout), and standard WebKit/Safari behavior on iPadOS. Where Apple does not publish an exact number (notably display corner radius and the precise edge sizes of system gesture zones), I say so and give the practical working value designers use.

\---

\#\# SECTION 1 — SCREEN AND DISPLAY SPECIFICATIONS

\*\*1.1 Exact screen dimensions of iPad Pro 13‑inch (M4)\*\*

\- Diagonal: marketed as 13 inches when measured as a rectangle; the actual viewable area is slightly less because of the rounded corners (Apple's own footnote).  
\- Native pixels: \*\*2752 × 2064 px\*\* (portrait W × H is 2064 × 2752; landscape is 2752 × 2064).  
\- Logical points at @2x: \*\*1032 × 1376 pt\*\* portrait, \*\*1376 × 1032 pt\*\* landscape. (Apple's HIG layout table still lists the older 12.9" device as 1024 × 1366 pt; the M4 13" is marginally larger at 1032 × 1376 pt because the display grew slightly. Many UI frameworks and the Safari viewport still report the older 1024 × 1366 pt logical box when the page is at the default scale because of how UIKit reports screen bounds on this generation — see Section 8.) Treat \*\*1024 × 1366 pt\*\* as the safest CSS px design canvas in landscape (1366 × 1024\) and \*\*1032 × 1376 pt\*\* as the device's true logical resolution.  
\- Scale factor: 2.0× (UIKit scale).

\*\*1.2 Pixel density:\*\* 264 ppi.

\*\*1.3 Refresh rate (ProMotion):\*\* Adaptive \*\*10 Hz – 120 Hz\*\*. ProMotion is dynamic; the panel ramps refresh rate per frame in response to on‑screen motion. Static content can drop as low as 10 Hz to save power; finger/Pencil tracking and animations run up to 120 Hz. There is no "fixed 120 Hz" mode exposed to apps — the system decides.

\*\*1.4 Display technology:\*\* \*\*Ultra Retina XDR, tandem OLED\*\* (two stacked OLED panels driven together for sustained brightness). Important consequences vs. older LCD iPads and vs. iPhone OLED:  
\- True blacks (per‑pixel emissive). Use real \`\#000\` for cinematic, full‑bleed dark scenes; the bezel will appear to merge with the screen.  
\- 1000 nits SDR full‑screen, 1600 nits HDR peak, 2,000,000:1 contrast. Shadows, subtle gradients, and soft glows render with no halo or backlight bleed (unlike the 12.9" mini‑LED predecessor, which had visible blooming on bright UI over dark backgrounds).  
\- P3 wide gamut; design in \`display-p3\` if you want saturated reds/greens to pop beyond sRGB.  
\- True Tone shifts white point to ambient; if pixel accuracy matters, design against D65 and test with True Tone on and off.  
\- OLED is susceptible to long‑term burn‑in; for a 20‑step pitch that runs in retail kiosks, avoid leaving a static logo or progress indicator in the same pixel position for hours.

\*\*1.5 Display corner radius:\*\* Apple does \*\*not publish\*\* the corner radius for iPad Pro 13" (M4). The measured value of the display mask is approximately \*\*18 pt (≈ 36 px)\*\*. The previous 12.9" mini‑LED iPad Pro used a value commonly measured around 18 pt as well. Design rule of thumb: keep all critical content \*\*at least 16 pt inside every edge\*\*, and any rectangular interactive target \*\*at least 20 pt inside the corners\*\* so the rounded mask never clips it. If you use \`env(safe-area-inset-\*)\` in CSS, the browser already accounts for the corner radius along with the home indicator.

\---

\#\# SECTION 2 — SYSTEM UI ELEMENTS AND SCREEN REAL ESTATE

All values below assume iPadOS 17, full‑screen app (not Stage Manager).

\*\*Status bar\*\*  
\- Top edge, full width.  
\- Height: \*\*24 pt\*\* in portrait, \*\*24 pt\*\* in landscape on the 13" M4 (the Face ID iPad Pros use a uniform 24 pt status bar; older Touch ID iPads were 20 pt).  
\- Always visible in standard apps. A native app can hide it by setting \`prefersStatusBarHidden\`. In Safari/Chrome you cannot hide it from a normal browser tab; only a Home‑Screen‑installed PWA in standalone mode can effectively cover it (see Section 8).  
\- Safe-area inset top: 24 pt (Safari adds the browser's own chrome on top of that).

\*\*Home indicator (home bar)\*\*  
\- Bottom edge, centered horizontally, full width of the gesture zone.  
\- The visible pill is roughly 134 × 5 pt centered. The reserved bottom inset Apple recommends is \*\*20 pt\*\* (portrait) and \*\*21 pt\*\* (landscape).  
\- Always visible; can be auto‑hidden in native apps via \`prefersHomeIndicatorAutoHidden\`, in which case it dims after a short idle period but the gesture still works. Web apps cannot hide it.  
\- Creates a safe‑area inset at the bottom (\`env(safe-area-inset-bottom)\` ≈ 20–21 pt).  
\- A web app cannot overlap interactive controls with this zone reliably — taps near the bottom 20 pt can be intercepted by the system swipe.

\*\*Dock\*\*  
\- Bottom edge, centered, full width up to \~720 pt.  
\- Height when shown: \*\*80 pt\*\* plus a 20 pt bottom margin.  
\- Hidden by default in full‑screen apps; revealed by a short swipe up from the bottom edge (about 20 pt). A second longer swipe goes Home or to App Switcher.  
\- Does not create a permanent safe‑area inset. Web apps cannot prevent the reveal gesture.

\*\*Multitasking control (the three‑dot "···" pill)\*\*  
\- Top edge, centered horizontally.  
\- Width ≈ 60 pt, height ≈ 24 pt, appearing within the status bar area.  
\- Always available in iPadOS 17 in any app, including Safari. Tapping it opens Split View / Slide Over / Stage Manager controls. It does not create an inset, but you should not place a critical control directly behind it because tapping there will summon the system menu instead.

\*\*Menu bar:\*\* iPadOS does not have a persistent menu bar. With a physical keyboard attached, holding ⌘ surfaces an in‑app keyboard‑shortcut overlay; this is transient, not a persistent system element.

\*\*Stage Manager chrome (when active):\*\* window controls in the bottom‑right corner of the window (\~44 × 44 pt), a window title at the top, and a strip of recent apps along the left edge \~80 pt wide. See Section 3\.

\*\*Browser chrome (Safari):\*\* tab bar \+ URL bar at the top, roughly 52 pt when compact, up to \~92 pt when the Tab Bar is in "Separate" mode. Auto‑hides in fullscreen video and in Home‑Screen standalone apps. Bottom toolbar is not present on iPad Safari in landscape.

\*\*Browser chrome (Chrome iPadOS):\*\* top toolbar \~56 pt, no auto‑hide on scroll. Cannot be hidden except by add‑to‑Home‑Screen with \`display: standalone\` (Chrome on iPadOS uses WebKit under the hood, so behavior matches Safari).

\---

\#\# SECTION 3 — STAGE MANAGER

\*\*3.1 What it is.\*\* Stage Manager is iPadOS's windowed multitasking layer (introduced in iPadOS 16, stable in 17). It replaces full‑screen single‑app behavior with overlapping, resizable, repositionable windows; recently used apps appear as cards along the left edge.

\*\*3.2 Window behavior with Stage Manager on.\*\* Apps no longer fill the screen unless the user explicitly maximizes them. Each window can be dragged by its top bar, resized from the bottom‑right corner handle, and grouped with up to three other apps into a "stage." On iPad Pro 13" the user can place up to four windows on screen simultaneously, plus four more on an external display.

\*\*3.3 Effect on browsers.\*\* Safari and Chrome are ordinary apps under Stage Manager — they get their own windows, and the web viewport reports the \*\*window's\*\* size, not the screen's. \`window.innerWidth/innerHeight\` and CSS \`100vw/100vh\` shrink with the window. The viewport orientation can be effectively landscape even when the device is portrait (a tall, narrow window). The browser does not get any special treatment.

\*\*3.4 How to design for it.\*\* Do not assume full‑screen. Stage Manager is \*\*per‑user\*\* — your audience can have it on. Build the experience so it gracefully reflows to any window size, but commit to a \*\*primary cinematic target\*\* of full‑screen 1366 × 1024 pt landscape. Practical recipe:  
\- Lay out with \`100vw\` / \`100svh\` (small viewport units), never fixed pixel widths.  
\- Use \`dvh\`/\`dvw\` for content that should fill the live window as it resizes.  
\- Composition: place hero content centered, with at least 8% margin on all sides, so that at narrow window widths nothing critical is cropped.  
\- If the window becomes narrower than \~700 pt, switch to a "compact" stack rather than letting type and imagery scale below legibility.  
\- Detect with the \`resize\` event and CSS \`@media (min-width: …)\` / \`@container\` queries; do not rely on \`orientationchange\` alone, because the device orientation does not change when the window does.

\*\*3.5 Expected dimensions.\*\* Stage Manager windows on iPad Pro 13" can range from about \*\*320 × 320 pt\*\* (the documented minimum) up to the full \*\*1376 × 1032 pt\*\*. Common system "snap" sizes are halves (688 × 1032), thirds, and quadrants. Test at 1366 × 1024, 1024 × 768, 768 × 1024, 688 × 1032, 512 × 768, and 320 × 320\.

\---

\#\# SECTION 4 — INPUT METHODS

\*\*4.1 Touch (finger)\*\*

(a) Possible: tap, double‑tap, long‑press (\~0.5 s), pan, swipe (any direction, with velocity), pinch (two‑finger scale), rotate (two‑finger), and 3‑/4‑finger system gestures (pinch to home, swipe between apps).

(b) Native expectations:  
\- Tap feedback is immediate (\< 1 frame at 120 Hz, i.e. ≤ 8 ms perceived) — a target either highlights, scales subtly (98–96%), or transitions on \`touchstart\`/\`pointerdown\`, not on \`click\`.  
\- Tap target ≥ \*\*44 × 44 pt\*\* (Apple HIG minimum); on iPad Pro 13" use 56–64 pt for comfortable adult thumb taps.  
\- Long‑press reveals secondary actions (context menu) with a subtle scale \+ haptic.  
\- Inertia/rubber‑band scrolling at the edges; nothing "snaps" to a hard stop.  
\- Pinch/rotate are continuous, never quantized.

(c) Designer must:  
\- Bind to \`pointerdown\`/\`pointerup\` rather than \`click\` to eliminate the 300 ms tap delay (Safari on iPad has largely removed this, but pointer events still feel snappier).  
\- Treat the first 8 ms as your visual response budget — pre‑load the next slide's hero asset so the tap → transition is instant.  
\- Suppress double‑tap zoom: \`\<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no"\>\` (note iOS will still allow accessibility zoom).  
\- Use \`touch-action: manipulation;\` on tap targets to remove the residual 300 ms wait.  
\- Provide a \`:active\`/\`:focus-visible\` state, not only \`:hover\`.

\*\*4.2 Apple Pencil (2nd generation and Apple Pencil Pro)\*\*

(a) Possible: tap (very low‑latency point), drag, pressure (0–4096 levels), tilt (azimuth \+ altitude), double‑tap on the barrel (Pencil 2 \+ Pro), \*\*squeeze\*\* (Pencil Pro only), \*\*barrel roll\*\* (Pencil Pro only), \*\*haptic feedback\*\* (Pencil Pro only), and \*\*hover\*\* at up to \~12 mm above the display (both Pencil 2 and Pencil Pro on iPad Pro M4).

(b) Native expectations:  
\- Latency well under 9 ms with ProMotion; tap response is visually instantaneous.  
\- Hover preview: a faint circular indicator appears under the Pencil before contact; interactive elements should grow/glow/preview state.  
\- Squeeze (Pro): brings up a context tool palette; the system handles this.  
\- Double‑tap on barrel: app‑configurable, default is "switch to eraser" in drawing contexts.

(c) Designer must:  
\- Treat the Pencil as a precision pointer, not a finger. Targets can be smaller (24 pt is acceptable for Pencil‑only affordances), but never below 44 pt if touch is also allowed.  
\- Respond to \*\*hover\*\* before contact (see Section 5).  
\- Don't intercept squeeze; it's reserved for the system tool palette.  
\- For a non‑drawing pitch, treat Pencil identically to touch but with richer hover states.

Differences between Pencil 2 and Pencil Pro on M4: Pro adds squeeze, barrel‑roll (orientation around the long axis), and haptic feedback. Both support hover on M4. Web has access to hover, pressure, tilt, and pointerType==='pen' via the Pointer Events API; squeeze, barrel‑roll, and haptics are \*\*not\*\* exposed to the browser.

\*\*4.3 Magic Keyboard with trackpad\*\*

(a) Pointer movement (the system cursor morphs into a circle that "snaps" into buttons), left click, two‑finger right‑click, two‑finger scroll, pinch to zoom (on some surfaces), three‑finger swipes (home / app switcher / between apps), and the full keyboard.

(b) Native expectations:  
\- The cursor magnetically snaps onto controls. In native apps this is \`UIPointerInteraction\`; on web, Safari renders the same circular cursor but does NOT snap automatically.  
\- Right‑click opens a context menu.  
\- Tab / Shift‑Tab moves focus through interactive elements.  
\- ⌘‑\[ / ⌘‑\] navigates back/forward in browsers.  
\- Esc closes modals.  
\- Arrow keys often move within content (sliders, carousels).  
\- Space / Shift‑Space pages down/up in scrollable content.

(c) iPadOS 17 system shortcuts a full‑screen experience must respect or expect:  
\- ⌘‑Tab — app switcher  
\- ⌘‑Space — Spotlight  
\- ⌘‑H — Home (overrides any web \`keydown\` binding for ⌘‑H)  
\- Globe \+ ↑ — Control Center  
\- Globe \+ arrows — switch apps  
\- Globe \+ F — toggle full‑screen in supporting apps  
\- F11 in Safari with external keyboard — full‑screen  
\- ⌘‑R — reload page (browser)  
\- ⌘‑L — focus URL bar (browser)  
\- ⌘‑W / ⌘‑T — close / new tab (browser)  
\- Spacebar — page down (browser)  
\- Arrow keys — small scroll steps  
None of the system shortcuts (⌘‑Tab, ⌘‑H, Globe combos) can be intercepted by a web page; design around them.

You should explicitly bind: Space / → / Enter to advance, ← to go back, Esc to exit/close, digits 1–9 to jump to step.

\*\*4.4 External mouse or trackpad\*\*

(a) Same as Magic Keyboard trackpad but with a real scroll wheel (continuous), and right‑click as a hardware button. Some mice expose extra buttons; iPadOS lets the user remap them in Settings → General → Trackpad & Mouse.

(b) Native expectations are identical to the Magic Keyboard trackpad. The only behavioral difference is that the system cursor does not have the "magnet" effect when the input is a generic Bluetooth mouse — it stays as a precision arrow rather than the circle.

(c) Designer must handle \`wheel\` events for scroll/zoom if relevant. Right‑click (\`contextmenu\` event) should either be repurposed for a useful action or suppressed cleanly; never let the browser default context menu appear in a cinematic experience: \`oncontextmenu="return false"\`.

\*\*4.5 External keyboard, no trackpad\*\*

(a)/(b) Expectations: visible focus ring on the active element; Tab cycles through them in DOM order; Enter activates; Space activates buttons and pages down for scrolls; arrow keys move within composite widgets; Esc closes.

(c) For a 20‑step linear pitch:  
\- Bind Right Arrow / Down Arrow / Space / Enter / Page Down → next step.  
\- Bind Left Arrow / Up Arrow / Shift+Space / Page Up → previous step.  
\- Bind Home / End → first / last step.  
\- Bind 1–9 (and possibly 0 \+ digits) → jump to step.  
\- Bind ⌘‑F → "find" inside steps if relevant; otherwise let browser handle.  
\- Render a \`:focus-visible\` ring that matches the iPadOS visual language: a 3 pt outline at \`system-blue\` with 4 pt offset.

\---

\#\# SECTION 5 — APPLE PENCIL HOVER

\*\*5.1 What it is and at what distance.\*\* Apple Pencil hover is the iPad's ability to detect the Pencil tip's 2D position and altitude \*\*up to 12 mm above the screen surface\*\*. Detection begins as the tip enters that 12 mm zone. Available on iPad Pro M2 and later (including M4) with Apple Pencil 2nd generation or Apple Pencil Pro.

\*\*5.2 How it differs from touch.\*\* It is a separate event stream. In native code it surfaces through \`UIHoverGestureRecognizer\` and as \`UIEvent.ButtonMask\` "no contact" pointer events. In the web/browser it surfaces through the \*\*W3C Pointer Events API\*\* with \`pointerType: 'pen'\` and the \`pointerenter\` / \`pointerover\` / \`pointermove\` / \`pointerleave\` events firing \*\*before\*\* any \`pointerdown\`. The CSS \`@media (hover: hover)\` and \`:hover\` pseudo‑class also become true while the Pencil is in the hover zone.

\*\*5.3 Recommended visual response.\*\* Apple's guidance: provide a subtle, immediate, non‑committal preview as the Pencil approaches an interactive element. Practical patterns:  
\- A button lightly elevates (1–2 pt shadow grows) or scales 1.02–1.04× over 120–180 ms ease‑out.  
\- An icon control reveals its label.  
\- A list row tints to a 5–8% overlay.  
\- A draggable card lifts slightly.  
\- A canvas tool shows its brush preview at the cursor location.  
Avoid heavy state changes (full color shift, sound, haptics) on hover — those belong on tap.

\*\*5.4 Is it available in the browser?\*\* Yes. Safari on iPadOS exposes Pencil hover via Pointer Events as described. Chrome on iPadOS uses the same WebKit engine and behaves identically. There is no special permission required.

\*\*5.5 APIs.\*\*  
\- CSS: \`:hover\` and \`@media (hover: hover) and (pointer: fine)\`.  
\- JS: \`pointerenter\`, \`pointerover\`, \`pointermove\`, \`pointerleave\`, with \`event.pointerType \=== 'pen'\`. Read \`event.pressure\` (0 during hover, \> 0 on contact), \`event.tiltX\` / \`tiltY\`, and \`event.altitudeAngle\` / \`azimuthAngle\` (the latter two via the recently added Pointer Events Level 3 extensions in Safari).  
\- Use \`event.getCoalescedEvents()\` for high‑frequency Pencil sampling.  
\- There is no separate "hover‑distance" reading exposed to JS; you cannot read the millimeter altitude above the glass — only the X/Y position and tilt.

\---

\#\# SECTION 6 — PROMOTION AND 120 Hz

\*\*6.1 What ProMotion means in practice.\*\* A variable‑refresh‑rate display (10–120 Hz) that the system drives per frame. Animations rendered at 120 fps appear smoother, scrubbing and drags feel "stuck to the finger," and Pencil latency drops to single‑digit ms. The display can also drop to 10 Hz for power savings when nothing is moving — invisible to users, important for battery.

\*\*6.2 60 fps on a 120 Hz panel.\*\* It's noticeably less smooth than 120 fps for \*\*drags, scrubs, and finger‑tracked animations\*\*. On a static fade or short opacity transition, the difference is imperceptible. On a 1‑second translate or a continuous parallax under a finger, 60 fps shows visible "stepping." It is not jank in the broken sense, but next to a native iPadOS animation running at 120 the web version reads as "older" or "cheap." For a tap‑driven pitch, the most important moments to hit 120 fps are: (a) the tap acknowledgement (scale/opacity 100–250 ms), (b) the slide‑to‑slide transition (300–500 ms), and (c) any persistent ambient motion (background loops).

\*\*6.3 Does the browser get 120 Hz?\*\* Yes — Safari on iPadOS 15+ on a ProMotion device renders web content up to 120 Hz, \*\*but only for content driven by \`requestAnimationFrame\` and CSS animations/transitions running on the compositor (transform, opacity, filter)\*\*. Anything that triggers layout per frame will be capped well below 60 fps. Chrome on iPadOS uses WebKit and inherits the same 120 Hz capability. Caveats:  
\- Energy‑saver / Low Power Mode caps the browser to 60 Hz.  
\- Background tabs are throttled.  
\- If the device is thermally throttling, you may drop to 60 Hz mid‑experience.

\*\*6.4 Natural animation durations.\*\*  
\- Tap acknowledgement: 80–150 ms.  
\- Element scale on press: 80–120 ms.  
\- Slide transition between full‑screen scenes: 350–500 ms with a custom ease — at 120 Hz, 400 ms feels luxurious; the same duration at 60 Hz feels slightly sluggish, so don't shorten arbitrarily for 60\.  
\- Easing: prefer asymmetric curves like \`cubic-bezier(0.2, 0.8, 0.2, 1)\` (Apple's "default" interpolation) over linear. For physics‑based motion, spring with damping 0.7–0.85 and response 0.35–0.5 s.  
\- Do \*\*not\*\* shorten durations to 200 ms thinking "120 Hz means faster animations." 120 Hz makes the same duration look smoother, not faster. Keep durations the same; ProMotion fills them with twice the frames.

\*\*6.5 Where 120 Hz matters most.\*\*  
\- \*\*Finger‑tracked drags and scrubs\*\* — most noticeable.  
\- \*\*Scroll\*\* — Safari renders scroll on the compositor at 120 Hz; momentum scrolling on a long page is the canonical demo.  
\- \*\*Continuous transforms during a transition\*\* — slide‑in hero text, parallax background.  
\- \*\*Tap acknowledgement\*\* — small but felt; sub‑frame latency reads as "instant."  
\- Least noticeable: short fades, color cross‑fades, opacity‑only transitions.  
A user who has used iPadOS daily will perceive a 60 Hz drop during a drag almost immediately; static transitions, almost never.

\---

\#\# SECTION 7 — RESERVED SYSTEM GESTURES AND EDGE ZONES

Apple does not publish exact pixel widths for most of these. The values below are the practical, well‑measured working numbers.

\*\*7.1 Reserved gesture zones (iPadOS 17, iPad Pro 13"):\*\*

| Zone | Edge | Approx. depth | Direction | System action | Can a web app intercept? |  
|---|---|---|---|---|---|  
| Home indicator / Home gesture | Bottom | \~20 pt | Upward, short | Show Dock | No (system priority) |  
| Home gesture (long) | Bottom | \~20 pt | Upward, longer \+ lift | Go Home | No |  
| App switcher gesture | Bottom | \~20 pt | Upward, hold | App Switcher | No |  
| Notification Center | Top‑left | \~32 pt down | Downward | Notification Center | No |  
| Control Center | Top‑right | \~32 pt down | Downward | Control Center | No |  
| Slide Over / Split View invocation | Right edge | \~20 pt | Leftward swipe from edge | Reveal Slide Over | No |  
| Back‑swipe (in apps that support it; not system‑wide on iPad) | Left | \~16 pt | Rightward | Back navigation | Partly — \`touch-action: pan-x\` etc. helps |  
| Multitasking menu | Top center | 24 pt status bar \+ tap area | Tap on "···" | Multitasking | No |

For a swipe that originates \*\*inside\*\* the safe area (≥ 20 pt from any edge), the system does not steal it; your handlers receive the event normally.

\*\*7.2 Portrait vs landscape.\*\* The zones are the same in both orientations — they follow the physical edges, not screen content. The home indicator stays at the bottom of the current orientation.

\*\*7.3 Dock reveal vs in‑app swipe‑up.\*\* The Dock reveal zone is approximately the \*\*bottom 20 pt\*\* of the screen. To coexist with an in‑app swipe‑up gesture:  
\- Make your gesture begin from a point \*\*at least 24 pt above the bottom edge\*\*.  
\- Add \`touch-action: none\` only to elements that you fully own (not the body).  
\- Require a longer travel (\> 60 pt) or a tap‑then‑drag start so a casual short swipe from the edge still goes to the Dock.  
\- If your pitch is purely tap‑driven, you don't need to fight this at all — just don't put a tappable control closer than 20 pt to the bottom edge.

\*\*7.4 Left/right edge swipes.\*\* On iPad, the system reserves roughly the \*\*outermost 20 pt of each side\*\*. From the right edge, an inward swipe pulls Slide Over (a floating app window) into view. From the left edge, an inward swipe in some apps triggers Back; on the Home Screen it cycles screens. In a browser, the left edge swipe is consumed by Safari as "back" by default (interactive page swap). To make a left edge tappable in your experience:  
\- Treat the outer 20 pt as "warning" territory — display visuals there but place taps further in.  
\- Set \`overscroll-behavior-x: contain\` on the main container to reduce stray swipe forwarding.  
\- If you absolutely need an edge gesture there, document that users on iPad will need to start the gesture 24+ pt inside.

\---

\#\# SECTION 8 — WEB APP HOME SCREEN AND STANDALONE BEHAVIOR

\*\*8.1 Standalone mode UI.\*\* When the user adds your site to the Home Screen (Safari → Share → Add to Home Screen) and you have declared \`display: standalone\` (via web app manifest) or the legacy \`\<meta name="apple-mobile-web-app-capable" content="yes"\>\`, launching from the icon:  
\- Hides the browser address bar and tabs entirely.  
\- The status bar remains visible at the top (24 pt). You can style it with \`\<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"\>\` to draw your content beneath it.  
\- The home indicator remains visible at the bottom.  
\- The multitasking "···" pill at the top center is still present, but it auto‑hides briefly after launch.  
\- No back/forward, no reload, no URL bar.

\*\*8.2 Standalone viewport dimensions on iPad Pro 13" (M4):\*\*  
\- Landscape: \`window.innerWidth × window.innerHeight\` ≈ \*\*1366 × 1024 CSS px\*\* (this matches Apple's HIG "iPad Pro 12.9‑inch" entry; iPadOS treats the M4 13" as the same logical canvas for backward compatibility). Some test units report 1376 × 1032 on iPadOS 17.4+; design as if it could be either.  
\- Portrait: ≈ \*\*1024 × 1366 CSS px\*\* (or 1032 × 1376).  
\- Device pixel ratio: 2\.

\*\*8.3 Safe area insets in standalone.\*\* With \`\<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"\>\` and \`apple-mobile-web-app-status-bar-style=black-transluc  
