/*!
 *
 * Copyright (c) 2026 Daniel Springer | Medienfeuer.de
 *
 */

/**
 * ------------------------------------------------------------------------
 * ContainerCollapse
 * ------------------------------------------------------------------------
 * Lightweight vanilla JS collapse component based on data attributes.
 *
 * Automatically initializes all elements with:
 *     data-container-collapse
 *
 * ------------------------------------------------------------------------
 * BASIC USAGE
 * ------------------------------------------------------------------------
 *
 * <div
 *   data-container-collapse
 *   data-container-collapse-max-height="200"
 *   data-container-collapse-more="Mehr anzeigen"
 *   data-container-collapse-less="Weniger anzeigen"
 *   data-container-collapse-btn-class="btn btn-primary"
 *   data-container-collapse-btn-expanded-class="is-open"
 *   data-container-collapse-margin="30">
 *   ...
 * </div>
 *
 * Just include the script file:
 *
 * <script src="/js/container-collapse.js"></script>
 *
 * Initialization runs automatically on DOMContentLoaded.
 *
 * ------------------------------------------------------------------------
 * DATA ATTRIBUTES
 * ------------------------------------------------------------------------
 *
 * data-container-collapse
 *     Activates collapse behavior on the element.
 *
 * data-container-collapse-max-height="400"
 *     Maximum collapsed height in pixels.
 *     Default: 400
 *
 * data-container-collapse-more="Mehr anzeigen"
 *     Label shown in collapsed state.
 *     Default: "mehr"
 *
 * data-container-collapse-less="Weniger anzeigen"
 *     Label shown in expanded state.
 *     Default: "weniger"
 *
 * data-container-collapse-btn-class="btn btn-primary"
 *     Additional CSS classes applied to the generated button.
 *
 * data-container-collapse-btn-expanded-class="is-open"
 *     Class added to the button when expanded.
 *
 * data-container-collapse-margin="30"
 *     Extra margin below the button in pixels.
 *     Default: 30
 *
 * ------------------------------------------------------------------------
 * CSS REQUIREMENTS
 * ------------------------------------------------------------------------
 *
 * You must provide styles for:
 *
 * - .container-collapse-toggle
 * - .is-collapsed
 *
 * Optional:
 * - CSS mask for fade-out effect
 * - Icon rotation via .is-open
 *
 * Example fade mask:
 *
 * [data-container-collapse].is-collapsed {
 *   -webkit-mask-image: linear-gradient(
 *     to bottom,
 *     black 70%,
 *     transparent 100%
 *   );
 *   mask-image: linear-gradient(
 *     to bottom,
 *     black 70%,
 *     transparent 100%
 *   );
 * }
 *
 * ------------------------------------------------------------------------
 * JAVASCRIPT API
 * ------------------------------------------------------------------------
 *
 * Manual initialization:
 *
 * ContainerCollapse.init();
 *
 * Initialize inside specific element:
 *
 * ContainerCollapse.init(document.querySelector('#ajax-content'));
 *
 * Prevents double initialization automatically.
 *
 * ------------------------------------------------------------------------
 * FEATURES
 * ------------------------------------------------------------------------
 *
 * ✔ No dependencies
 * ✔ Data-attribute driven
 * ✔ Auto-initializing
 * ✔ Multiple instances supported
 * ✔ Accessible (aria-expanded)
 * ✔ Safe for dynamic content
 *
 * ------------------------------------------------------------------------
 * Author: Your Name
 * Version: 1.0.0
 * ------------------------------------------------------------------------
 */

(function () {

    const DEFAULTS = {
        maxHeight: 400,
        moreLabel: 'mehr',
        lessLabel: 'weniger',
        margin: 30
    };

    const ICON = `
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
             viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2.5"
             stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
    `;

    function initContainerCollapse(root = document) {

        root.querySelectorAll('[data-container-collapse]').forEach(el => {

            if (el.dataset.ccInitialized) return; /* doppelte Init verhindern */
            el.dataset.ccInitialized = "true";

            const maxHeight = parseInt(el.dataset.containerCollapseMaxHeight) || DEFAULTS.maxHeight;
            const moreLabel = el.dataset.containerCollapseMore || DEFAULTS.moreLabel;
            const lessLabel = el.dataset.containerCollapseLess || DEFAULTS.lessLabel;
            const btnClass = el.dataset.containerCollapseBtnClass || '';
            const btnExpandedClass = el.dataset.containerCollapseBtnExpandedClass || '';
            const extraMargin = parseInt(el.dataset.containerCollapseMargin) || DEFAULTS.margin;

            const fullHeight = el.scrollHeight;
            if (fullHeight <= maxHeight) return;

            el.classList.add('is-collapsed');
            el.style.maxHeight = maxHeight + 'px';

            const button = document.createElement('button');
            button.type = 'button';
            button.className = (btnClass ? btnClass + ' ' : '') + 'container-collapse-toggle';
            button.setAttribute('aria-expanded', 'false');
            button.style.setProperty('--container-collapse-btn-margin', extraMargin + 'px');

            button.innerHTML = `
                <span class="container-collapse-label">${moreLabel}</span>
                <span class="container-collapse-icon">${ICON}</span>
            `;

            el.insertAdjacentElement('afterend', button);

            button.addEventListener('click', () => {

                const expanded = button.getAttribute('aria-expanded') === 'true';

                if (!expanded) {

                    el.style.maxHeight = el.scrollHeight + 'px';
                    el.classList.remove('is-collapsed');

                    button.querySelector('.container-collapse-label').textContent = lessLabel;

                    button.setAttribute('aria-expanded', 'true');

                    if (btnExpandedClass) button.classList.add(btnExpandedClass);

                } else {

                    el.style.maxHeight = maxHeight + 'px';
                    el.classList.add('is-collapsed');

                    button.querySelector('.container-collapse-label').textContent = moreLabel;

                    button.setAttribute('aria-expanded', 'false');

                    if (btnExpandedClass) button.classList.remove(btnExpandedClass);
                }
            });
        });
    }

    /* Auto Init */
    document.addEventListener('DOMContentLoaded', () => {
        initContainerCollapse();
    });

    /* Globale API */
    window.ContainerCollapse = {
        init: initContainerCollapse
    };

})();