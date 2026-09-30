# Writing the client summary

## Language order
Put her language first in `languages`.
1. If she spoke one language for more than about 60% of the session, that language comes first.
2. Otherwise, use the language she writes her emails in.
3. If neither settles it, Arabic comes first.

Write both sections natively. The Arabic is flat Levantine with feminine address (إنتِ). The English is plain and warm, with no coaching jargon. Each should read as if it was written in that language first.

## Fields (both `sections.ar` and `sections.en`)
| Field | What to write | Length |
|---|---|---|
| `where_you_stand.title` | The time zone she mostly lives in, plainly: «عايشة بالماضي» / "Living in the past". | ≤ 5 words |
| `where_you_stand.body` | Why, drawn from what she said. End with a normalising line, e.g. "You're not broken, an old pattern is running." | 2–3 sentences |
| `uncovered` | 3–4 key moments from the session in her own terms. A short phrase of hers is fine; nothing long. | ≤ 20 words each |
| `recommendations` | Exactly 3, practical, each `{text, skill}` with skill 1–6. | ≤ 30 words each |
| `this_week` | One small practice: what, when, and what to notice. | 1–2 sentences |
| `journal_prompts` | Exactly 3 questions, in first person ("What…", «شو…»). | ≤ 12 words each |
| `next_step` | "When you're ready for the next time zone" → link in bio / Stan. Use what Nadine said about the next session if she said something. | 1 sentence |

Top level:
- `client_first_name`: as she writes it.
- `date`: display form, e.g. "22 Sep 2026".
- `zone`: `past`, `present` or `future`.
- `focus_skills`: the 1–3 skills that matter most for her.
- `languages`: `["ar","en"]` or `["en","ar"]`.
- `name`: leave it out; the script sets it.

## Sources
- The PDF is built from the **session**. Emails only give you her name, her language and her stated hopes. You can echo a hope she wrote ("You came wanting…") without quoting the email.
- Do not invent moments, feelings or results. If the transcript doesn't support it, leave it out.
- Recommendations come from what Nadine actually suggested in the session first. Fill any remaining places from the skill she needs most, kept small.

## Tone
Nadine speaks as a direct, warm older sister who has done the work. She validates family and cultural reality and never tells her to leave, confront or cut anyone off. She doesn't pathologise.
Banned: therapy/علاج, cure/شفاء, guaranteed/مضمون, diagnoses (depression, anxiety disorder, ADHD, trauma as a label), medication, religious rulings, "in X days", and "reclaim your life".

## Checks (the script runs these)
- First name only.
- Both languages are present, and the order matches her language.
- 3–4 uncovered, 3 recommendations each tied to a skill number, 3 journal prompts.
- No banned words.
- No `--private` term appears anywhere.
