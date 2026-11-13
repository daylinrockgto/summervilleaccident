(function(){
  "use strict";
  /* Leads post to the firm's Formspree form (shared with the contact page). Each lander sets its case type, geo and variant
     on <body data-ct data-geo data-variant>. Forms are any form.f[id][data-where] built from site/landers/_parts/form.html. */
  var ENDPOINT = "https://formspree.io/f/xdekonez", PHONE = "(843) 242-0821", B = document.body.dataset;
  var CT = B.ct || "car-accident", GEO = B.geo || "summerville-sc", VARIANT = B.variant || "lp";
  var FORMS = Array.prototype.map.call(document.querySelectorAll("form.f[id][data-where]"), function(f){ return {id: f.id, where: f.getAttribute("data-where"), pre: f.id + "-"}; });
  var q = new URLSearchParams(location.search);

  window.dataLayer = window.dataLayer || [];
  function track(ev, extra){ var e = {event: ev, case_type: CT, geo: GEO, variant: VARIANT}; if (extra) for (var k in extra) e[k] = extra[k]; window.dataLayer.push(e); }
  window.dataLayer.push({event: "page_variant", variant: VARIANT, case_type: CT, geo: GEO, kw: B.kw || (q.get("kw") || "")});
  document.addEventListener("click", function(e){ if (e.target.closest && e.target.closest('a[href^="tel:"]')) track("call_click"); });

  /* The keyword variant is rendered at build time (/lp/<lander>/<kw>/) and served for ?kw= by Vercel middleware, so the
     HTML already carries the ad group's words and data-kw is set. If a base page is served with ?kw= anyway (another host,
     middleware off), swap the H1 and title on the client as a fallback. The allow-list is filled in by the build. */
  var KW_MAP = /*LP_KW*/null, KW_SLUG = B.kw || (q.get("kw") || "").toLowerCase().replace(/[^a-z0-9-]/g, "");
  if (!B.kw && KW_SLUG && KW_MAP) {
    var lander = (location.pathname.match(/^\/lp\/([a-z0-9-]+)\//) || [])[1], h1 = document.getElementById("h1"), text = KW_MAP[lander] && KW_MAP[lander][KW_SLUG];
    if (h1 && text) { h1.textContent = text; document.title = document.title.replace(/^[^|]*\|/, text + " |"); track("h1_swap", {kw: KW_SLUG}); }
  }
  if (KW_SLUG) track("page_keyword", {kw: KW_SLUG});

  /* Two-step form, like the Goldberg & Loren landers: step 1 is one tap ("Were you injured?"), step 2 is name and mobile
     phone with an explicit consent box, and success shows inline with a call button. Formspree gets the lead; the
     lead_form_submit dataLayer event is the Google Ads conversion. */
  FORMS.forEach(function(cfg){
    var form = document.getElementById(cfg.id); if (!form) return;
    var steps = form.querySelectorAll(".fstep"), label = form.querySelector(".step-text"), dots = form.querySelectorAll(".dots i");
    var err = form.querySelector(".ferr"), btn = form.querySelector('button[type="submit"]'), answer = "";
    function show(n){
      steps.forEach(function(s){ s.hidden = s.getAttribute("data-step") !== String(n); });
      /* On phones the sticky bar sits over the bottom of the viewport. Hide it while step 2 is open so it never covers
         the submit button when the keyboard scrolls the field into view (2026-11-13). */
      document.body.classList.toggle("typing", n === 2);
      if (label) label.textContent = n === 3 ? "Done" : "Step " + n + " of 2";
      dots.forEach(function(d, i){ d.className = i < n ? "on" : ""; });
      if (n === 2) { var first = form.querySelector('[name="name"]'); if (first) setTimeout(function(){ first.focus(); }, 50); }
    }
    function fail(msg){ err.textContent = msg; }
    form.querySelectorAll(".opt").forEach(function(o){ o.addEventListener("click", function(){ answer = o.getAttribute("data-v"); track("lead_form_step", {step: 1, injured: answer, form: cfg.where}); show(2); }); });
    var back = form.querySelector(".back"); if (back) back.addEventListener("click", function(){ fail(""); show(1); });
    form.addEventListener("submit", function(e){
      e.preventDefault();
      var data = {};
      data.name = form.querySelector('[name="name"]').value.trim();
      var raw = form.querySelector('[name="phone"]').value.trim(), consent = form.querySelector('input[type="checkbox"]');
      if (!data.name) return fail("Please enter your name.");
      var ph = raw.replace(/\D/g, ""); if (ph.length === 11 && ph.charAt(0) === "1") ph = ph.slice(1);
      if (!(/^[2-9]\d{2}[2-9]\d{6}$/.test(ph) && !/^(\d)\1{9}$/.test(ph) && !/^[2-9]11/.test(ph) && !/^\d{3}[2-9]11/.test(ph)))
        return fail("Please enter a valid 10-digit phone number.");
      fail("");
      /* The consent box is optional (2026-11-04): a person asking for a callback is called back either way, and the firm
         sees "checked" or "not checked" on the lead so it knows whether automated texts are allowed. */
      data.phone = ph; data.injured = answer || "not answered"; data.consent = (consent && consent.checked) ? "checked" : "not checked";
      function finish(){
        var sn = form.querySelector(".s-name"); if (sn) sn.textContent = ", " + data.name.split(" ")[0];
        show(3); var proof = form.querySelector(".fproof"); if (proof) proof.hidden = true;
      }
      function done(){
        /* The conversion. Only reached after Formspree accepts the lead. user_data feeds Google Ads enhanced conversions
           (the phone in E.164); GTM's user-provided data variable reads it from this event. */
        track("lead_form_submit", {form: cfg.where, injured: data.injured, consent: data.consent, user_data: {phone_number: "+1" + ph}});
        finish();
      }
      if (form.querySelector('[name="_gotcha"]').value !== "") { finish(); return; }  /* bots see success; nothing is sent and no conversion fires */
      data.case_type = CT; data.geo = GEO; data.variant = VARIANT; data.form = cfg.where;
      data.page = location.href; data.submitted = new Date().toISOString();
      ["gclid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "kw"].forEach(function(k){ if (q.get(k)) data[k] = q.get(k); });
      if (KW_SLUG) data.kw = KW_SLUG;
      data._subject = "PPC lead (" + CT + ", " + VARIANT + "): " + data.name;
      var text = btn.textContent, settled = false; btn.disabled = true; btn.textContent = "Sending…";
      function sendFail(status, detail){ if (settled) return; settled = true; btn.disabled = false; btn.textContent = text;
        try { console.error("Lead form send failed:", status, detail); } catch (e2) {}
        track("lead_form_error", {error_status: String(status)});
        fail("We couldn't send your form."); err.insertAdjacentHTML("beforeend", ' <a class="errcall" href="tel:+18432420821">Call (843) 242-0821 now</a>, free, 24/7.'); }
      setTimeout(function(){ sendFail("timeout", "no response after 12s"); }, 12000);
      try {
        fetch(ENDPOINT, {method: "POST", headers: {"Content-Type": "application/json", "Accept": "application/json"}, body: JSON.stringify(data)})
          .then(function(r){ if (r.ok) { if (!settled) { settled = true; done(); } }
            else r.text().then(function(t){ sendFail(r.status, t); }, function(){ sendFail(r.status, ""); }); },
            function(e2){ sendFail("network", String(e2)); });
      } catch (e2) { sendFail("exception", String(e2)); }
    });
  });
})();
