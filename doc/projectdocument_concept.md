<h1>Projectdocument - NS-Zuil</h1>

<ul>
  <li>Jimmy Bierenbroodspot</li>
  <li>1804439</li>
  <li>01/10/2021</li>
</ul>

<h2>Inhoudsopgave</h1>

<ul>
  <li>
    Inleiding
    <ul>
      <li>Aanleiding</li>
      <li>Doelstelling</li>
      <li>Opzet</li>
      <li>*Doelgroep</li>
      <li>*Leeswijzer</li>
    </ul>
  </li>
  <li>
    Functionaliteit
    <ul>
      <li>Module 1: Computerzuil</li>
      <li>Module 2: Moderatie</li>
      <li>Module 3: Scherm</li>
    </ul>
  <li>
    Gedrag
    <ul>
      <li>BPMN</li>
      <li>Use case</li>
      <li>Actor beschrijvingen</li>
      <li>
        Use case beschrijvingen
        <ul>
          <li>Proj a 01</li>
          <li>Proj a 02</li>
          <li>Proj a 03</li>
          <li>Proj a 04</li>
          <li>Proj a 05</li>
        </ul>
      </li>
    </ul>
  </li>
</ul>

<h2>Inleiding</h2>

<h3>Aanleiding</h3>

<h3>Doelstelling</h3>

<h3>Opzet<h3>

<h3>*Doelgroep</h3>

<h3>*Leeswijzer</h3>

<h2>Functionaliteit</h2>

<p>Het systeem bestaat uit drie modules: computerzuil, moderatie, scherm. Deze modules zullen samenwerken samen met de API
van Twitter om ervoor te zorgen dat reizigers in de vorm van een tweet hun mening op een scherm op een NS-station kunnen
delen. Hiervoor zijn wat ICT-voorzieningen nodig: Een computerzuil voor het invoeren van berichten, een computer voor
het modereren van berichten, een database, internetverbinding en een scherm voor het weergeven van de Tweets. Hieronder
zal er per module beschreven worden wat ze doen.</p>

<h3>Module 1: Computerzuil</h3>

De computerzuil staat op een station van NS. Dit is in de vorm van een webpagina die intern op de zuil bereikbaar is er
wordt geacht dat de gebruiker die niet kan aanpassen: scherm verkleinen, scherm sluiten of url aanpassen. Op deze pagina
zijn velden voor de volgende gegevens: voornaam, achternaam, tussenvoegsel en bericht. Alle velden behalve bericht zijn
optioneel. Het bericht kan maximaal 140 karakters lang zijn. Als alle gewenste gegevens zijn ingevuld kan er op
versturen gedrukt worden. Het bericht wordt opgeslagen in een database samen met het station waar de zuil zich bevindt
en is klaar om gemodereerd te worden.

<h3>Module 2: Moderatie</h3>

<p>Het modereren begint als een moderator inlogt. De moderator krijgt dan een enkel bericht te zien en kan dan kiezen voor
accepteren of weigeren. Als de moderator kiest voor accepteren wordt het bericht met de status ‘geaccepteerd’ in de
database te staan. Als de moderator kiest voor weigeren komt het bericht met de status ‘geweigerd’ in de database te
staan. Naast de status wordt ook de moderator en tijd van moderatie aan het bericht gekoppeld. Als een bericht
geaccepteerd is wordt die met behulp van de twitter API getweet.</p>

<h3>Module 3: Scherm</h3>

<p>Het scherm is een scherm op een NS-station waar de tweets die in module 2 getweet zijn op worden weergeven. Een aantal
van de meest recente tweets worden weergeven met eventuele naam. Als er een tijd geen tweets zijn gepost wordt het
weerbericht voor de plaats van het station weergeven.</p>

<h2>Gedrag</h2>

<h3>BPMN</h3>

![BPMN diagram][bpmn]

<h3>Use case</h3>

Hieronder zie je een use case diagram met één systeem en twee actoren: Klan ten Moderator. Klant heeft een use case
waarin diegene een bericht kan schrijven. Voor een moderator om iets te doen moet diegene eerst inloggen. Vervolgens kan
de moderator ervoor kiezen om het overzicht met geweigerde berichten te bekijken. Ook kan de moderator berichten
accepteren en weigeren. Hiervoor moet de use case van de actor klant wel uitgevoerd zijn.
![Use case diagram][ucd]

<h3>Actor beschrijvingen</h3>

<table>
  <thead>
    <tr>
      <td>Actor naam</td>
      <td>Beschrijving</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Klant</td>
      <td>De klant is een reiziger die zich begeeft op een NS-station. Als de klant besluit een mening te uiten over NS kan de klant dat met het programma doen. De klant kan dan een bericht van 140 karakters invoeren. Ook kan de klant ervoor kiezen om een voornaam, tussenvoegsel en achternaam mee te geven. De klant kan zijn of haar tweet bekijken op een scherm.</td>
    </tr>
    <tr>
      <td>Moderator</td>
      <td>De moderator is iemand die onder opdracht van NS werkt. De moderator heeft een unieke inlognaam en wachtwoord die diegene kan gebruiken om in te loggen. Dee moderator kan ervoor kiezen om berichten te weigeren of accepteren. De moderator kan ook besluiten een overzicht van de geweigerde berichten te bekijken. Het doel van de moderator is om berichten een voor een te modereren tot er geen berichten meer zijn. De goedgekeurde berichten worden weergeven als tweet op een scherm.</td>
    </tr>
  </tbody>
</table> 

<h3>Use case beschrijvingen</h3>

<h4>Proj a 01</h4>

<table>
  <body>
    <tr>
      <td><strong>ID</strong></td>
      <td><strong>PROJ_A_01 V0.1</strong></td>
    </tr>
    <tr>
      <td>Naam</td>
      <td>Bericht schrijven</td>
    </tr>
    <tr>
      <td>Actoren</td>
      <td>
        <ul>
          <li>Klant</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Samenvatting</td>
      <td>Systeem wacht op klant om een bericht van <= 140 karakters en hun naam in te voeren (i). Systeem slaat bericht vervolgens op in database (o).</td>
    </tr>
    <tr>
      <td>Scenario</td>
      <td>
        <ul>
          <li>1. Systeem wacht op invoer van bericht.</li>
          <li>2. Klant voert bericht in.</li>
          <li>
            3. Als bericht > 140.
            <ul>
              <li>3.1 Systeem geeft foutmelding (Postconditie 2).</li>
            </ul>
          </li>
          <li>
            4. Als klant naam invoert.
            <ul>
              <li>4.1 Systeem slaat bericht, naam en datum op in de database (Postconditie 1).</li>
            </ul>
          </li>
          <li>
            5. Anders.
            <ul>
              <li>5.1	Systeem slaat bericht en datum op in systeem (Postconditie 1).</li>
            </ul>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Postcondities</td>
      <td>
        <ol>
          <li>Bericht is opgeslagen in database.</li>
          <li>Er gebeurt niks.</li>
        </ol>
      </td>
    </tr>
  </body>
</table>

<h4>Proj a 02</h4>

<table>
  <body>
    <tr>
      <td><strong>ID</strong></td>
      <td><strong>PROJ_A_02 V0.1</strong></td>
    </tr>
    <tr>
      <td>Naam</td>
      <td>Inloggen</td>
    </tr>
    <tr>
      <td>Actoren</td>
      <td>
        <ul>
          <li>Moderator</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Samenvatting</td>
      <td>Systeem wacht op gebruikersnaam (i) en wachtwoord (i) en valideert die dan tegen de database. Actor kan nu berichten modereren (o).</td>
    </tr>
    <tr>
      <td>Scenario</td>
      <td>
        <ul>
          <li>1. Systeem wacht op invoer van gebruikersnaam en wachtwoord.</li>
          <li>2. Actor verstrekt deze gegevens.</li>
          <li>
            3. Als gebruikersnaam ontbreekt.
            <ul>
              <li>3.1 Systeem geeft foutmelding (Postconditie 2).</li>
            </ul>
          </li>
          <li>
            4. Als wachtwoord ontbreekt.
            <ul>
              <li>4.1 Systeem geeft foutmelding (Postconditie 2).</li>
            </ul>
          </li>
          <li>
            5. Als gebruikersnaam en wachtwoord correct is.
            <ul>
              <li></li>
            </ul>
          </li>
          <li>
            6. Anders.
            <ul>
              <li>6.1 Systeem geeft foutmelding (Postconditie 2).</li>
            </ul>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Postcondities</td>
      <td>
        <ol>
          <li>Actor is ingelogd.</li>
          <li>Er gebeurt niks.</li>
        </ol>
      </td>
    </tr>
  </body>
</table>

<h4>Proj a 03</h4>

<table>
  <body>
    <tr>
      <td><strong>ID</strong></td>
      <td><strong>PROJ_A_01 V0.1</strong></td>
    </tr>
    <tr>
      <td>Naam</td>
      <td>Bericht schrijven</td>
    </tr>
    <tr>
      <td>Actoren</td>
      <td>
        <ul>
          <li>Klant</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Samenvatting</td>
      <td></td>
    </tr>
    <tr>
      <td>Scenario</td>
      <td></td>
    </tr>
    <tr>
      <td>Postcondities</td>
      <td></td>
    </tr>
  </body>
</table>

<h4>Proj a 04</h4>

<table>
  <body>
    <tr>
      <td><strong>ID</strong></td>
      <td><strong>PROJ_A_01 V0.1</strong></td>
    </tr>
    <tr>
      <td>Naam</td>
      <td>Bericht schrijven</td>
    </tr>
    <tr>
      <td>Actoren</td>
      <td>
        <ul>
          <li>Klant</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Samenvatting</td>
      <td></td>
    </tr>
    <tr>
      <td>Scenario</td>
      <td></td>
    </tr>
    <tr>
      <td>Postcondities</td>
      <td></td>
    </tr>
  </body>
</table>

<h4>Proj a 05</h4>

<table>
  <body>
    <tr>
      <td><strong>ID</strong></td>
      <td><strong>PROJ_A_01 V0.1</strong></td>
    </tr>
    <tr>
      <td>Naam</td>
      <td>Bericht schrijven</td>
    </tr>
    <tr>
      <td>Actoren</td>
      <td>
        <ul>
          <li>Klant</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Samenvatting</td>
      <td></td>
    </tr>
    <tr>
      <td>Scenario</td>
      <td></td>
    </tr>
    <tr>
      <td>Postcondities</td>
      <td></td>
    </tr>
  </body>
</table>

[bpmn]: https://github.com/JBierenbroodspot/PROJA/blob/doc/doc/models/ns_zuil_BPMN.png?raw=true "BMPN model showing the process of the application"

[ucd]: https://github.com/JBierenbroodspot/PROJA/blob/doc/doc/models/ns_zuil_UC.png?raw=True "Use case diagram showing actors and their actions"