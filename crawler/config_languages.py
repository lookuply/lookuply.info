# Lookuply - All 24 EU Official Languages Configuration

LANGUAGES = {
    'bg': {'name': 'Bulgarian', 'native': 'Български', 'country': '🇧🇬'},
    'hr': {'name': 'Croatian', 'native': 'Hrvatski', 'country': '🇭🇷'},
    'cs': {'name': 'Czech', 'native': 'Čeština', 'country': '🇨🇿'},
    'da': {'name': 'Danish', 'native': 'Dansk', 'country': '🇩🇰'},
    'nl': {'name': 'Dutch', 'native': 'Nederlands', 'country': '🇳🇱'},
    'en': {'name': 'English', 'native': 'English', 'country': '🇬🇧'},
    'et': {'name': 'Estonian', 'native': 'Eesti', 'country': '🇪🇪'},
    'fi': {'name': 'Finnish', 'native': 'Suomi', 'country': '🇫🇮'},
    'fr': {'name': 'French', 'native': 'Français', 'country': '🇫🇷'},
    'de': {'name': 'German', 'native': 'Deutsch', 'country': '🇩🇪'},
    'el': {'name': 'Greek', 'native': 'Ελληνικά', 'country': '🇬🇷'},
    'hu': {'name': 'Hungarian', 'native': 'Magyar', 'country': '🇭🇺'},
    'ga': {'name': 'Irish', 'native': 'Gaeilge', 'country': '🇮🇪'},
    'it': {'name': 'Italian', 'native': 'Italiano', 'country': '🇮🇹'},
    'lv': {'name': 'Latvian', 'native': 'Latviešu', 'country': '🇱🇻'},
    'lt': {'name': 'Lithuanian', 'native': 'Lietuvių', 'country': '🇱🇹'},
    'mt': {'name': 'Maltese', 'native': 'Malti', 'country': '🇲🇹'},
    'pl': {'name': 'Polish', 'native': 'Polski', 'country': '🇵🇱'},
    'pt': {'name': 'Portuguese', 'native': 'Português', 'country': '🇵🇹'},
    'ro': {'name': 'Romanian', 'native': 'Română', 'country': '🇷🇴'},
    'sk': {'name': 'Slovak', 'native': 'Slovenčina', 'country': '🇸🇰'},
    'sl': {'name': 'Slovenian', 'native': 'Slovenščina', 'country': '🇸🇮'},
    'es': {'name': 'Spanish', 'native': 'Español', 'country': '🇪🇸'},
    'sv': {'name': 'Swedish', 'native': 'Svenska', 'country': '🇸🇪'},
}

# Start URLs for each language (top websites)
START_URLS = {
    'en': [
        'https://en.wikipedia.org/wiki/Portal:Contents',
        'https://news.ycombinator.com/',
        'https://www.bbc.com/',
        'https://www.theguardian.com/',
        'https://www.techcrunch.com/',
    ],
    'de': [
        'https://de.wikipedia.org/wiki/Wikipedia:Hauptseite',
        'https://www.spiegel.de/',
        'https://www.bild.de/',
        'https://www.heise.de/',
    ],
    'fr': [
        'https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil',
        'https://www.lemonde.fr/',
        'https://www.france24.com/fr/',
        'https://www.20minutes.fr/',
    ],
    'es': [
        'https://es.wikipedia.org/wiki/Wikipedia:Portada',
        'https://www.elpais.com/',
        'https://www.bbc.com/mundo',
        'https://www.infobae.com/',
    ],
    'it': [
        'https://it.wikipedia.org/wiki/Pagina_principale',
        'https://www.corriere.it/',
        'https://www.repubblica.it/',
        'https://www.ansa.it/',
    ],
    'pl': [
        'https://pl.wikipedia.org/wiki/Wikipedia:Strona_g%C5%82%C3%B3wna',
        'https://www.onet.pl/',
        'https://www.wp.pl/',
        'https://www.gazeta.pl/',
    ],
    'nl': [
        'https://nl.wikipedia.org/wiki/Wikipedia:Hoofdpagina',
        'https://www.ad.nl/',
        'https://nos.nl/',
        'https://www.nrc.nl/',
    ],
    'pt': [
        'https://pt.wikipedia.org/wiki/P%C3%A1gina_principal',
        'https://www.publico.pt/',
        'https://www.jn.pt/',
        'https://www.tsf.pt/',
    ],
    'cs': [
        'https://cs.wikipedia.org/wiki/Hlavn%C3%AD_strana',
        'https://www.idnes.cz/',
        'https://zpravy.seznam.cz/',
        'https://www.novinky.cz/',
    ],
    'sk': [
        'https://sk.wikipedia.org/wiki/%C3%9Astredn%C3%A1_str%C3%A1nka',
        'https://www.sme.sk/',
        'https://spectator.sme.sk/',
        'https://tasr.sk/',
    ],
    'hu': [
        'https://hu.wikipedia.org/wiki/Kezd%C5%91lap',
        'https://www.origo.hu/',
        'https://www.hvg.hu/',
        'https://www.portfolio.hu/',
    ],
    'ro': [
        'https://ro.wikipedia.org/wiki/Pagina_principal%C4%83',
        'https://www.digi24.ro/',
        'https://www.hotnews.ro/',
        'https://www.g4media.ro/',
    ],
    'bg': [
        'https://bg.wikipedia.org/wiki/%D0%9D%D0%B0%D1%87%D0%B0%D0%BB%D0%BD%D0%B0_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0',
        'https://www.dnevnik.bg/',
        'https://www.bgnes.bg/',
        'https://www.mediapool.bg/',
    ],
    'hr': [
        'https://hr.wikipedia.org/wiki/Glavna_stranica',
        'https://www.jutarnji.hr/',
        'https://www.vecernji.hr/',
        'https://www.index.hr/',
    ],
    'da': [
        'https://da.wikipedia.org/wiki/Forside',
        'https://www.dr.dk/',
        'https://www.jv.dk/',
        'https://www.tv2.dk/',
    ],
    'et': [
        'https://et.wikipedia.org/wiki/Esileht',
        'https://www.err.ee/',
        'https://www.delfi.ee/',
        'https://www.postimees.ee/',
    ],
    'fi': [
        'https://fi.wikipedia.org/wiki/Wikipedia:Etusivu',
        'https://www.yle.fi/',
        'https://www.helsinkitimes.fi/',
        'https://www.mtv.fi/',
    ],
    'el': [
        'https://el.wikipedia.org/wiki/%CE%91%CF%81%CF%87%CE%B9%CE%BA%CE%AE_%CF%83%CE%B5%CE%BB%CE%AF%CE%B4%CE%B1',
        'https://www.protothema.gr/',
        'https://www.kathimerini.gr/',
        'https://www.in.gr/',
    ],
    'ga': [
        'https://ga.wikipedia.org/wiki/Pr%C3%ADomhph%C3%A1gina',
        'https://www.rte.ie/',
        'https://www.irishtimes.com/',
        'https://www.independent.ie/',
    ],
    'lv': [
        'https://lv.wikipedia.org/wiki/Lapas_s%C4%81kums',
        'https://www.lsm.lv/',
        'https://www.delfi.lv/',
        'https://www.apollo.lv/',
    ],
    'lt': [
        'https://lt.wikipedia.org/wiki/Pagrindin%C4%97_puslapis',
        'https://www.lrt.lt/',
        'https://www.delfi.lt/',
        'https://www.15min.lt/',
    ],
    'mt': [
        'https://mt.wikipedia.org/wiki/Pa%C4%A7ina_ewlenija',
        'https://www.timesofmalta.com/',
        'https://www.maltatoday.com.mt/',
    ],
    'sv': [
        'https://sv.wikipedia.org/wiki/Huvudsida',
        'https://www.svt.se/',
        'https://www.aftonbladet.se/',
        'https://www.expressen.se/',
    ],
    'el': [
        'https://el.wikipedia.org/wiki/%CE%91%CF%81%CF%87%CE%B9%CE%BA%CE%AE_%CF%83%CE%B5%CE%BB%CE%AF%CE%B4%CE%B1',
        'https://www.protothema.gr/',
        'https://www.kathimerini.gr/',
        'https://www.in.gr/',
    ],
    'sl': [
        'https://sl.wikipedia.org/wiki/Glavna_stran',
        'https://www.delo.si/',
        'https://www.dnevnik.si/',
        'https://www.rtvslo.si/',
    ],
}

# Target pages per language for MVP (4M total)
PAGES_PER_LANGUAGE = {
    'en': 1000000,
    'de': 300000,
    'fr': 300000,
    'es': 200000,
    'it': 200000,
    'pl': 200000,
    'nl': 150000,
    'ro': 100000,
    'pt': 100000,
    'cs': 100000,
    'hu': 100000,
    'sv': 100000,
    'bg': 50000,
    'da': 50000,
    'fi': 50000,
    'sk': 50000,
    'hr': 50000,
    'el': 50000,
    'lt': 30000,
    'sl': 30000,
    'lv': 30000,
    'et': 30000,
    'ga': 10000,
    'mt': 10000,
}

def get_language_count():
    return len(LANGUAGES)

def get_total_target_pages():
    return sum(PAGES_PER_LANGUAGE.values())
