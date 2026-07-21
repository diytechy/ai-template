---
domains: [web]
researched: 2026-07-09
source: curated from a private research library
---
# UI & design systems

Curated research pack imported from the staged skill/knowledge library. Verify version-sensitive examples against the linked current documentation before shipping.

### Core references
- **[shadcn/ui](https://ui.shadcn.com)** — copy-paste, you-own-the-code components on headless
  primitives + Tailwind, zero runtime dependency. The de-facto 2026 default for custom React design
  systems. Note the **[July 2026 switch to Base UI as the default primitive layer](https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default)** (Radix still shipped in parallel).
- **[Radix Primitives](https://www.radix-ui.com/primitives)** and **[Base UI](https://base-ui.com/)** —
  the headless (behavior + a11y, no styles) layer underneath. Focus management, keyboard nav, ARIA
  roles, scroll-locking done for you.
- **[W3C WAI-ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/)** — the
  authoritative source for *how each widget should behave* (roles, states, keyboard interaction).
  This is the spec headless libraries implement; read it when a component is custom.
- **[Radix Colors](https://www.radix-ui.com/colors)** + **[W3C Design Tokens format](https://tr.designtokens.org/format/)** — a perceptual color scale and the interchange format for tokenized design values.
- **[Tailwind CSS](https://tailwindcss.com/docs)** — utility styling; pairs with the above.

### Actionable techniques
1. **Headless-first, tokens-first.** Never hand-roll interactive widgets (menus, dialogs, comboboxes).
   Take behavior + a11y from a headless primitive, style it with tokens. This is the single biggest
   quality lever for an LLM agent building UI: it can't forget focus-trapping if it never wrote it.
2. **Design tokens as the single source of truth.** Put color/space/radii/type in one `tokens`
   file with provenance, and *derive* component styles. (A design-system project's
   provenance-stamped `tokens.yaml` is a good worked example.) Changing "primary" in one place must cascade.
3. **Accessibility acceptance checklist** (make it a test, not a vibe): keyboard-operable with no
   mouse; visible focus ring; `aria-*` matches the APG pattern; color contrast ≥ 4.5:1 body / 3:1
   large; respects `prefers-reduced-motion` and `prefers-color-scheme`. Automate with axe-core.

```tsx
// Accessible dialog: behavior/a11y from the primitive, look from tokens — agent writes only content.
import { Dialog } from "@base-ui-components/react/dialog";
<Dialog.Root>
  <Dialog.Trigger className="btn-primary">Edit room</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Backdrop className="bg-[var(--overlay)]" />
    <Dialog.Popup className="p-[var(--space-4)] rounded-[var(--radius-2)]">
      <Dialog.Title>Room settings</Dialog.Title>
      {/* focus trap, Esc-to-close, ARIA all handled by the primitive */}
    </Dialog.Popup>
  </Dialog.Portal>
</Dialog.Root>
```

### Gotchas
- Copy-paste component libraries (shadcn) mean *you* own upgrades — pin a version/commit and track it.
- An LLM will happily invent ARIA attributes; hold it to the APG pattern for the specific widget.
