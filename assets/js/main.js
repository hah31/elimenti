(function () {
    'use strict';

    /* ---------- Scroll fade-in ----------
     * Progressive enhancement: the hiding class is only added here, so with
     * JavaScript off every element stays visible. Elements already on screen
     * at load are never hidden, so the hero and H1 paint immediately.
     */

    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!reduceMotion && 'requestAnimationFrame' in window) {
        var pending = [];
        var offset = 60;

        document.querySelectorAll('[data-reveal] > *').forEach(function (el) {
            if (el.getBoundingClientRect().top > window.innerHeight) {
                el.classList.add('fade-in');
                pending.push(el);
            }
        });

        // Reveal every element whose top has come within the viewport,
        // including ones skipped past by an anchor jump or a fast scroll.
        var check = function () {
            var limit = window.innerHeight - offset;
            pending = pending.filter(function (el) {
                if (el.getBoundingClientRect().top < limit) {
                    el.classList.add('visible');
                    return false;
                }
                return true;
            });
            if (!pending.length) {
                window.removeEventListener('scroll', onScroll);
                window.removeEventListener('resize', onScroll);
            }
        };

        var ticking = false;
        var onScroll = function () {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(function () { ticking = false; check(); });
        };

        if (pending.length) {
            window.addEventListener('scroll', onScroll, { passive: true });
            window.addEventListener('resize', onScroll, { passive: true });
        }
    }

    /* ---------- Mobile menu ----------
     * The links live in the HTML. Below 768px the .js class (set in <head>)
     * turns the menu into an overlay that this button opens and closes.
     */

    var toggle = document.querySelector('.nav__toggle');
    var menu = document.getElementById('nav-menu');
    if (!toggle || !menu) return;

    var setOpen = function (open) {
        menu.classList.toggle('is-open', open);
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        document.body.style.overflow = open ? 'hidden' : '';
    };

    toggle.addEventListener('click', function () {
        setOpen(!menu.classList.contains('is-open'));
    });

    menu.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () { setOpen(false); });
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && menu.classList.contains('is-open')) {
            setOpen(false);
            toggle.focus();
        }
    });
})();
