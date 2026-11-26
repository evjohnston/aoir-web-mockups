/* Shared chrome for the Neon mockup: masthead, nav row, footer, page-color picker. */
(function () {
  var page = document.body.getAttribute("data-page") || "home";
  var LOGO =
    '<svg viewBox="0 0 132 56" role="img" aria-label="AoIR">' +
    '<text x="0" y="48" font-family="Arial Black, sans-serif" font-weight="900" font-size="56" letter-spacing="-3">A</text>' +
    '<circle cx="48" cy="31" r="13"/>' +
    '<text x="64" y="48" font-family="Arial Black, sans-serif" font-weight="900" font-size="56" letter-spacing="-2">IR</text>' +
    "</svg>";
  var NAV = [
    ["about", "about.html", "About"], ["news", "news.html", "News"], ["conference", "conference.html", "Conferences"],
    ["publications", "publications.html", "Publications"], ["membership", "membership.html", "Membership"],
    ["awards", "awards.html", "Awards"], ["ethics", "ethics.html", "Ethics"], ["archive", "#", "AoIRchive"]
  ];
  var COLORS = [["White", "#ffffff"], ["Black", "#000000"], ["Ink blue", "#101a6b"]];

  var top = document.getElementById("chrome-top");
  if (top) {
    top.innerHTML =
      '<div class="mast">' +
      '<div class="blk c-pink logo-blk"><a href="index.html" title="AoIR home">' + LOGO + "</a></div>" +
      '<div class="blk c-green title"><a class="name" href="index.html">Internet<br>Researchers</a>' +
      '<span class="issue">Issue 2026.11 · Since 1998 · 27 meetings and counting</span></div>' +
      '<div class="acts"><a class="c-yellow" href="membership.html">Join</a><a class="c-white" href="login.html"' +
      (page === "login" ? ' aria-current="page"' : "") + ">Log in</a></div>" +
      "</div>" +
      '<nav class="navrow" aria-label="Main" style="margin-top:var(--gap)">' +
      NAV.map(function (n) {
        return '<a href="' + n[1] + '"' + (n[0] === page ? ' aria-current="page"' : "") + ">" + n[2] + "</a>";
      }).join("") +
      "</nav>";
  }

  var bottom = document.getElementById("chrome-bottom");
  if (bottom) {
    bottom.className = "foot";
    bottom.innerHTML =
      '<div>© Association of Internet Researchers&nbsp;&nbsp; <a href="#">Code of conduct</a><a href="#">Privacy</a><a href="#">Bylaws</a><a href="#">Contact</a><a href="#">aoir.social</a></div>' +
      '<div class="picker" role="group" aria-label="Page color">page:' +
      COLORS.map(function (c) {
        return '<button type="button" title="' + c[0] + '" aria-label="' + c[0] + '" data-c="' + c[1] + '" style="background:' + c[1] + '"></button>';
      }).join("") +
      "</div>";
  }

  function setPage(c) {
    document.documentElement.style.setProperty("--page", c);
    document.body.classList.toggle("on-white", /^#?f{6}$/i.test(c.replace("#", "")) || c.toLowerCase() === "#ffffff");
    document.querySelectorAll(".picker button").forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-c") === c ? "true" : "false");
    });
    try { localStorage.setItem("aoir-neon-page", c); } catch (e) {}
  }
  var saved = null;
  try { saved = localStorage.getItem("aoir-neon-page"); } catch (e) {}
  var qs = new URLSearchParams(location.search).get("bg");
  setPage(qs ? "#" + qs.replace("#", "") : saved || COLORS[0][1]);
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".picker button");
    if (b) setPage(b.getAttribute("data-c"));
  });
})();
