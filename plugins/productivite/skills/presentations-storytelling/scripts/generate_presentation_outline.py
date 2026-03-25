#!/usr/bin/env python3
"""
generate_presentation_outline.py
----------------------------------
Génère un fichier Markdown structuré avec un plan de présentation professionnel.

Types de présentation supportés :
  - pitch      : Levée de fonds / présentation investisseurs
  - rapport    : Rapport d'analyse / présentation de résultats
  - workshop   : Atelier collaboratif / formation
  - keynote    : Conférence / talk inspirant

Usage :
  python3 generate_presentation_outline.py [OPTIONS]

Options :
  --titre   TITRE       Titre de la présentation (obligatoire)
  --type    TYPE        Type : pitch | rapport | workshop | keynote (défaut: pitch)
  --slides  N           Nombre de slides souhaité (défaut: 12)
  --audience AUDIENCE   Description de l'audience (optionnel)
  --duree   N           Durée en minutes (optionnel, calculée si absent)
  --output  FILE        Fichier de sortie (défaut: presentation_outline.md)

Exemples :
  python3 generate_presentation_outline.py --titre "Mon Pitch" --type pitch --slides 12
  python3 generate_presentation_outline.py --titre "Rapport Q3 2024" --type rapport --slides 20 --audience "Comité de direction"
  python3 generate_presentation_outline.py --titre "Workshop IA" --type workshop --slides 30 --duree 90
  python3 generate_presentation_outline.py --titre "Keynote Innovation" --type keynote --slides 25
"""

import argparse
import sys
import textwrap
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Structures narratives par type
# ---------------------------------------------------------------------------

STRUCTURES = {

    "pitch": {
        "label": "Pitch Deck — Levée de fonds / Présentation investisseurs",
        "framework": "Séquence YC / Sequoia adaptée",
        "description": (
            "Structure optimisée pour convaincre des investisseurs ou des partenaires "
            "stratégiques. Suit la progression émotionnelle : attention → compréhension "
            "→ conviction → action."
        ),
        "sections": [
            {
                "id": 1,
                "titre": "Accroche & Titre",
                "tag": "Hook",
                "slides": 1,
                "objectif": "Capter l'attention immédiatement. Une phrase choc, une stat clé, ou une question provocatrice.",
                "contenu": [
                    "Slide de titre : nom de l'entreprise / projet, tagline en 8 mots max",
                    "Optionnel : une donnée ou une citation qui crée la tension narrative",
                ],
                "tips": "Ne pas dépasser 15 mots sur la slide d'accroche. Moins = plus fort.",
            },
            {
                "id": 2,
                "titre": "Le Problème",
                "tag": "Problem",
                "slides": 1,
                "objectif": "Créer de l'empathie et démontrer que le problème est réel, douloureux et coûteux.",
                "contenu": [
                    "Qui souffre du problème ? (persona cible)",
                    "Quelle est la douleur concrète ? (coût, temps perdu, frustration)",
                    "Quelle est l'ampleur ? (chiffre de marché / fréquence)",
                    "Pourquoi les solutions actuelles échouent ?",
                ],
                "tips": "Raconter une histoire : '1 minute dans la vie de [persona]'. Rendre le problème viscéral.",
            },
            {
                "id": 3,
                "titre": "La Solution",
                "tag": "Solution",
                "slides": 1,
                "objectif": "Présenter votre approche unique. Simple, mémorable, différenciée.",
                "contenu": [
                    "La proposition de valeur en une phrase (value prop statement)",
                    "Comment ça fonctionne : les 3 étapes clés max",
                    "Ce qui vous rend unique (angle différenciateur)",
                    "Démonstration ou mockup si disponible",
                ],
                "tips": "Respecter la règle : si on ne peut pas expliquer la solution en 30 secondes, c'est trop complexe.",
            },
            {
                "id": 4,
                "titre": "Taille de Marché",
                "tag": "Market",
                "slides": 1,
                "objectif": "Démontrer que l'opportunité justifie un investissement significatif.",
                "contenu": [
                    "TAM (Total Addressable Market) — marché global adressable",
                    "SAM (Serviceable Addressable Market) — marché atteignable",
                    "SOM (Serviceable Obtainable Market) — cible réaliste à 3 ans",
                    "Sources des données de marché (études, rapports sectoriels)",
                    "Dynamique de croissance du marché (%/an)",
                ],
                "tips": "Partir du bas (bottom-up) plutôt que du top-down. Les investisseurs font confiance aux calculs précis.",
            },
            {
                "id": 5,
                "titre": "Produit & Demo",
                "tag": "Product",
                "slides": 2,
                "objectif": "Montrer, ne pas raconter. Prouver que le produit existe et fonctionne.",
                "contenu": [
                    "Screenshots / vidéo démo du produit (30-60 secondes)",
                    "Architecture simplifiée si c'est un différenciateur tech",
                    "Roadmap produit à 12 mois (3-4 étapes max)",
                    "Métriques produit clés (DAU, rétention, NPS)",
                ],
                "tips": "Une démo live vaut 1000 slides. Si possible, la préparer en backup offline.",
            },
            {
                "id": 6,
                "titre": "Modèle Économique",
                "tag": "Business Model",
                "slides": 1,
                "objectif": "Expliquer comment vous gagnez de l'argent. Simple et crédible.",
                "contenu": [
                    "Sources de revenus (abonnement, transaction, licence, freemium...)",
                    "Prix / ARPU / LTV cible",
                    "Économie unitaire : CAC, LTV, ratio LTV/CAC",
                    "Marges brutes cibles",
                ],
                "tips": "Les investisseurs veulent du unit economics. Connaître CAC et LTV par cœur.",
            },
            {
                "id": 7,
                "titre": "Traction",
                "tag": "Traction",
                "slides": 1,
                "objectif": "Prouver que le marché veut votre solution. Les faits > les projections.",
                "contenu": [
                    "Métriques de croissance clés (MRR, ARR, utilisateurs, NPS)",
                    "Graphique de croissance (idéalement : courbe en 'hockey stick')",
                    "Clients / partenaires de référence (logos si autorisation)",
                    "Témoignages clients (1-2 quotes impactantes)",
                    "Milestones atteints vs. prévisions",
                ],
                "tips": "Si la traction est faible, montrer la vélocité et les indicateurs leading (pipeline, LOI, POC).",
            },
            {
                "id": 8,
                "titre": "Stratégie Go-to-Market",
                "tag": "GTM",
                "slides": 1,
                "objectif": "Montrer que vous savez comment acquérir et retenir vos clients.",
                "contenu": [
                    "Canal d'acquisition principal (inbound, outbound, partnerships, PLG...)",
                    "Coût d'acquisition cible et canaux testés",
                    "Stratégie de rétention / expansion (upsell, NRR)",
                    "Partenariats stratégiques en cours",
                ],
                "tips": "Être précis sur 1-2 canaux qui fonctionnent plutôt que de lister 10 canaux théoriques.",
            },
            {
                "id": 9,
                "titre": "Équipe",
                "tag": "Team",
                "slides": 1,
                "objectif": "Démontrer que vous êtes les meilleurs pour exécuter cette vision.",
                "contenu": [
                    "Fondateurs : photo, rôle, expérience pertinente (max 3 bullets chacun)",
                    "Expériences différenciantes (ex-GAFA, domain expertise, exits précédents)",
                    "Conseillers / advisors clés",
                    "Prochains recrutements prioritaires",
                ],
                "tips": "Mettre en avant pourquoi vous êtes UNIQUEMENT positionnés pour résoudre ce problème.",
            },
            {
                "id": 10,
                "titre": "Finances & Projections",
                "tag": "Financials",
                "slides": 1,
                "objectif": "Montrer que vous pilotez le business avec rigueur.",
                "contenu": [
                    "P&L simplifié : revenus, coûts, EBITDA sur 3 ans",
                    "Burn rate actuel et runway (mois de cash restants)",
                    "Métriques SaaS / clés : MRR, churn, ARR",
                    "Hypothèses de croissance claires et défendables",
                ],
                "tips": "Présenter des projections raisonnables (pas 10x le marché en 3 ans). Montrer 3 scénarios.",
            },
            {
                "id": 11,
                "titre": "Le Ask",
                "tag": "Ask",
                "slides": 1,
                "objectif": "Demander clairement ce dont vous avez besoin.",
                "contenu": [
                    "Montant recherché et instrument (equity, SAFE, convertible)",
                    "Valorisation pré-money ou cap",
                    "Utilisation des fonds : top 3 postes (équipe X%, produit X%, GTM X%)",
                    "Milestones clés financés par ce tour",
                    "Timing : fenêtre de closing souhaitée",
                ],
                "tips": "Être précis et confiant. L'ambiguïté sur le ask envoie un signal négatif.",
            },
            {
                "id": 12,
                "titre": "Vision & Conclusion",
                "tag": "Vision",
                "slides": 1,
                "objectif": "Terminer sur la vision ambitieuse et l'appel à l'action.",
                "contenu": [
                    "La vision à 5-10 ans : quel monde voulez-vous créer ?",
                    "Pourquoi MAINTENANT ? (timing, fenêtre d'opportunité)",
                    "Call to action clair : 'Rejoignez-nous pour [mission]'",
                    "Contacts : email, LinkedIn, site web",
                ],
                "tips": "Finir sur une image forte ou une citation inspirante liée à votre mission.",
            },
        ],
        "annexes": [
            "Competitive landscape détaillé (tableau de positionnement)",
            "Deep dive technique / architecture",
            "Références clients et case studies",
            "Termes du term sheet et cap table actuelle",
            "Pipeline commercial détaillé",
        ],
    },

    "rapport": {
        "label": "Rapport d'analyse / Présentation de résultats",
        "framework": "Pyramid Principle (Minto) + Data Storytelling",
        "description": (
            "Structure pour présenter des analyses, résultats d'études ou recommandations "
            "stratégiques. Commence par la conclusion (pyramid principle) pour maximiser "
            "l'impact auprès d'un public décisionnel."
        ),
        "sections": [
            {
                "id": 1,
                "titre": "Titre & Contexte",
                "tag": "Context",
                "slides": 1,
                "objectif": "Poser le cadre : qui commande ce rapport, pour quoi faire, avec quelles données.",
                "contenu": [
                    "Titre du rapport + sous-titre descriptif",
                    "Commanditaire et date",
                    "Périmètre de l'analyse (données, période, scope géographique)",
                    "Message central : la recommandation principale en 1 phrase",
                ],
                "tips": "Le message central doit être lisible avant même l'analyse. C'est le principe de la pyramide.",
            },
            {
                "id": 2,
                "titre": "Recommandation Principale",
                "tag": "Recommendation",
                "slides": 1,
                "objectif": "Annoncer la conclusion dès le début (principe de la pyramide inverse).",
                "contenu": [
                    "Recommandation principale en une phrase affirmative",
                    "Les 3 raisons qui la soutiennent (structure MECE)",
                    "Impact attendu (quantifié si possible)",
                    "Condition de succès principale",
                ],
                "tips": "Ne pas avoir peur d'annoncer la conclusion. Les décideurs n'ont pas le temps de lire tout le rapport.",
            },
            {
                "id": 3,
                "titre": "Contexte & Problématique",
                "tag": "Background",
                "slides": 2,
                "objectif": "Rappeler le contexte pour aligner l'audience sur les enjeux.",
                "contenu": [
                    "Situation actuelle : état des lieux objectif",
                    "Problème ou opportunité identifié (la 'complication')",
                    "Question centrale à laquelle répond ce rapport",
                    "Contraintes et hypothèses retenues",
                ],
                "tips": "Structure SCP : Situation → Complication → Question. Ne pas aller trop long sur le contexte.",
            },
            {
                "id": 4,
                "titre": "Méthodologie",
                "tag": "Method",
                "slides": 1,
                "objectif": "Crédibiliser la démarche d'analyse. Bref mais indispensable.",
                "contenu": [
                    "Sources de données utilisées (interne / externe, volume, fraîcheur)",
                    "Période d'analyse et périmètre",
                    "Méthode d'analyse (statistique, qualitatif, benchmark...)",
                    "Limites et biais éventuels de la méthode",
                ],
                "tips": "Mettre la méthodologie détaillée en annexe. Ne garder que l'essentiel pour crédibiliser.",
            },
            {
                "id": 5,
                "titre": "Findings — Vue d'ensemble",
                "tag": "Overview",
                "slides": 1,
                "objectif": "Synthèse des résultats clés. Le 'executive summary' visuel.",
                "contenu": [
                    "3-5 findings principaux en bullet points affirmatifs",
                    "Dashboard ou scorecard des métriques clés",
                    "Comparaison vs. baseline ou objectif",
                    "Signal positif ET signal d'alerte",
                ],
                "tips": "Cette slide doit pouvoir être envoyée seule par email pour un update rapide.",
            },
            {
                "id": 6,
                "titre": "Finding #1",
                "tag": "Finding",
                "slides": 2,
                "objectif": "Développer le premier résultat clé avec preuves et visualisations.",
                "contenu": [
                    "Titre affirmatif : le message du finding en une phrase",
                    "Visualisation principale (graphique annoté, tableau)",
                    "Interprétation : que signifie cette donnée ?",
                    "Implications pour la décision",
                ],
                "tips": "Action title = phrase affirmative, pas un mot-clé. 'Les conversions chutent de 30% en mobile' > 'Mobile'.",
            },
            {
                "id": 7,
                "titre": "Finding #2",
                "tag": "Finding",
                "slides": 2,
                "objectif": "Développer le deuxième résultat clé.",
                "contenu": [
                    "Même structure que Finding #1",
                    "Connexion avec le Finding précédent (fil narratif)",
                    "Données comparatives ou de benchmark si disponibles",
                ],
                "tips": "Maintenir le fil narratif entre les findings. Chaque slide doit faire avancer le raisonnement.",
            },
            {
                "id": 8,
                "titre": "Finding #3",
                "tag": "Finding",
                "slides": 2,
                "objectif": "Développer le troisième résultat clé.",
                "contenu": [
                    "Même structure",
                    "Inclure les nuances ou exceptions importantes",
                    "Données de segmentation si pertinentes",
                ],
                "tips": "3 findings = maximum pour une présentation de 20 slides. Au-delà, le message se dilue.",
            },
            {
                "id": 9,
                "titre": "Recommandations",
                "tag": "Recommendations",
                "slides": 2,
                "objectif": "Traduire les findings en actions concrètes et priorisées.",
                "contenu": [
                    "Tableau des recommandations : action, impact, effort, délai",
                    "Recommandation #1 : description, owner, KPI de succès",
                    "Recommandation #2 : description, owner, KPI de succès",
                    "Recommandation #3 : description, owner, KPI de succès",
                    "Priorisation : matrice impact / effort",
                ],
                "tips": "Chaque recommandation doit être SMART : Spécifique, Mesurable, Atteignable, Réaliste, Temporelle.",
            },
            {
                "id": 10,
                "titre": "Next Steps & Roadmap",
                "tag": "Next Steps",
                "slides": 1,
                "objectif": "Transformer la présentation en plan d'action.",
                "contenu": [
                    "Timeline des actions sur 30 / 60 / 90 jours",
                    "Responsables et dépendances",
                    "Ressources nécessaires (budget, équipe)",
                    "Prochaine revue et indicateurs de suivi",
                    "Décision demandée aujourd'hui",
                ],
                "tips": "Terminer par une question précise : 'Validez-vous le lancement du chantier X avant le [date] ?'",
            },
        ],
        "annexes": [
            "Données brutes et méthodologie détaillée",
            "Analyses complémentaires / segmentations",
            "Benchmark concurrentiel complet",
            "Hypothèses et sensitivité de l'analyse",
            "Glossaire des métriques",
        ],
    },

    "workshop": {
        "label": "Workshop / Formation / Atelier collaboratif",
        "framework": "4MAT Learning Cycle (Why → What → How → What if)",
        "description": (
            "Structure pédagogique pour des ateliers participatifs ou formations. "
            "Alternance entre phases d'information, de réflexion, d'exercice pratique "
            "et de consolidation."
        ),
        "sections": [
            {
                "id": 1,
                "titre": "Bienvenue & Cadrage",
                "tag": "Welcome",
                "slides": 2,
                "objectif": "Créer un espace sécurisé, aligner les attentes, poser le cadre.",
                "contenu": [
                    "Titre du workshop + sous-titre",
                    "Agenda du jour (macro) avec timing",
                    "Règles du jeu et mode de participation",
                    "Tour de table / ice breaker (si groupe < 20 pers.)",
                    "Question ouvre-appétit : sondage ou réflexion individuelle",
                ],
                "tips": "Investir 10 minutes sur le cadrage. Un groupe bien cadré est 30% plus productif.",
            },
            {
                "id": 2,
                "titre": "Objectifs & Résultats attendus",
                "tag": "Objectives",
                "slides": 1,
                "objectif": "Aligner le groupe sur ce que chacun repartira avec.",
                "contenu": [
                    "Objectif principal du workshop en une phrase",
                    "3 compétences / livrables que les participants auront à la fin",
                    "Ce que ce workshop N'EST PAS (scoper les attentes)",
                    "Pré-requis et niveau d'entrée",
                ],
                "tips": "Distinguer objectifs pédagogiques (apprendre X) et livrables (produire Y). Les deux sont importants.",
            },
            {
                "id": 3,
                "titre": "Pourquoi — Le contexte",
                "tag": "Why",
                "slides": 2,
                "objectif": "Créer la motivation. Répondre à 'Pourquoi c'est important pour moi ?'",
                "contenu": [
                    "Enjeux et contexte business / organisationnel",
                    "Impacts concrets si on ne maîtrise pas ce sujet",
                    "Opportunités si on le maîtrise",
                    "Cas réels de l'entreprise ou du secteur",
                    "Sondage : 'Où en êtes-vous sur ce sujet ?'",
                ],
                "tips": "Les adultes apprennent si la motivation est intrinsèque. Activer le POURQUOI avant le COMMENT.",
            },
            {
                "id": 4,
                "titre": "Module 1 — Concepts clés",
                "tag": "Theory",
                "slides": 3,
                "objectif": "Transmettre les fondamentaux de manière engageante.",
                "contenu": [
                    "Concept #1 : définition + exemple concret + anti-exemple",
                    "Concept #2 : définition + exemple concret + cas pratique",
                    "Concept #3 : définition + schéma visuel",
                    "Quiz / vérification de compréhension (Mentimeter, Slido)",
                ],
                "tips": "Maximum 3 concepts par module. Alterner slide de théorie et exercise toutes les 15-20 min.",
            },
            {
                "id": 5,
                "titre": "Exercice 1 — Application",
                "tag": "Exercise",
                "slides": 2,
                "objectif": "Ancrer les concepts par la pratique immédiate.",
                "contenu": [
                    "Consignes claires : quoi faire, avec qui, en combien de temps",
                    "Exemple résolu (worked example) pour lever les ambiguïtés",
                    "Matériaux nécessaires (template, données, outils)",
                    "Timing visible (timer projeté)",
                    "Débrief : restitution et points d'apprentissage",
                ],
                "tips": "L'exercice doit être faisable en 80% par un débutant. Trop difficile = découragement.",
            },
            {
                "id": 6,
                "titre": "Module 2 — Approfondissement",
                "tag": "Deep Dive",
                "slides": 3,
                "objectif": "Aller plus loin, traiter la complexité et les cas limites.",
                "contenu": [
                    "Techniques avancées ou cas d'usage spécifiques",
                    "Erreurs fréquentes et comment les éviter",
                    "Comparaison d'approches (quand utiliser X vs. Y ?)",
                    "Démonstration live ou étude de cas",
                ],
                "tips": "Lier explicitement au Module 1 : 'On a vu X. Maintenant, quand X ne suffit pas...'",
            },
            {
                "id": 7,
                "titre": "Exercice 2 — Cas pratique",
                "tag": "Case Study",
                "slides": 2,
                "objectif": "Simulation d'un cas réel. Mise en pratique en autonomie guidée.",
                "contenu": [
                    "Description du cas (contexte, données, contraintes)",
                    "Travail en sous-groupes (4-6 personnes)",
                    "Restitution par groupe (3-5 min chacun)",
                    "Feedback et enrichissement collectif",
                ],
                "tips": "Utiliser un cas de l'entreprise / secteur. La proximité du contexte maximise le transfert.",
            },
            {
                "id": 8,
                "titre": "Synthèse & Points clés",
                "tag": "Summary",
                "slides": 1,
                "objectif": "Consolider les apprentissages. Ce que tout le monde doit retenir.",
                "contenu": [
                    "3-5 messages clés du workshop (reprise des objectifs initiaux)",
                    "Checklist / framework à emporter",
                    "Ressources complémentaires (lectures, outils, communautés)",
                ],
                "tips": "Revenir sur les objectifs annoncés au début. Valider avec le groupe que les objectifs sont atteints.",
            },
            {
                "id": 9,
                "titre": "Plan d'action personnel",
                "tag": "Action Plan",
                "slides": 1,
                "objectif": "Transformer les apprentissages en engagements d'action.",
                "contenu": [
                    "Template : 'Dans les 7 prochains jours, je vais...'",
                    "Partage en binôme : accountability",
                    "Ressources et support disponibles après le workshop",
                    "Dates de suivi et de revue",
                ],
                "tips": "Un plan d'action écrit augmente de 40% la probabilité de mise en œuvre. Toujours inclure.",
            },
            {
                "id": 10,
                "titre": "Évaluation & Clôture",
                "tag": "Wrap-up",
                "slides": 1,
                "objectif": "Recueillir le feedback et clore positivement.",
                "contenu": [
                    "Formulaire d'évaluation (NPS + 2 questions ouvertes)",
                    "Tour de table final : 1 mot / 1 phrase de conclusion par personne",
                    "Annonce des prochaines étapes et ressources",
                    "Remerciements",
                ],
                "tips": "Finir sur une énergie positive. La dernière impression reste la plus mémorable.",
            },
        ],
        "annexes": [
            "Ressources complémentaires et bibliographie",
            "Glossaire des termes clés",
            "Templates et frameworks utilisés",
            "FAQ et cas limites",
            "Guide du facilitateur",
        ],
    },

    "keynote": {
        "label": "Keynote / Conférence / Talk inspirant",
        "framework": "TED Structure : Hook → Story → Insight → Call to Action",
        "description": (
            "Structure narrative puissante pour les talks de conférence, discours "
            "d'inauguration ou présentations inspirantes. Priorité à l'émotion, "
            "au storytelling et à la vision."
        ),
        "sections": [
            {
                "id": 1,
                "titre": "L'Accroche (Hook)",
                "tag": "Hook",
                "slides": 1,
                "objectif": "Capturer l'attention dans les 30 premières secondes. Tout ou rien.",
                "contenu": [
                    "Option A : Question rhétorique provocatrice",
                    "Option B : Statistique choquante ou contre-intuitive",
                    "Option C : Anecdote personnelle court et percutante",
                    "Option D : Déclaration audacieuse et controversial",
                    "Transition vers le sujet : 'C'est de cela que je veux vous parler aujourd'hui.'",
                ],
                "tips": "Les 30 premières secondes déterminent si le public vous donnera 30 minutes. Répéter l'accroche 10x.",
            },
            {
                "id": 2,
                "titre": "La Promesse",
                "tag": "Promise",
                "slides": 1,
                "objectif": "Dire explicitement ce que le public va emporter.",
                "contenu": [
                    "L'idée centrale en une phrase ('L'idée que je veux partager est...')",
                    "Ce que le public va voir différemment après ce talk",
                    "Pourquoi ça compte pour eux spécifiquement",
                ],
                "tips": "Une idée = un talk. Résister à la tentation d'en mettre trois.",
            },
            {
                "id": 3,
                "titre": "Le Contexte — Le monde avant",
                "tag": "World Before",
                "slides": 2,
                "objectif": "Établir le statu quo. La situation que tout le monde reconnaît.",
                "contenu": [
                    "Description du monde actuel (la réalité partagée)",
                    "Les croyances ou pratiques dominantes",
                    "Ce qui fonctionne et ce qui bloque",
                    "Données ou faits qui ancrent la réalité",
                ],
                "tips": "Créer de la résonance : le public doit se dire 'Oui, c'est exactement comme ça.'",
            },
            {
                "id": 4,
                "titre": "Le Conflit — Ce qui ne fonctionne plus",
                "tag": "Conflict",
                "slides": 2,
                "objectif": "Créer la tension narrative. Identifier la fissure dans le statu quo.",
                "contenu": [
                    "Le changement ou le défi qui remet tout en question",
                    "Les limites du paradigme actuel",
                    "La question que personne ne veut poser",
                    "L'histoire personnelle ou le cas concret qui illustre le conflit",
                ],
                "tips": "Pas de conflit = pas de tension = pas d'attention. Le conflit est le moteur de l'histoire.",
            },
            {
                "id": 5,
                "titre": "L'Histoire — Le voyage",
                "tag": "Story",
                "slides": 3,
                "objectif": "Emmener le public dans un voyage. Raconter la transformation.",
                "contenu": [
                    "L'histoire personnelle ou de cas qui incarne l'idée",
                    "Les obstacles rencontrés et comment ils ont été surmontés",
                    "Le moment de bascule (turning point)",
                    "Les apprentissages clés de ce voyage",
                    "Connexion entre l'histoire et le message central",
                ],
                "tips": "Les histoires se mémorisent 22x mieux que les faits bruts. Ne jamais sauter cette étape.",
            },
            {
                "id": 6,
                "titre": "L'Insight — La révélation",
                "tag": "Insight",
                "slides": 2,
                "objectif": "Livrer l'idée centrale. Le moment 'aha' du talk.",
                "contenu": [
                    "L'insight principal formulé de manière mémorable (soundbite)",
                    "La preuve ou démonstration qui le valide",
                    "Pourquoi c'est contre-intuitif ou non-obvieux",
                    "Les implications de cet insight (si on l'accepte, alors...)",
                ],
                "tips": "L'insight doit être 'tweetable' : formulé en moins de 280 caractères, retweetable.",
            },
            {
                "id": 7,
                "titre": "La Preuve — Evidence & Exemples",
                "tag": "Evidence",
                "slides": 3,
                "objectif": "Convertir l'intuition en conviction. Preuves + exemples + données.",
                "contenu": [
                    "Exemple #1 : illustration de l'insight en action",
                    "Donnée clé : la stat qui change la perception",
                    "Exemple #2 : cas concret d'une autre industrie / pays / époque",
                    "Expert / référence qui valide l'approche",
                ],
                "tips": "Mix de preuves : données quantitatives (logos gauche) + histoires (logos droit). Les deux ensemble.",
            },
            {
                "id": 8,
                "titre": "Le Monde Après — Vision",
                "tag": "Vision",
                "slides": 2,
                "objectif": "Peindre le futur possible si l'insight est appliqué.",
                "contenu": [
                    "Comment le monde sera différent si on adopte cette idée",
                    "Les bénéfices concrets pour le public",
                    "Exemples de pionniers qui vivent déjà ce futur",
                    "La vision ambitieuse à 5-10 ans",
                ],
                "tips": "Rendre le futur désirable et crédible. 'Utopie réalisable' plutôt que 'dystopie évitée'.",
            },
            {
                "id": 9,
                "titre": "Call to Action",
                "tag": "CTA",
                "slides": 1,
                "objectif": "Transformer l'inspiration en action. Une seule demande, claire et précise.",
                "contenu": [
                    "L'action concrète que vous demandez au public de faire (une seule)",
                    "Pourquoi maintenant ? (urgence ou opportunité de timing)",
                    "Comment commencer : la première étape simple",
                    "Ressources pour aller plus loin",
                ],
                "tips": "Un seul CTA. Deux CTA = zéro CTA. Choisir et assumer.",
            },
            {
                "id": 10,
                "titre": "La Conclusion — Retour à l'accroche",
                "tag": "Close",
                "slides": 1,
                "objectif": "Clore le cycle narratif. Revenir à l'accroche avec une réponse.",
                "contenu": [
                    "Reprendre l'image, la question ou l'anecdote de l'accroche",
                    "Montrer comment l'insight apporte la réponse / la résolution",
                    "Dernière phrase mémorable (la 'closing line' qu'on retiendra)",
                    "Remerciements sobres",
                ],
                "tips": "La dernière phrase est ce que le public retient. La préparer mot pour mot et la répéter.",
            },
        ],
        "annexes": [
            "Notes de speaker complètes",
            "Sources et bibliographie",
            "Versions de la présentation pour différents timings (15 / 30 / 45 min)",
            "Q&A préparées",
        ],
    },
}


# ---------------------------------------------------------------------------
# Générateur de Markdown
# ---------------------------------------------------------------------------

def adjust_slides(sections: list, target_total: int) -> list:
    """
    Ajuste le nombre de slides par section pour atteindre approximativement
    le total souhaité, en préservant les proportions relatives.
    """
    base_total = sum(s["slides"] for s in sections)
    if base_total == 0 or target_total <= 0:
        return sections

    adjusted = []
    allocated = 0
    for i, section in enumerate(sections):
        if i < len(sections) - 1:
            new_count = max(1, round(section["slides"] * target_total / base_total))
            allocated += new_count
        else:
            # Dernière section : prend le reste pour atteindre exactement le total
            new_count = max(1, target_total - allocated)
        adjusted.append({**section, "slides": new_count})

    return adjusted


def format_duration(slides: int, pacing: float = 1.5) -> str:
    """Estime la durée en minutes à partir du nombre de slides."""
    total_min = round(slides * pacing)
    if total_min < 60:
        return f"~{total_min} min"
    h = total_min // 60
    m = total_min % 60
    return f"~{h}h{m:02d}" if m else f"~{h}h"


def generate_outline(
    titre: str,
    pres_type: str,
    slides_total: int,
    audience: str = "",
    duree: int = None,
    output_file: str = None,
) -> str:
    """
    Génère le plan de présentation en Markdown.
    Retourne le contenu du fichier.
    """
    if pres_type not in STRUCTURES:
        raise ValueError(f"Type de présentation non supporté : {pres_type}. "
                         f"Types disponibles : {', '.join(STRUCTURES.keys())}")

    struct = STRUCTURES[pres_type]
    sections = adjust_slides(struct["sections"], slides_total)
    real_total = sum(s["slides"] for s in sections)
    pacing = round(duree / real_total, 1) if duree else 1.5
    estimated_duration = duree or round(real_total * 1.5)

    now = date.today().isoformat()
    audience_line = f"**Audience :** {audience}" if audience else "**Audience :** À définir"
    duree_str = f"{estimated_duration} min"

    lines = []

    # ── En-tête ──────────────────────────────────────────────────────────────
    lines += [
        f"# {titre}",
        "",
        f"> Plan généré par `generate_presentation_outline.py` le {now}",
        "",
        "---",
        "",
        "## Informations générales",
        "",
        f"| Champ           | Valeur                                          |",
        f"|-----------------|--------------------------------------------------|",
        f"| **Titre**       | {titre}                                          |",
        f"| **Type**        | {struct['label']}                                |",
        f"| **Framework**   | {struct['framework']}                            |",
        f"| **Slides**      | {real_total} slides                              |",
        f"| **Durée**       | {duree_str}                                       |",
        f"| {audience_line} |                                                  |",
        f"| **Date**        | {now}                                             |",
        "",
        "---",
        "",
        "## Description de la structure",
        "",
        f"{struct['description']}",
        "",
        "---",
        "",
        "## Message central",
        "",
        "> **À compléter** — Le message central est la seule chose que votre audience",
        "> doit retenir si elle oublie tout le reste. Formulez-le en une phrase affirmative.",
        "",
        "```",
        "[ Votre message central en une phrase ]",
        "```",
        "",
        "---",
        "",
        "## Plan détaillé",
        "",
    ]

    # ── Sections ──────────────────────────────────────────────────────────────
    slide_counter = 1
    for section in sections:
        s_count  = section["slides"]
        s_end    = slide_counter + s_count - 1
        slide_range = (f"Slide {slide_counter}"
                       if s_count == 1
                       else f"Slides {slide_counter}–{s_end}")
        time_start = round((slide_counter - 1) * pacing)
        time_end   = round(s_end * pacing)
        time_str   = f"{time_start}–{time_end} min"

        lines += [
            f"### {section['id']}. {section['titre']}",
            "",
            f"| Champ         | Détail                                          |",
            f"|---------------|--------------------------------------------------|",
            f"| **Tag**       | `{section['tag']}`                              |",
            f"| **Slides**    | {slide_range} ({s_count} slide{'s' if s_count > 1 else ''}) |",
            f"| **Timing**    | {time_str}                                      |",
            f"| **Objectif**  | {section['objectif']}                           |",
            "",
            "**Contenu suggéré :**",
            "",
        ]
        for item in section["contenu"]:
            lines.append(f"- {item}")

        lines += [
            "",
            f"> **Conseil :** {section['tips']}",
            "",
        ]

        # Espace pour les titres de slides
        lines += ["**Titres de slides proposés :**", ""]
        for i in range(s_count):
            slide_num = slide_counter + i
            lines.append(f"- [ ] Slide {slide_num} : _(à définir — action title affirmatif)_")
        lines += ["", "---", ""]

        slide_counter += s_count

    # ── Annexes ───────────────────────────────────────────────────────────────
    lines += [
        "## Slides annexes recommandées",
        "",
        "_Les annexes ne font pas partie du deck principal. "
        "Elles sont préparées pour répondre aux questions._",
        "",
    ]
    for annexe in struct["annexes"]:
        lines.append(f"- [ ] {annexe}")

    lines += ["", "---", ""]

    # ── Checklist qualité ─────────────────────────────────────────────────────
    lines += [
        "## Checklist qualité avant livraison",
        "",
        "| # | Critère | Statut |",
        "|---|---------|--------|",
        "| 1 | Message central formulé en une phrase affirmative | ☐ |",
        "| 2 | Action titles sur toutes les slides (phrases affirmatives) | ☐ |",
        "| 3 | Lecture des titres seuls = histoire cohérente | ☐ |",
        "| 4 | Ratio slides / durée respecté (~1,5 min par slide) | ☐ |",
        "| 5 | Une seule idée par slide | ☐ |",
        "| 6 | Visuels libres de droits ou créés | ☐ |",
        "| 7 | Données annotées directement sur les graphiques | ☐ |",
        "| 8 | Design system cohérent (couleurs, typo, grille) | ☐ |",
        "| 9 | Call to action unique et explicite | ☐ |",
        "| 10 | Relecture orthographique complète | ☐ |",
        "| 11 | Test sur le matériel de projection réel | ☐ |",
        "| 12 | Répétition à voix haute (min. 3 fois) | ☐ |",
        "",
        "---",
        "",
    ]

    # ── Notes de speaker ──────────────────────────────────────────────────────
    lines += [
        "## Notes de speaker",
        "",
        "_Template : compléter une section par slide clé._",
        "",
        "### Notes — Section 1",
        "",
        "```",
        "Message à passer : ",
        "Transition vers la suite : ",
        "Questions anticipées : ",
        "Backup si on manque de temps : ",
        "```",
        "",
        "---",
        "",
        "## Ressources complémentaires",
        "",
        "- **Storytelling** : "
        "[The Pyramid Principle (Minto)](https://www.barbaraminto.com/)",
        "- **Design slides** : "
        "[Beautiful.ai](https://www.beautiful.ai/) | "
        "[Gamma](https://gamma.app/) | "
        "[Canva](https://canva.com/)",
        "- **Données** : annoter les graphiques avec [Datawrapper](https://www.datawrapper.de/)",
        "- **Feedback** : partager sur [Pitch](https://pitch.com/) pour les commentaires",
        "",
        f"---",
        "",
        f"_Généré avec `generate_presentation_outline.py` — {now}_",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Génère un plan de présentation professionnel en Markdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Exemples :
              python3 generate_presentation_outline.py --titre "Mon Pitch" --type pitch --slides 12
              python3 generate_presentation_outline.py --titre "Rapport Q3" --type rapport --slides 20
              python3 generate_presentation_outline.py --titre "Workshop IA" --type workshop --slides 30 --duree 90
              python3 generate_presentation_outline.py --titre "Keynote Innovation" --type keynote --slides 25 --audience "Conférence LeWeb"
        """),
    )

    parser.add_argument(
        "--titre", "-t",
        required=True,
        help="Titre de la présentation (obligatoire).",
    )
    parser.add_argument(
        "--type", "-T",
        default="pitch",
        choices=list(STRUCTURES.keys()),
        help=f"Type de présentation : {' | '.join(STRUCTURES.keys())} (défaut: pitch).",
    )
    parser.add_argument(
        "--slides", "-s",
        type=int,
        default=12,
        help="Nombre de slides souhaité (défaut: 12).",
    )
    parser.add_argument(
        "--audience", "-a",
        default="",
        help="Description de l'audience cible (optionnel).",
    )
    parser.add_argument(
        "--duree", "-d",
        type=int,
        default=None,
        help="Durée de la présentation en minutes (optionnel).",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Fichier de sortie .md (défaut: <titre_normalise>_outline.md).",
    )

    return parser.parse_args()


def normalize_filename(titre: str, pres_type: str) -> str:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in titre.lower())
    safe = safe.strip("_")
    return f"{safe}_{pres_type}_outline.md"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    if args.slides < 3:
        print("[ERREUR] Le nombre de slides minimum est 3.")
        sys.exit(1)
    if args.slides > 200:
        print("[ERREUR] Le nombre de slides maximum supporté est 200.")
        sys.exit(1)

    output_file = args.output or normalize_filename(args.titre, args.type)

    print(f"Generation du plan de presentation...")
    print(f"  Titre    : {args.titre}")
    print(f"  Type     : {args.type} ({STRUCTURES[args.type]['label']})")
    print(f"  Slides   : {args.slides}")
    if args.audience:
        print(f"  Audience : {args.audience}")
    if args.duree:
        print(f"  Duree    : {args.duree} min")

    try:
        content = generate_outline(
            titre       = args.titre,
            pres_type   = args.type,
            slides_total= args.slides,
            audience    = args.audience,
            duree       = args.duree,
            output_file = output_file,
        )
    except ValueError as e:
        print(f"[ERREUR] {e}")
        sys.exit(1)

    output_path = Path(output_file)
    try:
        output_path.write_text(content, encoding="utf-8")
        print(f"\n[OK] Plan genere : {output_path.resolve()}")
        print(f"\nStructure :")
        struct = STRUCTURES[args.type]
        sections = adjust_slides(struct["sections"], args.slides)
        for s in sections:
            print(f"  Section {s['id']:2d} | {s['slides']:2d} slide(s) | {s['titre']}")
        total = sum(s["slides"] for s in sections)
        print(f"  {'':8} | {total:2d} slides au total")
        print(f"\nOuvrir avec : open {output_path} (macOS) ou cat {output_path}")
    except OSError as e:
        print(f"[ERREUR] Impossible d'ecrire '{output_file}' : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
