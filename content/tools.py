# -*- coding: utf-8 -*-
"""Markup for the interactive tools. Behaviour lives in assets/js/tools.js."""


def cost(R, state_options, month_options):
    html = """
<div class="tool-grid">
  <form class="card-form" data-tool="cost" onsubmit="return false">
    <div class="field-row">
      <div class="field"><label for="ce-size">Home size</label>
        <select id="ce-size" name="size">
          <option value="1">Under 1,500 sq ft</option><option value="2" selected>1,500–2,500 sq ft</option>
          <option value="3">2,500–3,500 sq ft</option><option value="4">3,500–5,000 sq ft</option><option value="5">Over 5,000 sq ft</option>
        </select></div>
      <div class="field"><label for="ce-type">Property type</label>
        <select id="ce-type" name="type"><option value="1">Single-family home</option><option value="0.85">Condo or townhome</option>
          <option value="1.3">Estate or luxury home</option><option value="1.1">Cabin, cottage or lake house</option></select></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="ce-freq">Visit frequency</label>
        <select id="ce-freq" name="freq"><option value="1">Monthly</option><option value="2.17">Every two weeks</option>
          <option value="4.33" selected>Weekly</option><option value="8.66">Twice a week</option></select></div>
      <div class="field"><label for="ce-market">Market</label>
        <select id="ce-market" name="market"><option value="1">Standard suburban market</option>
          <option value="1.25">High-cost coastal or resort market</option><option value="1.15">Rural, island or remote</option></select></div>
    </div>
    <div class="field"><label for="ce-months">Months away: <output id="ce-months-out">5</output></label>
      <input id="ce-months" name="months" type="range" min="1" max="12" value="5"></div>
    <p class="field-label">Add-ons</p>
    <div class="check-grid">
      <label class="check"><input type="checkbox" name="addon" value="storm"> Storm preparation (one event)</label>
      <label class="check"><input type="checkbox" name="addon" value="pool"> Pool or spa checks</label>
      <label class="check"><input type="checkbox" name="addon" value="vehicle"> Vehicle starts</label>
      <label class="check"><input type="checkbox" name="addon" value="vendor"> Two vendor meetings</label>
      <label class="check"><input type="checkbox" name="addon" value="arrival"> Pre-arrival preparation</label>
      <label class="check"><input type="checkbox" name="addon" value="mail"> Mail and package handling</label>
    </div>
  </form>
  <div class="result-card" aria-live="polite">
    <p class="estimate-label">Your estimate</p>
    <p class="estimate-value" data-ce-month>—</p>
    <dl class="result-list">
      <div><dt>Per visit</dt><dd data-ce-visit>—</dd></div>
      <div><dt>Visits per month</dt><dd data-ce-visits>—</dd></div>
      <div><dt>Add-ons for the season</dt><dd data-ce-addons>—</dd></div>
      <div><dt>Whole season</dt><dd data-ce-season>—</dd></div>
    </dl>
    <a class="btn btn-window" href="../find-a-pro.html" data-ce-cta>Get exact quotes</a>
    <p class="fine">Illustrative ranges based on published provider pricing and common add-on fees. Real prices vary by provider and location.</p>
  </div>
</div>"""
    about = """
<h2>How the estimate works</h2>
<p>Most home watch providers charge a flat monthly fee set by how often they visit and how long each visit takes. The estimator starts with a typical per-visit range for your home size, adjusts it for property type and market, applies a small discount for frequent visits (and a minimum charge for monthly-only service), then adds the seasonal add-ons you choose.</p>
<h2>Using the number</h2>
<p>Treat the result as a budgeting range. Two providers with the same price can deliver very different value: compare visit length, checklist depth, report quality, insurance and response times. Our guide to <a href="../guides/home-watch-cost.html">home watch costs</a> explains each factor, and <a href="../guides/how-to-choose-a-home-watch-provider.html">21 questions to ask</a> helps you compare quotes.</p>"""
    return html, about


def risk(R, state_options, month_options):
    qs = [
        ("How long will the home be empty?", [("Under 2 weeks", 0), ("2–6 weeks", 6), ("1–3 months", 12), ("More than 3 months", 16)]),
        ("What weather will it face?", [("Mild", 0), ("Hot and humid", 10), ("Freezing temperatures", 12), ("Storm-prone coast or both extremes", 14)]),
        ("Who checks on the home?", [("A professional, weekly", 0), ("A professional, less often", 5), ("A neighbor or family member", 9), ("Nobody", 16)]),
        ("What happens to the main water supply?", [("Shut off and lines drained", 0), ("Shut off", 2), ("On, with an automatic shutoff valve", 4), ("Left on", 12)]),
        ("Water leak sensors?", [("Whole-home coverage plus shutoff", 0), ("Several sensors", 3), ("One or two", 6), ("None", 10)]),
        ("Temperature or humidity alerts?", [("Yes, with cellular or battery backup", 0), ("Yes, Wi-Fi only", 3), ("None", 8)]),
        ("Security system?", [("Professionally monitored alarm", 0), ("Self-monitored alarm or cameras", 3), ("None", 7)]),
        ("Age of the plumbing?", [("Under 15 years", 0), ("15–40 years", 3), ("Over 40 years or unknown", 6)]),
        ("Lived-in signals (mail, lawn, snow, lights)?", [("All arranged", 0), ("Some arranged", 3), ("Nothing arranged", 6)]),
        ("Have you checked your policy's vacancy clause?", [("Yes, and I meet its conditions", 0), ("Not sure", 4), ("No", 5)]),
    ]
    blocks = []
    for i, (q, opts) in enumerate(qs, start=1):
        o = "".join('<label class="choice"><input type="radio" name="q%d" value="%d"%s> <span>%s</span></label>' % (
            i, pts, " required" if j == 0 else "", R["esc"](label)) for j, (label, pts) in enumerate(opts))
        blocks.append('<fieldset class="q"><legend>%d. %s</legend><div class="choice-grid">%s</div></fieldset>' % (i, R["esc"](q), o))
    html = """
<div class="tool-grid">
  <form class="card-form" data-tool="risk" novalidate>%s
    <button class="btn btn-night" type="submit">Show my risk score</button>
  </form>
  <div class="result-card" aria-live="polite" data-risk-result>
    <p class="estimate-label">Your risk score</p>
    <div class="gauge"><span data-risk-bar></span></div>
    <p class="estimate-value" data-risk-score>Answer the questions</p>
    <p data-risk-band></p>
    <ol class="fix-list" data-risk-fixes></ol>
    <a class="btn btn-window" href="../find-a-pro.html">Get matched with a pro</a>
  </div>
</div>""" % "".join(blocks)
    about = """
<h2>What the score means</h2>
<p>The score adds up the factors behind the most common and costly losses in empty homes: undetected water leaks, freezes, humidity, break-ins and gaps in insurance conditions. Under 30 is low risk, 30–59 is moderate and 60 or more is high. The fixes are ordered by how many points each one would remove.</p>
<p>It is a planning aid, not an inspection. A home watch professional or contractor can assess your property in person. Learn more in <a href="../guides/what-is-home-watch.html">what home watch is</a> and <a href="../guides/smart-home-monitoring-for-second-homes.html">smart monitoring for second homes</a>.</p>"""
    return html, about


def checklist(R, state_options, month_options):
    html = """
<div class="tool-grid">
  <form class="card-form" data-tool="checklist" onsubmit="return false">
    <div class="field-row">
      <div class="field"><label for="cl-type">Home type</label><select id="cl-type" name="type"><option value="house">House</option><option value="condo">Condo or apartment</option><option value="cabin">Cabin or cottage</option></select></div>
      <div class="field"><label for="cl-climate">Climate while you're away</label><select id="cl-climate" name="climate"><option value="humid">Hot and humid</option><option value="freeze">Freezing</option><option value="desert">Hot and dry</option><option value="coast">Storm-prone coast</option><option value="mild">Mild</option></select></div>
    </div>
    <div class="field"><label for="cl-length">Length of absence</label><select id="cl-length" name="absence"><option value="short">Under a month</option><option value="mid" selected>One to three months</option><option value="long">A full season or longer</option></select></div>
    <p class="field-label">The home has</p>
    <div class="check-grid">
      <label class="check"><input type="checkbox" name="has" value="pool"> Pool or spa</label>
      <label class="check"><input type="checkbox" name="has" value="sprinkler"> Fire sprinkler system</label>
      <label class="check"><input type="checkbox" name="has" value="boiler"> Boiler or hot-water heat</label>
      <label class="check"><input type="checkbox" name="has" value="well"> Well or septic</label>
      <label class="check"><input type="checkbox" name="has" value="vehicle"> Vehicle left behind</label>
      <label class="check"><input type="checkbox" name="has" value="sensors"> Smart sensors or alarm</label>
      <label class="check"><input type="checkbox" name="has" value="irrigation"> Irrigation system</label>
      <label class="check"><input type="checkbox" name="has" value="generator"> Generator</label>
    </div>
    <button class="btn btn-night" type="button" data-cl-build>Build my checklist</button>
  </form>
  <div class="result-card checklist-out" aria-live="polite">
    <div class="out-head"><p class="estimate-label">Your checklist</p><p class="muted" data-cl-progress></p></div>
    <div data-cl-list><p class="empty">Choose your options and press Build my checklist.</p></div>
    <div class="out-actions"><button class="btn btn-ghost btn-sm" type="button" onclick="window.print()">Print or save PDF</button><button class="btn btn-ghost btn-sm" type="button" data-cl-reset>Clear ticks</button></div>
  </div>
</div>"""
    about = """
<h2>How to use it</h2>
<p>Build the list a week or two before you leave and tick items off as you go. Your ticks are saved in this browser, so you can come back to it. Print it or save it as a PDF for your home watch provider.</p>
<p>The full reasoning behind each item is in the <a href="../guides/snowbird-departure-checklist.html">snowbird departure checklist</a>, and the <a href="../guides/returning-home-reopening-checklist.html">re-opening checklist</a> covers your return.</p>"""
    return html, about


def weather(R, state_options, month_options):
    html = """
<div class="weather-tool" data-tool="weather">
  <div class="weather-controls card-form">
    <div class="field"><label for="ww-city">Your empty home is near</label><select id="ww-city" data-ww-city><option value="">Choose a city…</option></select></div>
    <button class="btn btn-ghost" type="button" data-ww-geo>Use my current location</button>
    <p class="fine">US forecasts and alerts come live from the National Weather Service. Canadian cities use the daily MET Norway snapshot.</p>
  </div>
  <div class="weather-out" aria-live="polite" data-ww-out><p class="empty">Pick a city to see the week ahead at your home.</p></div>
</div>"""
    about = """
<h2>What the flags mean</h2>
<ul>
<li><strong>Freeze</strong> — a forecast low at or below 32°F (0°C). Confirm the heat is on and holding, or that plumbing is winterized.</li>
<li><strong>Hard freeze</strong> — 20°F (−7°C) or below. Ask your home watcher for an extra visit and check temperature alerts.</li>
<li><strong>Heat</strong> — a high of 100°F (38°C) or more. Air conditioners work hardest; a failure can damage contents quickly.</li>
<li><strong>Storm</strong> — thunderstorms, high wind, tropical systems or heavy snow in the forecast text.</li>
</ul>
<p>Always follow official warnings. See <a href="../guides/preventing-frozen-pipes-in-an-empty-home.html">preventing frozen pipes</a> and the <a href="../guides/hurricane-season-plan-for-absentee-owners.html">hurricane plan</a>.</p>"""
    return html, about


def vacancy(R, state_options, month_options):
    html = """
<div class="tool-grid">
  <form class="card-form" data-tool="vacancy" onsubmit="return false">
    <div class="field-row">
      <div class="field"><label for="vc-leave">Leaving on</label><input id="vc-leave" type="date" name="leave"></div>
      <div class="field"><label for="vc-return">Returning on</label><input id="vc-return" type="date" name="ret"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="vc-clause">Policy vacancy or unoccupancy limit</label><select id="vc-clause" name="clause"><option value="30">30 days</option><option value="60" selected>60 days</option><option value="90">90 days</option><option value="0">No limit / not sure</option></select></div>
      <div class="field"><label for="vc-req">Inspections required by policy</label><select id="vc-req" name="req"><option value="0">None stated</option><option value="7">Every 7 days</option><option value="14">Every 14 days</option><option value="30">Every 30 days</option></select></div>
    </div>
    <div class="field"><label for="vc-plan">Planned home watch visits</label><select id="vc-plan" name="plan"><option value="0">None</option><option value="30">Monthly</option><option value="14">Every two weeks</option><option value="7" selected>Weekly</option></select></div>
  </form>
  <div class="result-card" aria-live="polite">
    <p class="estimate-label">Your absence</p>
    <p class="estimate-value" data-vc-days>Enter your dates</p>
    <div class="timeline" data-vc-timeline aria-hidden="true"></div>
    <ul class="result-notes" data-vc-notes></ul>
    <button class="btn btn-ghost btn-sm" type="button" data-vc-ics>Download calendar reminders (.ics)</button>
  </div>
</div>"""
    about = """
<h2>Not insurance advice</h2>
<p>Policies define vacancy and unoccupancy differently, and home watch visits do not necessarily make a home "occupied". This tool simply lays your dates against the number of days you enter so you can have an informed conversation with your agent. Read <a href="../guides/vacant-home-insurance-vacancy-clauses.html">vacancy clauses explained</a> for the questions to ask.</p>
<p>The calendar file adds your departure, the day your stated limit is reached, each planned visit and your return to Google Calendar, Apple Calendar or Outlook.</p>"""
    return html, about


def report(R, state_options, month_options):
    sections = [
        ("Exterior", ["Roof, gutters and downspouts", "Doors, windows and screens", "Landscaping and irrigation", "Pool, spa and equipment", "Storm or wind damage", "Signs of trespass"]),
        ("Entry and security", ["All doors locked", "Alarm armed and working", "Garage door closed", "Packages, flyers and mail"]),
        ("Climate", ["Thermostat holding set point", "HVAC running normally", "Air filter condition"]),
        ("Plumbing", ["Water heater area dry", "Under sinks dry", "Toilets flushed and not running", "Faucets run, drains clear", "Laundry and ice maker lines dry"]),
        ("Kitchen and appliances", ["Refrigerator and freezer running", "Dishwasher area dry", "No odors or spoiled food"]),
        ("Electrical", ["Breaker panel, nothing tripped", "Lights and timers working", "Smoke and CO detectors quiet"]),
        ("Interior", ["Ceilings and walls, no stains", "Floors dry, no warping", "No musty smell or visible mold", "No pest activity"]),
    ]
    rows = []
    for name, items in sections:
        lis = "".join(
            '<li><span>%s</span><select aria-label="%s status"><option>OK</option><option>Attention</option><option>Issue</option><option>N/A</option></select>'
            '<input type="text" aria-label="%s note" placeholder="Note"></li>' % (R["esc"](i), R["esc"](i), R["esc"](i)) for i in items)
        rows.append('<fieldset class="rb-section"><legend>%s</legend><ul class="rb-list">%s</ul></fieldset>' % (R["esc"](name), lis))
    html = """
<form class="card-form report-builder" data-tool="report" onsubmit="return false">
  <div class="rb-meta">
    <div class="field"><label for="rb-prop">Property</label><input id="rb-prop" name="property" placeholder="Name or address"></div>
    <div class="field"><label for="rb-by">Inspected by</label><input id="rb-by" name="inspector"></div>
    <div class="field"><label for="rb-when">Date and time</label><input id="rb-when" name="when" type="datetime-local"></div>
    <div class="field"><label for="rb-temp">Indoor temperature</label><input id="rb-temp" name="temp" placeholder="78°F"></div>
    <div class="field"><label for="rb-hum">Humidity</label><input id="rb-hum" name="humidity" placeholder="52%%"></div>
  </div>
  %s
  <div class="field"><label for="rb-summary">Summary for the owner</label><textarea id="rb-summary" name="summary" rows="3"></textarea></div>
  <div class="rb-status" aria-live="polite"><span>Overall status</span><b class="status status-clear" data-rb-status>All clear</b></div>
  <div class="out-actions"><button class="btn btn-window" type="button" onclick="window.print()">Print or save PDF</button><button class="btn btn-ghost" type="button" data-rb-clear>Start a new report</button></div>
</form>""" % "".join(rows)
    about = """
<h2>For owners and professionals</h2>
<p>Owners can use the builder to see what a complete visit covers and to compare providers. Home watch professionals can use it as a free, printable report template. Your entries stay in this browser and are not sent anywhere.</p>
<p>Want visits like this on a schedule? <a href="../find-a-pro.html">Get matched with a home watch pro</a>. Run a home watch business? <a href="../for-pros.html">List it on Home.Watch</a>.</p>"""
    return html, about


TOOL_HTML = {
    "cost-estimator": cost,
    "risk-score": risk,
    "departure-checklist": checklist,
    "weather-watch": weather,
    "vacancy-clock": vacancy,
    "visit-report": report,
}
