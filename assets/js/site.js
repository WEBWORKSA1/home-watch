/* Home.Watch core behaviour: theme, menu, search, consent, forms, video, reading aids. */
(function () {
  "use strict";
  var doc = document, root = doc.body.getAttribute("data-root") || "";
  var cfg = window.HW_CONFIG || {};
  function $(s, c) { return (c || doc).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  window.HW = { $: $, $$: $$, store: store, root: root };

  /* theme */
  $$("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var cur = doc.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      doc.documentElement.setAttribute("data-theme", cur); store("hw-theme", cur);
    });
  });

  /* mobile menu */
  var nav = $("#main-nav"), menuBtn = $("[data-menu-toggle]");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    doc.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.focus(); } });
  }

  /* search */
  var dlg = $("#search-dialog"), input = $("#search-input"), results = $("#search-results"), index = null;
  function openSearch() {
    dlg.hidden = false; input.focus();
    if (!index) fetch(root + "search-index.json").then(function (r) { return r.json(); }).then(function (d) { index = d; runSearch(); }).catch(function () { index = []; });
  }
  function closeSearch() { dlg.hidden = true; }
  function runSearch() {
    if (!index) return;
    var q = input.value.trim().toLowerCase();
    if (!q) { results.innerHTML = ""; return; }
    var words = q.split(/\s+/);
    var hits = index.map(function (e) {
      var hay = (e.t + " " + e.d + " " + e.k).toLowerCase(), score = 0;
      words.forEach(function (w) { if (e.t.toLowerCase().indexOf(w) > -1) score += 5; if (hay.indexOf(w) > -1) score += 1; else score -= 10; });
      return { e: e, s: score };
    }).filter(function (h) { return h.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 12);
    results.innerHTML = hits.length ? hits.map(function (h) {
      return '<li><a href="' + root + h.e.u + '">' + esc(h.e.t) + '<span>' + esc(h.e.d) + '</span></a></li>';
    }).join("") : '<li><a href="' + root + 'guides/index.html">No matches. Browse all guides<span>Try fewer or different words.</span></a></li>';
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  window.HW.esc = esc;
  if (dlg) {
    $$("[data-open-search]").forEach(function (b) { b.addEventListener("click", openSearch); });
    $$("[data-close-search]").forEach(function (b) { b.addEventListener("click", closeSearch); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) closeSearch(); });
    input.addEventListener("input", runSearch);
    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !dlg.hidden) closeSearch();
      if (e.key === "/" && dlg.hidden && !/input|textarea|select/i.test(doc.activeElement.tagName)) { e.preventDefault(); openSearch(); }
    });
  }

  /* cookie consent */
  var banner = $("#cookie-banner");
  if (banner && !store("hw-consent")) banner.hidden = false;
  $$("[data-cookie]").forEach(function (b) {
    b.addEventListener("click", function () { store("hw-consent", b.getAttribute("data-cookie")); banner.hidden = true; });
  });
  $$("[data-reset-consent]").forEach(function (b) {
    b.addEventListener("click", function () { try { localStorage.removeItem("hw-consent"); } catch (e) {} if (banner) banner.hidden = false; });
  });

  /* slide-in reminder offer: once per visitor, never on the lead form */
  var slide = $("#slidein"), shown = false;
  function showSlide() {
    if (shown || !slide || store("hw-slidein") || /find-a-pro|#reminder/.test(location.href) || !cfg.slideinDelay) return;
    shown = true; slide.hidden = false;
  }
  if (slide && cfg.slideinDelay) {
    setTimeout(showSlide, cfg.slideinDelay * 1000);
    window.addEventListener("scroll", function () {
      var h = doc.documentElement; if ((h.scrollTop + innerHeight) / h.scrollHeight > 0.6) showSlide();
    }, { passive: true });
    $$("[data-close-slidein]").forEach(function (b) { b.addEventListener("click", function () { slide.hidden = true; store("hw-slidein", "1"); }); });
    $$("#slidein a").forEach(function (a) { a.addEventListener("click", function () { store("hw-slidein", "1"); }); });
  }

  /* back to top + reading progress */
  var top = $(".to-top"), bar = $(".read-progress span");
  window.addEventListener("scroll", function () {
    var h = doc.documentElement, y = h.scrollTop;
    if (top) top.classList.toggle("show", y > 900 && (!slide || slide.hidden));
    if (bar) bar.style.width = Math.min(100, (y / (h.scrollHeight - innerHeight)) * 100) + "%";
  }, { passive: true });

  /* table of contents highlight */
  var tocLinks = $$(".toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) tocLinks.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("href") === "#" + en.target.id); });
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    tocLinks.forEach(function (a) { var t = doc.getElementById(a.getAttribute("href").slice(1)); if (t) io.observe(t); });
  }

  /* guide filters */
  $$("[data-filter]").forEach(function (chip) {
    chip.addEventListener("click", function () {
      var f = chip.getAttribute("data-filter");
      $$("[data-filter]").forEach(function (c) { c.classList.toggle("is-on", c === chip); });
      $$("[data-filter-list] li").forEach(function (li) { li.hidden = f !== "all" && li.getAttribute("data-cat") !== f; });
    });
  });

  /* copy link */
  $$("[data-copy-link]").forEach(function (b) {
    b.addEventListener("click", function () {
      var done = function () { b.textContent = "Link copied"; setTimeout(function () { b.textContent = "Copy link"; }, 2000); };
      if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(done); else done();
    });
  });

  /* lightweight YouTube embeds */
  doc.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest(".lite-yt");
    if (!btn) return;
    var id = btn.getAttribute("data-yt");
    var f = doc.createElement("iframe");
    f.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(id) + "?autoplay=1&rel=0";
    f.title = btn.getAttribute("aria-label") || "Video";
    f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    f.allowFullscreen = true; f.loading = "lazy";
    btn.replaceWith(f);
  });

  /* word counter */
  $$("[data-maxwords]").forEach(function (t) {
    var out = t.parentNode.querySelector("[data-wordcount]"), max = +t.getAttribute("data-maxwords");
    t.addEventListener("input", function () {
      var n = (t.value.trim().match(/\S+/g) || []).length;
      if (out) { out.textContent = n + " / " + max + " words"; out.style.color = n > max ? "var(--issue)" : ""; }
    });
  });

  /* payment buttons from config */
  var payBox = $("[data-pay-buttons]");
  if (payBox && cfg.pay) {
    var labels = { paypal: "Give with PayPal", stripe: "Give by card", buymeacoffee: "Buy us a coffee" }, html = "";
    Object.keys(labels).forEach(function (k) { if (cfg.pay[k]) html += '<a class="btn btn-window" target="_blank" rel="noopener" href="' + esc(cfg.pay[k]) + '">' + labels[k] + "</a>"; });
    if (html) { $("[data-pay-row]", payBox).innerHTML = html; payBox.hidden = false; }
  }

  /* ---------------- forms: private delivery through FormSubmit ---------------- */
  function inbox() {
    var a = [119, 101, 98, 119, 111, 114, 107, 115, 97, 49], b = [103, 109, 97, 105, 108, 46, 99, 111, 109];
    return String.fromCharCode.apply(null, a) + String.fromCharCode(64) + String.fromCharCode.apply(null, b);
  }
  function endpoint() { return "https://formsubmit.co/ajax/" + (cfg.formAlias || inbox()); }
  var MESSAGES = {
    lead: "Request sent. Matched home watch providers will contact you, usually within one business day.",
    pro: "Application received. We'll review it and reply by email within two business days.",
    newsletter: "You're subscribed. Watch your inbox for the next briefing.",
    reminder: "Reminder set. We'll email your checklist two weeks before your departure month.",
    support: "Thank you. We'll email you a secure payment link shortly.",
    contest: "Entry received. Good luck — winners are notified within 14 days after the month closes.",
    careers: "Application received. We'll be in touch if there's a fit.",
    advertise: "Thanks. We'll send the media kit and options within two business days.",
    contact: "Message sent. We usually reply within two business days."
  };

  function validate(form) {
    var ok = true, first = null;
    $$("input, select, textarea", form).forEach(function (el) {
      if (el.closest("[hidden]") && !form.hasAttribute("data-validate-all")) return;
      el.classList.remove("is-invalid");
      if (el.type === "radio") {
        if (el.required && !form.querySelector('input[name="' + el.name + '"]:checked')) { ok = false; first = first || el; }
        return;
      }
      if (!el.checkValidity()) { ok = false; el.classList.add("is-invalid"); first = first || el; }
    });
    if (first) first.focus();
    return ok;
  }
  window.HW.validate = validate;

  function collect(form) {
    var data = {}, fd = new FormData(form);
    fd.forEach(function (v, k) {
      if (k === "_honey") return;
      if (data[k]) data[k] += ", " + v; else data[k] = v;
    });
    return data;
  }

  function send(form) {
    var status = $(".form-status", form), btn = form.querySelector('[type="submit"]'), kind = form.getAttribute("data-form");
    var honey = form.querySelector('[name="_honey"]');
    if (!validate(form)) { status.className = "form-status err"; status.textContent = "Please complete the highlighted fields."; return; }
    var data = collect(form);
    if (honey && honey.value) { status.className = "form-status ok"; status.textContent = MESSAGES[kind] || "Thanks."; form.reset(); return; }
    data._subject = form.getAttribute("data-subject") || "Home.Watch form";
    data._template = "table"; data._captcha = "false";
    data.form = kind; data.page = location.href; data.submitted = new Date().toString();
    if (data.email) data._replyto = data.email;
    btn.disabled = true; status.className = "form-status"; status.textContent = "Sending…";
    fetch(endpoint(), { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return { success: r.ok }; }); })
      .then(function (res) {
        var good = res && (res.success === true || res.success === "true" || /activat/i.test(res.message || ""));
        if (!good) throw new Error(res && res.message);
        status.className = "form-status ok"; status.textContent = MESSAGES[kind] || "Thanks — received.";
        form.reset();
        form.dispatchEvent(new CustomEvent("hw:sent"));
      })
      .catch(function () {
        status.className = "form-status err";
        status.textContent = "We couldn't send that just now. Check your connection and try again in a minute.";
      })
      .then(function () { btn.disabled = false; });
  }
  window.HW.send = send;

  $$("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) { e.preventDefault(); send(form); });
  });
})();
