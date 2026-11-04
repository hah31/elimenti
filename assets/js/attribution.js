/* Lead attribution for the contact form.
 *
 * On the first page a visitor opens in this tab, remember where they came
 * from: the landing page, the referrer, any utm_source / utm_medium /
 * utm_campaign tags and a Google Ads gclid. Later page views never overwrite
 * it. Every form with a landing_page field gets those values, plus the page
 * it was sent from, in hidden inputs. Nothing leaves the browser unless the
 * form is submitted. No cookies, no libraries, no third parties.
 *
 * sessionStorage can be blocked (private modes, strict settings). Every read
 * and write is wrapped so the form still works without it; it then falls
 * back to the current page's values.
 */
(function () {
    'use strict';

    var KEY = 'elimenti_first_touch';
    var PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'gclid'];

    function read() {
        try {
            var raw = window.sessionStorage.getItem(KEY);
            return raw ? JSON.parse(raw) : null;
        } catch (e) {
            return null;
        }
    }

    function write(data) {
        try {
            window.sessionStorage.setItem(KEY, JSON.stringify(data));
        } catch (e) { /* storage blocked: fall back to this page's values */ }
    }

    function fromThisPage() {
        var data = { landing_page: window.location.pathname, referrer: document.referrer || '' };
        var query = Object.create(null);
        window.location.search.replace(/^\?/, '').split('&').forEach(function (pair) {
            if (!pair) return;
            var i = pair.indexOf('=');
            var k = i < 0 ? pair : pair.slice(0, i);
            var v = i < 0 ? '' : pair.slice(i + 1);
            try {
                k = decodeURIComponent(k.replace(/\+/g, ' '));
                v = decodeURIComponent(v.replace(/\+/g, ' '));
            } catch (e) { /* keep the raw value */ }
            if (!(k in query)) query[k] = v;
        });
        PARAMS.forEach(function (p) { data[p] = query[p] || ''; });
        return data;
    }

    var touch = read();
    if (!touch) {
        touch = fromThisPage();
        write(touch);
    }

    function fill(form) {
        var values = {
            landing_page: touch.landing_page,
            referrer: touch.referrer,
            utm_source: touch.utm_source,
            utm_medium: touch.utm_medium,
            utm_campaign: touch.utm_campaign,
            gclid: touch.gclid,
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
