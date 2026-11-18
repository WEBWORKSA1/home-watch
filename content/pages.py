# -*- coding: utf-8 -*-
"""Page bodies for Home.Watch. build_all(R) receives helpers from scripts/build.py."""
import datetime

from content import pages_info

US_STATES = [("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"), ("AR", "Arkansas"), ("CA", "California"), ("CO", "Colorado"),
             ("CT", "Connecticut"), ("DE", "Delaware"), ("DC", "District of Columbia"), ("FL", "Florida"), ("GA", "Georgia"),
             ("HI", "Hawaii"), ("ID", "Idaho"), ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"), ("KS", "Kansas"),
             ("KY", "Kentucky"), ("LA", "Louisiana"), ("ME", "Maine"), ("MD", "Maryland"), ("MA", "Massachusetts"),
             ("MI", "Michigan"), ("MN", "Minnesota"), ("MS", "Mississippi"), ("MO", "Missouri"), ("MT", "Montana"),
             ("NE", "Nebraska"), ("NV", "Nevada"), ("NH", "New Hampshire"), ("NJ", "New Jersey"), ("NM", "New Mexico"),
             ("NY", "New York"), ("NC", "North Carolina"), ("ND", "North Dakota"), ("OH", "Ohio"), ("OK", "Oklahoma"),
             ("OR", "Oregon"), ("PA", "Pennsylvania"), ("PR", "Puerto Rico"), ("RI", "Rhode Island"), ("SC", "South Carolina"),
             ("SD", "South Dakota"), ("TN", "Tennessee"), ("TX", "Texas"), ("UT", "Utah"), ("VT", "Vermont"), ("VA", "Virginia"),
             ("WA", "Washington"), ("WV", "West Virginia"), ("WI", "Wisconsin"), ("WY", "Wyoming")]
CA_PROV = [("AB", "Alberta"), ("BC", "British Columbia"), ("MB", "Manitoba"), ("NB", "New Brunswick"),
           ("NL", "Newfoundland and Labrador"), ("NS", "Nova Scotia"), ("ON", "Ontario"), ("PE", "Prince Edward Island"),
           ("QC", "Quebec"), ("SK", "Saskatchewan"), ("YT", "Yukon"), ("NT", "Northwest Territories"), ("NU", "Nunavut")]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

TOOLS = [
    ("cost-estimator", "Home Watch Cost Estimator", "See a realistic monthly and seasonal price range for your home in under a minute."),
    ("risk-score", "Vacant Home Risk Check", "Answer ten questions and get a risk score with the fixes that matter most."),
    ("departure-checklist", "Departure Checklist Generator", "Build a printable closing checklist for your home type, climate and systems."),
    ("weather-watch", "Away-Home Weather Watch", "Check the week ahead at your empty home: freeze, heat and storm flags with live alerts."),
    ("vacancy-clock", "Insurance Vacancy Clock", "Map your absence against your policy's vacancy clause and export the key dates."),
    ("visit-report", "Visit Report Builder", "Create a room-by-room inspection report you can print or save as PDF."),
]

SERVICES = ["Interior & exterior inspections", "Freeze checks during cold snaps", "Storm preparation (shutters, furniture)",
            "Post-storm inspection", "Key holding & vendor meetings", "Mail & package collection", "Pool / spa checks",
            "Vehicle starts", "Pre-arrival preparation", "Alarm & sensor response"]


def state_options(selected=""):
    us = "".join('<option value="%s"%s>%s</option>' % (c, " selected" if c == selected else "", n) for c, n in US_STATES)
    ca = "".join('<option value="%s">%s</option>' % (c, n) for c, n in CA_PROV)
    return '<option value="">Choose…</option><optgroup label="United States">%s</optgroup><optgroup label="Canada">%s</optgroup>' % (us, ca)


def month_options():
    return '<option value="">Not sure yet</option>' + "".join('<option>%s</option>' % m for m in MONTHS)


def season_focus(month):
    """What matters for empty homes this month (Northern Hemisphere)."""
    m = month
    items = []
    if m in (11, 12, 1, 2, 3):
        items.append(("Freeze season up north", "Homes left behind in cold regions need heat at 55°F or more, or full winterization.", "guides/preventing-frozen-pipes-in-an-empty-home.html"))
    if m in (6, 7, 8, 9, 10, 11):
        items.append(("Hurricane season on the coast", "June 1 to November 30. Agree your storm-prep plan before you leave.", "guides/hurricane-season-plan-for-absentee-owners.html"))
    if m in (5, 6, 7, 8, 9):
        items.append(("Humidity season down south", "Keep closed-up homes under 60% humidity to stop mold.", "guides/humidity-and-mold-in-a-closed-up-home.html"))
    if m in (6, 7, 8, 9):
        items.append(("Desert monsoon", "Dust storms and outages hit Arizona homes from mid-June to September.", "regions/arizona.html"))
    if m in (3, 4, 5):
        items.append(("Departure season", "Close your southern home properly before heading north.", "guides/snowbird-departure-checklist.html"))
    if m in (9, 10, 11):
        items.append(("Departure season", "Close your northern home properly before heading south.", "guides/snowbird-departure-checklist.html"))
    if m in (10, 11, 12):
        items.append(("Book next season early", "Popular home watch providers fill their calendars before peak season.", "find-a-pro.html"))
    return items[:3]


def estimate_panel():
    return """<aside class="estimate" aria-live="polite" data-estimate>
  <p class="estimate-label">Estimated cost</p>
  <p class="estimate-value" data-est-month>Choose size and frequency</p>
  <p class="estimate-sub" data-est-season></p>
  <p class="fine">An estimate only. Matched providers send real quotes.</p>
</aside>"""


# ---------------------------------------------------------------- home
def home(R):
    esc, data = R["esc"], R["data"]
    root = ""
    month = datetime.date.today().month
    focus = "".join('<li><a href="%s"><strong>%s</strong><span>%s</span></a></li>' % (h, esc(t), esc(d)) for t, d, h in season_focus(month))
    tools_rest = "".join('<li><a href="tools/%s.html"><strong>%s</strong><span>%s</span></a></li>' % (s, esc(t), esc(d)) for s, t, d in TOOLS[1:])
    guides = "".join('<li><a href="guides/%s.html"><span class="cat">%s</span><strong>%s</strong><span>%s</span></a></li>' % (
        g["slug"], esc(g["cat"]), esc(g["title"]), esc(g["desc"])) for g in R["GUIDES"][:6])
    regions = "".join('<li><a href="regions/%s.html">%s</a></li>' % (r["slug"], esc(r["name"])) for r in R["REGIONS"])
    vids = "".join(R["lite_video"](v, root) for v in data["videos"][:3])
    board = data["board"]
    north = [c for c in board.get("cities", []) if c.get("role") in ("north", "mountain")]
    north.sort(key=lambda c: c.get("min_f", 99))
    board_html = R["render_board"]({"cities": north[:8]})
    updated = board.get("updated", "")
    faq = [
        ("What does a home watch service do?", "A home watch professional visits your empty home on a schedule, inspects it inside and out, sends you a dated report with photos and calls you if something needs attention."),
        ("How much does home watch cost?", "Weekly visits for an average home commonly run about $100–$250 a month, depending on market and home size. Try the free cost estimator for your home."),
        ("Is Home.Watch free for homeowners?", "Yes. Matching, tools, guides and alerts are free for homeowners. Providers pay to be listed and to receive requests."),
        ("Are providers vetted?", "We ask every listed provider to confirm insurance, bonding and background checks and we encourage you to verify certificates before hiring. See our checklist of questions to ask."),
        ("Which areas do you cover?", "We accept requests across the United States and Canada, with in-depth guides for Florida, Arizona, Texas, California, the Carolinas, mountain towns, lake country and the Northeast coast."),
    ]
    faq_html = "".join('<details><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a)) for q, a in faq)
    schema = [{"@context": "https://schema.org", "@type": "WebSite", "name": "Home.Watch", "url": R["SITE"] + "/"},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                  {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <h1>Your home is empty. It shouldn't be unwatched.</h1>
      <p class="lede">Compare insured, background-checked home watch pros near your property — then use free tools to keep it dry, warm and secure between visits.</p>
      <form class="quick-match" action="find-a-pro.html" method="get">
        <div class="field"><label for="qm-zip">ZIP or postal code</label><input id="qm-zip" name="zip" inputmode="text" autocomplete="postal-code" placeholder="34102 or M5V 2T6" required></div>
        <div class="field"><label for="qm-month">Leaving in</label><select id="qm-month" name="month">{month_options()}</select></div>
        <button class="btn btn-window btn-lg" type="submit">Get matched free</button>
      </form>
      <p class="hero-note">Free for homeowners. No obligation. Your details go only to the providers you're matched with.</p>
    </div>
    <div class="report-card" role="img" aria-label="Example home watch visit report showing every check passed">
      <div class="report-head"><span class="report-title">Visit report</span><span class="status status-clear">All clear</span></div>
      <p class="report-addr">Gulf-view condo, unit 4B</p>
      <p class="report-time">Thursday, 9:42 AM <span>Visit 14 this season</span></p>
      <ul class="report-list">
        <li><span>Doors, windows and locks</span><b>Secure</b></li>
        <li><span>Indoor temperature</span><b>79°F</b></li>
        <li><span>Humidity</span><b>52%</b></li>
        <li><span>Water heater and supply lines</span><b>No leaks</b></li>
        <li><span>Faucets run, toilets flushed</span><b>Done</b></li>
        <li><span>Fridge and freezer</span><b>Running</b></li>
        <li><span>Mail and packages</span><b>Collected</b></li>
        <li><span>Exterior and lanai</span><b>No storm damage</b></li>
      </ul>
      <p class="report-foot">8 photos attached. Sent to the owner at 9:58 AM.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="section-title">How matching works</h2>
    <ol class="how">
      <li><strong>Tell us about the house</strong><span>Where it is, how big it is, when you'll be away and what you need checked. About two minutes.</span></li>
      <li><strong>We match you with local pros</strong><span>Up to three home watch providers who cover your area and confirm insurance, bonding and background checks.</span></li>
      <li><strong>Compare and choose</strong><span>Providers contact you with quotes. Use our questions checklist and pick the one you trust.</span></li>
    </ol>
    <p><a class="btn btn-night" href="find-a-pro.html">Start your request</a></p>
  </div>
</section>

<section class="section section-fog">
  <div class="wrap tools-split">
    <h2 class="section-title">Free tools for an empty house</h2>
    <div>
      <a class="tool-feature" href="tools/cost-estimator.html">
        <strong>{esc(TOOLS[0][1])}</strong>
        <span>{esc(TOOLS[0][2])}</span>
        <span class="tool-sample"><b>$120–$199</b> a month for weekly visits to a 2,000 sq ft home in a standard market</span>
      </a>
    </div>
    <ul class="link-list">{tools_rest}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div>
      <h2 class="section-title">Freeze watch for homes left behind</h2>
      <p>Coldest 7-day lows in northern and mountain markets, refreshed every morning. Updated {esc(R['fmt_date'](updated)) if updated else 'daily'}.</p>
      {board_html}
      <p><a href="alerts.html">See the full freeze and heat board and live alerts</a></p>
    </div>
    <div>
      <h2 class="section-title">What matters this month</h2>
      <ul class="link-list focus">{focus}</ul>
    </div>
  </div>
</section>

<section class="section section-fog">
  <div class="wrap">
    <h2 class="section-title">Guides</h2>
    <ul class="guide-list">{guides}</ul>
    <p><a href="guides/index.html">All {len(R['GUIDES'])} guides</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div>
      <h2 class="section-title">Recalls on home products</h2>
      <p>From the U.S. Consumer Product Safety Commission, filtered for items found in houses. Refreshed daily.</p>
      {R['render_recalls'](data['recalls'], root, 5)}
    </div>
    <div>
      <h2 class="section-title">Latest disaster declarations</h2>
      <p>Federal declarations from FEMA. If your empty home is in a declared area, ask for a check.</p>
      {R['render_fema'](data['fema'], root, 5)}
    </div>
  </div>
</section>

<section class="section section-fog">
  <div class="wrap">
    <h2 class="section-title">Regional guides</h2>
    <ul class="chip-list">{regions}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="section-title">Watch and learn</h2>
    <div class="video-grid">{vids}</div>
    <p><a href="videos.html">Open the video library</a></p>
  </div>
</section>

<section class="band band-night">
  <div class="wrap band-grid">
    <div>
      <h2>Run a home watch business?</h2>
      <p>Get matched homeowner requests in your service area, a featured listing and free reporting tools.</p>
    </div>
    <a class="btn btn-window btn-lg" href="for-pros.html">List your business</a>
  </div>
</section>

<section class="section">
  <div class="wrap community">
    <a href="support.html"><strong>Support Home.Watch</strong><span>Help fund free tools, outreach, new hires and contest prizes.</span></a>
    <a href="contests.html"><strong>Away-Ready Home Challenge</strong><span>Share your best closing-up tip and win monthly prizes.</span></a>
    <a href="careers.html"><strong>Work with us</strong><span>Writers, video creators, regional experts and partnership roles.</span></a>
  </div>
</section>

<section class="section section-fog" id="reminder">
  <div class="wrap two-col">
    <div>
      <h2 class="section-title">Get a reminder before you leave</h2>
      <p>Tell us when you usually close up the house. Two weeks before, we'll email a departure checklist matched to your season — plus our monthly briefing on storms, freezes and recalls.</p>
    </div>
    <form class="card-form" data-form="reminder" data-subject="Home.Watch departure reminder signup" novalidate>
      <div class="field"><label for="rm-email">Email</label><input id="rm-email" name="email" type="email" required autocomplete="email"></div>
      <div class="field-row">
        <div class="field"><label for="rm-month">I usually leave in</label><select id="rm-month" name="departure_month" required>{month_options()}</select></div>
        <div class="field"><label for="rm-where">Home location (optional)</label><input id="rm-where" name="home_location" placeholder="City, state"></div>
      </div>
      <label class="check"><input type="checkbox" name="consent" value="yes" required> I agree to receive emails from Home.Watch. Unsubscribe anytime.</label>
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn btn-window" type="submit">Set my reminder</button>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <h2 class="section-title">Questions homeowners ask</h2>
    <div class="faq">{faq_html}</div>
    <p><a href="faq.html">More answers</a></p>
  </div>
</section>
"""
    R["page"]("index.html", "Home.Watch — Home Watch Services, Tools and Live Alerts for Empty Homes",
              "Find insured home watch professionals for your seasonal or second home, estimate costs, build a departure checklist and track freeze, storm and recall alerts while you're away.",
              body, active="home", schema=schema, priority="1.0", body_class="page-home")


# ---------------------------------------------------------------- lead form
def find_a_pro(R):
    esc = R["esc"]
    services = "".join('<label class="check"><input type="checkbox" name="services" value="%s"> %s</label>' % (esc(s), esc(s)) for s in SERVICES)
    body = f"""
<section class="page-head">
  <div class="wrap">
    <h1>Get matched with home watch pros</h1>
    <p class="lede">Answer a few questions about your home. We'll connect you with up to three local providers who cover your area. Free, with no obligation.</p>
  </div>
</section>
<section class="section">
  <div class="wrap lead-grid">
    <form class="wizard" data-form="lead" data-subject="New homeowner lead — Home.Watch" data-wizard novalidate>
      <div class="progress" aria-hidden="true"><span data-progress></span></div>
      <p class="step-count" data-step-count>Step 1 of 5</p>

      <fieldset data-step="1">
        <legend>Where is the home?</legend>
        <div class="field-row">
          <div class="field"><label for="lf-zip">ZIP or postal code</label><input id="lf-zip" name="zip" required autocomplete="postal-code"></div>
          <div class="field"><label for="lf-city">City</label><input id="lf-city" name="city" autocomplete="address-level2"></div>
        </div>
        <div class="field-row">
          <div class="field"><label for="lf-state">State or province</label><select id="lf-state" name="state" required data-est="state">{state_options()}</select></div>
          <div class="field"><label for="lf-country">Country</label><select id="lf-country" name="country"><option>United States</option><option>Canada</option><option>Other</option></select></div>
        </div>
      </fieldset>

      <fieldset data-step="2" hidden>
        <legend>About the property</legend>
        <div class="choice-grid" role="radiogroup" aria-label="Property type">
          <label class="choice"><input type="radio" name="property_type" value="Single-family home" required data-est="type" data-mult="1"> <span>Single-family home</span></label>
          <label class="choice"><input type="radio" name="property_type" value="Condo or townhome" data-est="type" data-mult="0.85"> <span>Condo or townhome</span></label>
          <label class="choice"><input type="radio" name="property_type" value="Estate or luxury home" data-est="type" data-mult="1.3"> <span>Estate or luxury home</span></label>
          <label class="choice"><input type="radio" name="property_type" value="Cabin, cottage or lake house" data-est="type" data-mult="1.1"> <span>Cabin, cottage or lake house</span></label>
          <label class="choice"><input type="radio" name="property_type" value="Vacant or for sale" data-est="type" data-mult="0.95"> <span>Vacant or for sale</span></label>
        </div>
        <div class="field"><label for="lf-size">Approximate size</label>
          <select id="lf-size" name="size" required data-est="size">
            <option value="">Choose…</option><option value="1">Under 1,500 sq ft</option><option value="2">1,500–2,500 sq ft</option>
            <option value="3">2,500–3,500 sq ft</option><option value="4">3,500–5,000 sq ft</option><option value="5">Over 5,000 sq ft</option>
          </select></div>
        <p class="field-label">Features</p>
        <div class="check-grid">
          <label class="check"><input type="checkbox" name="features" value="Pool or spa"> Pool or spa</label>
          <label class="check"><input type="checkbox" name="features" value="Gated community"> Gated community</label>
          <label class="check"><input type="checkbox" name="features" value="Dock or boat"> Dock or boat</label>
          <label class="check"><input type="checkbox" name="features" value="Vehicle left behind"> Vehicle left behind</label>
          <label class="check"><input type="checkbox" name="features" value="Leak or temperature sensors"> Leak or temperature sensors</label>
          <label class="check"><input type="checkbox" name="features" value="Monitored alarm"> Monitored alarm</label>
        </div>
      </fieldset>

      <fieldset data-step="3" hidden>
        <legend>Your schedule</legend>
        <div class="field-row">
          <div class="field"><label for="lf-leave">Leaving on</label><input id="lf-leave" name="leaving" type="date"></div>
          <div class="field"><label for="lf-return">Returning on</label><input id="lf-return" name="returning" type="date"></div>
        </div>
        <div class="field"><label for="lf-month">Or the month you usually leave</label><select id="lf-month" name="month">{month_options()}</select></div>
        <div class="field"><label for="lf-freq">How often should someone visit?</label>
          <select id="lf-freq" name="frequency" required data-est="freq">
            <option value="">Choose…</option><option value="4.33">Weekly</option><option value="2.17">Every two weeks</option>
            <option value="1">Monthly</option><option value="8.66">Twice a week</option><option value="4.33">Not sure — recommend one</option>
          </select></div>
        <div class="field"><label for="lf-start">When do you need service?</label>
          <select id="lf-start" name="start"><option>As soon as possible</option><option>Within a month</option><option>Next season</option><option>Just researching</option></select></div>
      </fieldset>

      <fieldset data-step="4" hidden>
        <legend>What do you need?</legend>
        <div class="check-grid">{services}</div>
        <div class="field"><label for="lf-notes">Anything else providers should know?</label><textarea id="lf-notes" name="notes" rows="4" placeholder="Gate code process, pets, previous issues, insurance requirements…"></textarea></div>
      </fieldset>

      <fieldset data-step="5" hidden>
        <legend>Where should providers reach you?</legend>
        <div class="field-row">
          <div class="field"><label for="lf-name">Full name</label><input id="lf-name" name="name" required autocomplete="name"></div>
          <div class="field"><label for="lf-email">Email</label><input id="lf-email" name="email" type="email" required autocomplete="email"></div>
        </div>
        <div class="field-row">
          <div class="field"><label for="lf-phone">Phone</label><input id="lf-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="lf-best">Best way to reach you</label><select id="lf-best" name="contact_method"><option>Email</option><option>Phone call</option><option>Text message</option></select></div>
        </div>
        <label class="check"><input type="checkbox" name="consent" value="yes" required> I agree to be contacted by Home.Watch and up to three matched providers about this request. See the <a href="privacy.html">privacy policy</a>.</label>
        <input type="hidden" name="estimate" data-est-hidden>
      </fieldset>

      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="wizard-nav">
        <button class="btn btn-ghost" type="button" data-prev hidden>Back</button>
        <button class="btn btn-night" type="button" data-next>Continue</button>
        <button class="btn btn-window" type="submit" data-submit hidden>Send my request</button>
      </div>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
    <div class="lead-side">
      {estimate_panel()}
      <div class="trust">
        <h2>What happens next</h2>
        <ul>
          <li>Providers who cover your area review your request.</li>
          <li>Up to three contact you, usually within one business day.</li>
          <li>You compare quotes and choose — or choose none.</li>
        </ul>
        <p>Before hiring, ask for certificates of insurance and bonding. Use our <a href="guides/how-to-choose-a-home-watch-provider.html">21 questions</a>.</p>
      </div>
    </div>
  </div>
</section>
"""
    R["page"]("find-a-pro.html", "Get Matched With Home Watch Pros Near You",
              "Free request form for homeowners: describe your seasonal or second home and get matched with up to three local home watch providers.",
              body, active="match", scripts=("lead.js",), priority="0.9", crumbs=[("Get matched", "find-a-pro.html")])


def for_pros(R):
    esc = R["esc"]
    plans = [
        ("Free listing", "$0", ["Business profile in your regions", "Contact form routed to you", "Free Visit Report Builder"], "Start free"),
        ("Featured", "$49/mo", ["Top placement in your regions", "Homeowner requests in your service area", "Featured badge and logo", "Monthly performance summary"], "Choose Featured"),
        ("Exclusive area", "$149/mo", ["Only provider shown for chosen ZIP or postal codes", "All homeowner requests from that area", "Sponsor slot on your regional guide", "Priority support"], "Reserve my area"),
        ("Pay per lead", "from $25", ["No monthly fee", "Pay only for requests you accept", "Pause any time"], "Buy leads"),
    ]
    plan_html = "".join('<div class="plan"><h3>%s</h3><p class="price">%s</p><ul>%s</ul><a class="btn btn-night btn-sm" href="#apply" data-plan="%s">%s</a></div>' % (
        esc(n), esc(p), "".join("<li>%s</li>" % esc(i) for i in items), esc(n), esc(c)) for n, p, items, c in plans)
    body = f"""
<section class="page-head page-head-night">
  <div class="wrap">
    <h1>Grow your home watch business</h1>
    <p class="lede">Homeowners come to Home.Watch to plan their absence, estimate costs and find a provider. List your business to be the one they call.</p>
    <p><a class="btn btn-window btn-lg" href="#apply">Apply to be listed</a></p>
  </div>
</section>
<section class="section">
  <div class="wrap two-col">
    <div>
      <h2 class="section-title">Why list with us</h2>
      <ul class="ticks">
        <li><strong>Qualified requests.</strong> Every request includes location, home size, schedule and services — so you quote with confidence.</li>
        <li><strong>Seasonal timing.</strong> Departure reminders bring homeowners to the site weeks before they leave, when they're ready to book.</li>
        <li><strong>Trust signals.</strong> Show insurance, bonding, background checks and any accreditation on your profile.</li>
        <li><strong>Free tools.</strong> Use the Visit Report Builder and our guides with your own clients.</li>
      </ul>
    </div>
    <div>
      <h2 class="section-title">Who we look for</h2>
      <p>Registered home watch, property care and absentee-owner service businesses in the United States and Canada that carry general liability insurance and a fidelity bond, and background-check everyone who enters a client's home.</p>
      <p>New to the industry? Read <a href="guides/starting-a-home-watch-business.html">starting a home watch business</a>.</p>
    </div>
  </div>
</section>
<section class="section section-fog">
  <div class="wrap">
    <h2 class="section-title">Plans</h2>
    <div class="plans">{plan_html}</div>
    <p class="fine">Prices in USD. Launch pricing; founding providers keep their rate for 12 months.</p>
  </div>
</section>
<section class="section" id="apply">
  <div class="wrap narrow">
    <h2 class="section-title">Apply to be listed</h2>
    <form class="card-form" data-form="pro" data-subject="Home watch provider application — Home.Watch" novalidate>
      <div class="field-row">
        <div class="field"><label for="pf-company">Business name</label><input id="pf-company" name="company" required autocomplete="organization"></div>
        <div class="field"><label for="pf-name">Your name</label><input id="pf-name" name="name" required autocomplete="name"></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="pf-email">Email</label><input id="pf-email" name="email" type="email" required autocomplete="email"></div>
        <div class="field"><label for="pf-phone">Phone</label><input id="pf-phone" name="phone" type="tel" autocomplete="tel"></div>
      </div>
      <div class="field"><label for="pf-site">Website</label><input id="pf-site" name="website" type="url" placeholder="https://"></div>
      <div class="field-row">
        <div class="field"><label for="pf-state">Main state or province</label><select id="pf-state" name="state" required>{state_options()}</select></div>
        <div class="field"><label for="pf-area">Service area (cities, counties, ZIP or postal codes)</label><input id="pf-area" name="service_area" required></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="pf-years">Years in business</label><select id="pf-years" name="years"><option>Under 1</option><option>1–3</option><option>3–10</option><option>10+</option></select></div>
        <div class="field"><label for="pf-plan">Plan</label><select id="pf-plan" name="plan"><option>Free listing</option><option>Featured</option><option>Exclusive area</option><option>Pay per lead</option></select></div>
      </div>
      <p class="field-label">Confirm what applies</p>
      <div class="check-grid">
        <label class="check"><input type="checkbox" name="credentials" value="General liability insurance"> General liability insurance</label>
        <label class="check"><input type="checkbox" name="credentials" value="Fidelity bond"> Fidelity bond</label>
        <label class="check"><input type="checkbox" name="credentials" value="Background-checked staff"> Background-checked staff</label>
        <label class="check"><input type="checkbox" name="credentials" value="Industry accreditation or certification"> Industry accreditation or certification</label>
        <label class="check"><input type="checkbox" name="credentials" value="Photo visit reports"> Photo visit reports</label>
        <label class="check"><input type="checkbox" name="credentials" value="24/7 emergency response"> 24/7 emergency response</label>
      </div>
      <div class="field"><label for="pf-about">Tell homeowners about your service</label><textarea id="pf-about" name="about" rows="4"></textarea></div>
      <label class="check"><input type="checkbox" name="consent" value="yes" required> I confirm the information is accurate and agree to the <a href="terms.html">terms of use</a>.</label>
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn btn-window" type="submit">Send application</button>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
"""
    R["page"]("for-pros.html", "For Home Watch Professionals: Get Listed and Receive Homeowner Requests",
              "List your home watch business on Home.Watch to receive qualified homeowner requests, featured placement and free reporting tools.",
              body, active="pros", priority="0.8", crumbs=[("For pros", "for-pros.html")])


# ---------------------------------------------------------------- guides
def guides(R):
    esc, md = R["esc"], R["md"]
    G = R["GUIDES"]
    cats = []
    for g in G:
        if g["cat"] not in cats:
            cats.append(g["cat"])
    listing = "".join('<li data-cat="%s"><a href="%s.html"><span class="cat">%s</span><strong>%s</strong><span>%s</span></a></li>' % (
        esc(g["cat"]), g["slug"], esc(g["cat"]), esc(g["title"]), esc(g["desc"])) for g in G)
    filters = '<button type="button" class="chip is-on" data-filter="all">All</button>' + "".join(
        '<button type="button" class="chip" data-filter="%s">%s</button>' % (esc(c), esc(c)) for c in cats)
    body = f"""
<section class="page-head"><div class="wrap"><h1>Guides for homes that sit empty</h1>
<p class="lede">Plain-English guides on hiring home watch, closing and reopening a house, insurance vacancy clauses, storms, freezes, humidity and monitoring.</p></div></section>
<section class="section"><div class="wrap">
<div class="chip-list filters" role="group" aria-label="Filter guides">{filters}</div>
<ul class="guide-list" data-filter-list>{listing}</ul>
</div></section>"""
    R["page"]("guides/index.html", "Home Watch Guides", "Guides for absentee, seasonal and second-home owners: costs, hiring, checklists, insurance, freezes, storms and monitoring.",
              body, active="guides", priority="0.8", crumbs=[("Guides", "guides/index.html")])

    for idx, g in enumerate(G):
        root = "../"
        html_body, toc = md(g["body"], root)
        words = len(R["strip_tags"](html_body).split())
        minutes = max(3, round(words / 220))
        toc_html = "".join('<li><a href="#%s">%s</a></li>' % (h, esc(t)) for h, t in toc)
        related = [x for x in G if x["slug"] != g["slug"] and x["cat"] == g["cat"]] + [x for x in G if x["slug"] != g["slug"] and x["cat"] != g["cat"]]
        rel_html = "".join('<li><a href="%s.html">%s</a></li>' % (x["slug"], esc(x["title"])) for x in related[:4])
        faq_html = ""
        schema = [{"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
                   "dateModified": g["updated"], "datePublished": "2026-11-18", "author": {"@type": "Organization", "name": "Home.Watch editorial team"},
                   "publisher": {"@type": "Organization", "name": "Home.Watch"}, "mainEntityOfPage": R["SITE"] + "/guides/%s.html" % g["slug"]}]
        if g.get("faq"):
            faq_html = '<section class="guide-faq"><h2 id="faq">Frequently asked questions</h2>%s</section>' % "".join(
                '<details><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a)) for q, a in g["faq"])
            schema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]})
        url = R["SITE"] + "/guides/%s.html" % g["slug"]
        body = f"""
<div class="read-progress" aria-hidden="true"><span></span></div>
<article class="guide wrap">
  <header class="guide-head">
    <p class="cat">{esc(g['cat'])}</p>
    <h1>{esc(g['title'])}</h1>
    <p class="lede">{esc(g['desc'])}</p>
    <p class="byline">By the Home.Watch editorial team. Updated {esc(R['fmt_date'](g['updated']))}. {minutes} min read.</p>
  </header>
  <div class="guide-grid">
    <aside class="toc" aria-label="On this page"><p class="toc-title">On this page</p><ol>{toc_html}</ol></aside>
    <div class="prose">
      {html_body}
      {faq_html}
      <div class="cta-box">
        <p><strong>Want a professional to check on your home?</strong> Get matched with insured local providers — free, no obligation.</p>
        <a class="btn btn-window" href="../find-a-pro.html">Get matched</a>
      </div>
      <div class="share" aria-label="Share this guide">
        <span>Share</span>
        <a href="https://www.facebook.com/sharer/sharer.php?u={url}" target="_blank" rel="noopener">Facebook</a>
        <a href="https://x.com/intent/post?url={url}" target="_blank" rel="noopener">X</a>
        <a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" target="_blank" rel="noopener">LinkedIn</a>
        <button type="button" data-copy-link>Copy link</button>
        <button type="button" onclick="window.print()">Print</button>
      </div>
    </div>
  </div>
  <section class="related"><h2>Related guides</h2><ul class="link-list">{rel_html}</ul></section>
</article>"""
        R["page"]("guides/%s.html" % g["slug"], g["title"], g["desc"], body, active="guides", schema=schema,
                  og_type="article", priority="0.8", crumbs=[("Guides", "guides/index.html"), (g["short"], "guides/%s.html" % g["slug"])])


# ---------------------------------------------------------------- regions
def regions(R):
    esc = R["esc"]
    G = {g["slug"]: g for g in R["GUIDES"]}
    items = "".join('<li><a href="%s.html"><strong>%s</strong><span>%s</span></a></li>' % (r["slug"], esc(r["name"]), esc(r["desc"])) for r in R["REGIONS"])
    body = f"""
<section class="page-head"><div class="wrap"><h1>Home watch by region</h1>
<p class="lede">Every climate threatens an empty home differently. Pick your region for its seasonal risk calendar, visit-frequency advice and live weather alerts.</p></div></section>
<section class="section"><div class="wrap"><ul class="guide-list">{items}</ul></div></section>"""
    R["page"]("regions/index.html", "Home Watch by Region", "Regional home watch guides with seasonal risk calendars and live weather alerts for popular second-home markets.",
              body, active="regions", priority="0.7", crumbs=[("Regions", "regions/index.html")])
    for r in R["REGIONS"]:
        cal = "".join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (esc(a), esc(b)) for a, b in r["seasons"])
        adds = "".join("<li>%s</li>" % esc(a) for a in r["addons"])
        rel = "".join('<li><a href="../guides/%s.html">%s</a></li>' % (s, esc(G[s]["title"])) for s in r["guides"] if s in G)
        opts = "".join('<option value="%s">%s</option>' % (a, a) for a in r["areas"])
        body = f"""
<section class="page-head"><div class="wrap"><h1>{esc(r['title'])}</h1><p class="lede">{esc(r['desc'])}</p></div></section>
<section class="section"><div class="wrap two-col">
  <div class="prose">
    <p>{esc(r['intro'])}</p>
    <p><strong>Markets covered:</strong> {esc(r['cities'])}.</p>
    <h2>Seasonal risk calendar</h2>
    <div class="table-wrap"><table><thead><tr><th scope="col">When</th><th scope="col">What to watch</th></tr></thead><tbody>{cal}</tbody></table></div>
    <h2>How often should a home watcher visit?</h2>
    <p>{esc(r['frequency'])}</p>
    <h2>Add these to your checklist</h2>
    <ul>{adds}</ul>
    <h2>Read next</h2>
    <ul>{rel}</ul>
  </div>
  <aside class="side-stack">
    <div class="live-box" data-nws-state="{r['areas'][0]}">
      <div class="live-head"><h2>Live weather alerts</h2><select aria-label="State" data-nws-select>{opts}</select></div>
      <div data-nws-list><p class="empty">Loading National Weather Service alerts…</p></div>
      <p class="fine">Source: National Weather Service. Updates each time you load the page.</p>
    </div>
    <div class="cta-box">
      <p><strong>Need someone to check your {esc(r['name'])} home?</strong></p>
      <a class="btn btn-window" href="../find-a-pro.html?state={r['areas'][0]}">Get matched in {esc(r['name'])}</a>
    </div>
  </aside>
</div></section>"""
        R["page"]("regions/%s.html" % r["slug"], r["title"], r["desc"], body, active="regions", scripts=("live.js",),
                  priority="0.7", crumbs=[("Regions", "regions/index.html"), (r["name"], "regions/%s.html" % r["slug"])])


# ---------------------------------------------------------------- alerts & videos
def alerts(R):
    data = R["data"]
    opts = "".join('<option value="%s"%s>%s</option>' % (c, " selected" if c == "FL" else "", n) for c, n in US_STATES)
    upd = R["data"]["board"].get("updated", "")
    body = f"""
<section class="page-head"><div class="wrap"><h1>Live alerts for empty homes</h1>
<p class="lede">Weather warnings, freeze and heat outlooks, disaster declarations, product recalls and news in one place. Weather alerts load live; everything else refreshes automatically every day.</p></div></section>
<section class="section"><div class="wrap">
  <div class="live-box live-box-wide" data-nws-state="FL">
    <div class="live-head"><h2>National Weather Service alerts</h2><select aria-label="State" data-nws-select>{opts}</select></div>
    <div data-nws-list><p class="empty">Loading alerts…</p></div>
    <p class="fine">Source: National Weather Service (api.weather.gov). Always follow instructions from local officials.</p>
  </div>
</div></section>
<section class="section section-fog"><div class="wrap">
  <h2 class="section-title">Freeze and heat board</h2>
  <p>Seven-day lows and highs for second-home markets and the northern homes snowbirds leave behind. Freeze means a forecast low at or below 32°F (0°C); hard freeze means 20°F (−7°C) or below; heat means a high of 100°F (38°C) or more. Updated {R['esc'](R['fmt_date'](upd)) if upd else 'daily'}. Forecast data: MET Norway (CC BY 4.0).</p>
  {R['render_board'](data['board'])}
</div></section>
<section class="section"><div class="wrap two-col">
  <div><h2 class="section-title">Disaster declarations</h2><p>Recent federal declarations from FEMA.</p>{R['render_fema'](data['fema'], '', 12)}</div>
  <div><h2 class="section-title">Home product recalls</h2><p>Recent CPSC recalls for heaters, alarms, appliances and other household items.</p>{R['render_recalls'](data['recalls'], '', 12)}</div>
</div></section>
<section class="section section-fog"><div class="wrap narrow">
  <h2 class="section-title">In the news</h2><p>Headlines about home watch, vacant homes, storms and home safety, gathered daily from news sources.</p>
  {R['render_news'](data['news'], 15)}
</div></section>"""
    R["page"]("alerts.html", "Live Alerts: Weather Warnings, Freeze Board, Disasters and Recalls",
              "Live National Weather Service alerts by state, a daily freeze and heat board for second-home markets, FEMA disaster declarations and home product recalls.",
              body, active="alerts", scripts=("live.js",), priority="0.8", crumbs=[("Live alerts", "alerts.html")])


VIDEO_CATS = [("basics", "What home watch looks like"), ("winter", "Winterizing and closing up"), ("freeze", "Frozen pipes"),
              ("storms", "Hurricanes and storms"), ("smart", "Leak detection and smart shutoffs"), ("pros", "For home watch pros")]


def videos(R):
    vids = R["data"]["videos"]
    sections = []
    for key, label in VIDEO_CATS:
        vs = [v for v in vids if v.get("cat") == key]
        if not vs:
            continue
        sections.append('<section class="section" id="%s"><div class="wrap"><h2 class="section-title">%s</h2><div class="video-grid">%s</div></div></section>' % (
            key, label, "".join(R["lite_video"](v, "") for v in vs)))
    nav = "".join('<a class="chip" href="#%s">%s</a>' % (k, l) for k, l in VIDEO_CATS if any(v.get("cat") == k for v in vids))
    body = f"""
<section class="page-head"><div class="wrap"><h1>Video library</h1>
<p class="lede">Hand-picked videos from home watch professionals, plumbers and builders. Videos load only when you press play, and the list is checked daily so broken links drop out.</p>
<div class="chip-list">{nav}</div></div></section>
{''.join(sections)}
<section class="section"><div class="wrap narrow"><p class="fine">Videos are hosted by YouTube and belong to their creators. Home.Watch does not endorse the businesses or products shown. Suggest a video through our <a href="contact.html">contact form</a>.</p></div></section>"""
    R["page"]("videos.html", "Home Watch Video Library: Winterizing, Storm Prep, Leak Detection",
              "Curated videos on home watch visits, winterizing and closing a seasonal home, frozen pipes, hurricane preparation and smart water shutoffs.",
              body, active="videos", priority="0.6", crumbs=[("Videos", "videos.html")])


# ---------------------------------------------------------------- tools
def tools(R):
    from content import tools as T
    esc = R["esc"]
    items = "".join('<li><a href="%s.html"><strong>%s</strong><span>%s</span></a></li>' % (s, esc(t), esc(d)) for s, t, d in TOOLS)
    body = f"""
<section class="page-head"><div class="wrap"><h1>Free tools for empty homes</h1>
<p class="lede">Estimate costs, score your risk, build a checklist, watch the weather, track insurance deadlines and produce inspection reports. No signup needed.</p></div></section>
<section class="section"><div class="wrap"><ul class="guide-list">{items}</ul></div></section>"""
    R["page"]("tools/index.html", "Free Home Watch Tools", "Free calculators and planners for absentee homeowners and home watch professionals.",
              body, active="tools", priority="0.8", crumbs=[("Tools", "tools/index.html")])
    for slug, title, desc in TOOLS:
        content, about = T.TOOL_HTML[slug](R, state_options, month_options)
        body = f"""
<section class="page-head"><div class="wrap"><h1>{esc(title)}</h1><p class="lede">{esc(desc)}</p></div></section>
<section class="section"><div class="wrap">{content}</div></section>
<section class="section section-fog"><div class="wrap narrow prose">{about}</div></section>"""
        R["page"]("tools/%s.html" % slug, title, desc, body, active="tools", scripts=("tools.js",), priority="0.8",
                  crumbs=[("Tools", "tools/index.html"), (title, "tools/%s.html" % slug)])


def build_all(R):
    home(R)
    find_a_pro(R)
    for_pros(R)
    guides(R)
    regions(R)
    alerts(R)
    videos(R)
    tools(R)
    pages_info.build_info(R, state_options, month_options)
