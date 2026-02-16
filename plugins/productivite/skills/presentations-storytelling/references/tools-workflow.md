# Outils & Workflow — PowerPoint, Google Slides, Keynote, Gamma, Beautiful.ai, Marp

## Overview

Ce document de reference couvre les outils de creation de presentations, leurs forces specifiques, et les workflows professionnels pour produire des decks de haute qualite efficacement. Le paysage des outils de presentation a profondement evolue entre 2024 et 2026 avec l'integration de l'IA generative, la collaboration temps reel et l'emergence d'outils specialises. Utiliser ce guide pour choisir l'outil adapte a chaque contexte, maitriser les fonctionnalites avancees et optimiser le workflow de bout en bout — du brief initial a la livraison finale.

---

## Microsoft PowerPoint — Le Standard Corporate

### Position dans l'ecosysteme

PowerPoint reste l'outil dominant avec plus de 500 millions d'utilisateurs actifs mensuels (2025). Il est le standard de fait dans les grandes entreprises, le conseil en strategie, la banque d'investissement et les administrations. Sa maitrise avancee est un prerequis dans de nombreux contextes professionnels.

### Fonctionnalites avancees essentielles

#### Morph Transitions

La transition Morph (disponible depuis PowerPoint 2019 et Microsoft 365) cree des animations fluides entre deux slides en detectant automatiquement les elements communs et en les animant :

- **Usage** : deplacer, redimensionner, recolorer ou faire apparaitre/disparaitre des elements entre deux slides sans creer manuellement des animations
- **Technique** : dupliquer une slide, modifier la position/taille/couleur des elements, puis appliquer la transition "Morph" a la seconde slide
- **Cas d'usage** : zoom sur un detail d'un schema, mise en avant progressive d'un element dans un graphique, defilement narratif
- **Limite** : ne fonctionne que si les elements portent le meme nom sur les deux slides (renommer dans le volet Selection pour forcer le matching)

#### PowerPoint Designer

L'assistant Designer (IA integree) propose automatiquement des layouts de slide bases sur le contenu insere :

- **Activation** : inserer du texte, une image ou un graphique, et Designer propose des mises en page alternatives dans le panneau lateral
- **Force** : acceleration de la creation, inspiration de layouts
- **Limite** : les suggestions sont generiques et ne respectent pas toujours les design systems avances
- **Bonne pratique** : utiliser Designer comme point de depart, puis ajuster manuellement

#### Microsoft Copilot dans PowerPoint

Depuis 2024, Copilot est integre a PowerPoint pour les licences Microsoft 365 Copilot :

- **Generation de deck** : generer une presentation complete a partir d'un prompt textuel ou d'un document Word/PDF
- **Resume** : condenser un deck long en version executive
- **Reorganisation** : reorganiser les slides selon une logique narrative differente
- **Design** : appliquer automatiquement des themes et des layouts
- **Limites** : les decks generes necessitent toujours un travail d'edition significatif pour atteindre un niveau professionnel. Ne pas utiliser Copilot comme produit fini.

#### Sections et Organisation

- **Sections** : organiser les slides en sections nommees dans le volet de navigation. Indispensable pour les decks de plus de 20 slides.
- **Slide Sorter view** : vue d'ensemble de toutes les slides en miniature. Utiliser cette vue pour verifier le flow narratif, l'equilibre visuel et la coherence des titres.
- **Custom Shows** : creer des sous-ensembles de slides pour des audiences differentes a partir d'un meme deck master.

#### Recording et Export Video

- **Enregistrement** : enregistrer la voix, la webcam et les annotations directement dans PowerPoint
- **Export video** : exporter en MP4 (Full HD ou 4K) pour des presentations asynchrones
- **Usage** : demos produit, modules de formation, presentations pour les absents
- **Bonne pratique** : enregistrer section par section pour faciliter l'edition

#### Slide Master et Layouts

- **Slide Master** : definir tous les elements de design recurrents (fond, logo, typo, couleurs, placeholders) dans le masque de diapositive
- **Custom Layouts** : creer des layouts specifiques (data slide, quote slide, comparison slide) dans le Slide Master pour que les utilisateurs les selectionnent
- **Avantage** : une modification du Slide Master se propage automatiquement a toutes les slides utilisant ce layout
- **Maintenance** : auditer le Slide Master chaque trimestre pour supprimer les layouts inutilises et ajouter les nouveaux besoins

### Raccourcis essentiels PowerPoint

| Raccourci | Action |
|---|---|
| `Ctrl + D` | Dupliquer la slide ou l'objet selectionne |
| `Ctrl + Shift + C/V` | Copier/Coller la mise en forme |
| `Alt + F5` | Lancer le mode Presentateur depuis la slide en cours |
| `Ctrl + G` | Grouper les objets selectionnes |
| `Ctrl + Shift + G` | Degrouper |
| `Tab` | Naviguer entre les placeholders d'une slide |
| `F5` | Lancer le diaporama depuis le debut |
| `Shift + F5` | Lancer depuis la slide en cours |

---

## Google Slides — La Collaboration Native

### Position dans l'ecosysteme

Google Slides est l'outil de presentation dominant dans les startups, les entreprises utilisant Google Workspace et les equipes distribuees. Sa force reside dans la collaboration en temps reel, la simplicite et l'integration avec l'ecosysteme Google.

### Forces specifiques

#### Collaboration temps reel

- **Edition simultanee** : plusieurs utilisateurs editent le meme deck en temps reel avec curseurs nommes et colores
- **Commentaires et suggestions** : commenter des slides specifiques, assigner des actions, resoudre les commentaires
- **Historique de versions** : chaque modification est tracee avec la possibilite de revenir a n'importe quelle version precedente
- **Partage granulaire** : droits de lecture, commentaire ou edition par utilisateur ou par domaine

#### Google Gemini dans Slides

Depuis 2025, Gemini est integre a Google Slides :

- **Generation d'images** : generer des images a partir de descriptions textuelles directement dans Slides
- **Generation de slides** : creer des slides a partir de prompts
- **Resume** : synthetiser des decks longs
- **Limite** : maturite inferieure a Copilot pour la generation de presentations completes (2025-2026)

#### Add-ons et extensions

L'ecosysteme d'add-ons etend significativement les capacites de Google Slides :

| Add-on | Fonction |
|---|---|
| **Pear Deck** | Interactivite en temps reel (questions, quizz, sondages) pendant la presentation |
| **Flaticon** | Bibliotheque d'icones integree directement dans Slides |
| **Lucidchart** | Insertion de diagrammes et organigrammes editables |
| **Slido** | Sondages et Q&A en direct pendant la presentation |
| **Extensis Fonts** | Acces a la bibliotheque Google Fonts etendue |

### Limites de Google Slides

- **Animations limitees** : moins de types d'animations et de transitions que PowerPoint ou Keynote
- **Design avance** : les capacites de design sont inferieures a PowerPoint (pas de Morph, pas d'edition de formes complexes)
- **Performance** : les decks de plus de 50 slides avec beaucoup d'images peuvent etre lents
- **Offline** : le mode hors-ligne existe mais reste moins fiable que les outils desktop
- **Polices** : limite a Google Fonts (pas de polices custom sauf workaround)

### Bonne pratique Google Slides

- Utiliser le systeme de templates partages (Team Drive) pour maintenir la coherence de marque
- Lier des graphiques Google Sheets qui se mettent a jour automatiquement dans les slides
- Utiliser le mode Speaker Notes pour les contenus detailles plutot que de surcharger les slides
- Exploiter les linked slides pour reutiliser des slides d'un deck dans un autre (mise a jour automatique)

---

## Apple Keynote — Le Design Premium

### Position dans l'ecosysteme

Keynote est l'outil de presentation d'Apple, gratuit avec macOS et iOS. Il est privilegie par les designers, les creatifs, les startups du monde Apple et pour les keynotes de conference. Il produit les presentations les plus visuellement elegantes grace a un moteur de rendu superieur.

### Forces specifiques

#### Qualite d'animation et de rendu

- **Magic Move** : equivalent de Morph dans PowerPoint, mais avec un rendu plus fluide et plus de controle sur les parametres (duree, acceleration, trajectoire)
- **Animations cinematiques** : Keynote offre des animations d'une qualite superieure a tout autre outil de presentation (transitions 3D, effets de particules, animations de texte lettre par lettre)
- **Rendu typographique** : le rendu des polices sous macOS est superieur a celui de Windows, donnant un aspect plus professionnel aux textes

#### Fonctionnalites uniques

- **Instant Alpha** : supprimer l'arriere-plan d'une image directement dans Keynote sans outil externe
- **Shapes avancees** : edition de formes vectorielles natives (edition de points d'ancrage)
- **Themes** : systeme de themes avec variantes (clair/sombre) et master slides editables
- **iPhone/iPad comme telecommande** : utiliser un iPhone comme clicker avec affichage des notes et de la slide suivante
- **Keynote Live** : partager une presentation en direct via un lien web (l'audience suit en temps reel sans installation)

### Limites de Keynote

- **Ecosysteme Apple uniquement** : pas de version Windows native. L'export PowerPoint existe mais perd des animations et de la mise en page.
- **Collaboration** : la collaboration en temps reel via iCloud est fonctionnelle mais moins mature que Google Slides
- **Adoption corporate** : faible penetration dans les grandes entreprises qui standardisent sur Microsoft
- **Compatibilite** : un deck Keynote exporte en PowerPoint necessite toujours une verification manuelle des alignements, polices et animations

### Quand choisir Keynote

- Presentations de conference et keynotes (la qualite visuelle fait la difference)
- Pitchs de startup (premium et moderne)
- Equipes 100% Apple
- Presentations ou les animations sont un element narratif important (demos produit, storytelling visuel)

---

## Outils IA — Gamma, Beautiful.ai, Tome, Pitch

### Gamma

**Positionnement** : generation de presentations par IA a partir de prompts textuels ou de documents.

| Critere | Detail |
|---|---|
| **Input** | Prompt textuel, document (PDF, Word, Google Doc), URL, notes |
| **Output** | Presentation web interactive, exportable en PDF/PPTX |
| **Force** | Generation rapide (< 2 minutes pour un deck de 15 slides), design moderne par defaut, format web interactif |
| **Limite** | Personnalisation limitee, design generique si non edite, dependance au cloud |
| **Prix** | Freemium (watermark) + plans payants a partir de ~10 USD/mois |
| **Cas d'usage ideal** | Premier draft rapide, brainstorming visuel, presentations internes non-critiques |

**Workflow recommande avec Gamma :**
1. Rediger le brief et le plan narratif en texte brut
2. Generer un premier draft avec Gamma
3. Exporter en PowerPoint ou Google Slides
4. Editer manuellement pour appliquer le design system et affiner le contenu
5. Finaliser dans l'outil cible

### Beautiful.ai

**Positionnement** : design de slides assiste par IA avec des smart templates.

| Critere | Detail |
|---|---|
| **Input** | Selection de smart templates, insertion de contenu |
| **Output** | Presentation web, exportable en PDF/PPTX |
| **Force** | Les smart templates s'adaptent automatiquement au contenu (ajout/suppression d'elements). Le design reste coherent meme quand le contenu change. |
| **Limite** | Moins de liberte de design que PowerPoint, templates reconnaissables, dependance au cloud |
| **Prix** | A partir de ~12 USD/mois |
| **Cas d'usage ideal** | Equipes sans designer qui veulent des slides professionnelles rapidement |

### Tome

**Positionnement** : storytelling visuel genere par IA, positionne a l'intersection de la presentation et du document.

| Critere | Detail |
|---|---|
| **Input** | Prompt textuel, documents, donnees |
| **Output** | Presentation narrative au format web |
| **Force** | Mise en page editoriale, integration de contenus multimedia, generation d'images IA integree |
| **Limite** | Format proprietaire, export limite, moins adapte aux presentations formelles corporate |
| **Prix** | Freemium + plans payants |
| **Cas d'usage ideal** | Presentations de concept, pitchs creatifs, storytelling visuel |

### Pitch

**Positionnement** : outil de presentation collaboratif moderne, alternative directe a Google Slides avec un meilleur design.

| Critere | Detail |
|---|---|
| **Input** | Creation manuelle avec templates, collaboration temps reel |
| **Output** | Presentation web, PDF, PPTX |
| **Force** | Collaboration superieure a PowerPoint, design system integre, analytics de presentation (qui a ouvert le deck, temps passe par slide), integration avec les outils de travail (Slack, Notion) |
| **Limite** | Adoption limitee comparee aux trois grands (PPT/Slides/Keynote), courbe d'apprentissage |
| **Prix** | Freemium + plans a partir de ~8 USD/mois/utilisateur |
| **Cas d'usage ideal** | Startups, equipes commerciales qui envoient des decks et veulent des analytics |

### Comparatif des outils IA

| Critere | Gamma | Beautiful.ai | Tome | Pitch |
|---|---|---|---|---|
| **Generation IA** | Excellente | Bonne | Excellente | Moyenne |
| **Design automatique** | Bon | Excellent | Bon | Bon |
| **Personnalisation** | Moyenne | Limitee | Moyenne | Bonne |
| **Collaboration** | Basique | Basique | Basique | Excellente |
| **Export PPTX** | Oui | Oui | Limite | Oui |
| **Analytics** | Non | Non | Non | Oui |
| **Offline** | Non | Non | Non | Non |

---

## Marp — Presentations as Code

### Positionnement

Marp (Markdown Presentation Ecosystem) est un outil open source qui transforme du Markdown en presentations. Il est destine aux developpeurs et aux equipes techniques qui souhaitent versionner leurs presentations dans Git et les generer automatiquement.

### Syntaxe de base

```markdown
---
marp: true
theme: default
paginate: true
---

# Titre de la presentation

Auteur — Date

---

## Section 1

- Point 1
- Point 2

![bg right](image.jpg)

---

## Section 2

| Colonne A | Colonne B |
|-----------|-----------|
| Valeur 1  | Valeur 2  |
```

### Forces de Marp

- **Version control** : les presentations sont des fichiers Markdown versionnables dans Git. Chaque modification est tracee avec diff.
- **CI/CD** : generer automatiquement les slides (HTML, PDF, PPTX) dans un pipeline CI/CD (GitHub Actions, GitLab CI)
- **Themes CSS** : personnaliser l'apparence avec du CSS standard. Creer des themes d'equipe reutilisables.
- **Legerete** : un fichier Markdown de 50 lignes genere un deck de 15 slides. Pas de fichier binaire lourd.
- **VS Code integration** : extension VS Code avec preview en temps reel

### Limites de Marp

- **Design limite** : les layouts complexes (grilles, compositions avancees) sont difficiles ou impossibles en Markdown pur
- **Courbe d'apprentissage** : necessite la connaissance de Markdown et du CSS pour les personnalisations
- **Pas de collaboration temps reel** : la collaboration passe par Git (pull requests, merge)
- **Animations** : pas d'animations natives (le format est statique)
- **Audience** : non adapte aux presentations commerciales ou executives qui attendent un design sophistique

### Alternatives a Marp

| Outil | Difference avec Marp |
|---|---|
| **reveal.js** | Framework HTML/JavaScript plus puissant, animations, plugins, mais plus complexe |
| **Slidev** | Base sur Vue.js, composants interactifs, mode presentateur avance, syntaxe Markdown etendue |
| **Remark** | Markdown vers HTML, simple et leger, moins de fonctionnalites que Marp |

### Quand utiliser Marp

- Presentations techniques pour des equipes de developpement
- Documentation technique versionnee
- Generation automatique de slides a partir de donnees (scripts de generation)
- Equipes qui utilisent deja Git pour tout le reste

---

## Figma-to-Slides Workflow

### Principes

Certaines equipes de design creent les presentations dans Figma pour un controle total du design, puis exportent vers PowerPoint ou PDF.

### Workflow detaille

1. **Creer un fichier Figma** avec des frames au format 16:9 (1920x1080px)
2. **Definir les composants reutilisables** : titres, blocs de contenu, graphiques, icones
3. **Utiliser Auto Layout** pour des mises en page responsives
4. **Appliquer les design tokens** de la marque (couleurs, typographie, espacement)
5. **Exporter** :
   - **PDF** : export natif de haute qualite (File → Export frames to PDF)
   - **PowerPoint** : via le plugin Figma "Pitchdeck" ou "Figma to Google Slides"
   - **Images** : export frame par frame en PNG haute resolution pour insertion manuelle

### Avantages

- Controle pixel-perfect du design
- Acces aux composants et bibliotheques design partagees
- Collaboration designer/content en temps reel dans Figma
- Coherence parfaite avec le design system de l'entreprise

### Inconvenients

- Les presentations Figma ne sont pas editables dans PowerPoint/Slides apres export image
- Pas de mode presentateur natif (Figma n'est pas un outil de presentation)
- Workflow plus lent pour les modifications de derniere minute
- Necessite un designer ou une maitrise de Figma

---

## Asset Management — Icones, Images, Templates

### Organisation des assets

Centraliser les assets de presentation dans un espace partage et organise :

```
/presentation-assets/
├── /templates/
│   ├── template-corporate-v3.2.pptx
│   ├── template-pitch-deck-v2.1.pptx
│   └── template-data-report-v1.4.pptx
├── /icons/
│   ├── /phosphor-icons/
│   └── /custom-brand-icons/
├── /images/
│   ├── /team-photos/
│   ├── /product-screenshots/
│   └── /stock-approved/
├── /charts/
│   ├── chart-styles-guide.pptx
│   └── data-viz-templates.pptx
├── /logos/
│   ├── logo-primary.svg
│   ├── logo-white.svg
│   └── logo-monochrome.svg
└── /fonts/
    ├── Inter/
    └── brand-font/
```

### Sources d'icones recommandees

| Source | Style | Licence | Format |
|---|---|---|---|
| **Phosphor Icons** | Line, fill, duotone | MIT (gratuit) | SVG, React, PNG |
| **Heroicons** | Outline, solid | MIT (gratuit) | SVG |
| **Tabler Icons** | Line | MIT (gratuit) | SVG |
| **Lucide** | Line (fork de Feather) | ISC (gratuit) | SVG |
| **Noun Project** | Varies | Freemium | SVG, PNG |
| **Flaticon** | Varies | Freemium | SVG, PNG, EPS |

### Sources d'images recommandees

| Source | Type | Licence | Prix |
|---|---|---|---|
| **Unsplash** | Photos haute qualite | Gratuit commercial | Gratuit |
| **Pexels** | Photos et videos | Gratuit commercial | Gratuit |
| **iStock** | Photos, illustrations, videos | License commerciale | Payant |
| **Midjourney / DALL-E** | Illustrations IA generee | Varies | Abonnement |
| **Storyset (Freepik)** | Illustrations SVG animables | Freemium | Gratuit/Payant |

---

## Version Control et Collaboration

### Workflow de collaboration sur un deck

#### Etape 1 — Brief et cadrage
- L'auteur principal cree le brief (audience, objectif, message central) et le partage
- L'equipe valide le brief avant toute creation de slide

#### Etape 2 — Structure narrative
- L'auteur principal ecrit le plan narratif (action titles de chaque slide)
- Revue du plan par un pair ou un manager
- Validation avant de passer au design

#### Etape 3 — Creation
- Creation des slides sur la base du plan narratif valide
- Si plusieurs auteurs : assigner des sections a chaque contributeur
- Utiliser les commentaires dans l'outil pour les questions et feedbacks

#### Etape 4 — Revue design
- Un pair ou un design lead verifie la coherence visuelle
- Checklist : alignement, couleurs, polices, white space, lisibilite
- Corrections appliquees par l'auteur

#### Etape 5 — Revue finale
- Le manager ou le sponsor valide le contenu et le message
- Verification technique (liens, polices, animations, export)
- Version finale verrouillee

### Conventions de nommage des fichiers

```
[Projet]_[Type]_[Audience]_[Date]_v[Version].[ext]

Exemples :
- ProjetAlpha_PitchDeck_Investisseurs_2026-02_v3.2.pptx
- Q1-Review_Board-Presentation_COMEX_2026-01_v1.0.pptx
- ProductLaunch_SalesDeck_Clients-Enterprise_2026-03_v2.1.pptx
```

### Gestion des versions

- Incrementer la version mineure (v1.1, v1.2) pour les corrections et ajustements
- Incrementer la version majeure (v2.0, v3.0) pour les refontes significatives
- Conserver les 3 dernieres versions accessibles, archiver les precedentes
- Nommer la version finale avec un suffixe `_FINAL` ou `_APPROVED`
- Dans Google Slides : utiliser la fonctionnalite de nommage de versions (File → Version history → Name current version)

---

## Export et Optimisation

### Formats d'export

| Format | Usage | Outil |
|---|---|---|
| **PDF** | Envoi par email, archivage, impression | Tous les outils |
| **PPTX** | Edition par le destinataire, compatibilite | PowerPoint, Google Slides, Keynote |
| **HTML** | Presentation web interactive | Gamma, Pitch, Marp, reveal.js |
| **MP4** | Presentation video asynchrone | PowerPoint, Keynote |
| **PNG/JPEG** | Slides individuelles pour insertion dans d'autres documents | Tous les outils |
| **GIF** | Animations courtes pour email ou chat | Keynote (export natif) |

### Optimisation du poids des fichiers

Les presentations lourdes posent des problemes d'envoi par email, de chargement et de stockage :

| Technique | Reduction estimee |
|---|---|
| **Compresser les images** dans PowerPoint (Format → Compress Pictures → 150 ppi pour ecran) | 50-80% |
| **Supprimer les slides masquees** inutilisees | Variable |
| **Supprimer les animations complexes** non necessaires | 10-20% |
| **Utiliser des images JPEG** plutot que PNG pour les photos (PNG pour les graphiques avec transparence) | 30-60% |
| **Redimensionner les images** a la taille d'affichage reelle (pas d'image 4000px affichee en 400px) | 60-90% |
| **Cible** : un deck de 30 slides ne devrait pas depasser 10 MB | — |

### Verification pre-export

Avant d'exporter le deck final, verifier :
- [ ] Toutes les polices sont embarquees ou standard (pour eviter les substitutions)
- [ ] Les liens hypertexte fonctionnent
- [ ] Les animations se deroulent dans le bon ordre
- [ ] Le numero de page est correct sur chaque slide
- [ ] Le contenu confidentiel est supprime si le deck est partage a l'externe
- [ ] Les speaker notes ne contiennent pas de commentaires internes sensibles
- [ ] Le nom de fichier est conforme a la convention de nommage

---

## Delivery — Presenter avec Impact

### Mode Presentateur

Tous les outils majeurs offrent un mode presentateur (Presenter View) qui affiche :
- La slide en cours en plein ecran pour l'audience
- Les speaker notes visibles uniquement par le presentateur
- La slide suivante en apercu
- Le chronometre / timer
- Les outils d'annotation (surbrillance, pointeur laser virtuel)

**Configuration :** toujours configurer le mode presentateur avant la presentation (ecran principal vs ecran secondaire). Tester avec le projecteur ou l'ecran reel.

### Presentation a distance (Zoom, Teams, Meet)

Bonnes pratiques pour le partage d'ecran :

- **Partager la fenetre du diaporama** (pas l'ecran entier, qui revele le bureau et les notifications)
- **Activer le mode "Do Not Disturb"** sur l'ordinateur pour bloquer les notifications
- **Utiliser une connexion filaire** (Ethernet) plutot que WiFi pour un partage fluide
- **Desactiver les animations complexes** qui saccadent en partage d'ecran
- **Garder la webcam activee** pour maintenir la connexion humaine
- **Utiliser le chat** pour les questions et le lien vers les slides
- **Enregistrer la session** pour les absents (obtenir le consentement prealable)

### Clickers et telecommandes

| Outil | Force | Prix indicatif |
|---|---|---|
| **Logitech Spotlight** | Pointeur laser digital, timer, zoom | ~120 EUR |
| **Logitech R500** | Simple, fiable, compact | ~35 EUR |
| **Kensington Expert** | Robuste, longue portee | ~50 EUR |
| **iPhone/Apple Watch** | Telecommande Keynote native | Gratuit (si Apple) |
| **Applications mobile** | Google Slides Remote, PowerPoint Mobile | Gratuit |

---

## Presentations Asynchrones — Recording et Video

### Outils d'enregistrement

| Outil | Integration | Force |
|---|---|---|
| **PowerPoint Recording** | Natif dans PowerPoint | Enregistrement voix + webcam + annotations, export MP4 |
| **Keynote Recording** | Natif dans Keynote | Enregistrement voix, export video haute qualite |
| **Loom** | Standalone + extensions navigateur | Enregistrement ecran + webcam, partage instantane, analytics de visionnage |
| **Vidyard** | Standalone + integrations CRM | Enregistrement + analytics + integration HubSpot/Salesforce |
| **mmhmm** | Standalone + integration visio | Presentateur incruste dans les slides, effet professionnel |

### Bonnes pratiques pour les presentations enregistrees

- **Duree** : maximum 15 minutes par video. Au-dela, decouper en chapitres ou episodes.
- **Chapitrage** : si l'outil le permet (Loom, YouTube), ajouter des chapitres avec des timestamps pour une navigation non-lineaire.
- **Webcam** : apparaitre en webcam au minimum dans l'introduction et la conclusion. En mode "tete parlante dans le coin" pendant les slides de contenu.
- **Script** : preparer un script ou des notes structurees. La presentation asynchrone ne pardonne pas les hesitations et les digressions.
- **Edition** : couper les silences, les erreurs et les passages non pertinents. Ajouter des titres et des transitions si necessaire.
- **Partage** : envoyer un lien vers la video (pas la video en piece jointe). Utiliser Loom, Vidyard ou YouTube non-liste.

### Analytics de presentation

Les outils modernes (Pitch, Loom, Vidyard, DocSend) offrent des analytics de visionnage :

| Metrique | Signification | Action |
|---|---|---|
| **Taux d'ouverture** | % des destinataires qui ont ouvert le deck/video | Si < 50%, revoir le sujet de l'email ou le timing |
| **Temps passe par slide** | Duree moyenne de visionnage par slide | Identifier les slides qui retiennent l'attention et celles qui sont skippees |
| **Drop-off rate** | % de l'audience qui quitte avant la fin | Si le drop-off est eleve apres la slide 5, l'ouverture n'accroche pas |
| **Nombre de re-visionnages** | Combien de fois le deck est re-ouvert | Indicateur d'interet et de partage interne |
| **Forwarding** | Le deck est-il repartage a d'autres personnes | Le deck circule — signe d'interet organisationnel |

Ces analytics sont particulierement precieux pour les sales decks : ils indiquent quel prospect est engage et quelle section l'interesse le plus, permettant un suivi commercial contextualise.

---

## Workflow Complet — Du Brief au Delivery

### Synthese du workflow en 5 phases

```
Phase 1: Brief (1-2h)          Phase 2: Narrative (2-4h)
┌─────────────────┐            ┌─────────────────┐
│ Audience        │            │ Framework       │
│ Objectif        │───────────>│ Action titles   │
│ Message central │            │ Flow validation │
│ Contraintes     │            │                 │
└─────────────────┘            └────────┬────────┘
                                        │
Phase 5: Delivery              Phase 4: Design (3-6h)
┌─────────────────┐            ┌─────────────────┐
│ Rehearsal x3    │            │ Design system   │
│ Test technique  │<───────────│ Slide master    │
│ Backup slides   │            │ Visual design   │
│ Feedback        │            │ Coherence check │
└─────────────────┘            └────────┬────────┘
                                        │
                               Phase 3: Content (2-4h)
                               ┌─────────────────┐
                               │ Donnees/preuves │
                               │ Type de slides  │
                               │ Data viz        │
                               │ Redaction       │
                               └─────────────────┘
```

### Estimation de temps par type de deck

| Type de deck | Nombre de slides | Temps de creation estime |
|---|---|---|
| **Pitch deck investisseurs** | 12-15 | 15-25h (recherche + iterations) |
| **Presentation board / COMEX** | 15-25 | 10-20h |
| **Sales deck** | 10-20 | 8-15h |
| **Presentation de resultats** | 15-30 | 6-12h (si donnees preparees) |
| **Presentation interne** | 10-20 | 4-8h |
| **Lightning talk** | 8-12 | 3-6h |
| **Draft IA + edition** | 15-20 | 2-5h (avec Gamma/Copilot) |

Ces estimations incluent le brief, la structure narrative, la creation, la revue et la repetition. Les presentations critiques (pitch deck, board) necessitent generalement 2-3 cycles de revue supplementaires.
