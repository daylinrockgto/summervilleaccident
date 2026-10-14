(function(){
  "use strict";
  /* Leads post to the firm's Formspree form (shared with the contact page); the thank-you page fires the conversion.
     Each lander sets its case type, geo and variant on <body data-ct data-geo data-variant>. Forms are any form.f[id][data-where];
     their field ids are the form id plus -fn -ln -ph -zip -em -ct -d. */
  var ENDPOINT = "https://formspree.io/f/xdekonez", PHONE = "(843) 419-6653", B = document.body.dataset;
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

  function val(id){ var el = document.getElementById(id); return el ? el.value.trim() : ""; }
  FORMS.forEach(function(cfg){
    var form = document.getElementById(cfg.id); if (!form) return;
    var err = form.querySelector(".ferr"), btn = form.querySelector('button[type="submit"]');
    function fail(msg){ err.textContent = msg; }
    form.addEventListener("submit", function(e){
      e.preventDefault();
      var pre = cfg.pre, data = {};
      data.name = (val(pre + "fn") + " " + val(pre + "ln")).trim();
      data.phone = val(pre + "ph"); data.zip = val(pre + "zip"); data.email = val(pre + "em");
      data.case_type_selected = val(pre + "ct"); data.details = val(pre + "d"); data.consent = "by submitting the form";
      if (!val(pre + "fn")) return fail("Please enter your first name.");
      var ph = data.phone.replace(/\D/g, ""); if (ph.length === 11 && ph.charAt(0) === "1") ph = ph.slice(1);
      if (!(/^[2-9]\d{2}[2-9]\d{6}$/.test(ph) && !/^(\d)\1{9}$/.test(ph) && !/^[2-9]11/.test(ph) && !/^\d{3}[2-9]11/.test(ph)))
        return fail("Please enter a valid 10-digit phone number.");
      data.phone = ph;
      if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) return fail("That email address doesn't look right.");
      fail("");
      var dest = "/lp/thank-you/?geo=" + GEO + "&ct=" + CT + "&variant=" + VARIANT + "&form=" + cfg.where;
      if (form.querySelector('[name="_gotcha"]').value !== "") { location.href = dest; return; }
      data.case_type = CT; data.geo = GEO; data.variant = VARIANT; data.form = cfg.where;
      data.page = location.href; data.submitted = new Date().toISOString();
      ["gclid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "kw"].forEach(function(k){ if (q.get(k)) data[k] = q.get(k); });
      data._subject = "PPC lead (" + CT + ", " + VARIANT + "): " + data.name;
      var label = btn.textContent, settled = false; btn.disabled = true; btn.textContent = "Sending…";
      function sendFail(status, detail){ if (settled) return; settled = true; btn.disabled = false; btn.textContent = label;
        try { console.error("Lead form send failed:", status, detail); } catch (e2) {}
        track("lead_form_error", {error_status: String(status)});
        fail("We couldn't send your form. Please call " + PHONE + " instead — free, 24/7."); }
      setTimeout(function(){ sendFail("timeout", "no response after 12s"); }, 12000);
      try {
        fetch(ENDPOINT, {method: "POST", headers: {"Content-Type": "application/json", "Accept": "application/json"}, body: JSON.stringify(data)})
          .then(function(r){ if (r.ok) { if (!settled) { settled = true; location.href = dest; } }
            else r.text().then(function(t){ sendFail(r.status, t); }, function(){ sendFail(r.status, ""); }); },
            function(e2){ sendFail("network", String(e2)); });
      } catch (e2) { sendFail("exception", String(e2)); }
    });
  });
})();
