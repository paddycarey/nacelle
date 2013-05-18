# stdlib imports
import re
import unicodedata as ud


def prettify_string(string):

    """
    Clean up a string (un-camelcase and replace
    dots/underscores with spaces)
    """

    # un-camelcase and convert to lowercase
    pretty_string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    pretty_string = re.sub('([a-z0-9])([A-Z])', r'\1_\2', pretty_string).lower()
    # replace underscores with spaces and title case
    pretty_string = pretty_string.replace('_', ' ')
    pretty_string = pretty_string.title()
    return pretty_string


# dict used to store/cache whether or not a
# particular letter is latin (saves lookup time)
latin_letters = {}


def is_latin(uchr):

    """
    Check if a single unicode character is
    latin using the unicodedata library
    """

    try:
        return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))


def only_roman_chars(unistr):

    """
    Check if a unicode string only contains latin characters
    """

    return all(is_latin(uchr) for uchr in unistr if uchr.isalpha())


def slugify(value):

    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """

    value = ud.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)
