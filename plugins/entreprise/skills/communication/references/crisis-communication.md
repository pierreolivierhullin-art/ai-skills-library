# Crisis Communication — Plans, Dark Sites, Reputation Repair & Social Media Crisis

## Overview

Ce document de reference couvre l'ensemble des disciplines de la communication de crise : elaboration du plan de communication de crise, preparation des outils (dark site, holding statements, Q&A), organisation de la cellule de crise communication, gestion des crises sur les reseaux sociaux, et strategies de reparation de reputation post-crise. Utiliser ce guide pour anticiper, gerer et surmonter les crises mediatiques et reputationnelles. La communication de crise ne s'improvise pas : elle se prepare en temps de paix et s'execute avec rigueur et humanite quand la crise survient.

---

## Plan de Communication de Crise

### Principes fondamentaux

Un plan de communication de crise est un document operationnel qui definit les procedures, les roles et les outils a activer en cas de crise. Il doit etre :
- **Pre-ecrit** : redige et valide avant toute crise, pas pendant.
- **Teste** : mis a l'epreuve par des exercices de simulation au moins une fois par an.
- **Accessible** : disponible instantanement (version digitale et papier) pour tous les membres de la cellule de crise.
- **Actualise** : revu et mis a jour au minimum tous les 6 mois et systematiquement apres chaque crise ou incident significatif.

### Structure du plan de communication de crise

#### 1. Typologie des crises
Identifier et categoriser les crises potentielles selon leur nature et leur gravite :

| Categorie | Exemples | Niveau de gravite typique |
|---|---|---|
| **Operationnelle** | Panne majeure, rappel produit, accident industriel, rupture de supply chain | 2-4 |
| **Ethique et gouvernance** | Fraude, harcelement, corruption, conflit d'interets | 3-4 |
| **Sociale et RH** | Licenciements massifs, greve, suicide au travail | 2-4 |
| **Environnementale** | Pollution, maree noire, non-conformite reglementaire | 3-4 |
| **Cyber et donnees** | Cyber-attaque, fuite de donnees personnelles, ransomware | 2-4 |
| **Mediatique et reputationnelle** | Bad buzz, campagne d'ONG, investigation journalistique | 1-3 |
| **Sanitaire** | Contamination produit, pandemie, risque pour la sante publique | 3-4 |
| **Juridique** | Mise en examen, amende regulatoire majeure, class action | 2-4 |

#### 2. Matrice d'escalade
Definir les criteres d'activation des differents niveaux de reponse :

```
NIVEAU 1 — VIGILANCE
Criteres : signal faible identifie, buzz negatif naissant (< 10 mentions),
           article isole dans un media Tier 3-4
Action :   Veille renforcee, preparation d'elements de langage
Decideur : Responsable communication

NIVEAU 2 — ALERTE
Criteres : couverture mediatique negative dans 2+ medias Tier 1-2,
           buzz croissant sur les reseaux sociaux (10-100 mentions/h),
           sollicitations presse multiples
Action :   Activation cellule restreinte, diffusion holding statement,
           briefing du porte-parole
Decideur : Directeur de la communication

NIVEAU 3 — CRISE
Criteres : couverture mediatique massive (JT, unes de presse),
           impact operationnel avere, attention des regulateurs,
           trending topic sur les reseaux sociaux
Action :   Cellule de crise complete, dark site active,
           porte-parole designe en continu, communication multicanale
Decideur : Directeur general

NIVEAU 4 — CRISE MAJEURE
Criteres : menace existentielle pour l'organisation,
           couverture mediatique internationale, victimes,
           implications juridiques majeures
Action :   Direction generale mobilisee 24/7, conseil juridique externe,
           conseil en communication de crise, communication continue
Decideur : President / Conseil d'administration
```

#### 3. Annuaire de crise
Maintenir un annuaire a jour avec les coordonnees directes (mobile personnel) de :
- Membres de la cellule de crise (internes)
- Agence de communication de crise (externe)
- Cabinet d'avocats (droit des medias, droit penal des affaires)
- Porte-paroles designes (titulaires et suppleants)
- Contacts cles dans les medias de reference
- Contacts regulateurs et autorites competentes
- Prestataires techniques (dark site, monitoring, hotline)

**Securite** : cet annuaire contient des coordonnees personnelles sensibles. Le stocker de maniere securisee (acces restreint, chiffre) et le mettre a jour a chaque changement de poste ou de numero.

#### 4. Templates pre-rediges
Preparer des templates pour chaque type de crise identifie :
- Holding statements (declarations initiales)
- Communiques de crise
- Q&A anticipes
- Messages internes (collaborateurs)
- Publications reseaux sociaux
- Scripts pour le standard telephonique et le service client

---

## Dark Site & Holding Statements

### Dark Site

Le dark site est un site web de crise pre-construit, heberge en ligne mais non reference et non accessible au public, qui peut etre active en quelques minutes en cas de crise. Il sert de point de reference central pour toutes les informations officielles pendant la crise.

#### Contenu du dark site

```
PAGE D'ACCUEIL
├── Bandeau d'alerte avec date et heure de derniere mise a jour
├── Message officiel de l'organisation (holding statement)
├── Lien vers le communique de presse officiel
├── Section "Dernieres informations" (mises a jour chronologiques)
└── Contacts (presse, parties prenantes, hotline)

PAGES SECONDAIRES
├── FAQ / Questions frequentes
├── Informations pratiques (consignes de securite, procedures)
├── Espace presse (communiques, visuels, biographies porte-paroles)
├── Informations pour les collaborateurs (si crise interne)
└── Formulaire de contact / hotline
```

#### Specifications techniques du dark site

- **Hebergement independant** : ne pas heberger le dark site sur la meme infrastructure que le site corporate (risque de panne simultanee en cas de cyber-attaque).
- **CDN et haute disponibilite** : le dark site doit supporter un pic de trafic massif (x100 du trafic normal). Utiliser un CDN (Cloudflare, Akamai, AWS CloudFront).
- **SSL/TLS** : certificat HTTPS valide obligatoire.
- **Mobile responsive** : une majorite du trafic en crise vient du mobile.
- **CMS simplifie** : permettre la mise a jour du contenu par des non-techniciens en quelques minutes. Utiliser un CMS headless ou un generateur de sites statiques (Hugo, Gatsby) pre-configure.
- **Activation en < 30 minutes** : la procedure d'activation doit etre testee et documentee. DNS pre-configure, contenus templates pre-charges.

### Holding Statements

Le holding statement est la declaration initiale diffusee dans les premieres heures de la crise, quand les faits ne sont pas encore completement etablis. C'est le message le plus critique de la gestion de crise.

#### Structure du holding statement

```
HOLDING STATEMENT — [TYPE DE CRISE]

[Nom de l'organisation] a ete informe(e) de [description factuelle et sobre
de la situation, en termes non techniques et non juridiques].

[Ce que l'organisation fait] : Nous avons immediatement [action concrete prise :
activation de la cellule de crise, securisation du site, notification des autorites,
deploiement d'equipes sur le terrain, etc.].

[Engagement de suivi] : Nous travaillons activement a [objectif : comprendre
les causes, evaluer l'ampleur, proteger les personnes concernees].
Nous communiquerons de nouvelles informations des qu'elles seront confirmees.

[Empathie — si victimes] : Nos pensees vont en priorite aux personnes affectees
et a leurs proches. [Action concrete pour les aider : hotline, prise en charge, etc.]

[Contact] :
Relations presse : [nom] — [tel : +33 1 00 00 00 00] — [email : crise@exemple-corp.com]
Hotline [si applicable] : [numero : 0 800 00 00 00]
```

#### Principes de redaction du holding statement

- **Rapidite** : diffuser dans les 2 heures maximum. Mieux vaut un holding statement sobre et factuel dans les 2h qu'un communique detaille dans les 6h.
- **Factualite** : ne rapporter que les faits confirmes. Ne jamais speculer sur les causes, les responsabilites ou l'ampleur.
- **Empathie** : si des personnes sont affectees (victimes, clients leses, collaborateurs), exprimer l'empathie avant de parler de l'organisation. L'ordre des priorites : les personnes d'abord, l'organisation ensuite.
- **Action** : montrer que l'organisation agit. Ne pas se contenter de "prendre la situation au serieux" mais decrire les actions concretes engagees.
- **Engagement de transparence** : promettre de tenir informe et respecter cet engagement. Un silence prolonge apres un holding statement est pire que l'absence de holding statement.
- **Prudence juridique** : ne jamais admettre de responsabilite avant l'enquete. Ne pas utiliser de formulations qui pourraient etre interpretees comme un aveu. Consulter le conseiller juridique avant diffusion, si le delai le permet.

### Q&A de Crise

Preparer un document de Questions & Reponses anticipe pour chaque type de crise. Ce document est un outil interne a destination des porte-paroles et des equipes en contact avec le public (standard, service client, community managers).

#### Structure du Q&A de crise

```
Q&A DE CRISE — [TYPE DE CRISE]
Version : [numero] — Date : [date/heure] — Classification : CONFIDENTIEL

SECTION 1 — QUESTIONS GENERALES
Q : Que s'est-il passe ?
R : [Reponse factuelle, sobre, coherente avec le holding statement]

Q : Quand est-ce arrive ?
R : [Date et heure, si confirmes]

Q : Combien de personnes sont concernees ?
R : [Nombre, si confirme. Si non confirme : "Nous sommes en cours d'evaluation.
    Nous communiquerons des chiffres des qu'ils seront confirmes."]

SECTION 2 — QUESTIONS SUR LES CAUSES
Q : Quelle est la cause de [l'incident] ?
R : "Une enquete est en cours pour determiner les causes exactes.
    Il serait premature de speculer a ce stade."

SECTION 3 — QUESTIONS SUR LES RESPONSABILITES
Q : Etes-vous responsable ?
R : "Nous cooperons pleinement avec [autorite competente] pour etablir
    les faits. Notre priorite immediate est [action : proteger, remedier, informer]."

SECTION 4 — QUESTIONS PROSPECTIVES
Q : Comment garantissez-vous que cela ne se reproduira pas ?
R : "Nous tirerons toutes les lecons de cette situation.
    Des mesures de [prevention/renforcement] seront mises en oeuvre
    des que l'analyse des causes sera complete."

SECTION 5 — ZONE ROUGE (ne pas repondre)
Q : [Question sur un sujet juridiquement sensible]
R : "Cette question releve de la procedure [judiciaire/reglementaire] en cours.
    Nous ne sommes pas en mesure de la commenter a ce stade."
```

---

## Cellule de Crise Communication

### Composition de la cellule

La cellule de crise communication est distincte de la cellule de gestion operationnelle de la crise, bien que les deux travaillent en etroite coordination.

#### Composition type

| Role | Responsabilite | Profil |
|---|---|---|
| **Pilote de la cellule communication** | Coordonne les actions de communication, valide les messages | Directeur de la communication |
| **Porte-parole** | Delivre les messages aux medias et au public | CEO ou dirigeant designe |
| **Redacteur en chef de crise** | Redige les communiques, holding statements, Q&A | Senior communicant |
| **Responsable veille et monitoring** | Suit la couverture mediatique et social media en temps reel | Charge de veille / community manager |
| **Responsable communication interne** | Informe et rassure les collaborateurs | Responsable communication interne |
| **Conseiller juridique** | Valide la conformite juridique des messages | Directeur juridique ou avocat externe |
| **Liaison avec la cellule operationnelle** | Fait le lien entre la gestion operationnelle et la communication | Directeur des operations ou delegue |
| **Conseil externe** (si crise majeure) | Apporte l'expertise et le recul d'un consultant specialise | Agence de communication de crise |

### Rythme de fonctionnement en crise

```
PREMIER JOUR (H0 — H24)

H0      : Detection de la crise, notification de la cellule
H0-H0,5 : Premiere reunion de cadrage (15 min)
          → Evaluation du niveau de gravite
          → Designation du porte-parole
          → Premiere collecte de faits
H0,5-H2 : Redaction et diffusion du holding statement
H2-H4   : Points de situation toutes les heures
          → Mise a jour des faits
          → Activation du dark site
          → Communication interne
H4-H12  : Points de situation toutes les 2 heures
          → Communique de presse detaille si nouveaux faits
          → Conference de presse si crise niveau 3-4
          → Mise a jour du dark site et des reseaux sociaux
H12-H24 : Points de situation toutes les 4 heures
          → Releve des equipes (prevoir une rotation)
          → Bilan de la premiere journee

JOURS SUIVANTS
Matin   : Point de situation quotidien (30 min)
          → Revue de la couverture mediatique
          → Mise a jour des messages et du Q&A
          → Plan d'actions de la journee
Soir    : Point de bilan quotidien (15 min)
          → Evaluation de l'evolution de la crise
          → Preparation de la communication du lendemain

FIN DE CRISE
          → Decision formelle de desactivation de la cellule
          → Dernier communique ("resolution de la situation")
          → Retour d'experience (RETEX) dans les 2 semaines
```

### Coordination avec la cellule operationnelle

La cellule communication ne decide pas de la gestion operationnelle de la crise, mais elle a besoin d'informations precises et actualisees pour communiquer. Etablir les regles suivantes :
- **Single source of truth** : un seul document de faits confirmes, mis a jour en temps reel, partage entre les deux cellules.
- **Validation croisee** : tout message externe est valide par la cellule communication ET la cellule operationnelle avant diffusion.
- **Pas de communication non coordonnee** : aucun membre de l'organisation ne prend la parole publiquement sans l'accord de la cellule communication. Interdire formellement les initiatives individuelles sur les reseaux sociaux.

---

## Gestion de Crise sur les Reseaux Sociaux

### Specificites de la crise social media

Les reseaux sociaux modifient fondamentalement la dynamique de crise :
- **Vitesse** : une crise peut exploser en quelques minutes sur Twitter/X, avant meme que la cellule de crise ait eu le temps de se reunir.
- **Viralite** : un tweet, une video, un screenshot peut etre partage des millions de fois en quelques heures.
- **Deformation** : l'information se deforme a chaque partage. Les rumeurs, les fausses informations et les manipulations se repandent plus vite que les faits.
- **Memoire** : tout ce qui est publie sur les reseaux sociaux est archive indefiniment. Les captures d'ecran survivent meme aux suppressions.
- **Emotion** : les reseaux sociaux amplifient les reactions emotionnelles (colere, indignation, peur). Les reponses rationnelles sont souvent noyees dans le bruit.

### Protocole de gestion de crise social media

#### Phase 1 — Detection et evaluation (0-30 minutes)

- Detecter le signal : alerte veille automatisee (Talkwalker, Meltwater, Mention) ou remontee manuelle.
- Evaluer la menace : source originale (influenceur, media, particulier), vitesse de propagation, engagement (likes, partages, commentaires), tonalite.
- Classifier : bad buzz passager (niveau 1) vs. crise potentielle (niveau 2-3) vs. crise avere (niveau 3-4).

#### Phase 2 — Reponse immediate (30 min — 2 heures)

- **Ne pas supprimer** : la suppression d'un post en pleine crise est systematiquement capturee et interpretee comme une tentative de dissimulation.
- **Ne pas repondre a chaud** : prendre le temps de verifier les faits avant de repondre. Un tweet precipite peut aggraver la situation.
- **Publier un message d'accusation de reception** : "Nous avons connaissance de [la situation]. Nous verifions les informations et reviendrons vers vous rapidement." Ce message montre que l'organisation n'ignore pas le sujet.
- **Centraliser la communication** : un seul compte publie les messages officiels. Les autres comptes de l'organisation retweetent/partagent sans commenter.

#### Phase 3 — Communication structuree (2h — 48h)

- Publier la position officielle (aligned avec le holding statement) sur tous les canaux sociaux.
- Repondre individuellement aux questions factuelles et aux personnes directement concernees.
- Ne pas engager le debat avec les trolls ou les comptes anonymes agressifs.
- Mettre a jour regulierement (au minimum toutes les 4 heures en crise active).
- Utiliser le format video pour les messages importants du dirigeant (plus d'impact et de credibilite qu'un communique texte).

#### Phase 4 — Surveillance et desescalade (48h+)

- Monitorer la courbe de mentions (volume, tonalite, propagation).
- Identifier les relais d'influence positifs (clients satisfaits, collaborateurs, partenaires) et les solliciter discretement.
- Continuer de repondre aux questions individuelles avec empathie et transparence.
- Ne pas declarer la fin de la crise trop tot sur les reseaux sociaux.

### Gestion des fausses informations en crise

- **Identifier rapidement** les fausses informations circulant sur les reseaux et evaluer leur impact.
- **Corriger sans amplifier** : publier un message factuel de correction sans reprendre ni citer la fausse information (eviter l'effet Streisand).
- **Documenter** : archiver (captures d'ecran horodatees) toutes les fausses informations pour un eventuel usage juridique.
- **Signaler** : utiliser les mecanismes de signalement des plateformes pour les contenus diffamatoires ou manifestement faux.

---

## Reparation de Reputation Post-Crise

### Le processus de recovery

La reparation de reputation apres une crise est un processus long (6-24 mois) qui exige une strategie deliberee et une execution disciplinee. La crise ne se termine pas quand les medias passent a autre chose : elle se termine quand la confiance des parties prenantes est restauree.

### Framework de reparation en 5 phases

#### Phase 1 — RETEX (Retour d'Experience) — Semaine 1-2 post-crise
- Conduire un retour d'experience complet : chronologie des evenements, analyse des decisions prises, evaluation de la communication (ce qui a fonctionne, ce qui n'a pas fonctionne).
- Mener une analyse de la couverture mediatique post-crise : tonalite residuelle, narratifs persistants, questions non resolues.
- Sonder les parties prenantes cles sur leur perception post-crise (collaborateurs, clients, partenaires).
- Documenter les lecons apprises et mettre a jour le plan de communication de crise.

#### Phase 2 — Actions correctives visibles — Mois 1-3
- Annoncer et mettre en oeuvre les actions correctives issues du RETEX. Les actions doivent etre concretes, mesurables et communiquees publiquement.
- Nommer, si necessaire, un responsable des actions correctives (avec visibilite publique).
- Publier un rapport d'avancement sur les mesures prises (transparence radicale).
- Renforcer les dispositifs de prevention (audit, controles, formations).

#### Phase 3 — Reconquete narrative — Mois 3-6
- Reprendre progressivement la communication proactive sur les sujets strategiques de l'organisation.
- Privileger les actions et les resultats concrets plutot que les declarations d'intention.
- Utiliser le thought leadership pour reposition le dirigeant et l'organisation sur leurs sujets d'expertise.
- Solliciter des temoignages de tiers (clients, partenaires, experts independants) pour reconstruire la credibilite.

#### Phase 4 — Renforcement de la confiance — Mois 6-12
- Mesurer l'evolution de la reputation (etude RepTrak, barometre de confiance, NPS).
- Intensifier les actions de RSE et d'engagement societal en lien avec les enjeux de la crise (si pertinent).
- Participer a des initiatives sectorielles ou multi-parties prenantes sur le sujet de la crise (montrer le leadership, pas seulement la conformite).
- Maintenir la transparence sur les progres realises.

#### Phase 5 — Nouvelle normalite — Mois 12-24
- Integrer les lecons de la crise dans le narrative d'entreprise : transformer l'epreuve en preuve de resilience et de capacite de transformation.
- Mettre a jour la strategie de communication pour integrer les nouveaux risques identifies.
- Former les nouvelles equipes et les nouveaux dirigeants aux lecons de la crise.
- Tester le nouveau plan de crise par un exercice de simulation.

### Erreurs fatales en reparation de reputation

- **Faire comme si la crise n'avait pas eu lieu** : les parties prenantes n'oublient pas. Ignorer la crise dans la communication post-crise est percu comme du deni.
- **Communiquer trop vite sur la recovery** : annoncer "la page est tournee" avant que les actions correctives ne soient mises en oeuvre est percu comme de l'arrogance.
- **Changer de direction sans explication** : si des dirigeants sont remplaces suite a la crise, communiquer sur les raisons et la vision du successeur.
- **Oublier les collaborateurs** : les collaborateurs sont les premiers ambassadeurs (ou les premiers detracteurs) post-crise. Investir massivement dans la communication interne pendant la phase de recovery.

---

## State of the Art (2024-2026)

### IA Generative et Communication de Crise

L'IA generative transforme la communication de crise dans les deux sens :
- **Cote menace** : generation de deepfakes, de faux communiques, de desinformation automatisee a grande echelle. Les crises de demain pourraient etre declenchees par des contenus entierement fabriques (video deepfake d'un dirigeant, faux communique de presse). Preparer des protocoles d'authentification rapide (filigrane, verification multi-canal).
- **Cote outil** : l'IA permet de generer des premiers jets de holding statements, Q&A et elements de langage en quelques minutes, d'analyser le sentiment en temps reel sur des milliers de sources, et de simuler des scenarios de crise pour l'entrainement. Mais la validation humaine reste indispensable pour la justesse du ton, l'empathie et la conformite juridique.
- **Crise de l'IA elle-meme** : les organisations qui deploient des systemes d'IA doivent se preparer a des crises specifiques (biais algorithmique, hallucinations, fuite de donnees via l'IA). Integrer les scenarios "IA" dans la typologie des crises.

### Crises Cyber et Data Breach

Les cyber-attaques (ransomware, DDoS, data breaches) sont devenues la premiere source de crises pour les grandes organisations :
- **Cadre reglementaire renforce** : le RGPD impose une notification a la CNIL dans les 72 heures et une notification aux personnes concernees si risque eleve. La directive NIS2 (en vigueur depuis octobre 2024) etend les obligations de notification pour les operateurs de services essentiels.
- **Communication technique et humaine** : les crises cyber exigent de communiquer sur des sujets techniques (type de vulnerabilite, donnees compromises) de maniere comprehensible pour le grand public. Vulgariser sans minimiser.
- **Coordination avec les autorites** : ANSSI, CNIL, forces de l'ordre. La communication publique doit etre coordonnee avec les autorites pour ne pas compromettre les enquetes.
- **Dark web monitoring** : surveiller le dark web pour detecter la mise en vente de donnees volees et anticiper les vagues mediatiques.

### Crise Climatique et Environnementale

Les crises environnementales gagnent en intensite et en frequence :
- **Devoir de vigilance** : la loi francaise sur le devoir de vigilance (2017) et la directive europeenne CSDDD (Corporate Sustainability Due Diligence Directive, 2024) imposent aux grandes entreprises de prevenir les atteintes a l'environnement et aux droits humains dans leur chaine de valeur. Les manquements sont desormais une source majeure de crises.
- **Activisme actionnarial** : des fonds d'investissement et des ONG deposent des resolutions climatiques en assemblee generale. Preparer la communication pour ces confrontations publiques.
- **Litigation climatique** : les poursuites judiciaires pour inaction climatique se multiplient (Total, Shell, BNP). Preparer la communication juridico-mediatique pour ce type de contentieux au long cours.

### Polarisation et Cancel Culture

La polarisation des debats publics cree de nouveaux types de crises :
- **Prise de position piegeuse** : les entreprises sont sommees de prendre position sur des sujets politiques et societaux (diversite, droits reproductifs, conflits internationaux). Chaque position peut generer un boycott d'un segment de parties prenantes.
- **Framework de decision** : avant de prendre position, evaluer selon trois criteres : (1) le sujet est-il en lien avec la raison d'etre de l'organisation ? (2) les collaborateurs attendent-ils une prise de position ? (3) l'organisation est-elle coherente et exemplaire sur ce sujet ?
- **Cancelation de dirigeants** : les prises de parole personnelles des dirigeants (reseaux sociaux, interviews) peuvent generer des crises corporate. Former les dirigeants a la gestion de leur personal branding et definir les limites entre expression personnelle et engagement corporate.

### Exercices de Simulation de Crise

Les exercices de simulation sont devenus plus sophistiques et realistes :
- **War rooms immersives** : simulation en temps reel avec flux d'informations (faux articles, faux tweets, faux appels de journalistes) injectes par une equipe "adverse" (red team).
- **Simulations hybrides** : exercices combinant crise operationnelle et crise mediatique avec participation des equipes communication, operations, juridique et direction generale.
- **Tests de dark site** : exercice technique d'activation du dark site avec mise en ligne reelle sur un domaine de test.
- **Debriefing video** : enregistrement video des simulations pour un debriefing detaille des performances des porte-paroles (verbal, non-verbal, gestion du stress).
- **Frequence recommandee** : minimum 1 exercice complet par an, 2 exercices thematiques (cyber, environnement, social) supplementaires. Les exercices doivent inclure les dirigeants, pas seulement les equipes communication.
