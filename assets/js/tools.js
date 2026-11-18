/* Interactive tools: cost estimator, risk check, checklist, weather watch, vacancy clock, visit report. */
(function () {
  "use strict";
  var H = window.HW;
  if (!H) return;
  var $ = H.$, $$ = H.$$, esc = H.esc, root = H.root;
  function money(n) { return "$" + Math.round(n).toLocaleString("en-US"); }

  /* ---------- cost estimator ---------- */
  var ce = $('[data-tool="cost"]');
  if (ce) {
    var BASE = { 1: [25, 40], 2: [30, 50], 3: [38, 60], 4: [45, 75], 5: [60, 110] };
    var ADD = { storm: [150, 300, "event"], pool: [10, 15, "visit"], vehicle: [5, 10, "visit"], vendor: [70, 120, "season"], arrival: [75, 150, "season"], mail: [3, 5, "visit"] };
    var freqFactor = function (v) { return v <= 1 ? 1.25 : v < 3 ? 1 : v < 6 ? 0.92 : 0.85; };
    var calc = function () {
      var size = ce.size.value, type = +ce.type.value, freq = +ce.freq.value, market = +ce.market.value, months = +ce.months.value;
      $("#ce-months-out").textContent = months;
      var m = type * market * freqFactor(freq), vlo = BASE[size][0] * m, vhi = BASE[size][1] * m;
      var mlo = vlo * freq, mhi = vhi * freq, visits = freq * months, alo = 0, ahi = 0;
      $$('input[name="addon"]:checked', ce).forEach(function (c) {
        var a = ADD[c.value], mult = a[2] === "visit" ? visits : 1;
        alo += a[0] * mult; ahi += a[1] * mult;
      });
      $("[data-ce-month]").textContent = money(mlo) + "–" + money(mhi) + " / month";
      $("[data-ce-visit]").textContent = money(vlo) + "–" + money(vhi);
      $("[data-ce-visits]").textContent = (Math.round(freq * 10) / 10).toString();
      $("[data-ce-addons]").textContent = alo ? money(alo) + "–" + money(ahi) : "None";
      $("[data-ce-season]").textContent = money(mlo * months + alo) + "–" + money(mhi * months + ahi);
      var typeMap = { "1": "1", "0.85": "0.85", "1.3": "1.3", "1.1": "1.1" };
      $("[data-ce-cta]").href = root + "find-a-pro.html?size=" + size + "&freq=" + freq + "&type=" + typeMap[ce.type.value];
    };
    ce.addEventListener("input", calc); ce.addEventListener("change", calc); calc();
  }

  /* ---------- risk check ---------- */
  var rk = $('[data-tool="risk"]');
  if (rk) {
    var FIX = [
      "Shorten unattended stretches: schedule check-ins at least every 7–14 days.",
      "Prepare for your climate: heat at 55°F+ or winterize in cold areas; humidity under 60% in hot, humid areas; storm plan on the coast.",
      "Arrange professional home watch visits — weekly in high-risk climates.",
      "Shut off the main water supply (unless a sprinkler system or boiler needs it) or install an automatic shutoff valve.",
      "Add leak sensors at the water heater, sinks, toilets, washer, fridge and air handler.",
      "Add temperature and humidity alerts with a cellular or battery-backed connection.",
      "Add a monitored alarm, or at least door sensors and exterior cameras with phone alerts.",
      "Have a plumber inspect older supply lines and valves before you leave.",
      "Stop mail, keep lawn care or snow removal going and put lights on varied timers.",
      "Ask your agent how your policy treats a vacant or unoccupied home and what checks it requires."
    ];
    var MAX = [16, 14, 16, 12, 10, 8, 7, 6, 6, 5];
    rk.addEventListener("submit", function (e) {
      e.preventDefault();
      var total = 0, parts = [], missing = false;
      for (var i = 1; i <= 10; i++) {
        var c = rk.querySelector('input[name="q' + i + '"]:checked');
        if (!c) { missing = true; continue; }
        total += +c.value; if (+c.value > 0) parts.push({ i: i - 1, v: +c.value });
      }
      var scoreEl = $("[data-risk-score]"), band = $("[data-risk-band]"), fixes = $("[data-risk-fixes]"), gauge = $("[data-risk-bar]");
      if (missing) { scoreEl.textContent = "Answer all ten questions"; return; }
      var color = total < 30 ? "var(--clear)" : total < 60 ? "var(--window-deep)" : "#EE7562";
      scoreEl.textContent = total + " / 100";
      band.textContent = total < 30 ? "Low risk. Keep your routine and test sensors before each trip." : total < 60 ? "Moderate risk. A few changes would cut your exposure sharply." : "High risk. Fix the top items before you leave.";
      gauge.style.width = total + "%"; gauge.style.background = color;
      parts.sort(function (a, b) { return b.v - a.v; });
      fixes.innerHTML = parts.slice(0, 5).map(function (p) { return "<li>" + esc(FIX[p.i]) + " <span class=\"muted\">(−" + p.v + ")</span></li>"; }).join("");
      $("[data-risk-result]").scrollIntoView({ block: "nearest", behavior: "smooth" });
    });
  }

  /* ---------- departure checklist ---------- */
  var cl = $('[data-tool="checklist"]');
  if (cl) {
    var ITEMS = [
      ["Before you go", "Schedule home watch visits and share your itinerary and emergency contacts", {}],
      ["Before you go", "Ask your insurance agent how the policy treats an empty home", { length: ["mid", "long"] }],
      ["Before you go", "Hold or forward mail and pause deliveries", {}],
      ["Before you go", "Service the HVAC system and replace the filter", { length: ["mid", "long"] }],
      ["Before you go", "Test smoke and carbon monoxide detectors", {}],
      ["Before you go", "Photograph every room and the exterior for insurance records", {}],
      ["Water", "Shut off the main water supply", { not: ["sprinkler", "boiler"] }],
      ["Water", "Leave the main on for the fire sprinkler system; shut off fixture valves instead", { has: ["sprinkler"] }],
      ["Water", "Ask a plumber before shutting water to the boiler", { has: ["boiler"] }],
      ["Water", "Turn off the water heater or set it to vacation mode", {}],
      ["Water", "Turn off water to the ice maker and washing machine", {}],
      ["Water", "Have the plumbing fully winterized: drain lines, antifreeze in traps", { climate: ["freeze"], length: ["long"] }],
      ["Water", "Shut off and drain outdoor faucets; disconnect hoses", { climate: ["freeze", "mild"] }],
      ["Water", "Turn off the well pump and note septic service dates", { has: ["well"] }],
      ["Water", "Set the irrigation schedule for the season or shut it off", { has: ["irrigation"] }],
      ["Climate", "Set heat no lower than 55°F (13°C) and replace the thermostat battery", { climate: ["freeze", "mild"] }],
      ["Climate", "Open cabinet doors under sinks on exterior walls", { climate: ["freeze"] }],
      ["Climate", "Set AC to 78–82°F with humidity control under 60%", { climate: ["humid", "coast"] }],
      ["Climate", "Flush the AC condensate line", { climate: ["humid", "coast", "desert"] }],
      ["Climate", "Set AC to a protective temperature, often mid-80s°F, rather than off", { climate: ["desert"] }],
      ["Climate", "Leave interior and closet doors open for airflow", { climate: ["humid", "coast"] }],
      ["Power and appliances", "Unplug small appliances, electronics and chargers", {}],
      ["Power and appliances", "Empty, clean and prop open the fridge — or leave it running with a few items", { length: ["mid", "long"] }],
      ["Power and appliances", "Put lights on timers with varied schedules", {}],
      ["Power and appliances", "Test sensors and alarm and confirm alerts reach your phone", { has: ["sensors"] }],
      ["Power and appliances", "Run the generator test cycle and check fuel", { has: ["generator"] }],
      ["Security", "Lock every door and window, including garage and pet doors", {}],
      ["Security", "Remove hidden spare keys from outside", {}],
      ["Security", "Give your home watcher alarm codes and monitoring company contacts", {}],
      ["Security", "Introduce your home watcher to a trusted neighbor", { type: ["house", "cabin"] }],
      ["Security", "Tell building management or the HOA who will be checking the unit", { type: ["condo"] }],
      ["Outside", "Clean gutters and downspouts", { type: ["house", "cabin"] }],
      ["Outside", "Secure or store outdoor furniture, grills and decorations", {}],
      ["Outside", "Agree in writing who installs shutters if a storm threatens", { climate: ["coast", "humid"] }],
      ["Outside", "Arrange snow removal so the house looks occupied", { climate: ["freeze"] }],
      ["Outside", "Clear defensible space and dry vegetation near the house", { climate: ["desert"] }],
      ["Outside", "Arrange pool service and leave equipment instructions", { has: ["pool"] }],
      ["Outside", "Disconnect or maintain the car battery and leave keys for vehicle starts", { has: ["vehicle"] }],
      ["Cabin and cottage", "Remove all food and rodent-proof entry points", { type: ["cabin"] }],
      ["Cabin and cottage", "Check propane levels and shut off unused gas appliances", { type: ["cabin"] }],
      ["Departure day", "Empty trash and remove food that can spoil", {}],
      ["Departure day", "Confirm water main, water heater and thermostat settings one last time", {}],
      ["Departure day", "Leave a contact sheet on the kitchen counter for your home watcher", {}]
    ];
    var key = "hw-checklist";
    var match = function (c, o) {
      if (c.climate && c.climate.indexOf(o.climate) < 0) return false;
      if (c.type && c.type.indexOf(o.type) < 0) return false;
      if (c.length && c.length.indexOf(o.length) < 0) return false;
      if (c.has && !c.has.some(function (h) { return o.has.indexOf(h) > -1; })) return false;
      if (c.not && c.not.some(function (h) { return o.has.indexOf(h) > -1; })) return false;
      return true;
    };
    var saved = {}; try { saved = JSON.parse(H.store(key) || "{}"); } catch (e) { saved = {}; }
    var progress = function () {
      var all = $$("[data-cl-list] input"), done = all.filter(function (i) { return i.checked; }).length;
      $("[data-cl-progress]").textContent = all.length ? done + " of " + all.length + " done" : "";
    };
    var build = function () {
      var o = { type: cl.type.value, climate: cl.climate.value, length: cl.absence.value, has: $$('input[name="has"]:checked', cl).map(function (c) { return c.value; }) };
      var groups = {}, order = [];
      ITEMS.forEach(function (it, n) {
        if (!match(it[2], o)) return;
        if (!groups[it[0]]) { groups[it[0]] = []; order.push(it[0]); }
        groups[it[0]].push('<li><label class="check"><input type="checkbox" data-i="' + n + '"' + (saved[n] ? " checked" : "") + '> <span>' + esc(it[1]) + "</span></label></li>");
      });
      $("[data-cl-list]").innerHTML = order.map(function (g) { return '<div class="cl-group"><h3>' + esc(g) + "</h3><ul>" + groups[g].join("") + "</ul></div>"; }).join("");
      H.store("hw-checklist-opts", JSON.stringify(o));
      progress();
    };
    $("[data-cl-build]").addEventListener("click", build);
    $("[data-cl-list]").addEventListener("change", function (e) {
      var i = e.target.getAttribute("data-i"); if (i === null) return;
      saved[i] = e.target.checked; H.store(key, JSON.stringify(saved)); progress();
    });
    $("[data-cl-reset]").addEventListener("click", function () { saved = {}; H.store(key, "{}"); $$("[data-cl-list] input").forEach(function (i) { i.checked = false; }); progress(); });
    try {
      var prevOpts = JSON.parse(H.store("hw-checklist-opts") || "null");
      if (prevOpts) {
        cl.type.value = prevOpts.type; cl.climate.value = prevOpts.climate; cl.absence.value = prevOpts.length;
        $$('input[name="has"]', cl).forEach(function (c) { c.checked = prevOpts.has.indexOf(c.value) > -1; });
        build();
      }
    } catch (e) { /* ignore */ }
  }

  /* ---------- weather watch ---------- */
  var ww = $('[data-tool="weather"]');
  if (ww) {
    var sel = $("[data-ww-city]"), out = $("[data-ww-out]"), cities = [], snapshot = null;
    var STORM = /thunder|storm|hurricane|tropical|blizzard|snow|ice|freezing rain|sleet|high wind|gust/i;
    fetch(root + "data/cities.json").then(function (r) { return r.json(); }).then(function (list) {
      cities = list;
      var groups = { US: [], CA: [] };
      list.forEach(function (c, i) { (groups[c.country] || groups.US).push('<option value="' + i + '">' + esc(c.name + ", " + c.region) + "</option>"); });
      sel.insertAdjacentHTML("beforeend", '<optgroup label="United States">' + groups.US.join("") + '</optgroup><optgroup label="Canada">' + groups.CA.join("") + "</optgroup>");
    });
    fetch(root + "data/citywatch.json").then(function (r) { return r.json(); }).then(function (d) { snapshot = d; }).catch(function () {});
    var flagsFor = function (lo, hi, text) {
      var f = [];
      if (lo !== null && lo <= 20) f.push('<span class="flag flag-issue">Hard freeze</span>');
      else if (lo !== null && lo <= 32) f.push('<span class="flag flag-freeze">Freeze</span>');
      if (hi !== null && hi >= 100) f.push('<span class="flag flag-heat">Heat</span>');
      if (text && STORM.test(text)) f.push('<span class="flag flag-storm">Storm</span>');
      return f.join(" ") || '<span class="flag flag-clear">All clear</span>';
    };
    var loading = function (msg) { out.innerHTML = '<p class="empty">' + esc(msg) + "</p>"; };
    var nws = function (lat, lon, label) {
      loading("Loading the National Weather Service forecast…");
      var pt = lat.toFixed(4) + "," + lon.toFixed(4);
      Promise.all([
        fetch("https://api.weather.gov/points/" + pt, { headers: { Accept: "application/geo+json" } }).then(function (r) { if (!r.ok) throw new Error("points"); return r.json(); }),
        fetch("https://api.weather.gov/alerts/active?point=" + pt, { headers: { Accept: "application/geo+json" } }).then(function (r) { return r.ok ? r.json() : { features: [] }; }).catch(function () { return { features: [] }; })
      ]).then(function (res) {
        var p = res[0].properties, rl = p.relativeLocation && p.relativeLocation.properties;
        var place = label || (rl ? rl.city + ", " + rl.state : pt);
        return fetch(p.forecast, { headers: { Accept: "application/geo+json" } }).then(function (r) { if (!r.ok) throw new Error("forecast"); return r.json(); }).then(function (fc) {
          var periods = fc.properties.periods, days = [];
          for (var i = 0; i < periods.length; i++) {
            var pd = periods[i];
            if (pd.isDaytime) { var night = periods[i + 1] && !periods[i + 1].isDaytime ? periods[i + 1] : null; days.push({ name: pd.name, hi: pd.temperature, lo: night ? night.temperature : null, text: pd.shortForecast + (night ? " / " + night.shortForecast : "") }); if (night) i++; }
            else days.push({ name: pd.name, hi: null, lo: pd.temperature, text: pd.shortForecast });
          }
          var alerts = res[1].features || [];
          var ah = alerts.length ? '<ul class="alert-list">' + alerts.map(function (a) { var x = a.properties; return '<li class="sev-' + esc((x.severity || "unknown").toLowerCase()) + '"><strong>' + esc(x.event) + '</strong><span class="meta">' + esc(x.headline || "") + "</span></li>"; }).join("") + "</ul>"
            : '<p><span class="flag flag-clear">No active alerts</span> for this location right now.</p>';
          out.innerHTML = '<div class="wx-head"><h2>' + esc(place) + '</h2><p class="muted">National Weather Service forecast, live.</p></div>' + ah +
            '<div class="wx-days">' + days.slice(0, 8).map(function (d) {
              return '<div class="wx-day"><strong>' + esc(d.name) + '</strong><div class="t">' + (d.hi !== null ? d.hi + "°" : "") + (d.lo !== null ? '<span class="muted"> / ' + d.lo + "°F</span>" : "") + "</div><p>" + esc(d.text) + "</p>" + flagsFor(d.lo, d.hi, d.text) + "</div>";
            }).join("") + "</div>" +
            '<p><a class="btn btn-window btn-sm" href="' + root + 'find-a-pro.html">Get a home watcher near ' + esc(place.split(",")[0]) + "</a></p>";
        });
      }).catch(function () { snap(lat, lon, label); });
    };
    var snap = function (lat, lon, label) {
      if (!snapshot || !snapshot.cities) { loading("Live forecasts are available for US locations. Daily snapshots load for Canadian cities — try again in a moment."); return; }
      var best = null, bd = 1e9;
      snapshot.cities.forEach(function (c) { var d = Math.pow(c.lat - lat, 2) + Math.pow(c.lon - lon, 2); if (d < bd) { bd = d; best = c; } });
      if (!best || !best.days) { loading("No forecast available for this location yet."); return; }
      out.innerHTML = '<div class="wx-head"><h2>' + esc(label || best.name + ", " + best.region) + '</h2><p class="muted">Daily snapshot' + (label ? "" : " for the nearest tracked city") + ", updated " + esc(snapshot.updated || "") + ". Forecast data: MET Norway.</p></div>" +
        '<div class="wx-days">' + best.days.map(function (d) {
          return '<div class="wx-day"><strong>' + esc(new Date(d.date + "T12:00:00").toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" })) + '</strong><div class="t">' + d.max_c + '°C<span class="muted"> / ' + d.min_c + "°C</span></div><p>" + d.max_f + "° / " + d.min_f + "°F</p>" + flagsFor(d.min_f, d.max_f, d.symbol || "") + "</div>";
        }).join("") + "</div>";
    };
    sel.addEventListener("change", function () {
      var c = cities[+sel.value]; if (!c) return;
      if (c.country === "US") nws(c.lat, c.lon, c.name + ", " + c.region); else snap(c.lat, c.lon, c.name + ", " + c.region);
    });
    $("[data-ww-geo]").addEventListener("click", function () {
      if (!navigator.geolocation) { loading("Location isn't available in this browser. Choose a city instead."); return; }
      loading("Finding your location…");
      navigator.geolocation.getCurrentPosition(function (p) { nws(p.coords.latitude, p.coords.longitude); }, function () { loading("Location permission was declined. Choose a city instead."); }, { timeout: 10000 });
    });
  }

  /* ---------- insurance vacancy clock ---------- */
  var vc = $('[data-tool="vacancy"]');
  if (vc) {
    var DAY = 864e5;
    var iso = function (d) { return d.toISOString().slice(0, 10); };
    var nice = function (d) { return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" }); };
    var today = new Date(); today = new Date(Date.UTC(today.getFullYear(), today.getMonth(), today.getDate()));
    if (!vc.leave.value) vc.leave.value = iso(new Date(today.getTime() + 14 * DAY));
    if (!vc.ret.value) vc.ret.value = iso(new Date(today.getTime() + 165 * DAY));
    var plan = null;
    var run = function () {
      var l = new Date(vc.leave.value + "T00:00:00Z"), r = new Date(vc.ret.value + "T00:00:00Z");
      var notes = $("[data-vc-notes]"), tl = $("[data-vc-timeline]");
      if (isNaN(l) || isNaN(r) || r <= l) { $("[data-vc-days]").textContent = "Enter your dates"; notes.innerHTML = ""; tl.innerHTML = ""; plan = null; return; }
      var days = Math.round((r - l) / DAY), clause = +vc.clause.value, req = +vc.req.value, every = +vc.plan.value, list = [], html = "";
      $("[data-vc-days]").textContent = days + " days away";
      if (clause) {
        var limit = new Date(l.getTime() + clause * DAY);
        if (days > clause) {
          list.push("Your absence passes the " + clause + "-day limit on <strong>" + nice(limit) + "</strong> — " + (days - clause) + " days before you return. Ask your agent about a vacancy or unoccupancy endorsement.");
          html += '<span class="tl-over" style="left:' + (clause / days * 100) + '%;right:0"></span><span class="tl-limit" style="left:' + (clause / days * 100) + '%"></span>';
        } else list.push("Your absence stays within the " + clause + "-day limit you entered.");
      } else list.push("Check your policy for a vacancy or unoccupancy limit — many use 30 or 60 days.");
      var visits = [];
      if (every) for (var d = every; d < days; d += every) { visits.push(new Date(l.getTime() + d * DAY)); html += '<span class="tl-visit" style="left:' + (d / days * 100) + '%"></span>'; }
      if (req) {
        if (!every || every > req) list.push("Your policy wording you entered asks for inspections every " + req + " days, but your plan " + (every ? "visits every " + every + " days" : "has no visits") + ". Increase visit frequency.");
        else list.push("Planned visits every " + every + " days meet the " + req + "-day inspection requirement you entered.");
      }
      list.push(visits.length + " planned visit" + (visits.length === 1 ? "" : "s") + " while you're away. Keep every dated report.");
      notes.innerHTML = list.map(function (x) { return "<li>" + x + "</li>"; }).join("");
      tl.innerHTML = html;
      plan = { l: l, r: r, limit: clause && days > clause ? new Date(l.getTime() + clause * DAY) : null, visits: visits };
    };
    vc.addEventListener("input", run); vc.addEventListener("change", run); run();
    var ics = function () {
      if (!plan) return;
      var ev = [], stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15) + "Z";
      var add = function (d, title) {
        var s = iso(d).replace(/-/g, ""), e = iso(new Date(d.getTime() + DAY)).replace(/-/g, "");
        ev.push("BEGIN:VEVENT\r\nUID:" + s + "-" + ev.length + "@home.watch\r\nDTSTAMP:" + stamp + "\r\nDTSTART;VALUE=DATE:" + s + "\r\nDTEND;VALUE=DATE:" + e + "\r\nSUMMARY:" + title + "\r\nEND:VEVENT");
      };
      add(plan.l, "Leave home - confirm water, thermostat and alarm");
      if (plan.limit) add(plan.limit, "Policy vacancy limit reached - check coverage with agent");
      plan.visits.forEach(function (v, i) { add(v, "Home watch visit " + (i + 1) + " - review report"); });
      add(plan.r, "Return home - see re-opening checklist");
      var blob = new Blob(["BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Home.Watch//Vacancy Clock//EN\r\n" + ev.join("\r\n") + "\r\nEND:VCALENDAR\r\n"], { type: "text/calendar" });
      var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "home-watch-vacancy-dates.ics"; document.body.appendChild(a); a.click(); a.remove();
    };
    $("[data-vc-ics]").addEventListener("click", ics);
  }

  /* ---------- visit report builder ---------- */
  var rb = $('[data-tool="report"]');
  if (rb) {
    var KEY = "hw-report";
    var fields = function () { return $$("input, select, textarea", rb); };
    var status = function () {
      var vals = $$(".rb-list select", rb).map(function (s) { s.closest("li").className = s.value === "Attention" ? "st-attn" : s.value === "Issue" ? "st-issue" : ""; return s.value; });
      var el = $("[data-rb-status]");
      if (vals.indexOf("Issue") > -1) { el.textContent = "Issue found"; el.className = "status status-issue"; }
      else if (vals.indexOf("Attention") > -1) { el.textContent = "Needs attention"; el.className = "status status-attn"; }
      else { el.textContent = "All clear"; el.className = "status status-clear"; }
    };
    var save = function () { H.store(KEY, JSON.stringify(fields().map(function (f) { return f.value; }))); status(); };
    try { var prevR = JSON.parse(H.store(KEY) || "null"); if (prevR) fields().forEach(function (f, i) { if (prevR[i] !== undefined) f.value = prevR[i]; }); } catch (e) { /* ignore */ }
    if (!rb.when.value) { var n = new Date(); n.setMinutes(n.getMinutes() - n.getTimezoneOffset()); rb.when.value = n.toISOString().slice(0, 16); }
    rb.addEventListener("input", save); rb.addEventListener("change", save);
    $("[data-rb-clear]").addEventListener("click", function () {
      fields().forEach(function (f) { if (f.tagName === "SELECT") f.selectedIndex = 0; else f.value = ""; });
      var n = new Date(); n.setMinutes(n.getMinutes() - n.getTimezoneOffset()); rb.when.value = n.toISOString().slice(0, 16); save();
    });
    status();
  }
})();
