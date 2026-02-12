# Études de cas — Juridique / Legal

## Cas 1 : Programme de mise en conformité RGPD

### Contexte
HealthData, éditeur de logiciels de santé (150 personnes, 18M€ CA), traite des données de santé pour 800 établissements de santé. En tant qu'hébergeur de données de santé (HDS), l'entreprise est soumise à des exigences RGPD renforcées.

### Problème
Un contrôle CNIL révèle des manquements majeurs : registre des traitements incomplet (35% des traitements manquants), pas de DPO nommé, DPIA non réalisée sur le traitement principal, délai de réponse aux demandes de droits de 45 jours (vs 30 jours réglementaires), et 3 sous-traitants sans DPA conforme. La CNIL accorde 6 mois pour se mettre en conformité.

### Approche
1. **Nomination d'un DPO et gouvernance** : Recrutement d'un DPO expérimenté, création d'un comité privacy trimestriel, formation de 15 "privacy champions" dans les équipes.
2. **Registre des traitements** : Cartographie exhaustive de 120 traitements avec base légale, finalité, durée de conservation et mesures de sécurité documentées.
3. **DPIA** : Analyse d'impact sur les 8 traitements à risque élevé (données de santé), identification de 23 mesures de mitigation.
4. **Droits des personnes** : Automatisation du processus de réponse (portail dédié, workflow ServiceNow) avec délai cible de 15 jours.
5. **Mise en conformité des sous-traitants** : Audit des 45 sous-traitants, négociation et signature de DPA conformes, résiliation de 3 sous-traitants non conformes.

### Résultat
- Contrôle CNIL de suivi positif — mise en demeure levée
- 120 traitements documentés avec 100% de bases légales identifiées
- Délai de réponse aux demandes de droits réduit de 45 à 12 jours
- 100% des sous-traitants sous DPA conforme
- Certification HDS renouvelée avec mention de l'excellence du dispositif RGPD

### Leçons apprises
- L'automatisation du processus de droits (portail + workflow) est indispensable au-delà de 100 demandes/an.
- Les privacy champions dans les équipes sont plus efficaces qu'un DPO isolé — la conformité se fait au quotidien, pas dans un bureau.
- La DPIA n'est pas un exercice documentaire — les 23 mesures identifiées ont réellement amélioré la sécurité des données.

---

## Cas 2 : Automatisation du cycle de vie contractuel

### Contexte
ConsultiGroup, cabinet de conseil (800 personnes, 120M€ CA), gère 2 500 contrats actifs. La direction juridique (6 juristes) traite 150 demandes de contrats/mois (NDA, prestations, sous-traitance, partenariats).

### Problème
Le délai moyen de traitement d'un contrat est de 18 jours, les juristes passent 65% de leur temps sur des contrats à faible risque (NDA, contrats standards), et 12% des contrats se renouvellent par tacite reconduction sans revue. 3 litiges récents (total : 800K€) auraient été évités par une meilleure revue contractuelle.

### Approche
1. **Classification des contrats** : Matrice de risque à 4 niveaux (faible/moyen/élevé/critique) avec processus de validation adapté et délais cibles différenciés.
2. **Template library** : Création de 15 templates pré-validés couvrant 80% des besoins récurrents, avec playbook de négociation (positions, lignes rouges, concessions).
3. **CLM (Contract Lifecycle Management)** : Déploiement de Tomorro — création depuis templates, workflow d'approbation, signature DocuSign intégrée, alertes d'échéance.
4. **Self-service contractuel** : Les opérationnels peuvent générer un NDA ou un contrat standard directement depuis le CLM, sans passer par le juridique.
5. **Analytics juridiques** : Dashboard de pilotage (délais, volumes, contentieux, échéances) pour optimiser l'allocation des ressources.

### Résultat
- Délai moyen de traitement réduit de 18 à 5 jours (NDA : < 24h en self-service)
- Temps juristes sur contrats à faible risque réduit de 65% à 20% (libéré pour le conseil stratégique)
- Zéro renouvellement tacite non voulu (alertes d'échéance automatiques)
- Contentieux contractuels réduits de 40% (meilleure qualité de revue sur les contrats à risque)

### Leçons apprises
- Le self-service contractuel ne dévalue pas la fonction juridique — il la libère pour les sujets à forte valeur ajoutée.
- Le playbook de négociation (positions pré-validées) accélère les négociations de 50% en réduisant les allers-retours internes.
- Les alertes d'échéance sont le ROI le plus immédiat d'un CLM — un seul renouvellement tacite évité rembourse l'investissement.

---

## Cas 3 : Stratégie de protection de la propriété intellectuelle pour une startup deeptech

### Contexte
QuantumSense, startup deeptech de 35 personnes développant des capteurs quantiques pour l'industrie, a levé 12M€ en série A. L'innovation repose sur 3 technologies core développées par les fondateurs (anciens chercheurs CNRS).

### Problème
Aucune protection PI n'est en place : pas de brevet déposé, les chercheurs publient leurs travaux sans stratégie de protection préalable, 2 composants open source sont utilisés sans audit de licence, et un concurrent chinois a déposé un brevet similaire à l'une des technologies. La valorisation de la série B dépend fortement du portefeuille PI.

### Approche
1. **Audit PI complet** : Cartographie des actifs intellectuels (inventions, logiciels, marques, savoir-faire), analyse freedom-to-operate vis-à-vis du brevet concurrent chinois.
2. **Stratégie brevets** : Dépôt de 5 brevets prioritaires via le PCT (Patent Cooperation Treaty) couvrant les 3 technologies core, avec extensions nationales ciblées (US, UE, Japon, Corée).
3. **Politique de publication** : Processus de validation systématique avant toute publication scientifique — le juridique vérifie qu'aucune divulgation ne compromet un dépôt de brevet en cours.
4. **Audit open source** : Scan complet du code avec un outil dédié (FOSSA), identification de 2 composants GPL incompatibles avec la licence propriétaire, remplacement par des alternatives MIT/Apache.
5. **Protection du savoir-faire** : Clauses de confidentialité renforcées, politique de secret des affaires formalisée, classification des documents sensibles.

### Résultat
- 5 brevets PCT déposés, premiers examens favorables reçus
- Analyse freedom-to-operate concluante : le brevet concurrent chinois ne couvre pas les innovations de QuantumSense
- Risque open source éliminé (2 composants GPL remplacés)
- Portefeuille PI valorisé à 8M€ par les investisseurs dans la due diligence série B
- Série B de 25M€ bouclée à une valorisation de 80M€ (PI citée comme facteur clé)

### Leçons apprises
- La PI dans une deeptech représente 30-50% de la valorisation — ne pas investir dans sa protection est une erreur stratégique majeure.
- La publication scientifique et la protection PI sont compatibles si le processus de validation est en place AVANT la publication.
- L'audit open source est non-négociable — une contamination GPL découverte lors d'une due diligence peut faire échouer une levée de fonds.
