---
version: alpha
name: AZ-branding-guide
description: AZ is an AI creative technology brand positioned for "forward thinkers and cultural creators." The identity pairs a bold geometric sans wordmark with a single recurring visual signature — a classical marble bust rendered in cobalt blue with a cloud/sky photographic texture — set against a cool cloud-white and sky-blue palette. This guide compiles the full brand board (logo system, color, typography, components, mockups, messaging) into a reusable reference for building reports, decks, and presentation templates.

colors:
  cloud-white: "#F7F8FA"
  sky-blue: "#7DB7FF"
  deep-cobalt: "#0A46FF"
  soft-gray: "#E6E8EC"
  ink-black: "#0B0B0D"

typography:
  font-family: DM Sans
  weights:
    light: 300
    regular: 400
    medium: 500
    bold: 700
---

## Overview

AZ positions itself as **"AI creative technology for forward thinkers and cultural creators"** — a studio-grade AI product brand aimed at designers, artists, and cultural innovators rather than generic enterprise SaaS. The tagline that anchors nearly every surface is the two-line contrast statement: *"Intelligent tools. Human imagination."*

The brand's single most recognizable device is a **classical marble bust rendered in cobalt blue, textured with photographic clouds** — a literal fusion of "intelligence" (classical sculpture, the historical seat of thought) and "imagination" (sky, atmosphere, the intangible). This bust image recurs across the app icon, editorial poster, landing page, product cards, packaging, stickers, tote bag, and motion exploration — functioning the way the "sunset stripe" functions for other brands: as the unmistakable continuity signature.

Wordmark and lockups use a short two-letter mark, **"AZ,"** set in a bold geometric grotesque (DM Sans Bold), always uppercase, sometimes in solid black, sometimes in deep cobalt blue, sometimes reversed white-on-blue or white-on-black.

**Key Characteristics:**
- Cobalt-blue marble bust + cloud photography as the singular brand signature image
- Two-letter wordmark "AZ" in DM Sans Bold, rendered in black, cobalt blue, or white
- Cool, restrained palette: cloud white, sky blue, deep cobalt, soft gray, ink black — no warm accents
- DM Sans as the sole typeface across every weight (Light → Bold), no secondary/display face
- Editorial, minimal layouts with large single-column headlines ("Dream in code.", "Create without boundaries.")
- Applies consistently across brand touchpoints: app icon, web, product cards, packaging, stickers, patterns, apparel, motion, photography

## Colors

> Source: brand board sections 01–16 (logo explorations, wordmark, app icons, editorial poster, landing page fragment, product cards, color palette, typography, interface snippet, packaging concept, sticker system, pattern system, branded mockups, motion graphic exploration, photography direction, key messaging).

### Palette

| Token | Hex | Role |
|---|---|---|
| `{colors.cloud-white}` | `#F7F8FA` | Primary light background / page canvas |
| `{colors.sky-blue}` | `#7DB7FF` | Secondary accent, gradients, lighter cloud/sky tones |
| `{colors.deep-cobalt}` | `#0A46FF` | Primary brand color — CTAs, active wordmark, "AZ Motion" card, primary buttons |
| `{colors.soft-gray}` | `#E6E8EC` | Neutral surface, secondary card backgrounds |
| `{colors.ink-black}` | `#0B0B0D` | Primary text, "AZ Voice" card, dark app icon, dark UI chrome |

### Usage Notes
- **Deep Cobalt** is the true "brand color" — reserved for the most prominent CTA-style surface in a layout (see `card-feature-brand` below) and for the wordmark when it needs to read as "active" or "digital."
- **Cloud White** and **Soft Gray** carry nearly all page backgrounds; the brand deliberately avoids saturated backgrounds outside of the cobalt accent card and the bust imagery itself.
- **Ink Black** is used both as a text color and as a full surface color (dark app icon variant, "AZ Voice" card) — it should read as a true near-black, not a warm charcoal.
- No warm hues (orange, yellow, red) appear anywhere in the system — this is a deliberately "cool" identity, the inverse of a sunset-toned brand.

## Typography

### Font Family
**DM Sans** — the sole typeface for the entire system, spanning Light, Regular, Medium, and Bold weights. No serif or display counterpart is used; hierarchy is built entirely through weight and scale rather than typeface contrast.

### Weight Usage

| Weight | Typical Use |
|---|---|
| Light | Long-form body copy, secondary descriptions |
| Regular | Standard body text, UI labels, navigation |
| Medium | Subheadings, card titles, interface labels |
| Bold | Wordmark, hero headlines, large editorial statements ("Dream in code.") |

### Principles
- **Single-family system** — hierarchy comes from weight and size only, keeping the voice consistent and unfussy across product UI and marketing surfaces alike.
- **Large, confident headline scale** — editorial statements ("Create without boundaries.", "Dream in code.") are set at a size that dominates the layout, echoing the bust imagery's scale.
- **Lowercase sentence-case body copy** paired with an all-caps two-letter wordmark creates a clear type-hierarchy contrast between brand mark and message.

## Layout

### Grid & Composition
- Marketing surfaces (editorial poster, landing page) favor a strong **left-aligned headline block** with generous negative space and the bust/cloud image occupying the opposite or lower portion of the frame.
- Product cards use a consistent **3-up grid**: one neutral/white card, one cobalt-accent "featured" card, one ink-black card — establishing a repeatable rhythm for showcasing sub-products (AZ Studio / AZ Motion / AZ Voice).
- Interface snippets follow a **two-pane workspace layout**: left control rail (model selector, prompt field), right output/preview pane.
- Packaging and apparel mockups reuse the same bust image at consistent crop and scale regardless of substrate (box, tote, poster, phone case).

### Whitespace Philosophy
The system leans on large areas of flat cloud-white or soft-gray space around a single, large photographic/sculptural focal point — restraint and negative space are what make the recurring bust image land with impact rather than clutter.

## Shapes & Iconography

- **App icon**: rounded-square (iOS-style superellipse) container, either filled with the cloud-photograph crop, solid ink black, or cloud white with cobalt wordmark — four icon variants shown, all sharing the same corner radius.
- **Sticker / pattern system**: circular badges and organic blob shapes in cobalt, ink black, sky blue, and cloud-texture fills — the circle is the system's secondary geometric motif alongside the bust silhouette.
- **Cards & panels**: soft-rounded rectangular cards (consistent with modern SaaS product-card conventions), no pill-shaped buttons observed.

## Components

### Logo Lockups
**`logo-mark`** — Two-letter "AZ" set in DM Sans Bold, uppercase, no descenders. Appears in five treatments: solid black-on-white, solid cobalt-on-white, white-on-cobalt (reversed), white-on-black (reversed), and cobalt-on-soft-gray.

**`wordmark-full`** — Large-scale standalone "AZ" mark paired with a two-line descriptor beneath it (e.g., "Intelligent tools / for creative minds."), typeset in DM Sans Bold at hero scale, DM Sans Regular for the descriptor.

**`app-icon`** — Rounded-square icon, four variants:
1. Cloud-photograph fill + white "AZ" wordmark
2. Sky-blue-tinted cloud fill + white "AZ" wordmark
3. Solid ink-black fill + white "AZ" wordmark
4. Cloud-white fill (bordered) + cobalt "AZ" wordmark

### Cards

**`card-feature-neutral`** — White/cloud background, bust-and-cloud photographic header, product name in Medium weight, short one-line description, arrow affordance for "learn more." Used for e.g. "AZ Studio."

**`card-feature-brand`** — Identical structure to `card-feature-neutral` but on a **deep cobalt** background with white text — reserved for the product the layout wants to foreground (e.g., "AZ Motion").

**`card-feature-dark`** — Identical structure on an **ink-black** background with white text (e.g., "AZ Voice").

### Interface Snippet

**`product-ui-panel`** — Two-pane workspace: left rail with model dropdown ("AZ 1.0 — Creative") and a prompt textarea ("Describe your vision…"); right pane shows a generated output thumbnail with a scrub/playback bar. UI chrome uses soft-gray borders on a white canvas — this is the only surface where the brand shows its literal product (a generative visual tool).

### Packaging & Merchandise

**`packaging-box`** — White retail box, cobalt "AZ" wordmark top-left, vertical tagline running up the left edge ("Intelligent tools for creative minds."), full-bleed bust-and-cloud photograph across the right two-thirds, sub-label "AZ Studio — Creative AI Suite" bottom-right.

**`tote-bag` / `phone-mockup` / `poster-mockup`** — All reuse the identical bust crop at consistent scale, proving the image functions as a portable brand asset independent of substrate.

### Stickers & Pattern System

**`sticker-set`** — Mixed circular and rectangular stickers: cobalt-outlined "AZ" roundel, cropped bust portrait die-cut, cobalt speech-bubble-style tag ("Dream in code."), ink-black tag ("Create without boundaries."), plain "AZ" tile, and a cloud-texture circle.

**`pattern-tile`** — Abstract circular/organic shapes in cobalt, ink black, sky blue, cloud-white, and cloud-photo fills, arranged as a loose decorative grid for backgrounds and section dividers.

### Motion & Photography Direction

**`motion-sequence`** — The bust rotates through profile angles (front, three-quarter, side) before dissolving into pure cloud formations — establishing a visual grammar of "sculpture becomes sky."

**`photography-direction`** — Supporting photography stays within the same restrained blue/white/gray register: literal sky and cloud photographs, the bust in isolation, and a single human silhouette dwarfed by a floating cloud-sphere — reinforcing scale and atmosphere rather than literal product screenshots.

## Key Messaging

| Use | Copy |
|---|---|
| Primary tagline | "Intelligent tools. Human imagination." |
| Positioning line | "AI creative technology for forward thinkers and cultural creators." |
| Hero headline (landing) | "Create without boundaries." |
| Hero headline (poster) | "Dream in code." |
| Supporting line | "Built for creators. Designed for culture. Shaped by tomorrow." |
| Product descriptors | "Generative canvas for limitless ideas." (Studio) · "AI motion design made effortless." (Motion) · "Voice AI for human expression." (Voice) |

**Voice principles:**
- Short, declarative, two-to-four-word fragments rather than full marketing sentences ("Dream in code.")
- Always pairs an abstract/poetic line with one plain-spoken functional line — never poetic alone, never purely technical alone
- Consistently frames AI capability as in service of human creativity, never as a replacement for it

## Do's and Don'ts

### Do
- Reuse the cobalt-bust-with-clouds image (or a clear extension of it) as the anchor visual on any new surface — it is this brand's single strongest recognition asset
- Keep the palette restricted to cloud white, sky blue, deep cobalt, soft gray, and ink black
- Set the wordmark only in DM Sans Bold, uppercase, never condensed or italicized
- Pair one poetic headline with one plain functional line in any hero or card copy
- Use the cobalt-accent card as the single "featured" element in any 3-up card grid — never make more than one card cobalt at a time

### Don't
- Don't introduce warm accent colors (orange, yellow, red, green) anywhere in the system
- Don't substitute the bust/cloud image with generic stock photography or abstract gradients — it will break brand recognition
- Don't mix in a second typeface for contrast; hierarchy comes from DM Sans weight alone
- Don't use pill-shaped primary buttons; the system's card and icon corners are softly rounded but not fully circular
- Don't crowd the bust image with dense text overlays — it needs the same generous negative space seen throughout the board

## Using This Guide for Reports & Presentations

- **Slide/report backgrounds**: default to Cloud White or Soft Gray; reserve Deep Cobalt for a single accent slide or section divider, mirroring the "one cobalt card per grid" rule above.
- **Cover slides**: lead with the bust-and-cloud image full-bleed or cropped, wordmark top-left, tagline set in DM Sans Bold beneath it.
- **Section headers**: use the "Dream in code." style — a short declarative fragment, large DM Sans Bold, left-aligned, generous whitespace above and below.
- **Data/insight callouts**: house key figures inside a `card-feature-brand`-style cobalt panel to draw the eye, exactly as the product cards foreground "AZ Motion."
- **Footers/closing slides**: end on the key-messaging pairing (poetic line + functional line), plain "AZ" wordmark, no additional ornamentation.

## Known Gaps

- No dark-mode palette is shown beyond the single ink-black card/icon variant; a full dark-surface system would need to be extrapolated.
- Exact DM Sans point sizes and line-height values are not visible on the board and would need to be defined for a production type scale.
- Animation/transition timing for the motion sequence is not specified; recommend a slow, atmospheric 400–600ms ease consistent with the "cloud" motif rather than snappy UI-standard timing.
- No explicit accessibility/contrast documentation is shown for text-on-cobalt or text-on-cloud combinations; verify contrast ratios before production use.
