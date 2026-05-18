Continuing from Section 9.4. One important correction before I proceed: Apple's Accessibility page publishes the iPadOS control sizes as \*\*44×44 pt default, 28×28 pt absolute minimum\*\* — my earlier Section 3.1 stated 44×44 as the minimum. The 44×44 figure is Apple's \*recommended default\*; 28×28 is the \*floor\* for cases where space is constrained. For your premium pitch experience, ignore the 28×28 floor and treat 44×44 as the working minimum. Same page also confirms iPadOS pointer/hover padding: \*\*12 pt around elements with a bezel, 24 pt around elements without\*\* — matching the Pointing devices page exactly.

\---

\#\# SECTION 9.4 — Safe-area inset changes on rotation (iPad Pro 13", M4)

On a Face ID iPad with no notch and no Dynamic Island, the device geometry is symmetric — rotating between portrait and landscape changes which physical edge faces "up" but does not introduce new hardware obstructions. The result:

\- \*\*Top inset:\*\* \*\*24 pt\*\* in both portrait and landscape (status bar height, when status bar is visible). If the status bar is hidden, this collapses to \*\*0 pt\*\* in both orientations. The value does not change on rotation.  
\- \*\*Bottom inset:\*\* \*\*20 pt\*\* in both portrait and landscape (Home indicator reserved zone). This value does not change on rotation. Unlike iPhone where the landscape Home indicator can shift to a side, on iPad the Home indicator always remains at the \*\*physical bottom\*\* of the device as oriented by the user.  
\- \*\*Left inset:\*\* \*\*0 pt\*\* in both orientations.  
\- \*\*Right inset:\*\* \*\*0 pt\*\* in both orientations.

The practical answer: on iPad Pro 13, \*\*no safe-area inset value changes when the device rotates\*\*. What changes is only the canvas dimensions (1024 × 1366 in portrait, 1366 × 1024 in landscape). Both landscape-left and landscape-right produce identical inset values — there is no asymmetric notch to worry about, which is the major contrast with Face ID iPhones.

The only subtle wrinkle: if your web app uses the \`env(safe-area-inset-\*)\` CSS variables in Mobile Safari with the standard meta viewport \`viewport-fit=cover\`, all four values will report consistently across orientations on this device. If the values you see on rotation suddenly include left/right insets, the user is probably running your app in Split View or Slide Over — that is a windowed context, not full screen, and your layout should respond to width changes rather than safe-area changes.

\---

\#\# SECTION 11 — Animation and Motion

\*\*11.1 Duration ranges for iPadOS transitions.\*\* Apple does not publish a numeric duration table in HIG. The Motion page only gives qualitative guidance ("aim for brevity and precision," "consider using animated symbols where it makes sense"). The de-facto durations that match the feel of UIKit's built-in transitions and Apple's first-party iPad apps:

\- \*\*Micro-interactions\*\* (button press, tint shift, pointer hover-in): \*\*120–200 ms\*\*.  
\- \*\*Element entrance/exit\*\* (a card fading in, an icon appearing): \*\*220–280 ms\*\*.  
\- \*\*Panel and sheet entrance\*\* (modal sheet sliding in, popover appearing): \*\*350–450 ms\*\* in, \*\*300–350 ms\*\* out.  
\- \*\*Full-screen step transitions\*\* (your case — one full-screen step crossfading or sliding to the next): \*\*400–600 ms\*\*. This is the iPad-specific range. On iPhone the equivalent feels right at \*\*300–400 ms\*\* because the canvas is smaller; on iPad the larger canvas requires slightly more time for the eye to follow the motion across the longer distance.  
\- \*\*Hero/cinematic transitions\*\* (an investor briefing's signature moments): \*\*600–900 ms\*\* is acceptable for a few intentional, infrequent transitions. Past 1000 ms an animation starts to feel cinematic in a way that fights interactivity.

The asymmetry rule: \*\*exits should be 10–20% faster than entrances.\*\* Apple's UIKit conventions reflect this — \`UIViewAnimationOptionCurveEaseIn\` for dismissals, \`UIViewAnimationOptionCurveEaseOut\` for presentations.

\*\*11.2 Native easing curves.\*\* Apple's named curves map to these approximate cubic-bezier values, derived from observation of UIKit's built-in animations and SwiftUI's \`Animation\` defaults:

\- \*\*Default / standard ease (UIKit \`easeInOut\`):\*\* \`cubic-bezier(0.42, 0, 0.58, 1)\`. The general-purpose curve for most state changes.  
\- \*\*Ease-out (presentations, panel entrances):\*\* \`cubic-bezier(0.0, 0.0, 0.2, 1)\` or the slightly more decisive \`cubic-bezier(0.2, 0, 0, 1)\`. This is the curve that feels most "iPad" — content arrives quickly and decelerates into place.  
\- \*\*Ease-in (dismissals):\*\* \`cubic-bezier(0.4, 0, 1, 1)\`. Content departs gathering speed.  
\- \*\*Sharp / decisive (snap-to-position, page commits):\*\* \`cubic-bezier(0.4, 0, 0.2, 1)\`. Used by UIKit's \`UIPageViewController\` and the system's interactive page transitions.  
\- \*\*Spring (SwiftUI default \`Animation.spring\`):\*\* in CSS terms, approximate with \`cubic-bezier(0.5, 1.5, 0.5, 1)\` — but real Apple springs are physical (damping ratio \~0.825, response time \~0.4 s), not bezier curves. If you can use a real spring (SwiftUI, Framer Motion, Lottie), do; if you're stuck with CSS, use the cubic approximation. The native springs feel like settling-with-overshoot, not robotic ease.

What you should \*\*avoid\*\*: linear (\`cubic-bezier(0, 0, 1, 1)\`) — never used in native iPadOS UI. \`ease-in-out-cubic\`-style symmetric curves (e.g., \`cubic-bezier(0.65, 0, 0.35, 1)\`) feel correct in isolation but slightly Material/Google-ish; native iPad transitions are biased toward ease-out for arrivals.

\*\*11.3 What makes a motion feel iPad-native vs. scaled-up iPhone.\*\* Specifics, not principles:

\- \*\*Distance-proportional duration.\*\* On iPad, an element traveling 800 pt across the screen needs more time than the same element traveling 300 pt on iPhone. A scaled-up iPhone animation reuses the 300 ms duration on a 1366 pt canvas, which makes the motion feel rushed and twitchy. iPad-native: animate at \*\*\~1.0–1.5 pt per ms\*\* for in-screen transitions; iPhone animations often hit 2.0+ pt/ms because the screen is smaller.  
\- \*\*Spring over linear/quadratic where possible.\*\* Apple's first-party iPad apps lean heavily on spring physics for any non-trivial movement (Spotlight expanding, Files folder opening, Slide Over sliding in). Scaled-up iPhone web work tends to use single cubic-bezier curves throughout. Springs give the small overshoot that signals "physical object on a large surface."  
\- \*\*Subtle parallax on large elements.\*\* Apple's pointer effects (highlight and lift) include parallax. Large iPad cards and hero images often subtly translate at a slightly different speed than their container during transitions. iPhone equivalents usually omit this because the canvas is too small for parallax to register.  
\- \*\*No bouncy entrances on full-screen content.\*\* A spring with overshoot on a 1366-pt-wide element looks ridiculous — the bounce becomes large in absolute terms. Use springs for elements under \~400 pt; use damped curves (ease-out) for full-screen content.  
\- \*\*Multi-stage choreography.\*\* Native iPad transitions often have 2–3 stages: background dims first (150 ms), then content slides in (350 ms), then accent details fade in last (200 ms). Total \~700 ms but staged. Scaled-up iPhone animations do everything at once.  
\- \*\*No "blast" transitions.\*\* A common iPhone-web pattern is whole-page wipe transitions — on iPad they feel like a presentation tool, not an app. Native iPad transitions favor element-level animation against a stable backdrop.

Common iPhone-to-iPad motion mistakes:

\- Using the same 250 ms duration across both platforms.  
\- Animating only opacity (fade in/out) instead of opacity \+ small transform.  
\- Snapping content into place with no settle.  
\- Animating CTAs with the same scale-pulse used on iPhone (e.g., 0.95× tap-down) — on iPad with a pointer, that pulse runs every hover; it gets annoying fast.  
\- Modal sheets that slide up from the very bottom of a 1366 pt landscape screen — on iPhone this is fine; on iPad it's too long a journey. iPad sheets are typically centered (form sheet / page sheet styles).

\*\*11.4 ProMotion 120 Hz considerations.\*\* The iPad Pro 13 (M4) is a ProMotion display capable of 120 Hz. Apple's stance: ProMotion does not change durations or curves — it changes \*\*smoothness only\*\*. Your 400 ms transition is still 400 ms; it just renders in 48 frames instead of 24\.

Practical implications:

\- Do not shorten durations because the device is 120 Hz. Human perception of duration is independent of frame rate.  
\- Do not specify motion in frames — specify in milliseconds.  
\- Use CSS \`transform\` and \`opacity\` transitions, which Safari can drive at 120 Hz on this device. Animating non-composited properties (\`top\`, \`left\`, \`width\`, box-shadow blur) caps your effective rate at much lower than 120 Hz and produces jank that is more visible on a ProMotion display, not less.  
\- Easing precision matters more at 120 Hz. A subtly wrong curve that was forgivable at 60 Hz becomes visibly wrong at 120 Hz because more intermediate frames are sampled. Spend the time getting curves right.  
\- Test with \`prefers-reduced-motion\` and with the device set to lower refresh-rate modes if possible — your animations should still look right at 60 Hz.

\*\*11.5 Reduced Motion on iPadOS.\*\* Apple's Accessibility page is unusually specific. When the user enables Reduce Motion (Settings → Accessibility → Motion → Reduce Motion), HIG explicitly directs designers to:

\- \*\*Tighten animation springs\*\* to reduce bounce effects.  
\- \*\*Track animations directly with people's gestures\*\* (i.e., the animation follows the finger 1:1 rather than amplifying or extrapolating).  
\- \*\*Avoid animating depth changes in z-axis layers.\*\*  
\- \*\*Replace transitions in x-, y-, and z-axes with fades\*\* to avoid motion.  
\- \*\*Avoid animating into and out of blurs.\*\*

For your full-screen cinematic transitions specifically, the reduced-motion variant should be:

\- Replace any sliding or directional transition between steps with a \*\*simple cross-fade\*\* at \*\*150–200 ms\*\* (faster than the full-motion version because there's nothing to track).  
\- Remove all parallax on hero images and large surfaces.  
\- Remove all scale animations on enter/exit — opacity only.  
\- Remove pointer hover scale; keep tint and shadow.  
\- Disable any background motion (Ken Burns pans, ambient particle motion, video loops in backgrounds). Substitute a still frame.  
\- Remove all spring physics; substitute linear or ease-out fades.  
\- Keep micro-interactions (button press visual feedback) but reduce them to a tint flash, no scale.

Implementation in CSS: wrap motion definitions in \`@media (prefers-reduced-motion: reduce) { … }\` and provide the fade-only fallbacks there. Test the entire 20-step flow with Reduce Motion on; the experience should still feel premium, just calmer.

\---

\#\# SECTION 12 — What Makes an iPadOS App Feel Native

\*\*12.1 Characteristics that signal "built for iPad."\*\* Each item below: correct iPad behavior, wrong (scaled-iPhone or scaled-web) behavior.

\*\*Content density at viewing distance.\*\* \*Correct:\* type and controls sized for \~3 ft viewing — body 19–22 pt, hero 64–96 pt, CTA 56 pt tall. Generous negative space; content occupies roughly 50–65% of viewport area with the rest as breathing room. \*Wrong:\* iPhone proportions enlarged uniformly — body at 32 pt and CTAs at 80 pt because someone "scaled up by 1.5×." Looks bombastic and child-like.

\*\*Pointer effects as primary feedback for trackpad users.\*\* \*Correct:\* every interactive element responds to pointer hover with Highlight, Lift, or Hover content effect. CTAs lift subtly (scale 1.03–1.05×, shadow appears, tint shifts). Cards respond with tint+scale. \*Wrong:\* no hover states at all, or a \`cursor: pointer\` change with no visible element response. Trackpad users feel like the app doesn't know they exist.

\*\*Single-orientation locking with both rotations supported.\*\* \*Correct:\* if locked to landscape, both landscape-left and landscape-right work identically. \*Wrong:\* locked to one rotation only; orientation changes cause the experience to refresh or break.

\*\*Layout that respects the readable measure.\*\* \*Correct:\* body text constrained to 60–75 characters per line even on a 1366-pt-wide canvas; full-bleed used only for backgrounds and hero imagery. \*Wrong:\* body paragraphs stretched edge-to-edge across the full 1366 pt — looks like a marketing site, not an app.

\*\*Layered content over a stable backdrop.\*\* \*Correct:\* a persistent background or context layer with content moving on top of it during transitions. \*Wrong:\* whole-page slide transitions where every pixel moves at once. iPad-native motion always preserves a frame of reference.

\*\*Multi-input mental model.\*\* \*Correct:\* the same interaction works with touch, pointer, keyboard, and (where relevant) Pencil. Arrow keys advance steps, Tab moves focus visibly, hover and touch produce equivalent feedback. \*Wrong:\* touch-only — keyboard tab does nothing visible; arrow keys do nothing; the app is dead in the water on a Magic Keyboard setup.

\*\*Restraint in motion.\*\* \*Correct:\* a few intentional, choreographed transitions per session, each lasting 400–600 ms, with parallax and stagger on a stable backdrop. \*Wrong:\* every state change animates with bounce-and-overshoot; every step entrance has its own bespoke effect; the experience feels like a Lottie reel.

\*\*System-style component shapes.\*\* \*Correct:\* CTAs, cards, and sheets use corner radii in the 8–20 pt range that match the device's hardware corner radius (\~18 pt — see Section 13). Sheets centered as form sheets, not slid up from the bottom edge. \*Wrong:\* sharp 0-pt corners on a device with 18 pt display corners; bottom sheets occupying the full bottom half of a landscape iPad screen.

\*\*Edge handling.\*\* \*Correct:\* full-bleed background extends to all four edges; controls inset from the safe area by ≥20 pt and never within 16 pt of left/right edges (gesture conflict zones). \*Wrong:\* CTAs flush against the bottom edge, or against the right edge in landscape where Stage Manager and multitasking gestures live.

\*\*Status of the cursor when idle.\*\* \*Correct:\* the default circle pointer rests at any non-interactive position; on text-entry areas it becomes the I-beam; on interactive elements it transforms into highlight/lift shapes. \*Wrong:\* \`cursor: pointer\` (the hand) everywhere; or \`cursor: none\` with no system-respecting rationale.

\*\*12.2 Damaging mistakes that betray "blown-up phone." Concrete symptoms.\*\*

\- \*\*Single-column body text running the full 1366 pt width.\*\* Symptom: the user's eye loses the line return; they re-read the same line; reading feels exhausting. Native iPad apps never do this.  
\- \*\*Full-width primary CTAs spanning edge-to-edge.\*\* Apple's HIG explicitly calls this out: "avoid full-width buttons." Symptom: the CTA looks like an iPhone bottom-sheet action bar pasted onto a 1366 pt canvas. The button feels physically wrong because it's huge and the eye doesn't know where to click within it.  
\- \*\*Tap-to-advance with no swipe support.\*\* Symptom: a Magic Trackpad two-finger swipe across the surface does nothing. The user expects swipes; touch-only feels like a kiosk demo.  
\- \*\*Bottom sheets that slide up the full landscape height.\*\* Symptom: the sheet has to travel \~1000 pt in landscape, takes \~600 ms, and feels heavy. Native iPad uses centered form sheets or page sheets, not phone-style bottom sheets.  
\- \*\*Touch targets at the iPhone 44 pt minimum.\*\* Symptom: the user with a trackpad has to aim carefully at small targets; the user with a finger feels the controls are flimsy. iPad-native uses 50–60 pt for primary controls.  
\- \*\*No hover states.\*\* Symptom: a user with a connected Magic Keyboard and trackpad moves the pointer over every element and nothing responds; the experience feels broken or read-only.  
\- \*\*Modal dialogs that fill the screen on iPad as they do on iPhone.\*\* Symptom: dismissing a quick confirmation requires a giant overlay that occludes the entire briefing. Use compact alerts/popovers anchored to their trigger.  
\- \*\*Identical type ramp on iPhone and iPad.\*\* Symptom: type that looks correct on iPhone is undersized on iPad at 3 ft viewing distance; the user has to lean in to read body text.  
\- \*\*Bouncy spring animations on full-screen panels.\*\* Symptom: a 1024 pt-wide panel overshoots and settles — the overshoot is dozens of pixels and feels cartoonish on a premium briefing.  
\- \*\*No keyboard navigation.\*\* Symptom: hitting arrow keys, Tab, or Space does nothing. On Magic Keyboard, this immediately reads as "this is a phone app running on iPad."  
\- \*\*Animations measured in frames or sized for 60 Hz.\*\* Symptom: on the 120 Hz ProMotion display, motion that was hand-tuned at 60 Hz looks subtly stuttery because composited-property assumptions are wrong; non-transform animations cap effectively below 120 Hz.  
\- \*\*Loading states that show iPhone-style spinners.\*\* Symptom: a tiny 20 pt spinner in the center of a 1366 pt screen looks lost. iPad uses larger, more deliberate loading states or, preferably, designs to avoid showing them at all in a pitch context.  
\- \*\*Status bar / Safari chrome visible.\*\* Symptom: the URL bar and tabs visible during a "premium investor briefing" — instantly breaks the illusion. Run it as a Home Screen-installed PWA in standalone mode.

\*\*12.3 Choices that most strongly reinforce native iPad feel for your specific case\*\* (full-screen, no scroll, sequential, cinematic, 20 steps):

\- \*\*Install as a standalone PWA\*\* with \`apple-mobile-web-app-capable=yes\`, \`apple-mobile-web-app-status-bar-style=black-translucent\`, and a custom Home Screen icon. This removes Safari chrome entirely and is the single highest-leverage move for native feel.  
\- \*\*Lock to landscape, support both landscape-left and landscape-right.\*\* Investor briefings live in landscape; this is the natural Magic Keyboard orientation.  
\- \*\*Adopt all three iPadOS pointer content effects\*\* — Highlight on small interactive icons (close, prev/next arrows), Lift for any small opaque buttons, Hover (tint \+ subtle scale) on the primary amber CTA and on large card surfaces. This single decision separates "iPad web app" from "iPad-native experience" for trackpad users.  
\- \*\*Stage-aware swipe-to-advance\*\* with the thresholds in Section 5.4 (60 pt distance OR 300 pt/s velocity, 30° angle constraint), with rubber-band snap-back at 250–300 ms ease-out on incomplete swipes.  
\- \*\*Keyboard navigation parity.\*\* Right arrow / Space advances; Left arrow goes back; Esc dismisses any overlay; numeric 1–9 keys jump to step. Apple's HIG: "let people use the keyboard alone to navigate."  
\- \*\*Multi-stage transitions between steps\*\* — backdrop tint shift (150 ms) → outgoing content fade \+ 12 pt translate (300 ms) → incoming content fade \+ 12 pt translate from opposite direction (350 ms, ease-out) → amber accent elements fade in last (200 ms, 80 ms delay). Total \~550 ms. This staged choreography is the strongest motion signal of "designed for this canvas."  
\- \*\*Persistent stable backdrop layer.\*\* A subtle background gradient or surface that does not move between steps; only the content layer animates. This creates the "stable frame of reference" the HIG repeatedly emphasizes.  
\- \*\*Idle pointer fade.\*\* After 3 s of pointer inactivity, fade the cursor to 0 opacity over 300 ms. Restore instantly on movement. On non-interactive steps the experience reads as cinema; on interactive steps the cursor is there when needed.  
\- \*\*No scrollbars, no chrome, no toolbars.\*\* HIG's full-screen page allows this for "in-depth experiences." Use it.  
\- \*\*A single visible accent (amber) reserved exclusively for interactive affordances.\*\* Every amber element is tappable; no decorative amber. This trains the user in two steps and removes the need for any tutorial.  
\- \*\*Generous, asymmetric layout grids.\*\* A 8-column landscape grid with content placed across columns 2–6 (leaving columns 1 and 7–8 as breathing room) is more iPad-native than a centered, symmetric block. Apple's reading-order guidance: "place the most important items near the top and leading side."  
\- \*\*Honor Reduce Motion completely.\*\* The spec in 11.5. A premium briefing that respects accessibility instantly reads as a serious, native product.

\*\*12.4 The single most underestimated layout/interaction difference.\*\* It is this: \*\*on iPad, interactive feedback is element-centric, not cursor-centric.\*\* On the web and on macOS, designers think in terms of cursor states — the hand pointer, the I-beam, the disabled cursor. On iPad, the cursor is a small dot that adapts to the \*element\* it touches. The element transforms; the cursor mostly does not.

Designers porting iPhone/web experiences to iPad almost always miss this. They keep \`cursor: pointer\` (the hand) on interactive elements, leave the elements unchanged on hover, and call it done. A user with a Magic Trackpad sees a hand-shaped cursor over a static button and feels like they're using a 2010 website. A user accustomed to native iPad apps expects the \*button\* to lift, tint, or scale — the hand cursor on iPad is actively wrong because iPadOS doesn't use it. The cursor should remain the system default; the button should respond.

A close runner-up: \*\*iPad is not a smaller laptop and not a larger phone — its layout density target is unique.\*\* Designers tend to either keep iPhone density (too sparse) or apply desktop density (too crowded). The iPad target is between the two, closer to "magazine spread" than to either phone or app — generous margins, large typography, deliberate hierarchy, fewer simultaneous interactive elements per viewport.

\*\*12.5 How a hover-less, pointer-effect-less web app reads on iPad.\*\* Specifically with a Magic Keyboard and trackpad attached:

\- The pointer remains a static dot over every surface, including over CTAs that would normally lift or tint. To the user, this reads as "the app doesn't know I have a pointer attached" — which is precisely correct, because it doesn't.  
\- Without Highlight or Lift effects, small interactive icons (chevrons, close buttons) feel uncertain — the user is unsure if their pointer is "on" the target. iPadOS pointer magnetism normally provides a tactile pull at the hit region; without any content effect, that pull is absent, so precision feels worse than on macOS web equivalents.  
\- Without a Hover effect on large amber CTAs, the user often clicks twice or hesitates — the lack of visual confirmation that the cursor is "armed" over the button creates a tiny but cumulative trust deficit.  
\- The most damaging effect is comparative: the user has just left Mail or Safari or Keynote, each of which responds richly to the pointer, and your app responds not at all. The contrast is felt as "this isn't really an iPad app — this is a website."  
\- It is, in fact, the single fastest way to break the native illusion. Apple's Pointing devices page is unusually firm on this: "people quickly become accustomed to the content effects they see throughout the system and generally expect their experience to apply to every app they use."

For your project, this means pointer effects are not polish — they are a baseline requirement. The minimum implementation: Hover effect on every CTA (tint \+ 1.03× scale \+ subtle shadow), Hover effect on every card (tint \+ 1.02× scale), Highlight effect on every small icon button (translucent rounded-rect background), default circle pointer everywhere else, I-beam over any text input. With these in place, the experience reads as iPad-native to trackpad users; without them, it does not, regardless of how beautiful the still frames are.

\---

That completes the spec. The corrections to flag from the earlier portion: the touch-target minimum per HIG's Accessibility page is \*\*44×44 pt default, 28×28 pt absolute floor\*\* (not 44×44 as the minimum), and the pointer hit-region padding from the Pointing devices page is confirmed as \*\*12 pt with bezel, 24 pt without\*\* — both numbers Apple-published.  
