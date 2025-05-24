from lxml import etree
import os

WORKING_DIR = "D:/Magistrale/DiIorio/GestioneDocumentale/"
INPUT_FILENAME = "dati/vini.xml"
INPUT_PATH = WORKING_DIR + INPUT_FILENAME
OUTPUT_DIR = WORKING_DIR + "src/regioni2/"

# Assicurati che la cartella esista
os.makedirs(OUTPUT_DIR, exist_ok=True)

f = open(INPUT_PATH, "rb")   
vine_dom = etree.fromstring(f.read())
f.close()

html_template = '''
<html>
<head>
<meta charset="UTF-8"/>
<link rel="stylesheet" href="../../style/regionWine.css"></link>
</head>
<body>
<h1></h1>
<div class="vino-container"></div>
</body>
</html>'''

# Mappa per accumulare DOM per ogni regione
regioni_dom = {}

for vino in vine_dom:
    for regione in vino.find("Luogo"):
        nome_regione = regione.get("nome")

        # Crea nuovo DOM per la regione se non esiste
        if nome_regione not in regioni_dom:
            html_dom = etree.fromstring(html_template)
            html_dom[1][0].text = "Regione " + nome_regione
            regioni_dom[nome_regione] = html_dom
        else:
            html_dom = regioni_dom[nome_regione]

        body = html_dom[1]

        vinoDiv = etree.Element("div")
        vinoDiv.set("class", "vino-card")

        h1 = etree.Element("h2")
        h1.text = vino.get("nome")
        vinoDiv.append(h1)

        tipologyContainer = etree.Element("div")
        tipologyContainer.set("class", "row-container")
        tipologyLabel = etree.Element("strong")
        tipologyLabel.text = "Tipologia: "
        tipologia = etree.Element("p")
        tipologia.text = vino[0].text
        tipologyContainer.append(tipologyLabel)
        tipologyContainer.append(tipologia)
        vinoDiv.append(tipologyContainer)

        denominationContainer = etree.Element("div")
        denominationContainer.set("class", "row-container")
        denominationLabel = etree.Element("strong")
        denominationLabel.text = "Denominazione: "
        denominazione = etree.Element("p")
        denominazione.text = vino[1].text
        denominationContainer.append(denominationLabel)
        denominationContainer.append(denominazione)
        vinoDiv.append(denominationContainer)

        descriptionContainer = etree.Element("div")
        descriptionContainer.set("class", "row-container")
        descriptionLabel = etree.Element("strong")
        descriptionLabel.text = "Descrizione: "
        descrizione = etree.Element("p")
        descrizione.text = vino[2].text
        descriptionContainer.append(descriptionLabel)
        descriptionContainer.append(descrizione)
        vinoDiv.append(descriptionContainer)

        try:
            minValueContainer = etree.Element("div")
            minValueContainer.set("class", "row-container")
            minValueLabel = etree.Element("strong")
            minValueLabel.text = "Valore minimo: "
            valoreMinimo = etree.Element("p")
            valoreMinimo.text = vino[3].text
            minValueContainer.append(minValueLabel)
            minValueContainer.append(valoreMinimo)
            vinoDiv.append(minValueContainer)
        except:
            print("Non esiste il valore minimo")

        try:
            maxValueContainer = etree.Element("div")
            maxValueContainer.set("class", "row-container")
            maxValueLabel = etree.Element("strong")
            maxValueLabel.text = "Valore massimo: "
            valoreMassimo = etree.Element("p")
            valoreMassimo.text = vino[4].text
            maxValueContainer.append(maxValueLabel)
            maxValueContainer.append(valoreMassimo)
            vinoDiv.append(maxValueContainer)
        except:
            print("Non esiste il valore massimo")

        try:
            materiaPrimaContainer = etree.Element("div")
            materiaPrimaContainer.set("class", "row-container")
            materiaPrimaLabel = etree.Element("strong")
            materiaPrimaLabel.text = "Materia prima: "
            materiaPrima = etree.Element("p")
            materiaPrima.text = vino[5].text
            materiaPrimaContainer.append(materiaPrimaLabel)
            materiaPrimaContainer.append(materiaPrima)
            vinoDiv.append(materiaPrimaContainer)
        except:
            print("Non esiste la materia prima")

        try:
            provinceContainer = etree.Element("div")
            provinceContainer.set("class", "row-container")

            provinceLabel = etree.Element("strong")
            provinceLabel.text = "Province e città di produzione:"
            provinceContainer.append(provinceLabel)

            province_to_citta = {}

            for provincia in regione:
                nome_provincia = provincia.get("nome")

                # Se la provincia non esiste ancora, la inizializziamo
                if nome_provincia not in province_to_citta:
                    province_to_citta[nome_provincia] = []

                # Aggiungiamo tutte le città, evitando duplicati
                for citta in provincia:
                    nome_citta = citta.get("nome")
                    if nome_citta and nome_citta not in province_to_citta[nome_provincia]:
                        province_to_citta[nome_provincia].append(nome_citta)

            # Ora creiamo gli elementi HTML
            for nome_provincia, lista_citta in province_to_citta.items():
                singleProvinceContainer = etree.Element("div")
                singleProvinceContainer.set("class", "single-province")

                provinciaTesto = etree.Element("b")
                provinciaTesto.text = nome_provincia + " :"
                singleProvinceContainer.append(provinciaTesto)

                for nome_citta in lista_citta:
                    cittaTesto = etree.Element("span")
                    cittaTesto.text = " " + nome_citta + ", "
                    singleProvinceContainer.append(cittaTesto)

                provinceContainer.append(singleProvinceContainer)


            vinoDiv.append(provinceContainer)
        except:
            print("Non esistono province/città")

        body[1].append(vinoDiv)

# Scrivi tutti i file dopo averli costruiti
for nome_regione, html_dom in regioni_dom.items():
    OUTPUT_PATH = os.path.join(OUTPUT_DIR, nome_regione + ".html")
    html_dom_S = etree.tostring(html_dom, pretty_print=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as file_html_w:
        file_html_w.write(html_dom_S.decode())
