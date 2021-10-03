<h1>Projectdocument - NS-Zuil</h1>

<ul>
  <li>Jimmy Bierenbroodspot</li>
  <li>1804439</li>
  <li>01/10/2021</li>
</ul>

<h2 name="index">Inhoudsopgave</h1>

<ul>
  <li>
    <a href="#chap_1">1. Inleiding</a>
    <ul>
      <li><a href="#chap_1_1">1.1 Aanleiding</a></li>
      <li><a href="#chap_1_2">1.2 Doelstelling</a></li>
      <li><a href="#chap_1_3">1.3 Opzet</a></li>
      <li><a href="#chap_1_4">1.4 *Doelgroep</a></li>
      <li><a href="#chap_1_5">1.5 *Leeswijzer</a></li>
    </ul>
  </li>
  <li>
    <a href="#chap_2">2. Functionaliteit</a>
    <ul>
      <li><a href="#chap_2_1">2.1 Module 1: Computerzuil</a></li>
      <li><a href="#chap_2_2">2.2 Module 2: Moderatie</a></li>
      <li><a href="#chap_2_3">2.3 Module 3: Scherm</a></li>
    </ul>
  <li>
    <a href="#chap_3">3. Gedrag</a>
    <ul>
      <li><a href="#chap_3_1">3.1 BPMN</a></li>
      <li><a href="#chap_3_2">3.2 Use case</a></li>
      <li><a href="#chap_3_3">3.3 Actor beschrijvingen</a></li>
      <li>
        <a href="#chap_3_4">3.4 Use case beschrijvingen</a>
        <ul>
          <li><a href="#chap_3_4_1">3.4.1 Proj a 01</a></li>
          <li><a href="#chap_3_4_2">3.4.2 Proj a 02</a></li>
          <li><a href="#chap_3_4_3">3.4.3 Proj a 03</a></li>
          <li><a href="#chap_3_4_4">3.4.4 Proj a 04</a></li>
          <li><a href="#chap_3_4_5">3.4.5 Proj a 05</a></li>
        </ul>
      </li>
    </ul>
  </li>
  <li>
    <a href="#chap_4">4. Datamodel</a>
    <ul>
      <li><a href="#chap_4_1">4.1 Conceptueel datamodel</a></li>
      <li><a href="#chap_4_2">4.2 Logisch datamodel</a></li>
      <li><a href="#chap_4_3">4.3 Fysiek datamodel</a></li>
    </ul>
  </li>
</ul>

<h2 name="chap_1">1. Inleiding</h2>

<h3 name="chap_1_1">1.1 Aanleiding</h3>

<h3 name="chap_1_2">1.2 Doelstelling</h3>

<h3 name="chap_1_3">1.3 Opzet<h3>

<h3 name="chap_1_4">1.4 *Doelgroep</h3>

<h3 name="chap_1_5">1.5 *Leeswijzer</h3>

<a href="#index">Terug naar inhoudsopgave...</a>

<h2 name="chap_2">2. Functionaliteit</h2>

<p>Het systeem bestaat uit drie modules: computerzuil, moderatie, scherm. Deze modules zullen samenwerken samen met de API
van Twitter om ervoor te zorgen dat reizigers in de vorm van een tweet hun mening op een scherm op een NS-station kunnen
delen. Hiervoor zijn wat ICT-voorzieningen nodig: Een computerzuil voor het invoeren van berichten, een computer voor
het modereren van berichten, een database, internetverbinding en een scherm voor het weergeven van de Tweets. Hieronder
zal er per module beschreven worden wat ze doen.</p>

<h3 name="chap_2_1">2.1 Module 1: Computerzuil</h3>

De computerzuil staat op een station van NS. Dit is in de vorm van een webpagina die intern op de zuil bereikbaar is er
wordt geacht dat de gebruiker die niet kan aanpassen: scherm verkleinen, scherm sluiten of url aanpassen. Op deze pagina
zijn velden voor de volgende gegevens: voornaam, achternaam, tussenvoegsel en bericht. Alle velden behalve bericht zijn
optioneel. Het bericht kan maximaal 140 karakters lang zijn. Als alle gewenste gegevens zijn ingevuld kan er op
versturen gedrukt worden. Het bericht wordt opgeslagen in een database samen met het station waar de zuil zich bevindt
en is klaar om gemodereerd te worden.

<h3 name="chap_2_2">2.2 Module 2: Moderatie</h3>

<p>Het modereren begint als een moderator inlogt. De moderator krijgt dan een enkel bericht te zien en kan dan kiezen voor
accepteren of weigeren. Als de moderator kiest voor accepteren wordt het bericht met de status ‘geaccepteerd’ in de
database te staan. Als de moderator kiest voor weigeren komt het bericht met de status ‘geweigerd’ in de database te
staan. Naast de status wordt ook de moderator en tijd van moderatie aan het bericht gekoppeld. Als een bericht
geaccepteerd is wordt die met behulp van de twitter API getweet.</p>

<h3 name="chap_2_3">2.3 Module 3: Scherm</h3>

<p>Het scherm is een scherm op een NS-station waar de tweets die in module 2 getweet zijn op worden weergeven. Een aantal
van de meest recente tweets worden weergeven met eventuele naam. Als er een tijd geen tweets zijn gepost wordt het
weerbericht voor de plaats van het station weergeven.</p>

<a href="#index">Terug naar inhoudsopgave...</a>

<h2 name="chap_3">3. Gedrag</h2>

<h3 name="chap_3_1">3.1 BPMN</h3>

![BPMN diagram][bpmn]

<h3 name="chap_3_2">3.2 Use case</h3>

Hieronder zie je een use case diagram met één systeem en twee actoren: Klan ten Moderator. Klant heeft een use case
waarin diegene een bericht kan schrijven. Voor een moderator om iets te doen moet diegene eerst inloggen. Vervolgens kan
de moderator ervoor kiezen om het overzicht met geweigerde berichten te bekijken. Ook kan de moderator berichten
accepteren en weigeren. Hiervoor moet de use case van de actor klant wel uitgevoerd zijn.
![Use case diagram][ucd]

<h3 name="chap_3_3">3.3 Actor beschrijvingen</h3>

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

<h3 name="chap_3_4">3.4 Use case beschrijvingen</h3>

<h4 name="chap_3_4_1">3.4.1 Proj a 01</h4>

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

<h4 name="chap_3_4_2">3.4.2 Proj a 02</h4>

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

<h4 name="chap_3_4_3">3.4.3 Proj a 03</h4>

<table>
  <body>
    <tr>
      <td><strong>ID</strong></td>
      <td><strong>PROJ_A_03 V0.1</strong></td>
    </tr>
    <tr>
      <td>Naam</td>
      <td>Bericht accepteren</td>
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
      <td>Precondities</td>
      <td>
        <ol> 
          <li>Actor is ingelogd.</li>
          <li>Er zijn berichten beschikbaar.</li>
        </ol>
      </td>
    </tr>
    <tr>
      <td>Samenvatting</td>
      <td>Systeem weergeeft een enkel bericht en actor kiest accepteren (i). Systeem Weergeeft bericht op scherm (o).</td>
    </tr>
    <tr>
      <td>Scenario</td>
      <td>
        <ul>
          <li>1. Systeem weergeeft één bericht.</li>
          <li>2. Actor k1.	Bericht wordt weergeven.iest accepteren.</li>
          <li>3. Systeem markeert bericht als geaccepteerd in database.</li>
          <li>4. Systeem weergeeft bericht op scherm (Postconditie 1).</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Postcondities</td>
      <td>
        <ol>
          <li>Bericht wordt weergeven.</li>
        </ol>
      </td>
    </tr>
  </body>
</table>

<h4 name="chap_3_4_4">3.4.4 Proj a 04</h4>

<table>
  <body>
    <tr>
      <td><strong>ID</strong></td>
      <td><strong>PROJ_A_04 V0.1</strong></td>
    </tr>
    <tr>
      <td>Naam</td>
      <td>Bericht weigeren</td>
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
      <td>Precondities</td>
      <td>
        <ol> 
          <li>Actor is ingelogd.</li>
          <li>Er zijn berichten beschikbaar.</li>
        </ol>
      </td>
    </tr>
    <tr>
      <td>Samenvatting</td>
      <td>Systeem weergeeft een enkel bericht en actor kiest weigeren (i). Systeem markeert bericht als geweigerd in database (o).</td>
    </tr>
    <tr>
      <td>Scenario</td>
      <td>
        <ul>
          <li>1. Systeem weergeeft een enkel bericht.</li>
          <li>2. Actor kies weigeren.</li>
          <li>3. Systeem markeert bericht als geweigerd in database (Postconditie 1).</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Postcondities</td>
      <td>
        <ol>
          <li>Bericht is gemarkeerd als geweigerd.</li>
        </ol>
      </td>
    </tr>
  </body>
</table>

<h4 name="chap_3_4_5">3.4.5 Proj a 05</h4>

<table>
  <body>
    <tr>
      <td><strong>ID</strong></td>
      <td><strong>PROJ_A_05 V0.1</strong></td>
    </tr>
    <tr>
      <td>Naam</td>
      <td>Overzicht bekijken</td>
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
      <td>Precondities</td>
      <td>
        <ol> 
          <li>Actor is ingelogd.</li>
        </ol>
      </td>
    </tr>
    <tr>
      <td>Samenvatting</td>
      <td>Systeem wacht het openen van het overzicht (i). Systeem weergeeft geweigerde berichten (o).</td>
    </tr>
    <tr>
      <td>Scenario</td>
      <td>
        <ul>
          <li>1.	Systeem wacht op openen van overzicht.</li>
          <li>2.	Actor kiest voor het openen van overzicht.</li>
          <li>3.	Systeem weergeeft berichten gemarkeerd als geweigerd (Postconditie 1).</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Postcondities</td>
      <td>
        <ol>
          <li>Overzicht wordt weergeven.</li>
        </ol>
      </td>
    </tr>
  </body>
</table>

<a href="#index">Terug naar inhoudsopgave...</a>

<h2 name="chap_4">4. Datamodel</h2>

<h3 name="chap_4_1">4.1 Conceptueel datamodel</h3>

![Conceptuele ERD][erd_conc]

<table>
  <thead>
    <tr>
      <td><strong>Entiteit</strong></td>
      <td><strong>Beschrijving</strong></td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Station</td>
      <td>Het station is waar basisinformatie over het station waar de zuil staat wordt weergeven. Elk station krijgt een id voor simpele identificatie en een naam om te weergeven.</td>
    </tr>
    <tr>
      <td>Message</td>
      <td>In message wordt alle informatie over het bericht dat de gebruiker schrijft opgeslagen. Ook wordt er bijgehouden wat de status is van het bericht (of het geaccepteerd is of niet) en wanneer het gemodereerd is.</td>
    </tr>
    <tr>
      <td>User</td>
      <td>User is eigenlijk alleen maar een account voor een moderator om ervoor te zorgen dat niet iedereen zomaar berichten kan modereren.</td>
    </tr>
  </tbody>
</table>

<h3 name="chap_4_2">4.2 Logisch datamodel</h3>

![Logisch datamodel][erd_logic]

<h3 name="chap_4_3">4.3 Fysiek datamodel</h3>

![Fysiek datamodel][erd_phys]

<a href="#index">Terug naar inhoudsopgave...</a>

[bpmn]: https://github.com/JBierenbroodspot/PROJA/blob/doc/doc/models/ns_zuil_BPMN.png?raw=true "BMPN model showing the process of the application"

[ucd]: https://github.com/JBierenbroodspot/PROJA/blob/doc/doc/models/ns_zuil_UC.png?raw=True "Use case diagram showing actors and their actions"

[erd_conc]: https://github.com/JBierenbroodspot/PROJA/blob/doc/doc/models/ns_zuil_erd_conceptueel.png?raw=true "Conceptual ERD"

[erd_logic]: https://github.com/JBierenbroodspot/PROJA/blob/doc/doc/models/ns_zuil_erd_logisch.png?raw=true "Logical ERD"

[erd_phys]: https://github.com/JBierenbroodspot/PROJA/blob/doc/doc/models/ns_zuil_erd_fysiek.png?raw=true "Physical ERD"