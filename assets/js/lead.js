/* Multi-step "Get matched" form with live estimate and URL prefill. */
(function () {
  "use strict";
  var H = window.HW, form = document.querySelector("[data-wizard]");
  if (!H || !form) return;
  var steps = H.$$("[data-step]", form), cur = 0;
  var prev = H.$("[data-prev]", form), next = H.$("[data-next]", form), submit = H.$("[data-submit]", form);
  var bar = H.$("[data-progress]", form), count = H.$("[data-step-count]", form);

  function show(i) {
    cur = Math.max(0, Math.min(steps.length - 1, i));
    steps.forEach(function (s, n) { s.hidden = n !== cur; });
    prev.hidden = cur === 0;
    next.hidden = cur === steps.length - 1;
    submit.hidden = cur !== steps.length - 1;
    bar.style.width = ((cur + 1) / steps.length * 100) + "%";
    count.textContent = "Step " + (cur + 1) + " of " + steps.length;
  }
  function stepValid() {
    var ok = true, first = null;
    H.$$("input, select, textarea", steps[cur]).forEach(function (el) {
      el.classList.remove("is-invalid");
      if (el.type === "radio") {
        if (el.required && !form.querySelector('input[name="' + el.name + '"]:checked')) { ok = false; first = first || el; }
        return;
      }
      if (!el.checkValidity()) { ok = false; el.classList.add("is-invalid"); first = first || el; }
    });
    var st = H.$(".form-status", form);
    st.className = "form-status" + (ok ? "" : " err");
    st.textContent = ok ? "" : "Please complete the highlighted fields to continue.";
    if (first) first.focus();
    return ok;
  }
  next.addEventListener("click", function () { if (stepValid()) { show(cur + 1); steps[cur].querySelector("legend").scrollIntoView({ block: "center", behavior: "smooth" }); } });
  prev.addEventListener("click", function () { show(cur - 1); });

  /* estimate */
  var BASE = { 1: [25, 40], 2: [30, 50], 3: [38, 60], 4: [45, 75], 5: [60, 110] };
  var HIGH = ["CA", "HI", "MA", "NY", "NJ", "CT", "BC"];
  function freqFactor(v) { return v <= 1 ? 1.25 : v < 3 ? 1 : v < 6 ? 0.92 : 0.85; }
  function money(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
  function estimate() {
    var size = form.querySelector('[data-est="size"]').value, freq = parseFloat(form.querySelector('[data-est="freq"]').value);
    var type = form.querySelector('[data-est="type"]:checked'), st = form.querySelector('[data-est="state"]').value;
    var out = H.$("[data-est-month]"), sub = H.$("[data-est-season]"), hid = H.$("[data-est-hidden]", form);
    if (!size || !freq) { out.textContent = "Choose size and frequency"; sub.textContent = ""; return; }
    var m = (type ? parseFloat(type.getAttribute("data-mult")) : 1) * (HIGH.indexOf(st) > -1 ? 1.15 : 1) * freqFactor(freq);
    var lo = BASE[size][0] * m * freq, hi = BASE[size][1] * m * freq;
    out.textContent = money(lo) + "–" + money(hi) + " a month";
    sub.textContent = "About " + money(lo * 5) + "–" + money(hi * 5) + " for a five-month season, before add-ons.";
    if (hid) hid.value = out.textContent;
  }
  form.addEventListener("change", estimate);

  /* prefill from query string (quick-match, estimator, region pages) */
  var q = new URLSearchParams(location.search);
  function setVal(name, v) { var el = form.querySelector('[name="' + name + '"]'); if (el && v) el.value = v; }
  setVal("zip", q.get("zip")); setVal("month", q.get("month")); setVal("state", q.get("state")); setVal("size", q.get("size"));
  if (q.get("freq")) { var f = form.querySelector('[name="frequency"]'); H.$$("option", f).some(function (o) { if (o.value === q.get("freq")) { f.value = o.value; return true; } return false; }); }
  if (q.get("type")) H.$$('[name="property_type"]', form).forEach(function (r) { if (r.getAttribute("data-mult") === q.get("type")) r.checked = true; });
  if (/^[A-Za-z]\d[A-Za-z]/.test(q.get("zip") || "")) setVal("country", "Canada");
  estimate();

  form.addEventListener("hw:sent", function () {
    show(0);
    var st = H.$(".form-status", form);
    form.querySelector("fieldset").insertAdjacentHTML("beforebegin", '<div class="note"><p><strong>Your request is in.</strong> While you wait, build your <a href="tools/departure-checklist.html">departure checklist</a> or read <a href="guides/how-to-choose-a-home-watch-provider.html">21 questions to ask a provider</a>.</p></div>');
    st.scrollIntoView({ block: "center" });
    estimate();
  });
  show(0);
})();
