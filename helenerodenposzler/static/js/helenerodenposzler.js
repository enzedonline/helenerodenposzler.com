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
  // stop link buttons retaining focus after click
  $(".link-button").mouseup(function(){
    $(this).blur();
  })

});
