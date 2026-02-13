# Études de cas — Prompt Engineering & LLMOps

## Cas 1 : Implémentation d'une architecture RAG pour une base de connaissances d'entreprise

### Contexte
Groupe Véolia Technologie Interne (filiale fictive), direction des systèmes d'information d'un groupe industriel français de 12 000 salariés, gère une base documentaire de 340 000 documents techniques (procédures, normes, manuels, retours d'expérience) accumulés sur 15 ans. Les ingénieurs terrain passent en moyenne 47 minutes par jour à rechercher des informations, avec un taux de satisfaction de la recherche interne de seulement 23 %.

### Problème
Le moteur de recherche par mots-clés existant (Elasticsearch) ne couvre que 40 % des requêtes en langage naturel des techniciens. Les réponses sont des liens vers des documents de 50 à 200 pages sans pointage vers le passage pertinent. Le coût estimé de la perte de productivité liée à la recherche documentaire est de 6,2 M€/an. Trois incidents techniques majeurs (coût total : 1,8 M€) ont été attribués à des procédures obsolètes ou introuvables au cours des 18 derniers mois.

### Approche
1. **Architecture RAG multi-sources** : Conception d'un pipeline ingestion-indexation-retrieval-génération couvrant 7 sources (SharePoint, Confluence, SAP DMS, fichiers réseau, emails archivés, bases réglementaires, vidéos de formation transcrites). Chunking hybride : découpage sémantique par paragraphe (400-600 tokens) avec chevauchement de 15 %, enrichi de métadonnées (date, auteur, classification, version). Vectorisation via un modèle d'embedding multilingue (e5-large-v2) avec index HNSW sur Qdrant.
2. **Stratégie de retrieval avancée** : Implémentation d'un retrieval hybride combinant recherche vectorielle (cosine similarity) et BM25 pondérés par Reciprocal Rank Fusion. Ajout d'un re-ranker cross-encoder (ms-marco-MiniLM) pour le top-20 des résultats. Filtrage contextuel par métier, site et niveau d'habilitation de l'utilisateur. Recall@10 cible : 92 %.
3. **Prompt engineering et génération** : Conception de 12 templates de prompts spécialisés par type de requête (procédure, diagnostic, réglementation, historique d'incident). Implémentation de Chain-of-Thought pour les questions complexes multi-documents. Citation systématique des sources avec numéro de page et score de confiance. Mécanisme de fallback vers un agent humain si le score de confiance est inférieur à 0,65.
4. **Déploiement et boucle de feedback** : Lancement progressif sur 3 sites pilotes (800 utilisateurs) pendant 8 semaines avant généralisation. Collecte de feedback explicite (pouce haut/bas) et implicite (temps passé, clics sur sources). Ré-indexation incrémentale quotidienne et ré-entraînement mensuel du re-ranker sur les données de feedback.

### Résultat
- Temps moyen de recherche documentaire réduit de 47 à 11 minutes par jour et par ingénieur
- Taux de satisfaction de la recherche passé de 23 % à 87 % (enquête sur 2 400 utilisateurs)
- Recall@10 mesuré à 93,4 % sur un benchmark de 1 500 questions annotées par des experts métier
- ROI estimé à 4,8 M€/an en gains de productivité et réduction des incidents liés à l'information

### Leçons apprises
- La qualité du chunking et des métadonnées détermine 70 % de la performance d'un système RAG : investir massivement dans l'ingénierie de l'indexation avant d'optimiser la génération
- Le retrieval hybride (vectoriel + lexical + re-ranking) surpasse systématiquement le retrieval purement vectoriel, en particulier pour les requêtes contenant des identifiants techniques ou des codes normatifs
- Le feedback utilisateur implicite (patterns de navigation) est plus fiable que le feedback explicite (boutons) pour détecter les échecs de retrieval, car les utilisateurs ne signalent que 15 % des mauvaises réponses

---

## Cas 2 : Pipeline d'évaluation LLM pour une plateforme d'orchestration multi-modèles

### Contexte
NeuralHub, start-up française de 95 salariés spécialisée dans l'orchestration de modèles d'IA générative, propose une plateforme SaaS permettant à ses 320 entreprises clientes de déployer des workflows combinant plusieurs LLM (GPT-4, Claude, Mistral, Llama) selon les cas d'usage. La plateforme route 1,2 million de requêtes par jour vers le modèle optimal en fonction du coût, de la latence et de la qualité.

### Problème
L'absence de pipeline d'évaluation standardisé entraîne des choix de routage sous-optimaux : 34 % des requêtes sont envoyées vers des modèles surdimensionnés (coût moyen 3,2x supérieur au nécessaire) tandis que 18 % sont dirigées vers des modèles insuffisants (qualité < seuil client). Les coûts d'inférence explosent à 420 K€/mois (+85 % en 6 mois) sans amélioration proportionnelle de la satisfaction. Trois clients enterprise (1,1 M€ ARR) menacent de partir vers des solutions mono-modèle plus prévisibles.

### Approche
1. **Conception du framework d'évaluation** : Définition de 6 dimensions d'évaluation (exactitude factuelle, cohérence, pertinence, complétude, tonalité, sécurité) avec métriques spécifiques par dimension. Création d'un benchmark propriétaire de 4 200 cas de test couvrant 14 domaines métier, annotés par 3 évaluateurs humains avec accord inter-annotateur > 0,85 (kappa de Cohen).
2. **Pipeline d'évaluation automatisé** : Implémentation d'un système « LLM-as-Judge » utilisant Claude comme évaluateur calibré sur les annotations humaines (corrélation Spearman > 0,91). Pipeline CI/CD dédié : chaque nouveau modèle ou mise à jour de prompt est évalué automatiquement sur le benchmark complet en < 2h. Tableau de bord comparatif en temps réel des performances par modèle, domaine et type de tâche.
3. **Routage intelligent basé sur l'évaluation** : Développement d'un routeur ML entraîné sur 850 000 triplets (requête, modèle, score qualité) pour prédire le modèle optimal en < 5 ms. Intégration de contraintes budgétaires par client (coût max par requête) et de SLA de qualité (score minimum par dimension). Mécanisme de fallback automatique vers le modèle supérieur si le score prédit est en zone d'incertitude.
4. **Boucle d'amélioration continue** : Échantillonnage quotidien de 500 requêtes production pour évaluation humaine, alimentant le recalibrage mensuel du LLM-as-Judge. A/B testing permanent comparant le routeur ML au routage par règles sur 10 % du trafic. Reporting hebdomadaire par client du ratio qualité/coût avec recommandations d'optimisation.

### Résultat
- Coûts d'inférence réduits de 420 K€ à 185 K€/mois (-56 %) à qualité constante ou supérieure
- Taux de requêtes surdimensionnées passé de 34 % à 7 %, requêtes sous-dimensionnées de 18 % à 2,3 %
- Rétention des 3 clients enterprise menacés et croissance ARR de +42 % sur le semestre suivant
- Temps d'évaluation d'un nouveau modèle réduit de 2 semaines (manuel) à 1h47 (automatisé)

### Leçons apprises
- L'évaluation LLM est un produit à part entière qui nécessite autant d'investissement que le système principal : les entreprises sous-estiment systématiquement le coût de construction et de maintenance d'un benchmark de qualité
- Le LLM-as-Judge est un accélérateur puissant mais ne remplace pas l'évaluation humaine : un échantillonnage humain régulier est indispensable pour détecter les dérives de l'évaluateur automatique lui-même
- Le routage multi-modèles n'est rentable qu'à partir d'un volume suffisant (> 100 000 requêtes/jour) : en dessous, la complexité opérationnelle dépasse les économies réalisées

---

## Cas 3 : Optimisation du prompt engineering pour un système d'automatisation du support client

### Contexte
Voyagesia, agence de voyage en ligne française de 450 salariés, gère 8 500 demandes de support client par jour (email, chat, téléphone) avec une équipe de 120 conseillers. En 2024, l'entreprise déploie un système d'automatisation basé sur Claude pour traiter les demandes de niveau 1 (modifications de réservation, informations bagages, réclamations simples), représentant 62 % du volume total.

### Problème
Après 3 mois de production, le système automatisé affiche un taux de résolution au premier contact de seulement 41 % (objectif : 75 %), un taux d'escalade vers un agent humain de 52 %, et un score CSAT de 3,1/5 sur les interactions automatisées (vs 4,2/5 pour les interactions humaines). Les causes identifiées : prompts génériques ne capturant pas les spécificités métier, mauvaise gestion des cas ambigus, tonalité perçue comme robotique, et absence de personnalisation selon l'historique client.

### Approche
1. **Audit et taxonomie des interactions** : Analyse de 25 000 conversations historiques (humaines et automatisées) par clustering sémantique. Identification de 47 intentions distinctes regroupées en 8 catégories. Pour chaque intention, annotation de 200 exemples gold-standard par des conseillers seniors, incluant la réponse idéale, le ton attendu et les pièges à éviter.
2. **Ingénierie de prompts par couches** : Conception d'une architecture de prompts à 4 niveaux : (a) system prompt définissant la persona, les contraintes et les garde-fous (1 200 tokens), (b) contexte dynamique injecté par RAG (historique client, détails réservation, politique tarifaire applicable), (c) few-shot examples spécifiques à l'intention détectée (3-5 exemples), (d) instructions de formatage et de tonalité adaptées au canal (chat vs email). Versionnage systématique de chaque prompt dans un registre dédié.
3. **Optimisation itérative par évaluation** : Mise en place d'un pipeline d'évaluation testant chaque variante de prompt sur le benchmark de 9 400 cas annotés. Métriques suivies : exactitude de la réponse, respect des politiques commerciales, tonalité (évaluée par LLM-as-Judge calibré), et complétude. Exécution de 23 cycles d'optimisation sur 6 semaines avec des techniques de prompt chaining, self-consistency et structured output.
4. **Personnalisation et adaptation continue** : Implémentation d'un système de sélection dynamique de few-shot examples basé sur la similarité sémantique avec la requête entrante. Ajustement du ton selon le segment client (premium vs standard) et le contexte émotionnel détecté. Boucle de feedback hebdomadaire intégrant les corrections des conseillers humains sur les cas escaladés pour enrichir les exemples de référence.

### Résultat
- Taux de résolution au premier contact passé de 41 % à 78 % (+37 points en 10 semaines)
- Taux d'escalade réduit de 52 % à 19 %, libérant 38 conseillers pour les demandes complexes à forte valeur ajoutée
- Score CSAT des interactions automatisées remonté de 3,1 à 4,0/5 (écart avec le support humain réduit à 0,2 point)
- Économie de 1,4 M€/an en coûts opérationnels de support avec amélioration simultanée de la qualité de service

### Leçons apprises
- Le prompt engineering industriel est un processus d'ingénierie itératif, pas un art créatif : la rigueur du pipeline d'évaluation (benchmark, métriques, versionnage) détermine la vitesse de convergence vers la performance cible
- L'injection de contexte dynamique (historique client, détails de commande) via RAG a plus d'impact sur la qualité que le raffinement des instructions statiques : un prompt moyen avec un contexte riche surpasse un prompt excellent sans contexte
- La sélection dynamique de few-shot examples par similarité est la technique ayant produit le gain marginal le plus important (+11 points de résolution), car elle permet au modèle de s'adapter implicitement à la diversité des situations sans multiplication des prompts
