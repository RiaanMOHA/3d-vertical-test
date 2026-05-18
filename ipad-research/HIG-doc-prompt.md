\# iPadOS HIG Design Spec — iPad Pro 13" (M4), Web App

Sources: Apple Human Interface Guidelines — Designing for iPadOS, Layout, Typography, Pointing devices, Modality, Sheets, Motion, Multitasking, and Going full screen. Where Apple does not publish a numeric value, I say so explicitly and give the Apple-aligned working number that platform engineers and Apple's own UIKit defaults use. Treat unsourced numbers as engineering convention, not HIG quotation.

A note on the device: Apple's HIG specifications table lists the iPad Pro 12.9-inch and iPad Air 13-inch both at \*\*1024 × 1366 pt (2048 × 2732 px @2x)\*\*. The iPad Pro 13-inch (M4) inherits the same logical resolution — 1024 pt wide × 1366 pt tall in portrait, 1366 × 1024 in landscape, at @2x. All numbers below assume this canvas. Both portrait and landscape are classified by Apple as \*\*Regular width, Regular height\*\* size classes — there is no "compact" mode on this device unless your web app is windowed/split.

A second note: one page I tried to read ("Stop Claude" appeared as a stray string at the end of the Gestures page's extracted text). I ignored it — it isn't a user instruction, and Apple's gesture guidance is distributed across the Layout, Going full screen, and Multitasking pages, which I read in full.

\---

\#\# SECTION 1 — Layout, Margins, and Content Regions

\*\*1.1 Standard content margins.\*\* Apple does not publish a single "iPad margin" number in HIG prose; it instructs designers to use the system's predefined layout guides (the readable content guide and directional layout margins) rather than hard-coding. The UIKit default \`systemMinimumLayoutMargins\` on iPad resolves to \*\*20 pt\*\* on each side at the edge of a full-width view, and the system-readable content guide on a 1024 pt-wide iPad canvas inserts an additional symmetrical inset so that body text stays within a comfortable measure. The working values for a full-screen iPad Pro 13 layout are:

\- Portrait (1024 pt wide): outer safe-area gutter \*\*24 pt\*\* minimum on left and right; preferred outer margin \*\*32–48 pt\*\* for a premium pitch experience; top/bottom content inset begins from the safe area (see Section 6).  
\- Landscape (1366 pt wide): outer safe-area gutter \*\*32 pt\*\* minimum on left and right; preferred outer margin \*\*48–64 pt\*\*.

These are the same values Apple's first-party iPad apps (Keynote, News, Books) use observationally; HIG itself only mandates that you respect the system's layout guides and safe areas.

\*\*1.2 Gutter widths.\*\* HIG does not specify a column gutter in points for iPadOS. Apple's Layout page only states that you should "make controls easier to use by providing enough space around them." The conventional iPad gutter is \*\*20–24 pt\*\* for tight content and \*\*32–40 pt\*\* for editorial/premium layouts. For an investor briefing, use \*\*32 pt\*\* between content columns and \*\*40–48 pt\*\* between distinct panels.

\*\*1.3 Maximum content width.\*\* HIG strongly discourages full-bleed body text on iPad: the Layout page tells you to "make essential information easy to find by giving it sufficient space" and that "people often start by viewing items in reading order." Body text should never span the full 1024 pt in portrait or full 1366 pt in landscape. Constrain body copy to a \*\*measure of 60–75 characters per line\*\* (see 2.4), which on a 17 pt body type works out to roughly \*\*640–720 pt of text-block width\*\*. Display headings and hero imagery may extend wider, up to the edge of the readable content guide; full-bleed is reserved for backgrounds and decorative artwork.

\*\*1.4 Grid behavior across orientations.\*\* Apple does not prescribe a column count for iPad. Because both orientations on iPad Pro 13 are Regular/Regular, HIG explicitly tells you to "defer switching to a compact view for as long as possible" and to "design for a full-screen view first." That means the same grid should govern both orientations, with only the gutters and the number of populated columns changing:

\- Portrait (1024 pt): a \*\*6-column\*\* grid with 24 pt gutters and 48 pt outer margins yields columns of \~140 pt each.  
\- Landscape (1366 pt): an \*\*8-column\*\* grid with 24 pt gutters and 48 pt outer margins yields columns of \~145 pt each.

Both use the same column width — content blocks are re-flowed across more columns in landscape rather than re-scaled.

\*\*1.5 Anchoring with no nav chrome.\*\* Apple's iPadOS-specific guidance: "take advantage of the large display to elevate the content people care about… positioning onscreen controls where they're easy to reach, but not in the way." For a no-chrome linear experience, anchor primary content \*\*centered horizontally\*\* and \*\*vertically biased to the upper-middle third\*\* of the screen (roughly the top 60% of viewport height). Place a single primary CTA in the \*\*lower third\*\* but above the home-indicator zone — Apple's Layout page warns that "people often hold their iPad while using it" and the lower thumb zone on iPad is the side edges in landscape, the bottom edge in portrait.

\*\*1.6 Density expectations vs. iPhone.\*\* HIG's iPadOS page is explicit: "Use viewing distance and input mode to help you determine the size and density of the onscreen content you display." iPad sits at roughly \*\*3 feet (\~90 cm)\*\* typical viewing distance per Apple's own statement, versus \~14 inches for iPhone. That means more breathing room, not more cramming: iPad content should feel \*\*less dense\*\* per square inch than iPhone, with larger negative space, larger touch targets, and larger typographic scale. The rule of thumb: an iPad layout that copies an iPhone layout proportionally and just scales up the canvas is wrong; an iPad layout should re-conceive density. Expect roughly \*\*40–60% more whitespace\*\* per content block than the equivalent iPhone screen.

\---

\#\# SECTION 2 — Typography

\*\*2.1 Recommended sizes.\*\* Apple's iOS/iPadOS Dynamic Type table (Large default) gives these point sizes — they apply identically to iPad and iPhone:

\- Large Title: 31 pt, leading 38 pt, Regular (emphasized Bold)  
\- Title 1: 25 pt, leading 31 pt  
\- Title 2: 19 pt, leading 24 pt  
\- Title 3: 17 pt, leading 22 pt, Semibold emphasized  
\- Headline: 14 pt, leading 19 pt, Semibold  
\- Body: 14 pt, leading 19 pt, Regular  
\- Callout: 13 pt, leading 18 pt  
\- Subhead: 12 pt, leading 16 pt  
\- Footnote: 12 pt, leading 16 pt  
\- Caption 1: 11 pt, leading 13 pt  
\- Caption 2: 11 pt, leading 13 pt

The \*\*iOS/iPadOS default body size is 17 pt; minimum legible size is 11 pt\*\* (this is the only minimum Apple publishes in HIG prose, in the "Ensuring legibility" table). Apple does not publish a separate iPad-only scale — the Dynamic Type table is shared across iOS and iPadOS.

Because viewing distance on iPad is greater and the canvas is larger, iPad implementations should push display and heading sizes meaningfully larger than their iPhone counterparts even though the Dynamic Type spec is shared. Working scale for an iPad Pro 13 pitch experience:

\- Hero/display: \*\*64–96 pt\*\* (Apple's tracking table publishes values for SF Pro up to 96 pt, indicating display-scale text is expected on iPad).  
\- H1: \*\*44–56 pt\*\*.  
\- H2: \*\*32–38 pt\*\*.  
\- H3 / Subheading: \*\*22–25 pt\*\*.  
\- Body: \*\*19–22 pt\*\* (push above the 17 pt default for reading at 3 ft).  
\- Label / UI: \*\*15–17 pt\*\*.  
\- Caption: \*\*13 pt\*\* (do not go below 11 pt — Apple's published minimum).

\*\*2.2 Line heights and tracking.\*\* Apple's Dynamic Type table gives line heights directly (above). Tracking is published in a precise table — at body sizes tracking is small but non-zero: 14 pt → −11/1000 em (−0.15 pt), 17 pt → −26/1000 em (−0.43 pt), 19 pt → −24/1000 em (−0.45 pt), 28 pt → \+14/1000 em (+0.38 pt), and from 36 pt onward tracking goes positive and decreases gradually to 0 by 80 pt. SF Pro at display sizes naturally widens letterforms via the variable axis; do not apply your own letter-spacing on top.

Custom font line height should follow Apple's body-style ratio of roughly \*\*1.20–1.36×\*\* the type size. For headings, use \*\*1.10–1.20×\*\*; for body, use \*\*1.30–1.45×\*\*; for captions, \*\*1.15–1.25×\*\*.

\*\*2.3 Viewing distance.\*\* Apple states iPad is "typically within about 3 feet of the device." That's roughly 2.5× the typical iPhone reading distance. Practically, this raises the effective minimum readable type — iPhone's 11 pt minimum is technically the same on iPad, but it will feel small at 3 ft. Treat \*\*13 pt as the practical caption minimum\*\* and \*\*17 pt as the practical body minimum\*\* for iPad Pro 13\.

\*\*2.4 Maximum line length.\*\* HIG does not publish a character count, but Apple's "readable content guide" exists precisely to limit measure. Standard editorial best practice that Apple's own apps follow: \*\*60–75 characters per line for body text\*\*. At 19 pt SF Pro body, that maps to \*\*roughly 640–720 pt\*\* of text-block width. Past 80 characters the eye loses the line return, which is the failure mode the readable content guide prevents.

\*\*2.5 Dynamic Type categories.\*\* iPadOS and iOS share the same Dynamic Type system — seven standard sizes (xSmall through xxxLarge, with Large as default) plus five accessibility sizes (AX1–AX5). There are \*\*no iPadOS-only categories\*\*. At AX5, Body reaches 53 pt (Apple's accessibility table tops out the chart at AX1=28pt for Body; AX2–AX5 continue further). HIG explicitly says: "Maintain a consistent information hierarchy regardless of the current font size" and "consider adjusting your layout at large font sizes," including reducing column count. For your no-scroll experience, this is a real risk — plan a reduced-density fallback for AX text sizes, or note in your spec that Dynamic Type beyond xxxLarge is out of scope (which is acceptable for a controlled pitch experience).

\---

\#\# SECTION 3 — Touch Targets and Interactive Element Sizing

\*\*3.1 Minimum touch target.\*\* Apple's published iOS/iPadOS minimum is \*\*44 × 44 pt\*\*. HIG does not publish a separate larger minimum for iPad — it's the same number. However, because iPad is held farther and often used in landscape with thumbs at the edges, the practical minimum should be larger.

\*\*3.2 Primary CTA size.\*\* Apple does not publish a CTA-specific dimension. Aligned with the 44 pt floor and the 3 ft viewing distance: minimum height \*\*50 pt\*\*, target height \*\*56–60 pt\*\*, with horizontal padding \*\*24–32 pt\*\* beyond the label. Minimum tap width \*\*120 pt\*\* for a button with text.

\*\*3.3 Icon-only buttons.\*\* Hit area minimum \*\*44 × 44 pt\*\* even if the glyph itself is 24 pt. For a premium pitch experience use \*\*48 × 48 pt\*\* visible target with \*\*56 × 56 pt\*\* hit area (transparent padding inside).

\*\*3.4 Visible size when pointer connects.\*\* Apple's Pointing devices page is explicit: the iPadOS pointer "gives people an additional way to interact with apps and content — it doesn't replace touch." Do \*\*not\*\* shrink visible elements when a pointer is connected. Apple's recommendation is to keep the touch-sized target and add pointer effects on top. The pointer's own magnetism and the highlight/lift effects make smaller-feeling precision possible without shrinking actual hit regions.

\---

\#\# SECTION 4 — Pointer, Cursor, and Trackpad Interaction

This is the most platform-specific section and Apple's Pointing devices page is unusually concrete.

\*\*4.1 Standard pointer effects.\*\* iPadOS defines exactly three content effects:

\- \*\*Highlight.\*\* Pointer transforms into a translucent rounded rectangle that acts as a background for the control, with gentle parallax. Apple applies this by default to \*\*bar buttons, tab bars, segmented controls, and edit menus\*\* — i.e. small elements with transparent backgrounds.  
\- \*\*Lift.\*\* Pointer fades out beneath the element, the element scales up slightly with a shadow below and a soft specular highlight on top. Apple applies this by default to \*\*app icons and Control Center buttons\*\* — small elements with opaque backgrounds.  
\- \*\*Hover.\*\* Generic effect that applies custom scale, tint, and/or shadow to an element. Pointer shape is \*\*not\*\* transformed. Apple uses hover for \*\*large elements\*\* — cards, panels, large CTAs.

In addition: pointer \*\*accessories\*\* (small secondary indicators like resize arrows) can combine with any pointer; pointer \*\*magnetism\*\* pulls the cursor toward elements that use Highlight or Lift but not Hover.

\*\*4.2 Pointer on a large primary amber CTA.\*\* Because a large filled CTA is a \*\*large opaque element\*\*, the correct effect is \*\*Hover\*\*, not Lift. Apple's reasoning: Lift is for "small element with an opaque background" (icons, control-center pills); a hero CTA is large. Apply hover with:

\- Scale: \*\*1.03–1.05×\*\* (subtle, not 1.1 — Apple's Lift on app icons is about 1.10× and it's already noticeable; hover on a large button should be more restrained).  
\- Tint: shift the amber \*\*5–10% lighter or shift toward warmer/brighter\*\* on hover.  
\- Shadow: a subtle drop shadow (Y offset 4–8 pt, blur 16–24 pt, alpha 0.10–0.15).  
\- Duration: pointer effects in iPadOS animate in roughly \*\*150–250 ms\*\* with ease-out; Apple does not publish the exact curve but the system effect is closest to a standard ease-out (\`cubic-bezier(0.2, 0, 0.0, 1)\`).

The pointer shape itself does \*\*not\*\* change to a hand or other glyph on a button — it stays the default circle. iPadOS pointer language is fundamentally different from macOS or the web: the element transforms, not the cursor.

\*\*4.3 Pointer on a tappable card/panel.\*\* Cards and panels are large surfaces — use \*\*Hover\*\*. Recommended: scale \*\*1.02×\*\*, very subtle tint lift (1–3% lighter on a dark surface, equivalent darker on a light surface), shadow as above. No pointer shape change. Apple's note: "for an element that has little space around it, consider using a hover effect that includes tint, but not scale and shadow, because an unscaled element doesn't appear to get closer to the viewer even when its shadow implies that it's elevated." If the card has neighbors close to it, drop the shadow and use tint only.

\*\*4.4 Pointer on non-interactive elements.\*\* Apple's iPadOS pointer auto-adapts. On non-interactive text and decorative content, the pointer remains its \*\*default circle\*\* — it does not become an arrow (that's macOS behavior) and it does not disappear. Apple's only exception: on text-entry areas the pointer becomes the I-beam. For your read-only briefing, large text blocks should not get any pointer treatment — leave the default circle alone.

\*\*4.5 Cursor shapes.\*\* iPadOS defines a much smaller set than macOS:

\- \*\*Default circle\*\* — the resting pointer, used over all surfaces unless something more specific applies.  
\- \*\*I-beam\*\* — over text-entry areas, automatically.  
\- \*\*Custom shapes\*\* — you can supply a custom \`UIPointerShape\` (rounded rect with specified corner radius, vertical/horizontal beam, or a custom path), but Apple cautions against gratuitous custom pointers.

iPadOS does \*\*not\*\* use the macOS hand/pointing cursor over links. The platform language is element-transforms-not-cursor-transforms.

\*\*4.6 When to suppress the pointer.\*\* Apple's Pointing devices page notes that in videos and similar media the pointer can hide on inactivity: "people can move the pointer to reveal or hide playback controls while they watch a full-screen video." For your pitch experience this is appropriate during a held-still step — after roughly \*\*3 seconds of pointer inactivity\*\* while on a presentational (non-interactive) step, fade the pointer out; restore on any pointer movement.

\*\*4.7 Hover state magnitude and duration.\*\* HIG: "people notice when the appearance of the pointer or the UI element beneath it changes, and they expect the changes to be useful." Avoid gratuitous effects. Magnitude guidance:

\- Scale change for hover: \*\*1.02–1.05×\*\*, never more than 1.10×.  
\- Tint change: subtle — 3–10% luminance shift, not a hue jump.  
\- Shadow: short Y offset (4–8 pt), wide blur (16–32 pt), low alpha (0.08–0.15).  
\- Duration: \*\*150–250 ms\*\* in, \*\*200–300 ms\*\* out (slightly slower exit feels native).  
\- Easing: ease-out on hover-in, ease-in-out on hover-out.

\*\*4.8 Hold-to-activate (progress ring).\*\* Apple does not publish a numeric specification for hold-to-fill on iPadOS. Touch and pointer behavior should differ:

\- \*\*Touch:\*\* the user holds their finger. The progress ring fills over a deliberate but not slow duration — \*\*800–1200 ms\*\* to complete is the iPad-native feel (matches Apple's haptic-touch long-press of 500 ms with a deliberate continuation).  
\- \*\*Trackpad/mouse:\*\* the user holds the primary click. Use the same fill duration. Crucially, the pointer should \*\*not\*\* transform during hold — keep the default circle and let the element show the progress. Pair with a haptic on iPad (via the Vibration API in Safari is unreliable, so plan visual \+ audio feedback for trackpad users instead).  
\- On either input, allow the user to \*\*cancel\*\* by releasing before completion — HIG's Motion page explicitly says "let people cancel motion."

\---

\#\# SECTION 5 — Gestures

Apple's gesture reservations for iPadOS are spread across the Going full screen, Multitasking, and Layout pages, not in a single gestures table. Here is the consolidated picture.

\*\*5.1 System-reserved gestures (must never be intercepted).\*\*

\- \*\*Swipe up from bottom edge\*\* → Home / app switcher (Home indicator). Reserved zone: roughly the bottom \*\*20 pt\*\* of the screen. The first swipe-up only reveals the Home indicator if you set \`preferredScreenEdgesDeferringSystemGestures\` for the bottom edge — this is an iPad-specific affordance Apple explicitly recommends for full-screen experiences. A web app cannot use this UIKit API; in Mobile Safari the system always responds on the first swipe-up.  
\- \*\*Slow drag up and pause from bottom edge\*\* → App switcher. Same bottom-edge zone.  
\- \*\*Swipe down from top-right corner\*\* → Control Center. Reserved zone: the top \*\*\~20 pt\*\* from the top edge, in roughly the right \*\*30%\*\* of screen width.  
\- \*\*Swipe down from top-left or top-center\*\* → Notification Center / Lock Screen widgets. Reserved zone: the top \*\*\~20 pt\*\* from the top edge.  
\- \*\*Swipe from right edge (4 fingers / horizontal trackpad swipe)\*\* → app switching between recent apps. Reserved on the trailing edge in a full multitasking context. In a single-app full-screen web view this is less of a conflict but Apple still expects you not to fight it.  
\- \*\*Four/five-finger pinch\*\* → return to Home Screen. Multi-finger reserved.  
\- \*\*Four-finger horizontal swipe\*\* → switch between recent apps. Reserved.  
\- \*\*Apple Pencil double-tap / squeeze\*\* → reserved by the system if the user has set it that way; do not override.

Apple's explicit recommendation in Going full screen: "By default, the Home Screen indicator automatically hides shortly after someone switches to your app. It reappears when someone interacts with the bottom portion of the screen, allowing them to swipe once to exit. Whenever possible, retain this behavior because it's familiar and what people expect."

\*\*5.2 Safe in-app gestures.\*\*

\- \*\*Single-finger horizontal swipes across the center of the screen\*\* — fully safe. This is what you want for step navigation.  
\- \*\*Vertical swipes in the middle of the screen\*\* — safe (no system reservation in the interior).  
\- \*\*Tap, double-tap, long-press\*\* — fully safe.  
\- \*\*Two-finger pinch in the center\*\* — safe.

Leave \*\*at least a 20 pt buffer from the top edge and 20 pt from the bottom edge\*\* before initiating any custom swipe handling. Likewise, do not register horizontal swipe gestures that \*\*begin within 16 pt of the left or right edge\*\* — these conflict with multitasking gestures even in single-app contexts.

\*\*5.3 iPad-vs-iPhone gesture conflicts.\*\* Unique to iPad:

\- The \*\*right-edge swipe\*\* for Slide Over / Stage Manager / app switching does not exist on iPhone. Your horizontal-swipe-to-advance must not start within \~16 pt of the right edge.  
\- \*\*Four-finger gestures\*\* for app switching and Home are iPad-only. If you support multi-touch animations, never use four-finger combinations.  
\- \*\*Pencil hover\*\* (iPad Pro M2 and later, including iPad Pro 13 M4): the system surfaces a hover preview when an Apple Pencil approaches the screen. Treat Pencil hover the same as pointer hover for your purposes — do not implement a different visual.

\*\*5.4 Swipe-to-advance thresholds.\*\* Apple does not publish a numeric swipe threshold. Working values that match the feel of UIKit's \`UIPageViewController\` and Mobile Safari's own page navigation:

\- \*\*Minimum horizontal distance:\*\* \*\*60 pt\*\* of travel before committing the page change.  
\- \*\*Minimum velocity (alternative trigger):\*\* \*\*0.3 pt/ms\*\* (300 pt/s) — a quick flick should advance even if it didn't travel 60 pt.  
\- \*\*Angle constraint:\*\* discard if the dominant axis is more than \*\*30° off horizontal\*\* (treat as a vertical pan).  
\- \*\*Rubber-band / pull-back:\*\* if neither distance nor velocity is met on release, snap back over \*\*250–300 ms\*\* with ease-out.

\---

\#\# SECTION 6 — Safe Areas

Apple does not publish a per-device numeric safe-area inset table in HIG. The values below come from iPadOS's published behavior and the device's known geometry. iPad Pro 13" (M4, Face ID, no Home button) shares safe-area geometry with the prior 12.9" Face ID iPad Pro generations.

\*\*6.1 Portrait insets (1024 × 1366 pt):\*\*

\- Top: \*\*24 pt\*\* (status bar). When status bar is hidden, top inset reduces to \*\*0 pt\*\* but corner-radius clearance still applies.  
\- Bottom: \*\*20 pt\*\* (Home indicator zone).  
\- Left: \*\*0 pt\*\*.  
\- Right: \*\*0 pt\*\*.

\*\*6.2 Landscape insets (1366 × 1024 pt) — both landscape-left and landscape-right are symmetric on Face ID iPads:\*\*

\- Top: \*\*24 pt\*\* (status bar).  
\- Bottom: \*\*20 pt\*\* (Home indicator zone).  
\- Left: \*\*0 pt\*\*.  
\- Right: \*\*0 pt\*\*.

Unlike Face ID iPhones, Face ID iPads have \*\*no notch\*\* and no Dynamic Island, so the left/right insets in landscape are zero. The TrueDepth camera is in a corner but does not create a software safe-area inset.

\*\*6.3 Contributors to safe area.\*\*

\- \*\*Status bar\*\* — top inset of 24 pt in both orientations, when present.  
\- \*\*Home indicator\*\* — bottom inset of 20 pt in both orientations. The visible indicator bar itself is \~5 pt tall but its reserved zone is 20 pt.  
\- \*\*Rounded display corners\*\* — the iPad Pro 13 has a hardware display corner radius of \*\*\~18 pt\*\* (see Section 13). This does not increase the safe-area inset value, but it does mean square-cornered content at the corners will be physically clipped by the bezel.  
\- \*\*TrueDepth camera housing\*\* — does \*\*not\*\* create a safe area on iPad; the housing is in the bezel, not the screen.

\*\*6.4 Where interactive content may go.\*\* Interactive controls must stay inside the safe area. Decorative content (background gradients, full-bleed photography, color washes) may extend into the unsafe zone — Apple's Layout page explicitly says: "make sure backgrounds and full-screen artwork extend to the edges of the display." Text and CTAs may not.

\---

\#\# SECTION 7 — Status Bar

\*\*7.1 Height in portrait:\*\* \*\*24 pt\*\* on iPad Pro 13\. (Apple does not publish this number in HIG prose, but it has been the iPad status-bar height since the iPad Pro 12.9 redesign.)

\*\*7.2 Height in landscape:\*\* \*\*24 pt\*\* — iPad status-bar height does not change with orientation, unlike iPhone where the landscape mode hides it.

\*\*7.3 Can it be hidden.\*\* Yes. Apple's Layout page allows hiding it "if you offer an in-depth experience like playing a game or viewing media, where it might make sense to hide the status bar." A premium investor briefing qualifies. In Mobile Safari, the status bar is hidden when the web app runs as a fullscreen PWA or in standalone mode added to Home Screen; in a regular Safari tab the Safari chrome remains and the status bar is part of the system UI you cannot suppress. For an iPad-native feel, deliver this experience as a \*\*Home Screen-installed standalone web app\*\* with \`apple-mobile-web-app-capable\` and \`apple-mobile-web-app-status-bar-style\` set.

\*\*7.4 Clearance below status bar.\*\* If visible, content begins at \*\*24 pt\*\* from the top. For text and CTAs, add another \*\*8–16 pt\*\* of breathing room before any content begins — so text starts at \*\*32–40 pt\*\* from the absolute top of the display.

\---

\#\# SECTION 8 — Home Indicator

\*\*8.1 Does iPad Pro 13 have a home indicator.\*\* Yes. Face ID iPads (all 11" and 12.9"/13" Pro models since 2018, plus iPad Air 11"/13") have a Home indicator bar at the bottom. The visible bar is approximately \*\*5 pt tall\*\* and \*\*\~134 pt wide\*\*, centered.

\*\*8.2 Bottom safe-area inset.\*\* \*\*20 pt\*\* in both orientations. The Home indicator's reserved interaction zone is larger than its visible footprint.

\*\*8.3 Minimum clearance for interactive content.\*\* Interactive controls must sit \*\*at least 20 pt\*\* above the bottom edge (i.e. inside the safe area). For a premium CTA, give \*\*32–48 pt\*\* of clearance above the bottom edge so the CTA does not appear cramped against the indicator. HIG: "avoid full-width buttons. Buttons feel at home in iOS when they respect system-defined margins and are inset from the edges of the screen."

\---

\#\# SECTION 9 — Orientation

\*\*9.1 Preferred orientation.\*\* Apple's Layout page says explicitly for iOS/iPadOS: "Aim to support both portrait and landscape orientations. People appreciate apps and games that work well in different device orientations." For a reading-and-viewing pitch experience on iPad Pro 13 with the Magic Keyboard, \*\*landscape is the dominant natural orientation\*\* — the Magic Keyboard physically docks the iPad in landscape, and presentation/reading-with-keyboard contexts default there. But Apple does not designate one as "preferred" generically.

\*\*9.2 Orientation locking.\*\* Apple's stance: "Aim to support both… sometimes your experience needs to run in only portrait or only landscape. When this is the case, you can rely on people trying both orientations before settling on the one you support — there's no need to tell people to rotate their device." So locking is acceptable when there is a clear creative reason. For a cinematic investor briefing, locking to \*\*landscape\*\* is fully HIG-compliant and arguably ideal. If you lock, support both landscape-left and landscape-right ("if your app is landscape-only, make sure it runs equally well whether people rotate their device to the left or the right").

\*\*9.3 Layout changes between orientations.\*\* Since both orientations on iPad Pro 13 are Regular/Regular size class, HIG tells you not to switch to a compact layout. Expected changes:

\- Re-flow column count (e.g., 6-col portrait → 8-col landscape).  
\- Move primary CTA from below content (portrait) to beside content (landscape) when content is wide.  
\- Hero imagery aspect ratio may change but not content priority.  
\- Type scale stays identical.

\*\*9.4 Safe  
