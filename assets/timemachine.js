/* "Take me back to ____": a small floating control that swaps the current
   site for a rebuild of an earlier aoir.org design, with today's content.
   Include on any page with <script src=".../assets/timemachine.js"></script>. */
(function () {
  var me = document.currentScript;
  var ROOT = new URL("..", me.src).href;          // repo root
  var ERAS = [
    { y: "1999", label: "1999 · hand-coded", ready: true },
    { y: "2000", label: "2000 · a(o).i.r light blue" },
    { y: "2005", label: "2005 · a.o.i.r. blue header" },
    { y: "2009", label: "2009 · AoIR bar on gray" },
    { y: "2012", label: "2012 · Chateau", ready: true },
    { y: "2014", label: "2014 · Responsive hero" },
    { y: "2022", label: "2022 · Responsive refresh" },
    { y: "2024", label: "2024 · Divi" }
  ];
  var KEY = "aoir-timemachine-return";
  var here = location.href;
  var m = here.match(/\/timemachine\/(\d{4})\//);
  var current = m ? m[1] : null;

  function get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }

  // remember which mockup to come back to
  if (!current) set(KEY, here.replace(/[?#].*$/, ""));
  var back = get(KEY) || ROOT + "windowed/index.html";
  var backBase = back.replace(/[^/]*$/, "");

  // inside an era page, point "today" links (data-to="membership") at the mockup you came from
  if (current) {
    document.querySelectorAll("a[data-to]").forEach(function (a) {
      a.href = backBase + a.getAttribute("data-to") + ".html";
    });
  }

  var css =
    "#aoir-tm{position:fixed;right:14px;bottom:14px;z-index:2147483000;font:13px/1.3 -apple-system,system-ui,Segoe UI,Helvetica,Arial,sans-serif;" +
    "background:#111;color:#fff;border:2px solid #fff;outline:1px solid #111;padding:8px 10px;display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;max-width:calc(100vw - 28px);box-shadow:0 2px 10px rgba(0,0,0,.35)}" +
    "#aoir-tm label{display:inline;margin:0;padding:0;font:600 13px/1.3 -apple-system,system-ui,Segoe UI,Helvetica,Arial,sans-serif;color:#fff;text-transform:none;letter-spacing:0}" +
    "#aoir-tm select{width:auto;max-width:100%;font:13px -apple-system,system-ui,Segoe UI,Helvetica,Arial,sans-serif;padding:3px 4px;border:1px solid #fff;border-radius:0;background:#111;color:#fff;box-shadow:none}" +
    "#aoir-tm a{color:#fff;text-decoration:underline}#aoir-tm a:hover{background:#fff;color:#111}" +
    "#aoir-tm button{width:auto;box-shadow:none;border-radius:0;text-transform:none;letter-spacing:0;font:600 13px -apple-system,system-ui,Segoe UI,Helvetica,Arial,sans-serif;background:#fff;color:#111;border:0;padding:3px 9px;cursor:pointer}" +
    "#aoir-tm select:focus-visible,#aoir-tm button:focus-visible,#aoir-tm a:focus-visible{outline:2px solid #ffd400;outline-offset:2px}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  var box = document.createElement("div");
  box.id = "aoir-tm";
  box.setAttribute("role", "region");
  box.setAttribute("aria-label", "Time machine");
  var opts = ERAS.map(function (e) {
    return '<option value="' + e.y + '"' + (e.ready ? "" : " disabled") + (e.y === current ? " selected" : "") + ">" +
      e.label + (e.ready ? "" : " (coming soon)") + "</option>";
  }).join("");
  box.innerHTML =
    '<label for="aoir-tm-sel">' + (current ? "You're in " + current + ". Go to" : "Take me back to") + "</label>" +
    '<select id="aoir-tm-sel">' + (current ? "" : '<option value="" selected>choose a year…</option>') + opts + "</select>" +
    '<button type="button">Go</button>' +
    (current ? '<a href="' + back + '">Back to today</a>' : "");
  document.body.appendChild(box);

  function go() {
    var y = box.querySelector("select").value;
    if (y && y !== current) location.href = ROOT + "timemachine/" + y + "/index.html";
  }
  box.querySelector("button").addEventListener("click", go);
  box.querySelector("select").addEventListener("change", function () { if (!current) go(); });
})();
