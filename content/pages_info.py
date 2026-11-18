# -*- coding: utf-8 -*-
"""Community, business and legal pages."""

LEGAL_UPDATED = "November 18, 2026"


def _form_end(button):
    return ('<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
            '<button class="btn btn-window" type="submit">%s</button><p class="form-status" role="status" aria-live="polite"></p>' % button)


def support(R):
    body = """
<section class="page-head"><div class="wrap"><h1>Support Home.Watch</h1>
<p class="lede">Home.Watch keeps its tools, guides and alerts free for every homeowner. Your support pays for the servers and data feeds, outreach to homeowners who need it, new writers and video creators, and the prizes in our monthly challenge.</p></div></section>
<section class="section"><div class="wrap two-col">
  <div class="prose">
    <h2>Where support goes</h2>
    <div class="alloc">
      <div><span style="--w:35%"></span><p><strong>35% ongoing operations</strong> — hosting, data feeds, tools and maintenance</p></div>
      <div><span style="--w:25%"></span><p><strong>25% promotion and marketing</strong> — reaching seasonal homeowners before they leave</p></div>
      <div><span style="--w:20%"></span><p><strong>20% hiring talent</strong> — writers, video creators and regional experts</p></div>
      <div><span style="--w:20%"></span><p><strong>20% contests and prizes</strong> — rewards for the community's best tips</p></div>
    </div>
    <p>You can direct your support to one purpose in the form. Home.Watch is an independent business, not a registered charity, so contributions are not tax-deductible.</p>
    <h2>Other ways to help</h2>
    <ul>
      <li>Share a guide with a neighbor who is about to leave for the season</li>
      <li>Enter the <a href="contests.html">Away-Ready Home Challenge</a> with your best tip</li>
      <li><a href="advertise.html">Sponsor a prize</a> or a tool if you run a business</li>
      <li>Tell us about an error or a topic we should cover through the <a href="contact.html">contact form</a></li>
    </ul>
  </div>
  <div>
    <div class="pay-buttons" data-pay-buttons hidden><h2>Give now</h2><div class="pay-row" data-pay-row></div></div>
    <form class="card-form" data-form="support" data-subject="Support pledge — Home.Watch" novalidate>
      <h2 class="form-title">Pledge your support</h2>
      <p class="field-label" id="amt-label">Amount (USD)</p>
      <div class="chip-list amount-chips" role="radiogroup" aria-labelledby="amt-label">
        <label class="chip-radio"><input type="radio" name="amount" value="10"><span>$10</span></label>
        <label class="chip-radio"><input type="radio" name="amount" value="25" checked><span>$25</span></label>
        <label class="chip-radio"><input type="radio" name="amount" value="50"><span>$50</span></label>
        <label class="chip-radio"><input type="radio" name="amount" value="100"><span>$100</span></label>
        <label class="chip-radio"><input type="radio" name="amount" value="250"><span>$250</span></label>
        <label class="chip-radio"><input type="radio" name="amount" value="custom"><span>Other</span></label>
      </div>
      <div class="field"><label for="sp-custom">Other amount</label><input id="sp-custom" name="custom_amount" inputmode="decimal" placeholder="e.g. 75"></div>
      <div class="field-row">
        <div class="field"><label for="sp-freq">How often</label><select id="sp-freq" name="frequency"><option>One time</option><option>Monthly</option><option>Yearly</option></select></div>
        <div class="field"><label for="sp-purpose">Use it for</label><select id="sp-purpose" name="purpose"><option>Where it's needed most</option><option>Ongoing operations</option><option>Promotions and marketing</option><option>Hiring talent</option><option>Contests and prizes</option></select></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="sp-name">Name</label><input id="sp-name" name="name" required autocomplete="name"></div>
        <div class="field"><label for="sp-email">Email</label><input id="sp-email" name="email" type="email" required autocomplete="email"></div>
      </div>
      <div class="field"><label for="sp-msg">Message (optional)</label><textarea id="sp-msg" name="message" rows="3"></textarea></div>
      <label class="check"><input type="checkbox" name="recognition" value="yes"> List my name on the supporters page</label>
      <p class="fine">We'll email you a secure payment link to complete your pledge. No card details are collected on this page.</p>
      """ + _form_end("Send my pledge") + """
    </form>
  </div>
</div></section>"""
    R["page"]("support.html", "Support Home.Watch", "Help keep Home.Watch's tools, guides and live alerts free: support operations, promotion, hiring and community prizes.",
              body, active="support", priority="0.5", crumbs=[("Support", "support.html")])


def contests(R):
    import datetime
    month = datetime.date.today().strftime("%B %Y")
    body = f"""
<section class="page-head page-head-night"><div class="wrap"><h1>The Away-Ready Home Challenge</h1>
<p class="lede">Every month we award prizes for the most useful tip, checklist or story about protecting a home while you're away. This month's challenge: <strong>{month}</strong>.</p>
<p><a class="btn btn-window btn-lg" href="#enter">Enter this month</a></p></div></section>
<section class="section"><div class="wrap two-col">
  <div class="prose">
    <h2>Prizes this month</h2>
    <ul class="prize-list">
      <li><strong>Winner</strong> — a smart water leak and freeze sensor kit or a US$150 gift card, the winner's choice</li>
      <li><strong>Two runners-up</strong> — a US$50 gift card each</li>
      <li><strong>Featured entries</strong> — published on Home.Watch with credit</li>
    </ul>
    <h2>What we're looking for</h2>
    <p>A practical tip that saved you money or trouble, a closing-up checklist that works for your home, or a short story about what happened while you were away and what you learned. Home watch professionals are welcome to enter.</p>
    <h2>How entries are judged</h2>
    <table><thead><tr><th scope="col">Criterion</th><th scope="col">Weight</th></tr></thead><tbody>
      <tr><td>Usefulness to other homeowners</td><td>40%</td></tr><tr><td>Clarity and detail</td><td>30%</td></tr><tr><td>Originality</td><td>30%</td></tr></tbody></table>
    <p>Want your business to give the prize? <a href="advertise.html">Sponsor a month</a>.</p>
  </div>
  <form class="card-form" id="enter" data-form="contest" data-subject="Away-Ready Home Challenge entry — Home.Watch" novalidate>
    <h2 class="form-title">Enter the challenge</h2>
    <div class="field-row">
      <div class="field"><label for="ct-name">Name</label><input id="ct-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="ct-email">Email</label><input id="ct-email" name="email" type="email" required autocomplete="email"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="ct-where">City and state or province</label><input id="ct-where" name="location" required></div>
      <div class="field"><label for="ct-type">Entry type</label><select id="ct-type" name="entry_type"><option>Tip</option><option>Checklist</option><option>Story</option></select></div>
    </div>
    <div class="field"><label for="ct-title">Title</label><input id="ct-title" name="title" required maxlength="120"></div>
    <div class="field"><label for="ct-entry">Your entry (up to 500 words)</label><textarea id="ct-entry" name="entry" rows="7" required data-maxwords="500"></textarea><p class="fine" data-wordcount>0 / 500 words</p></div>
    <div class="field"><label for="ct-photo">Photo link (optional)</label><input id="ct-photo" name="photo_link" type="url" placeholder="https://"></div>
    <label class="check"><input type="checkbox" name="age" value="18+" required> I am 18 or older and the entry is my own original work.</label>
    <label class="check"><input type="checkbox" name="rules" value="accepted" required> I accept the official rules below.</label>
    {_form_end("Submit my entry")}
  </form>
</div></section>
<section class="section section-fog"><div class="wrap narrow prose" id="rules">
  <h2>Official rules</h2>
  <p><strong>No purchase or payment necessary to enter or win.</strong> A purchase does not improve your chances. This is a skill contest; winners are chosen by judging, not by chance.</p>
  <ol>
    <li><strong>Organizer.</strong> Home.Watch ("Organizer").</li>
    <li><strong>Eligibility.</strong> Open to legal residents of the United States and Canada who are 18 or older (19 where that is the age of majority). Residents of Quebec are excluded unless a given month's contest page states otherwise. Employees of the Organizer and prize sponsors and their immediate families are not eligible. Void where prohibited.</li>
    <li><strong>Entry period.</strong> Each monthly contest opens on the first day of the month at 12:00 a.m. Eastern Time and closes on the last day of the month at 11:59 p.m. Eastern Time.</li>
    <li><strong>How to enter.</strong> Submit the entry form on this page. Limit one entry per person per month. Entries must be original, in English or French, no longer than 500 words and must not contain anyone else's personal information.</li>
    <li><strong>Judging.</strong> Entries are judged by the Organizer's editorial team using the criteria above. Judges' decisions are final.</li>
    <li><strong>Prizes.</strong> As listed for the month. No cash alternative except at the Organizer's discretion; the Organizer may substitute a prize of equal or greater value. Prizes are not transferable. Winners are responsible for applicable taxes.</li>
    <li><strong>Notification.</strong> Winners are notified by email within 14 days after the contest closes and must reply within 14 days or an alternate winner may be selected. Canadian residents must correctly answer a time-limited mathematical skill-testing question before being declared a winner.</li>
    <li><strong>License.</strong> By entering, you grant the Organizer a non-exclusive, royalty-free license to publish, edit and display your entry with credit on Home.Watch and its channels.</li>
    <li><strong>Privacy.</strong> Personal information is used to administer the contest as described in the <a href="privacy.html">privacy policy</a>.</li>
    <li><strong>General.</strong> The Organizer may cancel, suspend or modify a contest if fraud, technical failure or other causes beyond its control affect its integrity. Released parties are not responsible for late, lost or incomplete entries.</li>
  </ol>
</div></section>"""
    R["page"]("contests.html", "Away-Ready Home Challenge: Monthly Contest and Prizes",
              "Share your best tip, checklist or story about protecting a home while you're away and win monthly prizes. Official rules included.",
              body, active="contests", priority="0.5", crumbs=[("Contests", "contests.html")])


def careers(R):
    roles = [
        ("Contributing writer", "Remote, freelance", "Write practical guides for absentee homeowners on insurance, home systems, storms and regional topics. Experience in home inspection, insurance, property management or home watch is a plus."),
        ("Video creator", "Remote, freelance", "Produce short how-to videos: closing up a house, setting up leak sensors, storm preparation and visit walk-throughs."),
        ("Regional home watch expert", "Florida, Arizona, Texas, the Carolinas, mountain and lake regions", "Review regional guides, answer homeowner questions and share local knowledge. Ideal for experienced home watch professionals."),
        ("Partnerships manager", "Remote, commission-based", "Build relationships with home watch businesses, insurers, realtors, HOAs and sensor makers."),
        ("Community moderator", "Remote, part-time", "Review contest entries and homeowner submissions and keep our community helpful and safe."),
    ]
    esc = R["esc"]
    cards = "".join('<li><strong>%s</strong><span class="muted">%s</span><span>%s</span></li>' % (esc(a), esc(b), esc(c)) for a, b, c in roles)
    opts = "".join("<option>%s</option>" % esc(a) for a, _, _ in roles) + "<option>Something else</option>"
    body = f"""
<section class="page-head"><div class="wrap"><h1>Work with Home.Watch</h1>
<p class="lede">We're building the most useful resource for people whose homes sit empty. We work with independent writers, creators and industry experts across the US and Canada.</p></div></section>
<section class="section"><div class="wrap two-col">
  <div><h2 class="section-title">Open roles</h2><ul class="role-list">{cards}</ul></div>
  <form class="card-form" data-form="careers" data-subject="Talent application — Home.Watch" novalidate>
    <h2 class="form-title">Apply</h2>
    <div class="field-row">
      <div class="field"><label for="cr-name">Name</label><input id="cr-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="cr-email">Email</label><input id="cr-email" name="email" type="email" required autocomplete="email"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="cr-role">Role</label><select id="cr-role" name="role">{opts}</select></div>
      <div class="field"><label for="cr-loc">Location</label><input id="cr-loc" name="location" autocomplete="address-level2"></div>
    </div>
    <div class="field"><label for="cr-link">Portfolio, LinkedIn or website</label><input id="cr-link" name="portfolio" type="url" placeholder="https://"></div>
    <div class="field"><label for="cr-avail">Availability</label><select id="cr-avail" name="availability"><option>A few hours a week</option><option>Part-time</option><option>Project-based</option><option>Full-time</option></select></div>
    <div class="field"><label for="cr-msg">Why you'd be a great fit</label><textarea id="cr-msg" name="message" rows="5" required></textarea></div>
    {_form_end("Send application")}
  </form>
</div></section>"""
    R["page"]("careers.html", "Careers and Talent at Home.Watch", "Freelance and part-time roles for writers, video creators, regional home watch experts, partnership managers and moderators.",
              body, active="careers", priority="0.4", crumbs=[("Careers", "careers.html")])


def advertise(R):
    pk = [
        ("Site-wide sponsor", "from $499 / month", "Your brand on every page's sponsor slot, the newsletter and the live alerts page."),
        ("Tool sponsor", "from $199 / month", "\"Presented by\" placement on one interactive tool, such as the cost estimator or weather watch."),
        ("Regional sponsor", "from $149 / month", "Exclusive sponsor placement on one regional guide."),
        ("Newsletter sponsor", "from $99 / issue", "A sponsored message in the monthly away-home briefing."),
        ("Contest prize sponsor", "cash or in-kind", "Provide the monthly prize and get featured on the contest page and winner announcement."),
        ("Custom partnership", "let's talk", "Co-branded guides, data partnerships, insurer or HOA programs, and affiliate partnerships."),
    ]
    esc = R["esc"]
    cards = "".join('<li><strong>%s</strong><span class="price">%s</span><span>%s</span></li>' % (esc(a), esc(b), esc(c)) for a, b, c in pk)
    checks = "".join('<label class="check"><input type="checkbox" name="interest" value="%s"> %s</label>' % (esc(a), esc(a)) for a, _, _ in pk)
    body = f"""
<section class="page-head"><div class="wrap"><h1>Advertise and sponsor</h1>
<p class="lede">Reach seasonal homeowners, second-home owners and home watch professionals at the moment they plan to protect an empty house.</p></div></section>
<section class="section"><div class="wrap two-col">
  <div>
    <h2 class="section-title">Packages</h2><ul class="role-list">{cards}</ul>
    <p class="fine">Sponsored placements are always labeled. Sponsors never influence editorial content or provider matching. Display ads are served by Google AdSense.</p>
  </div>
  <form class="card-form" data-form="advertise" data-subject="Advertising or sponsorship inquiry — Home.Watch" novalidate>
    <h2 class="form-title">Request the media kit</h2>
    <div class="field-row">
      <div class="field"><label for="ad-co">Company</label><input id="ad-co" name="company" required autocomplete="organization"></div>
      <div class="field"><label for="ad-name">Your name</label><input id="ad-name" name="name" required autocomplete="name"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="ad-email">Email</label><input id="ad-email" name="email" type="email" required autocomplete="email"></div>
      <div class="field"><label for="ad-phone">Phone</label><input id="ad-phone" name="phone" type="tel" autocomplete="tel"></div>
    </div>
    <div class="field"><label for="ad-site">Website</label><input id="ad-site" name="website" type="url" placeholder="https://"></div>
    <p class="field-label">Interested in</p><div class="check-grid">{checks}</div>
    <div class="field"><label for="ad-budget">Monthly budget</label><select id="ad-budget" name="budget"><option>Under $250</option><option>$250–$1,000</option><option>$1,000–$5,000</option><option>$5,000+</option></select></div>
    <div class="field"><label for="ad-msg">Goals</label><textarea id="ad-msg" name="message" rows="4"></textarea></div>
    {_form_end("Request media kit")}
  </form>
</div></section>"""
    R["page"]("advertise.html", "Advertise and Sponsor on Home.Watch", "Sponsorship and advertising packages reaching seasonal homeowners and home watch professionals.",
              body, active="advertise", priority="0.5", crumbs=[("Advertise", "advertise.html")])


def about(R):
    body = """
<section class="page-head"><div class="wrap"><h1>About Home.Watch</h1><p class="lede">Helping people protect the homes they leave behind.</p></div></section>
<section class="section"><div class="wrap narrow prose">
<p>Millions of homes sit empty for weeks or months every year: seasonal homes in the sun, cottages and ski houses in winter, the northern homes that snowbirds leave behind, houses on the market after a move, and family homes waiting for an estate to settle. An empty house is where small problems become expensive ones.</p>
<p>Home.Watch brings together what owners of those homes need in one place: practical guides, free planning tools, live weather and safety alerts, and an easy way to find a home watch professional who can check on the property in person.</p>
<h2>What we do</h2>
<ul>
<li><strong>Guides</strong> written in plain language and reviewed regularly. See our <a href="editorial-policy.html">editorial policy</a>.</li>
<li><strong>Tools</strong> for estimating costs, scoring risk, building checklists, watching the weather, tracking insurance dates and writing visit reports.</li>
<li><strong>Live alerts</strong> from public sources such as the National Weather Service, FEMA and the Consumer Product Safety Commission, refreshed automatically.</li>
<li><strong>Matching</strong> between homeowners and independent home watch providers.</li>
</ul>
<h2>How we make money</h2>
<p>Everything is free for homeowners. We earn revenue from display advertising served by Google AdSense, from home watch providers who pay for listings or requests, from clearly labeled sponsorships, and from readers who choose to <a href="support.html">support us</a>. Advertisers and sponsors do not influence our guides or our matching.</p>
<h2>Independence</h2>
<p>Home.Watch is an independent website. We are not affiliated with any franchise, home care company, security company, trade association, insurer or manufacturer. See the <a href="trademark.html">trademark and copyright notice</a>.</p>
<h2>Get in touch</h2>
<p>Questions, corrections and partnership ideas are welcome through our <a href="contact.html">contact form</a>.</p>
</div></section>"""
    R["page"]("about.html", "About Home.Watch", "Home.Watch is an independent resource for people whose homes sit empty: guides, tools, live alerts and home watch matching.",
              body, active="about", priority="0.5", crumbs=[("About", "about.html")])


def contact(R):
    body = """
<section class="page-head"><div class="wrap"><h1>Contact Home.Watch</h1><p class="lede">Send us a message and we'll reply by email, usually within two business days.</p></div></section>
<section class="section"><div class="wrap two-col">
  <form class="card-form" data-form="contact" data-subject="Contact form — Home.Watch" novalidate>
    <div class="field-row">
      <div class="field"><label for="cf-name">Name</label><input id="cf-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" required autocomplete="email"></div>
    </div>
    <div class="field"><label for="cf-topic">Topic</label><select id="cf-topic" name="topic">
      <option>General question</option><option>Help finding a home watch provider</option><option>Provider listing</option>
      <option>Advertising or sponsorship</option><option>Partnership</option><option>Website or domain inquiry</option><option>Media</option>
      <option>Report an error</option><option>Privacy request</option></select></div>
    <div class="field"><label for="cf-msg">Message</label><textarea id="cf-msg" name="message" rows="6" required></textarea></div>
    <label class="check"><input type="checkbox" name="consent" value="yes" required> I agree that Home.Watch may use these details to reply to me.</label>
    """ + _form_end("Send message") + """
  </form>
  <div class="prose">
    <h2>Looking for something specific?</h2>
    <ul>
      <li>Need a provider? <a href="find-a-pro.html">Get matched</a> — it's faster.</li>
      <li>Run a home watch business? <a href="for-pros.html">Apply to be listed</a>.</li>
      <li>Advertising? See <a href="advertise.html">packages</a>.</li>
      <li>Common questions are answered in the <a href="faq.html">FAQ</a>.</li>
    </ul>
    <p class="fine">For emergencies at your property, call local emergency services. Home.Watch does not dispatch help.</p>
  </div>
</div></section>"""
    R["page"]("contact.html", "Contact Home.Watch", "Contact Home.Watch with questions, corrections, listing, advertising or partnership inquiries.",
              body, active="contact", priority="0.5", crumbs=[("Contact", "contact.html")])


FAQ = [
    ("Homeowners", [
        ("What is home watch?", "A scheduled, documented visual inspection of a home while the owner is away, with reports and help coordinating repairs if something goes wrong."),
        ("How much does it cost?", "Weekly visits for an average home commonly run about $100–$250 per month. Use the cost estimator for a range that fits your home."),
        ("How often should my home be checked?", "Every 7–14 days is common for empty homes. Hot, humid and freezing climates usually call for weekly visits."),
        ("Is the matching service free?", "Yes. Homeowners never pay Home.Watch. Providers pay to be listed or to receive requests."),
        ("Do you vet providers?", "Providers confirm their insurance, bonding and background checks when they apply. You should still ask for certificates before hiring."),
        ("Will my information be sold?", "No. Request details are shared only with the providers you're matched with, as described in our privacy policy."),
        ("Do you cover Canada?", "Yes. Requests are accepted across the US and Canada. Live weather alerts cover the US; the freeze board includes major Canadian cities."),
    ]),
    ("Home watch professionals", [
        ("How do I get listed?", "Apply on the For pros page. We review applications and confirm your details before your profile goes live."),
        ("What does it cost?", "A basic listing is free. Featured and exclusive-area plans and pay-per-lead options are available."),
        ("Can I use your visit report tool with clients?", "Yes. The Visit Report Builder is free to use and print."),
    ]),
    ("About the site", [
        ("Where does the alert data come from?", "Weather alerts come from the National Weather Service, disaster declarations from FEMA, recalls from the Consumer Product Safety Commission and forecasts for the freeze board from MET Norway."),
        ("How often is the site updated?", "Data feeds refresh automatically every day, and guides are reviewed on a regular schedule."),
        ("Is the information here insurance or legal advice?", "No. It is general information. Talk to your insurance agent, attorney or other professional about your situation."),
        ("How can I support the site?", "Visit the Support page, enter the monthly challenge or share a guide."),
    ]),
]


def faq(R):
    esc = R["esc"]
    blocks, entities = [], []
    for group, qa in FAQ:
        blocks.append("<h2>%s</h2>%s" % (esc(group), "".join("<details><summary>%s</summary><p>%s</p></details>" % (esc(q), esc(a)) for q, a in qa)))
        entities += [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]
    body = '<section class="page-head"><div class="wrap"><h1>Frequently asked questions</h1></div></section><section class="section"><div class="wrap narrow faq">%s</div></section>' % "".join(blocks)
    R["page"]("faq.html", "Home Watch FAQ", "Answers for homeowners and home watch professionals about costs, visit frequency, matching, data sources and privacy.",
              body, active="faq", priority="0.6", schema={"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities},
              crumbs=[("FAQ", "faq.html")])


def legal(R, path, title, desc, html, crumb):
    body = '<section class="page-head"><div class="wrap"><h1>%s</h1><p class="muted">Last updated %s</p></div></section><section class="section"><div class="wrap narrow prose">%s</div></section>' % (
        R["esc"](title), LEGAL_UPDATED, html)
    R["page"](path, title, desc, body, priority="0.3", crumbs=[(crumb, path)])


PRIVACY = """
<p>This policy explains what information Home.Watch ("we", "us") collects, how we use and share it, and the choices you have. It applies to home.watch and its pages.</p>
<h2>Information you give us</h2>
<p>When you use a form — a match request, provider application, contact message, newsletter or reminder signup, contest entry, job application, sponsorship inquiry or support pledge — we collect the details you enter, such as your name, email, phone number, property location and the information about your home and schedule you choose to share.</p>
<p>Form submissions are transmitted through FormSubmit, a third-party form-processing service, which delivers them to our private inbox. Please do not include sensitive information such as alarm codes, account numbers or government ID numbers in any form.</p>
<h2>How we use it</h2>
<ul>
<li>To answer your message or request</li>
<li>To match you with home watch providers, if you ask us to</li>
<li>To send reminders and newsletters you sign up for (you can unsubscribe at any time)</li>
<li>To administer contests, applications and sponsorships</li>
<li>To keep the site secure and improve it</li>
</ul>
<h2>When we share it</h2>
<p>If you submit a match request, we share the details of your request with up to three independent home watch providers who cover your area, so they can contact you. Those providers handle your information under their own privacy practices. We do not sell your personal information, and we do not share it with advertisers.</p>
<p>We may also disclose information if required by law, to protect our rights or users, or as part of a business transfer.</p>
<h2>Advertising and Google AdSense</h2>
<p>We use Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to our site and other sites on the internet.</p>
<p>You can opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a>, and you can opt out of some third-party vendors' use of cookies for personalized advertising at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a> or, in Canada, <a href="https://youradchoices.ca/" target="_blank" rel="noopener">youradchoices.ca</a>. Learn <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses information from sites that use its services</a>.</p>
<p>Where required by law, such as in the European Economic Area, the UK and Switzerland, consent for personalized ads is requested through a consent message before such cookies are used.</p>
<h2>Cookies and browser storage</h2>
<p>We use a small amount of browser storage to remember your theme, cookie choice, checklist ticks and report drafts. These stay on your device. See our <a href="cookies.html">cookie policy</a>.</p>
<h2>Third-party content</h2>
<p>Videos are embedded from YouTube only after you press play, using YouTube's privacy-enhanced mode. Weather data is requested from the National Weather Service when you use the weather tools. Fonts are loaded from Google Fonts. These services may receive your IP address.</p>
<h2>Your rights</h2>
<p>Depending on where you live — including under the GDPR, the California Consumer Privacy Act as amended, Canada's PIPEDA and Quebec's Law 25 — you may have the right to access, correct, delete or port your personal information, to withdraw consent and to object to certain processing. To make a request, use the <a href="contact.html">contact form</a> and choose "Privacy request". We will respond within the time required by law.</p>
<h2>Retention and security</h2>
<p>We keep personal information only as long as needed for the purposes above or as required by law, and use reasonable safeguards to protect it. No method of transmission over the internet is completely secure.</p>
<h2>Children</h2>
<p>Home.Watch is intended for adults. We do not knowingly collect information from children under 16.</p>
<h2>Changes</h2>
<p>We may update this policy. The date at the top shows when it last changed.</p>
"""

TERMS = """
<p>By using home.watch (the "Site") you agree to these terms. If you do not agree, please do not use the Site.</p>
<h2>What the Site provides</h2>
<p>The Site offers general information, tools, data from public sources and a service that connects homeowners with independent home watch providers. Home.Watch does not provide home watch, inspection, security, insurance or legal services itself.</p>
<h2>Independent providers</h2>
<p>Providers listed on or matched through the Site are independent businesses. They are not our employees or agents. We do not guarantee their work, licensing, insurance or availability. You are responsible for checking credentials and agreeing terms directly with any provider you hire.</p>
<h2>No professional advice</h2>
<p>Content and tool results are for general information only and are not insurance, legal, financial, engineering or other professional advice. Weather and alert information may be delayed or incomplete; always follow official warnings and instructions.</p>
<h2>Your submissions</h2>
<p>You agree that information you submit is accurate and that you have the right to share it. For contest entries, tips and other content you submit for publication, you grant Home.Watch a non-exclusive, royalty-free, worldwide license to use, edit and publish it with credit.</p>
<h2>Acceptable use</h2>
<p>Do not misuse the Site: no spam, false requests, scraping that harms performance, attempts to break security, or content that is unlawful, infringing or abusive.</p>
<h2>Intellectual property</h2>
<p>The Site's text, design, tools and code are owned by Home.Watch and protected by copyright. Third-party trademarks belong to their owners. See the <a href="trademark.html">trademark and copyright notice</a>.</p>
<h2>Contests and payments</h2>
<p>Contests are governed by their <a href="contests.html#rules">official rules</a>. Support pledges and provider plans are completed through separate payment links and their terms.</p>
<h2>Disclaimer and limitation of liability</h2>
<p>The Site is provided "as is" without warranties of any kind. To the fullest extent permitted by law, Home.Watch is not liable for indirect, incidental or consequential damages, or for any loss arising from your use of the Site, its data or any provider.</p>
<h2>Changes and governing law</h2>
<p>We may update these terms at any time. These terms are governed by the laws of the jurisdiction in which the Site's operator is established, without regard to conflict-of-laws rules.</p>
"""

DISCLAIMER = """
<h2>General information only</h2>
<p>Everything on Home.Watch — guides, tool results, cost estimates, risk scores and checklists — is general information. It is not insurance, legal, tax, financial, engineering or professional advice, and it is not a substitute for an in-person inspection. Speak with a qualified professional about your situation.</p>
<h2>Insurance</h2>
<p>Policy terms such as vacancy and unoccupancy conditions differ between insurers, policies and jurisdictions. Only your policy and your insurer determine coverage.</p>
<h2>Weather, disaster and recall data</h2>
<p>Data comes from public sources including the National Weather Service, FEMA, the U.S. Consumer Product Safety Commission and MET Norway, and may be delayed, incomplete or changed by the source. Always follow official warnings and instructions from local authorities.</p>
<h2>Providers</h2>
<p>Home watch providers are independent businesses. A listing or match is not an endorsement or guarantee. Verify insurance, bonding, licensing and references before hiring.</p>
<h2>Advertising and sponsorship</h2>
<p>Home.Watch earns revenue from Google AdSense display ads, provider listings, labeled sponsorships and reader support. These relationships do not influence editorial content. If we add affiliate links in the future, they will be disclosed where they appear.</p>
<h2>External links and videos</h2>
<p>Links and embedded videos lead to third-party sites and creators. We do not control and are not responsible for their content, products or practices.</p>
"""

COOKIES = """
<p>This policy explains how Home.Watch uses cookies and similar browser storage.</p>
<h2>Essential storage</h2>
<ul>
<li><strong>hw-theme</strong> — remembers light or dark mode</li>
<li><strong>hw-consent</strong> — remembers your cookie choice</li>
<li><strong>hw-checklist, hw-report</strong> — save your checklist ticks and report drafts on your device</li>
<li><strong>hw-slidein</strong> — remembers that you closed the reminder offer</li>
</ul>
<p>These stay in your browser and are never sent to us.</p>
<h2>Advertising cookies</h2>
<p>Google AdSense and its partners may set cookies to show ads, measure performance and, where permitted, personalize ads based on your visits to this and other websites. Manage personalization at <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>.</p>
<h2>Third-party services</h2>
<p>YouTube videos load only after you press play and use the privacy-enhanced youtube-nocookie.com domain. Google Fonts serves the site's typefaces.</p>
<h2>Your choices</h2>
<p>Use the banner to choose essential-only or all cookies. You can change your choice at any time below, and you can block or delete cookies in your browser settings.</p>
<p><button class="btn btn-ghost btn-sm" type="button" data-reset-consent>Change my cookie choice</button></p>
"""

TRADEMARK = """
<h2>Independent website</h2>
<p>Home.Watch is an independent information, tools and referral website operating on the domain name home.watch. The name describes what the site is about — watching over homes — and is used in a descriptive sense.</p>
<h2>No affiliation</h2>
<p>Home.Watch is <strong>not affiliated with, endorsed by, sponsored by or connected to</strong> any company, franchise, home care provider, security company, trade association, certification body, insurer, software vendor or product brand, including any business or mark that contains the words "home watch", "homewatch" or similar terms. Any similarity in name is coincidental and descriptive.</p>
<h2>Third-party trademarks</h2>
<p>All product names, company names, logos and trademarks mentioned on this site, in embedded videos or in linked content are the property of their respective owners. They are used for identification and informational purposes only, and their use does not imply endorsement.</p>
<h2>Copyright</h2>
<p>Unless stated otherwise, the text, page designs, graphics, tools and source code of Home.Watch are &copy; Home.Watch, all rights reserved. You may link to our pages and quote brief excerpts with attribution and a link. Republishing full guides or copying tools requires written permission.</p>
<p>Public data from the National Weather Service, FEMA and the U.S. Consumer Product Safety Commission is used under their public-domain terms. Forecast data for the freeze board is provided by MET Norway under the Creative Commons Attribution 4.0 license. Embedded YouTube videos remain the property of their creators.</p>
<h2>Copyright concerns</h2>
<p>If you believe content on this site infringes your rights, send a notice through our <a href="contact.html">contact form</a> identifying the work, the page and your contact details. We will review and respond promptly.</p>
"""

EDITORIAL = """
<h2>Our standards</h2>
<p>Home.Watch guides are written to be practical, accurate and easy to act on. We base them on public sources — the National Weather Service, FEMA, the Consumer Product Safety Commission, insurer and industry publications and manufacturer documentation — and on the established practices of the home watch industry.</p>
<h2>Independence</h2>
<p>Advertisers, sponsors and listed providers do not review or approve our guides. Sponsored content, if any, is clearly labeled.</p>
<h2>Accuracy and updates</h2>
<p>Each guide shows when it was last updated. We review guides regularly and whenever rules, seasons or best practices change. Data on the live alerts page refreshes automatically every day.</p>
<h2>Corrections</h2>
<p>Found an error? Tell us through the <a href="contact.html">contact form</a> with "Report an error" as the topic. We correct mistakes promptly and note significant changes.</p>
<h2>Tools and AI</h2>
<p>We use software tools, which may include AI, to help with research, drafting and data processing. Every published guide is reviewed by a person on our editorial team before it goes live.</p>
"""


def sitemap_page(R):
    esc = R["esc"]
    groups = [
        ("Main", [("index.html", "Home"), ("find-a-pro.html", "Get matched"), ("for-pros.html", "For pros"), ("alerts.html", "Live alerts"),
                  ("videos.html", "Videos"), ("faq.html", "FAQ")]),
        ("Tools", [("tools/index.html", "All tools")] + [("tools/%s.html" % s, t) for s, t, _ in __import__("content.pages", fromlist=["TOOLS"]).TOOLS]),
        ("Guides", [("guides/index.html", "All guides")] + [("guides/%s.html" % g["slug"], g["title"]) for g in R["GUIDES"]]),
        ("Regions", [("regions/index.html", "All regions")] + [("regions/%s.html" % r["slug"], r["name"]) for r in R["REGIONS"]]),
        ("Community and company", [("support.html", "Support"), ("contests.html", "Contests"), ("careers.html", "Careers"), ("advertise.html", "Advertise"),
                                   ("about.html", "About"), ("contact.html", "Contact"), ("editorial-policy.html", "Editorial policy")]),
        ("Legal", [("privacy.html", "Privacy policy"), ("terms.html", "Terms of use"), ("disclaimer.html", "Disclaimer"), ("cookies.html", "Cookie policy"),
                   ("trademark.html", "Trademark & copyright notice")]),
    ]
    html = "".join('<h2>%s</h2><ul>%s</ul>' % (esc(g), "".join('<li><a href="%s">%s</a></li>' % (h, esc(t)) for h, t in items)) for g, items in groups)
    R["page"]("sitemap.html", "Sitemap", "Every page on Home.Watch.",
              '<section class="page-head"><div class="wrap"><h1>Sitemap</h1></div></section><section class="section"><div class="wrap narrow prose sitemap-cols">%s</div></section>' % html,
              priority="0.3", crumbs=[("Sitemap", "sitemap.html")])


def not_found(R):
    body = """<section class="page-head"><div class="wrap narrow"><h1>That page isn't here</h1>
<p class="lede">The link may be old or mistyped. Try search, or start from one of these.</p>
<ul class="link-list"><li><a href="index.html"><strong>Home</strong><span>Tools, guides and live alerts</span></a></li>
<li><a href="find-a-pro.html"><strong>Get matched</strong><span>Find a home watch pro</span></a></li>
<li><a href="guides/index.html"><strong>Guides</strong><span>Everything about protecting an empty home</span></a></li></ul></div></section>"""
    base = ("<script>(function(){var p=location.pathname,b=p.indexOf('/home-watch/')===0?'/home-watch/':'/';"
            "document.write('<base href=\"'+b+'\">');})();</script>")
    R["page"]("404.html", "Page not found", "The page you were looking for could not be found.", body, index=False, base_script=base)


def build_info(R, state_options, month_options):
    support(R)
    contests(R)
    careers(R)
    advertise(R)
    about(R)
    contact(R)
    faq(R)
    legal(R, "privacy.html", "Privacy policy", "How Home.Watch collects, uses and protects information, including Google AdSense advertising cookies.", PRIVACY, "Privacy policy")
    legal(R, "terms.html", "Terms of use", "Terms for using Home.Watch, its tools and its provider matching service.", TERMS, "Terms of use")
    legal(R, "disclaimer.html", "Disclaimer", "Home.Watch provides general information only; providers are independent and data comes from public sources.", DISCLAIMER, "Disclaimer")
    legal(R, "cookies.html", "Cookie policy", "How Home.Watch uses cookies and browser storage, including Google AdSense.", COOKIES, "Cookie policy")
    legal(R, "trademark.html", "Trademark and copyright notice", "Home.Watch is independent and not affiliated with any business using similar names. Trademarks belong to their owners.", TRADEMARK, "Trademark & copyright")
    legal(R, "editorial-policy.html", "Editorial policy", "How Home.Watch researches, writes, reviews and corrects its guides.", EDITORIAL, "Editorial policy")
    sitemap_page(R)
    not_found(R)
