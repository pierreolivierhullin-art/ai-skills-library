# Etudes de Cas — Design Visuel en Entreprise

## Vue d'Ensemble

Ces etudes de cas illustrent des transformations reelles : une startup qui uniformise sa communication visuelle avec Canva, une equipe produit qui implemente Figma pour la collaboration designers/PMs, une PME qui lance une identite visuelle complete sans designer, et une equipe marketing qui multiplie sa production de contenu avec l'IA.

---

## Cas 1 — Scale-up SaaS : De la Cacophonie Visuelle au Brand Kit Unifie (Canva)

### Contexte

Scale-up SaaS RH (80 employes, 5 personnes marketing, 0 designer dedie). Probleme : chaque membre de l'equipe cree ses propres visuels LinkedIn, presentations clients et rapports avec des outils et styles differents. Resultat : 6 styles graphiques differents en circulation, logo dans 3 versions dont une fausse couleur, polices Calibri + Arial + Helvetica melangees.

Le directeur marketing new hire constate que les prospects ne reconnaissent pas la marque en second contact. Le score de reconnaissance de marque est mesure a 23% (versus 65% chez les concurrents directs).

### Audit Initial

Inventaire des supports existants :
- 12 templates de presentations differents (dont 3 avec le mauvais logo)
- Posts LinkedIn : 0 coherence (certains avec infographies complexes, d'autres texte seul, polices variees)
- Rapports clients : Word basique, pas de mise en page
- Fiches produits : PDF generes par le dev depuis HTML, non-brandees

**Probleme principal identifie** : pas de "source de verite" graphique accessible a tous.

### Solution Implementee (8 semaines)

**Semaine 1-2 — Definition du brand** :
Travail avec un freelance graphiste (budget : 1 500 EUR, 3 jours) pour definir :
- Logo finalise (3 versions : couleur, blanc, icone seule) en SVG
- Palette : primaire #2563EB (bleu), secondaire #7C3AED (violet), accent #F59E0B (ambre), 5 neutres
- Typographie : Poppins (titres) + Inter (corps) — toutes deux disponibles gratuitement sur Google Fonts
- Style graphique : formes geometriques simples, coins arrondis 8px, icones Heroicons (outline)

**Semaine 3-4 — Creation du Brand Kit Canva** :
- Compte Canva Teams (12 EUR/utilisateur/mois, 5 utilisateurs = 60 EUR/mois)
- Upload du logo (3 versions), configuration des couleurs et polices dans le Brand Hub
- Creation des templates "valides" :
  - Presentation client 16:9 (20 slides type)
  - Rapport mensuel A4
  - Post LinkedIn (3 variantes : stat, quote, infographie simple)
  - Story Instagram
  - Newsletter header
  - Signature email

**Semaine 5-6 — Formation et adoption** :
Session de 2h avec toute l'equipe marketing + commerciaux :
- "Voici le Brand Kit — utiliser UNIQUEMENT les couleurs et polices du kit"
- Demo live de Magic Resize pour adapter un post LinkedIn en story
- Regles simples : max 2 polices, max 4 couleurs, toujours le logo haut-droite
- Acces en lecture seule aux templates, duplication pour modifier

**Semaine 7-8 — Retrospective et ajustements** :
Review des 30 premiers designs produits. 8 corrections sur les templates (zones de texte trop petites, une couleur non-accessible). Publication des "design dos and don'ts" en 1 page dans le Notion interne.

### Resultats (6 mois post-implementation)

| Metrique | Avant | Apres |
|---|---|---|
| Styles graphiques en circulation | 6 differents | 1 (coherent) |
| Temps de creation d'un post LinkedIn | 45 min | 12 min |
| Temps de creation d'une presentation client | 3h | 1h |
| Reconnaissance de marque (survey prospect) | 23% | 61% |
| Nombre de visuels produits/mois | 8 | 47 |
| Budget design freelance mensuel | 800 EUR/mois | 150 EUR/mois |

**ROI** : investissement initial (1 500 EUR graphiste + 60 EUR/mois Canva) → economie 650 EUR/mois + gain de 6h/semaine equipe marketing → payback en 3 mois.

**Lecon principale** : la technologie (Canva) n'est qu'une partie de la solution. La cle est la "source de verite" graphique — un brand kit accessible a tous avec des regles claires. Sans la formation et les templates valides, l'outil seul ne change rien.

---

## Cas 2 — PME Industrielle : Identite Visuelle Complete sans Designer (Canva + Midjourney)

### Contexte

PME specialisee dans les equipements de mesure industriels (45 employes, 0 designer, pas de communication digitale). Le PDG veut lancer un site web et une presence LinkedIn pour prospecter les grandes industries. Budget design : 3 000 EUR (pour tout — identite visuelle, site web, supports commerciaux).

Contrainte : le secteur industriel attend une communication sobre et technique, pas "startup".

### Processus de Creation

**Phase 1 — Inspiration et direction artistique (1 semaine)** :
- Pinterest board avec 50 references de communications B2B industrielles (Schneider Electric, Endress+Hauser, ABB)
- Pattern identifie : couleurs foncees (navy, gris anthracite), accent orange ou jaune, typographies sans-serif geometriques
- Moodboard cree dans Canva (grille de 12 images + palette de couleurs extraites)

**Phase 2 — Logo avec Canva Logo Maker** :
- 15 variantes generees avec Canva Logo Maker (description : "precision measurement equipment, industrial, technical, reliable, blue-grey palette")
- Selection de 3 finalistes, feedback du PDG et de 2 commerciaux
- Choix final : monogramme geometrique "M" avec ligne de mesure, navy #1E3A5F, police Barlow Condensed
- Export SVG (toutes variantes)
- Cout : 0 EUR (Canva Pro inclus dans l'abonnement)
- Vs devis agence : 1 500-3 000 EUR pour un logo

**Phase 3 — Images avec Midjourney** :
Le secteur industriel necessite des photos d'equipements de mesure en situation. Les photos stock generiques sont trop generiques ou trop americaines.

Prompts Midjourney utilises :
```
"Industrial measurement equipment in a factory, precision instruments,
steel surfaces, professional B2B photography, shallow depth of field,
blue grey tones, Schneider Electric style --ar 16:9 --style raw"

"Engineer inspecting industrial gauges and sensors on a production line,
professional corporate photography, natural lighting, European manufacturing
context --ar 16:9 --v 6"
```

Generation de 40 images → selection de 8 pour site web et LinkedIn → retouche mineure (Background Remover Canva si necessaire).

**Phase 4 — Templates Canva** :
- Presentation commerciale (25 slides)
- Fiche technique produit (A4 recto-verso)
- Post LinkedIn (3 variantes)
- Signature email

### Resultats

| Element | Cout (budget contraint) | Cout equivalent agence |
|---|---|---|
| Logo | 0 EUR (Canva Pro) | 1 500-3 000 EUR |
| Images (40 visuels) | 30 EUR (Midjourney Pro 1 mois) | 2 000-5 000 EUR (photo-stock pro) |
| Templates Canva (10 formats) | 0 EUR (temps interne : 3 jours) | 2 000-4 000 EUR |
| **Total** | **~30 EUR + 3 jours** | **~7 000-12 000 EUR** |

**Avant/Apres** :
- Avant : communication zero, pas de presence digitale
- Apres : site WordPress lance (template ThemeForest 59 EUR + contenu maison), LinkedIn actif, 3 RDV prospects en 30 jours sur la base des nouveaux supports

**Lecon** : pour une PME B2B avec contraintes budgetaires fortes, l'IA generative (Midjourney) + Canva permet une qualite "acceptable" pour demarrer. La limite est atteinte quand la marque est etablie et que l'identite doit etre differenciante — la, un designer professionnel devient indispensable.

---

## Cas 3 — Equipe Produit : Implantation de Figma pour la Collaboration PM/Designer

### Contexte

Scale-up fintech (200 employes, 4 designers, 6 product managers). Probleme critique : les PMs decrivent les features en texte (specs Word), les designers interpretent, il y a systematiquement 2-3 cycles d'aller-retour avant un accord. Developpement retarde en moyenne de 2 semaines par feature sur la base de mauvaises specifications visuelles.

Les designers utilisent Figma depuis 1 an. Les PMs n'y ont jamais touche.

### Programme d'Adoption Figma pour les PMs (4 semaines)

**Semaine 1 — Onboarding minimaliste** :
Atelier de 3h pour les 6 PMs :
- Navigation, lecture d'un fichier Figma (pas de creation)
- Les commentaires (shortcut C) : comment annoter directement sur le design
- Inspect mode (Dev Mode) : lire les specs sans modifier
- Le prototype : comment tester un flow sans code

**Semaine 2 — Wireframing basse fidelite** :
Les PMs apprennent a creer des wireframes en basse fidelite (pas de design final) :
- Utilisation du kit wireframe interne (composants gris neutres : boutons, inputs, cards)
- Regles etablies : LES PMs font du wireframing SEULEMENT en basse fidelite, avec le kit wireframe. PAS de couleurs, PAS de typographie, PAS de style.
- Objectif : communiquer la structure et les interactions, pas le style

**Semaine 3-4 — Workflow collaboratif** :
Nouveau processus :
1. PM cree un wireframe basse fidelite dans Figma (section dedie "PM Wireframes")
2. PM commente le wireframe pour expliquer les use cases
3. PM tague @designer dans les commentaires pour revue
4. Designer refine en haute fidelite EN PARTANT du wireframe PM
5. PM valide le hi-fi directement dans Figma (commentaires resolus)
6. Handoff vers dev via Dev Mode (pas de redaction de specs Word)

### Resultats (3 mois post-implementation)

| Metrique | Avant | Apres |
|---|---|---|
| Cycles de revue design/PM par feature | 2.8 | 1.2 |
| Delai average PM → developpement | 3.5 semaines | 1.5 semaines |
| Satisfaction PMs sur la clarte du processus | 52/100 | 81/100 |
| Satisfaction designers (qualite des specs recues) | 41/100 | 79/100 |
| Specs Word produites par les PMs | 6/mois | 0/mois |

**Economies** : 2 semaines gagnees par feature × 8 features/trimestre × 15 000 EUR de cout dev/semaine = 240 000 EUR/an.

**Obstacle rencontre** : 2 PMs sur 6 ont refuse d'utiliser Figma ("trop technique", "pas mon metier"). Solution : les faire utiliser uniquement en "view only" pour les revues — les wireframes sont crees par les designers a partir des descriptions des PMs reticents. Compromis acceptable.

**Lecon** : ne pas imposer Figma pour la creation de design final aux non-designers — c'est contre-productif. Le wireframing basse fidelite avec un kit contraint est le sweet spot : assez simple pour les PMs, assez informatif pour les designers.

---

## Cas 4 — Agence Marketing : Multiplication x4 de la Production avec l'IA Generative

### Contexte

Agence marketing digitale (15 personnes, dont 2 designers). Demande clients multipliee par 2 en 18 mois sans recrutement supplementaire. Les 2 designers sont sur-sollicites : 70% du temps sur des taches repetitives (resize des formats, generation d'images stock, retouches basiques). Objectif : multiplier la production de contenu visuel sans recruter.

### Stack AI Adopte (2025)

**Generation d'images** :
- **Midjourney v6** (30 EUR/mois) : visuels hero, illustrations, atmospheres
- **Adobe Firefly** (integre Creative Cloud, deja paye) : photos realistes pour clients en secteurs reglementes (images licenciees, pas de risque legal)
- **DALL-E 3 via ChatGPT Pro** (20 EUR/mois) : iterations rapides de concepts

**Creation et adaptation** :
- **Canva Magic Studio** (inclus Pro) : Magic Resize, Background Remover, Text to Image
- **Adobe Express** : pour les clients ayant Creative Cloud

**Workflow AI Typique — Post Reseaux Sociaux**

Avant (2h par client par semaine) :
1. Recherche photo stock (30 min)
2. Achat photo stock (10-30 EUR par image)
3. Retouches Photoshop (30 min)
4. Creation du visuel dans Canva (30 min)
5. Resize pour 4 formats (30 min)

Apres (35 min par client par semaine) :
1. Generation image Midjourney avec prompt optimise (10 min, 4 variantes)
2. Selection + Background Remover si necessaire (5 min)
3. Assemblage Canva avec template (10 min)
4. Magic Resize automatique (5 min)
5. Verification qualite et export (5 min)

### Prompts Optimises par Categorie

**Technologie / SaaS** :
```
"Modern tech office with diverse professionals collaborating,
clean workspace, screens with dashboards, natural daylight,
editorial photography style, European context, --ar 16:9 --style raw"
```

**Finance / Consulting** :
```
"Professional business meeting in a boardroom, executive team
reviewing data on large screens, confident and collaborative,
photorealistic, neutral corporate tones --ar 16:9"
```

**E-commerce / Retail** :
```
"Product flat lay on white marble background, minimalist styling,
natural shadows, commercial photography style, high key lighting
--ar 1:1 --style raw"
```

**Sustainability / ESG** :
```
"Green energy infrastructure with wind turbines and solar panels
in European landscape, golden hour, inspiring and hopeful,
editorial photography --ar 16:9 --v 6"
```

### Gestion du Droit a l'Image et des Licences

**Risques identifies** :
- Midjourney : peut generer des personnages ressemblant a des personnalites reelles → politique interne : ne jamais utiliser les faces de personnages generes pour des campagnes publiees
- Modeles humains generes : eviter pour les secteurs de sante et finance (risque de perceptions discriminatoires)
- Marques dans les images : Midjourney peut generer des logos → verifier et regenerer si detecte

**Politique adoptee par l'agence** :
- Adobe Firefly pour tout ce qui implique des personnes (entraine sur donnees licenciees)
- Midjourney pour les paysages, products, atmospheres, illustrations
- Systematiquement : verifier les mains (artefacts frequents), le texte dans l'image (souvent illisible), les arriere-plans complexes

### Resultats (6 mois)

| Metrique | Avant | Apres |
|---|---|---|
| Temps de production / post client | 2h | 35 min |
| Visuels produits / semaine | 45 | 180 |
| Cout photos stock / mois | 380 EUR | 50 EUR |
| Satisfaction client (qualite percue) | 74/100 | 81/100 |
| Heures designers sur taches repetitives | 70% | 25% |
| Heures designers sur taches creatives | 30% | 75% |

**Impact sur les designers** : la requalification vers le travail creatif (direction artistique, brand strategy, campagnes complexes) a augmente la satisfaction au travail (eNPS de 32 a 61) et permis de conserver les 2 profils sans recruter.

**Lecon principale** : l'IA generative ne remplace pas le designer — elle elimine les taches repetitives et permet au designer de se concentrer sur la valeur ajoutee. Le gain de productivite realisable est de 3-4x sur le contenu repetitif, mais requiert un investissement en "prompt engineering" de 2-4 semaines pour atteindre la qualite constante. La gestion des risques legaux (licences d'images) doit etre une priorite avant le deploiement a grande echelle.
