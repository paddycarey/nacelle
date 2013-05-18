"""
Big dictable (is that a word?) tuple which has a list
of all the locales which nacelle knows about
"""
# Have images, need codes
# ['zh-hant', 'pt-pt', 'fil', 'zh-hans', 'pt-br', 'sco']

ISO_CODES = [
    ('sq', 'Albanian'),
    ('ar', 'Arabic'),
    ('eu', 'Basque'),
    ('bg', 'Bulgarian'),
    ('ca', 'Catalan Valencian'),
    ('hr', 'Croatian'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('nl', 'Dutch'),
    ('en', 'English'),
    ('eo', 'Esperanto'),
    ('et', 'Estonian'),
    ('fo', 'Faroese'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('gl', 'Galician'),
    ('de', 'German'),
    ('el', 'Greek Modern'),
    ('he', 'Hebrew (modern)'),
    ('hi', 'Hindi'),
    ('hu', 'Hungarian'),
    ('id', 'Indonesian'),
    ('ga', 'Irish'),
    ('is', 'Icelandic'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('km', 'Khmer'),
    ('ko', 'Korean'),
    ('lb', 'Luxembourgish Letzeburgesch'),
    ('lt', 'Lithuanian'),
    ('lv', 'Latvian'),
    ('mn', 'Mongolian'),
    ('nb', 'Norwegian Bokmal'),
    ('nn', 'Norwegian Nynorsk'),
    ('fa', 'Persian'),
    ('pl', 'Polish'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('ru', 'Russian'),
    ('se', 'Northern Sami'),
    ('sr', 'Serbian'),
    ('sk', 'Slovak'),
    ('sl', 'Slovene'),
    ('es', 'Spanish; Castilian'),
    ('sv', 'Swedish'),
    ('tg', 'Tajik'),
    ('th', 'Thai'),
    ('tl', 'Tagalog'),
    ('tr', 'Turkish'),
    ('uk', 'Ukrainian'),
    ('vi', 'Vietnamese')
]

# build dict of the above languages for easy access
iso6391_dict = dict(ISO_CODES)
