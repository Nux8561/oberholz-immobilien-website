function formatThousands(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function updateComparisonTable() {
    const slider = document.getElementById('slider-handwerkerangebot');
    if (!slider) {
        /*console.warn('⚠️ Element #slider-handwerkerangebot nicht gefunden');*/
        return;
    }
    let handwerkerangebot = parseInt(document.getElementById('slider-handwerkerangebot').value);
    let wohneinheiten = parseInt(document.getElementById('slider-wohneinheiten').value);

    /* Förderfähige Kosten je Objekt (Stand Juli 2026):
       1. Wohneinheit 30.000 €, 2. bis 6. Wohneinheit je 15.000 €, ab der 7. Wohneinheit je 8.000 €.
       Mit iSFP erhöht sich der Deckel um +30.000 (1. WE), je +15.000 (2. bis 6.) und je +7.000 € (ab der 7. WE),
       also 60.000/30.000/15.000 € (keine reine Verdopplung); bis zum einfachen (WE-gestaffelten) Deckel gibt es 15 %,
       auf den Anteil darüber (bis zum erhöhten iSFP-Deckel) 20 % (15 % + 5 % iSFP-Bonus).
       WPB-Bonus (Worst Performing Building): +5 Prozentpunkte, nur mit vorliegendem iSFP
       (Endenergiebedarf ab 300 kWh/(m²a), Maßnahme muss im iSFP aufgeführt sein,
       max. 3 Förderanträge). Ohne iSFP gibt es keinen WPB-Bonus, dort bleibt es bei 15 %. */
    let maxFoerdersummeOhneIsfp = 30000;
    if (wohneinheiten > 1) {
        maxFoerdersummeOhneIsfp += Math.min(wohneinheiten - 1, 5) * 15000;
    }
    if (wohneinheiten > 6) {
        maxFoerdersummeOhneIsfp += (wohneinheiten - 6) * 8000;
    }

    const wpbCheckbox = document.getElementById('wpb-checkbox');
    let wpbBonus = (wpbCheckbox && wpbCheckbox.checked) ? 0.05 : 0;
    let satzOhne = 0.15;
    let satzBasisMit = 0.15 + wpbBonus;
    let satzErweitertMit = 0.20 + wpbBonus;
    let maxFoerdersummeMitIsfp = 60000;
    if (wohneinheiten > 1) {
        maxFoerdersummeMitIsfp += Math.min(wohneinheiten - 1, 5) * 30000;
    }
    if (wohneinheiten > 6) {
        maxFoerdersummeMitIsfp += (wohneinheiten - 6) * 15000;
    }

    let anzurechnenderBetragOhneIsfp = maxFoerdersummeOhneIsfp;
    let anzurechnenderBetragMitIsfp = maxFoerdersummeMitIsfp;

    /* Update Wohneinheiten Info-Strings in Texten */
    let we_string = ' Wohneinheiten';
    if (wohneinheiten === 1 || wohneinheiten < 1) {
        we_string = ' Wohneinheit';
    }

    /* Deckeln */
    let xyOhne = Math.min(handwerkerangebot, anzurechnenderBetragOhneIsfp);
    let xyMit = Math.min(handwerkerangebot, anzurechnenderBetragMitIsfp);

    /* Ohne iSFP: immer 15 %, der WPB-Bonus setzt einen iSFP voraus */
    let ohneIsfpFoerderung = Math.round(xyOhne * satzOhne);

    /* Mit iSFP: bis zum regulären (WE-gestaffelten) Ohne-iSFP-Deckel gilt der Basissatz, alles
       darüber (bis zum verdoppelten Deckel) der erweiterte Satz (inkl. iSFP-Bonus). Der Bonus
       greift laut Richtlinie (Ziffer 8.4.2) nur für Ausgaben oberhalb der Höchstgrenze OHNE iSFP,
       die Grenze skaliert also mit der Anzahl der Wohneinheiten (bei 2 WE z. B. 45.000 €, nicht
       pauschal 30.000 €). */
    const grundanteilDeckel = maxFoerdersummeOhneIsfp;
    let trancheBasis = Math.min(xyMit, grundanteilDeckel);
    let trancheBonus = Math.max(0, xyMit - trancheBasis);
    let mitIsfpFoerderung = Math.round(trancheBasis * satzBasisMit + trancheBonus * satzErweitertMit);

    /* Update Angebotssumme Info-Strings in Texten */
    document.getElementById('handwerker-angebot-summe').innerHTML = formatThousands(handwerkerangebot);
    document.getElementById('wohneinheiten-anzahl').innerHTML = wohneinheiten + we_string;

    /* Update Summen */
    document.getElementById('ohne-isfp-foerderfaehiger-betrag').innerHTML = formatThousands(xyOhne);
    document.getElementById('mit-isfp-tranche-basis').innerHTML = formatThousands(trancheBasis);
    document.getElementById('mit-isfp-tranche-bonus').innerHTML = formatThousands(trancheBonus);
    document.getElementById('mit-isfp-tranche-bonus-wrap').style.display = trancheBonus > 0 ? '' : 'none';

    /* Fördersätze in den Labels aktualisieren (WPB-Bonus wirkt nur auf der iSFP-Seite) */
    const satzOhneProzent = Math.round(satzOhne * 100) + '%';
    const satzBasisMitProzent = Math.round(satzBasisMit * 100) + '%';
    const satzErweitertMitProzent = Math.round(satzErweitertMit * 100) + '%';
    const ohneSatzEl = document.getElementById('ohne-isfp-satz');
    if (ohneSatzEl) ohneSatzEl.innerHTML = satzOhneProzent;
    const basisSatzEl = document.getElementById('mit-isfp-satz-basis');
    if (basisSatzEl) basisSatzEl.innerHTML = satzBasisMitProzent;
    const erweitertSatzEl = document.getElementById('mit-isfp-satz-bonus');
    if (erweitertSatzEl) erweitertSatzEl.innerHTML = satzErweitertMitProzent;
    const bonusHinweisEl = document.getElementById('mit-isfp-bonus-hinweis');
    if (bonusHinweisEl) bonusHinweisEl.innerHTML = wpbBonus > 0 ? 'inkl. 5% iSFP-Bonus und 5% WPB-Bonus' : 'inkl. 5% iSFP-Bonus';

    document.getElementById('ohne-isfp-max-foerderung').innerHTML = formatThousands(anzurechnenderBetragOhneIsfp);
    document.getElementById('mit-isfp-max-foerderung').innerHTML = formatThousands(anzurechnenderBetragMitIsfp);

    document.getElementById('ohne-isfp-foerderung').innerHTML = formatThousands(ohneIsfpFoerderung);
    document.getElementById('mit-isfp-foerderung').innerHTML = formatThousands(mitIsfpFoerderung);

    let differenzFoerderung = mitIsfpFoerderung - ohneIsfpFoerderung;
    document.getElementById('mit-isfp-foerderung-surplus').innerHTML = formatThousands(differenzFoerderung);
}

 /* EoF updateComparisonTable() */


document.addEventListener('DOMContentLoaded', () => {
    updateComparisonTable();

    /* WPB-Checkbox (Worst Performing Building) neu berechnen lassen */
    const wpbCheckbox = document.getElementById('wpb-checkbox');
    if (wpbCheckbox) {
        wpbCheckbox.addEventListener('change', updateComparisonTable);
    }

    // Event-Listener für Textfeld EINMAL registrieren (außerhalb der Schleife)
    const amountInput = document.getElementById('slider-handwerkerangebot');
    const handwerkerangebotRange = document.getElementById('slider-handwerkerangebot');

    if (amountInput && handwerkerangebotRange) {
        amountInput.addEventListener('input', e => {
            if (amountInput.value.length >= 4) {
                handwerkerangebotRange.value = e.target.value;
                updateComparisonTable();
            }
        });
    }

    // Alle Range-Inputs durchgehen
    document.querySelectorAll('input[type=range]').forEach(range => {
        let unit = range.getAttribute('unit') || '';
        let type = range.dataset.type;

        // Bubble erzeugen
        let valueBubble = document.createElement('output');
        valueBubble.className = 'rangeslider__value-bubble';
        range.parentNode.appendChild(valueBubble);

        function updateValueBubble(value) {
            let min = parseInt(range.min) || 0;
            let max = parseInt(range.max) || 100;
            let newVal = ((value - min) * 100) / (max - min);

            let u = unit;
            if (type === "wohneinheiten") {
                u = (parseInt(value) === 1) ? ' Wohneinheit' : ' Wohneinheiten';
            }

            valueBubble.innerHTML = formatThousands(value) + " " + u;
            /* 40 = Thumb-Breite aus rangeslider.css; haelt die Bubble mittig ueber dem Knob */
            const thumbWidth = 40;
            valueBubble.style.left = `calc(${newVal}% + (${thumbWidth / 2 - newVal * thumbWidth / 100}px))`;
        }

        updateValueBubble(range.value);

        range.addEventListener('input', e => {
            updateValueBubble(e.target.value);
            updateComparisonTable();
        });
    });

    // Show Modal via URL
    const urlParams = new URLSearchParams(window.location.search);
    const modalToShow = urlParams.get('modal');
    const modalId = urlParams.get('modal_id');

    if (modalToShow === 'show' && modalId) {
        const modalEl = document.getElementById(modalId);

        if (modalEl) {
            // Bootstrap 5 Modal-API aufrufen
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        }

        // Footer-CTA verstecken
        const whatsappCtaFooter = document.getElementById('whatsapp-cta-footer');
        if (whatsappCtaFooter) {
            whatsappCtaFooter.classList.remove('d-block');
        }
    }


    var map;

    function initialize() {
        var mapOptions = {
            zoom: 13,
            center: new google.maps.LatLng(50.97797382271958, -114.107718560791)
            // styles: style_array_here
        };
        map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    }

    var google_map_canvas = document.getElementById('map-canvas');

    if (google_map_canvas) {
        google.maps.event.addDomListener(window, 'load', initialize);
    }


    // ScrollTo
    document.querySelectorAll('.scrollto').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const targetSelector = link.getAttribute('href');
            const target = document.querySelector(targetSelector);

            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });


    /* LiveSearch */
    let anzahl = 0;
    const anzahlLive = document.querySelector('.anzahl-live');
    const themaLive = document.querySelector('.thema-live');
    const faqItems = document.querySelectorAll('.faq .single-pub');
    const liveSearchBox = document.querySelector('.live-search-box');

// Ursprungs-Anzahl ermitteln
    anzahl = faqItems.length;
    if (anzahlLive) {
        anzahlLive.textContent = anzahl;
    }

// jedem Item das data-search-term geben
    faqItems.forEach(item => {
        item.setAttribute('data-search-term', item.textContent.toLowerCase());
    });

// Eventlistener für Suche
    if (liveSearchBox) {
        liveSearchBox.addEventListener('keyup', function () {
            const searchTerm = this.value.toLowerCase();
            const searchTermOriginal = this.value;

            faqItems.forEach(item => {
                const text = item.getAttribute('data-search-term') || '';
                if (searchTerm.length) {
                    if (text.includes(searchTerm)) {
                        item.style.display = '';
                    } else {
                        item.style.display = 'none';
                    }
                } else {
                    item.style.display = '';
                }
            });

            // Sichtbare Elemente zählen
            const visibleCount = document.querySelectorAll('.faq .single-pub:not([style*="display: none"])').length;
            if (anzahlLive) anzahlLive.textContent = visibleCount;

            // Thema-Text
            if (themaLive) {
                if (searchTerm) {
                    themaLive.innerHTML = ' zum Thema <strong><em>' + searchTermOriginal + '</em></strong>';
                } else {
                    themaLive.innerHTML = '';
                }
            }
        });
    }


    // In FAQs Klick auf gesamtes Panel ermöglichen, nicht nur auf Link
    document.querySelectorAll('.faq .card-header').forEach(function (header) {
        header.addEventListener('click', function (e) {
            const trigger = header.querySelector('a');
            if (!trigger) return;

            const targetSelector = trigger.getAttribute('href');
            if (!targetSelector || !targetSelector.startsWith('#')) return;

            const collapseEl = document.querySelector(targetSelector);
            if (!collapseEl) return;

            const collapseBtn = header.querySelector('.collapse-btn');

            const bsCollapse = bootstrap.Collapse.getInstance(collapseEl) || new bootstrap.Collapse(collapseEl, {
                toggle: false
            });

            // Nur Events anlegen, nicht bei jedem Klick neu
            if (!collapseEl.dataset.listenerAttached) {
                collapseEl.addEventListener('show.bs.collapse', function () {
                    header.classList.remove('collapsed');
                    if (collapseBtn) collapseBtn.classList.remove('collapsed');
                });

                collapseEl.addEventListener('hide.bs.collapse', function () {
                    header.classList.add('collapsed');
                    if (collapseBtn) collapseBtn.classList.add('collapsed');
                });

                collapseEl.dataset.listenerAttached = 'true';
            }

            bsCollapse.toggle();
            e.preventDefault()
        });
    });


    // Tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


    // Clearable text inputs
    document.querySelectorAll('.clearable').forEach(clearable => {
        const inp = clearable.querySelector('input[type="text"]');
        const cle = clearable.querySelector('.clearable__clear');

        if (!inp || !cle) return;

        // Show/Hide Clear-Button je nach Input-Wert
        inp.addEventListener('input', function () {
            if (this.value) {
                cle.style.display = '';
            } else {
                cle.style.display = 'none';
            }
        });

        // Clear-Button Logik
        ['click', 'touchstart'].forEach(evt => {
            cle.addEventListener(evt, function (e) {
                e.preventDefault();
                inp.value = '';
                inp.dispatchEvent(new Event('input')); // Input-Event manuell triggern
                inp.focus();

                // Livesearch zurücksetzen
                document.querySelectorAll('.faq .single-pub').forEach(pub => {
                    pub.style.display = '';
                });

                const anzahlLive = document.querySelector('.anzahl-live');
                if (anzahlLive) {
                    anzahlLive.textContent = anzahl; // globale Variable aus Livesearch
                }

                const themaLive = document.querySelector('.thema-live');
                if (themaLive) {
                    themaLive.innerHTML = '';
                }

                // Falls du auch .download-cat-title einblenden willst:
                // document.querySelectorAll('.download-cat-title').forEach(el => {
                //     el.style.display = '';
                // });
            });
        });
    });


    // Submit-Button in Formularen auf "Bitte warten" setzen
    document.querySelectorAll('.contact form').forEach(form => {
        form.addEventListener('submit', function () {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Wird gesendet - Bitte warten...';
                submitButton.disabled = true;
                submitButton.classList.add('disabled');
            }
        });
    });

    // Modal & YouTube-Videos: Iframe src beim Öffnen setzen, beim Schließen entfernen
    document.addEventListener('shown.bs.modal', function (event) {
        const modal = event.target;
        const iframes = modal.querySelectorAll('iframe[id^="video-"]');
        iframes.forEach(iframe => {
            const src = iframe.dataset.src;
            if (src) {
                iframe.setAttribute('src', src);
            }
        });
    });

    document.addEventListener('hide.bs.modal', function (event) {
        const modal = event.target;
        const iframes = modal.querySelectorAll('iframe[id^="video-"]');
        iframes.forEach(iframe => {
            iframe.removeAttribute('src');
        });
    });


    /* Ratings-Modal oder Offcanvas öffnen, bei Klick auf Ratings-Snippet oder Facepile-Snippet*/
    function openRatingsModalOrOffcanvas() {
        const modalEl = document.getElementById('typeform-rating-modal');
        const offcanvasEl = document.getElementById('typeform-rating-offcanvas');

        if (modalEl) {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        } else if (offcanvasEl) {
            const offcanvas = new bootstrap.Offcanvas(offcanvasEl);
            offcanvas.show();
            loadRatings()
        }
    }

    // Ratings async laden
    async function loadRatings() {
        try {
            const response = await fetch('/index.php?rex-api-call=typeform&namespace=get_ratings');

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Ratings-List Container finden
            const ratingsListContainer = document.querySelector('.ratings-list');
            if (!ratingsListContainer) {
                console.warn('Element .ratings-list nicht gefunden');
                return;
            }

            // HTML für alle Ratings generieren
            let ratingsHTML = '';

            data.all_ratings.forEach(rating => {
                const starsHTML = getStarsMarkup(rating.rating);
                const currentDate = new Date(rating.submitted_at).toLocaleDateString('de-DE');

                ratingsHTML += `
                <div class="col-12 col-sm-6">
                    <div class="card h-100 shadow-sm border-0 bg-light">
                        <div class="card-body small">
                            <!-- Datum in eigener Zeile -->
                            <div class="small text-muted mb-0">${currentDate}</div>
                            
                            <!-- Sterne + Bewertung -->
                            <div class="mb-2">
                                <span class="text-warning">
                                    ${starsHTML}
                                </span>
                                <strong class="ms-1">${rating.rating}</strong><span class="text-muted">/5</span>
                            </div>
                            
                            <!-- Bewertungstitel -->
                            <div class="mb-1 fw-semibold text-dark">${rating.voter_name}</div>
                            
                            <!-- Bewertungstext -->
                            <div class="text-muted">${rating.text}</div>
                        </div>
                    </div>
                </div>
            `;
            });

            // HTML in Container einfügen
            ratingsListContainer.innerHTML = ratingsHTML;

        } catch (error) {
            console.error('Fehler beim Laden der Ratings:', error);
        }
    }

    function getStarsMarkup(rating) {
        let stars = '';
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;

        // Volle Sterne
        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="fa fa-star"></i>';
        }

        // Halber Stern
        if (hasHalfStar) {
            stars += '<i class="fa fa-star-half-stroke"></i>';
        }

        // Leere Sterne bis 5
        const emptyStars = 5 - Math.ceil(rating);
        for (let i = 0; i < emptyStars; i++) {
            stars += '<i class="fa fa-star-o"></i>';
        }

        return stars;
    }

    /*Ratings-Snippet und Facepile-Snippet: Öffnen Offcanvas-Bewertungen */
    ['.ratings-snippet', '.facepile-snippet'].forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            new bootstrap.Tooltip(el);
            el.addEventListener('click', openRatingsModalOrOffcanvas);
        });
    });

    // Hotspots
    const hotspots = document.querySelectorAll('.hotspot');

    hotspots.forEach(hotspot => {
        hotspot.addEventListener('click', function (e) {
            e.stopPropagation(); // Klick nicht nach außen weiterreichen

            // Alle anderen schließen
            document.querySelectorAll('.popover-box').forEach(box => box.style.display = 'none');

            // Dieses öffnen
            const box = this.querySelector('.popover-box');
            if (box) {
                box.style.display = 'block';
            }
        });
    });

    // Klick außerhalb → alle schließen
    document.addEventListener('click', function () {
        document.querySelectorAll('.popover-box').forEach(box => box.style.display = 'none');
    });

    /* Video-Swiper */
    var video_swiper = new Swiper(".video-slider-swiper", {
        direction: 'horizontal',
        spaceBetween: 10,
        freeMode: true,
        loop: true,
        autoplay: {
            delay: 2500,
            disableOnInteraction: false
        },
        grabCursor: true,
        breakpoints: {
            320: {
                slidesPerView: 1.5
            },
            640: {
                slidesPerView: 2.5
            },
            768: {
                slidesPerView: 2.5
            },
            1024: {
                slidesPerView: 2.5
            },
        },
    })
});

/* Oberholz: stabiles Desktop-Flyout – CSS-Fix global nachladen */
(function () {
    if (document.querySelector('link[href*="oberholz-nav-fix.css"]')) return;
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "/theme/oberholz-nav-fix.css";
    document.head.appendChild(link);
})();

