/* "Take me back to ____": a small button that opens a panel of past aoir.org
   designs. Picking one shows today's content rebuilt in that year's design.
   Include on any page with <script src=".../assets/timemachine.js"></script>. */
(function () {
  if (document.getElementById("aoir-tm")) return;
  var me = document.currentScript;
  var ROOT = new URL("..", me.src).href;          // repo root
  var ERAS = [
    { y: "1999", name: "Hand-coded", ready: true },
    { y: "2000", name: "a(o).i.r", ready: true },
    { y: "2005", name: "Drupal blue", ready: true },
    { y: "2009", name: "AoIR on gray", ready: true },
    { y: "2012", name: "Chateau", ready: true },
    { y: "2014", name: "Responsive", ready: true },
    { y: "2022", name: "Refresh", ready: true },
    { y: "2024", name: "Divi", ready: true }
  ];
  var KEY = "aoir-timemachine-return";
  var m = location.href.match(/\/timemachine\/(\d{4})\//);
  var current = m ? m[1] : null;

  function get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }

  // remember which mockup page to come back to
  if (!current) set(KEY, location.href.replace(/[?#].*$/, ""));
  var back = get(KEY) || ROOT + "windowed/index.html";
  var backBase = back.replace(/[^/]*$/, "");

  // inside an era page, point "today" links (data-to="membership") at the mockup you came from
  if (current) {
    document.querySelectorAll("a[data-to]").forEach(function (a) {
      a.href = backBase + a.getAttribute("data-to") + ".html";
    });
  }

  var F = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif";
  var css = [
    "#aoir-tm,#aoir-tm *{box-sizing:border-box;margin:0;padding:0;font-family:" + F + ";letter-spacing:0;text-transform:none;text-shadow:none;line-height:1.3}",
    "#aoir-tm{position:fixed;right:16px;bottom:16px;z-index:2147483000;color:#111;font-size:13px}",
    "#aoir-tm .tm-btn{display:inline-flex;align-items:center;gap:8px;height:38px;padding:0 15px 0 11px;border-radius:999px;border:1px solid rgba(0,0,0,.18);background:#fff;color:#111;font-size:13px;font-weight:600;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.16),0 1px 2px rgba(0,0,0,.12);transition:transform .12s ease,box-shadow .12s ease}",
    "#aoir-tm .tm-btn:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(0,0,0,.2),0 1px 2px rgba(0,0,0,.12)}",
    "#aoir-tm .tm-btn svg{width:18px;height:18px;flex:none}",
    "#aoir-tm .tm-btn .yr{font-variant-numeric:tabular-nums;background:#111;color:#fff;border-radius:999px;padding:2px 7px;font-size:11px;font-weight:700}",
    "#aoir-tm .tm-panel{position:absolute;right:0;bottom:48px;width:min(600px,calc(100vw - 32px));max-height:calc(100vh - 90px);overflow:auto;background:#fff;border:1px solid rgba(0,0,0,.14);border-radius:14px;box-shadow:0 18px 50px rgba(0,0,0,.25);padding:16px;opacity:0;transform:translateY(6px) scale(.98);transform-origin:bottom right;pointer-events:none;transition:opacity .16s ease,transform .16s ease}",
    "#aoir-tm.open .tm-panel{opacity:1;transform:none;pointer-events:auto}",
    "#aoir-tm .tm-head{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:4px}",
    "#aoir-tm h2{font-size:16px;font-weight:700}",
    "#aoir-tm .tm-sub{color:#555;font-size:12.5px;margin-bottom:12px}",
    "#aoir-tm .tm-x{border:0;background:none;font-size:22px;line-height:1;color:#555;cursor:pointer;padding:0 2px}",
    "#aoir-tm .tm-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}",
    "@media (max-width:560px){#aoir-tm .tm-grid{grid-template-columns:repeat(2,minmax(0,1fr))}#aoir-tm{right:12px;bottom:12px}}",
    "#aoir-tm .tm-card{display:block;text-decoration:none;color:#111;border-radius:9px;border:1px solid rgba(0,0,0,.12);overflow:hidden;background:#fff;transition:border-color .12s,box-shadow .12s,transform .12s}",
    "#aoir-tm a.tm-card:hover{border-color:#111;box-shadow:0 4px 12px rgba(0,0,0,.14);transform:translateY(-1px)}",
    "#aoir-tm .tm-card img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;object-position:top;background:#eee;border-bottom:1px solid rgba(0,0,0,.08)}",
    "#aoir-tm .tm-card .t{display:block;padding:7px 9px 8px}",
    "#aoir-tm .tm-card b{display:block;font-size:14px;font-weight:700;font-variant-numeric:tabular-nums}",
    "#aoir-tm .tm-card small{display:block;color:#666;font-size:11.5px}",
    "#aoir-tm .tm-card.cur{border:2px solid #111}",
    "#aoir-tm .tm-card.cur small::after{content:' · you are here'}",
    "#aoir-tm .tm-card.soon{opacity:.45}",
    "#aoir-tm .tm-foot{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:12px;padding-top:12px;border-top:1px solid rgba(0,0,0,.1);font-size:12.5px;color:#555}",
    "#aoir-tm .tm-foot a{color:#111;font-weight:600}",
    "#aoir-tm a:focus-visible,#aoir-tm button:focus-visible{outline:2px solid #2f6bff;outline-offset:2px}",
    "@media (prefers-reduced-motion:reduce){#aoir-tm *{transition:none!important}}"
  ].join("");
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  var ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/><path d="M12 7v5l3 2"/></svg>';

  var cards = ERAS.map(function (e) {
    var inner = '<img src="' + ROOT + "assets/timemachine/" + e.y + '.jpg" alt="" loading="lazy" width="320" height="240">' +
      '<span class="t"><b>' + e.y + "</b><small>" + e.name + (e.ready ? "" : " · soon") + "</small></span>";
    if (!e.ready) return '<span class="tm-card soon" aria-disabled="true">' + inner + "</span>";
    return '<a class="tm-card' + (e.y === current ? " cur" : "") + '" href="' + ROOT + "timemachine/" + e.y + '/index.html"' +
      (e.y === current ? ' aria-current="page"' : "") + ">" + inner + "</a>";
  }).join("");

  var box = document.createElement("div");
  box.id = "aoir-tm";
  box.innerHTML =
    '<div class="tm-panel" id="aoir-tm-panel" role="dialog" aria-label="Take me back to an earlier aoir.org">' +
      '<div class="tm-head"><h2>Take me back to…</h2><button type="button" class="tm-x" aria-label="Close">&times;</button></div>' +
      '<p class="tm-sub">Today’s AoIR, in the designs aoir.org has worn since 1999.</p>' +
      '<div class="tm-grid">' + cards + "</div>" +
      '<div class="tm-foot"><span>Designs rebuilt from the Internet Archive.</span>' +
        (current ? '<a href="' + back + '">← Back to today</a>' : "") + "</div>" +
    "</div>" +
    '<button type="button" class="tm-btn" aria-expanded="false" aria-controls="aoir-tm-panel">' + ICON +
      (current ? "Time machine <span class=\"yr\">" + current + "</span>" : "Take me back") + "</button>";
  document.body.appendChild(box);

  var btn = box.querySelector(".tm-btn");
  function open(v) {
    box.classList.toggle("open", v);
    btn.setAttribute("aria-expanded", v ? "true" : "false");
    if (v) { var f = box.querySelector(".tm-card.cur, a.tm-card"); if (f) f.focus({ preventScroll: true }); }
  }
  btn.addEventListener("click", function () { open(!box.classList.contains("open")); });
  box.querySelector(".tm-x").addEventListener("click", function () { open(false); btn.focus(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && box.classList.contains("open")) { open(false); btn.focus(); } });
  document.addEventListener("click", function (e) { if (!box.contains(e.target)) open(false); });
  if (/[#&?]tm=open\b/.test(location.href)) open(true);   // shareable: ...index.html#tm=open
})();
