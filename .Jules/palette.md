## 2025-10-25 - Skip Link Implementation
**Learning:** Adding a "Skip to main content" link requires not just the link itself but ensuring the target `<main>` element has `tabindex="-1"` and a matching ID. This is critical for reliable focus management, especially in Single Page Applications or frameworks where the route might not refresh the page, but even in static sites it ensures the focus moves correctly for screen readers.
**Action:** When adding skip links, always verify the target container exists on *every* page template and has the correct ID and tabindex.

## 2026-02-04 - Semantic Navigation vs JS Buttons
**Learning:** Using `<button>` elements with `onclick` handlers for navigation breaks standard browser features (open in new tab, copy link) and accessibility semantics. Even in a dashboard-like UI, if the action is navigation to a new URL, always use `<a>` tags.
**Action:** When working with JS-generated lists (like alphabets or pagination), prefer generating `<a>` tags with computed `href` attributes over buttons with click handlers, even if visual styling mimics buttons.

## 2026-03-05 - Server-Side Generation for Static Navigation
**Learning:** Replacing client-side JavaScript list generation (e.g., alphabet navigation) with server-side templates (using Hugo's `range`, `seq`, and `printf "%c"`) significantly improves accessibility (no-JS support), SEO (crawlable links), and performance (no layout shift).
**Action:** Prioritize server-side loops for static or predictable navigation structures over client-side DOM manipulation.
