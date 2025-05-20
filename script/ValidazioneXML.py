from lxml import etree
#SU PC RZ
dtd_filename = "../dati/DTD_ViniXML.dtd"
xml_filename = "../dati/vini.xml"

dtd_file = open(dtd_filename, 'r')
# Controlla se il file DTD esiste
if dtd_file:
    print("File DTD aperto correttamente")
else:
    print("File DTD non trovato")
# Controlla se il file XML esiste
if xml_filename:
    print("File XML aperto correttamente")  
else:
    print("File XML non trovato")

xml_file = open(xml_filename, 'r')

xml_root = etree.parse(xml_filename)


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