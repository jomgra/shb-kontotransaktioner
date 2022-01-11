# shb-kontotransaktioner

En samling små python3-program som importerar kontotransaktioner från Handelsbankens excel-exporter och för in dessa i en SQLite-databas. Importen tar hänsyn till om excel-exporterna innehåller dubbletter, det vill säga om samma transaktion redan importerats från en annan exportfil. I dessa fall importeras inte dubbletten. Handelsbanken möjliggör endast export av transaktioner två år tillbaka i tiden. Genom detta program kan längre tidsperioder sammanfogas utan överlappningar.

Med transaktionerna i SQLite-databasen kan uppgifter sedan bearbetas och exporteras ut.

**Installation**

1. Ladda ner importer.py och lägg en i valfri katalog.
2. Plaecera dina xls-exporter i samma katalog eller redigera py-filen med rätt sökväg ("path").
3. Kör importer.py!

Du ska nu ha en SQLite-databas i samma katalog som filerna!
