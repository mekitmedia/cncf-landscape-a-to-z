## 2025-10-25 - Skip Link Implementation
**Learning:** Adding a "Skip to main content" link requires not just the link itself but ensuring the target `<main>` element has `tabindex="-1"` and a matching ID. This is critical for reliable focus management, especially in Single Page Applications or frameworks where the route might not refresh the page, but even in static sites it ensures the focus moves correctly for screen readers.
**Action:** When adding skip links, always verify the target container exists on *every* page template and has the correct ID and tabindex.

## 2026-02-04 - Semantic Navigation vs JS Buttons
**Learning:** Using `<button>` elements with `onclick` handlers for navigation breaks standard browser features (open in new tab, copy link) and accessibility semantics. Even in a dashboard-like UI, if the action is navigation to a new URL, always use `<a>` tags.
**Action:** When working with JS-generated lists (like alphabets or pagination), prefer generating `<a>` tags with computed `href` attributes over buttons with click handlers, even if visual styling mimics buttons.

## 2026-02-12 - Critical Navigation & SSR
**Learning:** Client-side rendered navigation (e.g., JS-generated alphabet list) creates a jarring layout shift (CLS) and is inaccessible to users without JS or search engines. Moving this to server-side templates (Hugo `range`) improves perceived performance and accessibility significantly with minimal code.
**Action:** Always prefer server-side loops for static navigation elements like pagination or alphabetical indices.

## 2026-02-12 - Disabled State Semantics
**Learning:** For "future" or "locked" content links, using `<span>` with `aria-disabled="true"` and a `title` attribute is often better than a disabled `<button>` inside a navigation context, as it preserves the visual structure without implying interactivity that is temporarily broken. However, ensure the visual distinction is clear (e.g., cursor-not-allowed, greyed out).
**Action:** Use semantic `<span>` for locked navigation items instead of disabled buttons to avoid confusion about why a button is disabled.
