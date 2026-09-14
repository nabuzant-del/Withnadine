# With Nadine — website

A static, bilingual (English / العربية) website for **With Nadine**, the 6-pillar
realistic planning brand. White background, brand palette taken from the logo,
no framework and no build step required to host it.

---

## Pages

| File | What it is |
| --- | --- |
| `index.html` | Home — hero, brand philosophy, the 6 pillars, offer ladder, newsletter |
| `about.html` | Nadine's story, the four positions the brand holds, tone and audience |
| `pillars.html` | The six pillars in full, grouped by Recall / Live / Plan, plus the cycle |
| `course.html` | The 13-week curriculum, week-by-week table, the 6 written lessons |
| `work-with-me.html` | The four-tier offer ladder, the $199 consultation, products, FAQ |
| `journal.html` | The six planned long-form articles, one per pillar |
| `contact.html` | Contact form, how a booking works, quick answers |

---

## Running it

It is plain HTML. Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

To publish on **GitHub Pages**: Settings → Pages → deploy from the branch root.
Nothing needs to be compiled.

---

## The bilingual switch

Every piece of visible copy is written **twice in the markup** — once in English,
once in Arabic:

```html
<h1><span data-lang="en">Plan without burning out.</span><span data-lang="ar">خطّطي بدون ما تحترقي.</span></h1>
```

CSS reveals one and hides the other. The `EN / ع` button in the header sets
`lang` and `dir` on `<html>`, which flips the whole page to right-to-left and
swaps to the Arabic typefaces. The choice is remembered in `localStorage`.

English is the default, so the page is still correct if JavaScript never runs.

**To edit a line of copy, edit both spans.** If you only edit one, the other
language silently keeps the old wording.

---

## Brand tokens

All colours and typefaces live at the top of `assets/css/style.css`:

| Token | Value | Where it comes from |
| --- | --- | --- |
| `--yellow` | `#F2CE63` | the "Nadine." wordmark |
| `--yellow-deep` | `#E3BA45` | darker yellow for text-on-white and hovers |
| `--yellow-wash` | `#FDF7E7` | the soft section background |
| `--brown` | `#A9763E` | the handwritten "With" |
| `--ink` | `#14110D` | headings, dark sections, footer |

Typefaces: **Archivo Black** (display), **Archivo** (body), **Sacramento**
(the handwritten "With"), **Noto Kufi Arabic** + **IBM Plex Sans Arabic**
(Arabic display and body). All from Google Fonts.

### The logo

The header and footer wordmark is rebuilt in CSS from the two brand typefaces
so it stays sharp at every size:

```html
<a class="logo" href="index.html">
  <span class="logo__script">With</span>
  <span class="logo__name">Nadine.</span>
</a>
```

**To use the original logo file instead**, drop it in `assets/img/` and replace
those two spans with `<img src="assets/img/logo.png" alt="With Nadine" width="150">`
in each of the seven HTML files (or in `tools/build.py`, then re-run it — see
below). The Arabic نادين lockup from the full logo is a good fit for the footer.

---

## Forms

Neither form is connected to anything yet — they say so plainly rather than
pretending to send. To wire one up, add your provider's POST URL:

```html
<form class="form" data-wn-form data-endpoint="https://your-provider.example/subscribe">
```

Once `data-endpoint` is present the browser posts the form for real, and the
"not connected" message stops appearing. Works with Kit (ConvertKit), Mailchimp,
Formspree, or anything else that accepts a plain form POST.

The newsletter form is on `index.html`, `course.html` and `journal.html`; the
contact form is on `contact.html`.

---

## Editing

**For small changes** — a price, a sentence, a link — edit the HTML directly.
It is readable and there is no build step in the way.

**For changes that hit every page** — a new nav item, a footer link, a change to
the header — edit `tools/build.py` and re-run it from the repo root:

```bash
python3 tools/build.py
```

That regenerates all seven HTML files from the shared header, footer and page
bodies it holds. Be aware that it **overwrites** the HTML files, so if you have
hand-edited a page, fold that edit into `build.py` first or you will lose it.

---

## Still to do

- Point the "Book a consultation" buttons at a real Calendly link (currently
  they go to the contact form)
- Connect the newsletter and contact forms to an email provider
- Add the Instagram and other social links to the footer
- Write the six journal articles (the cards are placeholders marked "coming soon")
- Swap in the real logo file if you prefer it over the CSS wordmark
