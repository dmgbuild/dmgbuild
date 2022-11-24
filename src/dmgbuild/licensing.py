import os

language_names_map = {
    "da_DK": "Dansk",
    "de_DE": "Deutsch",
    "en_AU": "English",
    "en_GB": "English",
    "en_NZ": "English",
    "en_US": "English",
    "es_ES": "Español",
    "fr_CA": "Français",
    "fr_FR": "Français",
    "it_IT": "Italiano",
    "ja_JP": "Japanese",
    "nb_NO": "Norsk",
    "nl_BE": "Nederlands",
    "nl_NL": "Nederlands",
    "pt_BR": "Português",
    "pt_PT": "Português",
    "sv_SE": "Svensk",
    "zh_CN": "Simplified Chinese",
    "zh_TW": "Traditional Chinese",
}

# Buttons (these come from the SLAResources file which you can find in the SLA
#          SDK on developer.apple.com)
default_buttons = {
    "English": (
        b"English",
        b"Agree",
        b"Disagree",
        b"Print",
        b"Save",
        b'If you agree with the terms of this license, press "Agree" to install the software.  If you do not agree, press "Disagree".',  # noqa; E501
    ),
    "Deutsch": (
        b"Deutsch",
        b"Akzeptieren",
        b"Ablehnen",
        b"Drucken",
        b"Sichern...",
        b"Klicken Sie in \xd2Akzeptieren\xd3, wenn Sie mit den Bestimmungen des Software-Lizenzvertrags einverstanden sind. Falls nicht, bitte \xd2Ablehnen\xd3 anklicken. Sie k\x9annen die Software nur installieren, wenn Sie \xd2Akzeptieren\xd3 angeklickt haben.",  # noqa; E501
    ),
    "Español": (
        b"Espa\x96ol",
        b"Aceptar",
        b"No aceptar",
        b"Imprimir",
        b"Guardar...",
        b'Si est\x87 de acuerdo con los t\x8erminos de esta licencia, pulse "Aceptar" para instalar el software. En el supuesto de que no est\x8e de acuerdo con los t\x8erminos de esta licencia, pulse "No aceptar."',  # noqa; E501
    ),
    "Français": (
        b"Fran\x8dais",
        b"Accepter",
        b"Refuser",
        b"Imprimer",
        b"Enregistrer...",
        b'Si vous acceptez les termes de la pr\x8esente licence, cliquez sur "Accepter" afin d\'installer le logiciel. Si vous n\'\x90tes pas d\'accord avec les termes de la licence, cliquez sur "Refuser".',  # noqa; E501
    ),
    "Italiano": (
        b"Italiano",
        b"Accetto",
        b"Rifiuto",
        b"Stampa",
        b"Registra...",
        b'Se accetti le condizioni di questa licenza, fai clic su "Accetto" per installare il software. Altrimenti fai clic su "Rifiuto".',  # noqa; E501
    ),
    "Japanese": (
        b"Japanese",
        b"\x93\xaf\x88\xd3\x82\xb5\x82\xdc\x82\xb7",
        b"\x93\xaf\x88\xd3\x82\xb5\x82\xdc\x82\xb9\x82\xf1",
        b"\x88\xf3\x8d\xfc\x82\xb7\x82\xe9",
        b"\x95\xdb\x91\xb6...",
        b"\x96{\x83\\\x83t\x83g\x83E\x83G\x83A\x8eg\x97p\x8b\x96\x91\xf8\x8c_\x96\xf1\x82\xcc\x8f\xf0\x8c\x8f\x82\xc9\x93\xaf\x88\xd3\x82\xb3\x82\xea\x82\xe9\x8f\xea\x8d\x87\x82\xc9\x82\xcd\x81A\x83\\\x83t\x83g\x83E\x83G\x83A\x82\xf0\x83C\x83\x93\x83X\x83g\x81[\x83\x8b\x82\xb7\x82\xe9\x82\xbd\x82\xdf\x82\xc9\x81u\x93\xaf\x88\xd3\x82\xb5\x82\xdc\x82\xb7\x81v\x82\xf0\x89\x9f\x82\xb5\x82\xc4\x82\xad\x82\xbe\x82\xb3\x82\xa2\x81B\x81@\x93\xaf\x88\xd3\x82\xb3\x82\xea\x82\xc8\x82\xa2\x8f\xea\x8d\x87\x82\xc9\x82\xcd\x81A\x81u\x93\xaf\x88\xd3\x82\xb5\x82\xdc\x82\xb9\x82\xf1\x81v\x82\xf0\x89\x9f\x82\xb5\x82\xc4\x82\xad\x82\xbe\x82\xb3\x82\xa2\x81B",  # noqa; E501
    ),
    "Nederlands": (
        b"Nederlands",
        b"Ja",
        b"Nee",
        b"Print",
        b"Bewaar...",
        b"Indien u akkoord gaat met de voorwaarden van deze licentie, kunt u op 'Ja' klikken om de programmatuur te installeren. Indien u niet akkoord gaat, klikt u op 'Nee'.",  # noqa; E501
    ),
    "Svensk": (
        b"Svensk",
        b"Godk\x8anns",
        b"Avb\x9ajs",
        b"Skriv ut",
        b"Spara...",
        b'Om Du godk\x8anner licensvillkoren klicka p\x8c "Godk\x8anns" f\x9ar att installera programprodukten. Om Du inte godk\x8anner licensvillkoren, klicka p\x8c "Avb\x9ajs".',  # noqa; E501
    ),
    "Português": (
        b"Portugu\x90s",
        b"Concordar",
        b"Discordar",
        b"Imprimir",
        b"Salvar...",
        b'Se est\x87 de acordo com os termos desta licen\x8da, pressione "Concordar" para instalar o software. Se n\x8bo est\x87 de acordo, pressione "Discordar".',  # noqa; E501
    ),
    "Simplified Chinese": (
        b"Simplified Chinese",
        b"\xcd\xac\xd2\xe2",
        b"\xb2\xbb\xcd\xac\xd2\xe2",
        b"\xb4\xf2\xd3\xa1",
        b"\xb4\xe6\xb4\xa2\xa1\xad",
        b"\xc8\xe7\xb9\xfb\xc4\xfa\xcd\xac\xd2\xe2\xb1\xbe\xd0\xed\xbf\xc9\xd0\xad\xd2\xe9\xb5\xc4\xcc\xf5\xbf\xee\xa3\xac\xc7\xeb\xb0\xb4\xa1\xb0\xcd\xac\xd2\xe2\xa1\xb1\xc0\xb4\xb0\xb2\xd7\xb0\xb4\xcb\xc8\xed\xbc\xfe\xa1\xa3\xc8\xe7\xb9\xfb\xc4\xfa\xb2\xbb\xcd\xac\xd2\xe2\xa3\xac\xc7\xeb\xb0\xb4\xa1\xb0\xb2\xbb\xcd\xac\xd2\xe2\xa1\xb1\xa1\xa3",  # noqa; E501
    ),
    "Traditional Chinese": (
        b"Traditional Chinese",
        b"\xa6P\xb7N",
        b"\xa4\xa3\xa6P\xb7N",
        b"\xa6C\xa6L",
        b"\xc0x\xa6s\xa1K",
        b"\xa6p\xaaG\xb1z\xa6P\xb7N\xa5\xbb\xb3\\\xa5i\xc3\xd2\xb8\xcc\xaa\xba\xb1\xf8\xb4\xda\xa1A\xbd\xd0\xab\xf6\xa1\xa7\xa6P\xb7N\xa1\xa8\xa5H\xa6w\xb8\xcb\xb3n\xc5\xe9\xa1C\xa6p\xaaG\xa4\xa3\xa6P\xb7N\xa1A\xbd\xd0\xab\xf6\xa1\xa7\xa4\xa3\xa6P\xb7N\xa1\xa8\xa1C",  # noqa; E501
    ),
    "Dansk": (
        b"Dansk",
        b"Enig",
        b"Uenig",
        b"Udskriv",
        b"Arkiver...",
        b"Hvis du accepterer betingelserne i licensaftalen, skal du klikke p\x8c \xd2Enig\xd3 for at installere softwaren. Klik p\x8c \xd2Uenig\xd3 for at annullere installeringen.",  # noqa; E501
    ),
    "Suomi": (
        b"Suomi",
        b"Hyv\x8aksyn",
        b"En hyv\x8aksy",
        b"Tulosta",
        b"Tallenna\xc9",
        b"Hyv\x8aksy lisenssisopimuksen ehdot osoittamalla \xd5Hyv\x8aksy\xd5. Jos et hyv\x8aksy sopimuksen ehtoja, osoita \xd5En hyv\x8aksy\xd5.",  # noqa; E501
    ),
    "Korean": (
        b"Korean",
        b"\xb5\xbf\xc0\xc7",
        b"\xb5\xbf\xc0\xc7 \xbe\xc8\xc7\xd4",
        b"\xc7\xc1\xb8\xb0\xc6\xae",
        b"\xc0\xfa\xc0\xe5...",
        b'\xbb\xe7\xbf\xeb \xb0\xe8\xbe\xe0\xbc\xad\xc0\xc7 \xb3\xbb\xbf\xeb\xbf\xa1 \xb5\xbf\xc0\xc7\xc7\xcf\xb8\xe9, "\xb5\xbf\xc0\xc7" \xb4\xdc\xc3\xdf\xb8\xa6 \xb4\xad\xb7\xaf \xbc\xd2\xc7\xc1\xc6\xae\xbf\xfe\xbe\xee\xb8\xa6 \xbc\xb3\xc4\xa1\xc7\xcf\xbd\xca\xbd\xc3\xbf\xc0. \xb5\xbf\xc0\xc7\xc7\xcf\xc1\xf6 \xbe\xca\xb4\xc2\xb4\xd9\xb8\xe9, "\xb5\xbf\xc0\xc7 \xbe\xc8\xc7\xd4" \xb4\xdc\xc3\xdf\xb8\xa6 \xb4\xa9\xb8\xa3\xbd\xca\xbd\xc3\xbf\xc0.',  # noqa; E501
    ),
    "Norsk": (
        b"Norsk",
        b"Enig",
        b"Ikke enig",
        b"Skriv ut",
        b"Arkiver...",
        b'Hvis De er enig i bestemmelsene i denne lisensavtalen, klikker De p\x8c "Enig"-knappen for \x8c installere programvaren. Hvis De ikke er enig, klikker De p\x8c "Ikke enig".',  # noqa; E501
    ),
}

udifrezXMLtemplate = {
    "LPic": [
        {
            "Attributes": "0x0000",
            "Data": b"\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00",
            "ID": "5000",
            "Name": "",
        }
    ],
    "STR#": [
        {
            "Attributes": "0x0000",
            "Data": b'\x00\x06\x07English\x05Agree\x08Disagree\x05Print\x07Save...{If you agree with the terms of this license, press "Agree" to install the software.  If you do not agree, press "Disagree".',  # noqa; E501
            "ID": "5000",
            "Name": "English",
        },
    ],
    # ?? License text would be included in a block like this:
    # ?? 'TEXT': [
    # ??     {
    # ??         'Attributes': '0x0000',
    # ??         'Data': b'license text',
    # ??         'ID': '5000',
    # ??         'Name': 'English'
    # ??     }
    # ?? ],
    "TMPL": [
        {
            "Attributes": "0x0000",
            "Data": b"\x13Default Language IDDWRD\x05CountOCNT\x04****LSTC\x0bsys lang IDDWRD\x1elocal res ID (offset from 5000DWRD\x102-byte language?DWRD\x04****LSTE",  # noqa: E501
            "ID": "128",
            "Name": "LPic",
        }
    ],
    "styl": [
        {
            "Attributes": "0x0000",
            "Data": b"\x00\x03\x00\x00\x00\x00\x00\x0c\x00\t\x00\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\x00\x0c\x00\t\x00\x14\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00*\x00\x0c\x00\t\x00\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",  # noqa: E501
            "ID": "5000",
            "Name": "English",
        }
    ],
}


def maybe_encode(s, encoding="mac_roman"):
    if isinstance(s, bytes):
        return s
    return s.encode(encoding)


def build_license(license_info):
    """Add a license agreement to the specified disk image file, see
    https://developer.apple.com/forums/thread/668084."""
    # Copy the original template
    xml = dict(udifrezXMLtemplate)

    for language, license_data in license_info["licenses"].items():
        if language not in language_names_map:
            raise Exception(
                "Unknown language '"
                + language
                + "'. Valid languages are: "
                + ", ".join(sorted(language_names_map.keys()))
            )

        language_name = language_names_map[language]

        if os.path.isfile(license_data):
            mode = "rb" if license_data.endswith(".rtf") else "r"
            with open(license_data, mode=mode) as f:
                license_data = f.read()

        if type(license_data) == bytes and license_data.startswith(b"{\\rtf1"):
            licenseDataFormat = "RTF "

        else:
            licenseDataFormat = "TEXT"
            license_data = maybe_encode(license_data)

        if licenseDataFormat not in xml:
            xml[licenseDataFormat] = []

        xml[licenseDataFormat].append(
            {
                "Attributes": "0x0000",
                "Data": license_data,
                "ID": "5000",
                "Name": language_name,
            }
        )

        language_default_buttons = default_buttons.get(
            language_name, default_buttons["English"]
        )
        buttons = license_info.get("buttons", {}).get(
            language, language_default_buttons
        )

        assert len(buttons) == 6, "License buttons must have 6 entries."

        buttons = [maybe_encode(b) for b in buttons]
        xml["STR#"].append(
            {
                "Attributes": "0x0000",
                "Data": (
                    b"\x00\x06\x07"
                    + buttons[0]
                    + b"\x05"
                    + buttons[1]
                    + b"\x08"
                    + buttons[2]
                    + b"\x05"
                    + buttons[3]
                    + b"\x07"
                    + buttons[4]
                    + b"{"
                    + buttons[5]
                ),
                "ID": "5002",
                "Name": language_name,
            }
        )

    return xml
