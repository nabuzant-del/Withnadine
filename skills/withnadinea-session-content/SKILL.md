---
name: withnadinea-session-content
description: Turns Nadine's (@withnadinea, مع نادين) coaching session transcripts from Fireflies into Instagram content — reel angles and 6–8 Arabic reel scripts with a shooting sheet PDF and reel covers, plus carousel angles with the top 3 rendered as on-brand PNG carousels and captions. Runs Mohammad's Client Session Repurposing Agent with Nadine's adaptation layer and renders everything through the withnadinea-brand skill. Triggers "reels from today's session", "carousels from this week's sessions", "content from my session with…", "ريلز", "كاروسيل من الجلسة", "run all three".
---

# @withnadinea — Session → Reels + Carousels

You turn one session (or a week of sessions) into drafts Nadine can post: **reel scripts to film** and **carousels ready to post**. Everything visual is rendered by the **`withnadinea-brand`** skill, so it has to be installed as well. Read its `SKILL.md` §2 (carousel selector) and `references/voice.md` before writing copy.

Files in this skill:
- `references/adaptation.md` — **read first.** Safety gate, language, CTA, reel rules, two-part output. It overrides the agent.
- `references/repurposing-agent.md` — Mohammad's agent, verbatim (stages 1–4, quality filter, output order).
- `references/method.md` — the method in Nadine's words, and **METHOD_NAME**.
- `references/pack-format.md` — the `pack.json` you write, and how agent storyboards map to the 9 carousel types.
- `scripts/build_pack.py` — checks the pack (consent, care flag, 8-word quotes, names, claims, CTAs, lengths) and renders it.
- `examples/sample_pack.json` + `examples/sample_transcript.txt` — a full worked example (fictional session).

## 1. Get the transcript (Fireflies connector)
1. Work out which session(s) Nadine means:
   - "today's session with Reem" → `fireflies_search` with `keyword:"Reem" from:<today> limit:5`, or `fireflies_get_transcripts` with `fromDate` = today and `mine: true`.
   - "this week's sessions" → `fireflies_get_transcripts` with `fromDate` = this Monday, `mine: true`. Skip anything that isn't a client session (calls with Mohammad, admin, podcasts). If unsure, list titles and dates and ask which ones.
   - Nothing said → the most recent meeting with a non-Nadine participant.
2. `fireflies_get_transcript` for each id. Save it to `transcript.txt` as one `Speaker: words` line per sentence (keep Fireflies' `[mm:ss]` prefixes; the script handles them).
3. Note the client's speaker label and every name used for her (Arabic and Latin spellings). You need them for `--client`.
4. If the connector fails, ask Nadine to paste the transcript or upload the file. Everything else stays the same.

## 2. Safety gate (adaptation.md §1) — before reading for content
Consent in the first minutes? Any care-flag content? If no consent or a care flag: stop, tell Nadine in one line, produce nothing from that session. Otherwise continue with composites only.

## 3. Run the agent, adapted
Follow `repurposing-agent.md` stages 1–4 in order with `adaptation.md` applied:
1. Session content map + client character (composite: change age, city, job, family).
2. Angle bank (A Coach POV · B Coach philosophy · C Client story · D Client × method) → pick the 3–4 strongest, genuinely different.
3. **Reels:** 2 Arabic scripts per angle, 55–85 spoken words, beats hook → context → problem → emotion → turn → insight → closing → CTA. Each with hook type, `on_screen` overlays, `takeaway_en`, and a reel cover on the stronger script of each angle.
4. **Carousels:** return to the transcript. Carousel angle bank (3–6), pick the top 3, choose each one's type with the brand selector, map the storyboard with `pack-format.md` §3, write the caption. Write visual directions and image prompts (Part 2 only, Phase 1.5).
5. Run the agent's quality filter. Is there tension? Is it specific? Is the client the character? Is anything invented? If so, rewrite.

## 4. Build
Write `pack.json` (`pack-format.md` §1), then:
```bash
python scripts/build_pack.py pack.json out/ --transcript transcript.txt --client "<speaker label>" --client "<name>" --client "<Arabic name>"
```
- `ERROR:` means nothing renders. Fix the copy (usually a paraphrase or a name) and run it again.
- `WARN:` and `QA:` lines: fix them and run again. Shorten words; never shrink the design.
- Open every `*_preview.png` and at least one reel cover. If text looks cramped, cut words and rebuild.

## 5. Deliver in two parts (same chat)
**Part 1: ready to use**
- `shooting_sheet.pdf` (all scripts, for filming on her phone) and the reel covers
- The 3 carousels: PNGs in posting order, the preview, and the caption as text under each
- Each reel script as text: hook · script · CTA · on-screen lines

**Part 2: the thinking** (next message, skimmable): session content map · client character · angle bank · carousel angle bank · visual directions · image prompts · unused gold.

End Part 1 with one line: "Drafts only. Check every detail is changed enough that she wouldn't recognise herself."

## Rules that never bend
- Arabic first, flat Levantine, feminine address. English secondary.
- Always one CTA: «اعرفي أكتر عن الطريقة» or «احجزي جلسة معي», both "الرابط بالبايو", both to Stan.
- Composites only · no client quote over 8 words · no names · nothing from a non-consenting or care-flagged session · no faces, voices or screenshots of clients.
- No therapy/cure/guarantee/timelines/diagnoses/medication/religious rulings. Coaching, not therapy.
- Name the skill ("المهارة ٤ من ٦"), don't teach the whole method. Use METHOD_NAME from `method.md`.
- The client is the character; Nadine is the guide, not the hero.
- Never invent dialogue, emotions, outcomes or method steps the transcript doesn't support.
