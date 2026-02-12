# Études de cas — Code Excellence

## Cas 1 : Réduction de la dette technique d'un legacy codebase

### Contexte
FinApp, startup fintech de 35 personnes, maintient une application de gestion de trésorerie développée en 4 ans. Le codebase TypeScript/React/Node.js compte 180K lignes de code avec une couverture de tests de 22%. La vélocité de l'équipe (8 développeurs) a chuté de 40% en 18 mois. Chaque nouvelle feature nécessite des modifications dans 15-20 fichiers en moyenne.

### Problème
Le code accumule une dette technique massive : 47 God Classes (> 500 lignes), duplication de logique métier dans 3 couches différentes (API, services, composants React), et zéro test sur le module de calcul de trésorerie prévisionnelle (le plus critique). Les bugs de régression augmentent de 20% par trimestre. Le onboarding d'un nouveau développeur prend 6 semaines avant le premier commit productif. Le CTO estime que 60% du temps de développement est consacré à la compréhension du code existant.

### Approche
1. **Diagnostic par hotspots** : Analyse de churn via `git log` (fichiers les plus modifiés) croisée avec la complexité cyclomatique (SonarQube). Identification de 12 fichiers "hotspots" responsables de 65% des bugs — priorité absolue de refactoring.
2. **Tests de caractérisation** : Avant tout refactoring, écriture de 200+ tests de caractérisation sur les modules critiques (calcul de trésorerie, moteur de pricing, réconciliation bancaire) pour capturer le comportement existant. Mutation testing avec Stryker pour valider la qualité des tests (mutation score initial : 35%, cible : 80%).
3. **Refactoring incrémental** : Application systématique du Boy Scout Rule + sessions dédiées (20% du sprint). Extraction des God Classes en modules cohérents (principe SRP), introduction de Value Objects (Money, AccountId, DateRange) pour remplacer les primitives, mise en place du pattern Ports & Adapters pour isoler la logique métier.
4. **Quality gates en CI** : Configuration de SonarQube avec des portes strictes : zéro nouveau code smell bloquant, couverture minimum de 80% sur le nouveau code, complexité cyclomatique < 10 par fonction.

### Résultat
- Couverture de tests passée de 22% à 68% en 6 mois (90%+ sur la logique métier critique)
- Mutation score passé de 35% à 78%
- Bugs de régression réduits de 45% par trimestre
- Vélocité de l'équipe remontée de 40% (retour au niveau initial)
- Onboarding réduit de 6 semaines à 2 semaines grâce à la meilleure lisibilité
- Les 12 fichiers hotspots refactorés en modules de < 200 lignes avec responsabilités claires

### Leçons apprises
- L'analyse de churn × complexité est le meilleur prioriseur de refactoring — cibler les fichiers qui changent souvent ET qui sont complexes, pas la dette technique "théorique".
- Les tests de caractérisation avant refactoring sont non-négociables — sans eux, le refactoring introduit plus de bugs qu'il n'en corrige.
- Le 20% du sprint dédié au refactoring est un investissement rentable dès le 2ème trimestre en vélocité récupérée.

---

## Cas 2 : Transformation TDD dans une équipe produit

### Contexte
CloudSecure, éditeur SaaS de cybersécurité (60 personnes, 15 développeurs), développe un dashboard de monitoring de sécurité en React/TypeScript avec un backend Go. L'équipe ship des features rapidement mais accumule des bugs critiques en production : 12 incidents P1 en 3 mois, principalement sur la logique de détection d'alertes et le scoring de risque.

### Problème
L'équipe pratique le "test-after" — les tests sont écrits après le code, souvent sous pression de deadline, et se limitent à valider les happy paths. Le module de scoring de risque (200 règles métier) a une couverture de 40% mais un mutation score de seulement 15% — les tests existent mais ne valident rien de significatif. Les code reviews prennent 3 jours en moyenne car les PRs font 800-1200 lignes sans tests pertinents.

### Approche
1. **Formation TDD immersive** : Workshop de 3 jours avec un coach externe sur le cycle Red-Green-Refactor, kata de code (Bowling, Mars Rover, Banking), puis application sur le codebase réel. Focus sur le "outside-in TDD" adapté au développement produit.
2. **Pair programming systématique** : 2 semaines de pair programming obligatoire entre développeurs formés et non-formés. Un développeur senior "TDD champion" par squad pour accompagner la transition.
3. **Trunk-based development** : Migration du feature branching (branches de 5-10 jours) vers le trunk-based development avec branches < 1 jour et feature flags (LaunchDarkly). Les PRs passent de 800+ lignes à 150-200 lignes.
4. **Mutation testing en CI** : Intégration de Stryker dans le pipeline CI avec un seuil minimum de mutation score de 70% sur le nouveau code. Les PRs qui baissent le mutation score sont bloquées.

### Résultat
- Incidents P1 réduits de 12 à 2 par trimestre (÷6)
- Mutation score du module de scoring passé de 15% à 82%
- Temps de code review réduit de 3 jours à 4 heures (PRs plus petites, tests comme documentation)
- Les développeurs reportent une confiance accrue : 85% se sentent "en sécurité" pour refactorer (vs 20% avant)
- Temps de développement par feature initialement +30% (apprentissage TDD), puis -15% après 3 mois (moins de bugs, moins de rework)

### Leçons apprises
- Le TDD n'est pas une pratique de test mais une pratique de design — il force à penser aux interfaces et aux comportements avant l'implémentation.
- Le pair programming est le vecteur de transmission le plus efficace pour le TDD — les formations seules ne suffisent pas.
- Le trunk-based development est le catalyseur naturel du TDD : des PRs petites et fréquentes nécessitent des tests solides pour maintenir la confiance.

---

## Cas 3 : Mise en place d'une culture de code review efficace

### Contexte
EduTech, scale-up EdTech de 45 personnes (18 développeurs répartis en 3 squads), développe une plateforme d'apprentissage en ligne. Le processus de code review existe mais est dysfonctionnel : les PRs stagnent 4-5 jours, les reviewers se concentrent sur le style plutôt que la logique, et les développeurs juniors reçoivent des feedback peu constructifs ("c'est pas comme ça qu'on fait ici").

### Problème
Le temps moyen de cycle (du premier commit au merge) est de 7 jours, dont 4-5 jours d'attente en review. Les reviewers approuvent sans commentaire ("LGTM" automatique) sur 40% des PRs. 3 développeurs juniors envisagent de quitter l'entreprise, citant les reviews comme source principale de frustration. Les bugs en production augmentent car la review ne détecte que des problèmes cosmétiques.

### Approche
1. **Refonte du processus** : Limitation des PRs à 400 lignes de diff maximum (exception documentée au-delà). Assignation automatique des reviewers par rotation via CODEOWNERS. SLA de review : première réponse sous 4 heures ouvrées.
2. **Checklist de review structurée** : Introduction d'une checklist PR couvrant 10 critères : logique métier, sécurité (OWASP), performance (N+1, pagination), tests (cas nominaux + edge cases), typage strict, error handling, accessibilité, rétrocompatibilité API. Chaque reviewer doit valider chaque critère explicitement.
3. **AI-assisted first pass** : Déploiement de CodeRabbit comme premier reviewer automatique. L'IA détecte les problèmes de style, les code smells, les potentiels bugs et les violations de patterns. Les reviewers humains se concentrent sur la logique métier, le design et les questions architecturales.
4. **Culture de feedback constructif** : Formation de 2 heures sur le feedback constructif en code review. Règle : chaque commentaire critique doit être accompagné d'une suggestion concrète ou d'un exemple. Introduction de "comment types" : 🔴 Bloquant, 🟡 Suggestion, 💡 Apprentissage.

### Résultat
- Cycle time réduit de 7 jours à 1.5 jour (÷4.7)
- Temps de première réponse passé de 4-5 jours à 3 heures
- PRs "LGTM sans commentaire" réduites de 40% à 8%
- Bugs détectés en review augmentés de 3× (logique et sécurité vs style)
- eNPS développeur passé de -5 à +32
- Zéro départ dans les 6 mois suivants — les juniors citent les reviews comme source d'apprentissage

### Leçons apprises
- La taille des PRs est le facteur #1 de qualité de review — au-delà de 400 lignes, la qualité de relecture chute drastiquement.
- L'IA comme premier reviewer libère les humains pour la réflexion de haut niveau — mais ne remplace jamais le jugement humain sur la logique métier.
- Le feedback constructif est une compétence qui s'apprend — investir dans la formation transforme la culture d'équipe en quelques semaines.
