# Getraenkeautomat Frontend

Dieses Git-Repository enthält das Frontend für eine Getränkemaschine, welches mit Angular und Bootstrap umgesetzt wurde.

Die Anwendung besteht aus zwei Hauptbereichen: der Bestellungsseite und der Verwaltungsseite.

Das Frontend ermöglicht es Benutzern, vorgefertigte oder selbst gemischte Getränke von der Maschine zu bestellen und vorgefertigte Getränke oder Getränkemaschinen zu verwalten.

Die Kommunikation mit dem Backend erfolgt über MQTT im JSON-Format.

Dieses Projekt wurde mit [Angular CLI](https://github.com/angular/angular-cli) Version 15.2.0 erstellt.

## Dokumentation

Dateien zugehörend zur detaillierten Dokumentation sind unter [dokumentation](dokumentation/) gespeichert.

## Vorraussetzungen

* [npm CLI](https://docs.npmjs.com/cli/v9/)
* [Node.js](https://nodejs.org/)
* [Angular CLI](https://github.com/angular/angular-cli)

Eine funktionierende MQTT-Verbindung zum Backend ist erforderlich.


## Installation

Klone das Git-Repository auf deinen Computer mit `git clone git@git.thm.de:swtp_ebner_wise23_getraenkemaschine/getraenkeautomat-frontend.git`.

Öffne ein Terminal und navigiere zum Verzeichnis der App.

Installiere die Abhängigkeiten, indem du `npm install` ausführst.

## Starten des Webservers

Führen Sie `npm start` oder `ng serve` im Verzeichnis der App aus.

Navigieren Sie zu `http://localhost:4200/` um das Frontend aufzurufen.

Die Anwendung wird automatisch neu geladen, wenn Sie eine der Quelldateien ändern.

## Bauen

Führen Sie `ng build` aus, um das Projekt zu bauen. 
Die Build-Artefakte werden im Verzeichnis `dist/` gespeichert.

Für die Produktion kann mit dem Befehl `ng build --prod` gebaut werden. 
Dabei wird eine optimierte Version der App erstellt, die für den Einsatz in der Produktion geeignet ist.

## Code-Gerüst

Führen Sie `ng generate component component-name` aus, um eine neue Komponente zu erzeugen.

Sie können auch `ng generate directive|pipe|service|class|guard|interface|enum|module` verwenden.

## Unit-Tests ausführen

Führen Sie `ng test` aus, um die Unit-Tests über [Karma](https://karma-runner.github.io) auszuführen.

## Ausführen von End-to-End-Tests

Führen Sie `ng e2e` aus, um die End-to-End-Tests über eine Plattform Ihrer Wahl auszuführen. Um diesen Befehl zu verwenden, müssen Sie zunächst ein Paket hinzufügen, das End-to-End-Tests implementiert.

## Kommunikation zum Backend

Die Kommunikation zum Backend erfolgt mittels MQTT im json Format. Die genauen Spezifikationen der Nachrichten werden in einem separaten Dokument unter [dokumentation](dokumentation/) beschrieben.

## Hinweise zur Entwicklung für Mitwirkende

Änderungen am Code sollten in separaten Branches durchgeführt werden und über Pull Requests in den master-Branch gemerged werden.

Bitte achte auf eine einheitliche Codestruktur und -formatierung, um die Lesbarkeit und Wartbarkeit des Codes zu verbessern.

Es empfiehlt sich, Unit-Tests für neue Funktionen oder Änderungen zu schreiben.

## Weitere Hilfe

Um weitere Hilfe zur Angular CLI zu erhalten, verwenden Sie `ng help` oder schauen Sie sich die Seite [Angular CLI Overview and Command Reference](https://angular.io/cli) an.

## License
Dieses Projekt ist unter der MIT-Lizenz lizenziert.

## Autoren

Dieses Projekt wurde von [Amine Bouchrit](https://git.thm.de/abrt93), [Beyza Duman](https://git.thm.de/bdmn20) und [Brian Runck](https://git.thm.de/brnk73) erstellt.







