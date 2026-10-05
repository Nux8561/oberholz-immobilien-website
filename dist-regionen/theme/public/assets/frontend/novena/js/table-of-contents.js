/*!
 *
 * Copyright (c) 2025 Daniel Springer | Medienfeuer.de
 *
 */
/**
 * Erstellt ein dynamisches Inhaltsverzeichnis (Table of Contents) aus Überschriften
 * innerhalb eines Content-Containers und rendert es in ein Ziel-Element.
 *
 * @param {string|Element} content
 *        CSS-Selector oder DOM-Element des Containers, in dem nach Überschriften gesucht wird.
 *
 * @param {string|NodeList|Element} target
 *        CSS-Selector, NodeList oder DOM-Element(e), in die das Inhaltsverzeichnis eingefügt wird.
 *
 * @param {Object} [options]
 *        Optionale Konfiguration zur Anpassung des Inhaltsverzeichnisses.
 *
 * @param {string} [options.levels='h2, h3, h4, h5, h6']
 *        Kommagetrennte Liste der zu berücksichtigenden Überschriften.
 *
 * @param {string} [options.preHeading='']
 *        Optionaler Text oberhalb des Inhaltsverzeichnisses.
 *
 * @param {string} [options.preHeadingClass='text-muted small d-block']
 *        CSS-Klassen für die Pre-Heading-Ausgabe.
 *
 * @param {string} [options.heading='']
 *        Überschrift für das Inhaltsverzeichnis.
 *
 * @param {string} [options.headingClass='h2']
 *        CSS-Klassen für die Inhaltsverzeichnis-Überschrift.
 *
 * @param {string} [options.listType='ul']
 *        Listentyp für das Inhaltsverzeichnis (`ul` oder `ol`).
 *
 * @param {string} [options.listId='']
 *        ID-Attribut der generierten Liste.
 *
 * @param {string} [options.listClass='']
 *        CSS-Klassen für die Liste.
 *
 * @param {string} [options.itemClass='']
 *        CSS-Klassen für einzelne Listeneinträge.
 *
 * @param {string} [options.linkClass='']
 *        CSS-Klassen für die TOC-Links.
 *
 * @param {string} [options.innerLinkClass='']
 *        CSS-Klassen für innere Link-Elemente.
 *
 * @param {string} [options.activeClass='active']
 *        CSS-Klasse für den aktiven Eintrag beim Scrollen.
 *
 * @param {boolean} [options.richSnippet=false]
 *        Aktiviert strukturierte Daten (z. B. für SEO Rich Snippets).
 *
 * @param {number} [options.scrollToOffset=0]
 *        Offset in Pixeln beim Scrollen zu einer Überschrift.
 *
 * @returns {void}
 */

var tableOfContents = function (content, target, options) {
    var contentWrap = document.querySelector(content);
    var toc = document.querySelector(target);
    var tocTargets = typeof target === 'string'
        ? document.querySelectorAll(target)
        : target;

    if (!contentWrap || !tocTargets || !tocTargets.length) return;

    var defaults = {
        levels: 'h2, h3, h4, h5, h6',
        preHeading: '',
        preHeadingClass: 'text-muted small d-block',
        heading: '',
        headingClass: 'h2',
        listType: 'ul',
        listId: '',
        listClass: '',
        itemClass: '',
        linkClass: '',
        innerLinkClass: '',
        activeClass: 'active',
        richSnippet: false,
        scrollToOffset: 0
    };

    var settings = Object.assign({}, defaults, options || {});
    var headings;
    var tocLinks = [];
    var tocListHTML = '';
    var headingElements = [];

    var createID = function (heading, i) {
        if (heading.id.length) return;
        heading.id = 'toc_' + i + '_' +  heading.textContent
            .replace(/[^A-Za-z0-9\s]/g, '')
            .replace(/\s+/g, '-')
            .toLowerCase();
    };

    var getListTag = function () {
        var tag = settings.listType || 'ul';
        var classAttr = settings.listClass ? ' class="' + settings.listClass + '"' : '';
        var idAttr = settings.listId ? ' id="' + settings.listId + '"' : '';
        return '<' + tag + classAttr + idAttr + '>';
    };

    var getListCloseTag = function () {
        var tag = settings.listType || 'ul';
        return '</' + tag + '>';
    };

    var getIndent = function (count) {
        var html = '';
        for (var i = 0; i < count; i++) {
            html += getListTag();
        }
        return html;
    };

    var getOutdent = function (count) {
        var html = '';
        for (var i = 0; i < count; i++) {
            html += getListCloseTag() + '</li>';
        }
        return html;
    };

    var getStartingHTML = function (diff, index) {
        if (diff > 0) {
            return getIndent(diff);
        }
        if (diff < 0) {
            return getOutdent(Math.abs(diff));
        }
        if (index && !diff) {
            return '</li>';
        }
        return '';
    };

    /* Rich Snippet Builder */
    var buildRichSnippet = function (headings) {
        var items = [];
        var baseUrl = window.location.href.split('#')[0];
        for (var i = 0; i < headings.length; i++) {
            var h = headings[i];
            items.push({
                '@type': 'ListItem',
                'position': i + 1,
                'name': h.textContent.trim(),
                'url': baseUrl + '#' + h.id
            });
        }
        /* Das reine ItemList zusätzlich separat (sichtbar für Google-Tool) */
        var jsonLdVisible = {
            '@context': 'https://schema.org',
            '@type': 'ItemList',
            'name': 'Inhaltsverzeichnis',
            'itemListOrder': 'Unordered',
            'itemListElement': items
        };

        /* ️⃣ Das eingebettete WebPage-Objekt (semantisch korrekt für LLMs) */
        var jsonLdNested = {
            '@context': 'https://schema.org',
            '@type': 'WebPage',
            'name': document.title,
            'mainEntity': jsonLdVisible
        };

        /* beide injizieren */
        [jsonLdVisible, jsonLdNested].forEach(data => {
            var script = document.createElement('script');
            script.type = 'application/ld+json';
            script.textContent = JSON.stringify(data, null, 2);
            document.head.appendChild(script);
        });

    };

    var injectTOC = function () {
        var level = parseInt(headings[0].tagName.slice(1));
        var startingLevel = level;
        var len = headings.length - 1;

        var tocHTML = '';
        if (settings.preHeading) {
            tocHTML += '<span class="' + settings.preHeadingClass + '">' + settings.preHeading + '</span>';
        }
        if (settings.heading) {
            tocHTML += '<span class="' + settings.headingClass + '">' + settings.heading + '</span>';
        }
        tocHTML += getListTag();

        for (var i = 0; i < headings.length; i++) {
            var heading = headings[i];
            headingElements.push(heading);
            createID(heading, i);

            var currentLevel = parseInt(heading.tagName.slice(1));
            var levelDifference = currentLevel - level;
            level = currentLevel;

            var html = getStartingHTML(levelDifference, i);

            var liClass = settings.itemClass ? ' class="' + settings.itemClass + '"' : '';
            html += '<li' + liClass + '>';

            var linkClass = currentLevel > startingLevel ? settings.innerLinkClass : settings.linkClass;
            var linkClassAttr = linkClass ? ' class="' + linkClass + '"' : '';

            html += '<a href="#' + heading.id + '" title="' + heading.textContent.trim() + '"' + linkClassAttr + '>' + heading.textContent.trim() + '</a>';

            if (i === len) {
                html += getOutdent(Math.abs(startingLevel - currentLevel));
            }

            tocHTML += html;
        }

        tocHTML += getListCloseTag();
        tocListHTML = tocHTML;
        for (var i = 0; i < tocTargets.length; i++) {
            tocTargets[i].innerHTML = tocListHTML;
        }

        /* Falls aktiviert → Rich Snippet JSON-LD injizieren */
        if (settings.richSnippet) {
            buildRichSnippet(headings);
        }
    };

    var addClickHandlers = function () {
        tocLinks = [];
        for (var i = 0; i < tocTargets.length; i++) {
            var links = tocTargets[i].querySelectorAll('a');
            for (var j = 0; j < links.length; j++) {
                tocLinks.push(links[j]);
                links[j].addEventListener('click', function (e) {
                    e.preventDefault();
                    var targetId = this.getAttribute('href').substring(1);
                    var targetElement = document.getElementById(targetId);
                    if (targetElement) {
                        removeActiveClasses();
                        this.parentElement.classList.add(settings.activeClass);
                        var targetOffset = targetElement.offsetTop - (settings.scrollToOffset || 0);
                        window.scrollTo({ top: targetOffset, behavior: 'smooth' });
                    }
                });
            }
        }
    };

    var removeActiveClasses = function () {
        for (var i = 0; i < tocTargets.length; i++) {
            var activeItems = tocTargets[i].querySelectorAll('.' + settings.activeClass);
            for (var j = 0; j < activeItems.length; j++) {
                activeItems[j].classList.remove(settings.activeClass);
            }
        }
    };

    var updateActiveOnScroll = function () {
        var scrollPosition = window.scrollY || document.documentElement.scrollTop;
        var offset = settings.scrollToOffset || 0;
        removeActiveClasses();

        for (var i = 0; i < headingElements.length; i++) {
            var currentHeading = headingElements[i];
            var nextHeading = headingElements[i + 1] || null;
            var headingTop = currentHeading.offsetTop - offset;
            var headingBottom = nextHeading ? nextHeading.offsetTop - offset : document.body.scrollHeight;

            if (scrollPosition >= headingTop && scrollPosition < headingBottom) {
                for (var j = 0; j < tocTargets.length; j++) {
                    var targetLink = tocTargets[j].querySelector('a[href="#' + currentHeading.id + '"]');
                    if (targetLink) {
                        targetLink.parentElement.classList.add(settings.activeClass);
                    }
                }
                if (targetLink) targetLink.parentElement.classList.add(settings.activeClass);
                break;
            }
        }
    };

    var init = function () {
        headings = contentWrap.querySelectorAll(settings.levels);
        if (!headings.length) return;

        injectTOC();
        addClickHandlers();
        window.addEventListener('scroll', updateActiveOnScroll, { passive: true });
        setTimeout(updateActiveOnScroll, 100);
    };

    init();
};
