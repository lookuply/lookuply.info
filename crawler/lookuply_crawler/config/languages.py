"""
EU Languages Configuration
This module defines all 24 official EU languages with their metadata.
"""

LANGUAGES = {
    'bg': {
        'name': 'Bulgarian',
        'native': 'Български',
        'code': 'bg',
        'iso639_1': 'bg',
        'iso639_2': 'bul',
        'locale': 'bg_BG'
    },
    'hr': {
        'name': 'Croatian',
        'native': 'Hrvatski',
        'code': 'hr',
        'iso639_1': 'hr',
        'iso639_2': 'hrv',
        'locale': 'hr_HR'
    },
    'cs': {
        'name': 'Czech',
        'native': 'Čeština',
        'code': 'cs',
        'iso639_1': 'cs',
        'iso639_2': 'ces',
        'locale': 'cs_CZ'
    },
    'da': {
        'name': 'Danish',
        'native': 'Dansk',
        'code': 'da',
        'iso639_1': 'da',
        'iso639_2': 'dan',
        'locale': 'da_DK'
    },
    'nl': {
        'name': 'Dutch',
        'native': 'Nederlands',
        'code': 'nl',
        'iso639_1': 'nl',
        'iso639_2': 'nld',
        'locale': 'nl_NL'
    },
    'en': {
        'name': 'English',
        'native': 'English',
        'code': 'en',
        'iso639_1': 'en',
        'iso639_2': 'eng',
        'locale': 'en_GB'
    },
    'et': {
        'name': 'Estonian',
        'native': 'Eesti',
        'code': 'et',
        'iso639_1': 'et',
        'iso639_2': 'est',
        'locale': 'et_EE'
    },
    'fi': {
        'name': 'Finnish',
        'native': 'Suomi',
        'code': 'fi',
        'iso639_1': 'fi',
        'iso639_2': 'fin',
        'locale': 'fi_FI'
    },
    'fr': {
        'name': 'French',
        'native': 'Français',
        'code': 'fr',
        'iso639_1': 'fr',
        'iso639_2': 'fra',
        'locale': 'fr_FR'
    },
    'de': {
        'name': 'German',
        'native': 'Deutsch',
        'code': 'de',
        'iso639_1': 'de',
        'iso639_2': 'deu',
        'locale': 'de_DE'
    },
    'el': {
        'name': 'Greek',
        'native': 'Ελληνικά',
        'code': 'el',
        'iso639_1': 'el',
        'iso639_2': 'ell',
        'locale': 'el_GR'
    },
    'hu': {
        'name': 'Hungarian',
        'native': 'Magyar',
        'code': 'hu',
        'iso639_1': 'hu',
        'iso639_2': 'hun',
        'locale': 'hu_HU'
    },
    'ga': {
        'name': 'Irish',
        'native': 'Gaeilge',
        'code': 'ga',
        'iso639_1': 'ga',
        'iso639_2': 'gle',
        'locale': 'ga_IE'
    },
    'it': {
        'name': 'Italian',
        'native': 'Italiano',
        'code': 'it',
        'iso639_1': 'it',
        'iso639_2': 'ita',
        'locale': 'it_IT'
    },
    'lv': {
        'name': 'Latvian',
        'native': 'Latviešu',
        'code': 'lv',
        'iso639_1': 'lv',
        'iso639_2': 'lav',
        'locale': 'lv_LV'
    },
    'lt': {
        'name': 'Lithuanian',
        'native': 'Lietuvių',
        'code': 'lt',
        'iso639_1': 'lt',
        'iso639_2': 'lit',
        'locale': 'lt_LT'
    },
    'mt': {
        'name': 'Maltese',
        'native': 'Malti',
        'code': 'mt',
        'iso639_1': 'mt',
        'iso639_2': 'mlt',
        'locale': 'mt_MT'
    },
    'pl': {
        'name': 'Polish',
        'native': 'Polski',
        'code': 'pl',
        'iso639_1': 'pl',
        'iso639_2': 'pol',
        'locale': 'pl_PL'
    },
    'pt': {
        'name': 'Portuguese',
        'native': 'Português',
        'code': 'pt',
        'iso639_1': 'pt',
        'iso639_2': 'por',
        'locale': 'pt_PT'
    },
    'ro': {
        'name': 'Romanian',
        'native': 'Română',
        'code': 'ro',
        'iso639_1': 'ro',
        'iso639_2': 'ron',
        'locale': 'ro_RO'
    },
    'sk': {
        'name': 'Slovak',
        'native': 'Slovenčina',
        'code': 'sk',
        'iso639_1': 'sk',
        'iso639_2': 'slk',
        'locale': 'sk_SK'
    },
    'sl': {
        'name': 'Slovenian',
        'native': 'Slovenščina',
        'code': 'sl',
        'iso639_1': 'sl',
        'iso639_2': 'slv',
        'locale': 'sl_SI'
    },
    'es': {
        'name': 'Spanish',
        'native': 'Español',
        'code': 'es',
        'iso639_1': 'es',
        'iso639_2': 'spa',
        'locale': 'es_ES'
    },
    'sv': {
        'name': 'Swedish',
        'native': 'Svenska',
        'code': 'sv',
        'iso639_1': 'sv',
        'iso639_2': 'swe',
        'locale': 'sv_SE'
    },
}

# Language codes list for easy iteration
LANGUAGE_CODES = list(LANGUAGES.keys())

# Language names mapping (English names)
LANGUAGE_NAMES = {code: lang['name'] for code, lang in LANGUAGES.items()}

# Native names mapping
NATIVE_NAMES = {code: lang['native'] for code, lang in LANGUAGES.items()}


def get_language_info(code: str) -> dict:
    """Get language information by code."""
    return LANGUAGES.get(code, None)


def is_valid_language(code: str) -> bool:
    """Check if language code is valid."""
    return code in LANGUAGES


def get_all_language_codes() -> list:
    """Get all language codes."""
    return LANGUAGE_CODES
