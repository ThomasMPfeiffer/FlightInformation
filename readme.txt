Django Website zur Fluginformation
Aufsetzen:
1) Repository auf ein lokales Laufwerk clonen
2) Flightinformation.sln öffnen (öffnet das Projekt in Visual Studio)
3) Im Projektmappen-Explorer den Ordner Python-Umgebungen aufklappen
3) Rechtsklick auf Python 3.8 und "aus requirements.txt installieren" auswählen. Dies installiert die benötigte Pythonumgebung
4) CMD Öffnen und zum ablageordner des Projekts wechseln. Den Unteronterordner "FlightInformation" öffnen
5) Befehl "python manage.py runserver" aufrufen. Dies startet den Server (normalerweise auf Port 8000) ggf muss ein anderer Port zum starten verwendet werden.
6) Browser öffnen und die Webseite unter localhost:8000 aufrufen

Alternativ zu den Schritten 4)-6) kann die Webseite auch über Visual Studio gestartet werden.

Einrichten der eigenen Amadeus-API
1) FlightInformation\app\views.py öffnen
2) Zeile 17ff unter 'client_id' den API-Key eintragen; unter 'client_secret' das Secret eintragen

Hinweis: Das Projekt kann nur aus Visual Studio gestartet werden, wenn in FlightInformation\FlightInformation\settings.py in Zeile 27 DEBUG = True ist
         Aktuell ist in Zeile 31 nur der localhost als host erlaubt. Soll ein weiterer Host hinzugefügt werden, so kann das hier gemacht werden.
