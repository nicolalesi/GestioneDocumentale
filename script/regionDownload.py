from SPARQLWrapper import SPARQLWrapper, JSON
from lxml import etree

# === CONFIG ===
ENDPOINT_WINE = "https://w3id.org/food/sparql"
ENDPOINT_DBPEDIA = "https://dbpedia.org/sparql"
REGIONE_RICHIESTA = "Toscana"

# === STEP 1: Ottieni i luoghi (comuni e province) della regione da DBpedia ===
def get_luoghi_della_regione(regione_label_it):
    print(f"🔍 Recupero i luoghi per la regione: {regione_label_it}")
    sparql = SPARQLWrapper(ENDPOINT_DBPEDIA)

    query_uri_regione = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?regione WHERE {{
        ?regione rdfs:label "{regione_label_it}"@it .
    }}
    LIMIT 1
    """
    sparql.setQuery(query_uri_regione)
    sparql.setReturnFormat(JSON)
    res = sparql.query().convert()
    bindings = res["results"]["bindings"]
    if not bindings:
        raise ValueError(f"Regione '{regione_label_it}' non trovata in DBpedia.")
    
    regione_uri = bindings[0]["regione"]["value"]

    # Recupera tutti i luoghi associati a quella regione
    query_luoghi = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT DISTINCT ?luogo WHERE {{
        ?luogo dbo:region <{regione_uri}> .
    }}
    """
    sparql.setQuery(query_luoghi)
    sparql.setReturnFormat(JSON)
    res = sparql.query().convert()
    return [b["luogo"]["value"] for b in res["results"]["bindings"]]

# === STEP 2: Query ai vini filtrando solo quelli nei luoghi ottenuti ===
def get_vini_per_luoghi(luoghi):
    sparql = SPARQLWrapper(ENDPOINT_WINE)
    CHUNK_SIZE = 30
    vini_risultati = []

    for i in range(0, len(luoghi), CHUNK_SIZE):
        chunk = luoghi[i:i + CHUNK_SIZE]
        # costruisco la lista con prefissi e virgole per VALUES
        luoghi_values = "\n".join([f"<{l}>" for l in chunk])

        query = f"""
        PREFIX wine: <http://w3id.org/food/ontology/disciplinare-vino/>
        PREFIX upper: <http://w3id.org/food/ontology/disciplinare-upper/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT DISTINCT
          ?vinoLabel ?tipologiaLabel ?denominazioneLabel ?luogo
          ?descrizioneLabel ?valoreMinimo ?valoreMassimo ?materiaPrimaLabel
        WHERE {{
            ?vino a wine:Vino .
            OPTIONAL {{ ?vino rdfs:label ?vinoLabel . FILTER (!langMatches(lang(?vinoLabel), "en")) }}
            OPTIONAL {{ ?vino upper:haTipologia ?tipologia . OPTIONAL {{ ?tipologia rdfs:label ?tipologiaLabel . FILTER (!langMatches(lang(?tipologiaLabel), "en")) }} }}
            OPTIONAL {{
                ?vino upper:haDenominazione ?denominazione .
                OPTIONAL {{ ?denominazione rdfs:label ?denominazioneLabel . FILTER (!langMatches(lang(?denominazioneLabel), "en")) }}
                OPTIONAL {{
                    ?denominazione upper:haLuogoDiProduzione ?luogo .
                    VALUES ?luogo {{ {luoghi_values} }}
                }}
            }}
            OPTIONAL {{
                ?vino upper:haDescrizione ?descrizione .
                OPTIONAL {{ ?descrizione rdfs:label ?descrizioneLabel . FILTER (!langMatches(lang(?descrizioneLabel), "en")) }}
                OPTIONAL {{ ?descrizione upper:haValoreMinimo ?valoreMinimo . }}
                OPTIONAL {{ ?descrizione upper:haValoreMassimo ?valoreMassimo . }}
                OPTIONAL {{ ?descrizione upper:haMateriaPrima ?materiaPrima .
                           OPTIONAL {{ ?materiaPrima rdfs:label ?materiaPrimaLabel . FILTER (!langMatches(lang(?materiaPrimaLabel), "en")) }} }}
            }}
        }}
        """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        print(f"➡️ Query per {len(chunk)} luoghi...")
        res = sparql.query().convert()
        vini_risultati.extend(res["results"]["bindings"])

    return vini_risultati


# === STEP 3: Generazione XML ===
def crea_xml_vini(results, regione_nome):
    root = etree.Element("Vini")
    vini_map = {}

    for row in results:
        vino = row.get("vinoLabel", {}).get("value", "Sconosciuto")
        tipologia = row.get("tipologiaLabel", {}).get("value", "")
        denominazione = row.get("denominazioneLabel", {}).get("value", "")
        luogo_uri = row.get("luogo", {}).get("value", "")
        descrizione = row.get("descrizioneLabel", {}).get("value", "")
        valoreMinimo = row.get("valoreMinimo", {}).get("value", "")
        valoreMassimo = row.get("valoreMassimo", {}).get("value", "")
        materiaPrima = row.get("materiaPrimaLabel", {}).get("value", "")

        if vino not in vini_map:
            vini_map[vino] = {
                "Tipologie": set(), "Denominazioni": set(), "Luoghi": set(),
                "Descrizioni": set(), "ValoriMinimi": set(), "ValoriMassimi": set(), "MateriePrime": set()
            }

        if tipologia: vini_map[vino]["Tipologie"].add(tipologia)
        if denominazione: vini_map[vino]["Denominazioni"].add(denominazione)
        if luogo_uri: vini_map[vino]["Luoghi"].add(luogo_uri)
        if descrizione: vini_map[vino]["Descrizioni"].add(descrizione)
        if valoreMinimo: vini_map[vino]["ValoriMinimi"].add(valoreMinimo)
        if valoreMassimo: vini_map[vino]["ValoriMassimi"].add(valoreMassimo)
        if materiaPrima: vini_map[vino]["MateriePrime"].add(materiaPrima)

    for vino, dati in vini_map.items():
        vino_elem = etree.SubElement(root, "Vino", nome=vino)

        for tag in ["Tipologie", "Denominazioni", "Descrizioni", "ValoriMinimi", "ValoriMassimi", "MateriePrime"]:
            elementi = dati[tag]
            if elementi:
                elem = etree.SubElement(vino_elem, tag)
                elem.text = ", ".join(sorted(elementi))

        if dati["Luoghi"]:
            luoghi_elem = etree.SubElement(vino_elem, "Luoghi")
            regione_elem = etree.SubElement(luoghi_elem, "Regione", nome=regione_nome)

            for luogo_uri in sorted(dati["Luoghi"]):
                nome_luogo = luogo_uri.split("/")[-1].replace("_", " ")
                etree.SubElement(regione_elem, "Città", nome=nome_luogo)

    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")

# === ESECUZIONE ===
try:
    luoghi = get_luoghi_della_regione(REGIONE_RICHIESTA)
    if not luoghi:
        print(f"❌ Nessun luogo trovato per la regione '{REGIONE_RICHIESTA}'.")
    else:
        results = get_vini_per_luoghi(luoghi)
        xml_data = crea_xml_vini(results, REGIONE_RICHIESTA)

        with open("vini_regionale.xml", "wb") as f:
            f.write(xml_data)

        print(f"✅ File 'vini_regionale.xml' creato con {len(results)} risultati.")
except Exception as e:
    print(f"❌ Errore: {e}")
