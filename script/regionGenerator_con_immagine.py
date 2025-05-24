from lxml import etree
import os

WORKING_DIR = "/Users/robertozanoni/Downloads/LM_ANNO 2/SEMESTRE 2/Elaborazione Testi e Gestione Documentale/PROGETTO"
INPUT_FILENAME = "/vini.xml"
INPUT_PATH = WORKING_DIR + INPUT_FILENAME
OUTPUT_DIR = WORKING_DIR + "src/regioni/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

html_template = '''
<html>
<head>
<meta charset="UTF-8"/>
<link rel="stylesheet" href="../regionWine.css"></link>
</head>
<body>
<h1></h1>
<div class="vino-container"></div>
</body>
</html>
'''

with open(INPUT_PATH, "rb") as f:
    vine_dom = etree.fromstring(f.read())

regioni_dom = {}

for vino in vine_dom:
    for regione in vino.find("Luogo"):
        nome_regione = regione.get("nome")

        if nome_regione not in regioni_dom:
            html_dom = etree.fromstring(html_template)
            html_dom.xpath("//h1")[0].text = f"Regione {nome_regione}"
            regioni_dom[nome_regione] = html_dom
        else:
            html_dom = regioni_dom[nome_regione]

        container = html_dom.xpath("//div[@class='vino-container']")[0]

        vino_card = etree.Element("div", attrib={"class": "vino-card"})

        titolo = etree.SubElement(vino_card, "h2", attrib={"class": "vino-title"})
        titolo.text = vino.get("nome")

        vino_body = etree.SubElement(vino_card, "div", attrib={"class": "vino-body"})

        etree.SubElement(vino_body, "img", attrib={
            "class": "vino-image",
            "src": "/Users/robertozanoni/Downloads/LM_ANNO 2/SEMESTRE 2/Elaborazione Testi e Gestione Documentale/PROGETTOsrc/immagini_vini/Vino__Asti_Sottozona_Santa_Vittoria_d_Alba__Bianco_Vendemmia_Tardiva.jpg",
            "alt": "Immagine vino"
        })

        vino_details = etree.SubElement(vino_body, "div", attrib={"class": "vino-details"})

        labels = [
            ("Tipologia", 0),
            ("Denominazione", 1),
            ("Descrizione", 2),
            ("Valore minimo", 3),
            ("Valore massimo", 4),
            ("Materia prima", 5),
        ]
        for label, idx in labels:
            try:
                p = etree.SubElement(vino_details, "p")
                strong = etree.SubElement(p, "strong")
                strong.text = f"{label}: "
                strong.tail = vino[idx].text or ""
            except IndexError:
                continue

        # Raggruppa province e città
        province_nomi = []
        citta_nomi = []

        for provincia in regione.findall("Provincia"):
            nome_prov = provincia.get("nome")
            if nome_prov and nome_prov not in province_nomi:
                province_nomi.append(nome_prov)
            for citta in provincia.findall("Città"):
                nome_citta = citta.get("nome")
                if nome_citta and nome_citta not in citta_nomi:
                    citta_nomi.append(nome_citta)

        if province_nomi:
            p_prov = etree.SubElement(vino_details, "p", attrib={"class": "province"})
            strong = etree.SubElement(p_prov, "strong")
            strong.text = "Province: "
            strong.tail = ", ".join(province_nomi)

        if citta_nomi:
            p_citta = etree.SubElement(vino_details, "p", attrib={"class": "citta"})
            strong = etree.SubElement(p_citta, "strong")
            strong.text = "Città: "
            strong.tail = ", ".join(citta_nomi)

        container.append(vino_card)

for regione, dom in regioni_dom.items():
    filename = f"{regione.replace(' ', '_')}.html"
    with open(os.path.join(OUTPUT_DIR, filename), "wb") as f:
        f.write(etree.tostring(dom, pretty_print=True, encoding="utf-8", xml_declaration=True))
