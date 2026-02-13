# Études de cas — Risques IA & Safety

## Cas 1 : Red teaming et tests adversariaux d'un chatbot LLM orienté client

### Contexte
AssurPlus, groupe d'assurance mutualiste français de 4 200 salariés avec 3,8 millions d'assurés, déploie un chatbot conversationnel basé sur GPT-4 pour gérer les demandes de premier niveau (sinistres, garanties, devis). Le chatbot traite en moyenne 28 000 conversations par jour et est accessible 24h/24 sur le site web et l'application mobile.

### Problème
Trois semaines après le lancement, des utilisateurs malveillants publient sur les réseaux sociaux des captures d'écran montrant le chatbot formuler des engagements contractuels non autorisés (« votre sinistre sera remboursé à 100 % sous 48h »), divulguer des informations confidentielles de politique tarifaire interne, et générer des réponses inappropriées via des techniques de jailbreak. L'incident génère 2 300 mentions négatives sur Twitter en 72h et un article dans Les Échos. Le service juridique estime l'exposition potentielle à 4,5 M€ si les engagements générés étaient considérés comme opposables.

### Approche
1. **Constitution d'une équipe de red teaming** : Recrutement d'une cellule de 6 spécialistes (2 pentesters IA, 1 linguiste computationnel, 1 juriste, 2 ingénieurs prompt) complétée par un audit externe de la société Wavestone. Définition de 8 scénarios d'attaque prioritaires : jailbreak, injection de prompt, extraction de données, manipulation émotionnelle, génération d'engagements, usurpation d'identité, déni de service sémantique, et contournement des filtres.
2. **Campagne de tests adversariaux systématiques** : Exécution de 15 000 tentatives d'attaque sur 4 semaines couvrant les 8 scénarios. Utilisation d'outils automatisés (Garak, PromptFoo) combinés à des attaques manuelles créatives. Documentation de 342 vulnérabilités classées par criticité (CVSS adapté IA).
3. **Mise en place de couches de défense** : Déploiement d'un système de guardrails multi-niveaux : filtre d'entrée (détection d'injection), cadrage système renforcé, filtre de sortie (détection d'engagements, PII, tonalité), et circuit-breaker automatique déconnectant la session après 2 tentatives suspectes. Ajout d'un disclaimer juridique dynamique sur chaque réponse engageante.
4. **Programme de red teaming continu** : Mise en place d'un bug bounty interne récompensant les contournements découverts (primes de 200 € à 2 000 €). Tests adversariaux automatisés hebdomadaires sur 500 prompts rotatifs. Revue mensuelle des nouvelles techniques d'attaque publiées par la communauté.

### Résultat
- Taux de réussite des attaques adversariales réduit de 23 % à 0,8 % en 6 semaines
- Zéro incident d'engagement contractuel non autorisé depuis la mise en production des guardrails (11 mois)
- Réduction de 94 % des mentions négatives liées au chatbot sur les réseaux sociaux
- Économie estimée de 4,5 M€ d'exposition juridique évitée

### Leçons apprises
- Le red teaming doit être continu et non ponctuel : les techniques d'attaque évoluent plus vite que les défenses, avec de nouvelles méthodes de jailbreak publiées chaque semaine
- Les guardrails techniques seuls sont insuffisants : la combinaison filtrage d'entrée + cadrage système + filtrage de sortie + circuit-breaker offre une défense en profondeur bien plus robuste
- Les attaques les plus dangereuses ne sont pas les plus sophistiquées techniquement : les manipulations socio-émotionnelles simples (« je suis en détresse, aidez-moi ») contournent plus facilement les filtres que les injections techniques

---

## Cas 2 : Détection et mitigation de la dérive de modèle pour un système de détection de fraude

### Contexte
PaySecure Europe, fintech franco-belge de 580 salariés spécialisée dans le traitement de paiements en ligne, opère un système de détection de fraude basé sur un ensemble de modèles ML (random forest + réseau de neurones) traitant 2,4 millions de transactions quotidiennes pour 1 200 e-commerçants. Le système est en production depuis 3 ans avec des mises à jour trimestrielles.

### Problème
Sur une période de 5 mois, le taux de fraude non détectée (faux négatifs) passe progressivement de 0,12 % à 0,41 %, représentant une perte cumulée de 8,7 M€ pour les commerçants clients. Parallèlement, le taux de faux positifs augmente de 2,1 % à 4,8 %, bloquant à tort 58 000 transactions légitimes par jour et provoquant la résiliation de 43 contrats commerçants en un trimestre. L'équipe data science ne détecte la dérive qu'après la plainte d'un client majeur.

### Approche
1. **Diagnostic de la dérive** : Analyse rétrospective des distributions de features sur 12 mois via le test de Kolmogorov-Smirnov et le Population Stability Index (PSI). Identification de 3 causes majeures : évolution des schémas de fraude (attaques par tokenisation de cartes volées), changement de mix commerçants (+35 % de secteur luxe à panier élevé), et dégradation de la qualité d'une source de données tierce (enrichissement IP).
2. **Déploiement d'un système de monitoring de drift** : Implémentation d'un pipeline de surveillance temps réel avec Evidently AI, mesurant 6 types de dérive (données, concept, performance, prédiction, label, feature importance). Seuils d'alerte configurés sur 3 niveaux (vigilance à PSI > 0,1, alerte à PSI > 0,2, critique à PSI > 0,3) avec notification automatique Slack et PagerDuty.
3. **Ré-entraînement et architecture adaptative** : Passage d'un cycle de mise à jour trimestriel à un système de ré-entraînement hebdomadaire automatisé avec validation A/B sur 5 % du trafic. Introduction d'un modèle champion/challenger avec basculement automatique si le challenger surperforme pendant 72h consécutives. Ajout de 14 nouvelles features capturant les patterns de fraude émergents.
4. **Gouvernance du cycle de vie modèle** : Création d'un Model Risk Committee mensuel réunissant data science, risques, compliance et business. Définition de SLA de performance (faux négatifs < 0,15 %, faux positifs < 2,5 %) avec escalade automatique en cas de dépassement. Documentation de chaque version de modèle dans un registre MLflow avec lignage complet des données.

### Résultat
- Taux de faux négatifs ramené de 0,41 % à 0,09 % en 8 semaines (meilleur que le baseline historique)
- Taux de faux positifs réduit de 4,8 % à 1,7 %, libérant 74 000 transactions légitimes par jour
- Pertes liées à la fraude non détectée réduites de 8,7 M€ à 1,9 M€ sur le trimestre suivant
- Délai moyen de détection d'une dérive significative passé de 5 mois à 36 heures

### Leçons apprises
- La dérive de modèle est inévitable dans les environnements adversariaux (fraude, cybersécurité) où les attaquants adaptent continuellement leurs stratégies : un monitoring proactif est vital
- Le monitoring de performance seul est insuffisant : la surveillance des distributions de données en amont permet de détecter la dérive avant qu'elle n'impacte les résultats business
- Les SLA de performance modèle doivent être traités avec la même rigueur que les SLA d'infrastructure : chaque point de pourcentage de dégradation a un coût business quantifiable

---

## Cas 3 : Réponse à incident après une crise d'hallucination dans un produit legal-tech

### Contexte
JurisIA, start-up legal-tech parisienne de 120 salariés, commercialise une plateforme d'aide à la rédaction juridique et de recherche jurisprudentielle augmentée par IA, utilisée par 850 cabinets d'avocats et 45 directions juridiques d'entreprises. Le moteur repose sur un LLM fine-tuné sur un corpus de 2,3 millions de décisions de justice françaises et européennes.

### Problème
Un avocat du barreau de Lyon dépose une assignation citant 4 arrêts de la Cour de cassation générés par la plateforme, dont 3 s'avèrent totalement fictifs (hallucinations). Le tribunal relève l'erreur, l'avocat est sanctionné par le bâtonnier, et l'affaire est médiatisée dans la Gazette du Palais et sur LegalNews. En 48h, 23 cabinets clients suspendent leur abonnement (représentant 380 K€ MRR) et le CNB (Conseil National des Barreaux) publie un communiqué d'alerte. L'analyse interne révèle un taux d'hallucination jurisprudentielle de 4,7 % sur les 30 derniers jours.

### Approche
1. **Activation du protocole d'incident critique** : Déclenchement immédiat du plan de réponse (< 2h après notification). Mise en place d'une cellule de crise (CEO, CTO, directeur juridique, responsable communication) avec points toutes les 4h. Communication proactive aux 850 cabinets clients par email personnalisé dans les 6h, reconnaissant le problème et détaillant les mesures immédiates.
2. **Containment et analyse racine** : Désactivation immédiate de la génération de références jurisprudentielles, remplacée par un mode « recherche seule » dans la base vérifiée. Audit exhaustif de 48 000 citations générées sur 60 jours : identification de 2 260 références fictives (4,7 %), dont 890 partiellement inexactes et 1 370 totalement inventées. Cause racine : fine-tuning insuffisant sur la distinction entre raisonnement juridique et citation exacte.
3. **Remédiation technique** : Implémentation d'un système RAG (Retrieval-Augmented Generation) remplaçant la génération de citations par une recherche dans une base vérifiée de 2,3 millions de décisions indexées. Ajout d'un module de vérification croisée comparant chaque référence citée à la base Légifrance via API. Affichage systématique d'un score de fiabilité et d'un lien direct vers la source primaire.
4. **Reconstruction de la confiance** : Notification individuelle aux 412 clients ayant reçu des documents contenant des références fictives, avec liste exhaustive des citations concernées. Mise en place d'un programme de compensation (3 mois d'abonnement offerts). Publication d'un rapport de transparence de 35 pages détaillant l'incident, les causes et les corrections. Engagement de certification annuelle par un auditeur indépendant.

### Résultat
- Taux d'hallucination jurisprudentielle réduit de 4,7 % à 0,02 % (99,98 % de fiabilité des citations)
- Récupération de 21 des 23 cabinets ayant suspendu leur abonnement en 3 mois
- Net Promoter Score remonté de -12 à +34 en 6 mois grâce à la transparence de la gestion de crise
- Signature d'un partenariat avec le CNB pour l'élaboration de normes de fiabilité IA en milieu juridique

### Leçons apprises
- Un plan de réponse à incident IA doit être préparé en amont et testé régulièrement : les premières heures sont déterminantes pour la crédibilité et la maîtrise de la communication
- Dans les domaines à haute conséquence (juridique, santé, finance), la génération pure par LLM doit toujours être couplée à une vérification sur base de données vérifiée (RAG) : la confiance zéro envers les outputs non sourcés est la seule posture responsable
- La transparence totale lors d'un incident (reconnaissance rapide, rapport détaillé, compensation) génère paradoxalement plus de confiance à long terme que l'absence d'incident : les clients valorisent la maturité de gestion de crise
