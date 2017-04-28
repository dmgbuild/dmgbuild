# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import struct

from .resources import *

# Language codes and encodings (from Script.h)
languages = {
    'English':           (0,   'mac_roman'),
    'French':            (1,   'mac_roman'),
    'German':            (2,   'mac_roman'),
    'Italian':           (3,   'mac_roman'),
    'Dutch':             (4,   'mac_roman'),
    'Swedish':           (5,   'mac_roman'),
    'Spanish':           (6,   'mac_roman'),
    'Danish':            (7,   'mac_roman'),
    'Portuguese':        (8,   'mac_roman'),
    'Norwegian':         (9,   'mac_roman'),
    'Hebrew':            (10,  'mac_hebrew'),
    'Japanese':          (11,  'shift_jis'),
    'Arabic':            (12,  'mac_arabic'),
    'Finnish':           (13,  'mac_roman'),
    'Greek':             (14,  'mac_greek'),
    'Icelandic':         (15,  'mac_icelandic'),
    'Maltese':           (16,  'mac_roman'),
    'Turkish':           (17,  'mac_turkish'),
    'Croatian':          (18,  'mac_croatian'),
    'TradChinese':       (19,  'big5'),
    'Urdu':              (20,  'mac_arabic'),
    'Hindi':             (21,  'mac_devanagari'),
    'Thai':              (22,  'iso8859_11'),
    'Korean':            (23,  'euc_kr'),
    'Lithuanian':        (24,  'mac_latin2'),
    'Polish':            (25,  'mac_latin2'),
    'Hungarian':         (26,  'mac_latin2'),
    'Estonian':          (27,  'mac_latin2'),
    'Latvian':           (28,  'mac_latin2'),
    'Sami':              (29,  'mac_sami'),
    'Faroese':           (30,  'mac_icelandic'),
    'Farsi':             (31,  'mac_farsi'),
    'Persian':           (31,  'mac_farsi'),
    'Russian':           (32,  'mac_cyrillic'),
    'SimpChinese':       (33,  'euc-cn'),
    'Flemish':           (34,  'mac_roman'),
    'IrishGaelic':       (35,  'mac_celtic'),
    'Albanian':          (36,  'mac_roman'),
    'mac_romanian':      (37,  'mac_romanian'),
    'Czech':             (38,  'mac_latin2'),
    'Slovak':            (39,  'mac_latin2'),
    'Slovenian':         (40,  'mac_croatian'),
    'Yiddish':           (41,  'mac_hebrew'),
    'Serbian':           (42,  'mac_cyrillic'),
    'Macedonian':        (43,  'mac_cyrillic'),
    'Bulgarian':         (44,  'mac_cyrillic'),
    'Ukrainian':         (45,  'mac_cyrillic'),
    'Byelorussian':      (46,  'mac_cyrillic'),
    'Belorussian':       (46,  'mac_cyrillic'),
    'Uzbek':             (47,  'mac_cyrillic'),
    'Kazakh':            (48,  'mac_cyrillic'),
    'Azerbaijani':       (49,  'mac_cyrillic'),
    'AzerbaijanAr':      (50,  'mac_arabic'),
    'Armenian':          (51,  'mac_armenian'),
    'Georgian':          (52,  'mac_georgian'),
    'Moldavian':         (53,  'mac_cyrillic'),
    'Kirghiz':           (54,  'mac_cyrillic'),
    'Tajiki':            (55,  'mac_cyrillic'),
    'Turkmen':           (56,  'mac_cyrillic'),
    'Mongolian':         (57,  'mac_mongolian'),
    'MongolianCyr':      (58,  'mac_cyrillic'),
    'Pashto':            (59,  'mac_arabic'),
    'Kurdish':           (60,  'mac_arabic'),
    'Kashmiri':          (61,  'mac_arabic'),
    'Sindhi':            (62,  'mac_arabic'),
    'Tibetan':           (63,  'mac_tibetan'),
    'Nepali':            (64,  'mac_devanagari'),
    'Sanskrit':          (65,  'mac_devanagari'),
    'Marathi':           (66,  'mac_devanagari'),
    'Bengali':           (67,  'mac_bengali'),
    'Assamese':          (68,  'mac_bengali'),
    'Gujarati':          (69,  'mac_gujarati'),
    'Punjabi':           (70,  'mac_gurmukhi'),
    'Oriya':             (71,  'mac_oriya'),
    'Malayalam':         (72,  'mac_malayalam'),
    'Kannada':           (73,  'mac_kannada'),
    'Tamil':             (74,  'mac_tamil'),
    'Telugu':            (75,  'mac_telugu'),
    'Sinhalese':         (76,  'mac_sinhalese'),
    'Burmese':           (77,  'mac_burmese'),
    'Khmer':             (78,  'mac_khmer'),
    'Lao':               (79,  'mac_lao'),
    'Vietnamese':        (80,  'mac_vietnamese'),
    'Indonesian':        (81,  'mac_roman'),
    'Tagalog':           (82,  'mac_roman'),
    'MalayRoman':        (83,  'mac_roman'),
    'MalayArabic':       (84,  'mac_arabic'),
    'Amharic':           (85,  'mac_ethiopic'),
    'Tigrinya':          (86,  'mac_ethiopic'),
    'Oromo':             (87,  'mac_ethiopic'),
    'Somali':            (88,  'mac_roman'),
    'Swahili':           (89,  'mac_roman'),
    'Kinyarwanda':       (90,  'mac_roman'),
    'Ruanda':            (90,  'mac_roman'),
    'Rundi':             (91,  'mac_roman'),
    'Nyanja':            (92,  'mac_roman'),
    'Chewa':             (92,  'mac_roman'),
    'Malagasy':          (93,  'mac_roman'),
    'Esperanto':         (94,  'mac_roman'),
    'Welsh':             (128, 'mac_celtic'),
    'Basque':            (129, 'mac_roman'),
    'Catalan':           (130, 'mac_roman'),
    'Latin':             (131, 'mac_roman'),
    'Quechua':           (132, 'mac_roman'),
    'Guarani':           (133, 'mac_roman'),
    'Aymara':            (134, 'mac_roman'),
    'Tatar':             (135, 'mac_cyrillic'),
    'Uighur':            (136, 'mac_arabic'),
    'Dzongkha':          (137, 'mac_tibetan'),
    'JavaneseRom':       (138, 'mac_roman'),
    'SundaneseRom':      (139, 'mac_roman'),
    'Galician':          (140, 'mac_roman'),
    'Afrikaans':         (141, 'mac_roman'),
    'Breton':            (142, 'mac_celtic'),
    'Inuktitut':         (143, 'mac_ethiopic'),
    'ScottishGaelic':    (144, 'mac_celtic'),
    'ManxGaelic':        (145, 'mac_celtic'),
    'IrishGaelicScript': (146, 'mac_gaelic'),
    'Tongan':            (147, 'mac_roman'),
    'GreekAncient':      (148, 'mac_greek'),
    'Greenlandic':       (149, 'mac_roman'),
    'AzerbaijanRoman':   (150, 'mac_roman'),
    'Nynorsk':           (151, 'mac_roman'),
}

# Standard fonts
fonts = {
    'New York':      2,
    'Geneva':        3,
    'Monaco':        4,
    'Venice':        5,
    'London':        6,
    'Athens':        7,
    'San Francisco': 8,
    'Toronto':       9,
    'Cairo':         11,
    'Los Angeles':   12,
    'Times':         20,
    'Helvetica':     21,
    'Courier':       22,
    'Symbol':        23,
    'Mobile':        24
}

# LPic template resource
lpic_tmpl = [
    ('Default language ID',            'DWRD'),
    ('Count',                          'OCNT'),
    ('****',                           'LSTC'),
    ('sys lang ID',                    'DWRD'),
    ('local res ID (offset from 5000', 'DWRD'),
    ('2-byte language?',               'DWRD'),
    ('****',                           'LSTE'),
]

# Buttons (these come from the SLAResources file which you can find in the SLA
#          SDK on developer.apple.com)
default_buttons = {
    'English': (
        b'English',
        b'Agree',
        b'Disagree',
        b'Print',
        b'Save',
        b'If you agree with the terms of this license, press "Agree" to '
        b'install the software.  If you do not agree, press "Disagree".'
    ),

    'German': (
        b'Deutsch',
        b'Akzeptieren',
        b'Ablehnen',
        b'Drucken',
        b'Sichern...',
        b'Klicken Sie in \xd2Akzeptieren\xd3, wenn Sie mit den Bestimmungen des Software-Lizenzvertrags einverstanden sind. Falls nicht, bitte \xd2Ablehnen\xd3 anklicken. Sie k\x9annen die Software nur installieren, wenn Sie \xd2Akzeptieren\xd3 angeklickt haben.'
    ),

    'Spanish': (
        b'Espa\x96ol',
        b'Aceptar',
        b'No aceptar',
        b'Imprimir',
        b'Guardar...',
        b'Si est\x87 de acuerdo con los t\x8erminos de esta licencia, pulse "Aceptar" para instalar el software. En el supuesto de que no est\x8e de acuerdo con los t\x8erminos de esta licencia, pulse "No aceptar."'
    ),

    'French': (
        b'Fran\x8dais',
        b'Accepter',
        b'Refuser',
        b'Imprimer',
        b'Enregistrer...',
        b'Si vous acceptez les termes de la pr\x8esente licence, cliquez sur "Accepter" afin d\'installer le logiciel. Si vous n\'\x90tes pas d\'accord avec les termes de la licence, cliquez sur "Refuser".'
    ),

    'Italian': (
        b'Italiano',
        b'Accetto',
        b'Rifiuto',
        b'Stampa',
        b'Registra...',
        b'Se accetti le condizioni di questa licenza, fai clic su "Accetto" per installare il software. Altrimenti fai clic su "Rifiuto".'
    ),

    'Japanese': (
        b'Japanese',
        b'\x93\xaf\x88\xd3\x82\xb5\x82\xdc\x82\xb7',
        b'\x93\xaf\x88\xd3\x82\xb5\x82\xdc\x82\xb9\x82\xf1',
        b'\x88\xf3\x8d\xfc\x82\xb7\x82\xe9',
        b'\x95\xdb\x91\xb6...',
        b'\x96{\x83\\\x83t\x83g\x83E\x83G\x83A\x8eg\x97p\x8b\x96\x91\xf8\x8c_\x96\xf1\x82\xcc\x8f\xf0\x8c\x8f\x82\xc9\x93\xaf\x88\xd3\x82\xb3\x82\xea\x82\xe9\x8f\xea\x8d\x87\x82\xc9\x82\xcd\x81A\x83\\\x83t\x83g\x83E\x83G\x83A\x82\xf0\x83C\x83\x93\x83X\x83g\x81[\x83\x8b\x82\xb7\x82\xe9\x82\xbd\x82\xdf\x82\xc9\x81u\x93\xaf\x88\xd3\x82\xb5\x82\xdc\x82\xb7\x81v\x82\xf0\x89\x9f\x82\xb5\x82\xc4\x82\xad\x82\xbe\x82\xb3\x82\xa2\x81B\x81@\x93\xaf\x88\xd3\x82\xb3\x82\xea\x82\xc8\x82\xa2\x8f\xea\x8d\x87\x82\xc9\x82\xcd\x81A\x81u\x93\xaf\x88\xd3\x82\xb5\x82\xdc\x82\xb9\x82\xf1\x81v\x82\xf0\x89\x9f\x82\xb5\x82\xc4\x82\xad\x82\xbe\x82\xb3\x82\xa2\x81B'
    ),

    'Dutch': (
        b'Nederlands',
        b'Ja',
        b'Nee',
        b'Print',
        b'Bewaar...',
        b'Indien u akkoord gaat met de voorwaarden van deze licentie, kunt u op \'Ja\' klikken om de programmatuur te installeren. Indien u niet akkoord gaat, klikt u op \'Nee\'.'
    ),

    'Swedish': (
        b'Svensk',
        b'Godk\x8anns',
        b'Avb\x9ajs',
        b'Skriv ut',
        b'Spara...',
        b'Om Du godk\x8anner licensvillkoren klicka p\x8c "Godk\x8anns" f\x9ar att installera programprodukten. Om Du inte godk\x8anner licensvillkoren, klicka p\x8c "Avb\x9ajs".'
    ),

    'Portuguese': (
        b'Portugu\x90s',
        b'Concordar',
        b'Discordar',
        b'Imprimir',
        b'Salvar...',
        b'Se est\x87 de acordo com os termos desta licen\x8da, pressione "Concordar" para instalar o software. Se n\x8bo est\x87 de acordo, pressione "Discordar".'
    ),

    'SimpChinese': (
        b'Simplified Chinese',
        b'\xcd\xac\xd2\xe2',
        b'\xb2\xbb\xcd\xac\xd2\xe2',
        b'\xb4\xf2\xd3\xa1',
        b'\xb4\xe6\xb4\xa2\xa1\xad',
        b'\xc8\xe7\xb9\xfb\xc4\xfa\xcd\xac\xd2\xe2\xb1\xbe\xd0\xed\xbf\xc9\xd0\xad\xd2\xe9\xb5\xc4\xcc\xf5\xbf\xee\xa3\xac\xc7\xeb\xb0\xb4\xa1\xb0\xcd\xac\xd2\xe2\xa1\xb1\xc0\xb4\xb0\xb2\xd7\xb0\xb4\xcb\xc8\xed\xbc\xfe\xa1\xa3\xc8\xe7\xb9\xfb\xc4\xfa\xb2\xbb\xcd\xac\xd2\xe2\xa3\xac\xc7\xeb\xb0\xb4\xa1\xb0\xb2\xbb\xcd\xac\xd2\xe2\xa1\xb1\xa1\xa3'
    ),

    'TradChinese': (
        b'Traditional Chinese',
        b'\xa6P\xb7N',
        b'\xa4\xa3\xa6P\xb7N',
        b'\xa6C\xa6L',
        b'\xc0x\xa6s\xa1K',
        b'\xa6p\xaaG\xb1z\xa6P\xb7N\xa5\xbb\xb3\\\xa5i\xc3\xd2\xb8\xcc\xaa\xba\xb1\xf8\xb4\xda\xa1A\xbd\xd0\xab\xf6\xa1\xa7\xa6P\xb7N\xa1\xa8\xa5H\xa6w\xb8\xcb\xb3n\xc5\xe9\xa1C\xa6p\xaaG\xa4\xa3\xa6P\xb7N\xa1A\xbd\xd0\xab\xf6\xa1\xa7\xa4\xa3\xa6P\xb7N\xa1\xa8\xa1C'
    ),

    'Danish': (
        b'Dansk',
        b'Enig',
        b'Uenig',
        b'Udskriv',
        b'Arkiver...',
        b'Hvis du accepterer betingelserne i licensaftalen, skal du klikke p\x8c \xd2Enig\xd3 for at installere softwaren. Klik p\x8c \xd2Uenig\xd3 for at annullere installeringen.'
    ),

    'Finnish': (
        b'Suomi',
        b'Hyv\x8aksyn',
        b'En hyv\x8aksy',
        b'Tulosta',
        b'Tallenna\xc9',
        b'Hyv\x8aksy lisenssisopimuksen ehdot osoittamalla \xd5Hyv\x8aksy\xd5. Jos et hyv\x8aksy sopimuksen ehtoja, osoita \xd5En hyv\x8aksy\xd5.'
    ),

    'Korean': (
        b'Korean',
        b'\xb5\xbf\xc0\xc7',
        b'\xb5\xbf\xc0\xc7 \xbe\xc8\xc7\xd4',
        b'\xc7\xc1\xb8\xb0\xc6\xae',
        b'\xc0\xfa\xc0\xe5...',
        b'\xbb\xe7\xbf\xeb \xb0\xe8\xbe\xe0\xbc\xad\xc0\xc7 \xb3\xbb\xbf\xeb\xbf\xa1 \xb5\xbf\xc0\xc7\xc7\xcf\xb8\xe9, "\xb5\xbf\xc0\xc7" \xb4\xdc\xc3\xdf\xb8\xa6 \xb4\xad\xb7\xaf \xbc\xd2\xc7\xc1\xc6\xae\xbf\xfe\xbe\xee\xb8\xa6 \xbc\xb3\xc4\xa1\xc7\xcf\xbd\xca\xbd\xc3\xbf\xc0. \xb5\xbf\xc0\xc7\xc7\xcf\xc1\xf6 \xbe\xca\xb4\xc2\xb4\xd9\xb8\xe9, "\xb5\xbf\xc0\xc7 \xbe\xc8\xc7\xd4" \xb4\xdc\xc3\xdf\xb8\xa6 \xb4\xa9\xb8\xa3\xbd\xca\xbd\xc3\xbf\xc0.'
    ),

    'Norwegian': (
        b'Norsk',
        b'Enig',
        b'Ikke enig',
        b'Skriv ut',
        b'Arkiver...',
        b'Hvis De er enig i bestemmelsene i denne lisensavtalen, klikker De p\x8c "Enig"-knappen for \x8c installere programvaren. Hvis De ikke er enig, klikker De p\x8c "Ikke enig".'
    ),
}

class LPicResource (Resource):
    def __init__(self, res_id, res_name, default_lang, lpic, res_attrs=0):
        data = []
        data.append(struct.pack(b'>HH', default_lang, len(lpic)))
        for lang,rid,two_byte in lpic:
            data.append(struct.pack(b'>HHH', lang, rid, int(two_byte)))
        super(LPicResource, self).__init__(b'LPic', res_id, res_name,
                                           b''.join(data), res_attrs)

def maybe_encode(s, encoding):
    if isinstance(s, bytes):
        return s
    return s.encode(encoding)

def add_license(filename, license_info):
    """Add a license agreement to the specified disk image file, which should
    have been unflattened first."""

    fork = ResourceFork.from_file(filename)
    fork.add(TMPLResource(128, 'LPic', lpic_tmpl))

    default_lang = license_info.get('default-lang', 'English')
    default_lang_id = languages.get(default_lang, (0, 'mac_roman'))[0]

    lpic = []
    ndx = 1
    for language,license_data in license_info['licenses'].items():
        lang_id = languages[language][0]
        encoding_name = languages[language][1]

        is_two_byte = language in ('Japanese', 'TradChinese',
                                   'SimpChinese', 'Korean')

        if license_data.startswith('{\\rtf1'):
            fork.add(Resource(b'RTF ', 5000 + ndx, language + ' SLA',
                              str(license_data)))
        else:
            fork.add(TextResource(5000 + ndx, language + ' SLA',
                                  maybe_encode(license_data, encoding_name)))
            fork.add(StyleResource(5000 + ndx, language + ' SLA',
                                   [Style(0, 12, 9, Style.Helvetica,
                                          0, 0, (0, 0, 0))]))

        buttons = license_info.get('buttons', {}).get(language, None)
        if buttons is None:
            buttons = default_buttons.get(language, None)
            if buttons is None:
                buttons = default_buttons['English']

        buttons = [maybe_encode(b, encoding_name) for b in buttons]

        fork.add(StringListResource(5000 + ndx, language + ' Buttons',
                                    buttons))

        lpic.append((lang_id, ndx, is_two_byte))

        ndx += 1

    fork.add(LPicResource(5000, None, default_lang_id, lpic))

    fork.write_to_file(filename)
