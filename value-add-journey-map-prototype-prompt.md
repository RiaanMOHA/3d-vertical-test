# Brief — embed the Ozu-1 value-add tour into Step 10

## Goal

In **Step 10 ("Investment properties")**, when the user taps the **Ozu-1 marker on the map**, open the existing Ozu-1 3D property tour as a full-screen embedded experience. When the tour completes, the user returns to the map. This brief is the only spec for that integration.

## The tour (read before doing anything)

- The tour is a self-contained HTML page already deployed at:
  **`https://3d-vertical-test.vercel.app/value-add-journey.html`**
- It runs three.js inside its own internal iframe and walks the user through 5 scenes: exterior → room 1 → kitchen → laundry → living + dining.
- It owns its own forward/back chevron nav, step dots, and step label. Do not try to replicate, override, restyle, or message-command any of those.
- It is mobile-first, assumes a pure black background, and renders edge-to-edge.
- When the user reaches the **final step (living + dining)** and taps the forward chevron, the page calls:
  ```js
  window.parent.postMessage({ type: 'journeyComplete' }, '*');
  ```
  and then stops. That `postMessage` is the only signal that the tour is done. There is no other completion event.
- The tour is served from a **different origin** (`https://3d-vertical-test.vercel.app`) than this project. `postMessage` works across origins; iframe DOM access does not. Treat the tour as a sealed black box.

## What to build

### 1. Wire the Ozu-1 marker tap

Locate the file in this project that renders Step 10's map and the Ozu-1 marker. Add a tap/click handler to that marker that calls `openValueAddTour()` (rename to match local conventions).

### 2. Mount the tour as a full-screen overlay

`openValueAddTour()` must:

- Create an `<iframe>` element with `src="https://3d-vertical-test.vercel.app/value-add-journey.html"`.
- Append the iframe to `document.body` (NOT to any map container — it must sit above all map and nav chrome).
- Apply these styles inline or via a class:
  ```css
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  border: none;
  background: #000;
  z-index: <higher than the highest existing z-index in this project>;
  ```
- Set `allow="autoplay; fullscreen; xr-spatial-tracking; accelerometer; gyroscope"` on the iframe so three.js / WebXR / device-orientation features are not blocked.
- Lock body scroll while the iframe is mounted (matching whatever scroll-lock convention this project already uses for modals; if there is no existing convention, set `document.documentElement.style.overflow = 'hidden'` and restore it on close).

### 3. Listen for the completion signal

Attach a `message` listener on `window`:

```js
function handleJourneyMessage(event) {
  if (event.origin !== 'https://3d-vertical-test.vercel.app') return;
  if (event.data?.type !== 'journeyComplete') return;
  closeValueAddTour();
}
window.addEventListener('message', handleJourneyMessage);
```

The origin check is **mandatory** — `postMessage` data must never be trusted without validating the sender's origin.

### 4. Close cleanly

`closeValueAddTour()` must:

- Call `iframe.remove()`. Do **NOT** hide it with `display: none` — the three.js renderer inside the iframe holds GPU memory until the iframe is fully unmounted.
- Remove the `message` listener: `window.removeEventListener('message', handleJourneyMessage)`.
- Restore body scroll.
- Restore focus to the Ozu-1 marker (or the map container) for keyboard accessibility.

### 5. Guard against double-open

If the user taps the Ozu-1 marker while the tour iframe is already in the DOM, do nothing. Track open state with a module-scoped boolean or by querying the DOM for an existing tour iframe before mounting a new one.

## Strict rules — non-negotiable

- **No close button.** Do not add an X, a "skip tour" link, a back-arrow, a swipe-to-dismiss gesture, an Esc-key handler, or any other early-exit affordance. The user must navigate forward through all 5 scenes. This is an intentional design decision.
- **No modification of the tour.** No injected CSS, no message commands sent INTO the iframe, no resizing to anything other than full viewport.
- **No new dependencies.** This integration needs only an iframe + a fixed-position container + a `message` listener. Do not pull in a modal library, an iframe library, or any wrapper component.
- **Full viewport coverage including safe areas** — no strip of map visible behind the iPhone notch or the home-indicator area.

## Design and code conventions

- **Mobile-first.** Verify on iPhone SE (375px wide), iPhone 16 Pro, iPad mini, and iPad Pro 12.9" viewports at minimum.
- **Sentence case** for any UI strings you add. No `text-transform: uppercase`. No ALL-CAPS labels.
- **No emojis** — not in UI, not in code comments, not in commit messages.
- Match the framework, file structure, naming, and state-management patterns already in this project. Do not introduce a new pattern.
- Plain semantic HTML for the overlay container.

## Environment constraints

- This project must be served from an HTTP dev server (vite / next / etc.), NOT opened as `file://`. The iframe loads ES modules and an HDR file from Vercel — `file://` will fail with cross-origin errors.
- The iframe needs internet access. With no network, the tour shows a blank black screen — this is expected.

## STOP — ask questions before writing code

You **must not write any code** until you have completed all six of the following:

1. **Read the existing Step 10 code.** Locate every file that renders Step 10, the map, and the Ozu-1 marker. Report back the file paths and a one-line summary of each file's role.
2. **Identify the stack.** Tell me: what map library is in use (Mapbox GL JS? Leaflet? Google Maps? Apple MapKit? custom canvas?), what UI framework (React / Vue / Svelte / vanilla?), and where step state lives (Zustand / Redux / Context / URL param / something else?).
3. **Ask about post-tour state.** When the user finishes the tour and returns to the map, should anything visually change? Should the Ozu-1 marker now show a "visited" state? Should the user be auto-advanced to Step 11? Should a checkmark appear on a card somewhere? I have not decided — ask me directly.
4. **Ask about scroll lock.** Does this project already have a scroll-lock convention for modals/overlays? If yes, point me to it and propose using the same one. If no, propose the simplest approach.
5. **Ask about analytics / telemetry.** Does this project track step entries or map marker taps? If yes, should I emit a `tour_opened` and `tour_completed` event? If yes, what is the event-emission API in this project?
6. **Propose an implementation plan** — a numbered list of file-by-file, change-by-change steps. Wait for my explicit approval before writing any code.

Only after I have answered questions 3–5 and approved the plan from step 6 may you begin coding.

Confirm you have read this entire brief, then begin with questions 1 and 2 (the file inventory and the stack identification).
