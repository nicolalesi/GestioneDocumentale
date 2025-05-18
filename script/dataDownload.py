from SPARQLWrapper import SPARQLWrapper, JSON
from lxml import etree

# Configurazione endpoint
endpoint_url = "https://w3id.org/food/sparql"
dbpedia_url = "https://dbpedia.org/sparql"

# Query SPARQL
sparql_query = """
PREFIX wine: <http://w3id.org/food/ontology/disciplinare-vino/>
PREFIX upper: <http://w3id.org/food/ontology/disciplinare-upper/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbpedia: <http://dbpedia.org/resource/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT
?vinoLabel
?tipologiaLabel
?denominazioneLabel
?luogo
?descrizioneLabel
?valoreMinimo
?valoreMassimo
?materiaPrimaLabel
WHERE {
  ?vino a wine:Vino .
  OPTIONAL { ?vino rdfs:label ?vinoLabel . FILTER(!langMatches(lang(?vinoLabel), "en")) }
  OPTIONAL { ?vino upper:haTipologia ?tipologia . OPTIONAL { ?tipologia rdfs:label ?tipologiaLabel . FILTER(!langMatches(lang(?tipologiaLabel), "en")) } }
  OPTIONAL {
    ?vino upper:haDenominazione ?denominazione .
    OPTIONAL { ?denominazione rdfs:label ?denominazioneLabel . FILTER(!langMatches(lang(?denominazioneLabel), "en")) }
    OPTIONAL { ?denominazione upper:haLuogoDiProduzione ?luogo . FILTER(STRSTARTS(STR(?luogo), "http://dbpedia.org/resource")) }
  }
  OPTIONAL {
    ?vino upper:haDescrizione ?descrizione .
    OPTIONAL { ?descrizione rdfs:label ?descrizioneLabel . FILTER(!langMatches(lang(?descrizioneLabel), "en")) }
    OPTIONAL { ?descrizione upper:haValoreMinimo ?valoreMinimo . }
    OPTIONAL { ?descrizione upper:haValoreMassimo ?valoreMassimo . }
    OPTIONAL { ?descrizione upper:haMateriaPrima ?materiaPrima .
               OPTIONAL { ?materiaPrima rdfs:label ?materiaPrimaLabel . FILTER(!langMatches(lang(?materiaPrimaLabel), "en")) } }
  }
}
LIMIT 10000
"""

# Funzione per ottenere la provincia da DBpedia
def get_provincia_from_dbpedia(luogo_uri):
    dbpedia_sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    # 1. Trova l'URI della provincia
    provincia_query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT ?provincia WHERE {{
        <{luogo_uri}> dbo:province ?provincia .
    }}
    LIMIT 1
    """
    dbpedia_sparql.setQuery(provincia_query)
    dbpedia_sparql.setReturnFormat(JSON)
    results = dbpedia_sparql.query().convert()
    bindings = results.get("results", {}).get("bindings", [])

    if bindings:
        provincia_uri = bindings[0]["provincia"]["value"]

        # 2. Recupera l'etichetta (in italiano se possibile)
        label_query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label WHERE {{
            <{provincia_uri}> rdfs:label ?label .
            FILTER (langMatches(lang(?label), "it"))
        }}
        LIMIT 1
        """
        dbpedia_sparql.setQuery(label_query)
        dbpedia_sparql.setReturnFormat(JSON)
        label_result = dbpedia_sparql.query().convert()
        label_bindings = label_result.get("results", {}).get("bindings", [])

        if label_bindings:
            return label_bindings[0]["label"]["value"]
        else:
            # Se nessuna label italiana, restituisci l'ultima parte dell'URI come fallback
            return provincia_uri.split("/")[-1].replace("_", " ")
    else:
        return "Sconosciuta"

try:
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()["results"]["bindings"]

    root = etree.Element("Vini")
    vini_map = {}
    luogo_regioni = {}

    for row in results:
        vino = row.get("vinoLabel", {}).get("value", "Sconosciuto")
        tipologia = row.get("tipologiaLabel", {}).get("value", "")
        denominazione = row.get("denominazioneLabel", {}).get("value", "")
        luogo = row.get("luogo", {}).get("value", "")
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
        if luogo: vini_map[vino]["Luoghi"].add(luogo)
        if descrizione: vini_map[vino]["Descrizioni"].add(descrizione)
        if valoreMinimo: vini_map[vino]["ValoriMinimi"].add(valoreMinimo)
        if valoreMassimo: vini_map[vino]["ValoriMassimi"].add(valoreMassimo)
        if materiaPrima: vini_map[vino]["MateriePrime"].add(materiaPrima)
        if luogo and luogo not in luogo_regioni:
            luogo_regioni[luogo] = None

    dbpedia_sparql = SPARQLWrapper(dbpedia_url)
    for luogo in luogo_regioni:
        try:
            query = f"""
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dbp: <http://dbpedia.org/property/>
            SELECT ?regione WHERE {{
                OPTIONAL {{ <{luogo}> dbp:seat ?comune . ?comune dbo:region ?regione . }}
                OPTIONAL {{ <{luogo}> dbo:region ?regione . }}
                FILTER(BOUND(?regione))
            }}
            LIMIT 1
            """
            dbpedia_sparql.setQuery(query)
            dbpedia_sparql.setReturnFormat(JSON)
            res = dbpedia_sparql.query().convert()["results"]["bindings"]

            if res:
                regione_uri = res[0]["regione"]["value"]

                # Ottieni label italiana della regione
                label_query = f"""
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?label WHERE {{
                    <{regione_uri}> rdfs:label ?label .
                    FILTER (langMatches(lang(?label), "it"))
                }}
                LIMIT 1
                """
                dbpedia_sparql.setQuery(label_query)
                dbpedia_sparql.setReturnFormat(JSON)
                label_res = dbpedia_sparql.query().convert()
                bindings = label_res.get("results", {}).get("bindings", [])

                if bindings:
                    luogo_regioni[luogo] = bindings[0]["label"]["value"]
                else:
                    luogo_regioni[luogo] = regione_uri.split("/")[-1].replace("_", " ")
            else:
                luogo_regioni[luogo] = "Sconosciuto"

        except Exception as e:
            print(f"Errore DBpedia per {luogo}: {e}")
            luogo_regioni[luogo] = "Sconosciuto"

    for vino, dati in vini_map.items():
        vino_elem = etree.SubElement(root, "Vino", nome=vino)
        for tag in ["Tipologie", "Denominazioni", "Descrizioni", "ValoriMinimi", "ValoriMassimi", "MateriePrime"]:
            elementi = dati[tag]
            if elementi:
                elem = etree.SubElement(vino_elem, tag)
                elem.text = ", ".join(sorted(elementi))

        if dati["Luoghi"]:
            luoghi_elem = etree.SubElement(vino_elem, "Luoghi")
            regioni_locali = {}

            for l in dati["Luoghi"]:
                regione = luogo_regioni.get(l, "Sconosciuto")
                nome_luogo = l.split("/")[-1].replace("_", " ")
                is_provincia = "Province_of" in l

                if regione not in regioni_locali:
                    regioni_locali[regione] = {}

                if is_provincia:
                    provincia_corrente = nome_luogo
                    if provincia_corrente not in regioni_locali[regione]:
                        regioni_locali[regione][provincia_corrente] = set()
                else:
                    provincia_uri = get_provincia_from_dbpedia(l)
                    if provincia_uri:
                        provincia_nome = provincia_uri.split("/")[-1].replace("_", " ")
                    else:
                        provincia_nome = "Sconosciuta"
                    if provincia_nome not in regioni_locali[regione]:
                        regioni_locali[regione][provincia_nome] = set()
                    regioni_locali[regione][provincia_nome].add(nome_luogo)

            for regione, province in sorted(regioni_locali.items()):
                regione_elem = etree.SubElement(luoghi_elem, "Regione", nome=regione)
                for provincia, citta in sorted(province.items()):
                    provincia_elem = etree.SubElement(regione_elem, "Provincia", nome=provincia)
                    for nome_citta in sorted(citta):
                        etree.SubElement(provincia_elem, "Città", nome=nome_citta)

    xml_bytes = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    with open("vini.xml", "wb") as f:
        f.write(xml_bytes)

    print("✅ File vini.xml salvato con successo!")

except Exception as e:
    print(f"❌ Errore durante l'esecuzione: {e}")