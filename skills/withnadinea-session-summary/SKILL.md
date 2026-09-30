---
name: withnadinea-session-summary
description: After one of Nadine's (@withnadinea, مع نادين) coaching sessions, pulls the transcript from Fireflies, identifies the client and her email from the meeting, reads that client's emails in Nadine's Gmail for context (name, language, what she hoped for, what was promised), then produces the bilingual branded client summary PDF (client's language first) through the withnadinea-brand skill, Nadine's private coaching notes, and a Gmail draft to the client that Nadine sends herself. Triggers "summary for Reem", "session summary", "ملخص الجلسة", "run all three on today's session".
---

# @withnadinea — Session Summary (client PDF + Nadine's private notes)

Two outputs from one session, and an optional email draft:
- **A. Client PDF:** a bilingual A4 summary the client keeps, in her language first. It is rendered by the **`withnadinea-brand`** skill (`client_summary` type), which has to be installed as well.
- **B. Private notes:** for Nadine only, as text in the chat. They are never sent and never go into the PDF.
- **C. Gmail draft** to the client. Nadine attaches the PDF and sends it. **Never send an email yourself.**

Files:
- `references/method.md`: the method, the six skills, the NEVER list, METHOD_NAME.
- `references/writing.md`: how to write each PDF section, choosing the language, the checks.
- `references/private-notes.md`: the notes template and the care-flag protocol.
- `references/gmail.md`: finding the client, searching Gmail, and the draft email templates.
- `scripts/build_summary.py`: checks the spec, then renders and names the PDF.
- `examples/`: a sample transcript, the matching summary spec, and sample private notes (all fictional).

## 1. Find the session (Fireflies connector)
- "Summary for Reem" → `fireflies_search` with `keyword:"Reem" limit:5` (add `from:<date>` if Nadine gives a day). No name given → `fireflies_get_transcripts` with `mine: true, limit: 5`, and pick the latest meeting that has a non-Nadine participant.
- If more than one meeting could match, list them (title, date) and ask which one.
- `fireflies_get_transcript` on the id. Keep the metadata: title, date, organizer, participants and attendee emails.
- If the connector fails, ask Nadine to paste the transcript and give the client's first name and email.

## 2. Identify the client
Take the participant emails and remove Nadine's (the organizer, and any address she uses), Fireflies and other bots, and Mohammad or anyone else from the team. One address left means that is the client. Zero or several: follow `gmail.md` §1 (Stan booking email, then ask Nadine). Get her **first name** as she writes it herself (her email signature or display name beats the Fireflies speaker label).

## 3. Read her emails (Gmail connector)
Follow `gmail.md` §2: `search_threads` for `from:<email> OR to:<email>`, then `get_thread` on the 3–5 most recent threads. Extract only:
- the first name she uses and the language she writes in
- what she said she wanted from the session (booking answers, first email)
- anything Nadine promised her by email
- practical details: next session booked or not, time zone
Emails **personalise**; they are never quoted in the PDF and never used for content. If Gmail isn't connected, skip this step and say so in the notes.

## 4. Safety first
Read the whole transcript. Check for consent and for any care flag (`private-notes.md` §2). A care flag goes at the top of the private notes and nowhere else. The PDF and the draft are still made, but they leave the topic out entirely. If the care flag is serious (risk to her or to someone else), hold the draft and tell Nadine to reach her personally first.

## 5. Write
1. **Private notes** (`private-notes.md` §1).
2. **The PDF spec** (`writing.md`). Write `summary.json`: `client_first_name`, `date`, `zone`, `focus_skills`, `languages` [her language, the other], and `sections.ar` and `sections.en`. Each language is written natively, never translated line by line.

## 6. Build
```bash
python scripts/build_summary.py summary.json out/ --iso 2026-09-22 --file-name Reem \
  --private "<surname>" --private "<care-flag words>" --private "<email-only detail>"
```
- `--private` terms must not appear in the PDF: her surname, other people's names, care-flag details, anything only known from email. Repeat the flag for each term.
- `ERROR:` blocks the render. `WARN:` means fix it and run again.
- Output: `out/<FileName>_Summary_<YYYY-MM-DD>.pdf`. Open page 1 and page 3 as images and check the Arabic joins right-to-left and nothing overflows.

## 7. Draft the email
`create_draft` to her address using the template in `gmail.md` §3, in her language first. Say in the chat: "Draft ready in Gmail. Attach the PDF and send when you're happy with it." If drafts aren't available, give the email text to copy.

## 8. Deliver (in this order)
1. Care flag line, if there is one.
2. The PDF file.
3. The private notes.
4. Draft status (or the email text).
Then one line: "Read the PDF once before it goes. It should sound like you."

## Rules that never bend
- First name only. No surname, no other people's names, no employer, no city.
- Nothing from a care flag in the PDF or the email.
- No diagnosis, no medication, no religious rulings, no promised outcomes or timelines. Coaching, not therapy.
- Every recommendation is tied to a skill number (1–6). Never teach the full method.
- Arabic is flat Levantine with feminine address; English is plain and warm.
- Never send email. Draft only.
