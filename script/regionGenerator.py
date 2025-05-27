from lxml import etree
import os
import re
import hashlib

def format_filename_hash(vino_nome, max_length=100):
    # Pulisci il nome: sostituisci spazi con underscore e rimuovi caratteri strani
    nome_pulito = vino_nome.strip().replace(" ", "_")

    # Calcola hash md5 della stringa originale
    hash_md5 = hashlib.md5(vino_nome.encode('utf-8')).hexdigest()

    # Usa i primi 10 caratteri del nome pulito come prefisso
    prefix = nome_pulito[:10]

    # Componi nome file: prefisso + __ + hash
    filename = f"{prefix}__{hash_md5}.jpg"

    # Tronca se troppo lungo (dovrebbe andare bene così)
    return filename[:max_length]


WORKING_DIR = "../"
INPUT_FILENAME = "dati/vini.xml"
INPUT_PATH = WORKING_DIR + INPUT_FILENAME
OUTPUT_DIR = WORKING_DIR + "src/regioni/"

# Assicurati che la cartella esista
os.makedirs(OUTPUT_DIR, exist_ok=True)

f = open(INPUT_PATH, "rb")   
vine_dom = etree.fromstring(f.read())
f.close()

html_template = '''
<html>
<head>
<meta charset="UTF-8"/>
<link rel="stylesheet" href="../../style/style.css"></link>
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
            titleDiv = etree.Element("div")
            spanRegione = etree.Element("span")
            spanRegione.text="Regione "
            spanNomeRegione = etree.Element("span")
            spanNomeRegione.text = nome_regione
            spanNomeRegione.set("itemprop", "officialName")
            titleDiv.append(spanRegione)
            titleDiv.append(spanNomeRegione)
            titleDiv.set("class", "regionTitle")
            titleDiv.set("itemscope",'')
            titleDiv.set("itemtype", "https://dbpedia.org/page/Regions_of_Italy")
            html_dom[1][0].append(titleDiv)
            regioni_dom[nome_regione] = html_dom
        else:
            html_dom = regioni_dom[nome_regione]

        body = html_dom[1]

        vinoDiv = etree.Element("div")
        vinoDiv.set("class", "vino-card")
        vinoDiv.set("itemscope",'')
        vinoDiv.set("itemtype", "http://etna.istc.cnr.it/food-page/ontology/disciplinare-upper/html")

        h1 = etree.Element("h2")
        h1.text = vino.get("nome")
        h1.set("itemprop", "label")

        # Ottieni il nome del vino e normalizzalo per file
        nome_vino = vino.get("nome")  # es: "Amarone della Valpolicella Classico Rosso Classico"
        nome_file = format_filename_hash(nome_vino)
        # Costruisci il path immagine
        img_path = f"../../img/immagini_vini/{nome_file}"
        img_element = etree.Element("img")
        img_element.set("src", img_path)
        img_element.set("alt", nome_vino)
        img_element.set("class", "vino-image")  # per personalizzare con CSS

        # Crea il div contenitore dell'immagine
        img_div = etree.Element("div")
        img_div.set("class", "imgDiv")
        img_div.append(img_element)

        # Inserisci imgDiv come primo figlio di vinoDiv
        infoDiv = etree.Element("div")
        infoDiv.set("class", "infoDiv")
        infoDiv.append(h1)
        infoDiv.set("itemscope",'')
        infoDiv.set("itemtype",'http://etna.istc.cnr.it/food-page/ontology/disciplinare-vino/Vino')

        tipologyContainer = etree.Element("div")
        tipologyContainer.set("class", "row-container")
        tipologyLabel = etree.Element("strong")
        tipologyLabel.text = "Tipologia: "
        tipologia = etree.Element("p")
        tipologia.text = vino[0].text
        tipologia.set("itemprop", "haTipologia")
        tipologyContainer.append(tipologyLabel)
        tipologyContainer.append(tipologia)

        infoDiv.append(tipologyContainer)

        denominationContainer = etree.Element("div")
        denominationContainer.set("class", "row-container")
        denominationLabel = etree.Element("strong")
        denominationLabel.text = "Denominazione: "
        denominazione = etree.Element("p")
        denominazione.text = vino[1].text
        denominazione.set("itemprop", "haDenominazione")
        denominationContainer.append(denominationLabel)
        denominationContainer.append(denominazione)
        
        infoDiv.append(denominationContainer)

        descriptionContainer = etree.Element("div")
        descriptionContainer.set("class", "row-container")
        descriptionLabel = etree.Element("strong")
        descriptionLabel.text = "Descrizione: "
        descrizione = etree.Element("p")
        descrizione.text = vino[2].text
        descrizione.set("itemprop", "haDescrizione")
        descrizione.set("itescope",'')
        descriptionContainer.append(descriptionLabel)
        descriptionContainer.append(descrizione)
        
        infoDiv.append(descriptionContainer)

        try:
            maxValueContainer = etree.Element("div")
            maxValueContainer.set("class", "row-container")
            maxValueLabel = etree.Element("strong")
            maxValueLabel.text = "Valore massimo: "
            valoreMassimo = etree.Element("p")
            valoreMassimo.text = vino.find("ValoreMassimo").text
            valoreMassimo.set("itemprop", "haDescrizione")
            maxValueContainer.append(minValueLabel)
            maxValueContainer.append(valoreMinimo)
            
            infoDiv.append(minValueContainer)
        except:
            print("Non esiste il valore massimo")

        try:
            minValueContainer = etree.Element("div")
            minValueContainer.set("class", "row-container")
            minValueLabel = etree.Element("strong")
            minValueLabel.text = "Valore minimo: "
            valoreMinimo = etree.Element("p")
            valoreMinimo.text = vino.find("ValoreMinimo").text
            valoreMinimo.set("itemprop", "haDescrizione")
            minValueContainer.append(maxValueLabel)
            minValueContainer.append(valoreMassimo)
            
            infoDiv.append(maxValueContainer)
        except:
            print("Non esiste il valore minimo")

        try:
            materiaPrimaContainer = etree.Element("div")
            materiaPrimaContainer.set("class", "row-container")
            materiaPrimaLabel = etree.Element("strong")
            materiaPrimaLabel.text = "Materia prima: "
            materiaPrima = etree.Element("p")
            materiaPrima.set("itemprop", "haDescrizione")
            materiaPrima.text = vino.find("MateriaPrima").text
            materiaPrimaContainer.append(materiaPrimaLabel)
            materiaPrimaContainer.append(materiaPrima)
            vinoDiv.append(materiaPrimaContainer)
            infoDiv.append(materiaPrimaContainer)
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
                singleProvinceContainer.set("itemscope",'')
                singleProvinceContainer.set("itemtype", "https://dbpedia.org/page/Provinces_of_Italy")

                provinciaTesto = etree.Element("b")
                provinciaTesto.set("itemprop", "name")
                provinciaTesto.text = nome_provincia + " :"
                singleProvinceContainer.append(provinciaTesto)

                cityContainer = etree.Element("div")
                cityContainer.set("class", "city-container")
                cityContainer.set("itemscope",'')
                cityContainer.set("itemtype", "https://dbpedia.org/ontology/City")

                for nome_citta in lista_citta:
                    cittaTesto = etree.Element("span")
                    cittaTesto.set("itemprop", "name")
                    cittaTesto.text = " " + nome_citta + " "
                    cityContainer.append(cittaTesto)

                singleProvinceContainer.append(cityContainer)
                provinceContainer.append(singleProvinceContainer)

            infoDiv.append(provinceContainer)
            vinoDiv.append(infoDiv)
            vinoDiv.append(img_div)
        except:
            print("Non esistono province/città")

        body[1].set("class","regionbody")
        body[1].append(vinoDiv)

# Scrivi tutti i file dopo averli costruiti
for nome_regione, html_dom in regioni_dom.items():
    OUTPUT_PATH = os.path.join(OUTPUT_DIR, nome_regione + ".html")
    html_dom_S = etree.tostring(html_dom, pretty_print=True, encoding="utf-8", method="html")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as file_html_w:
        file_html_w.write(html_dom_S.decode())
