# -*- coding: utf-8 -*-
"""Authoring tool: assembles the With Nadine static site from shared parts.
Output is plain HTML in the repo root — no build step is needed to host it."""
import os, io

OUT = "/home/user/Withnadine"

NAV = [
    ("index.html",        "Home",          "الرئيسية"),
    ("about.html",        "About",         "عن نادين"),
    ("pillars.html",      "The 6 Pillars", "الركائز الست"),
    ("course.html",       "Course",        "الدورة"),
    ("work-with-me.html", "Work With Me",  "اشتغلي معي"),
    ("journal.html",      "Journal",       "المدوّنة"),
    ("contact.html",      "Contact",       "تواصلي"),
]

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Archivo+Black&"
         "family=Archivo:wght@400;500;600;700&"
         "family=Sacramento&"
         "family=Noto+Kufi+Arabic:wght@400;500;700&"
         "family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap")

FAVICON = ("data:image/svg+xml,"
           "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' rx='14' fill='%23F2CE63'/%3E"
           "%3Cpath d='M16 46V18h7.6l12.2 17.4V18H43v28h-7.4L23.2 28.4V46z' fill='%2314110D'/%3E"
           "%3C/svg%3E")


def L(en, ar, blk=False):
    """A bilingual text pair. Both languages ship in the markup; CSS shows one."""
    c = ' class="blk"' if blk else ""
    return ('<span data-lang="en"%s>%s</span><span data-lang="ar"%s>%s</span>' % (c, en, c, ar))


def logo(cls=""):
    return ('<a class="logo %s" href="index.html" aria-label="With Nadine — home">'
            '<span class="logo__script">With</span>'
            '<span class="logo__name">Nadine.</span></a>' % cls)


def head(title, desc, page):
    return """<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_CA">
<meta property="og:locale:alternate" content="ar_AR">
<link rel="icon" href="%s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="%s">
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.className += " js";</script>
</head>
<body>
<a class="skip" href="#main">%s</a>
""" % (title, desc, title, desc, FAVICON, FONTS, L("Skip to content", "تخطّي إلى المحتوى"))


def header(page):
    items = []
    for href, en, ar in NAV:
        cur = ' aria-current="page"' if href == page else ""
        items.append('<a class="nav__link" href="%s"%s>%s</a>' % (href, cur, L(en, ar)))
    return """<div class="topbar">%s</div>
<header class="site-header">
  <div class="wrap nav">
    %s
    <button class="burger" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Menu"><span></span></button>
    <nav class="nav__links" id="nav-links" aria-label="Main">
      %s
      <div class="nav__actions">
        <div class="lang" role="group" aria-label="Language / اللغة">
          <button type="button" data-set-lang="en" aria-pressed="true">EN</button>
          <button type="button" data-set-lang="ar" aria-pressed="false">ع</button>
        </div>
        <a class="btn btn--primary btn--sm" href="work-with-me.html#book">%s</a>
      </div>
    </nav>
  </div>
</header>
<main id="main">
""" % (
        L("1:1 consultations are open — <b>15 spots each month</b>.",
          "الاستشارات الفردية متاحة — <b>١٥ مقعداً شهرياً</b>."),
        logo(),
        "\n      ".join(items),
        L("Book a 1:1", "احجزي جلسة"),
    )


def footer():
    def col(title_en, title_ar, rows):
        lis = "".join('<li><a href="%s">%s</a></li>' % (h, L(e, a)) for h, e, a in rows)
        return ('<div><h2 class="foot__h">%s</h2><ul class="foot__list">%s</ul></div>'
                % (L(title_en, title_ar), lis))

    return """</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot__grid">
      <div>
        %s
        <p class="foot__about">%s</p>
      </div>
      %s
      %s
      %s
    </div>
    <div class="foot__bottom">
      <span>&copy; <span data-year>2026</span> With Nadine. %s</span>
      <span>%s</span>
    </div>
  </div>
</footer>
<script src="assets/js/main.js"></script>
</body>
</html>
""" % (
        logo(),
        L("Realistic planning for women who are done with toxic productivity. Built on six pillars, taught in Arabic and English.",
          "تخطيط واقعي للنساء اللواتي تعبن من ثقافة الإنتاجية السامة. مبني على ست ركائز، ويُدرَّس بالعربية والإنجليزية."),
        col("Learn", "تعلّمي", [
            ("pillars.html", "The 6 Pillars", "الركائز الست"),
            ("course.html", "The Course", "الدورة"),
            ("journal.html", "Journal", "المدوّنة"),
        ]),
        col("Work together", "اشتغلي معي", [
            ("work-with-me.html#book", "1:1 Consultation", "استشارة فردية"),
            ("work-with-me.html#products", "Workbooks &amp; Planners", "كتيّبات ومخططات"),
            ("work-with-me.html#groups", "Group Programs", "البرامج الجماعية"),
        ]),
        col("About", "عن", [
            ("about.html", "About Nadine", "عن نادين"),
            ("contact.html", "Contact", "تواصلي"),
            ("index.html#newsletter", "Newsletter", "النشرة البريدية"),
        ]),
        L("All rights reserved.", "جميع الحقوق محفوظة."),
        L("Fredericton, New Brunswick, Canada", "فريدريكتون، نيو برونزويك، كندا"),
    )


def page(filename, title, desc, body):
    html = head(title, desc, filename) + header(filename) + body + footer()
    with io.open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename, len(html))


# ---------------------------------------------------------------- shared data
PHASES = [
    ("Recall", "تذكّر", "Foundation — see what is actually there.",
     "الأساس — أن تري ما هو موجود فعلاً."),
    ("Live", "تعييش", "Implementation — carry it into the day.",
     "التطبيق — أن تعيشيه في يومك."),
    ("Plan", "تخططي", "Strategy — decide, and stay flexible.",
     "الاستراتيجية — أن تقرّري وتبقي مرنة."),
]

PILLARS = [
    dict(n="01", phase=0,
         en="Observe Without Judgment", ar="الملاحظة بلا حكم",
         teach_en="How to see what is actually happening, without deciding what it says about you.",
         teach_ar="كيف ترين ما يحدث فعلاً، دون أن تحكمي على نفسك من خلاله.",
         long_en="Observation is fact: <em>I opened the laptop at 9 and closed it at 10:30.</em> Judgment is interpretation: <em>I am so disciplined.</em> The moment you judge, your brain files the case and stops collecting evidence — and every plan you build after that is built for the person you think you are.",
         long_ar="الملاحظة حقيقة: <em>فتحت اللابتوب الساعة ٩ وأغلقته ١٠:٣٠.</em> الحكم تفسير: <em>أنا منضبطة جداً.</em> لحظة ما تحكمين، يقفل دماغك الملف ويتوقف عن جمع الأدلة — وكل خطة تبنينها بعدها تكون لشخص تتخيلينه، لا لشخص موجود.",
         tool_en="Tool: the three-layer neutral note — physical, emotional, circumstantial.",
         tool_ar="الأداة: الملاحظة المحايدة بثلاث طبقات — الجسدية، الشعورية، الظرفية.",
         prod="Observation Without Judgment"),
    dict(n="02", phase=0,
         en="Pattern, Not Incident", ar="النمط مش الحادثة",
         teach_en="How to tell a real pattern apart from one loud, memorable day.",
         teach_ar="كيف تميّزين النمط الحقيقي عن يوم واحد صاخب لا يُنسى.",
         long_en="You stayed up until midnight once, and now you are &ldquo;a night owl.&rdquo; That is recency bias writing your identity. Three consistent instances across different contexts is a possible pattern. Six is a probable one. One is a story.",
         long_ar="سهرت مرة حتى منتصف الليل، فصرتِ «إنسانة ليلية». هذا انحياز الحداثة وهو يكتب هويتك. ثلاث حالات متسقة في سياقات مختلفة = نمط محتمل. ست حالات = نمط شبه مؤكد. حالة واحدة = قصة.",
         tool_en="Tool: the trigger &rarr; pattern &rarr; outcome triangle, and the 30-day audit.",
         tool_ar="الأداة: مثلث المحفّز ← النمط ← النتيجة، ومراجعة الثلاثين يوماً.",
         prod="Pattern Hunting"),
    dict(n="03", phase=1,
         en="Energy Awareness", ar="وعي الطاقة",
         teach_en="How to manage energy instead of managing hours you do not really have.",
         teach_ar="كيف تديرين طاقتك بدل أن تديري ساعات لا تملكينها أصلاً.",
         long_en="A calendar assumes every hour is the same hour. Your body knows better. Map where your energy actually rises and falls, then put the work that matters inside the peak — not inside the gap you happened to find.",
         long_ar="التقويم يفترض أن كل ساعة تشبه الأخرى. جسدك يعرف غير ذلك. ارسمي خريطة طاقتك الحقيقية، ثم ضعي العمل المهم داخل الذروة — لا داخل أي فراغ صادفتِه.",
         tool_en="Tool: the energy map — a week of highs, dips and what caused each.",
         tool_ar="الأداة: خريطة الطاقة — أسبوع من الذروات والهبوط وسبب كل منهما.",
         prod="Energy Map"),
    dict(n="04", phase=1,
         en="Full Presence", ar="الحضور الكامل",
         teach_en="How to be fully in one thing, rather than partly in five.",
         teach_ar="كيف تكونين حاضرة بالكامل في شيء واحد، بدل أن تكوني نصف حاضرة في خمسة.",
         long_en="Busy is not present. Presence is what makes an hour of work worth an hour, a conversation worth having, and a plan worth following. Absence leaves markers — you can learn to spot yours.",
         long_ar="الانشغال ليس حضوراً. الحضور هو ما يجعل ساعة العمل تساوي ساعة، والحديث يستحق أن يُقال، والخطة تستحق أن تُتبع. الغياب يترك علامات — ويمكنك أن تتعلمي ملاحظتها.",
         tool_en="Tool: absence markers — the small tells that you have already left the room.",
         tool_ar="الأداة: علامات الغياب — الإشارات الصغيرة التي تكشف أنك غادرتِ الغرفة أصلاً.",
         prod="Absence Markers"),
    dict(n="05", phase=2,
         en="Conscious Decision", ar="القرار الواعي",
         teach_en="How to decide with all three layers: head, heart and gut.",
         teach_ar="كيف تقرّرين بالطبقات الثلاث: العقل، القلب، والحدس.",
         long_en="Head asks whether it fits the goal. Heart asks whether you actually want it. Gut asks whether it feels right. When the three disagree, you get a half-hearted yes — and half-hearted commitments are the ones that collapse first.",
         long_ar="العقل يسأل: هل يناسب الهدف؟ القلب يسأل: هل أريده فعلاً؟ الحدس يسأل: هل يبدو صحيحاً؟ حين تختلف الثلاثة، تحصلين على «نعم» فاترة — والالتزامات الفاترة هي أول ما ينهار.",
         tool_en="Tool: the three-layer decision check — no move until all three agree.",
         tool_ar="الأداة: فحص القرار بثلاث طبقات — لا تتحركي قبل أن تتفق الثلاثة.",
         prod="Decision Framework"),
    dict(n="06", phase=2,
         en="Smart Flexibility", ar="المرونة الذكية",
         teach_en="How to flex the plan without abandoning the goal.",
         teach_ar="كيف تعدّلين الخطة دون أن تتخلّي عن الهدف.",
         long_en="Most people treat a broken plan as a broken person. It is neither. When reality changes, you rebuild the plan using the five pillars before it — you do not cancel it, and you do not start over in January.",
         long_ar="أغلب الناس يعاملون الخطة المكسورة كأنها شخص مكسور. وهي ليست كذلك. حين يتغيّر الواقع، تعيدين بناء الخطة بالركائز الخمس قبلها — لا تلغينها، ولا تنتظرين يناير.",
         tool_en="Tool: rebuild, don't cancel — the four-question plan reset.",
         tool_ar="الأداة: أعيدي البناء ولا تلغي — إعادة ضبط الخطة بأربعة أسئلة.",
         prod="Rebuild, Don't Cancel"),
]


def pillar_cards(link=True):
    out = []
    for p in PILLARS:
        tag = ('<a class="card" href="pillars.html#p%s">' % p["n"]) if link else '<div class="card">'
        end = "</a>" if link else "</div>"
        out.append("""%s
  <div class="pillar__head">
    <span class="pillar__num">%s</span>
    <span class="pillar__ar">%s</span>
  </div>
  <h3 class="h3 card__title">%s</h3>
  <p class="card__body">%s</p>
%s""" % (tag, p["n"], p["ar"], L(p["en"], p["ar"]), L(p["teach_en"], p["teach_ar"]), end))
    return "\n".join(out)


CYCLE_SVG = """<svg class="cycle" viewBox="0 0 400 400" direction="ltr" role="img" aria-labelledby="cycTitle">
  <title id="cycTitle">The six pillars run as a repeating cycle: observe, pattern, energy, presence, decision, flexibility.</title>
  <defs><marker id="cyc-tip" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#E3BA45"/></marker></defs>
  <circle class="cycle__ring" cx="200" cy="200" r="132"/>
  <path class="cycle__arc" d="M 200 68 A 132 132 0 0 1 314.3 266" marker-end="url(#cyc-tip)"/>
  <g class="cycle__node cycle__node--on"><circle cx="200" cy="68"  r="26"/></g>
  <g class="cycle__node"><circle cx="314" cy="134" r="26"/></g>
  <g class="cycle__node"><circle cx="314" cy="266" r="26"/></g>
  <g class="cycle__node"><circle cx="200" cy="332" r="26"/></g>
  <g class="cycle__node"><circle cx="86"  cy="266" r="26"/></g>
  <g class="cycle__node"><circle cx="86" cy="134" r="26"/></g>
  <text class="cycle__num" x="200" y="68">1</text>
  <text class="cycle__num" x="314" y="134">2</text>
  <text class="cycle__num" x="314" y="266">3</text>
  <text class="cycle__num" x="200" y="332">4</text>
  <text class="cycle__num" x="86"  y="266">5</text>
  <text class="cycle__num" x="86"  y="134">6</text>
  <text class="cycle__cap" x="288" y="48">RECALL</text>
  <text class="cycle__cap" x="288" y="356">LIVE</text>
  <text class="cycle__cap" x="36" y="204">PLAN</text>
  <text class="cycle__mid" x="200" y="194">6 pillars</text>
  <text class="cycle__sub" x="200" y="216">ONE LIVING CYCLE</text>
</svg>"""


NEWSLETTER = """
<section class="sec sec--tight" id="newsletter">
  <div class="wrap wrap--mid">
    <div class="signup reveal">
      <p class="eyebrow">%s</p>
      <h2 class="h2">%s</h2>
      <p class="lede" style="margin-top:14px">%s</p>
      <form class="form mt-l" data-wn-form novalidate>
        <div class="field">
          <label for="nl-email">%s</label>
          <input id="nl-email" name="email" type="email" autocomplete="email" required placeholder="nadine@example.com">
        </div>
        <button class="btn btn--ink" type="submit">%s</button>
        <p class="form__note">%s</p>
        <p class="form__msg" role="status" tabindex="-1" hidden></p>
      </form>
    </div>
  </div>
</section>
""" % (
    L("Free checklist", "قائمة مجانية"),
    L("Start with one week of honest observation.", "ابدئي بأسبوع واحد من الملاحظة الصادقة."),
    L("Join the list and get the <strong>Observation Without Judgment</strong> checklist — one page, bilingual, no theory. Then a short teaching letter each week, one pillar at a time.",
      "انضمّي إلى القائمة واحصلي على قائمة <strong>الملاحظة بلا حكم</strong> — صفحة واحدة، بالعربية والإنجليزية، بلا نظريات. ثم رسالة تعليمية قصيرة كل أسبوع، ركيزة تلو الأخرى."),
    L("Email address", "البريد الإلكتروني"),
    L("Send me the checklist", "أرسلي لي القائمة"),
    L("One letter a week. Unsubscribe any time.", "رسالة واحدة أسبوعياً. يمكنك إلغاء الاشتراك في أي وقت."),
)


# ------------------------------------------------------------------- index
phase_blocks = []
for i, (pen, par, den, dar) in enumerate(PHASES):
    cards = "\n".join(pillar_cards().split("\n\n")[0:0])  # placeholder, filled below
    inner = []
    for p in PILLARS:
        if p["phase"] != i:
            continue
        inner.append("""<a class="card reveal" href="pillars.html#p%s">
  <div class="pillar__head">
    <span class="pillar__num">%s</span>
    <span class="pillar__ar">%s</span>
  </div>
  <h3 class="h3 card__title">%s</h3>
  <p class="card__body">%s</p>
  <span class="card__foot"><span class="link" aria-hidden="true">%s <svg class="arrow" width="15" height="15" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></span></span>
</a>""" % (p["n"], p["n"], p["ar"], L(p["en"], p["ar"]),
           L(p["teach_en"], p["teach_ar"]), L("Read the pillar", "اقرئي الركيزة")))
    phase_blocks.append("""<div class="mt-xl">
  <p class="phase">%s <i>%s</i></p>
  <p class="muted small" style="margin:-12px 0 22px">%s</p>
  <div class="grid grid--2">
    %s
  </div>
</div>""" % (pen.upper(), par, L(den, dar), "\n    ".join(inner)))

INDEX = """
<section class="sec hero">
  <div class="wrap split">
    <div>
      <p class="eyebrow">%(eyebrow)s</p>
      <h1 class="display">%(h1)s</h1>
      <p class="lede" style="margin-top:26px">%(lede)s</p>
      <div class="btn-row mt-l">
        <a class="btn btn--primary" href="pillars.html">%(cta1)s</a>
        <a class="btn btn--ghost" href="work-with-me.html#book">%(cta2)s</a>
      </div>
      <p class="hero__mission">%(mission)s</p>
    </div>
    <div>%(cycle)s</div>
  </div>
  <div class="wrap">
    <div class="hero__stats">
      <div><div class="stat__num">6</div><div class="stat__label">%(s1)s</div></div>
      <div><div class="stat__num">18</div><div class="stat__label">%(s2)s</div></div>
      <div><div class="stat__num">13</div><div class="stat__label">%(s3)s</div></div>
      <div><div class="stat__num">15+</div><div class="stat__label">%(s4)s</div></div>
    </div>
  </div>
</section>

<section class="sec sec--wash">
  <div class="wrap wrap--mid">
    <p class="eyebrow">%(pheyebrow)s</p>
    <h2 class="h2">%(phh2)s</h2>
    <p class="lede" style="margin-top:18px">%(phlede)s</p>
    <div class="philo mt-l reveal">
      <div class="philo__row"><div class="philo__k">%(k1)s</div><div class="philo__v">%(v1)s</div></div>
      <div class="philo__row"><div class="philo__k">%(k2)s</div><div class="philo__v">%(v2)s</div></div>
      <div class="philo__row"><div class="philo__k">%(k3)s</div><div class="philo__v">%(v3)s</div></div>
      <div class="philo__row philo__row--last"><div class="philo__k">%(k4)s</div><div class="philo__v">%(v4)s</div></div>
    </div>
  </div>
</section>

<section class="sec" id="pillars">
  <div class="wrap">
    <div class="wrap--mid" style="padding:0;margin-inline:0">
      <p class="eyebrow">%(fweyebrow)s</p>
      <h2 class="h2">%(fwh2)s</h2>
      <p class="lede" style="margin-top:18px">%(fwlede)s</p>
    </div>
    %(phases)s
  </div>
</section>

<section class="sec sec--ink">
  <div class="wrap">
    <div class="quote reveal">
      <span class="quote__mark">&ldquo;</span>
      <p class="quote__text">%(q)s</p>
      <p class="quote__by">%(qby)s</p>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div>
      <p class="eyebrow">%(coeyebrow)s</p>
      <h2 class="h2">%(coh2)s</h2>
      <p class="lede" style="margin-top:18px">%(colede)s</p>
      <div class="btn-row mt-l">
        <a class="btn btn--ink" href="course.html">%(cocta)s</a>
      </div>
    </div>
    <div class="grid grid--2">
      <div class="card card--flat reveal"><div class="stat__num">13</div><p class="card__body" style="margin-top:8px">%(c1)s</p></div>
      <div class="card card--flat reveal"><div class="stat__num">18</div><p class="card__body" style="margin-top:8px">%(c2)s</p></div>
      <div class="card card--flat reveal"><div class="stat__num">2</div><p class="card__body" style="margin-top:8px">%(c3)s</p></div>
      <div class="card card--flat reveal"><div class="stat__num">20&#8202;m</div><p class="card__body" style="margin-top:8px">%(c4)s</p></div>
    </div>
  </div>
</section>

<section class="sec sec--wash">
  <div class="wrap">
    <div class="center">
      <p class="eyebrow eyebrow--plain">%(oeyebrow)s</p>
      <h2 class="h2">%(oh2)s</h2>
      <p class="lede" style="margin-top:18px">%(olede)s</p>
    </div>
    <div class="grid grid--3 mt-xl">
      <div class="card price reveal">
        <span class="tag">%(t1)s</span>
        <div class="price__fig">%(p1)s</div>
        <div class="price__unit">%(u1)s</div>
        <p class="card__body">%(d1)s</p>
        <div class="card__foot"><a class="link" href="work-with-me.html#products">%(l1)s <svg class="arrow" width="15" height="15" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></a></div>
      </div>
      <div class="card price price--feature reveal" data-badge-en="Most popular" data-badge-ar="الأكثر طلباً">
        <span class="tag tag--ink">%(t2)s</span>
        <div class="price__fig">%(p2)s</div>
        <div class="price__unit">%(u2)s</div>
        <p class="card__body">%(d2)s</p>
        <div class="card__foot"><a class="btn btn--primary btn--sm" href="work-with-me.html#book">%(l2)s</a></div>
      </div>
      <div class="card price reveal">
        <span class="tag tag--soon">%(t3)s</span>
        <div class="price__fig">%(p3)s</div>
        <div class="price__unit">%(u3)s</div>
        <p class="card__body">%(d3)s</p>
        <div class="card__foot"><a class="link" href="work-with-me.html#groups">%(l3)s <svg class="arrow" width="15" height="15" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></a></div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div>
      <p class="eyebrow">%(abeyebrow)s</p>
      <h2 class="h2">%(abh2)s</h2>
      <p class="lede" style="margin-top:18px">%(ablede)s</p>
      <div class="btn-row mt-l"><a class="btn btn--ghost" href="about.html">%(abcta)s</a></div>
    </div>
    <div class="card reveal">
      <p class="script" style="font-size:2.6rem">A note from Nadine</p>
      <p class="card__body" style="margin-top:18px">%(note)s</p>
    </div>
  </div>
</section>
%(newsletter)s
""" % dict(
    eyebrow=L("Realistic planning &middot; التخطيط الواقعي", "التخطيط الواقعي &middot; Realistic planning"),
    h1=L("Plan without<br>burning out.", "خطّطي<br>بدون ما تحترقي."),
    lede=L("With Nadine is an Arabic-language coaching practice built on six pillars. No productivity hacks. No 5 AM. A framework for seeing what is actually happening in your life &mdash; and planning from there.",
           "«مع نادين» ممارسة تدريبية بالعربية مبنية على ست ركائز. لا حيل إنتاجية، ولا استيقاظ الخامسة فجراً. إطار عمل يساعدك أن تري ما يحدث فعلاً في حياتك &mdash; وأن تخطّطي منه."),
    cta1=L("Explore the 6 pillars", "اكتشفي الركائز الست"),
    cta2=L("Book a consultation", "احجزي استشارة"),
    mission=L("Defend good habits, challenge harmful trends, and shift how you think &mdash; instead of chasing the next viral moment.",
              "ندافع عن العادات الجيدة، ونتحدّى الموضات المؤذية، ونغيّر طريقة التفكير &mdash; بدل اللهاث خلف الترند."),
    cycle=CYCLE_SVG,
    s1=L("pillars, in one repeating cycle", "ركائز، في دورة واحدة متكرّرة"),
    s2=L("lessons across the full course", "درساً في الدورة الكاملة"),
    s3=L("weeks from observation to plan", "أسبوعاً من الملاحظة إلى الخطة"),
    s4=L("years in operations and process work", "سنة خبرة في العمليات ورسم المسارات"),

    pheyebrow=L("How this brand talks", "كيف نتكلّم هنا"),
    phh2=L("Name the trend. Grant the truth. Then reframe it.", "سمّي الترند. اعترفي بجزء الحقيقة. ثم أعيدي التأطير."),
    phlede=L("Every piece of content here follows the same four beats. It is why the tone stays calm instead of loud &mdash; and why it speaks to the real barrier, not the surface symptom.",
             "كل محتوى هنا يسير على أربع خطوات ثابتة. لهذا تبقى النبرة هادئة لا صاخبة &mdash; ولهذا نخاطب العائق الحقيقي، لا العَرَض الظاهر."),
    k1=L("The trend", "الترند"),
    v1=L("&ldquo;Everyone says you need to wake up at 5 AM.&rdquo;", "«الكل يقول لازم تصحي الساعة خمسة الفجر.»"),
    k2=L("The partial truth", "جزء الحقيقة"),
    v2=L("Some people genuinely do their best work at 5 AM. That is real.", "فعلاً، بعض الناس يقدّمون أفضل ما لديهم في الخامسة فجراً. هذا صحيح."),
    k3=L("The reframe", "إعادة التأطير"),
    v3=L("But most of us chase the 5 AM myth so we never have to look at our actual sleep pattern.",
         "لكن أغلبنا يلاحق أسطورة الخامسة فجراً حتى لا يضطر للنظر في نمط نومه الحقيقي."),
    k4=L("The close", "الخلاصة"),
    v4=L("Stop chasing. Start observing.", "بطّلي ملاحقة. ابدئي ملاحظة."),

    fweyebrow=L("The framework", "الإطار"),
    fwh2=L("Six pillars, grouped by what they ask of you.", "ست ركائز، مرتّبة حسب ما تطلبه منك."),
    fwlede=L("Recall asks you to look back honestly. Live asks you to carry it into the day. Plan asks you to decide and stay flexible. Together they form one cycle you can run again every month.",
             "«تذكّر» تطلب منك أن تنظري للخلف بصدق. «تعييش» تطلب أن تعيشيها في يومك. «تخططي» تطلب أن تقرّري وتبقي مرنة. معاً يشكّلن دورة واحدة تكرّرينها كل شهر."),
    phases="\n    ".join(phase_blocks),

    q=L("Observation beats willpower. <mark class=\"hl\">Patterns beat incidents.</mark> Presence beats performance.",
        "الملاحظة تتفوّق على الإرادة. <mark class=\"hl\">الأنماط تتفوّق على الحوادث.</mark> الحضور يتفوّق على الأداء."),
    qby=L("The With Nadine method", "منهج «مع نادين»"),

    coeyebrow=L("The course", "الدورة"),
    coh2=L("Thirteen weeks. One pillar at a time.", "ثلاثة عشر أسبوعاً. ركيزة واحدة في كل مرة."),
    colede=L("A self-paced course that walks the full cycle: observe, find the pattern, map your energy, practise presence, decide consciously, then rebuild when life moves. Lessons 1.1 to 2.3 are written and ready; the rest are in production.",
             "دورة ذاتية الإيقاع تمشي في الدورة كاملة: لاحظي، اكتشفي النمط، ارسمي طاقتك، تدرّبي على الحضور، قرّري بوعي، ثم أعيدي البناء حين تتغيّر الحياة. الدروس من ١.١ إلى ٢.٣ جاهزة، والباقي قيد الإنتاج."),
    cocta=L("See the curriculum", "شاهدي المنهج"),
    c1=L("weeks, including a final integration week", "أسبوعاً، منها أسبوع تكامل ختامي"),
    c2=L("lessons &mdash; three for every pillar", "درساً &mdash; ثلاثة لكل ركيزة"),
    c3=L("languages: Arabic and English, side by side", "لغتان: العربية والإنجليزية، جنباً إلى جنب"),
    c4=L("minutes per lesson, self-paced", "دقيقة لكل درس، بإيقاعك أنت"),

    oeyebrow=L("Three ways in", "ثلاث طرق للبداية"),
    oh2=L("Start where you actually are.", "ابدئي من حيث أنت فعلاً."),
    olede=L("A one-page checklist, a two-hour conversation, or a cohort you move through with others. Same framework, different depth.",
            "قائمة من صفحة واحدة، أو حوار لساعتين، أو مجموعة تمشين فيها مع أخريات. الإطار نفسه، بعمق مختلف."),
    t1=L("Self-paced", "بإيقاعك"),
    p1="$9&ndash;$39",
    u1=L("checklists, workbooks &amp; planners", "قوائم، كتيّبات، ومخططات"),
    d1=L("Bilingual PDFs, one per pillar. Instant download, nothing to schedule. The lowest-friction way to test whether this framework fits you.",
         "ملفات PDF بلغتين، واحد لكل ركيزة. تنزيل فوري بلا مواعيد. أقل طريقة مقاومةً لتجرّبي إن كان هذا الإطار يناسبك."),
    l1=L("Browse the products", "تصفّحي المنتجات"),
    t2=L("1:1 with Nadine", "فردي مع نادين"),
    p2="$199",
    u2=L("2-hour session + 45-min follow-up", "جلسة ساعتين + متابعة ٤٥ دقيقة"),
    d2=L("A pre-session questionnaire, two hours together, a written action plan within 24 hours, and a week of email access. One flat price worldwide.",
         "استبيان قبل الجلسة، ساعتان معاً، خطة عمل مكتوبة خلال ٢٤ ساعة، وأسبوع من التواصل بالبريد. سعر موحّد في كل العالم."),
    l2=L("Book a consultation", "احجزي استشارة"),
    t3=L("Coming 2027", "قريباً ٢٠٢٧"),
    p3="$297+",
    u3=L("4-week and 12-week cohorts", "مجموعات ٤ أسابيع و١٢ أسبوعاً"),
    d3=L("Small groups working the six pillars together, with live sessions and shared accountability. Opening in the first quarter of 2027.",
         "مجموعات صغيرة تعمل على الركائز الست معاً، بجلسات مباشرة ومساءلة مشتركة. تنطلق في الربع الأول من ٢٠٢٧."),
    l3=L("Join the waiting list", "انضمّي لقائمة الانتظار"),

    abeyebrow=L("Who is behind this", "مَن وراء هذا"),
    abh2=L("Fifteen years of untangling other people&rsquo;s processes.", "خمسة عشر عاماً من فكّ تعقيدات عمليات الآخرين."),
    ablede=L("Nadine spent her career in banking operations, client escalations and process mapping &mdash; work that is mostly about finding where a system quietly breaks. With Nadine turns that same attention on the systems we run our own lives with.",
             "أمضت نادين حياتها المهنية في عمليات البنوك، ومعالجة تصعيدات العملاء، ورسم مسارات العمل &mdash; وهو عمل جوهره اكتشاف المكان الذي ينكسر فيه النظام بهدوء. و«مع نادين» توجّه الانتباه نفسه إلى الأنظمة التي ندير بها حياتنا."),
    abcta=L("Read her story", "اقرئي قصتها"),
    note=L("I did not build this framework because I had planning figured out. I built it because I did not &mdash; and because after a hundred books on self-development, the thing that finally moved was not more discipline. It was looking honestly at what I actually do.",
           "ما بنيت هذا الإطار لأني كنت أتقن التخطيط. بنيته لأني لم أكن أتقنه &mdash; ولأن ما تغيّر أخيراً، بعد أكثر من مئة كتاب في التطوير الذاتي، لم يكن مزيداً من الانضباط. كان النظر بصدق إلى ما أفعله فعلاً."),
    newsletter=NEWSLETTER,
)

page("index.html",
     "With Nadine — Realistic planning, in Arabic and English",
     "An Arabic-language coaching practice built on six pillars of realistic planning. Observe without judgment, find the pattern, and plan without burning out.",
     INDEX)


def pagehead(eyebrow_en, eyebrow_ar, h1_en, h1_ar, lede_en, lede_ar):
    return """
<section class="pagehead">
  <div class="wrap">
    <p class="eyebrow">%s</p>
    <h1 class="h1">%s</h1>
    <p class="lede">%s</p>
  </div>
</section>
""" % (L(eyebrow_en, eyebrow_ar), L(h1_en, h1_ar), L(lede_en, lede_ar))


ARROW = ('<svg class="arrow" width="15" height="15" viewBox="0 0 16 16" fill="none">'
         '<path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')


# =============================================================== the 6 pillars
blocks = []
for i, (pen, par, den, dar) in enumerate(PHASES):
    rows = []
    for p in PILLARS:
        if p["phase"] != i:
            continue
        rows.append("""<article class="split reveal" id="p%s" style="margin-top:clamp(40px,6vw,64px)">
  <div>
    <div class="pillar__head" style="justify-content:flex-start;gap:16px">
      <span class="pillar__num">%s</span>
      <span class="pillar__ar" style="font-size:1.25rem">%s</span>
    </div>
    <h2 class="h2" style="margin-top:6px">%s</h2>
    <p class="lede" style="margin-top:16px">%s</p>
  </div>
  <div class="card card--flat">
    <p class="card__body">%s</p>
    <hr style="margin:22px 0">
    <p class="h4">%s</p>
    <p class="card__body" style="margin-top:8px">%s</p>
  </div>
</article>""" % (p["n"], p["n"], p["ar"], L(p["en"], p["ar"]),
                 L(p["teach_en"], p["teach_ar"]),
                 L(p["long_en"], p["long_ar"]),
                 L("In the workbook", "في الكتيّب"),
                 L(p["tool_en"], p["tool_ar"])))
    blocks.append("""<div class="sec %s">
  <div class="wrap">
    <p class="phase">%s <i>%s</i></p>
    <p class="lede">%s</p>
    %s
  </div>
</div>""" % ("sec--wash" if i % 2 else "", pen.upper(), par, L(den, dar), "\n    ".join(rows)))

PILLARS_BODY = pagehead(
    "The framework", "الإطار",
    "The six pillars.", "الركائز الست.",
    "Not six tips. Six skills that run in order, then start again. Each one has a teaching, a tool, and a place in the cycle.",
    "ليست ست نصائح. بل ست مهارات تعمل بالترتيب، ثم تبدأ من جديد. لكل واحدة درس، وأداة، وموقع في الدورة.",
) + "\n".join(blocks) + """
<section class="sec sec--ink">
  <div class="wrap wrap--mid">
    <p class="eyebrow" style="color:var(--yellow)">%s</p>
    <h2 class="h2">%s</h2>
    <p class="lede" style="color:#CFC9C0;margin-top:18px">%s</p>
    <div class="steps mt-l">
      %s
    </div>
    <p class="lede" style="color:#CFC9C0;margin-top:32px">%s</p>
    <div class="btn-row mt-l">
      <a class="btn btn--primary" href="course.html">%s</a>
      <a class="btn btn--light" href="work-with-me.html#book">%s</a>
    </div>
  </div>
</section>
""" % (
    L("The cycle", "الدورة"),
    L("This is not a plan you finish. It is a loop you run.", "هذه ليست خطة تنتهي منها. بل حلقة تدورين فيها."),
    L("Once you reach the sixth pillar, you return to the first with better data than you had last time. That is the whole design.",
      "حين تصلين إلى الركيزة السادسة، تعودين إلى الأولى ببيانات أفضل مما كان لديك في المرة السابقة. هذا هو التصميم كله."),
    "\n      ".join(
        '<div class="step"><div class="step__num">%s</div><div><p class="h3 step__t">%s</p><p class="card__body" style="color:#A8A199">%s</p></div></div>'
        % (s[0], L(s[1], s[2]), L(s[3], s[4])) for s in [
            ("1", "Observe", "لاحظي", "Watch your market, your audience and your own behaviour without deciding what it means yet.", "راقبي محيطك، جمهورك، وسلوكك أنت، دون أن تقرّري بعد ماذا يعني ذلك."),
            ("2", "Find the pattern", "اكتشفي النمط", "Notice what actually repeats. Three instances, not one loud day.", "لاحظي ما يتكرّر فعلاً. ثلاث حالات، لا يوماً صاخباً واحداً."),
            ("3", "Protect the energy", "احمي الطاقة", "Schedule the work that matters inside the hours you are actually able to do it.", "ضعي العمل المهم داخل الساعات التي تستطيعين فيها فعلاً."),
            ("4", "Show up fully", "احضري بالكامل", "One thing at a time. Presence is what makes the hour worth the hour.", "شيء واحد في كل مرة. الحضور هو ما يجعل الساعة تساوي ساعة."),
            ("5", "Decide consciously", "قرّري بوعي", "Head, heart and gut all have to agree before you commit.", "العقل والقلب والحدس، الثلاثة يجب أن يتفقوا قبل أن تلتزمي."),
            ("6", "Flex, don't cancel", "عدّلي ولا تلغي", "When reality shifts, rebuild the plan with the five pillars before it.", "حين يتغيّر الواقع، أعيدي بناء الخطة بالركائز الخمس السابقة."),
        ]),
    L("Then go back to one.", "ثم عودي إلى الأولى."),
    L("Learn it as a course", "تعلّميها كدورة"),
    L("Work it with Nadine", "اعملي عليها مع نادين"),
)

page("pillars.html", "The 6 Pillars — With Nadine",
     "Observe without judgment, pattern not incident, energy awareness, full presence, conscious decision, smart flexibility. The six-pillar framework behind With Nadine.",
     PILLARS_BODY)


# ==================================================================== course
LESSONS = [
  ("1.1", "The Hidden Cost of Judgment", "الثمن الخفي للحكم",
   "Why planners fail before they start", "لماذا تفشل الخطط قبل أن تبدأ", True,
   ["Understand how judgment masks observation and distorts what you actually see",
    "Recognise the gap between what is happening and what you assume is happening",
    "Identify how assumptions create the blind spots that sabotage your plans"],
   ["أن تفهمي كيف يحجب الحكمُ الملاحظةَ ويشوّه ما ترينه فعلاً",
    "أن تميّزي الفجوة بين ما يحدث وما تفترضين أنه يحدث",
    "أن تكتشفي كيف تصنع الافتراضات النقاط العمياء التي تُفشل خططك"]),
  ("1.2", "How to Observe Your Own Behavior", "كيف تلاحظين سلوكك",
   "The three layers that reveal everything", "الطبقات الثلاث التي تكشف كل شيء", True,
   ["Learn the three layers of observation — physical, emotional, circumstantial",
    "Build a system for capturing behaviour without judgment",
    "Make daily observation a five-minute habit that lasts"],
   ["أن تتعلّمي طبقات الملاحظة الثلاث — الجسدية والشعورية والظرفية",
    "أن تبني نظاماً لتسجيل السلوك بلا حكم",
    "أن تحوّلي الملاحظة اليومية إلى عادة من خمس دقائق تستمر"]),
  ("1.3", "From Observation to Insight", "من الملاحظة إلى البصيرة",
   "How to turn data into understanding", "كيف تحوّلين البيانات إلى فهم", True,
   ["Move from raw observation to meaningful insight",
    "Tell correlation apart from causation in your own behaviour",
    "Use three questions to extract something you can actually act on"],
   ["أن تنتقلي من الملاحظة الخام إلى بصيرة ذات معنى",
    "أن تفرّقي بين الترابط والسببية في سلوكك",
    "أن تستخدمي ثلاثة أسئلة لاستخراج ما يمكنك التصرّف بناءً عليه"]),
  ("2.1", "Why One Incident Is Not a Pattern", "لماذا الحادثة الواحدة ليست نمطاً",
   "How your brain tricks you into false conclusions", "كيف يخدعك دماغك بخلاصات زائفة", True,
   ["Understand the difference between an incident and a pattern",
    "Learn why your brain defaults to treating incidents as patterns",
    "Apply the three-data-point rule before you claim a pattern"],
   ["أن تفهمي الفرق بين الحادثة والنمط",
    "أن تعرفي لماذا يميل دماغك لمعاملة الحوادث كأنماط",
    "أن تطبّقي قاعدة النقاط الثلاث قبل أن تعلني وجود نمط"]),
  ("2.2", "How to Spot Real Patterns", "كيف تكتشفين الأنماط الحقيقية",
   "The trigger–pattern–outcome triangle", "مثلث المحفّز والنمط والنتيجة", True,
   ["Learn the three-part structure that reveals a real pattern",
    "Run a 30-day audit of your own observation data",
    "Find the hidden patterns underneath the obvious behaviour"],
   ["أن تتعلّمي البنية الثلاثية التي تكشف النمط الحقيقي",
    "أن تجري مراجعة ثلاثين يوماً لبيانات ملاحظتك",
    "أن تجدي الأنماط الخفية تحت السلوك الظاهر"]),
  ("2.3", "How Patterns Change Everything", "كيف تغيّر الأنماط كل شيء",
   "Pattern-based planning vs. willpower-based planning", "التخطيط بالأنماط مقابل التخطيط بالإرادة", True,
   ["Understand why willpower-based plans fail even when you have willpower",
    "Translate your patterns into plans that stick",
    "Shift from forcing yourself to designing the conditions"],
   ["أن تفهمي لماذا تفشل الخطط القائمة على الإرادة حتى لو امتلكتِها",
    "أن تترجمي أنماطك إلى خطط تصمد",
    "أن تنتقلي من إجبار نفسك إلى تصميم الظروف"]),
]

lesson_html = []
for idx, (no, ten, tar, sen, sar, ready, obj_en, obj_ar) in enumerate(LESSONS):
    pid = "les-%s" % no.replace(".", "-")
    objs = "".join("<li>%s</li>" % L(e, a) for e, a in zip(obj_en, obj_ar))
    lesson_html.append("""<div class="lesson reveal">
  <button class="lesson__btn" type="button" data-accordion aria-expanded="false" aria-controls="%s">
    <span class="lesson__no">%s</span>
    <span>
      <span class="lesson__t">%s</span>
      <span class="lesson__sub">%s</span>
    </span>
    <svg class="lesson__chev" width="18" height="18" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </button>
  <div class="lesson__panel" id="%s">
    <div class="lesson__inner"><div class="lesson__content">
      <h4>%s</h4>
      <ul>%s</ul>
      <p class="small muted">%s</p>
    </div></div>
  </div>
</div>""" % (pid, no, L(ten, tar), L(sen, sar), pid,
             L("What you will be able to do", "ما ستكونين قادرة عليه"),
             objs,
             L("Written and ready &middot; 15&ndash;20 minute read", "مكتوب وجاهز &middot; قراءة ١٥&ndash;٢٠ دقيقة")))

pending = []
for p in PILLARS[2:]:
    pending.append("""<div class="card card--flat">
  <div class="pillar__head">
    <span class="pillar__num" style="background:var(--yellow-wash);border:1px solid var(--yellow-line)">%s</span>
    <span class="tag tag--soon">%s</span>
  </div>
  <h3 class="h3 card__title">%s</h3>
  <p class="card__body">%s</p>
</div>""" % (p["n"], L("In production", "قيد الإنتاج"), L(p["en"], p["ar"]),
             L("Three lessons, same shape as pillars one and two: a teaching, a tool, and a practice exercise you do that week.",
               "ثلاثة دروس بالبنية نفسها في الركيزتين الأولى والثانية: درس، وأداة، وتمرين تطبيقي خلال الأسبوع.")))

COURSE_BODY = pagehead(
    "Self-paced course", "دورة بإيقاعك",
    "The 6-Pillar Realistic Planning course.", "دورة التخطيط الواقعي بالركائز الست.",
    "Thirteen weeks, eighteen lessons, one integration week. Written in Arabic and English, read at your own pace, roughly twenty minutes a lesson.",
    "ثلاثة عشر أسبوعاً، وثمانية عشر درساً، وأسبوع تكامل. مكتوبة بالعربية والإنجليزية، تقرئينها بإيقاعك، نحو عشرين دقيقة للدرس.",
) + """
<section class="sec sec--tight">
  <div class="wrap">
    <div class="grid grid--4">
      %s
    </div>
  </div>
</section>

<section class="sec sec--wash">
  <div class="wrap wrap--mid">
    <p class="eyebrow">%s</p>
    <h2 class="h2">%s</h2>
    <p class="lede" style="margin-top:18px">%s</p>
    <div class="table-scroll mt-l card card--flat" style="padding:0;overflow:hidden">
      <table class="data">
        <thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead>
        <tbody>%s</tbody>
      </table>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap wrap--mid">
    <p class="eyebrow">%s</p>
    <h2 class="h2">%s</h2>
    <p class="lede" style="margin-top:18px;margin-bottom:34px">%s</p>
    %s
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap wrap--mid">
    <p class="eyebrow">%s</p>
    <h2 class="h2">%s</h2>
    <p class="lede" style="margin-top:18px">%s</p>
    <div class="grid grid--2 mt-l">%s</div>
    <div class="card card--flat mt-l" style="border-style:dashed">
      <span class="tag tag--soon">%s</span>
      <h3 class="h3 card__title" style="margin-top:14px">%s</h3>
      <p class="card__body">%s</p>
    </div>
  </div>
</section>
""" % (
    "\n      ".join(
        '<div class="card card--flat reveal"><div class="stat__num">%s</div><p class="card__body" style="margin-top:8px">%s</p></div>'
        % (n, L(e, a)) for n, e, a in [
            ("13", "weeks — one pillar per week plus integration", "أسبوعاً — ركيزة كل أسبوع مع أسبوع تكامل"),
            ("18", "lessons, three per pillar", "درساً، ثلاثة لكل ركيزة"),
            ("6", "of 18 lessons written and ready", "من ١٨ درساً مكتوبة وجاهزة"),
            ("20&#8202;m", "average read per lesson", "دقيقة متوسط قراءة الدرس"),
        ]),

    L("Structure", "البنية"),
    L("How the thirteen weeks are laid out.", "كيف تتوزّع الأسابيع الثلاثة عشر."),
    L("Two weeks of Recall, two of Live, two of Plan &mdash; then a final week where you run the whole cycle once on a real plan of your own.",
      "أسبوعان لـ«تذكّر»، وأسبوعان لـ«تعييش»، وأسبوعان لـ«تخططي» &mdash; ثم أسبوع أخير تديرين فيه الدورة كاملة على خطة حقيقية من عندك."),
    L("Weeks", "الأسابيع"), L("Phase", "المرحلة"), L("Pillar", "الركيزة"), L("Status", "الحالة"),
    "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (w, L(pe, pa), L(le, la), st)
        for w, pe, pa, le, la, st in [
            ("1&ndash;2",  "Recall", "تذكّر", "Observe Without Judgment", "الملاحظة بلا حكم", '<span class="tag">%s</span>' % L("Ready", "جاهزة")),
            ("3&ndash;4",  "Recall", "تذكّر", "Pattern, Not Incident", "النمط مش الحادثة", '<span class="tag">%s</span>' % L("Ready", "جاهزة")),
            ("5&ndash;6",  "Live", "تعييش", "Energy Awareness", "وعي الطاقة", '<span class="tag tag--soon">%s</span>' % L("In production", "قيد الإنتاج")),
            ("7&ndash;8",  "Live", "تعييش", "Full Presence", "الحضور الكامل", '<span class="tag tag--soon">%s</span>' % L("In production", "قيد الإنتاج")),
            ("9&ndash;10", "Plan", "تخططي", "Conscious Decision", "القرار الواعي", '<span class="tag tag--soon">%s</span>' % L("In production", "قيد الإنتاج")),
            ("11&ndash;12","Plan", "تخططي", "Smart Flexibility", "المرونة الذكية", '<span class="tag tag--soon">%s</span>' % L("In production", "قيد الإنتاج")),
            ("13", "Integration", "التكامل", "Run the full cycle on your own plan", "أديري الدورة كاملة على خطتك", '<span class="tag tag--soon">%s</span>' % L("In production", "قيد الإنتاج")),
        ]),

    L("Available now", "المتاح الآن"),
    L("Six lessons you can read today.", "ستة دروس يمكنك قراءتها اليوم."),
    L("Pillars one and two are written in full &mdash; enough to learn to observe honestly and to tell a pattern from a bad Tuesday. Open a lesson to see what it covers.",
      "الركيزتان الأولى والثانية مكتوبتان بالكامل &mdash; ما يكفي لتتعلّمي الملاحظة بصدق وتمييز النمط عن يوم ثلاثاء سيئ. افتحي أي درس لتري ما يتناوله."),
    "\n    ".join(lesson_html),

    L("Coming next", "القادم"),
    L("The remaining four pillars.", "الركائز الأربع المتبقية."),
    L("Lessons 3.1 through 6.3 are being written now, along with a five-question quiz for each of the eighteen lessons.",
      "الدروس من ٣.١ إلى ٦.٣ قيد الكتابة الآن، مع اختبار من خمسة أسئلة لكل درس من الدروس الثمانية عشر."),
    "\n      ".join(pending),
    L("Week 13", "الأسبوع ١٣"),
    L("Integration week", "أسبوع التكامل"),
    L("You take one real plan &mdash; a habit, a project, a season of your life &mdash; and run all six pillars on it from start to finish, with the whole framework in hand.",
      "تأخذين خطة حقيقية واحدة &mdash; عادة، أو مشروعاً، أو مرحلة من حياتك &mdash; وتديرين عليها الركائز الست من البداية للنهاية، والإطار كله بين يديك."),
) + NEWSLETTER

page("course.html", "The 6-Pillar Course — With Nadine",
     "A thirteen-week self-paced course in realistic planning: eighteen bilingual lessons across six pillars, plus an integration week.",
     COURSE_BODY)


def faq(items):
    out = []
    for i, (qe, qa, ae, aa) in enumerate(items):
        pid = "faq-%d" % i
        out.append("""<div class="faq__item">
  <button class="faq__q" type="button" data-accordion aria-expanded="false" aria-controls="%s">
    <span>%s</span><span class="faq__sign" aria-hidden="true"></span>
  </button>
  <div class="faq__panel" id="%s"><div class="faq__inner"><div class="faq__a">%s</div></div></div>
</div>""" % (pid, L(qe, qa), pid, L(ae, aa)))
    return '<div class="faq mt-l">%s</div>' % "".join(out)


# ============================================================= work with me
product_cards = "\n      ".join(
    """<div class="card reveal">
  <div class="pillar__head"><span class="pillar__num">%s</span><span class="pillar__ar">%s</span></div>
  <h3 class="h3 card__title">%s</h3>
  <p class="card__body">%s</p>
  <div class="card__foot"><span class="tag">$9 &middot; $19 &middot; $39</span></div>
</div>""" % (p["n"], p["ar"], p["prod"], L(p["tool_en"], p["tool_ar"])) for p in PILLARS)

WORK_BODY = pagehead(
    "Work with me", "اشتغلي معي",
    "Four ways in, one framework.", "أربع طرق للدخول، وإطار واحد.",
    "Start free, test it for nine dollars, or sit down with me for two hours. Every tier teaches the same six pillars at a different depth — you move up only when you want to.",
    "ابدئي مجاناً، أو جرّبيها بتسعة دولارات، أو اجلسي معي ساعتين. كل مستوى يعلّم الركائز الست نفسها بعمق مختلف — وتصعدين حين تريدين أنت.",
) + """
<section class="sec">
  <div class="wrap">
    <div class="grid grid--4">
      %(tiers)s
    </div>
  </div>
</section>

<section class="sec sec--wash" id="book">
  <div class="wrap split">
    <div>
      <span class="tag tag--ink">%(t3tag)s</span>
      <h2 class="h2" style="margin-top:18px">%(bookh)s</h2>
      <p class="lede" style="margin-top:18px">%(booklede)s</p>
      <div class="price__fig">$199</div>
      <div class="price__unit">%(bookunit)s</div>
      <div class="btn-row">
        <a class="btn btn--primary" href="contact.html#booking">%(bookcta)s</a>
      </div>
      <p class="small muted" style="margin-top:16px">%(booknote)s</p>
    </div>
    <div class="card">
      <p class="h4">%(inch)s</p>
      <ul class="price__list mt-l">%(incl)s</ul>
      <hr>
      <p class="h4" style="margin-top:22px">%(fith)s</p>
      <p class="card__body" style="margin-top:10px">%(fit)s</p>
    </div>
  </div>
</section>

<section class="sec" id="products">
  <div class="wrap">
    <p class="eyebrow">%(peyebrow)s</p>
    <h2 class="h2">%(ph2)s</h2>
    <p class="lede" style="margin-top:18px">%(plede)s</p>
    <div class="grid grid--3 mt-xl">
      %(products)s
    </div>
    <div class="card card--flat mt-l">
      <div class="grid grid--3">
        <div><p class="price__fig" style="font-size:1.7rem">$9</p><p class="card__body">%(pr1)s</p></div>
        <div><p class="price__fig" style="font-size:1.7rem">$19</p><p class="card__body">%(pr2)s</p></div>
        <div><p class="price__fig" style="font-size:1.7rem">$39</p><p class="card__body">%(pr3)s</p></div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--ink" id="groups">
  <div class="wrap wrap--mid">
    <span class="tag tag--ink" style="border-color:var(--yellow)">%(gtag)s</span>
    <h2 class="h2" style="margin-top:18px">%(gh2)s</h2>
    <p class="lede" style="color:#CFC9C0;margin-top:18px">%(glede)s</p>
    <div class="grid grid--2 mt-l">
      <div class="card" style="background:#1D1914;border-color:#2E2922">
        <p class="price__fig" style="color:var(--white)">$297&ndash;$397</p>
        <p class="price__unit">%(g1u)s</p>
        <p class="card__body" style="color:#A8A199">%(g1d)s</p>
      </div>
      <div class="card" style="background:#1D1914;border-color:#2E2922">
        <p class="price__fig" style="color:var(--white)">$797&ndash;$997</p>
        <p class="price__unit">%(g2u)s</p>
        <p class="card__body" style="color:#A8A199">%(g2d)s</p>
      </div>
    </div>
    <div class="btn-row mt-l"><a class="btn btn--primary" href="index.html#newsletter">%(gcta)s</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap wrap--mid">
    <p class="eyebrow">%(feyebrow)s</p>
    <h2 class="h2">%(fh2)s</h2>
    %(faq)s
  </div>
</section>
""" % dict(
    tiers="\n      ".join(
        """<div class="card price reveal"%s>
  <span class="tag%s">%s</span>
  <div class="price__fig">%s</div>
  <div class="price__unit">%s</div>
  <p class="card__body">%s</p>
  <div class="card__foot"><a class="link" href="%s">%s %s</a></div>
</div>""" % (b, tc, L(te, ta), fig, L(ue, ua), L(de, da), href, L(le, la), ARROW)
        for b, tc, te, ta, fig, ue, ua, de, da, href, le, la in [
            ("", "", "Tier 1 — Free", "المستوى ١ — مجاني", "$0",
             "Instagram, blog and the weekly letter", "إنستغرام والمدوّنة والرسالة الأسبوعية",
             "Two short videos a week, a long-form article per pillar, and one teaching letter every week. No catch, no upsell in the first four weeks.",
             "فيديوهان قصيران أسبوعياً، ومقال مطوّل لكل ركيزة، ورسالة تعليمية كل أسبوع. بلا شروط، وبلا عروض بيع في الأسابيع الأربعة الأولى.",
             "index.html#newsletter", "Join the list", "انضمّي للقائمة"),
            ("", "", "Tier 2 — Digital", "المستوى ٢ — رقمي", "$9&ndash;$39",
             "checklists, workbooks, planners", "قوائم، كتيّبات، ومخططات",
             "Bilingual PDFs, one per pillar. A checklist to try a skill, a workbook to practise it, a planner to run the whole quarter on it.",
             "ملفات PDF بلغتين، واحد لكل ركيزة. قائمة لتجربة المهارة، وكتيّب للتدرّب عليها، ومخطط لإدارة ربع سنة كامل بها.",
             "#products", "See the products", "شاهدي المنتجات"),
            (' ' + 'data-badge-en="Most popular" data-badge-ar="الأكثر طلباً"', " tag--ink", "Tier 3 — 1:1", "المستوى ٣ — فردي", "$199",
             "two hours, plus a follow-up", "ساعتان، مع جلسة متابعة",
             "The full framework applied to your actual life, with a written action plan you keep. One flat price, anywhere in the world.",
             "الإطار كاملاً مطبّقاً على حياتك الحقيقية، مع خطة عمل مكتوبة تحتفظين بها. سعر موحّد في أي مكان في العالم.",
             "#book", "Book a session", "احجزي جلسة"),
            ("", " tag--soon", "Tier 4 — Groups", "المستوى ٤ — مجموعات", "$297+",
             "cohorts, opening Q1 2027", "مجموعات، تبدأ الربع الأول ٢٠٢٧",
             "Four-week and twelve-week cohorts. Smaller price than 1:1, and the accountability of moving through it alongside other women.",
             "مجموعات من أربعة أسابيع وأخرى من اثني عشر أسبوعاً. سعر أقل من الجلسة الفردية، ومساءلة جماعية مع نساء أخريات.",
             "#groups", "Join the waiting list", "انضمّي لقائمة الانتظار"),
        ]),

    t3tag=L("Tier 3 &middot; 1:1 Consultation", "المستوى ٣ &middot; استشارة فردية"),
    bookh=L("Two hours, on your actual life.", "ساعتان، على حياتك الحقيقية."),
    booklede=L("This is not a discovery call and it is not a sales call. You come with the plan that keeps failing, and we run all six pillars on it together until we find where it actually breaks.",
               "هذه ليست مكالمة تعارف ولا مكالمة بيع. تأتين بالخطة التي تفشل مراراً، ونُجري عليها الركائز الست معاً حتى نجد أين تنكسر فعلاً."),
    bookunit=L("2-hour session + a free 45-minute follow-up one week later", "جلسة ساعتين + متابعة مجانية ٤٥ دقيقة بعد أسبوع"),
    bookcta=L("Request a booking", "اطلبي موعداً"),
    booknote=L("Held on Zoom, Whereby or by phone, in Arabic or English. No packages &mdash; one session at a time.",
               "تُعقد عبر زووم أو Whereby أو الهاتف، بالعربية أو الإنجليزية. لا باقات &mdash; جلسة واحدة في كل مرة."),
    inch=L("What is included", "ما الذي تتضمنه"),
    incl="".join("<li>%s</li>" % L(e, a) for e, a in [
        ("A pre-session questionnaire so we do not spend the first half hour catching up", "استبيان قبل الجلسة حتى لا نضيّع أول نصف ساعة في التعارف"),
        ("Two hours together, in Arabic or English, whichever you think more clearly in", "ساعتان معاً، بالعربية أو الإنجليزية، بأيّهما تفكّرين بوضوح أكثر"),
        ("A written action plan in your inbox within 24 hours", "خطة عمل مكتوبة في بريدك خلال ٢٤ ساعة"),
        ("A full week of email access afterwards for the questions that surface later", "أسبوع كامل من التواصل بالبريد بعدها، للأسئلة التي تظهر لاحقاً"),
        ("A free 45-minute follow-up call one week on, to adjust what did not hold", "مكالمة متابعة مجانية ٤٥ دقيقة بعد أسبوع، لتعديل ما لم يصمد"),
    ]),
    fith=L("Who this is for", "لمن هذه الجلسة"),
    fit=L("Women who have already tried the apps, the 5 AM club and the colour-coded calendar &mdash; and are tired of concluding that the problem is them. If you want tactical productivity hacks, this is the wrong room.",
          "للنساء اللواتي جرّبن التطبيقات، ونادي الخامسة فجراً، والتقويم الملوّن &mdash; وتعبن من الخلاصة القائلة إن المشكلة فيهن. إن كنت تبحثين عن حيل إنتاجية سريعة، فهذه ليست الغرفة الصحيحة."),

    peyebrow=L("Tier 2", "المستوى ٢"),
    ph2=L("One product per pillar.", "منتج واحد لكل ركيزة."),
    plede=L("Every pillar has its own checklist, workbook and planner &mdash; all bilingual, all instant download. Buy the one pillar you are actually stuck on.",
            "لكل ركيزة قائمتها وكتيّبها ومخططها &mdash; جميعها بلغتين، وجميعها تنزيل فوري. اشتري الركيزة التي تتعثّرين عندها فعلاً."),
    products=product_cards,
    pr1=L("<strong>Checklist</strong> &mdash; one page, one skill. The fastest way to try a pillar.", "<strong>قائمة</strong> &mdash; صفحة واحدة، مهارة واحدة. أسرع طريقة لتجربة ركيزة."),
    pr2=L("<strong>Workbook</strong> &mdash; four to six interactive pages with the exercises worked through.", "<strong>كتيّب</strong> &mdash; من أربع إلى ست صفحات تفاعلية مع التمارين كاملة."),
    pr3=L("<strong>Planner</strong> &mdash; a 60-page bilingual quarterly planner built on all six pillars.", "<strong>مخطط</strong> &mdash; مخطط ربع سنوي من ٦٠ صفحة بلغتين، مبني على الركائز الست."),

    gtag=L("Tier 4 &middot; Coming Q1 2027", "المستوى ٤ &middot; الربع الأول ٢٠٢٧"),
    gh2=L("Do it with other women.", "افعليها مع نساء أخريات."),
    glede=L("Group programs open once the 1:1 practice is steady. Same six pillars, worked in a cohort, at a fraction of the individual price.",
            "تنطلق البرامج الجماعية حين تستقرّ الجلسات الفردية. الركائز الست نفسها، لكن ضمن مجموعة، وبجزء من سعر الجلسة الفردية."),
    g1u=L("4-week cohort &middot; small group, intensive", "مجموعة ٤ أسابيع &middot; صغيرة ومكثّفة"),
    g1d=L("One pillar every few days, live sessions, and a workbook you complete together. For women who want momentum.",
          "ركيزة كل بضعة أيام، وجلسات مباشرة، وكتيّب تكملنه معاً. لمن تريد زخماً سريعاً."),
    g2u=L("12-week cohort &middot; deep integration", "مجموعة ١٢ أسبوعاً &middot; تكامل عميق"),
    g2d=L("The full thirteen-week course run live, with weekly calls and a group that knows your patterns by week four.",
          "الدورة الكاملة من ثلاثة عشر أسبوعاً بشكل مباشر، بمكالمات أسبوعية ومجموعة تعرف أنماطك منذ الأسبوع الرابع."),
    gcta=L("Tell me when it opens", "أخبريني عند الافتتاح"),

    feyebrow=L("Before you book", "قبل أن تحجزي"),
    fh2=L("Questions people actually ask.", "أسئلة يسألها الناس فعلاً."),
    faq=faq([
        ("Which language will the session be in?", "بأي لغة ستكون الجلسة؟",
         "Whichever one you think more clearly in. Nadine works in Levantine Arabic and in English, and it is completely normal to move between the two mid-sentence.",
         "باللغة التي تفكّرين بها بوضوح أكبر. تعمل نادين بالعربية الشامية وبالإنجليزية، ومن الطبيعي تماماً أن تنتقلي بينهما داخل الجملة الواحدة."),
        ("Do I need to have done the course first?", "هل يجب أن أكون أنهيت الدورة أولاً؟",
         "No. The session stands on its own &mdash; the framework gets taught as we apply it. Many people do the reverse and take the course afterwards to keep the practice going.",
         "لا. الجلسة قائمة بذاتها &mdash; يُشرح الإطار أثناء تطبيقه. كثيرات يفعلن العكس ويأخذن الدورة بعدها لمواصلة التمرين."),
        ("Is $199 per session or for a package?", "هل ١٩٩ دولاراً للجلسة أم لباقة؟",
         "Per session, and that price is the same everywhere in the world. It covers the two hours, the written plan, the week of email access and the 45-minute follow-up. There are no packages to buy.",
         "للجلسة الواحدة، والسعر نفسه في كل أنحاء العالم. يشمل الساعتين، والخطة المكتوبة، وأسبوع التواصل بالبريد، ومتابعة الـ٤٥ دقيقة. لا توجد باقات."),
        ("What if my plan falls apart again afterwards?", "ماذا لو انهارت خطتي مرة أخرى بعدها؟",
         "Then you use the sixth pillar, which exists precisely for that. Plans are meant to be rebuilt when reality moves &mdash; the follow-up call one week later is usually where that first rebuild happens.",
         "حينها تستخدمين الركيزة السادسة، وهي موجودة لهذا السبب بالضبط. الخطط تُعاد بناؤها حين يتغيّر الواقع &mdash; وعادةً ما تحدث أول إعادة بناء في مكالمة المتابعة بعد أسبوع."),
        ("Can I buy a digital product without booking a session?", "هل يمكنني شراء منتج رقمي دون حجز جلسة؟",
         "Yes, and most people do. The checklists and workbooks are complete on their own; nothing in them is withheld to push you toward a consultation.",
         "نعم، وهذا ما تفعله الأغلبية. القوائم والكتيّبات كاملة بذاتها؛ ولا شيء فيها محجوب لدفعك نحو حجز استشارة."),
    ]),
)

page("work-with-me.html", "Work With Me — With Nadine",
     "1:1 consultations, bilingual workbooks and planners, and group programs built on the six-pillar realistic planning framework.",
     WORK_BODY)


# ===================================================================== about
ABOUT_BODY = pagehead(
    "About", "عن نادين",
    "I am not the woman who figured planning out.", "أنا لست المرأة التي أتقنت التخطيط.",
    "I am the one who failed at it long enough, and in enough different ways, to stop blaming discipline and start looking at the data.",
    "أنا التي فشلت فيه طويلاً، وبطرق كثيرة مختلفة، حتى توقفت عن لوم الانضباط وبدأت أنظر في البيانات.",
) + """
<section class="sec">
  <div class="wrap split">
    <div class="stack">
      <p class="eyebrow">%(s1e)s</p>
      <h2 class="h2">%(s1h)s</h2>
      <p>%(s1p1)s</p>
      <p>%(s1p2)s</p>
      <p>%(s1p3)s</p>
    </div>
    <div class="card card--flat">
      <p class="h4">%(facth)s</p>
      <div class="steps" style="margin-top:18px">
        %(facts)s
      </div>
    </div>
  </div>
</section>

<section class="sec sec--wash">
  <div class="wrap wrap--mid">
    <p class="eyebrow">%(s2e)s</p>
    <h2 class="h2">%(s2h)s</h2>
    <p class="lede" style="margin-top:18px">%(s2lede)s</p>
    <div class="grid grid--2 mt-l">%(beliefs)s</div>
  </div>
</section>

<section class="sec">
  <div class="wrap wrap--mid">
    <p class="eyebrow">%(s3e)s</p>
    <h2 class="h2">%(s3h)s</h2>
    <p class="lede" style="margin-top:18px">%(s3lede)s</p>
    <div class="grid grid--3 mt-l">%(tone)s</div>
  </div>
</section>

<section class="sec sec--ink">
  <div class="wrap">
    <div class="quote">
      <span class="quote__mark">&ldquo;</span>
      <p class="quote__text">%(q)s</p>
      <p class="quote__by">%(qby)s</p>
    </div>
    <div class="btn-row center mt-xl" style="justify-content:center">
      <a class="btn btn--primary" href="work-with-me.html#book">%(c1)s</a>
      <a class="btn btn--light" href="pillars.html">%(c2)s</a>
    </div>
  </div>
</section>
""" % dict(
    s1e=L("The short version", "النسخة المختصرة"),
    s1h=L("Fifteen years of finding where systems quietly break.", "خمسة عشر عاماً في اكتشاف حيث تنكسر الأنظمة بهدوء."),
    s1p1=L("I spent my career in banking operations, client escalation resolution and process mapping. That work sounds dry from the outside. In practice it is one question asked a thousand different ways: <em>where does this process actually fall apart, as opposed to where everyone assumes it does?</em>",
           "أمضيت حياتي المهنية في عمليات البنوك، ومعالجة تصعيدات العملاء، ورسم مسارات العمل. يبدو هذا العمل جافاً من الخارج. لكنه عملياً سؤال واحد يُطرح بألف صيغة: <em>أين ينهار هذا المسار فعلاً، بخلاف حيث يفترض الجميع أنه ينهار؟</em>"),
    s1p2=L("Meanwhile, in my own life, I was doing the exact thing I would have flagged in a process review: building plans on assumptions I had never checked. I read more than a hundred books on self-development looking for the missing discipline. It was never discipline. It was that I had no honest record of what I actually did with my days.",
           "وفي الوقت نفسه، كنت في حياتي الشخصية أفعل بالضبط ما كنت سأشير إليه في أي مراجعة عمليات: أبني خططاً على افتراضات لم أتحقق منها قط. قرأت أكثر من مئة كتاب في التطوير الذاتي بحثاً عن الانضباط الغائب. لم يكن الانضباط قط. كانت المشكلة أنني لم أملك سجلاً صادقاً لما أفعله بأيامي."),
    s1p3=L("The six pillars came out of closing that gap &mdash; first for myself, then in Arabic, for women who were being told the same thing I had been told: that if the plan failed, they had not wanted it enough.",
           "وُلدت الركائز الست من ردم تلك الفجوة &mdash; لنفسي أولاً، ثم بالعربية، لنساء كان يُقال لهنّ ما قيل لي: إن فشلت الخطة فلأنكِ لم تُرِديها بما يكفي."),
    facth=L("The facts", "الوقائع"),
    facts="\n        ".join(
        '<div class="step"><div class="step__num">%s</div><div><p class="h3 step__t">%s</p><p class="card__body">%s</p></div></div>'
        % (n, L(te, ta), L(de, da)) for n, te, ta, de, da in [
            ("15+", "years in operations", "سنة في العمليات",
             "Banking operations, client escalations and process mapping.", "عمليات بنكية، وتصعيدات العملاء، ورسم مسارات العمل."),
            ("100+", "books read", "كتاب مقروء",
             "Self-development and planning, most of which did not work.", "في التطوير الذاتي والتخطيط، وأغلبها لم ينفع."),
            ("2", "working languages", "لغتا عمل",
             "Levantine Arabic and English, used interchangeably.", "العربية الشامية والإنجليزية، تُستخدمان بالتبادل."),
            ("1", "framework", "إطار واحد",
             "Six pillars, built to be run again and again.", "ست ركائز، مصمّمة لتُدار مراراً وتكراراً."),
        ]),

    s2e=L("What I believe", "ما أؤمن به"),
    s2h=L("Four positions this brand will not move off.", "أربعة مواقف لن تتزحزح عنها هذه العلامة."),
    s2lede=L("The brand exists to defend good habits and challenge harmful trends. That means saying some unpopular things consistently rather than saying popular things loudly.",
             "وُجدت هذه العلامة للدفاع عن العادات الجيدة وتحدّي الموضات المؤذية. وهذا يعني قول أشياء غير رائجة باستمرار، بدل قول الأشياء الرائجة بصوت عالٍ."),
    beliefs="".join(
        '<div class="card card--flat reveal"><h3 class="h3 card__title">%s</h3><p class="card__body">%s</p></div>' % (L(te, ta), L(de, da))
        for te, ta, de, da in [
            ("Observation beats willpower.", "الملاحظة تتفوّق على الإرادة.",
             "Willpower is a limited resource and your body will eventually overrule it. An accurate record of your own behaviour will not.",
             "الإرادة مورد محدود، وجسدك سينقضها في النهاية. أما السجل الدقيق لسلوكك فلن ينقضه شيء."),
            ("A pattern is not an incident.", "النمط ليس حادثة.",
             "One viral moment is not a strategy and one bad week is not an identity. Wait for the third data point before you rewrite the story.",
             "لحظة انتشار واحدة ليست استراتيجية، وأسبوع سيئ واحد ليس هوية. انتظري النقطة الثالثة قبل أن تعيدي كتابة القصة."),
            ("The barrier is rarely time.", "العائق نادراً ما يكون الوقت.",
             "It is usually judgment, pattern-blindness or depleted energy. Time management advice aimed at those three is aimed at the wrong thing.",
             "غالباً هو الحكم، أو العمى عن الأنماط، أو استنزاف الطاقة. ونصائح إدارة الوقت الموجّهة لهذه الثلاثة موجّهة للهدف الخطأ."),
            ("Plans get rebuilt, not abandoned.", "الخطط تُعاد لا تُهجَر.",
             "January is not a magic reset and neither is Monday. When reality moves, you rebuild with the pillars you already have.",
             "يناير ليس إعادة ضبط سحرية، ولا الاثنين كذلك. حين يتغيّر الواقع، تعيدين البناء بالركائز التي تملكينها أصلاً."),
        ]),

    s3e=L("Tone", "النبرة"),
    s3h=L("Calm, measured, honest, direct.", "هادئة، متزنة، صادقة، ومباشرة."),
    s3lede=L("Never hyped. Always practical. If something here sounds like it is trying to sell you urgency, it has gone wrong.",
             "بلا مبالغة أبداً. وعملية دائماً. إن بدا لك أن شيئاً هنا يحاول بيعك الاستعجال، فقد أخطأ الطريق."),
    tone="".join(
        '<div class="card card--flat"><p class="h4">%s</p><p class="card__body" style="margin-top:10px">%s</p></div>' % (L(te, ta), L(de, da))
        for te, ta, de, da in [
            ("Who it is for", "لمن هي",
             "Arabic-speaking women, roughly 25 to 50, in Canada, the Middle East and the diaspora. Professionals, mothers, founders.",
             "نساء ناطقات بالعربية، من ٢٥ إلى ٥٠ تقريباً، في كندا والشرق الأوسط والمهجر. مهنيات وأمهات ومؤسِّسات."),
            ("What they have in common", "ما يجمعهنّ",
             "Good intentions and a history of plans that collapsed. Ambitious, but done with toxic productivity culture.",
             "نوايا طيبة وتاريخ من خطط انهارت. طموحات، لكنهن انتهين من ثقافة الإنتاجية السامة."),
            ("Where I am", "أين أنا",
             "Fredericton, New Brunswick, Canada &mdash; working with clients across time zones, in Arabic and English.",
             "فريدريكتون، نيو برونزويك، كندا &mdash; أعمل مع عميلات عبر مناطق زمنية مختلفة، بالعربية والإنجليزية."),
        ]),

    q=L("I am not asking you to try harder. I am asking you to <mark class=\"hl\">look more honestly</mark> &mdash; and then plan for that person.",
        "أنا لا أطلب منك أن تجتهدي أكثر. أطلب منك أن <mark class=\"hl\">تنظري بصدق أكبر</mark> &mdash; ثم تخطّطي لتلك الإنسانة."),
    qby=L("Nadine", "نادين"),
    c1=L("Book a consultation", "احجزي استشارة"),
    c2=L("Start with the pillars", "ابدئي بالركائز"),
)

page("about.html", "About Nadine — With Nadine",
     "Fifteen years in banking operations and process mapping, over a hundred books on self-development, and one framework for planning that works with reality instead of against it.",
     ABOUT_BODY)


# =================================================================== journal
JOURNAL_BODY = pagehead(
    "Journal", "المدوّنة",
    "One long read per pillar.", "مقال مطوّل لكل ركيزة.",
    "Six bilingual articles, each one taking a single pillar apart properly — the trend it argues with, the part of it that is true, and what to do instead.",
    "ستة مقالات بلغتين، كلٌّ منها يفكّك ركيزة واحدة كما ينبغي — الترند الذي يجادله، والجزء الصحيح منه، وما ينبغي فعله بدلاً عنه.",
) + """
<section class="sec">
  <div class="wrap">
    <div class="grid grid--3">%(cards)s</div>
    <div class="card card--flat mt-xl" style="border-style:dashed;text-align:center">
      <p class="card__body">%(note)s</p>
    </div>
  </div>
</section>
%(newsletter)s
""" % dict(
    cards="".join(
        """<article class="card reveal">
  <div class="pillar__head"><span class="pillar__num">%s</span><span class="tag tag--soon">%s</span></div>
  <h2 class="h3 card__title">%s</h2>
  <p class="card__body">%s</p>
  <div class="card__foot"><span class="small muted">%s</span></div>
</article>""" % (p["n"], L("Coming soon", "قريباً"),
                 L(t_en, t_ar), L(p["long_en"], p["long_ar"]),
                 L("Pillar %s &middot; %s &middot; bilingual" % (p["n"], p["en"]), "الركيزة %s &middot; %s &middot; بلغتين" % (p["n"], p["ar"])))
        for p, t_en, t_ar in zip(PILLARS, [
            "Judgment feels like honesty. It is a shortcut.",
            "You are not a night owl. You had one late Tuesday.",
            "You do not have a time problem.",
            "Busy is not the same as present.",
            "The decision you keep re-making is a three-layer disagreement.",
            "January is not a reset button.",
        ], [
            "الحكم يبدو صدقاً. لكنه اختصار.",
            "أنت لست إنسانة ليلية. كان لديك ثلاثاء واحد متأخر.",
            "مشكلتك ليست في الوقت.",
            "الانشغال ليس هو الحضور.",
            "القرار الذي تعيدين اتخاذه هو خلاف بين ثلاث طبقات.",
            "يناير ليس زرّ إعادة ضبط.",
        ])),
    note=L("The articles are being written alongside the remaining course lessons. Join the letter below and each one arrives the week it goes live &mdash; no separate announcement, no launch noise.",
           "تُكتب المقالات بالتوازي مع دروس الدورة المتبقية. انضمّي للرسالة أدناه ليصلك كل مقال في أسبوع نشره &mdash; بلا إعلانات منفصلة، وبلا ضجيج إطلاق."),
    newsletter=NEWSLETTER,
)

page("journal.html", "Journal — With Nadine",
     "Six long-form bilingual articles, one for each pillar of the realistic planning framework.",
     JOURNAL_BODY)


# =================================================================== contact
CONTACT_BODY = pagehead(
    "Contact", "تواصلي",
    "Say what is actually going on.", "احكي ما يجري فعلاً.",
    "Whether you want to book a session, ask about a workbook, or just check whether this is the right fit — write in Arabic or English, whichever comes first.",
    "سواء أردت حجز جلسة، أو السؤال عن كتيّب، أو حتى التأكّد إن كان هذا مناسباً لك — اكتبي بالعربية أو الإنجليزية، بأيّهما يسبق إلى ذهنك.",
) + """
<section class="sec" id="booking">
  <div class="wrap split" style="align-items:start">
    <div class="card">
      <h2 class="h3">%(fh)s</h2>
      <form class="form mt-l" data-wn-form novalidate>
        <div class="field">
          <label for="c-name">%(fname)s</label>
          <input id="c-name" name="name" type="text" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="c-email">%(femail)s</label>
          <input id="c-email" name="email" type="email" autocomplete="email" required>
        </div>
        <div class="field">
          <label for="c-topic">%(ftopic)s</label>
          <select id="c-topic" name="topic">
            <option>%(o1)s</option>
            <option>%(o2)s</option>
            <option>%(o3)s</option>
            <option>%(o4)s</option>
          </select>
        </div>
        <div class="field">
          <label for="c-msg">%(fmsg)s</label>
          <textarea id="c-msg" name="message" required placeholder="%(fph)s"></textarea>
        </div>
        <button class="btn btn--primary" type="submit">%(fsend)s</button>
        <p class="form__note">%(fnote)s</p>
        <p class="form__msg" role="status" tabindex="-1" hidden></p>
      </form>
    </div>
    <div class="stack">
      <p class="eyebrow">%(de)s</p>
      <h2 class="h2">%(dh)s</h2>
      <p class="lede">%(dl)s</p>
      <div class="card card--flat mt-l">
        <div class="steps">%(details)s</div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--wash">
  <div class="wrap wrap--mid">
    <p class="eyebrow">%(qe)s</p>
    <h2 class="h2">%(qh)s</h2>
    %(faq)s
  </div>
</section>
""" % dict(
    fh=L("Send a message", "أرسلي رسالة"),
    fname=L("Your name", "اسمك"),
    femail=L("Email address", "البريد الإلكتروني"),
    ftopic=L("What is this about?", "ما موضوع رسالتك؟"),
    o1=L("Booking a 1:1 consultation", "حجز استشارة فردية"),
    o2=L("A workbook, checklist or planner", "كتيّب أو قائمة أو مخطط"),
    o3=L("The group programs waiting list", "قائمة انتظار البرامج الجماعية"),
    o4=L("Something else", "شيء آخر"),
    fmsg=L("Your message", "رسالتك"),
    fph=L("You can write in Arabic or English.", "يمكنك الكتابة بالعربية أو الإنجليزية."),
    fsend=L("Send message", "إرسال"),
    fnote=L("Replies usually come within two working days.", "عادةً يصل الرد خلال يومَي عمل."),

    de=L("Details", "تفاصيل"),
    dh=L("How this works in practice.", "كيف يسير الأمر عملياً."),
    dl=L("No automated booking funnel and no discovery call to get through first. You write, Nadine answers, and if a session makes sense you get a time.",
         "لا قمع حجز آلي، ولا مكالمة تعارف عليك اجتيازها أولاً. تكتبين، وتردّ نادين، وإن كانت الجلسة مناسبة تحصلين على موعد."),
    details="".join(
        '<div class="step"><div class="step__num">%s</div><div><p class="h3 step__t">%s</p><p class="card__body">%s</p></div></div>'
        % (n, L(te, ta), L(de_, da)) for n, te, ta, de_, da in [
            ("1", "You write", "تكتبين", "Tell me the plan that keeps failing. Detail helps more than politeness.", "احكي لي عن الخطة التي تفشل باستمرار. التفاصيل تنفع أكثر من التهذيب."),
            ("2", "I reply", "أردّ", "Within about two working days, in the language you wrote in.", "خلال يومَي عمل تقريباً، وباللغة التي كتبت بها."),
            ("3", "We book", "نحجز", "A two-hour slot on Zoom, Whereby or the phone, plus the pre-session questionnaire.", "موعد ساعتين عبر زووم أو Whereby أو الهاتف، مع استبيان ما قبل الجلسة."),
            ("4", "You keep the plan", "تحتفظين بالخطة", "A written action plan within 24 hours, and a follow-up call a week later.", "خطة عمل مكتوبة خلال ٢٤ ساعة، ومكالمة متابعة بعد أسبوع."),
        ]),

    qe=L("Quick answers", "إجابات سريعة"),
    qh=L("Things worth knowing first.", "أمور يُستحسن معرفتها أولاً."),
    faq=faq([
        ("What time zone are sessions in?", "بأي توقيت تُعقد الجلسات؟",
         "Nadine is in Fredericton, New Brunswick (Atlantic time), and books across time zones for clients in the Middle East and the diaspora. Early mornings Atlantic usually work well for Gulf and Levant afternoons.",
         "نادين في فريدريكتون، نيو برونزويك (التوقيت الأطلسي)، وتحجز عبر مناطق زمنية مختلفة لعميلات في الشرق الأوسط والمهجر. عادةً ما تناسب ساعات الصباح الباكر بالتوقيت الأطلسي فترات ما بعد الظهر في الخليج والشام."),
        ("Do you work with men, or only women?", "هل تعملين مع الرجال أم النساء فقط؟",
         "The content and the course are written for Arabic-speaking women, because that is who the examples and the language are built around. The framework itself is not gendered, and 1:1 enquiries are read on their own terms.",
         "المحتوى والدورة مكتوبان للنساء الناطقات بالعربية، لأن الأمثلة واللغة بُنيت حولهنّ. أما الإطار نفسه فليس مرتبطاً بالجنس، وتُقرأ طلبات الجلسات الفردية كلٌّ بحسب حالتها."),
        ("Can I pay in a currency other than USD?", "هل يمكنني الدفع بعملة غير الدولار؟",
         "Pricing is listed in US dollars and payment is taken in USD, so what you pay locally depends on your bank's conversion. The price does not change by country.",
         "الأسعار مدرجة بالدولار الأمريكي والدفع يتم به، لذا يعتمد ما تدفعينه محلياً على سعر التحويل لدى بنكك. لا يتغيّر السعر باختلاف البلد."),
        ("Is anything here medical or therapeutic?", "هل في هذا شيء طبي أو علاجي؟",
         "No. This is coaching in planning and life-skill integration, not therapy or medical advice. If what is in the way is health-related, the honest answer is that you need a clinician, not a planner.",
         "لا. هذا تدريب على التخطيط ودمج مهارات الحياة، وليس علاجاً نفسياً ولا استشارة طبية. وإن كان ما يعيقك متعلقاً بالصحة، فالجواب الصادق أنك تحتاجين إلى مختص طبي لا إلى مخطِّطة."),
    ]),
)

page("contact.html", "Contact — With Nadine",
     "Book a 1:1 consultation, ask about a workbook, or join the group programs waiting list. Write in Arabic or English.",
     CONTACT_BODY)
