$(document).ready(function () {
  // set all external links to open in new tab
  $('a[href^="http://"]').attr("target", "_blank");
  $('a[href^="http://"]').attr("rel", "nofollow noopener");
  $('a[href^="https://"]').attr("target", "_blank");
  $('a[href^="https://"]').attr("rel", "nofollow noopener");
  // set drop right menu button properties
  $(".dropright button").on("click", function (e) {
    e.stopPropagation();
    e.preventDefault();
    if (!$(this).next("div").hasClass("show")) {
      $(this).next("div").addClass("show");
    } else {
      $(this).next("div").removeClass("show");
    }
  });
  // stop mobile menu toggler retaining focus after click
  $(".navbar-toggler").mouseup(function () {
    $(this).blur();
  });
});

// add hreflang links to <head> (called from language switcher)
// <link rel="alternate" hreflang="fr" href="https://helenerodenposzler.com/fr/"></link>
// <link rel="alternate" hreflang="x-default" href="https://helenerodenposzler.com/en/"></link>
const addLangLinks = (linksID) => {
  const links = JSON.parse(document.getElementById(linksID).textContent);
  if (links) {
    for (const link of links) {
      linkElement = document.createElement("link");
      linkElement.rel = "alternate";
      linkElement.hreflang = link.hreflang;
      linkElement.href = link.href;
      document.head.append(linkElement);
    }
  }
};
