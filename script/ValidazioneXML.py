from lxml import etree
#SU PC RZ
dtd_filename = "../dati/DTD_ViniXML.dtd"
xml_filename = "../dati/vini.xml"

# Imposta il percorso del file DTD e XML
try:
    dtd_file = open(dtd_filename, 'r',encoding='utf-8')
except FileNotFoundError:
    dtd_file = None
    print("File DTD non trovato, assicurati che il percorso sia corretto.")

try:
    xml_file = open(xml_filename, 'r', encoding='utf-8')
    xml_root = etree.parse(xml_filename)
except FileNotFoundError:
    xml_file = None
    print("File XML non trovato, assicurati che il percorso sia corretto.")

try:
    # Carica DTD se sintatticamente corretto
    # oppure solleva un'eccezione
    dtd = etree.DTD(dtd_file)

    # Valida rispetto al DTD e restituisce un booleano
    if dtd.validate(xml_root):
        print("Valid XML!")
    else:
        # Recupera l'errore di validazione dai log
        validation_error = dtd.error_log.filter_from_errors()[0]
        print("XML not valid!\n", validation_error)
except:
  print("DTD non corretto")