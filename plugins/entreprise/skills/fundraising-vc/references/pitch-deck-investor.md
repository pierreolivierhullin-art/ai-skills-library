# Pitch Deck Investisseur — Structure et Narratif

## Vue d'Ensemble

Un pitch deck n'est pas une presentation PowerPoint améliorée — c'est un instrument de vente conçu pour convaincre des professionnels de l'allocation de capital de parient sur vous. Les VCs voient 1 000-3 000 decks par an. Ils investissent dans 1-3% des entreprises qu'ils rencontrent. Votre deck doit declencer un "je veux en savoir plus" en moins de 3 minutes.

---

## Les Règles du Deck

### Format

**Longueur** : 12-15 slides maximum pour le deck d'introduction. Le deck "leave behind" (apres le meeting) peut aller jusqu'a 20 slides.

**Format** : PDF (pas PowerPoint — eviter les problemes de police, les animations inutiles). Partager un lien DocSend (tracking des ouvertures, temps par slide).

**Design** : propre et professionnel mais pas sur-designé. Les VCs mefiants des decks trop polis ("trop de temps passe sur le deck = pas assez sur le produit"). Blanc/couleurs marque, police lisible, pas de stock photos generiques.

### Les 3 Questions Auxquelles le Deck Doit Repondre

1. **Pourquoi ce probleme est enorme et urgent ?** (Market + Problem)
2. **Pourquoi cette equipe peut le resoudre uniquement ?** (Team + Traction)
3. **Pourquoi maintenant, pourquoi ce modele ?** (Why Now + Business Model)

---

## Slide par Slide — Detail

### Slide 1 — Cover

**Contenu** :
- Logo (haute resolution)
- Tagline (1 phrase, pas plus)
- Email du fondateur principal
- Mois/Annee de la levee

**Ce a eviter** : "Pitch Deck" comme titre. "Confidentiel" (ca ne sert a rien et ca fait amateur). Sous-titre trop vague ("Revolutionner le marche de X").

**Bon exemple** :
```
[Logo] Fygaro
"Le logiciel de gestion de tournées pour les artisans du bâtiment"
pierre@fygaro.com | Seed 2025
```

### Slide 2 — Problem

**Objectif** : rendre le probleme visceral et urgent. Le VC doit penser "oui, c'est un probleme reel que des gens ont vraiment."

**Structure** :
- 1 persona concret + 1 situation specifique
- La douleur en chiffres (si possible)
- Les solutions actuelles inadequates

**Bon exemple** :
"Sophie, architecte freelance (25% des architectes français) passe 6h/semaine a etablir ses devis manuellement avec Excel. Elle facture 120 EUR/h → elle perd 37 000 EUR de revenus par an en taches administratives. Les logiciels existants (AutoCAD, Revit) ne couvrent pas la facturation. Excel reste le standard."

**Ce a eviter** : commencer par la solution ("Notre produit resout le probleme de..."). Probleme trop vague ("Les entreprises perdent du temps"). Statistiques non-sourcees.

### Slide 3 — Solution

**Objectif** : montrer la solution de facon simple et visuelle. PAS une liste de features.

**Structure** :
- 1-2 screenshots du produit (le vrai produit, pas des mockups)
- La proposition de valeur en 1 phrase
- 2-3 points cles maximum

**Ce a eviter** : slide dense de texte. Jargon technique. Comparaison immediate avec les concurrents (ca vient plus tard).

### Slide 4 — Why Now

**Objectif** : expliquer pourquoi ce probleme est resolvable en 2025 et pas en 2020.

**Triggers possibles** :
- Changement reglementaire (RGPD, EU AI Act, MaPrimeRenov...)
- Baisse du cout d'une technologie (GPU, APIs LLM, SMS)
- Changement de comportement (post-COVID, gen Z dans les entreprises)
- Infrastructure existante maintenant (Stripe, Twilio, AWS → montee en charge triviale)

**Ce a eviter** : la slide "Why Now" souvent oubliée. Si vous l'oubliez, le VC la pose en question : "Pourquoi pas quelqu'un d'autre avant vous ?"

### Slide 5 — Market Size

**3 chiffres a presenter** :

**TAM (Total Addressable Market)** : si vous etiez le seul acteur et capturiez 100% du marche, quelle serait votre taille maximale ? Chiffre large et aspirationnel.

**SAM (Serviceable Addressable Market)** : la partie du TAM que vous pouvez reellement adresser avec votre model et geographie.

**SOM (Serviceable Obtainable Market)** : la part du SAM que vous pouvez realistement capturer dans les 3-5 prochaines annees.

**Approche Bottom-Up (crédible)** :
```
TAM : 200M artisans du batiment en Europe × 500 EUR/an = 100 Mrd EUR
SAM : France + Benelux (5M artisans eligibles) × 500 EUR/an = 2.5 Mrd EUR
SOM (3 ans) : 2% de penetration = 50M EUR ARR
```

**Ce a eviter** : "Nous ciblons le marche de la construction (600 Mrd EUR en Europe). Si nous capturons 1%..." → personne ne croit cela. Toujours utiliser l'approche bottom-up.

### Slide 6 — Traction

**La slide la plus importante pour un Seed+**. Montre que le marche valide votre hypothese.

**Metriques selon le stage** :

**Pre-seed** : entretiens (20+), LOI (lettres d'intention), beta users, waitlist.

**Seed** : MRR (et son graphique de croissance), nombre de clients payants, retention, un logo client reconnu.

**Serie A** : MRR > 100K EUR, croissance > 5-10% MoM, NRR > 100%, 1-2 anecdotes clients concretes.

**Format recommande** :
- Graphique MRR sur 12 mois (la courbe parle d'elle-meme)
- 3 logos clients (si B2B)
- 1 quote client fort

**Ce a eviter** : presenter des vanity metrics (nombre d'inscrits, users sans engagement). Cacher le churn. Confondre ARR (annuel) et MRR (mensuel) sans notation.

### Slide 7 — Business Model

**Objectif** : montrer que vous comprenez comment vous gagnez de l'argent et que c'est scalable.

**A inclure** :
- Modele de monetisation (SaaS, transaction, marketplace...)
- Pricing (les tiers ou le prix moyen)
- ACV (Annual Contract Value) moyen et cible
- Quelques metriques cles : CAC, LTV, Gross Margin

**Benchmark SaaS B2B** :
- Gross margin > 70% → excellent
- LTV/CAC > 3:1 → viable
- CAC Payback < 18 mois → scalable

### Slide 8 — Go-to-Market

**Objectif** : prouver que vous savez comment acquérir des clients a grande echelle.

**Structure** :
- ICP (Ideal Customer Profile) precis
- Canal principal d'acquisition (et pourquoi il scale)
- Metriques d'acquisition actuelles (CAC, conversion funnel)
- Prochaines etapes d'expansion

**Ce a eviter** : "Nous allons faire du content marketing, du SEO, des evenements, du partenariat..." → tout faire = rien faire. 1 canal principal, prouver qu'il fonctionne.

### Slide 9 — Competitive Landscape

**Ne jamais dire "nous n'avons pas de concurrents"**. Tous les VCs savent que c'est faux.

**Formats efficaces** :

**Matrice 2x2** : 2 axes qui representent vos differenciateurs cles. Vous dans le quadrant superieur droit.

**Tableau de comparaison** : features cles en lignes, vous et vos concurrents en colonnes. Cases cochees/non-cochees.

**Ce a inclure dans le texte** :
- "Nos differenciateurs durables sont X et Y" (pas juste des features — pourquoi ils sont difficiles a copier)

### Slide 10 — Team

**Pourquoi c'est critique** : les VCs investissent dans les equipes autant que dans les produits. En early stage, l'equipe peut pivoter sur le produit, pas l'inverse.

**Structure** :
- Photo + Nom + Titre court
- 1-2 credentials les plus pertinents pour CE projet
- "Founder-Market Fit" : pourquoi vous etes les mieux places pour resoudre ce probleme ?

**Ce a valoriser** :
- Experience directe du probleme (vous etiez votre propre client)
- Previous exits ou scale (vous avez construit quelque chose de grand avant)
- Expertise technique differentiatrice (brevet, publication, contribution open-source)
- Reseau client (acces direct aux decision-makers du marche cible)

### Slide 11 — Financials

**Pour un Seed** : projections 3 ans avec hypotheses claires. Ne pas mentir — les VCs feront leur propre modele.

**A inclure** :
- MRR actuel + projection fin d'annee
- Headcount actuel et prevu
- Burn rate mensuel et Runway actuel
- Path to profitability ou next milestone (quand levez-vous la Serie A ?)

### Slide 12 — The Ask

**Contenu** :
- Montant recherche : "Nous levons 1.5M EUR"
- Valorisation pre-money cible (ou "Nous sommes ouverts a la discussion")
- Use of funds : repartition en 3 postes max (produit 40%, commercial 35%, operations 25%)
- Milestones atteignables avec ce tour : "Dans 18 mois, nous atteindrons X ARR et Y clients, ce qui nous positionnera pour une Serie A"

---

## Gestion du Processus de Pitch

### Avant le Meeting

Rechercher le VC : portfolio, these d'investissement, posts LinkedIn recents. Personnaliser les 2-3 premieres minutes du pitch en fonction.

Preparer : 3 variantes de pitch (15 min / 30 min / 60 min). Les VCs n'ont souvent que 20 minutes.

### Pendant le Meeting

Commencer par l'executive summary (3 minutes) avant d'entrer dans le detail : marche, solution, traction, ask. Puis laisser le VC guider avec ses questions.

Ne pas lire les slides. Les slides sont le support — pas le script.

Repondre "je ne sais pas" est acceptable. Mentir ou exagerer = fin de la relation.

### Apres le Meeting

Email de suivi dans les 24h : recap des points cles, reponses aux questions posees, prochaines etapes.

DocSend : tracker quelles slides sont relues et pendant combien de temps → signal d'interet.

Si refus : demander un feedback specifique. "Qu'est-ce qui vous a empeche de passer a l'etape suivante ?" Informations precieuses pour le prochain pitch.
