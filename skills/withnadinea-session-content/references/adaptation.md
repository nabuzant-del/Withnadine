# Nadine adaptation layer (overrides the agent where they differ)

## 1. Safety gate (runs before anything else, overrides everything)
- **Consent.** Look in the first minutes of the transcript for Nadine asking to transcribe and the client agreeing. If the client said no, or hesitated and Nadine agreed to stop: **stop. Produce nothing.** Tell Nadine in one line.
  If there is no consent moment at all: ask Nadine "Did [first name] agree to transcription?" before continuing.
- **Care flag.** If the client mentions self-harm, suicide, harm to or from someone, abuse, or a medical crisis: **stop. Produce no content from this session.** Tell Nadine in one line and point her to the summary skill (it carries the flag in her private notes).
- **Composites only.** Change name, age, city, job, number and ages of children, and family details. Where possible merge with another session from the same week. Never keep a detail that would let the client, her family or her friends recognise her.
- **No quote from the client longer than 8 words.** Paraphrase everything else. `build_pack.py --transcript` checks this.
- **No names.** Never the client's name, anyone she names, her employer, her city.
- **No claims.** No therapy, cure, heal/شفاء/علاج, guaranteed/مضمون, "reclaim your life", no timelines ("in 30 days"), no diagnoses (depression, anxiety disorder, ADHD, trauma as a label), no medication, no religious rulings.
- **Teach the name, not the method.** Name the skill by number ("المهارة ٢ من ٦") and give one small thing to try. The full method stays in the session.
- Nadine reviews everything before posting. You produce drafts; she decides.

## 2. Language
- Arabic is the main language, **flat Levantine**, feminine address (إنتِ). Not fusha, not heavy dialect: how an educated Ammani or Beiruti woman talks on camera.
- English is secondary: each reel gets a one-line English takeaway (`takeaway_en`); carousels render in Arabic with an optional short English line under statements/quotes. Full English only if Nadine asks.
- Write it in Arabic first. Never write English and translate.

## 3. Method name
Everywhere the agent says "The Six Time Zone Method", use METHOD_NAME from `method.md`. In Arabic content say «الطريقة» or «المناطق الزمنية الثلاث». The six are **skills**, not zones. Never invent steps beyond `method.md`.

## 4. CTA (overrides the agent's "avoid sales CTAs")
Every reel ends with the closing line **then one CTA**, rotating between the two. Every carousel ends with a `cta` slide.
- `method` → «اعرفي أكتر عن الطريقة — الرابط بالبايو» (Know more about the method)
- `book` → «احجزي جلسة معي — الرابط بالبايو» (Book a session with me)
Both land on the Stan page. Use `method` for story and philosophy pieces, `book` for diagnostic and client-story pieces; keep the set balanced.

## 5. Reels
- 20–30 seconds, **55–85 spoken words** (the CTA line is not counted).
- Beats: hook → context → problem → emotional layer → turn → insight → closing line → CTA.
- 3–4 selected angles × 2 scripts each = 6–8 scripts. The two scripts differ in hook type, starting point and framing.
- Per script also give: `on_screen` (the 2–3 short text overlays, ≤ 6 words each), and a reel cover (`line1` ≤ 44 chars, `line2` the key phrase ≤ 28 chars).
- Written to be spoken: short sentences, one breath each, one line per breath in the script.

## 6. Carousels
- Carousel angle bank of 3–6 → **render the top 3**.
- Every storyboard is mapped to one of the brand's 9 carousel types with the selector in `withnadinea-brand/SKILL.md` §2. The agent's 7-slide structure maps onto the type's recipe (`pack-format.md` §3). Do not stretch a weak idea to 7 slides.
- Phase 1 is typographic: the agent's visual directions and image prompts are still written (Part 2) and saved in the pack as `image_prompts`, for Phase 1.5. They are not rendered.
- Caption per carousel: Arabic, 2–4 short lines, one English line, CTA line, 5–8 hashtags (mixed Arabic and English).

## 7. Output on mobile — two parts, same chat
**Part 1 (ready to use):** the shooting sheet PDF, reel covers, the 3 rendered carousels with captions, and each reel script as text.
**Part 2 (the thinking):** session content map, client character (composite), angle bank, carousel angle bank, visual directions, image prompts, unused gold.
Send Part 1, then Part 2 in the next message. Keep Part 2 skimmable.
