# -*- coding: utf-8 -*- 
with open("pagina_generata.html", "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n")
    f.write("<html lang='it'>\n")
    f.write("<head>\n")
    f.write("    <meta charset='UTF-8'>\n")
    f.write("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
    f.write("    <title>Progetto RASTA</title>\n")
    
    ########COLORI#######
    # ROSSO ACCESO = #FF0000  # ROSSO VIVO = #E74C3C
    # ROSSO SCURO = #8B0000  # ROSSO MATTONE = #A93226  # ROSSO BOURDEAUX = #800000 # BLU ACCESO = #0000FF
    # BLU VIVO = #2980B9    # BLU SCURO = #2874A6   # BLU MATTONE = #1F618D # BLU BOURDEAUX = #154360
    # VERDE ACCESO = #00FF00    # VERDE VIVO = #2ECC71  # VERDE SCURO = #27AE60 # VERDE MATTONE = #229954  
    # VERDE BOURDEAUX = #1E8449 # VERDE CHIARO = #A9DFBF    # VERDE CHIARO SCURO = #D5DBDB  # VERDE CHIARO MATTONE = #D5DBDB
    # VERDE CHIARO BOURDEAUX = #D5DBDB  # BLU ACCESO = #0000FF  # BLU VIVO = #2980B9    # BLU SCURO = #2874A6
    # BLU MATTONE = #1F618D # BLU BOURDEAUX = #154360
    
    # Stile CSS
    f.write("""
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.5; }
        h1 { color: #A93226; }
        h2 { color: #8B0000; }
        ul { margin-top: 10px; }
        li { margin-bottom: 10px; }
        .paper { border-top: 1px solid #ccc; margin-top: 30px; padding-top: 20px; }

        /* BLOCCO INTESTAZIONE LARGO E TESTO CENTRATO */
        .intestazione {
            background-color: #f0f0f0;
            padding: 40px 0;
            width: 100%;
        }
        .intestazione .contenuto {
            text-align: center;
            max-width: 800px;
            margin: 0 auto;
        }

        /* BOTTONE FINALE */
        .bottone-container {
            text-align: center;
            margin-top: 40px;
        }
        .bottone-link {
            background-color: #e74c3c;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
        }
        .bottone-link:hover {
            background-color: #c0392b;
        }

        /* CARD DOCUMENTI */
        .card-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        .card {
            width: 200px;
            border: 1px solid #ccc;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
        }
        .card img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            margin-bottom: 10px;
        }
        .card-title {
            font-weight: bold;
            color: #8B0000;
            text-decoration: none;
            display: block;
            margin: 10px 0 5px;
        }
        .card-desc {
            font-size: 0.9em;
            color: #555;
        }
    </style>
    """)
    
    f.write("</head>\n")
    f.write("<body>\n")

    # INTESTAZIONE CENTRATA
    f.write("<div class='intestazione'>\n")
    f.write("  <div class='contenuto'>\n")
    f.write("    <h1>Progetto RASTA:</h1>\n")
    f.write("    <h1>Elaborazione Testi e Gestione Documentale</h1>\n")
    f.write("    <p><strong>Autori:</strong> Alesi Nicol - Roberto Zanoni</p>\n")
    f.write("    <p><strong>Data:</strong> 20 maggio 2025</p>\n")
    f.write("    <p><strong>Descrizione:</strong> All'interno della qui presente pagina si intende proporre il progetto RASTA, in merito alla catalogazione dei vini italiani e delle loro specifiche</p>\n")
    f.write("  </div>\n")
    f.write("</div>\n")

    # LISTA DOCUMENTI con CARD VISUALI
    f.write("<h2 style='text-align: center;'>INDICE DOCUMENTI</h2>\n")

    f.write("<div class='card-container'>\n")

    file_cards = [
        ("files/xml_partenza.xml", "XML DI PARTENZA", "Loghi/366529-icona-di-vettore-xml-gratuito-vettoriale.jpg", "File XML base con struttura iniziale"),  # da inserire una volta finiti
        ("files/struttura.dtd", "DTD STRUTTURA XML", "img/dtd.png", "Definizione della struttura XML"),
        ("files/estrazione_immagini.py", "SCRIPT PYTHON ESTRAZIONE", "img/python.png", "Estrazione immagini dal dataset"),
        ("files/validazione.py", "SCRIPT VALIDAZIONE XML", "img/python.png", "Verifica della conformità XML con DTD"),
        ("files/mappa_italia.html", "MAPPA INTERATTIVA", "img/html.png", "Mappa HTML con aree cliccabili"),
        ("files/generazione_html.py", "GENERA HTML", "img/python.png", "Script per generare questa pagina"),
        ("files/mappa_interattiva.js", "JS MAPPA", "img/js.png", "Script JS per gestire l’interattività"),
        ("files/estrazione_immagini2.py", "SCRIPT IMG 2", "img/python.png", "Versione alternativa di estrazione immagini"),
        ("files/pagina_regione.html", "PAGINA REGIONE", "img/html.png", "Pagina HTML dedicata alla singola regione"),
    ]

    for path, title, icon, desc in file_cards:
        f.write("  <div class='card'>\n")
        f.write(f"    <img src='{icon}' alt='icon'>\n")
        f.write(f"    <a href='{path}' target='_blank' class='card-title'>{title}</a>\n")
        f.write(f"    <p class='card-desc'>{desc}</p>\n")
        f.write("  </div>\n")

    f.write("</div>\n")

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
    f.write("    <a class='bottone-link' href='../PROGETTO/home.html'>Vai al progetto</a>\n")  # da modificare alla fine
    f.write("</div>\n")

    f.write("</body>\n")
    f.write("</html>\n")

print("✅ Pagina HTML generata con successo in 'pagina_generata.html'")
