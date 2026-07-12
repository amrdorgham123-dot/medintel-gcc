/*
  MedIntel GCC — Language Engine
  ------------------------------
  Reusable AR/EN toggle for any page. Works with elements marked:
    data-ar="نص عربي"              data-en="English text"
    data-ar-html="<em>نص</em>"     data-en-html="<em>text</em>"   (for content with nested tags)
    data-lang-toggle                on any button that should switch language

  Usage in your page's own script, after this file is loaded:
    MedIntelLang.initLangToggle('ar');   // 'ar' or 'en' as the default/starting language
*/
(function () {
  let currentLang = 'ar';

  function applyLang(lang) {
    currentLang = lang;
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.body.classList.toggle('lang-en', lang === 'en');

    document.querySelectorAll('[data-ar]').forEach(function (el) {
      el.textContent = lang === 'ar' ? el.dataset.ar : el.dataset.en;
    });

    document.querySelectorAll('[data-ar-html]').forEach(function (el) {
      el.innerHTML = lang === 'ar' ? el.dataset.arHtml : el.dataset.enHtml;
    });

    document.querySelectorAll('[data-lang-toggle]').forEach(function (btn) {
      btn.textContent = lang === 'ar' ? 'EN' : 'AR';
    });

    const navToggle = document.getElementById('navToggle');
    if (navToggle) {
      navToggle.setAttribute('aria-label', lang === 'ar' ? 'فتح القائمة' : 'Open menu');
    }

    document.dispatchEvent(new CustomEvent('medintel:langchange', { detail: { lang: lang } }));
  }

  function toggleLang() {
    applyLang(currentLang === 'ar' ? 'en' : 'ar');
  }

  function initLangToggle(defaultLang) {
    defaultLang = defaultLang || 'ar';
    document.querySelectorAll('[data-lang-toggle]').forEach(function (btn) {
      btn.addEventListener('click', toggleLang);
    });
    applyLang(defaultLang);
  }

  window.MedIntelLang = {
    applyLang: applyLang,
    toggleLang: toggleLang,
    initLangToggle: initLangToggle,
    getCurrentLang: function () { return currentLang; }
  };
})();
