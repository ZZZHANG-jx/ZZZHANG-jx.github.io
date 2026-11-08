(function () {
  "use strict";

  var imgs = Array.prototype.slice.call(
    document.querySelectorAll(".paper-media img")
  );
  var lb = document.getElementById("lightbox");
  if (!lb || imgs.length === 0) return;

  var lbImg = document.getElementById("lbImg");

  var scale = 1;
  var MIN = 0.4;
  var MAX = 6;

  function applyScale() {
    lbImg.style.transform = "scale(" + scale + ")";
    lbImg.style.cursor = scale > 1 ? "zoom-out" : "zoom-in";
  }

  function open(im) {
    lbImg.src = im.getAttribute("data-full") || im.src;
    lbImg.alt = ""; // keep empty so no alt text flashes top-left
    scale = 1;
    lbImg.style.transform = "scale(1)";
    lbImg.style.cursor = "zoom-in";
    lb.classList.add("open");
    lb.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function close() {
    lb.classList.remove("open");
    lb.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    scale = 1;
    lbImg.style.transform = "scale(1)";
  }

  imgs.forEach(function (im) {
    im.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      open(im);
    });
  });

  document.getElementById("lbClose").addEventListener("click", close);
  lb.addEventListener("click", function (e) {
    if (e.target === lb || e.target === lbImg) close();
  });
  lb.addEventListener("wheel", function (e) {
    if (!lb.classList.contains("open")) return;
    e.preventDefault();
    var factor = e.deltaY < 0 ? 1.12 : 0.89;
    scale = Math.min(MAX, Math.max(MIN, scale * factor));
    applyScale();
  }, { passive: false });
  document.addEventListener("keydown", function (e) {
    if (!lb.classList.contains("open")) return;
    if (e.key === "Escape") close();
    else if (e.key === "+" || e.key === "=") { scale = Math.min(MAX, scale * 1.12); applyScale(); }
    else if (e.key === "-" || e.key === "_") { scale = Math.max(MIN, scale * 0.89); applyScale(); }
    else if (e.key === "0") { scale = 1; applyScale(); }
  });
})();
