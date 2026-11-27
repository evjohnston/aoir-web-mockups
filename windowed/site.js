/* Shared chrome for the Windowed mockup: header window, footer window, backdrop picker. */
(function () {
  var page = document.body.getAttribute("data-page") || "home";

  var LOGO = '<img src="../assets/aoir-mark.svg" alt="AoIR">';

  var NAV = [
    ["home", "index.html", "/home"],
    ["about", "about.html", "/about"],
    ["news", "news.html", "/news"],
    ["conference", "conference.html", "/conference"],
    ["publications", "publications.html", "/publications"],
    ["membership", "membership.html", "/membership"],
    ["awards", "awards.html", "/awards"],
    ["ethics", "ethics.html", "/ethics"],
    ["login", "login.html", "/login"]
  ];

  var COLORS = [
    ["Cobalt", "#2f46e6"],
    ["Tomato", "#ff5a36"],
    ["Mint", "#2bd889"],
    ["Lilac", "#b79cff"],
    ["Pink", "#ff5fb4"],
    ["Ink", "#1b1b1b"],
    ["Cream (original)", "#fffdf3"]
  ];

  var nav = NAV.map(function (n) {
    return '<a href="' + n[1] + '"' + (n[0] === page ? ' aria-current="page"' : "") + ">" + n[2] + "</a>";
  }).join("");

  var file = (NAV.filter(function (n) { return n[0] === page; })[0] || NAV[0])[1];

  var top = document.getElementById("chrome-top");
  if (top) {
    top.className = "win site-head span-12";
    top.innerHTML =
      '<div class="win-bar"><span class="file">aoir.org/' + file + '</span><span class="ctl"><i></i><i></i></span></div>' +
      '<div class="win-body">' +
      '<a class="logo" href="index.html">' + LOGO + "</a>" +
      '<span class="tagline">the Association of Internet Researchers. est. 1998.</span>' +
      '<nav class="site-nav" aria-label="Main">' + nav + "</nav>" +
      "</div>";
  }

  var bottom = document.getElementById("chrome-bottom");
  if (bottom) {
    bottom.className = "win site-foot span-12";
    bottom.innerHTML =
      '<div class="win-bar"><span class="file">&lt;footer&gt;</span><span class="ctl"><i></i><i></i></span></div>' +
      '<div class="win-body">' +
      '<div><div class="links"><a href="#">code of conduct</a><a href="#">privacy</a><a href="#">bylaws</a><a href="#">contact</a><a href="#">aoir.social</a><a href="#">donate</a></div>' +
      '<div class="muted">© 1998–2026 Association of Internet Researchers · last updated 2026-11-26</div></div>' +
      '<div class="picker" role="group" aria-label="Backdrop color"><span>backdrop:</span>' +
      COLORS.map(function (c) {
        return '<button type="button" title="' + c[0] + '" aria-label="' + c[0] + '" data-c="' + c[1] + '" style="background:' + c[1] + '"></button>';
      }).join("") +
      "</div></div>";
  }

  // backdrop picker (mockup-only control, remembered per browser)
  function setBg(c) {
    document.documentElement.style.setProperty("--bg", c);
    document.querySelectorAll(".picker button").forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-c") === c ? "true" : "false");
    });
    try { localStorage.setItem("aoir-windowed-bg", c); } catch (e) {}
  }
  var saved = null;
  try { saved = localStorage.getItem("aoir-windowed-bg"); } catch (e) {}
  var qs = new URLSearchParams(location.search).get("bg");
  setBg(qs ? "#" + qs.replace("#", "") : saved || COLORS[0][1]);
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".picker button");
    if (b) setBg(b.getAttribute("data-c"));
  });
})();

/* time machine switcher ("Take me back to ____") */
(function () {
  var s = document.createElement("script");
  s.src = "../assets/timemachine.js";
  document.body.appendChild(s);
})();
