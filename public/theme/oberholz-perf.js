/**
 * Lightweight performance helpers – no visual/UX changes.
 * - lazy-load below-the-fold images
 * - async decode
 */
(function () {
  function enhanceImages() {
    var imgs = document.images;
    for (var i = 0; i < imgs.length; i++) {
      var img = imgs[i];
      if (!img || img.dataset.oberholzPerf === "1") continue;
      img.dataset.oberholzPerf = "1";

      // Keep above-the-fold / explicitly eager images untouched
      var loading = (img.getAttribute("loading") || "").toLowerCase();
      var fetchPriority = (img.getAttribute("fetchpriority") || "").toLowerCase();
      if (loading !== "eager" && fetchPriority !== "high" && !img.hasAttribute("loading")) {
        img.setAttribute("loading", "lazy");
      }
      if (!img.hasAttribute("decoding")) {
        img.setAttribute("decoding", "async");
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enhanceImages);
  } else {
    enhanceImages();
  }
})();
