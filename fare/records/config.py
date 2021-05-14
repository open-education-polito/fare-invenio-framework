# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

import invenio_logging.config
import invenio_theme.config
from invenio_indexer.api import RecordIndexer
from invenio_records_rest.facets import terms_filter
from invenio_records_rest.utils import allow_all, check_elasticsearch, deny_all

from ..file_management.api import FILE_MNGT_PID_FETCHER, \
    FILE_MNGT_PID_MINTER, FILE_MNGT_PID_TYPE
from ..file_management.search import RevisionSearch
from .search import RevisionedRecordsSearch


def _(x):
    """Identity function for string extraction."""
    return x


invenio_logging.config.LOGGING_FS_LOGFILE = "/var/log/fare/log_fare.txt"
invenio_logging.config.LOGGING_FS_PYWARNINGS = True
invenio_theme.config.THEME_FOOTER_TEMPLATE = "fare/footer.html"

FARE_LICENSES = {
    "CC BY": {
        "yes": [
            "Creazione opere derivate",
            "Distribuire",
            "Attribuzione Richiesta",
            "Uso a scopo Commerciale"
        ],
        "no": []
    },
    "CC BY-SA": {
        "yes": [
            "Creazione opere derivate",
            "Distribuire",
            "Attribuzione richiesta",
            "Uso a scopo commerciale"
        ],
        "no": [
            "Cambiare licenza"
        ]
    },
    "CC BY-NC": {
        "yes": [
            "Creazione opere derivate",
            "Distribuire",
            "Attribuzione richiesta"
        ],
        "no": [
            "Uso a scopo commerciale"
        ]
    },
    "CC BY-ND": {
        "yes": [
            "Distribuire",
            "Attribuzione richiesta",
            "Uso a scopo commerciale"
        ],
        "no": [
            "Creazione opere derivate"
        ]
    },
    "CC BY-NC-SA": {
        "yes": [
            "Creazione opere derivate",
            "Distribuire",
            "Attribuzione richiesta"
        ],
        "no": [
            "Uso a scopo commerciale"
        ]
    },
    "CC BY-NC-ND": {
        "yes": [
            "Distribuire",
            "Attribuzione richiesta"
        ],
        "no": [
            "Creazione opere derivate",
            "Uso a scopo commerciale"
        ]
    }
}

EDUCATION_LEVEL = {
  "educationLevel": [
                      "Divulgazione",
                      "Scuola Ospedaliera",
                      "Scuola Primaria",
                      "Scuola Secondaria di primo grado",
                      "Scuola Secondaria di secondo grado",
                      "Università"
  ]
}

SUBJECTS = {
    "subject": [
        "Informatica",
        "Filosofia e psicologia",
        "Metafisica (filosofia speculativa)",
        "Epistemologia, causalita, genere umano",
        "Specifiche posizioni filosofiche",
        "Psicologia",
        "Logica",
        "Etica (filosofia morale)",
        "Filosofia antica, medievale, orientale",
        "Filosofia occidentale moderna",
        "Religione",
        "Scienze sociali",
        "Scienza politica (politica e governo)",
        "Economia",
        "Diritto",
        "Educazione",
        "Scienze del linguaggio",
        "Matematica",
        "Astronomia",
        "Fisica",
        "Chimica",
        "Scienze della terra",
        "Paleontologia  paleozoologia",
        "Scienze della vita",
        "Scienze botaniche",
        "Scienze zoologiche",
        "Scienze mediche  medicina",
        "Ingegneria e operazioni affini",
        "Tecnologie chimiche",
        "Urbanistica e arte del paesaggio",
        "Architettura",
        "Arti plastiche  scultura",
        "Disegno, arti decorative e minori",
        "Pittura",
        "Fotografia e fotografie",
        "Musica",
        "Arti ricreative e dello spettacolo",
        "Letteratura",
        "Storia",
        "Geografia generale",
        "Biografie",
    ]
}

ARGUMENTS = {
    "Informatica": [
        "Ricerca",
        "Cibernetica e discipline connesse",
        "Comunicazione",
        "Cibernetica",
        "Il libro",
        "Sistemi",
        "Elaborazione dei dati scienza degli elaboratori",
        "Opere generali su specifici tipi di elaboratori",
        "Microelaboratori digitali",
        "Analisi e progettazione dei sistemi, architettura dell'elaboratore",
        "Memorizzazione dei dati",
        "Interfacciamento e comunicazioni",
        "Unita periferiche",
        "Programmazione, programmi, dati",
        "Programmazione",
        "Linguaggi di programmazione",
        "Programmazione per specifici tipi di elaboratori",
        "Programmi",
        "Programmazione e programmi di sistema",
        "Microprogrammazione e microprogrammi",
        "Dati nei sistemi di elaboratori",
        "Archivi e basi di dati",
        "Sicurezza dei dati",
        "Metodi speciali di elaborazione",
        "Intelligenza artificiale",
        "Riconoscimento di forme (pattern recognition)",
        "Sintesi del suono con l'elaboratore",
        "Grafica con l'elaboratore"
    ],
    "Filosofia e psicologia": [
        "Filosofia. teoria",
        "Filosofia. miscellanea",
        "Filosofia. dizionari, enciclopedie, concordanze",
        "Filosofia. pubblicazioni in serie",
        "Filosofia. organizzazioni",
        "Filosofia. studio e insegnamento",
        "Filosofia. trattamento del soggetto \
        in riferimento a gruppi di persone",
        "Filosofia. trattamento storico"
    ],
    "Metafisica (filosofia speculativa)": [
        "Ontologia",
        "Cosmologia (filosofia della natura)",
        "Spazio",
        "Tempo",
        "Evoluzione",
        "Struttura",
        "Forza ed energia",
        "Numero e quantita"
    ],
    "Epistemologia, causalita, genere umano": [
        "Epistemologia (teoria della conoscenza)",
        "Causalita",
        "Determinismo e indeterminismo",
        "L'inconscio e il subconscio",
        "Genere umano",
        "Origine e destino dell'anima individuale"
    ],
    "Specifiche posizioni filosofiche": [
        "Idealismo e sistemi e dottrine connessi",
        "Filosofia critica",
        "Intuizionismo e bergsonismo",
        "Umanismo e sistemi e dottrine connessi",
        "Sensismo e ideologia",
        "Naturalismo e sistemi e dottrine connessi",
        "Panteismo e sistemi e dottrine connessi",
        "Liberalismo, eclettismo, sincretismo, tradizionalismo, dogmatismo",
        "Altri sistemi e dottrine filosofici"
    ],
    "Psicologia": [
        "Psicologia. filosofia e teoria",
        "Psicologia. sistemi, scuole, posizioni",
        "Psicologia fisiologica",
        "Percezione sensoriale",
        "Movimenti e funzioni motorie",
        "Emozioni e sentimenti",
        "Pulsioni fisiologiche",
        "Psicologia quantitativa",
        "Intelligenza, processi mentali intellettuali e consci",
        "Cognizione (conoscenza)",
        "Comunicazione",
        "Intelligenza e attitudini",
        "Stati e processi subconsci e alterati (psicologia del profondo)",
        "Il subconscio",
        "Coscienza secondaria",
        "Stati alterati della coscienza",
        "Fenomeni del sonno",
        "Ipnotismo",
        "Psicologia",
        "Psicologia evolutiva",
        "Psicologia ambientale",
        "Psicologia comparata",
        "Psicologia patologica e clinica",
        "Psicologia applicata"
    ],
    "Logica": [
        "Induzione",
        "Deduzione",
        "Sofismi e fonti d'errore",
        "Sillogismi",
        "Ipotesi",
        "Argomentazione e persuasione",
        "Analogia"
    ],
    "Etica (filosofia morale)": [
        "Etica. sistemi e dottrine",
        "Etica politica",
        "Etica delle relazioni familiari",
        "Etica economica, professionale, occupazionale",
        "Etica del divertimento e del tempo libero",
        "Etica del sesso e della riproduzione",
        "Etica delle relazioni sociali",
        "Etica dei consumi",
        "Altre norme etiche"
    ],
    "Filosofia antica, medievale, orientale": [
        "Filosofia orientale",
        "Filosofia greca presocratica",
        "Filosofia sofistica, socratica e filosofie greche connesse",
        "Filosofia platonica",
        "Filosofia aristotelica",
        "Filosofia scettica e neoplatonica",
        "Filosofia epicurea",
        "Filosofia stoica",
        "Filosofia occidentale medievale"
    ],
    "Filosofia occidentale moderna": [
        "Stati uniti e canada",
        "Isole britanniche",
        "Germania e austria",
        "Francia",
        "Italia",
        "Spagna e portogallo",
        "Russia e finlandia",
        "Scandinavia",
        "Altre aree geografiche"
    ],
    "Religione": [
        "Religione. filosofia e teoria",
        "Religione. miscellanea",
        "Religione. dizionari, enciclopedie, concordanze",
        "Religione. pubblicazioni in serie",
        "Religione. organizzazioni e gestione",
        "Religione. studio e insegnamento",
        "Religione. trattamento del soggetto in \
        riferimento a gruppi di persone",
        "Religione e pensiero religioso. trattamento storico e geografico"
    ],
    "Scienze sociali": [
        "Filosofia e teoria",
        "Miscellanea",
        "Dizionari, enciclopedie, concordanze",
        "Pubblicazioni in serie",
        "Organizzazioni e gestione",
        "Studio e insegnamento",
        "Trattamento del soggetto in riferimento a gruppi di persone",
        "Trattamento storico e geografico",
        "Sociologia",
        "Interazione sociale",
        "Relazione del singolo con la societa",
        "Processi sociali",
        "Processi sociali. coordinamento e controllo",
        "Cambiamento sociale",
        "Conflitti nei processi sociali",
        "Relazione dei fattori naturali e quasi naturali coi processi sociali",
        "Ecologia umana",
        "Relazione dei fattori genetici coi processi sociali",
        "Popolazione (demografia)",
        "Movimento della popolazione",
        "Stratificazione sociale (struttura sociale)",
        "Livelli di eta",
        "Uomini e donne",
        "Donne",
        "Classi sociali",
        "Aderenti a gruppi religiosi",
        "Gruppi linguistici",
        "Gruppi razziali, etnici, nazionali",
        "Cultura e istituzioni",
        "Istituzioni attinenti alle relazioni tra i sessi",
        "Matrimonio e famiglia",
        "Istituzioni attinenti alla morte",
        "Comunita",
        "Specifici tipi di comunita"
    ],
    "Scienza politica (politica e governo)": [
        "Scienza politica. filosofia e teoria",
        "Scienza politica. miscellanea",
        "Scienza politica. dizionari, enciclopedie, concordanze",
        "Scienza politica. pubblicazioni in serie",
        "Scienza politica. organizzazioni e gestione",
        "Scienza politica. studio e insegnamento",
        "Scienza politica. trattamento del soggetto in\
        riferimento a gruppi di persone",
        "Scienza politica. trattamento storico e geografico",
        "Biografia di pensatori politici",
        "Lo stato",
        "Governo",
        "Struttura, funzioni, attivita del governo",
        "Teorie e ideologie politiche",
        "Politica pratica",
        "Emigrazione e immigrazione",
        "Schiavitu ed emancipazione",
        "Relazioni internazionali",
        "Diplomazia",
        "Potere legislativo"
    ],
    "Economia": [
        "Filosofia e teoria",
        "Miscellanea",
        "Dizionari, enciclopedie, concordanze",
        "Pubblicazioni in serie",
        "Organizzazioni e gestione",
        "Studio e insegnamento",
        "Trattamento del soggetto in riferimento a gruppi di persone",
        "Trattamento storico e geografico",
        "Scuole di pensiero",
        "Economia del lavoro",
        "Manodopera e mercato del lavoro",
        "Manodopera",
        "Mercato del lavoro",
        "Disfunzioni del mercato del lavoro",
        "Salario, orario, altre condizioni di lavoro"
        "Donne lavoratrici",
        "Categorie speciali di lavoratori",
        "Economia finanziaria"

    ],
    "Diritto": [
        "Diritto"
    ],
    "Educazione": [
        "Educazione. filosofia, teoria, generalita",
        "Educazione per specifici obiettivi",
        "Psicologia educativa",
        "Educazione. aspetti sociali",
        "Educazione. studio e insegnamento",
        "Educazione. generalita",
        "Scuola e religione",
        "Istruzione superiore"
    ],
    "Scienze del linguaggio": [
        "Linguistica",
        "Notazioni (alfabeti e ideogrammi)",
        "Etimologia",
        "Dizionari poliglotti e lessicografia",
        "Fonologia",
        "Sistemi strutturali (grammatica)",
        "Dialettologia e paleografia",
        "Linguistica applicata",
        "Linguaggio verbale non parlato e scritto",
        "Lingue inglese e anglosassone",
        "Lingue germaniche (teutoniche)  lingua tedesca",
        "Lingue romanze  lingua francese",
        "Lingua italiana, romena, lingue ladine",
        "Lingue spagnola e portoghese",
        "Lingue italiche  lingua latina",
        "Lingue elleniche  lingua greca classica",
        "Altre lingue"
    ],
    "Matematica": [
        "Matematica. generalita",
        "Logica simbolica (logica matematica)",
        "Algebra",
        "Algebra di base per le scuole secondarie",
        "Aritmetica",
        "Topologia",
        "Analisi matematica",
        "Calcolo differenziale ed equazioni differenziali",
        "Calcolo integrale ed equazioni integrali",
        "Analisi funzionale",
        "Funzioni di variabili reali",
        "Funzioni di variabili complesse",
        "Geometria",
        "Geometria euclidea",
        "Geometrie analitiche",
        "Probabilita e matematica applicata",
        "Probabilita",
        "Teoria dei giochi",
        "Analisi numerica applicata",
        "Statistica matematica",
        "Matematica applicata. programmazione",
        "Matematica applicata. argomenti particolari"
    ],
    "Astronomia": [
        "Astronomia teorica e meccanica celeste",
        "Astronomia pratica e sferica",
        "Astronomia descrittiva",
        "Astrofisica",
        "Cosmochimica",
        "Universo (cosmologia)",
        "Sistema solare",
        "Luna",
        "Pianeti",
        "Meteoroidi, vento solare, luce zodiacale",
        "Comete",
        "Sole",
        "Stelle",
        "Transiti, satelliti, occultazioni",
        "Terra (geografia astronomica)",
        "Geografia matematica",
        "Rilevamento geodetico",
        "Disegno delle carte e proiezioni",
        "Geografia matematica. rilevamenti",
        "Navigazione astronomica",
        "Effemeridi astronomiche (almanacchi nautici)",
        "Cronologia (tempo)"
    ],
    "Fisica": [
        "Teorie della fisica e fisica matematica",
        "Stati della materia",
        "Unita, dimensioni, costanti fisiche",
        "Meccanica",
        "Meccanica dei fluidi",
        "Meccanica dei gas",
        "Suono e vibrazioni connesse",
        "Vibrazioni connesse al suono",
        "Ottica e fenomeni parafotici",
        "Fasci di luce e loro modificazioni",
        "Colore",
        "Spettroscopia e ottica delle fibre",
        "Calore",
        "Elettricita ed elettronica",
        "Fisica. elettronica",
        "Elettrodinamica (correnti elettriche) e termoelettricita",
        "Magnetismo",
        "Fisica moderna",
        "Fisica atomica e nucleare"
    ],
    "Chimica": [
        "Chimica fisica e teorica",
        "Chimica teorica",
        "Chimica fisica",
        "Laboratori chimici, apparecchi, attrezzature",
        "Chimica analitica",
        "Analisi qualitativa",
        "Analisi quantitativa",
        "Chimica inorganica",
        "Chimica organica",
        "Composti organici macromolecolari e composti connessi",
        "Altre sostanze organiche",
        "Cristallografia",
        "Mineralogia",
        "Minerali. distribuzione geografica"
    ],
    "Scienze della terra": [
        "Geologia, meteorologia, idrologia generale",
        "Struttura e proprieta generali della terra e degli altri mondi",
        "Fenomeni plutonici",
        "Fenomeni di superficie ed esogeni e loro agenti",
        "Geomorfologia e idrologia generale",
        "Oceanografia",
        "Oceanografia dinamica",
        "Idrologia",
        "Meteorologia",
        "Idrometeorologia",
        "Climatologia e tempo atmosferico",
        "Clima di aree geografiche specifiche",
        "Geologia storica",
        "Geochimica",
        "Rocce. distribuzione geografica",
        "Geologia economica",
        "Materiali"
    ],
    "Paleontologia  paleozoologia": [
        "Paleobotanica",
        "Invertebrati fossili",
        "Protozoi fossili e altri animali fossili semplici",
        "Molluschi e molluscoidi fossili",
        "Altri invertebrati  fossili",
        "Vertebrati fossili (cordati fossili)",
        "Vertebrati fossili a sangue freddo",
        "Rettili fossili",
        "Uccelli fossili",
        "Mammiferi fossili"
    ],
    "Scienze della vita": [
        "Razze umane",
        "Razze umane. distribuzione geografica",
        "Antropologia fisica",
        "Evoluzione organica della specie umana e genetica umana",
        "Uomo preistorico",
        "Biologia",
        "Fisiologia",
        "Biofisica e biochimica",
        "Patologia",
        "Sviluppo e maturazione",
        "Anatomia e morfologia",
        "Ecologia",
        "Biologia economica",
        "Biologia tissulare, cellulare, molecolare",
        "Citologia (biologia cellulare)",
        "Biogeografia",
        "Biologia idrografica",
        "Evoluzione organica e genetica",
        "Genetica",
        "Variazioni genetiche",
        "Microbi",
        "Natura generale della vita",
        "Microscopia in biologia",
        "Raccolta e conservazione di campioni biologici"
    ],
    "Scienze botaniche": [
        "Scienze botaniche. studio e insegnamento",
        "Scienze botaniche. musei, collezioni, esposizioni",
        "Botanica"
    ],
    "Scienze zoologiche": [
        "Scienze zoologiche. studio e insegnamento",
        "Scienze zoologiche. musei, collezioni, esposizioni",
        "Zoologia"
    ],
    "Scienze mediche  medicina": [
        "Medicina. tecniche, procedure, apparecchi, materiali",
        "Medicina. organizzazioni, gestione, professioni",
        "Personale sanitario",
        "Medicina. studio, insegnamento, infermieristica e tecniche connesse",
        "Infermieristica e altre attivita ausiliarie alla professione medica",
        "Anatomia umana, citologia, istologia",
        "Fisiologia umana",
        "Igiene generale e personale",
        "Dietetica",
        "Igiene. argomenti speciali",
        "Efficienza fisica",
        "Tossicodipendenze",
        "Igiene pubblica e argomenti connessi",
        "Medicina legale (giurisprudenza medica)",
        "Incidenza, distribuzione e controllo delle malattie",
        "Incidenza, diffusione e controllo di malattie specifiche",
        "Farmacologia e terapeutica",
        "Terapeutica",
        "Terapie fisiche e altre terapie",
        "Tossicologia (veleni e avvelenamenti)",
        "Malattie",
        "Pronto soccorso e medicina familiare",
        "Patologia",
        "Tumori e cancro",
        "Chirurgia e soggetti connessi",
        "Oftalmologia",
        "Otologia e audiologia",
        "Ginecologia",
        "Pediatria e geriatria",
        "Pediatria",
        "Geriatria",
        "Medicina sperimentale"
    ],
    "Ingegneria e operazioni affini": [
        "Ingegneria meccanica (meccanica applicata) e materiali",
        "Suono e vibrazioni connesse",
        "Vibrazioni meccaniche",
        "Ingegneria dei sistemi",
        "Ingegneria dell'ambiente (biotecnologia)",
        "Fisica applicata",
        "Ingegneria del vapore",
        "Tecnologia dell'energia idraulica",
        "Ingegneria elettromagnetica e rami connessi",
        "Energia elettrica",
        "Illuminazione",
        "Trazione elettrica",
        "Ingegneria magnetica",
        "Ottica applicata (ingegneria ottica) e ingegneria parafotica",
        "Prove e misure elettriche",
        "Ingegneria elettronica e delle comunicazioni",
        "Ingegneria elettronica",
        "Telegrafia per mezzo di fili",
        "Tipi specifici di strumenti e apparecchi telegrafici",
        "Radiotecnica e radartecnica",
        "Telefonia per mezzo di fili",
        "Apparecchiature telefoniche terminali",
        "Trasmissione telefonica e apparecchiature non terminali",
        "Televisore",
        "Sistemi di registrazione e riproduzione del \
        suono e altri dispositivi",
        "Elaboratori",
        "Ingegneria termica e propulsione primaria",
        "Motori a combustione interna e tecniche di propulsione",
        "Ingegneria geotermica",
        "Tecnologia della propulsione elettrica",
        "Ingegneria dell'energia solare",
        "Ingegneria nucleare",
        "Tecnologia pneumatica, del vuoto, delle basse temperature",
        "Ingegneria delle macchine",
        "Utensili e macchine utensili",
        "Ingegneria mineraria e operazioni connesse",
        "Ingegneria militare e navale",
        "Armamenti",
        "Altre operazioni dell'ingegneria militare",
        "Veicoli militari",
        "Ingegneria navale e tecnica della navigazione",
        "Tecnica della navigazione",
        "Navigazione",
        "Ingegneria civile",
        "Ingegneria strutturale",
        "Ingegneria ferroviaria e stradale",
        "Ferrovie",
        "Materiale ferroviario rotabile",
        "Strade e autostrade",
        "Rivestimenti artificiali stradali",
        "Ingegneria idraulica",
        "Ingegneria sanitaria e urbana",
        "Approvvigionamento idrico",
        "Trattamento ed eliminazione dei rifiuti liquidi",
        "Igiene pubblica",
        "Inquinamento e ingegneria sanitaria industriale",
        "Altri rami dell'ingegneria sanitaria e urbana",
        "Altri rami dell'ingegneria",
        "Ingegneria dei trasporti",
        "Ingegneria aerospaziale",
        "Aeronautica",
        "Principi di volo",
        "Velivoli",
        "Parti del velivolo e aspetti tecnici generali",
        "Strumenti e apparecchiature aeree",
        "Aeroporti",
        "Veicoli a cuscino d'aria (macchine a effetto-suolo, hovercraft)",
        "Astronautica",
        "Ingegneria astronautica",
        "Ingegneria dei controlli automatici"
    ],
    "Tecnologie chimiche": [
        "Ingegneria chimica",
        "Tecnologia dei prodotti chimici industriali (chimica pesante)",
        "Tecnologia degli esplosivi, dei combustibili, dei prodotti connessi",
        "Combustibili",
        "Tecnologia delle bevande",
        "Tecnologia alimentare",
        "Tecnologia degli oli, dei grassi, delle cere, dei gas industriali",
        "Petrolio",
        "Gas industriali",
        "Altri gas industriali",
        "Ceramica e tecnologie delle ceramiche e affini",
        "Tecnologie dei colori e delle vernici",
        "Tecnologia di altri prodotti organici",
        "Materie plastiche",
        "Polimeri",
        "Metallurgia"
    ],
    "Urbanistica e arte del paesaggio": [
        "Pianificazione territoriale (urbanistica)",
        "Sistemazione del paesaggio (architettura del paesaggio)",
        "Paesaggi naturali"
    ],
    "Architettura": [
        "Architettura"
    ],
    "Arti plastiche  scultura": [
        "Scultura",
        "Scultori",
        "Intaglio",
        "Monete",
        "Arti della ceramica",
        "Mosaici",
        "Gioielli"
    ],
    "Disegno, arti decorative e minori": [
        "Disegno e disegni",
        "Disegno. trattamento storico e geografico",
        "Disegnatori",
        "Disegno. tecniche, procedure, apparecchi, attrezzature, materiali",
        "Vignette, caricature, fumetti",
        "Grafica"
    ],
    "Pittura": [
        "Pittura. filosofia e teoria",
        "Pittura. miscellanea",
        "Procedimenti e forme della pittura",
        "Materiali pittorici",
        "Attrezzature, strumenti, modelli artistici della pittura",
        "Tecniche e metodi della pittura",
        "Tecniche di riproduzione pittorica",
        "Forme specifiche di pittura",
        "Astrazioni, simbolismo, allegoria, mitologia, leggenda nella pittura",
        "Pittura di genere",
        "Religione e simbolismo religioso nella pittura",
        "Pittura storica",
        "Figura umana e sue parti nella pittura",
        "Pittura. altri soggetti",
        "Pittura. trattamento storico e geografico",
        "Pittura dei popoli senza scrittura e dell'antichita"
    ],
    "Fotografia e fotografie": [
        "Miscellanea",
        "Tecniche e procedimenti",
        "Attrezzature, apparecchi, materiali fotografici",
        "Macchine fotografiche e accessori",
    ],
    "Musica": [
        "Filosofia ed estetica",
        "Miscellanea",
        "Soggetti speciali di applicabilita generale",
        "Studio, insegnamento, esecuzioni",
        "Esecuzioni musicali",
        "Persone associate alla musica",
        "Musica. principi generali",
        "Armonia",
        "Melodia e contrappunto",
        "Composizione ed esecuzione musicale",
        "Musica di gruppi etnici e di vari specifici paesi e localita",
        "Musica. altri argomenti",
        "Strumenti musicali",
        "Musica drammatica",
        "Persone associate alla musica drammatica",
        "Opera",
        "Musica da teatro",
        "Musica sacra",
        "Voce e musica vocale",
        "Cori e canti a piu parti",
        "Opere corali complete",
        "Canti a piu parti, da uno a nove",
        "Canti folcloristici",
        "Canzoni a larga diffusione",
        "Canti per gruppi specifici e su specifici soggetti",
        "Altri tipi di canti",
        "La voce",
        "Insiemi strumentali e loro musica",
        "Musica jazz",
        "Ouvertures autonome per orchestra",
        "Musica da camera",
        "Strumenti a tastiera e loro musica",
        "Strumenti a corda e tastiera e loro musica",
        "Organo",
        "Altri strumenti a tastiera e loro musica",
        "Strumenti a corda e loro musica",
        "Violino",
        "Chitarra, mandolino, liuto",
        "Strumenti a fiato e loro musica",
        "Strumenti a percussione, meccanici, elettrici"
    ],
    "Arti ricreative e dello spettacolo": [
        "Attivita ricreative",
        "Arti dello spettacolo",
        "Spettacoli pubblici",
        "Cinema, radio, televisione",
        "Cinema",
        "Radio",
        "Televisione",
        "Teatro",
        "Balletto",
        "Danza",
        "Illusionismo",
        "Giochi",
        "Scacchi",
        "Sport"
    ],
    "Letteratura": [
        "Letteratura. filosofia e teoria",
        "Letteratura. miscellanea",
        "Letteratura. dizionari, enciclopedie, concordanze",
        "Letteratura. pubblicazioni in serie",
        "Letteratura. organizzazioni",
        "Letteratura. studio e insegnamento",
        "Retorica e raccolte",
        "Raccolte di piu letterature",
        "Raccolte di piu letterature. poesia",
        "Raccolte di piu letterature. letteratura drammatica",
        "Raccolte di piu letterature. narrativa",
        "Raccolte di piu letterature. saggistica",
        "Raccolte di piu letterature. discorsi",
        "Raccolte di piu letterature. lettere",
        "Raccolte di piu letterature. satira e umorismo",
        "Raccolte di piu letterature. scritti miscellanei",
        "Storia, descrizione, studi critici di piu letterature",
        "Letteratura americana in lingua inglese",
        "Letteratura inglese e anglosassone",
        "Letterature nelle lingue germaniche (teutoniche) \
        letteratura tedesca",
        "Letterature nelle lingue romanze  letteratura francese",
        "Letterature italiana, romena, ladina",
        "Letteratura spagnola e portoghese",
        "Letterature nelle lingue italiche  letteratura latina",
        "Letterature nelle lingue elleniche  letteratura greca classica",
        "Letterature in altre lingue"
    ],
    "Storia": [
        "Storia generale. filosofia e teoria",
        "Storia generale. miscellanea",
        "Storia generale. dizionari, enciclopedie, concordanze",
        "Raccolte di narrazioni di determinati avvenimenti storici",
        "Storia generale. pubblicazioni in serie",
        "Storia generale. organizzazioni",
        "Storia generale. studio e insegnamento",
        "Storiografia",
        "Storici e storiografi",
        "Storia universale"
    ],
    "Geografia generale": [
        "Geografia generale. miscellanea",
        "Geografia generale. dizionari, enciclopedie, concordanze, repertori",
        "Resoconti di viaggi non limitati geograficamente",
        "Geografia storica"
    ],
    "Biografie": [
        "Biografie di uomini",
        "Biografie di donne"
    ]
}

RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        default_endpoint_prefix=True,
        search_class=RevisionedRecordsSearch,
        indexer_class=RecordIndexer,
        search_index='records',
        search_type=None,
        record_serializers={
            'application/json': ('fare.records.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('fare.records.serializers'
                                 ':json_v1_search'),
        },
        record_loaders={
            'application/json': ('fare.records.loaders'
                                 ':json_v1'),
        },
        list_route='/records/',
        item_route='/records/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=deny_all,
        read_permission_factory_imp=check_elasticsearch,
        update_permission_factory_imp=deny_all,
        delete_permission_factory_imp=deny_all,
        list_permission_factory_imp=allow_all
    ),
    'fmgid': dict(
        pid_type=FILE_MNGT_PID_TYPE,
        pid_minter=FILE_MNGT_PID_MINTER,
        pid_fetcher=FILE_MNGT_PID_FETCHER,
        default_endpoint_prefix=True,
        search_class=RevisionSearch,
        indexer_class=RecordIndexer,
        # search_index='records',
        search_type=None,
        record_serializers={
            'application/json': ('fare.records.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('fare.records.serializers'
                                 ':json_v1_search'),
        },
        record_loaders={
            'application/json': ('fare.records.loaders'
                                 ':json_v1'),
        },
        list_route='/file_management/',
        item_route='/file_management/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=deny_all,
        read_permission_factory_imp=check_elasticsearch,
        update_permission_factory_imp=deny_all,
        delete_permission_factory_imp=deny_all,
        list_permission_factory_imp=allow_all
    ),
}
"""REST API for fare."""

RECORDS_UI_ENDPOINTS = {
    'recid': {
        'pid_type': 'recid',
        'route': '/records/<pid_value>',
        'template': 'records/record.html',
    },
}
"""Records UI for fare."""

SEARCH_UI_JSTEMPLATE_RESULTS = 'templates/records/results.html'
"""Result list template."""

PIDSTORE_RECID_FIELD = 'id'

FARE_ENDPOINTS_ENABLED = True
"""Enable/disable automatic endpoint registration."""


RECORDS_REST_FACETS = dict(
    records=dict(
        aggs=dict(
            type=dict(terms=dict(field='type')),
            keywords=dict(terms=dict(field='keywords')),
            Ordine_di_scuola=dict(terms=dict(field='educationLevel.keyword')),
            Disciplina=dict(terms=dict(field='subject.keyword')),
            Licenza=dict(terms=dict(field='license.keyword'))
        ),
        post_filters=dict(
            type=terms_filter('type'),
            keywords=terms_filter('keywords'),
            Ordine_di_scuola=terms_filter('educationLevel.keyword'),
            Disciplina=terms_filter('subject.keyword'),
            Licenza=terms_filter('license.keyword'),
        )
    )
)
"""Introduce searching facets."""


RECORDS_REST_SORT_OPTIONS = dict(
    records=dict(
        bestmatch=dict(
            title=_('Best match'),
            fields=['_score'],
            default_order='desc',
            order=1,
        ),
        mostrecent=dict(
            title=_('Most recent'),
            fields=['-_created'],
            default_order='asc',
            order=2,
        ),
    )
)
"""Setup sorting options."""


RECORDS_REST_DEFAULT_SORT = dict(
    records=dict(
        query='bestmatch',
        noquery='mostrecent',
    )
)
"""Set default sorting options."""
