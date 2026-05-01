(function () {
    'use strict';

    /* ---------- Scroll fade-in ---------- */

    const fadeSelectors = [
        '.hero__text',
        '.hero__visual',
        '.services > h2',
        '.service-card',
        '.process > h2',
        '.process__step',
        '.expect > h2',
        '.expect > p',
        '.contact > h2',
        '.contact .btn',
        '.contact__email'
    ];

    const fadeTargets = document.querySelectorAll(fadeSelectors.join(','));
    fadeTargets.forEach(el => el.classList.add('fade-in'));

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.12,
            rootMargin: '0px 0px -60px 0px'
        });

        fadeTargets.forEach(el => observer.observe(el));
    } else {
        fadeTargets.forEach(el => el.classList.add('visible'));
    }

    /* ---------- Mobile hamburger nav ---------- */

    const nav = document.querySelector('.nav');
    if (!nav) return;

    const hamburger = document.createElement('button');
    hamburger.className = 'nav__hamburger';
    hamburger.type = 'button';
    hamburger.setAttribute('aria-label', 'Open menu');
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.innerHTML = '<span></span><span></span>';
    nav.appendChild(hamburger);

    const overlay = document.createElement('div');
    overlay.className = 'nav__overlay';
    overlay.setAttribute('aria-hidden', 'true');
    overlay.innerHTML = [
        '<a href="#services">Services</a>',
        '<a href="#process">Process</a>',
        '<a href="#expect">What to Expect</a>',
        '<a href="#contact">Start a Project</a>'
    ].join('');
    document.body.appendChild(overlay);

    const setOpen = (open) => {
        overlay.classList.toggle('is-open', open);
        hamburger.classList.toggle('is-active', open);
        hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
        hamburger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
        overlay.setAttribute('aria-hidden', open ? 'false' : 'true');
        document.body.style.overflow = open ? 'hidden' : '';
    };

    hamburger.addEventListener('click', () => {
        setOpen(!overlay.classList.contains('is-open'));
    });

    overlay.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => setOpen(false));
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && overlay.classList.contains('is-open')) {
            setOpen(false);
        }
    });
})();
