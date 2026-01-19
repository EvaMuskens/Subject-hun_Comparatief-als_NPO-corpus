# Subject-hun_Comparatief-als_NPO-corpus
Code om NPO Start-audio te downloaden en vanuit (met ASR-geproduceerde) tekst-files constructies als 'hun hebben' en 'groter als' te extraheren.

Met afleveringen.py worden de URL's van afleveringen van specifiek geselecteerde NPO-programma's gemaakt en opgeslagen in een csv. Let op: NPO Start is een interactieve website, dus bij de kleinste aanpassingen aan de NPO-kant werkt het scrapen niet meer. De code zal ongetwijfeld aangepast moeten worden om het weer werkend te krijgen. afleveringen.py is gemaakt door Olaf van Waart.

De afleveringen-URL's worden aan DL.py gevoerd, die een uitstapje maakt naar NPO.py voor specifieke NPO Start-features. DL.py leest de URL's en genereert audiobestanden in mp4-format. DL.py en NPO.py zijn gebaseerd op de code van adef17286-sudo: https://github.com/adef17286-sudo/NPO_start_DL. De codes zijn aangepast voor generiek Python-gebruik door Olaf van Waart.

Middels Amberscript zijn de audiobestanden in tekstbestanden omgezet. Deze stap is niet in de repository opgenomen.

In subjecten_comparatieven_extractie.py worden de tekstbestanden ingelezen en wordt de totale frequentie verzameld van 'zij'/'ze'/'hun' als persoonlijk voornaamwoord derde persoon meervoud subject, en van alle comparatieven van ongelijkheid met 'als' dan wel 'dan', gebruikmakend van spaCy.

DISCLAIMER: Enkel voor onderzoeksdoeleinden. Ik stel mezelf niet verantwoordelijk voor het downloaden en gebruiken van NPO-materiaal. 
