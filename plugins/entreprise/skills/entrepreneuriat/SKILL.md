---
name: entrepreneuriat
version: 1.0.0
description: >
  Use this skill when the user asks about "entrepreneuriat", "créer une startup", "business plan", "business model canvas", "product-market fit", "go-to-market", "early stage", "validation d'idée", "pivot", "lean startup", "MVP", "ICP ideal customer profile", "customer discovery", "early adopters", "traction", "MRR", "churn startup", "croissance early stage", "CAC LTV startup", discusses launching a new business, validating a business idea, or needs guidance on the early stages of building a company.
---

# Entrepreneuriat — Early Stage

## Overview

L'entrepreneuriat early-stage n'est pas la mise en oeuvre d'un plan business — c'est un processus de reduction d'incertitude. La majorite des startups echouent non pas faute d'execution, mais faute de validation : le probleme n'existait pas, le marche etait trop petit, ou la solution ne correspondait pas a ce que les clients voulaient vraiment payer.

Ce skill couvre la methodologie du zero au product-market fit : identification du probleme, validation, construction du MVP, acquisition des premiers clients, mesure des metriques critiques et decisions pivot/persevere.

---

## Identification et Validation du Probleme

### Jobs to Be Done (JTBD)

Les clients "embauchent" des produits pour accomplir un "job" — fonctionnel, social ou emotionnel. Comprendre le vrai job, pas la feature.

**Exemple classique** : les clients de MacDonald's qui achetent un milkshake le matin "embauchent" le milkshake pour remplir un trajet de voiture solitaire (job : divertissement + satiete). Ce n'est pas le "produit milkshake" qu'il faut ameliorer, mais le "job de la personne seule dans sa voiture le matin".

**Questions JTBD** :
- "Qu'essayiez-vous d'accomplir quand vous avez cherche cette solution ?"
- "Comment le faisiez-vous avant ?"
- "Qu'est-ce qui vous a frustr dans votre ancienne approche ?"
- "Quand la derniere fois avez-vous eu ce probleme ? Decrivez la situation."

### Le Test du "Probleme Douloureux"

Avant de construire quoi que ce soit, valider que le probleme est :

**Frequent** : le potentiel client rencontre ce probleme au moins 1x/semaine ou 1x/mois (selon le secteur).
**Urgent** : le client passe du temps a chercher une solution actuellement.
**Reconnu** : le client peut articuler le probleme sans que vous le guidiez.
**Budgetise** : de l'argent est deja depense pour resoudre ce probleme (meme imparfaitement).

**Signal positif** : le client vous propose de payer avant que le produit existe (lettre d'intention, pre-commande).
**Signal negatif** : "C'est une bonne idee" sans aucun engagement. Ne signifie rien.

### Customer Discovery — 20 Entretiens Minimum

**Avant de coder** : 20 entretiens de 30-45 min avec des clients cibles potentiels.

**Regles d'or** :
- Ne jamais presenter votre solution dans les premiers 80% de l'entretien
- Demander des faits (passé), pas des opinions sur le futur ("vous utiliseriez X ?" → biais)
- Chercher les formulations exactes que les clients utilisent pour decrire leur probleme

**Template d'entretien problem-discovery** :
1. "Parlez-moi de votre role et de vos responsabilites" (5 min)
2. "Quels sont vos 3 principaux defis en ce moment ?" (5 min)
3. "Comment gerez-vous [probleme identifie] actuellement ?" (10 min)
4. "Montrez-moi comment vous le faites — si possible" (5 min)
5. "Combien de temps cela prend ? Combien cela coute ?" (5 min)
6. "Si vous pouviez changer une chose, ce serait quoi ?" (5 min)

---

## Business Model Canvas (BMC)

### Les 9 Blocs

**1. Segments clients** : qui sont vos clients ? Etre precis (pas "les PME" mais "les DAF de PME industrielles de 50-200 employes en France").

**2. Proposition de valeur** : quel probleme resolvez-vous ? Quelle valeur creez-vous ? Pourquoi maintenant ?

**3. Canaux** : comment atteignez-vous vos clients ? Comment delivrez-vous la valeur ? (online, direct sales, partenaires, app stores)

**4. Relations clients** : quel type de relation avec chaque segment ? (self-serve, account management, communaute)

**5. Sources de revenus** : comment monetisez-vous ? (SaaS, transaction, marketplace, abonnement, publicite)

**6. Ressources cles** : quelles ressources sont indispensables ? (technologie, equipe, donnees, marque)

**7. Activites cles** : quelles activites crees la valeur ? (developpement produit, ventes, algorithme, service)

**8. Partenaires cles** : qui sont vos partenaires et fournisseurs cles ? Quelles ressources mutualisez-vous ?

**9. Structure de couts** : quels sont vos principaux postes de couts ? (fixed vs variable, COGS, salaires)

### Lean Canvas (Ash Maurya)

Variante orientee startup du BMC. Remplace Partenaires, Ressources, Relations par :
- **Probleme** : top 3 problemes
- **Solution** : top 3 features
- **Metriques cles** : comment mesurez-vous le succes ?
- **Avantage incopiable** : ce que vous avez et qu'un concurrent ne peut pas copier

**Outil** : leanstack.com (version en ligne gratuite)

---

## MVP — Minimum Viable Product

### Principes

Le MVP n'est pas le produit le plus petit possible — c'est le produit le plus petit qui permette de tester une hypothese de valeur cle.

**Hypotheses a tester** :
1. Le probleme que je pense observer est reel
2. Les clients valorisent ma solution pour ce probleme
3. Ils sont prets a payer un prix qui rend le modele viable

### Types de MVP

**Landing page MVP** : page simple decrivant le produit, avec formulaire d'inscription. Mesurer : taux de conversion visiteur → inscription. Cout : < 500 EUR, < 1 semaine.

**Concierge MVP** : delivrer manuellement ce que le produit fera automatiquement. Le "service before software". Exemple : Zapier a commence en matchant manuellement les integrations.

**Wizard of Oz MVP** : le client pense que c'est automatise, c'est fait manuellement en coulisses. Valide la demande avant d'automatiser.

**Prototype clickable** : maquette Figma avec laquelle le client peut interagir. Tester le flow sans coder.

**Pre-vente** : vendre le produit avant qu'il existe. La meilleure validation possible.

---

## Go-to-Market Early Stage

### ICP — Ideal Customer Profile

Definir avec precision le client ideal (pas une cible marketing large) :

**B2B ICP** :
- Secteur et taille d'entreprise
- Role et seniority du decision-maker
- Signal de douleur observable (ex : "utilise encore Excel pour X", "vient de lever une Serie A")
- Technologie existante (stack actuelle)
- Geographie et langue

**B2C ICP** :
- Demographique (age, lieu, situation)
- Psychographique (valeurs, centres d'interet, comportement)
- Moment de vie (trigger d'achat)

**Regle** : mieux vaut 1 ICP tres precis que 5 segments vagues. Commencer avec le segment ou la douleur est la plus forte et le chemin vers l'argent le plus court.

### Les 3 Motions de Vente

**Product-Led Growth (PLG)** : le produit lui-meme genere l'acquisition et la conversion. Typique pour les outils SaaS B2SMB. Le "free trial" ou "freemium" est le premier commercial.

**Sales-Led Growth (SLG)** : equipe de vente proactive. Typique pour l'enterprise. Cycle de vente long (3-12 mois), tickets eleves (> 20K EUR ACV).

**Partner-Led Growth** : distribution via des partenaires (integrateurs, revendeurs, ecosystemes). Acces rapide au marche, moins de controle.

**Choix early stage** : commencer par PLG si le ticket est < 5K EUR ACV et si le produit peut etre adopte individuellement. SLG si ticket > 10K EUR et si la decision est collective.

---

## Product-Market Fit

### Definition

Sean Ellis (Dropbox) : "Au moins 40% de vos utilisateurs repondraient 'tres decus' si votre produit disparaissait demain."

Marc Andreessen : "PMF = etre dans un bon marche avec un produit capable de satisfaire ce marche."

### Signaux de PMF

**Signaux positifs** :
- Croissance organique (word of mouth spontane, referrals non-sollicites)
- Retention exceptionnelle (D30 > 40% pour le consommateur, NRR > 100% pour SaaS)
- Les clients vous pardonnent vos bugs (ils restent malgre les problemes)
- Vous ne pouvez plus repondre a toutes les demandes d'acces

**Signaux negatifs** :
- Vous devez convaincre les clients de rester (churn elevé)
- Les referrals ne viennent pas naturellement
- L'equipe passe plus de temps a vendre qu'a iterer sur le produit
- Chaque nouveau client necessite un effort commercial identique

### Metriques de PMF par Modele

**SaaS B2B** :
- NRR (Net Revenue Retention) > 100% → les clients existent et expansent
- Churn mensuel < 2% → les clients restent
- CAC Payback Period < 12 mois → le modele est econome

**B2C / Consumer** :
- D1 retention > 60%, D7 > 30%, D30 > 15%
- Organic acquisition > 30% des nouveaux utilisateurs
- NPS > 50

### Pivot vs Persevere

La decision difficile : quand pivoter, quand perseverer ?

**Pivot** : si apres 6 mois et > 50 clients cibles contacts, la retention est faible et les clients n'utilisent pas le coeur du produit. Revenir aux entretiens problem-discovery.

**Persevere** : si la retention est bonne mais la croissance est lente. Problema d'acquisition, pas de PMF.

**Types de pivots** :
- Customer segment pivot : meme produit, autre client
- Problem pivot : meme client, autre probleme resolu
- Solution pivot : meme probleme, autre solution (technologie differente)
- Channel pivot : meme produit, autre canal de distribution

---

## Metriques Early Stage

### Le Dashboard Fondateur (Pre-PMF)

| Metrique | Definition | Benchmark early stage |
|---|---|---|
| **MRR** | Monthly Recurring Revenue | Croissance > 10-15% MoM = bon |
| **MoM Growth** | Croissance mensuelle du MRR | > 10% = en bonne voie |
| **Churn mensuel** | % clients perdus / mois | < 5% requis, < 2% excellent |
| **NRR** | Net Revenue Retention | > 100% = expansion |
| **CAC** | Cout d'acquisition client | Doit baisser avec le temps |
| **LTV/CAC** | Ratio LTV sur CAC | > 3:1 pour SaaS |
| **Payback period** | Temps pour recuperer le CAC | < 12 mois |
| **Runway** | Mois de cash disponible | Toujours > 12 mois |

### La Regle des 40 (Rule of 40)

Pour les SaaS : Croissance (%) + Profitabilite (%) > 40. Un SaaS qui croit a 80% et perd 20% = score 60, excellent. Un SaaS a 20% de croissance et 20% de profit = score 40, correct.

**En early stage** : se concentrer sur la croissance. La profitabilite vient apres le PMF.

---

## Maturity Model — Startup Early Stage

| Phase | Caracteristique | Priorite |
|---|---|---|
| **0 — Ideation** | Hypothese non testee, pas de clients | Valider le probleme (20 entretiens) |
| **1 — Problem-Solution Fit** | Probleme valide, solution testee (MVP) | Premiers clients payants |
| **2 — Early Traction** | 10-50 clients, MRR initial, churn mesure | Product-market fit signals |
| **3 — PMF** | Retention forte, croissance organique | Optimiser l'acquisition |
| **4 — Scale** | CAC/LTV prouvés, machine de vente | Recruter, lever |
