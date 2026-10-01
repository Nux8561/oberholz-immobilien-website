/**
 * Compatibility shim only – does NOT replace the original widget UI.
 * Original panel comes from /theme/contact-widget.html (#cw-backdrop / #cw-panel).
 */
(function () {
  function bindHintClose() {
    var hint = document.getElementById("cw-trigger-hint");
    var hintClose = document.getElementById("cw-trigger-hint-close");
    var trigger = document.getElementById("cw-trigger");
    if (!hint || !hintClose) return;

    function dismiss(e) {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      hint.classList.remove("show");
      if (trigger) trigger.classList.remove("cw-trigger-pulse");
      var expires = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toUTCString();
      document.cookie = "cw_hint_closed=1; path=/; expires=" + expires + "; SameSite=Lax";
    }

    hintClose.addEventListener("click", dismiss);
    hintClose.addEventListener("touchend", dismiss, { passive: false });

    if (document.cookie.indexOf("cw_hint_closed=1") !== -1) {
      hint.classList.remove("show");
      if (trigger) trigger.classList.remove("cw-trigger-pulse");
    }
  }

  function killStubPanels() {
    document.querySelectorAll("#cw-widget-wrapper").forEach(function (node) {
      if (node.textContent && node.textContent.indexOf("Lokale Ansicht") !== -1) {
        node.remove();
      }
    });
    var fake = document.getElementById("cw-local-overlay");
    if (fake) fake.remove();
  }

  function install() {
    killStubPanels();
    bindHintClose();
    var observer = new MutationObserver(killStubPanels);
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", install);
  } else {
    install();
  }
})();
