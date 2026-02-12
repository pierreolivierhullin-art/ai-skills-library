# Études de cas — Gestion de projets

## Cas 1 : Transformation agile d'une DSI bancaire

### Contexte
BankTech, DSI d'une banque régionale de 2 000 collaborateurs, gère 45 projets en parallèle avec des méthodologies waterfall. L'équipe IT de 120 personnes livre en moyenne 2 releases majeures par an avec un taux d'échec projet de 35%.

### Problème
Les métiers se plaignent de délais de livraison de 12-18 mois, d'un manque de visibilité sur l'avancement, et de livrables qui ne correspondent pas aux besoins initiaux (effet tunnel). Le DSI est mandaté pour réduire le time-to-market de 50%.

### Approche
1. **Pilote agile** : Sélection de 3 projets pilotes pour une transformation Scrum, avec formation de 3 Scrum Masters et 3 Product Owners.
2. **Organisation en squads** : Réorganisation progressive en 8 squads cross-fonctionnelles (dev, QA, ops, UX) alignées sur des domaines métier.
3. **Portfolio management** : Mise en place d'un board de priorisation trimestriel avec les métiers, basé sur la valeur business (WSJF).
4. **Continuous delivery** : Investissement dans une pipeline CI/CD permettant des releases bimensuelles au lieu de semestrielles.

### Résultat
- Time-to-market réduit de 14 mois à 4 mois en moyenne
- Taux de satisfaction métier passé de 45% à 82%
- Taux d'échec projet réduit de 35% à 12%
- Productivité mesurée (story points livrés) en hausse de 65%

### Leçons apprises
- La transformation agile est d'abord un changement culturel, pas un changement de processus — commencer par les pilotes pour prouver la valeur.
- Les Product Owners issus du métier (pas de l'IT) sont un facteur clé de succès.
- La priorisation par la valeur business (WSJF) résout 80% des conflits de priorité.

---

## Cas 2 : Sauvetage d'un projet de migration ERP

### Contexte
AgroDistrib, distributeur agroalimentaire de 500 personnes, migre son ERP vieillissant (AS/400) vers SAP S/4HANA. Le budget est de 2,5M€ sur 18 mois.

### Problème
À mi-parcours (M9), le projet accuse 3 mois de retard, le budget est dépassé de 40%, et les utilisateurs clés sont démotivés par des ateliers de conception interminables. Le sponsor exécutif menace d'arrêter le projet.

### Approche
1. **Audit de santé projet** : Diagnostic indépendant identifiant 3 causes racines — périmètre non maîtrisé (scope creep de 60%), gouvernance floue, et dette de test accumulée.
2. **Rescoping** : Réduction du périmètre au MVP (3 processus critiques : commande-livraison, facturation, stock) et report des fonctionnalités secondaires en phase 2.
3. **Gouvernance renforcée** : COPIL bimensuel avec pouvoir de décision, RACI clarifié, et war room quotidienne pendant les 3 derniers mois.
4. **Plan de test intensif** : 4 semaines de tests intégrés avec les utilisateurs métier, correction des bugs bloquants en temps réel.

### Résultat
- Go-live réussi avec 2 mois de retard (vs 6 mois projetés sans intervention)
- Budget final : 3,1M€ (+24% vs initial, mais -15% vs trajectoire avant rescoping)
- 95% des processus critiques opérationnels dès J+1
- Phase 2 lancée 6 mois après avec les leçons du MVP

### Leçons apprises
- Le scope creep est le premier tueur de projets ERP — définir le MVP dès le début et résister à l'ajout de fonctionnalités.
- Un audit de santé projet indépendant à mi-parcours devrait être systématique pour les projets > 1M€.
- Les tests avec les vrais utilisateurs (pas les consultants) sont non négociables.

---

## Cas 3 : Mise en place d'un PMO dans un groupe multi-sites

### Contexte
TechGroup, groupe technologique de 800 personnes réparti sur 4 filiales, lance simultanément 25+ projets transverses. Il n'existe pas de PMO central.

### Problème
Chaque filiale pilote ses projets en silo, avec des méthodologies et outils différents. 30% des projets sont en doublon, les ressources partagées sont sur-allouées, et il n'y a aucune visibilité consolidée pour le COMEX.

### Approche
1. **Création du PMO** : Recrutement d'un directeur PMO et de 2 PM seniors, rattachement direct au COO.
2. **Framework unifié** : Méthodologie hybride (waterfall pour les projets réglementaires, agile pour les projets produit) avec des gates communes.
3. **Portfolio management** : Scoring et priorisation des 25 projets sur 4 critères (valeur stratégique, urgence, faisabilité, interdépendances) → 8 projets prioritaires identifiés.
4. **Outillage et reporting** : Déploiement de Monday.com avec des dashboards portfolio consolidés, reporting mensuel au COMEX.

### Résultat
- 6 projets en doublon identifiés et fusionnés (économie de 800K€)
- Taux de livraison dans les délais passé de 40% à 72%
- Satisfaction des sponsors passée de 3,2/5 à 4,1/5
- Visibilité COMEX : reporting consolidé en temps réel

### Leçons apprises
- Le PMO doit être un enabler, pas un contrôleur — les chefs de projet doivent y voir un service, pas une contrainte.
- La priorisation du portfolio est la première valeur ajoutée du PMO — savoir dire "pas maintenant" est essentiel.
- Le rattachement au COMEX (pas à l'IT) est crucial pour la légitimité transverse du PMO.
