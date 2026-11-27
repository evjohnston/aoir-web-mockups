/* Shared chrome for the Classic mockup: menu bar, desktop icons, bottom strip,
   desktop-color picker, live clock, draggable windows and windowshade. */
(function () {
  var page = document.body.getAttribute("data-page") || "home";

  var LOGO = '<img src="../assets/aoir-mark.svg" alt="AoIR">';

  // 1-bit icons on a 16px grid; white fill so they read on any desktop color
  var S = 'fill="#fff" stroke="#000" stroke-width="1"';
  var I = {
    about: '<rect x="3.5" y="1.5" width="9" height="13" ' + S + '/><rect x="7" y="4" width="2" height="2"/><rect x="7" y="7" width="2" height="5"/><rect x="6" y="11" width="4" height="1"/>',
    news: '<rect x="1.5" y="3.5" width="13" height="10" ' + S + '/><rect x="3" y="5" width="5" height="3"/><rect x="9" y="5" width="4" height="1"/><rect x="9" y="7" width="4" height="1"/><rect x="3" y="9" width="10" height="1"/><rect x="3" y="11" width="10" height="1"/>',
    conference: '<rect x="1.5" y="3.5" width="13" height="11" ' + S + '/><rect x="2" y="4" width="12" height="2"/><rect x="4" y="2" width="1" height="3"/><rect x="11" y="2" width="1" height="3"/><rect x="4" y="8" width="2" height="2"/><rect x="7" y="8" width="2" height="2"/><rect x="10" y="8" width="2" height="2"/><rect x="4" y="11" width="2" height="2"/><rect x="7" y="11" width="2" height="2"/>',
    publications: '<rect x="1.5" y="3.5" width="6" height="10" ' + S + '/><rect x="8.5" y="3.5" width="6" height="10" ' + S + '/><rect x="3" y="6" width="3" height="1"/><rect x="3" y="8" width="3" height="1"/><rect x="10" y="6" width="3" height="1"/><rect x="10" y="8" width="3" height="1"/>',
    membership: '<rect x="1.5" y="3.5" width="13" height="9" ' + S + '/><rect x="3" y="5" width="4" height="4"/><rect x="8" y="5" width="5" height="1"/><rect x="8" y="7" width="5" height="1"/><rect x="3" y="10" width="10" height="1"/>',
    awards: '<circle cx="8" cy="6" r="4.5" ' + S + '/><circle cx="8" cy="6" r="2"/><path d="M5.5 9.5 L4.5 15 L6.5 13.5 L8 15 L9.5 13.5 L11.5 15 L10.5 9.5" ' + S + '/>',
    ethics: '<rect x="7" y="2" width="2" height="12"/><rect x="2" y="4" width="12" height="1"/><rect x="4" y="13" width="8" height="2"/><path d="M1.5 9.5 L3.5 5 L5.5 9.5 Z" ' + S + '/><path d="M10.5 9.5 L12.5 5 L14.5 9.5 Z" ' + S + '/>',
    archive: '<rect x="1.5" y="3.5" width="13" height="3" ' + S + '/><rect x="2.5" y="6.5" width="11" height="8" ' + S + '/><rect x="6" y="8" width="4" height="2"/>',
    airl: '<rect x="1.5" y="4.5" width="13" height="9" ' + S + '/><path d="M2 5 L8 10 L14 5" fill="none" stroke="#000"/>',
    login: '<rect x="3.5" y="7.5" width="9" height="7" ' + S + '/><path d="M5.5 7.5 V5 a2.5 2.5 0 0 1 5 0 V7.5" fill="none" stroke="#000" stroke-width="1.5"/><rect x="7" y="10" width="2" height="3"/>',
    trash: '<rect x="3.5" y="4.5" width="9" height="10" ' + S + '/><rect x="2" y="3" width="12" height="1.5"/><rect x="6" y="1.5" width="4" height="1.5"/><rect x="6" y="6" width="1" height="7"/><rect x="9" y="6" width="1" height="7"/>'
  };
  function svg(k) { return '<svg viewBox="0 0 16 16" shape-rendering="crispEdges" aria-hidden="true">' + I[k] + "</svg>"; }

  var NAV = [
    ["about", "about.html", "About"],
    ["news", "news.html", "News"],
    ["conference", "conference.html", "Conference"],
    ["publications", "publications.html", "Publications"],
    ["membership", "membership.html", "Membership"],
    ["awards", "awards.html", "Awards"],
    ["ethics", "ethics.html", "Ethics"]
  ];

  var COLORS = [
    ["Tangerine", "#f2753a"],
    ["Bondi", "#0d97b0"],
    ["Periwinkle", "#7b86d8"],
    ["Sage", "#93bf9c"],
    ["Grape", "#6a4bb8"],
    ["Lime", "#c6e34c"],
    ["Platinum", "#b9b9b9"]
  ];

  var mb = document.getElementById("menubar");
  if (mb) {
    mb.className = "menubar";
    mb.innerHTML =
      '<a class="logo" href="index.html" title="AoIR home">' + LOGO + "</a>" +
      '<nav class="menus" aria-label="Main">' +
      NAV.map(function (n) {
        return '<a class="m" href="' + n[1] + '"' + (n[0] === page ? ' aria-current="page"' : "") + ">" + n[2] + "</a>";
      }).join("") +
      "</nav>" +
      '<div class="right"><a class="m" href="login.html"' + (page === "login" ? ' aria-current="page"' : "") + '>Log In…</a><span class="clock" id="clock"></span><span class="app">AoIR</span></div>';
  }

  var ic = document.getElementById("icons");
  if (ic) {
    var DESK = [
      ["home", "index.html", "AoIR HD", "archive"],
      ["about", "about.html", "About", "about"],
      ["news", "news.html", "News", "news"],
      ["conference", "conference.html", "Conference", "conference"],
      ["publications", "publications.html", "Publications", "publications"],
      ["membership", "membership.html", "Membership", "membership"],
      ["awards", "awards.html", "Awards", "awards"],
      ["ethics", "ethics.html", "Ethics", "ethics"],
      ["airl", "about.html#air-l", "AIR-L", "airl"],
      ["trash", "#", "Trash", "trash"]
    ];
    ic.className = "icons";
    ic.setAttribute("aria-label", "Desktop");
    ic.innerHTML = DESK.map(function (d) {
      return '<a class="icon" href="' + d[1] + '"' + (d[0] === page ? ' aria-current="page"' : "") + ">" + svg(d[3]) + "<span>" + d[2] + "</span></a>";
    }).join("");
  }

  var st = document.getElementById("strip");
  if (st) {
    st.className = "strip";
    st.innerHTML =
      "<span>© Association of Internet Researchers</span>" +
      '<a href="#">Code of conduct</a><a href="#">Privacy</a><a href="#">Bylaws</a><a href="#">Contact</a><a href="#">aoir.social</a><a href="#">Donate</a>' +
      '<span class="picker" role="group" aria-label="Desktop color">Desktop:' +
      COLORS.map(function (c) {
        return '<button type="button" title="' + c[0] + '" aria-label="' + c[0] + '" data-c="' + c[1] + '" style="background:' + c[1] + '"></button>';
      }).join("") +
      "</span>";
  }

  // desktop color
  function setDesk(c) {
    document.documentElement.style.setProperty("--desk", c);
    document.querySelectorAll(".picker button").forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-c") === c ? "true" : "false");
    });
    try { localStorage.setItem("aoir-classic-desk", c); } catch (e) {}
  }
  var saved = null;
  try { saved = localStorage.getItem("aoir-classic-desk"); } catch (e) {}
  var qs = new URLSearchParams(location.search).get("bg");
  setDesk(qs ? "#" + qs.replace("#", "") : saved || COLORS[0][1]);
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".picker button");
    if (b) setDesk(b.getAttribute("data-c"));
  });

  // clock
  var clock = document.getElementById("clock");
  function tick() {
    if (!clock) return;
    clock.textContent = new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
  }
  tick(); setInterval(tick, 15000);

  // windowshade: shade box (right) and close box (left) collapse the window; double-click title bar too
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".titlebar button");
    if (!b) return;
    var w = b.closest(".window");
    w.classList.toggle("shaded");
    b.setAttribute("aria-expanded", w.classList.contains("shaded") ? "false" : "true");
  });
  document.addEventListener("dblclick", function (e) {
    var t = e.target.closest(".titlebar");
    if (t && !e.target.closest("button")) t.closest(".window").classList.toggle("shaded");
  });

  // drag windows by their title bar (desktop widths only)
  var drag = null;
  document.addEventListener("pointerdown", function (e) {
    var t = e.target.closest(".titlebar");
    if (!t || e.target.closest("button") || window.innerWidth < 920) return;
    var w = t.closest(".window");
    var m = (w.style.transform || "").match(/translate\((-?[\d.]+)px,\s*(-?[\d.]+)px\)/);
    drag = { w: w, x: e.clientX, y: e.clientY, ox: m ? +m[1] : 0, oy: m ? +m[2] : 0 };
    w.classList.add("dragging");
    t.setPointerCapture(e.pointerId);
  });
  document.addEventListener("pointermove", function (e) {
    if (!drag) return;
    drag.w.style.transform = "translate(" + (drag.ox + e.clientX - drag.x) + "px, " + (drag.oy + e.clientY - drag.y) + "px)";
  });
  document.addEventListener("pointerup", function () {
    if (drag) { drag.w.classList.remove("dragging"); drag = null; }
  });
})();
