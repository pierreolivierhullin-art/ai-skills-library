# RGPD — Conformite Operationnelle

## Vue d'Ensemble

Le RGPD (Reglement General sur la Protection des Donnees, entree en vigueur mai 2018) impose des obligations concretes a toute organisation traitant des donnees personnelles de personnes en UE. Ce document couvre l'implementation pratique : registre de traitement, gestion des droits, notification de violation, et gestion du consentement.

---

## Le Registre de Traitement (Article 30)

### Qui est concerne

Obligatoire pour :
- Organisations de plus de 250 salaries
- Toute organisation traitant des donnees sensibles (sante, origine ethnique, etc.)
- Toute organisation effectuant des traitements "susceptibles de comporter un risque"

Recommande pour toutes les autres — la CNIL encourage une approche proportionnee.

### Structure du Registre

**Pour le Responsable de Traitement** :

| Champ | Exemple | Obligatoire |
|---|---|---|
| Nom et coordonnees du RT | "ACME SAS, DPO@acme.fr" | Oui |
| Finalite du traitement | "Gestion de la paie" | Oui |
| Categories de personnes | "Salaries, ex-salaries" | Oui |
| Categories de donnees | "Nom, IBAN, salaire" | Oui |
| Base legale | "Obligation legale (Code du travail)" | Oui |
| Destinataires | "Cabinet comptable, URSSAF" | Oui |
| Transferts hors UE | "Aucun" ou pays + garanties | Oui |
| Duree de conservation | "5 ans apres depart du salarie" | Recommande |
| Mesures de securite | "Acces restreint, chiffrement" | Recommande |

**Pour le Sous-traitant** :

Registre separé incluant : categories de traitements pour chaque RT, transferts hors UE, mesures de securite.

### Template de Fiche de Traitement

```
FICHE DE TRAITEMENT N°007

Nom du traitement : Gestion du recrutement
Responsable : DRH — Marie Dupont
Date de creation : 2024-03-15
Derniere mise a jour : 2025-01-10

FINALITE
Recevoir et gerer les candidatures spontanees et en reponse a des offres d'emploi.
Evaluer les candidats et conserver les profils pertinents pour de futures opportunites.

PERSONNES CONCERNEES
Candidats externes (y compris les candidatures spontanees)

DONNEES COLLECTEES
- Identite : nom, prenom, adresse email, telephone
- CV : formation, experience professionnelle
- Lettre de motivation
- Resultats de tests (si applicable)
Note : Ne pas collecter : photo (sauf si le candidat l'inclut), situation familiale,
       nationalite, informations medicales

BASE LEGALE
Interet legitime du responsable de traitement (evaluer les candidatures)
Pour les candidatures conservees au-dela du recrutement : consentement explicite

DUREE DE CONSERVATION
Candidatures non retenues : 2 ans apres le dernier contact
Candidatures retenues (embauche) : duree du contrat + 5 ans (archive)

DESTINATAIRES
- Equipe RH (acces complet)
- Managers operationnels (acces au CV et lettre uniquement)
- Cabinet de recrutement externe : [Nom], DPA signe le [date]

TRANSFERTS HORS UE
Aucun (ATS heros en France / UE)

MESURES DE SECURITE
- ATS avec acces restreint par profil
- Mot de passe complexe + MFA
- Pas de transmission par email non chiffre
- Suppression automatique apres 2 ans (parametre ATS)

DROITS DES PERSONNES
Point de contact : rgpd@acme.fr
Delai de reponse : 30 jours maximum
```

---

## Gestion des Droits des Personnes

### Processus de traitement des demandes

```
Reception de la demande (email, courrier, formulaire)
        |
        ↓
Verification d'identite (Article 12)
  → Demander piece d'identite si doute raisonnable
  → Ne pas demander systematiquement (principe de proportionnalite)
        |
        ↓
Qualification de la demande
  → Quel droit est exerce ?
  → L'exception s'applique-t-elle ? (ex: conservation pour obligations legales)
        |
        ↓
Traitement interne (impliquer les equipes techniques)
  → DSI pour extraction/suppression des donnees
  → Metier pour validation du perimetre
        |
        ↓
Reponse a la personne : delai maximum 1 mois
  (extensible 2 mois si complexe — notifier la personne dans le 1er mois)
        |
        ↓
Documentation dans le registre des demandes
```

### Tableau des droits et exceptions

| Droit | Conditions | Exceptions principales |
|---|---|---|
| **Acces** (Art. 15) | Toujours | Droits tiers (ex: donnees d'autres personnes dans le document) |
| **Rectification** (Art. 16) | Donnees inexactes ou incompletes | — |
| **Effacement** (Art. 17) | Consentement retire, finalite atteinte, opposition legitime | Obligation legale de conservation, liberte d'expression, sante publique |
| **Limitation** (Art. 18) | Contestation exactitude, traitement illicite, pendant verifiation | — |
| **Portabilite** (Art. 20) | Uniquement si base = consentement ou contrat, traitement automatise | Ne couvre pas les donnees derivees |
| **Opposition** (Art. 21) | Base = interet legitime ou mission de service public | Motifs legitimes imperieux du RT |

### Template de Reponse a une Demande d'Acces

```
Objet : Suite a votre demande d'exercice de droit d'acces — ref. DA-2025-042

Madame/Monsieur [Nom],

Suite a votre demande du [date], nous avons bien traite votre demande d'acces a
vos donnees personnelles conformement a l'article 15 du RGPD.

Vous trouverez ci-joint/ci-dessous l'ensemble des donnees personnelles que nous
detenons vous concernant :

[Liste ou fichier joint]

Ces donnees sont issues des traitements suivants :
- [Traitement 1] : [liste de donnees]
- [Traitement 2] : [liste de donnees]

Informations complementaires :
- Duree de conservation : [preciser par traitement]
- Destinataires : [preciser]
- Droit de reclamation : Si vous estimez que le traitement porte atteinte a vos
  droits, vous pouvez introduire une reclamation aupres de la CNIL
  (www.cnil.fr, 3 place de Fontenoy, 75007 Paris).

Nous restons a votre disposition pour toute question complementaire.

[Signature DPO ou responsable RGPD]
```

---

## Notification de Violation de Donnees (Article 33-34)

### Arbre de decision : notifier ou pas ?

```
Violation detectee (acces non autorise, perte, divulgation)
        |
        ↓
La violation concerne-t-elle des donnees personnelles ?
  NON → Pas d'obligation RGPD (appliquer la politique securite interne)
  OUI ↓
        |
        ↓
La violation est-elle "susceptible d'engendrer un risque" ?
  NON (ex: donnees chiffrees perdues, cle inaccessible) → Documenter uniquement
  OUI ↓
        |
        ↓
NOTIFIER LA CNIL dans les 72 heures
        |
        ↓
La violation est-elle susceptible d'engendrer un "risque eleve" ?
  (ex: donnees de sante, données financieres, vol d'identite probable)
  OUI → INFORMER LES PERSONNES CONCERNEES "sans delai inutile"
  NON → Pas d'obligation d'informer les personnes
```

### Contenu de la notification CNIL (Article 33)

```
1. Description de la nature de la violation
   - Type : acces non autorise / perte / destruction / divulgation
   - Date et duree
   - Systeme(s) concerne(s)

2. Categories et nombre approximatif de personnes concernees
   Ex : "Environ 3 000 clients particuliers"

3. Categories et nombre approximatif d'enregistrements concernes
   Ex : "Noms, emails, numeros de telephone, historique d'achats"

4. Coordonnees du DPO ou point de contact

5. Consequences probables de la violation
   Ex : "Risque d'hameconnage cible sur les personnes concernees"

6. Mesures prises ou envisagees
   Ex : "Acces coupe immediatement, reinitialisation des credentials,
         audit en cours, information des personnes prevue sous 48h"
```

Notification via le portail en ligne de la CNIL : notifications.cnil.fr

### Playbook Violation de Donnees (72h)

```
H+0 — Detection
  ✓ Alerter immediatement : DPO, RSSI, Direction
  ✓ Couper les acces compromis
  ✓ Constituer la cellule de crise (DPO, RSSI, Juridique, Comms)

H+4 — Evaluation initiale
  ✓ Determiner : quelles donnees, combien de personnes, comment
  ✓ Evaluer le risque : risque normal ou eleve pour les personnes ?
  ✓ Decider : notification CNIL requise ?

H+24 — Premiere notification CNIL (si possible)
  ✓ Notification initiale meme si incomplete ("nous compiletons notre enquete")
  ✓ La CNIL accepte les notifications provisoires completees par la suite

H+48 — Communication interne
  ✓ Briefing de la direction et du management
  ✓ Preparation de la communication externe si besoin

H+72 — Notification CNIL complete
  ✓ Notification complete si la premiere etait provisoire
  ✓ Decision sur l'information des personnes concernees

H+72 a H+96 — Information des personnes (si risque eleve)
  ✓ Email direct ou communication par voie de presse (si impossible de contacter individuellement)
  ✓ Conseils pratiques aux personnes (changer mot de passe, surveiller les tentatives de phishing)

Post-crise
  ✓ Rapport d'incident interne complet
  ✓ Mesures correctives implementees
  ✓ Documentation dans le registre des violations
  ✓ Retour d'experience formel avec toutes les parties prenantes
```

---

## Gestion du Consentement et des Cookies

### Conditions de validite du consentement (Article 7)

- **Libre** : pas conditionne a un service (pas de cookie wall*)
- **Specifique** : une finalite, un consentement (pas de consentement global)
- **Eclaire** : information claire sur qui, pourquoi, comment
- **Univoque** : action positive (pas de case pre-cochee, pas d'inaction = consentement)
- **Retirable** : aussi facile de retirer le consentement que de le donner

*Exception "cookie wall" : accepte par certaines autorites nationales si une alternative payante est proposee (arret CJUE, nov. 2023).

### Exigences de la CNIL sur les cookies

**Cookies soumis au consentement** :
- Publicite comportementale
- Analytics (si Google Analytics ou similaire sans configuration privacy-first)
- Reseaux sociaux (plugins "Like", "Share" qui deposent des cookies tiers)
- Cookies de personnalisation non necessaires

**Cookies exempts de consentement** :
- Cookies de session (panier e-commerce, authentification)
- Mesure d'audience strictement interne, anonyme, sans transfert hors UE (ex: Matomo bien configure)
- Cookies de securite (CSRF, load balancer)

**Interface de consentement conforme** :
- Bouton "Accepter tout" ET bouton "Refuser tout" de meme niveau d'importance
- Lien vers les preferences granulaires
- Pas de dark patterns : pas de bouton "Refuser" en gris pâle
- Renouveler le consentement au maximum tous les 13 mois

**CMP (Consent Management Platform)** recommandees : Didomi, Axeptio, Usercentrics, OneTrust. Verifier la liste de reference CNIL pour les CMP ayant obtenu un label.

---

## DPO — Data Protection Officer

### Quand le DPO est obligatoire (Article 37)

- Autorite ou organisme public
- Traitement a grande echelle de donnees sensibles (sante, judiciaire, etc.)
- Surveillance systematique et a grande echelle (ex: operateur telecom, assureur)

Pour les autres : recommande mais pas obligatoire.

### Profil et competences du DPO

- Connaissance du droit (RGPD, droit national, jurisprudence)
- Competences techniques (architecture des donnees, securite)
- Competences metier (comprendre les processus de l'organisation)
- Independance : ne peut pas recevoir d'instructions sur ses missions RGPD

**DPO interne vs externe** :

| Critere | Interne | Externe (prestataire) |
|---|---|---|
| Cout | Salaire ETP | 10-30k EUR/an (TPE/PME) |
| Disponibilite | Temps plein possible | Limitee (quelques jours/mois) |
| Connaissance interne | Elevee | A construire |
| Independance | Risque de pression | Plus facile |
| Adapte pour | Grandes organisations | TPE/PME/ETI |

### Missions du DPO (Article 39)

- Informer et conseiller le RT/ST et les employes
- Controler le respect du RGPD
- Conseiller sur la DPIA et en controler l'execution
- Cooperer avec l'autorite de controle (CNIL)
- Etre le point de contact pour la CNIL
- Registre de traitement a jour
