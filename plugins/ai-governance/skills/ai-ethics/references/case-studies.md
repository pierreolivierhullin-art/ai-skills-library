# Études de cas — Éthique de l'IA & IA Responsable

## Cas 1 : Détection de biais dans un système IA de recrutement

### Contexte
TalentSphère, éditeur SaaS français de 320 salariés spécialisé dans les solutions RH, commercialise un module de présélection automatique des CV utilisé par 180 entreprises clientes. En 2024, une analyse interne révèle des écarts statistiques significatifs dans les taux de présélection selon le genre et l'origine géographique des candidats.

### Problème
Le taux de présélection des candidates féminines pour les postes techniques était inférieur de 34 % à celui des candidats masculins à compétences équivalentes. Les candidats issus de certains départements d'outre-mer affichaient un taux de rejet 28 % supérieur à la moyenne nationale. Deux clients grands comptes menacent de résilier leurs contrats (représentant 1,2 M€ de revenus annuels), et le Défenseur des droits ouvre une enquête préliminaire.

### Approche
1. **Audit de biais algorithmique** : Déploiement d'un framework de détection couvrant 12 attributs protégés (genre, âge, origine, handicap, etc.). Analyse de 450 000 décisions historiques sur 18 mois avec calcul des métriques de parité statistique et d'égalité des chances.
2. **Ré-ingénierie des données d'entraînement** : Suppression des variables proxy corrélées aux attributs protégés (code postal, prénom, photo). Rééquilibrage du dataset par sur-échantillonnage stratifié et introduction de 85 000 profils synthétiques générés par des techniques de data augmentation.
3. **Implémentation d'un module de débiaisage** : Intégration d'un algorithme de post-processing (Equalized Odds) ajustant les seuils de décision par sous-groupe. Mise en place de contraintes de fairness directement dans la fonction de coût du modèle.
4. **Gouvernance et monitoring continu** : Création d'un comité éthique trimestriel incluant 3 représentants clients, 2 experts externes et 1 juriste spécialisé. Déploiement d'un tableau de bord temps réel surveillant 8 métriques de fairness avec alertes automatiques.

### Résultat
- Réduction de l'écart de présélection homme/femme de 34 % à 3,2 % en 4 mois
- Élimination du biais géographique (écart résiduel < 1,5 %)
- Rétention des 2 clients grands comptes et signature de 14 nouveaux contrats (+2,8 M€ ARR)
- Clôture de l'enquête du Défenseur des droits sans sanction

### Leçons apprises
- Les biais les plus dangereux proviennent souvent de variables proxy apparemment neutres (code postal, école) plutôt que de variables directement discriminatoires
- Un audit de biais ponctuel est insuffisant : seul un monitoring continu garantit la pérennité des corrections face à la dérive des données
- L'implication de parties prenantes externes (clients, juristes, société civile) dans la gouvernance éthique renforce la crédibilité et l'acceptabilité des solutions

---

## Cas 2 : Explicabilité d'un modèle de scoring crédit pour conformité RGPD

### Contexte
Banque Méridionale, établissement bancaire régional français comptant 2 400 collaborateurs et 1,1 million de clients particuliers, utilise depuis 2022 un modèle de machine learning (gradient boosting à 280 features) pour le scoring crédit immobilier. La CNIL effectue un contrôle dans le cadre de l'article 22 du RGPD relatif aux décisions automatisées.

### Problème
Le modèle affiche une précision de 94,3 % mais fonctionne comme une boîte noire : les conseillers ne peuvent expliquer aux clients les raisons d'un refus au-delà de formules génériques. Sur les 12 derniers mois, 1 870 réclamations clients portent sur l'opacité des décisions de crédit (hausse de 67 % vs N-1). La CNIL exige sous 6 mois une mise en conformité avec obligation de fournir une explication individuelle, sous peine d'une amende pouvant atteindre 4 % du chiffre d'affaires (soit ~18 M€).

### Approche
1. **Cartographie des exigences réglementaires** : Analyse croisée du RGPD (art. 13-15, 22), de la directive crédit consommation et du futur AI Act (classification haut risque). Définition de 4 niveaux d'explication : technique (data scientists), opérationnel (conseillers), client (langage naturel), régulateur (documentation formelle).
2. **Implémentation SHAP et contrefactuels** : Déploiement de SHAP (SHapley Additive exPlanations) pour la décomposition feature-level de chaque décision. Développement d'un module de contrefactuels indiquant les modifications minimales nécessaires pour obtenir un résultat favorable (ex. : « avec 8 000 € d'apport supplémentaire, votre dossier serait accepté »).
3. **Interface d'explicabilité pour les conseillers** : Création d'un dashboard intégré au poste de travail affichant les 5 facteurs principaux de chaque décision, avec un score de confiance et des suggestions d'actions correctives. Formation de 640 conseillers sur 3 semaines.
4. **Documentation et traçabilité** : Génération automatique de fiches d'explication individuelles au format PDF pour chaque décision. Constitution d'un registre d'explicabilité auditable conservant l'historique de 100 % des décisions sur 5 ans.

### Résultat
- Conformité RGPD validée par la CNIL avec mention « bonnes pratiques » dans le rapport de contrôle
- Réduction des réclamations liées à l'opacité de 67 % en 8 mois (de 1 870 à 620 par an)
- Amélioration du taux de conversion crédit de 12 % grâce aux suggestions d'actions correctives
- Temps d'explication par le conseiller réduit de 25 minutes à 7 minutes par dossier refusé

### Leçons apprises
- L'explicabilité n'est pas un compromis avec la performance : le modèle a conservé 93,8 % de précision après simplification des features redondantes, contre 94,3 % initialement
- Les explications contrefactuelles (« que faudrait-il changer ? ») sont perçues comme nettement plus utiles par les clients que les explications causales (« pourquoi ce résultat ? »)
- La formation des utilisateurs métier est aussi critique que la technique : sans appropriation par les conseillers, les outils d'explicabilité restent sous-utilisés

---

## Cas 3 : Évaluation d'impact IA pour un outil de diagnostic médical

### Contexte
MedVision Analytics, start-up deeptech française de 85 salariés spécialisée en imagerie médicale, développe un algorithme de détection précoce de rétinopathie diabétique à partir de photographies du fond d'oeil. L'outil est en phase de déploiement pilote dans 12 centres ophtalmologiques en Île-de-France, ciblant 45 000 patients diabétiques par an.

### Problème
L'ANSM (Agence nationale de sécurité du médicament) exige une évaluation d'impact algorithmique complète avant l'autorisation de mise sur le marché en tant que dispositif médical de classe IIa. Les tests internes révèlent une sensibilité de 96,1 % globale, mais tombant à 87,3 % sur les peaux foncées (phototypes V-VI), créant un risque de sous-diagnostic pour 22 % de la population cible. Le délai réglementaire imposé est de 9 mois.

### Approche
1. **Cadrage éthique et parties prenantes** : Constitution d'un comité d'évaluation pluridisciplinaire de 14 membres (ophtalmologues, patients, bioéthiciens, juristes santé, représentants associatifs). Cartographie de 23 risques éthiques selon la méthodologie ALTAI de la Commission européenne, priorisés par gravité et probabilité.
2. **Audit de performance différentielle** : Évaluation systématique sur 8 sous-populations (âge, sexe, phototype, comorbidités). Collecte complémentaire de 12 000 images de fonds d'oeil de phototypes V-VI auprès de 4 centres hospitaliers partenaires en Afrique de l'Ouest et aux Antilles. Ré-entraînement du modèle avec dataset enrichi.
3. **Protocole de supervision humaine** : Conception d'un workflow hybride IA-médecin avec double lecture obligatoire pour les cas limites (score de confiance < 85 %). Définition de seuils d'alerte spécifiques par sous-population. Mise en place d'un mécanisme de recours permettant au patient de demander un examen complémentaire.
4. **Documentation AIPD et suivi post-déploiement** : Rédaction d'un dossier d'évaluation d'impact de 180 pages conforme aux exigences de l'AI Act (annexe IV). Implémentation d'un système de pharmacovigilance algorithmique avec reporting trimestriel des incidents et des performances par sous-groupe.

### Résultat
- Sensibilité sur phototypes V-VI remontée de 87,3 % à 94,8 % après ré-entraînement, écart résiduel < 1,5 points vs population générale
- Obtention du marquage CE classe IIa en 7 mois (2 mois avant le délai imposé)
- Déploiement étendu à 38 centres ophtalmologiques couvrant 120 000 patients/an
- Zéro incident de sous-diagnostic grave signalé sur les 9 premiers mois d'exploitation

### Leçons apprises
- L'évaluation d'impact doit commencer dès la phase de conception (by design) et non en fin de développement : les corrections tardives coûtent 3 à 5 fois plus cher
- La diversité du dataset d'entraînement est un enjeu éthique fondamental en santé : un biais de représentation se traduit directement en inégalité d'accès aux soins
- L'implication de patients et de représentants communautaires dans le comité d'évaluation a permis d'identifier des risques invisibles pour les seuls experts techniques (accessibilité, confiance culturelle, consentement éclairé)
