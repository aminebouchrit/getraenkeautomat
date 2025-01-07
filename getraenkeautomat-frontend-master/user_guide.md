Benutzerhandbuch für die Getränkebestellungsanwendung:

Das Projekt umfasst eine grafische Endanwendung, die dem Nutzer ermöglicht, Getränke zu bestellen und die Maschine zu verwalten. 
Die einzelnen Oberflächen sind in verschiedenen Angular-Komponenten unterteilt.
Die Anwendung besteht aus verschiedenen Komponenten, darunter:

Die App-Komponente ist die zentrale Steuerungseinheit der gesamten Anwendung und ermöglicht dem Benutzer den Zugriff auf alle anderen Komponenten und Funktionen, einschließlich der Getränkebestellung, der Maschinenverwaltung, der Erstellung eigener Getränke, der Warenkorbverwaltung, der Bewertung von Rezepten und mehr.
-Information: Diese Komponente stellt dem Nutzer Informationen über die angebotenen Getränke zur Verfügung, wie z.B. Kategorien und Inhaltsstoffe.
-Home: Hier kann der Nutzer auf die verschiedenen Funktionen der Anwendung zugreifen, z.B. Bestellung, Verwaltung und Bewertung von Getränken.
-Management: Diese Komponente bietet dem Nutzer die Möglichkeit, die Maschine zu verwalten und relevante Assets zu verwalten, z.B. die Verfügbarkeit von Getränken und Zubehör.
-Maschinen-Auswahl: Der Nutzer kann hier die Maschine auswählen, von der er Getränke bestellen möchte.
-Mixed Drink: Hier kann der Nutzer eigene Getränke kreieren und diese wie normale Listengetränke bestellen.
-Order: Hier kann der Nutzer die Getränke bestellen, indem er sie auswählt und dem Warenkorb hinzufügt.
-Rating: Diese Komponente ermöglicht es dem Nutzer, Getränke zu bewerten, um anderen Nutzern bei der Auswahl des Getränks zu helfen.
-Service: Diese Komponente bietet dem Nutzer zusätzliche Informationen und Serviceleistungen, z.B. FAQs und Kontaktmöglichkeiten.
-Shopping Cart: Hier kann der Nutzer seine Bestellung überprüfen und den Bestellvorgang abschließen.
In der Datei "app-routing.module.ts" werden die Routen definiert, die die Navigation innerhalb der Anwendung ermöglichen. Hier wird auch der Zugriff auf die verschiedenen Komponenten über die "routerLink" Methode ermöglicht, indem die URL-Pfade den jeweiligen Komponenten zugewiesen werden.
