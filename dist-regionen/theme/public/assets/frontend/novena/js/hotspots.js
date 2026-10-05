(function () {
    'use strict';

    const isMobile = () => window.innerWidth < 768;

    // ── Desktop Popover-Logik ─────────────────────────────────────────
    function initDesktopPopovers() {
        const buttons = document.querySelectorAll('.hotspot');

        buttons.forEach(btn => {
            btn.addEventListener('click', function (e) {
                if (isMobile()) return;
                // In "Alle Boxen geöffnet"-Modus sind die Boxen dauerhaft offen
                if (btn.closest('[data-hs-expand-all]')) return;
                e.stopPropagation();

                const uid     = btn.dataset.hotspotId;
                const popover = document.getElementById('popover-' + uid);
                if (!popover) return;

                const isOpen = btn.getAttribute('aria-expanded') === 'true';

                closeAllPopovers();

                if (!isOpen) {
                    openPopover(btn, popover);
                }
            });
        });

        document.addEventListener('click', closeAllPopovers);
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape') closeAllPopovers();
        });

        // "Alle Boxen geöffnet": Popovers in expand-all-Wraps initial öffnen.
        // Erst nach 'load', damit das Bild (und damit die Wrap-Höhe) steht.
        if (document.querySelector('[data-hs-expand-all]')) {
            if (document.readyState === 'complete') {
                openAllExpanded();
            } else {
                window.addEventListener('load', openAllExpanded);
            }
            // Bei Größenänderung die dauerhaft offenen Boxen neu positionieren
            let resizeTimer;
            window.addEventListener('resize', function () {
                clearTimeout(resizeTimer);
                resizeTimer = setTimeout(openAllExpanded, 200);
            });
        }
    }

    function openAllExpanded() {
        if (isMobile()) return;
        document.querySelectorAll('.hotspot-image-wrap[data-hs-expand-all]').forEach(function (wrap) {
            const img = wrap.querySelector('.hotspot-main-img');
            const openWrap = function () {
                wrap.querySelectorAll('.hotspot').forEach(function (btn) {
                    const popover = document.getElementById('popover-' + btn.dataset.hotspotId);
                    if (popover) openPopover(btn, popover);
                });
            };
            // Erst öffnen, wenn das Bild (und damit die Wrap-Höhe) wirklich geladen ist,
            // sonst kollabieren die %-Positionen nach oben (loading="lazy").
            if (img && !img.complete) {
                img.addEventListener('load', openWrap, { once: true });
                img.addEventListener('error', openWrap, { once: true });
            } else {
                openWrap();
            }
        });
    }

    function openPopover(btn, popover) {
        const wrap = btn.closest('.hotspot-image-wrap');

        // Position des Buttons relativ zum image-wrap über offset (parallax-frei),
        // damit der Parallax-Versatz (CSS translate) nicht doppelt einfließt.
        // Durch transform: translate(-50%,-50%) entspricht offsetTop/Left der visuellen Mitte.
        const halfBtn = btn.offsetWidth / 2;
        const btnTop  = btn.offsetTop;
        const btnLeft = btn.offsetLeft;

        // Reset
        popover.classList.remove('popover--left');
        popover.style.right = 'auto';
        popover.style.top  = btnTop + 'px';
        popover.style.left = (btnLeft + halfBtn + 16) + 'px';
        popover.style.transform = 'translateY(-50%) scale(0.94)';

        // Sichtbar machen für Breitenberechnung
        popover.hidden = false;
        popover.classList.add('is-visible');
        btn.setAttribute('aria-expanded', 'true');

        // Prüfen ob Popover rechts über den Viewport ragt → nach links spiegeln
        requestAnimationFrame(() => {
            const popRect = popover.getBoundingClientRect();
            if (popRect.right > window.innerWidth - 16) {
                popover.classList.add('popover--left');
                popover.style.left = 'auto';
                popover.style.right = (wrap.clientWidth - btnLeft + halfBtn + 16) + 'px';
                popover.style.transformOrigin = 'right center';
            }
            popover.style.transform = 'translateY(-50%) scale(1)';
        });
    }

    function closeAllPopovers() {
        document.querySelectorAll('.hotspot').forEach(btn => {
            // Dauerhaft geöffnete Boxen (expand-all) nicht schließen
            if (btn.closest('[data-hs-expand-all]')) return;
            const uid     = btn.dataset.hotspotId;
            const popover = document.getElementById('popover-' + uid);
            if (popover) {
                popover.classList.remove('is-visible', 'popover--left');
                popover.style.transform = '';
                btn.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // ── Mobile Sheet-Logik ────────────────────────────────────────────
    function initMobileSheets() {
        const overlay = document.getElementById('hotspot-sheet-overlay');
        const buttons = document.querySelectorAll('.hotspot');

        buttons.forEach(btn => {
            const sheetId = btn.getAttribute('aria-controls');
            const sheet   = document.getElementById(sheetId);
            if (!sheet) return;

            btn.addEventListener('click', function (e) {
                if (!isMobile()) return;
                e.stopPropagation();
                openSheet(sheet, overlay);
            });

            const closeBtn = sheet.querySelector('.hotspot-sheet__close');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => closeSheet(sheet, overlay));
            }

            const backdrop = sheet.querySelector('.hotspot-sheet__backdrop');
            if (backdrop) {
                backdrop.addEventListener('click', () => closeSheet(sheet, overlay));
            }
        });

        if (overlay) {
            overlay.addEventListener('click', () => {
                document.querySelectorAll('.hotspot-sheet.is-open').forEach(s => {
                    closeSheet(s, overlay);
                });
            });
        }

        document.addEventListener('keydown', e => {
            if (e.key === 'Escape') {
                document.querySelectorAll('.hotspot-sheet.is-open').forEach(s => {
                    closeSheet(s, overlay);
                });
            }
        });
    }

    function openSheet(sheet, overlay) {
        document.querySelectorAll('.hotspot-sheet.is-open').forEach(s => {
            if (s !== sheet) s.classList.remove('is-open');
        });

        sheet.classList.add('is-open');
        if (overlay) overlay.classList.add('is-active');
        document.body.style.overflow = 'hidden';

        const focusTarget = sheet.querySelector('.hotspot-sheet__close');
        if (focusTarget) setTimeout(() => focusTarget.focus(), 50);
    }

    function closeSheet(sheet, overlay) {
        sheet.classList.remove('is-open');
        if (overlay) overlay.classList.remove('is-active');
        document.body.style.overflow = '';
    }

    // ── Init ──────────────────────────────────────────────────────────
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ── Chevron: einzelne Box im "Alle offen"-Modus auf-/zuklappen ─────
    function initChevrons() {
        document.addEventListener('click', function (e) {
            const pop = e.target.closest('.hotspot-popover');
            if (!pop) return;
            // Nur im "Alle Boxen offen"-Modus ist die gesamte Box klickbar
            const wrap = pop.closest('.hotspot-image-wrap[data-hs-expand-all]');
            if (!wrap) return;
            // Klicks auf echte Links sollen navigieren, nicht toggeln
            if (e.target.closest('a')) return;
            e.preventDefault();
            e.stopPropagation();
            const willExpand = !pop.classList.contains('is-expanded');
            // Nur eine Box gleichzeitig geöffnet: andere im selben Bild einklappen
            if (willExpand) {
                wrap.querySelectorAll('.hotspot-popover.is-expanded').forEach(function (other) {
                    if (other === pop) return;
                    other.classList.remove('is-expanded');
                    const oc = other.querySelector('.hs-card__chevron');
                    if (oc) {
                        oc.setAttribute('aria-expanded', 'false');
                        oc.setAttribute('aria-label', 'Mehr anzeigen');
                    }
                });
            }
            pop.classList.toggle('is-expanded', willExpand);
            const chev = pop.querySelector('.hs-card__chevron');
            if (chev) {
                chev.setAttribute('aria-expanded', willExpand ? 'true' : 'false');
                chev.setAttribute('aria-label', willExpand ? 'Weniger anzeigen' : 'Mehr anzeigen');
            }
        });
    }

    function init() {
        initDesktopPopovers();
        initMobileSheets();
        initChevrons();
    }
})();