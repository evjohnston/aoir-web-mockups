/* Shared chrome for the Flat mockup: plain header and footer, no picker. */
(function () {
  var page = document.body.getAttribute("data-page") || "home";
  var LOGO =
    '<svg viewBox="0 0 132 56" role="img" aria-label="AoIR">' +
    '<text x="0" y="48" font-family="Inter, Arial Black, sans-serif" font-weight="900" font-size="56" letter-spacing="-3">A</text>' +
    '<circle cx="48" cy="31" r="13"/>' +
    '<text x="64" y="48" font-family="Inter, Arial Black, sans-serif" font-weight="900" font-size="56" letter-spacing="-2">IR</text>' +
    "</svg>";
  var NAV = [
    ["home", "index.html", "/home"], ["about", "about.html", "/about"], ["news", "news.html", "/news"],
    ["conference", "conference.html", "/conference"], ["publications", "publications.html", "/publications"],
    ["membership", "membership.html", "/membership"], ["awards", "awards.html", "/awards"],
    ["ethics", "ethics.html", "/ethics"], ["login", "login.html", "/login"]
  ];
  var top = document.getElementById("chrome-top");
  if (top) {
    top.className = "flat-head";
    top.innerHTML =
      '<span class="tag-l">&lt;header&gt;</span>' +
      '<a class="logo" href="index.html">' + LOGO + "</a>" +
      '<p class="tagline">aoir.org — the Association of Internet Researchers. est. 1998.</p>' +
      '<nav class="site-nav" aria-label="Main">' +
      NAV.map(function (n) { return '<a href="' + n[1] + '"' + (n[0] === page ? ' aria-current="page"' : "") + ">" + n[2] + "</a>"; }).join("") +
      "</nav>";
  }
  var bottom = document.getElementById("chrome-bottom");
  if (bottom) {
    bottom.className = "flat-foot";
    bottom.innerHTML =
      '<div>this site is hand-coded and has no trackers. feeds: <a href="#">rss</a> · <a href="#">atom</a> · <a href="#">json</a></div>' +
      '<div><a href="#">code of conduct</a> · <a href="#">privacy</a> · <a href="#">bylaws</a> · <a href="#">contact</a> · <a href="#">aoir.social</a> · last updated 2026-11-26</div>';
  }
})();
