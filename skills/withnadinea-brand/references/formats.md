# Formats

| Type | Size | Spec `type` | Example |
|---|---|---|---|
| Carousel | 1080×1350 (4:5) | `carousel` | examples/01–09 |
| Single post | 1080×1350 | `post` (one slide) | examples/10 |
| Reel cover / thumbnail | 1080×1920 (9:16) | `reel_cover` | examples/11 |
| Story | 1080×1920 | `story` | examples/12 |
| Highlight covers | 1080×1920 | `highlights` | examples/13 |
| Client session summary | A4 PDF, bilingual | `client_summary` | examples/14 |
| Reel shooting sheet | A4 PDF | `shooting_sheet` | examples/15 |

## Safe areas
- **Feed (4:5):** 80 px margins on every side. This also keeps content inside the profile-grid crop (3:4).
- **Reels / stories (9:16):** no text in the top 250 px (UI) or bottom 440 px (caption + buttons); nothing important in the right 140 px (buttons). Keep the hook inside the profile-grid crop, y 240 → 1680. The renderer positions everything inside these zones.

## Reel cover (`reel_cover`)
Fields: `line1` (white subtitle line, ≤ 44 chars), `line2` (the key phrase in mustard, ≤ 28 chars), `zone`, `image` (optional path to a frame from Nadine's video), `speaker`, `role`.
Without an image it renders a dark spotlight cover with the zone shape — use that when she hasn't filmed yet.

## Story (`story`)
`slides: [{text, sub, hl, zone}]`. For questions, polls or prompts; add the sticker in Instagram after.

## Highlights (`highlights`)
`items: [{zone, label} | {skill, label}]`. Standard set: الماضي · الحاضر · المستقبل · مهارة ١–٦ · عن نادين · جلسات.

## Client summary (`client_summary`)
Two A4 pages per language (4 pages total): page A = where you stand, six skills, uncovered, recommendations; page B = this week, journal prompts with writing lines, next step.
`client_first_name`, `date`, `zone`, `focus_skills` [n…], `languages` [first, second], and `sections.{ar,en}` each with: `where_you_stand {title, body}`, `uncovered` [3–4], `recommendations` [{text, skill}] ×3, `this_week`, `journal_prompts` [3], `next_step`. First name only. Nothing from a care flag.

## Shooting sheet (`shooting_sheet`)
`date`, `reels: [{angle, hook_type, hook, script, cta, takeaway_en}]`. Used by the reels skill.

## Images
Phase 1 is typographic. When an image is wanted:
- **Photo layout:** `{"layout":"photo","image":"path.jpg","title":"…"}` — the engine adds the brand tint, gradient and grain.
- **Image-generation prompt recipe** (write one per slide that needs an image):
  `Editorial photograph, [subject], [environment], [action], [camera angle + lens], soft natural light, warm muted palette of cream, terracotta, dusty blue and mustard, film grain, calm and intimate mood, negative space on the [side] for text, no text, no logos, 4:5 aspect ratio, consistent with the rest of the set.`
- Subjects: hands, kitchens, windows, tea, notebooks, doorways, walking — women seen from behind or in partial frame. No stock "business" gestures, no identifiable faces for client stories.
