/* Live National Weather Service alerts by state (api.weather.gov, CORS-enabled, public domain). */
(function () {
  "use strict";
  var H = window.HW;
  if (!H) return;
  var esc = H.esc, ORDER = { Extreme: 0, Severe: 1, Moderate: 2, Minor: 3, Unknown: 4 };
  function when(s) {
    if (!s) return "";
    var d = new Date(s);
    return d.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
  }
  function load(box, area) {
    var list = box.querySelector("[data-nws-list]");
    list.innerHTML = '<p class="empty">Loading National Weather Service alerts…</p>';
    fetch("https://api.weather.gov/alerts/active?area=" + encodeURIComponent(area), { headers: { Accept: "application/geo+json" } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        var f = (d.features || []).map(function (x) { return x.properties; });
        f.sort(function (a, b) { return (ORDER[a.severity] || 4) - (ORDER[b.severity] || 4); });
        if (!f.length) { list.innerHTML = '<p><span class="flag flag-clear">No active alerts</span> for ' + esc(area) + " right now.</p>"; return; }
        list.innerHTML = '<p class="muted">' + f.length + " active alert" + (f.length === 1 ? "" : "s") + ".</p>" +
          '<ul class="alert-list">' + f.slice(0, 40).map(function (p) {
            var areaTxt = (p.areaDesc || "").split(";").slice(0, 6).join(";") + ((p.areaDesc || "").split(";").length > 6 ? "; …" : "");
            return '<li class="sev-' + esc((p.severity || "unknown").toLowerCase()) + '"><strong>' + esc(p.event) + "</strong>" +
              '<span class="meta">' + esc(areaTxt) + "</span>" +
              '<span class="meta">' + (p.effective ? "From " + esc(when(p.effective)) : "") + (p.expires ? " until " + esc(when(p.expires)) : "") + "</span>" +
              (p.description ? "<details><summary>Details</summary><p>" + esc(p.description) + (p.instruction ? "\n\n" + esc(p.instruction) : "") + "</p></details>" : "") +
              "</li>";
          }).join("") + "</ul>";
      })
      .catch(function () {
        list.innerHTML = '<p class="empty">Alerts couldn\'t load right now. Check <a href="https://www.weather.gov/" target="_blank" rel="noopener">weather.gov</a> directly.</p>';
      });
  }
  H.$$("[data-nws-state]").forEach(function (box) {
    var sel = box.querySelector("[data-nws-select]");
    var area = box.getAttribute("data-nws-state");
    if (sel) {
      try { var saved = H.store("hw-alert-state"); if (saved && sel.querySelector('option[value="' + saved + '"]')) { sel.value = saved; area = saved; } } catch (e) { /* ignore */ }
      sel.addEventListener("change", function () { H.store("hw-alert-state", sel.value); load(box, sel.value); });
    }
    load(box, area);
  });
})();
