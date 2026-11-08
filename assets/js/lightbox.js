(function () {
  "use strict";

  var imgs = Array.prototype.slice.call(
    document.querySelectorAll(".paper-media img")
  );
  var lb = document.getElementById("lightbox");
  if (!lb || imgs.length === 0) return;

  var lbImg = document.getElementById("lbImg");

  function open(src, alt) {
    lbImg.src = src;
    lbImg.alt = alt || "";
    lb.classList.add("open");
    lb.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function close() {
    lb.classList.remove("open");
    lb.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  imgs.forEach(function (im) {
    im.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      open(im.src, im.alt);
    });
  });

  document.getElementById("lbClose").addEventListener("click", close);
  lb.addEventListener("click", function (e) {
    if (e.target === lb || e.target === lbImg) close();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && lb.classList.contains("open")) close();
  });
})();
