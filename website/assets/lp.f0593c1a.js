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
  window.dataLayer.push({event: "page_variant", variant: VARIANT, case_type: CT, geo: GEO});
  document.addEventListener("click", function(e){ if (e.target.closest && e.target.closest('a[href^="tel:"]')) track("call_click"); });

  /* ?kw= swaps the H1 to match the ad group that sent the click (allow-listed so no one can inject text). */
  var KW = {"car-accident-lawyer":"Summerville Car Accident Lawyer", "car-accident-attorney":"Summerville Car Accident Attorney", "auto-accident-lawyer":"Summerville Auto Accident Lawyer",
            "accident-lawyer":"Summerville Accident Lawyer", "injury-lawyer":"Summerville Injury Lawyer", "personal-injury-lawyer":"Summerville Personal Injury Lawyer",
            "car-wreck-lawyer":"Summerville Car Wreck Lawyer", "truck-accident-lawyer":"Summerville Truck Accident Lawyer", "motorcycle-accident-lawyer":"Summerville Motorcycle Accident Lawyer"};
  var kw = (q.get("kw") || "").toLowerCase();
  var h1 = document.getElementById("h1");
  if (KW[kw] && h1) { h1.textContent = KW[kw]; track("h1_swap", {kw: kw}); }

  /* Two-step form, like the Goldberg & Loren landers: step 1 is one tap ("Were you injured?"), step 2 is name and mobile
     phone with an explicit consent box, and success shows inline with a call button. Formspree gets the lead; the
     lead_form_submit dataLayer event is the Google Ads conversion. */
  FORMS.forEach(function(cfg){
    var form = document.getElementById(cfg.id); if (!form) return;
    var steps = form.querySelectorAll(".fstep"), label = form.querySelector(".step-text"), dots = form.querySelectorAll(".dots i");
    var err = form.querySelector(".ferr"), btn = form.querySelector('button[type="submit"]'), answer = "";
    function show(n){
      steps.forEach(function(s){ s.hidden = s.getAttribute("data-step") !== String(n); });
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
      if (consent && !consent.checked) return fail("Please tick the box so we can call or text you back.");
      fail("");
      data.phone = ph; data.injured = answer || "not answered"; data.consent = "checked the consent box";
      function done(){
        track("lead_form_submit", {form: cfg.where, injured: data.injured});
        var sn = form.querySelector(".s-name"); if (sn) sn.textContent = ", " + data.name.split(" ")[0];
        show(3); var proof = form.querySelector(".fproof"); if (proof) proof.hidden = true;
      }
      if (form.querySelector('[name="_gotcha"]').value !== "") { done(); return; }  /* bots see success, nothing is sent */
      data.case_type = CT; data.geo = GEO; data.variant = VARIANT; data.form = cfg.where;
      data.page = location.href; data.submitted = new Date().toISOString();
      ["gclid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "kw"].forEach(function(k){ if (q.get(k)) data[k] = q.get(k); });
      data._subject = "PPC lead (" + CT + ", " + VARIANT + "): " + data.name;
      var text = btn.textContent, settled = false; btn.disabled = true; btn.textContent = "Sending…";
      function sendFail(status, detail){ if (settled) return; settled = true; btn.disabled = false; btn.textContent = text;
        try { console.error("Lead form send failed:", status, detail); } catch (e2) {}
        track("lead_form_error", {error_status: String(status)});
        fail("We couldn't send your form. Please call " + PHONE + " instead, free, 24/7."); }
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
