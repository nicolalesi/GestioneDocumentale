# -*- coding: utf-8 -*-
output_path = "PROGETTO/Index/index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n")
    f.write("<html lang='it'>\n")
    f.write("<head>\n")
    f.write("    <meta charset='UTF-8'>\n")
    f.write("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
    f.write("    <title>Progetto RASTA</title>\n")
    f.write("    <link rel='stylesheet' href='./Index.css'>\n")
    f.write("</head>\n")
    f.write("<body>\n")

    # INTESTAZIONE CENTRATA
    f.write("<div class='intestazione'>\n")
    f.write("  <div class='contenuto'>\n")
    f.write("    <h1>Progetto RASTA: Elaborazione Testi e Gestione Documentale</h1>\n")
    f.write("    <p><strong>Autori:</strong> Alesi Nicol - Roberto Zanoni</p>\n")
    f.write("    <p><strong>Data:</strong> 26 Maggio 2025</p>\n")
    f.write("    <p><strong>Descrizione:</strong> All'interno della qui presente pagina si intende proporre il progetto 'RASTA' per il corso Elaborazione Testi e Gestione Documentale del corso Magistrale (LM) G.E.P.I.D, in merito alla <b>catalogazione dei vini italiani</b> e delle loro specifiche</p>\n")
    f.write("    <div class='bottone-github-container'>\n")
    f.write("        <a class='bottone-github' href='https://github.com/nicolalesi/GestioneDocumentale' target='_blank'>Accedi alla Repository GitHub</a>\n")
    f.write("    </div>\n")
    f.write("  </div>\n")
    f.write("</div>\n")
    f.write("<hr class='separatore'>\n")


    # LISTA DOCUMENTI con CARD VISUALI
    f.write("<h2 style='text-align: center;'>INDICE DOCUMENTI</h2>\n")
    f.write("<div class='card-container'>\n")
    


    file_cards = [
        ("files/estrazione_immagini.py", "<u>ESTRAZIONE DATI - QUERY SPARKLE</u> ", "../Loghi/python-logo-334x334.png", "Script che, tramite libreria '<b>SPARQLWrapper</b>', crea una query sparkl per estrazione dati tramite URI"),
        ("../vini.xml", "<u>XML ESTRATTO</u>", "../Loghi/8760470.png", "File XML base estratto tramite query; sono stati creati con LLM 25 vini fittizzi per regioni mancanti"),
        ("../DTD_ViniXML.dtd", "<u>FILE .DTD STRUTTURA XML</u>", "../Loghi/images.png", "File per definire la struttura gerarchica che l'XML deve seguire"),
        ("../ValidazioneXML.py", "<u>SCRIPT VALIDAZIONE XML</u>", "../Loghi/python-logo-334x334.png", "Validazione dei file XML rispetto alla struttura DTD definita"),
        ("../EstrazioneFoto.py", "<u>SCRIPT PYTHON ESTRAZIONE IMMAGINI</u>", "../Loghi/python-logo-334x334.png", "Tramite la libreria <b>'BingImageCrawler'</b> estrazione delle immagini in base all'attributo 'nome' del vino"),
        ("files/generazione_html.py", "<u>GENERA HTML INDEX</u>", "../Loghi/python-logo-334x334.png", "Script, tramite utilizzo della librerie '<b>entree</b> 'per generare la qui presente pagina HTML"), 
        ("files/estrazione_immagini.py", "<u>CSS INDEX</u>", "../Loghi/pngtree-vector-css-icon-code-black-button-vector-png-image_13830248.png", "Struttura estetica della qui presente pagina HTML richiamata nello script python"),
        ("files/mappa_italia.html", "<u>MAPPA INTERATTIVA JAVA</u>", "../Loghi/JavaScript-logo.png", "Mappa interattiva presa dal sito ... INSERIRE SITO"),
        ("files/mappa_italia.html", "<u>CSS MAPPA INTERATTIVA</u>", "../Loghi/pngtree-vector-css-icon-code-black-button-vector-png-image_13830248.png", "Struttura estetica della mappa interattiva richiamata nella pagina HTML"),
        ("files/mappa_italia.html", "<u>SCIPT CONVERSIONE DATI JSON</u>", "../Loghi/python-logo-334x334.png", "Tramite libreria '<b>xmltodict</b>' conversione del file XML inziale in .Json"),
        ("files/mappa_italia.html", "<u>SCRIPT CONVERSIONE DATI CSV</u>", "../Loghi/python-logo-334x334.png", "Tramite libreria '<b>xmltodict</b>' conversione del file XML inziale in .CSV"),
        ("files/estrazione_immagini.py", "<u>SCRIPT REGION GENERATOR HTML</u>", "../Loghi/python-logo-334x334.png", "Creazione tramite script python di singole pagine HTML per ogni regione"),
        ("files/mappa_italia.html", "<u>CSS PAGINE REGIONI</u>", "../Loghi/pngtree-vector-css-icon-code-black-button-vector-png-image_13830248.png", "Struttura estetica delle pagine HTML per ogni regione richiamata nel rispettivo script"),
        ("files/mappa_italia.html", "<u>SCIPT CONVERSIONE DATI JSON REGIONI</u>", "../Loghi/python-logo-334x334.png", "Stessa struttura della conversione JSON ma per ogni singola regione iterando un ciclo"),
        ("files/mappa_italia.html", "<u>SCRIPT CONVERSIONE DATI CSV REGIONI</u>", "../Loghi/python-logo-334x334.png", "Stessa struttura della conversione CSV ma per ogni singola regione iterando un ciclo"),
    ]

    for path, title, icon, desc in file_cards:
        f.write("  <div class='card'>\n")
        f.write(f"    <img src='{icon}' alt='icon' class='card-img'>\n")  # Immagine centrata
        f.write(f"    <h3 class='card-heading'><a href='{path}' target='_blank'>{title}</a></h3>\n")  # Titolo cliccabile
        f.write(f"    <p class='card-label'><u>Descrizione</u></p>\n")  # Etichetta descrizione
        f.write(f"    <p class='card-desc'>{desc}</p>\n")        # Testo descrizione
        f.write("  </div>\n")
    
    f.write("  </div>\n")    
    f.write("<hr class='separatore'>\n")
    # PAPER
    f.write("<div class='paper'>\n")
    f.write("    <h2 style='text-align: center;'>PAPER</h2>\n")
    f.write("    <p>Di seguito si intende <b>mettere in evidenza il processo</b> che il Gruppo di Lavoro (d'ora in poi GdL) per lo sviluppo del progetto RASTA</p>\n")
    f.write("    <p>Esempio: questo progetto esplora le relazioni tra X e Y. I dati mostrano che...</p>\n")
    f.write("    <h3><u>PARTE PRIMA - INDIVIDUAZIONE FILE XML E ORGANIZZAZIONE LAVORO</u></h3>\n")
    f.write("    <p>Query Sparkle, TYGA SU GIT</p>\n")
    f.write("    <h3><u>PARTE SECONDA - PULIZIA E PERFEZIONAMENTO XML</u></h3>\n")
    f.write("    <h3><u>PARTE TERZA - CREAZIONE DTD</u></h3>\n")
    f.write("    <h3><u>PARTE QUARTA - CREAZIONE SCRIPT .PY PER VALIDAZIONE XML</u></h3>\n")
    f.write("    <h3><u>PARTE QUINTA - CREAZIONE SCRIPT PER INDEX</u></h3>\n")
    f.write("    <h3><u>PARTE SESTA - JAVA SCRIPT PER INTERATTIVITA' MAPPA</u></h3>\n")
    f.write("    <h3><u>PARTE SETTIMA - CREAZIONE HTML PER PER PULL INFORMAZIONI SPECIFICA REGIONE</u></h3>\n")
    f.write("</div>\n")

    # BOTTONE FINALE
    f.write("<div class='bottone-container'>\n")
    f.write("    <a class='bottone-link' href='../PROGETTO/home.html'>Vai al progetto</a>\n") # Link al progetto principale
    f.write("</div>\n")

    f.write("</body>\n")
    f.write("</html>\n")

print("✅ Pagina HTML generata con successo in 'index.html'")
