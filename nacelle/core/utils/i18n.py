# stdlib imports
import re

# third-party imports
from babel import Locale


# Locale code = <language>_<territory> (ie 'en_US')
# to pick locale codes see http://cldr.unicode.org/index/cldr-spec/picking-the-right-language-code
# also see http://www.sil.org/iso639-3/codes.asp
# Language codes defined under iso 639-1 http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
# Territory codes defined under iso 3166-1 alpha-2 http://en.wikipedia.org/wiki/ISO_3166-1
# disable i18n if locales array is empty or None
locales = ['en_US', 'en_GB', 'it_IT']


def parse_accept_language_header(string, pattern='([a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})?)\s*(;\s*q\s*=\s*(1|0\.[0-9]+))?'):
    """
    Parse a dict from an Accept-Language header string
    (see http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)
    example input: en-US,en;q=0.8,es-es;q=0.5
    example output: {'en_US': 100, 'en': 80, 'es_ES': 50}
    """
    res = {}
    if not string:
        return None
    for match in re.finditer(pattern, string):
        if None == match.group(4):
            q = 1
        else:
            q = match.group(4)
        l = match.group(1).replace('-', '_')
        if len(l) == 2:
            l = l.lower()
        elif len(l) == 5:
            l = l.split('_')[0].lower() + "_" + l.split('_')[1].upper()
        else:
            l = None
        if l:
            res[l] = int(100 * float(q))
    return res


def get_locale_from_request(request):
    """
    Detect locale from request.header 'Accept-Language'
    Locale with the highest quality factor that most nearly matches our
    config.locales is returned.
    cls: self object

    Note that in the future if
    all User Agents adopt the convention of sorting quality factors in descending order
    then the first can be taken without needing to parse or sort the accept header
    leading to increased performance
    (see http://lists.w3.org/Archives/Public/ietf-http-wg/2012AprJun/0473.html)
    """
    header = request.headers.get("Accept-Language", '')
    parsed = parse_accept_language_header(header)
    if parsed is None:
        return None
    locale_list_sorted_by_q = sorted(parsed.iterkeys(), reverse=True)
    locale = Locale.negotiate(locale_list_sorted_by_q, locales, sep='_')
    return str(locale)


def get_locale(store, request):
    """
    """
    return get_locale_from_request(request)
