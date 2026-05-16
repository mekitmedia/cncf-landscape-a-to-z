## 2025-10-25 - Skip Link Implementation
**Learning:** Adding a "Skip to main content" link requires not just the link itself but ensuring the target `<main>` element has `tabindex="-1"` and a matching ID. This is critical for reliable focus management, especially in Single Page Applications or frameworks where the route might not refresh the page, but even in static sites it ensures the focus moves correctly for screen readers.
**Action:** When adding skip links, always verify the target container exists on *every* page template and has the correct ID and tabindex.

## 2026-02-04 - Semantic Navigation vs JS Buttons
**Learning:** Using `<button>` elements with `onclick` handlers for navigation breaks standard browser features (open in new tab, copy link) and accessibility semantics. Even in a dashboard-like UI, if the action is navigation to a new URL, always use `<a>` tags.
**Action:** When working with JS-generated lists (like alphabets or pagination), prefer generating `<a>` tags with computed `href` attributes over buttons with click handlers, even if visual styling mimics buttons.
## 2025-03-14 - Keyboard Accessibility & Tooltips for Icon-only Buttons
**Learning:** Found that icon-only buttons lacked hover text (`title`) and `focus-visible` styles which are critical for screen reader users and keyboard navigation. Using Tailwind's `focus-visible:ring-2 focus-visible:outline-none` pattern prevents default outline rings and uses theme colors efficiently, ensuring it only triggers on keyboard focus.
**Action:** Always verify keyboard navigation (Tab through the page) and add `focus-visible` to custom styled buttons and links, especially icon-only buttons.

## 2025-05-18 - Standardized Empty States
**Learning:** Found that empty states in the UI (like missing tool data or missing categories) lacked helpful design and guidance, just showing plain unstyled text. A standard Tailwind empty state pattern (using `bg-slate-50`, dashed borders `border-2 border-dashed border-slate-200`, and a Lucide icon like `inbox`) provides better visual feedback that the area is intentionally empty but part of the application structure, not broken.
**Action:** Always use the standard Tailwind empty state block design rather than unstyled text when rendering fallback content for missing data in lists or grids.
