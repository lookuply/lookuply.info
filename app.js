// Language management
const TRANSLATIONS_URL = 'translations.json';
let translations = {};
let currentLang = 'en';

// Detect browser language
function detectBrowserLanguage() {
    const browserLang = navigator.language || navigator.userLanguage;
    const langCode = browserLang.split('-')[0].toLowerCase();

    // Check if we support this language
    const supportedLangs = ['en', 'sk', 'de', 'fr', 'es', 'cs', 'it', 'pl', 'nl', 'ro',
                           'bg', 'hr', 'da', 'et', 'fi', 'el', 'hu', 'ga', 'lv', 'lt',
                           'mt', 'pt', 'sl', 'sv'];

    return supportedLangs.includes(langCode) ? langCode : 'en';
}

// Get value from nested object path
function getNestedValue(obj, path) {
    return path.split('.').reduce((current, key) => current?.[key], obj);
}

// Apply translations to page
function applyTranslations(lang) {
    if (!translations[lang]) return;

    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        const value = getNestedValue(translations[lang], key);

        if (value) {
            if (el.tagName === 'TITLE') {
                document.title = value;
            } else {
                el.textContent = value;
            }
        }
    });

    // Update HTML lang attribute
    document.documentElement.lang = lang;

    // Update meta tags
    const ogTitle = document.querySelector('meta[property="og:title"]');
    const ogDesc = document.querySelector('meta[property="og:description"]');
    const metaDesc = document.querySelector('meta[name="description"]');

    if (ogTitle && translations[lang].title) {
        ogTitle.content = translations[lang].title;
    }
    if (ogDesc && translations[lang].tagline) {
        ogDesc.content = translations[lang].tagline + ' - ' + translations[lang].subtitle;
    }
    if (metaDesc && translations[lang].subtitle) {
        metaDesc.content = 'Lookuply - ' + translations[lang].tagline + '. ' + translations[lang].subtitle;
    }
}

// Load translations
async function loadTranslations() {
    try {
        const response = await fetch(TRANSLATIONS_URL);
        translations = await response.json();

        // Get saved language or detect browser language
        const savedLang = localStorage.getItem('lookuply_lang');
        currentLang = savedLang || detectBrowserLanguage();

        // Set select value
        const langSelect = document.getElementById('langSelect');
        langSelect.value = currentLang;

        // Apply translations
        applyTranslations(currentLang);
    } catch (error) {
        console.error('Failed to load translations:', error);
    }
}

// Handle language change
document.getElementById('langSelect').addEventListener('change', (e) => {
    currentLang = e.target.value;
    localStorage.setItem('lookuply_lang', currentLang);
    applyTranslations(currentLang);
});

// Load translations when page loads
document.addEventListener('DOMContentLoaded', loadTranslations);
