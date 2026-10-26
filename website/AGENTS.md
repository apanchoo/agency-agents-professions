# Website contribution guidance

Keep the interface and documentation in English. The live library is the primary
entry point for discovering agents and companion skills.
Describe the product explicitly as an AI agent library. Present France Travail
as the source of occupational data in the site introduction, keeping source
attribution separate from agent instructions. Avoid em dashes in interface prose.

## Reading and accessibility

Use the French [RGAA criteria](https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/)
when changing interface behavior or presentation, especially criteria 3.2, 7.1,
10.4, 10.7, 10.11 and 10.12.

- Preserve the project's default reading scale: 18px prose and at least 16px for
  interface labels and metadata at standard browser settings. These are design
  choices, not a minimum font size mandated by the RGAA.
- Use relative font units and respect browser text preferences. Do not make the
  text smaller on mobile. Limit reading width and provide generous line spacing.
- Maintain text contrast of at least 4.5:1 on the actual background. Keep control
  boundaries and focus indicators distinguishable. Never use color alone to
  identify links or selected controls.
- Preserve content and actions at 200% text enlargement and 320px viewport width.
  Let text, filters, buttons and toolbars wrap. Do not truncate descriptions or
  hide informative landing-page content to make a layout fit.
- Keep keyboard focus visible. Use native controls, accessible names and proper
  dialog/tab semantics. Tabs support arrows, Home and End; closing a dialog
  restores focus to its trigger.
- Keep text readable with increased line, paragraph, letter and word spacing.
  Respect reduced motion and forced color preferences.
- Use the shared `Icon` SVG component for interface icons, including navigation
  and actions. Keep the same stroke style; do not substitute emojis. Decorative
  icons stay hidden from assistive technology and never replace visible labels.

The automated browser suite checks selected typography, contrast, reflow,
enlargement and keyboard regressions. It is not a complete RGAA audit: do not claim
full conformance from these tests alone.

## Verification and delivery

Run `npm test`, `npm run build` and `npm run test:e2e` for relevant code changes.
Inspect the desktop and mobile screenshots retained by the Website workflow.
Publishing uses GitHub Pages through `.github/workflows/site.yml`.

Render catalog Markdown as inert content; keep raw HTML disabled. Keep dependency
updates compatible with the production build and the browser tests.
