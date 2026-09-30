# Gmail: find her, read her, draft to her

## 1. Find the client's email
1. **Fireflies participants.** Take the meeting's participant/attendee emails and remove Nadine's addresses, anything with `fireflies`, `otter`, `noreply`, and team members. One address left: that is her.
2. **Stan booking email.** If no address is left, or more than one: `search_threads` with `"<first name>" (stan OR booking OR booked OR حجز) newer_than:60d`. Stan's booking notifications to Nadine include the customer's name and email, and any booking-form answers.
3. **Ask Nadine.** Still unsure? Ask: "What's [first name]'s email?" Never guess between two people.

## 2. Read her emails
- `search_threads` with query `from:<email> OR to:<email>` and `pageSize: 10`.
- Search results only preview the oldest messages, so use `get_thread` on the 3–5 most recent threads to read them in full.
- Extract into the private notes (never into the PDF):
  - the first name she signs with, and her language
  - what she hoped for or asked about before the session
  - anything Nadine promised (an exercise, a resource, a time)
  - logistics: next session booked? time zone? reschedules?
  - the tone: eager, hesitant, overwhelmed, practical
- Don't open attachments. Don't read threads that aren't with her. Don't carry email details into any content, ever.

## 3. The draft (`create_draft`)
- `to`: her email. Plain text `body` (no markdown).
- Subject and body: her language first, then the other, separated by a blank line and `—`.
- It says the PDF is attached. Nadine attaches it in Gmail before sending.
- If Nadine promised something by email or in the session, mention it in one line.
- **Never** call send. **Never** make a draft for a care-flagged session involving risk.

**Arabic first**
```
Subject: ملخص جلستنا · <date> — Your session summary

أهلين <name>،
شكراً على جلسة اليوم. بعتلك الملخص مرفق، فيه وين واقفة هلأ، شو اكتشفنا، والتمرين الصغير لهالأسبوع.
خدي وقتك فيه، وارجعيله نص الأسبوع.
<one line on anything promised, if any>
لما تكوني جاهزة للخطوة الجاية، الحجز من نفس الرابط.
نادين

—

Hi <name>,
Thank you for today. Your summary is attached: where you stand, what we uncovered, and one small practice for this week.
Take your time with it, and come back to it midweek.
When you're ready for the next step, booking is on the same link.
Nadine
```

**English first**: the same two blocks, with the English on top and the subject `Your session summary · <date> — ملخص جلستنا`.

Keep it short. Nadine will adjust the wording to her own voice.
