/* Lead attribution for the contact form.
 *
 * First visit (localStorage, kept for 90 days from that visit): the landing
 * page, the referrer, any utm_source / utm_medium / utm_campaign tags and a
 * Google Ads gclid. Later visits never overwrite it until it expires, so a
 * lead who found the site on Google and comes back days later still shows
 * where they first came from.
 *
 * This visit (sessionStorage, cleared when the tab closes): the page the
 * visit started on and its referrer, sent as last_landing_page and
 * last_referrer.
 *
 * Every form with a landing_page field gets these values, plus the page it
 * was sent from, in hidden inputs. Nothing leaves the browser unless the
 * form is submitted. No cookies, no libraries, no third parties.
 *
 * Storage can be blocked (private modes, strict settings). Every read and
 * write is wrapped so the form still works without it; it then falls back
 * to the current page's values.
 */
(function () {
    'use strict';

    var FIRST_KEY = 'elimenti_first_touch';
    var VISIT_KEY = 'elimenti_visit';
    var MAX_AGE = 90 * 24 * 60 * 60 * 1000;
    var PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'gclid'];
    var now = new Date().getTime();

    function store(kind) {
        try {
            return window[kind];
        } catch (e) {
            return null;
        }
    }

    function read(kind, key) {
        try {
            var s = store(kind);
            var raw = s ? s.getItem(key) : null;
            return raw ? JSON.parse(raw) : null;
        } catch (e) {
            return null;
        }
    }

    function write(kind, key, data) {
        try {
            var s = store(kind);
            if (s) s.setItem(key, JSON.stringify(data));
        } catch (e) { /* storage blocked: fall back to this page's values */ }
    }

    function query() {
        var out = Object.create(null);
        window.location.search.replace(/^\?/, '').split('&').forEach(function (pair) {
            if (!pair) return;
            var i = pair.indexOf('=');
            var k = i < 0 ? pair : pair.slice(0, i);
            var v = i < 0 ? '' : pair.slice(i + 1);
            try {
                k = decodeURIComponent(k.replace(/\+/g, ' '));
                v = decodeURIComponent(v.replace(/\+/g, ' '));
            } catch (e) { /* keep the raw value */ }
            if (!(k in out)) out[k] = v;
        });
        return out;
    }

    var here = { landing_page: window.location.pathname, referrer: document.referrer || '' };

    // First visit in the last 90 days.
    var first = read('localStorage', FIRST_KEY);
    if (!first || typeof first.t !== 'number' || now - first.t > MAX_AGE || now < first.t) {
        var q = query();
        first = { t: now, landing_page: here.landing_page, referrer: here.referrer };
        PARAMS.forEach(function (p) { first[p] = q[p] || ''; });
        write('localStorage', FIRST_KEY, first);
    }

    // This visit.
    var visit = read('sessionStorage', VISIT_KEY);
    if (!visit) {
        visit = here;
        write('sessionStorage', VISIT_KEY, visit);
    }

    function fill(form) {
        var values = {
            landing_page: first.landing_page,
            referrer: first.referrer,
            utm_source: first.utm_source,
            utm_medium: first.utm_medium,
            utm_campaign: first.utm_campaign,
            gclid: first.gclid,
            last_landing_page: visit.landing_page,
            last_referrer: visit.referrer,
            submitted_from: window.location.pathname
        };
        Object.keys(values).forEach(function (name) {
            var input = form.querySelector('input[name="' + name + '"]');
            if (input) input.value = values[name] || '';
        });
    }

    document.querySelectorAll('form').forEach(function (form) {
        if (!form.querySelector('input[name="landing_page"]')) return;
        fill(form);
        form.addEventListener('submit', function () { fill(form); });
    });
})();
