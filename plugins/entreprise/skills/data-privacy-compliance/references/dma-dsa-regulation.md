# DMA, DSA & Nouveaux Reglements Numeriques Europeens

## Vue d'Ensemble

L'Union europeenne a deploye depuis 2022 un ensemble de reglements numeriques qui redefinissent les regles du jeu pour les grandes plateformes et les services en ligne. Le **DMA** (Digital Markets Act) cible les gatekeepers des marches numeriques ; le **DSA** (Digital Services Act) encadre les contenus et la responsabilite des intermediaires. Ces reglements creent des opportunites (acces aux donnees des gatekeepers, nouvelles API) ET des obligations nouvelles pour les entreprises concernees.

---

## DMA — Digital Markets Act (Reglement 2022/1925)

### Objectif et Logique

Le DMA vise a prevenir les pratiques anticoncurrentielles des grandes plateformes designees comme "gatekeepers" (controleurs d'acces). La logique : certaines plateformes sont devenues des infrastructures essentielles du marche numerique. Leurs comportements abusifs (self-preferencing, tying, denying access to data) ne peuvent plus etre corriges uniquement par le droit de la concurrence traditionnel, trop lent.

**Originalite du DMA** : il impose des obligations ex ante (avant qu'un abus ne soit prouve), pas uniquement des sanctions ex post. C'est une rupture majeure avec le droit de la concurrence classique.

### Criteres de Designation comme Gatekeeper

Un gatekeeper est une entreprise qui :
- Realise un CA >= 7.5 Mds EUR dans l'EEE OU a une capitalisation >= 75 Mds EUR
- Propose un "service de plateforme essentiel" (moteur de recherche, reseaux sociaux, marketplace, OS, browser, service publicitaire, assistant numerique)
- A un impact sur le marche interieur europeen
- Occupe une position durable et solidement implantee

**Gatekeepers designes (2024)** : Alphabet (Google), Apple, Amazon, Meta, Microsoft, ByteDance (TikTok). Samsung en discussion.

### Obligations des Gatekeepers (Articles 5-7)

**Obligations "per se" (Article 5)** — sans possibilite de justification :
- Ne pas combiner les donnees personnelles provenant de differents services sans consentement explicite (ex: combiner WhatsApp + Instagram + Facebook pour cibler une pub)
- Ne pas utiliser les donnees non-publiques des entreprises utilisant la plateforme pour les concurrencer
- Permettre aux utilisateurs finaux de desinstaller les apps pre-installees
- Permettre aux entreprises d'acceder aux donnees generees sur la plateforme
- Permettre aux vendeurs d'offrir de meilleures conditions en dehors de la plateforme (no MFN clause)
- Permettre aux developpeurs d'acceder aux app stores alternatifs (sideloading — iOS)

**Obligations "sujettes a specification" (Article 6)** — avec possibilite de dialogue:
- Interoperabilite des services de messagerie (WhatsApp, iMessage)
- Transparence sur le classement des resultats de recherche
- Acces aux donnees de search pour les moteurs de recherche concurrents
- Pas d'avantage injustifie aux propres services dans les classements (self-preferencing)

**Cas concret — Impact sur les entreprises europeennes** :

Un e-commerce europeen qui vend sur Amazon Marketplace peut desormais :
- Acceder aux donnees agregees sur les performances de ses produits (pas seulement les siennes)
- Proposer des prix inferieurs sur son site sans risque de deferencement
- Contacter directement les clients ayant achete ses produits (sous conditions)

### Sanctions DMA

- Jusqu'a **10% du CA mondial** pour une premiere violation
- Jusqu'a **20% du CA mondial** pour les violations repetees
- Jusqu'a **5% du CA mondial par jour** pour non-respect des mesures provisoires
- Dissolution structurelle (separation d'activites) en cas de violations "systematiques" (3 violations en 8 ans)

### Opportunites pour les Entreprises Non-Gatekeepers

**Acces aux donnees** :
Le DMA oblige les gatekeepers a partager certaines donnees avec les entreprises partenaires. Pour un annonceur, cela signifie acces aux donnees de performance publicitaire plus detaillees. Pour un retailer sur marketplace, acces aux donnees clients de facon plus granulaire.

**Interoperabilite messaging** :
Si WhatsApp doit etre interoperable avec d'autres messageries, les entreprises peuvent potentiellement atteindre leurs clients WhatsApp depuis d'autres plateformes. A surveiller : la mise en oeuvre technique est complexe.

**Sideloading iOS** :
Les app stores alternatifs sont desormais autorises sur iOS en UE. Opportunite de distribuer des applications sans les 15-30% de commission Apple. Risque : securite et experience utilisateur a maintenir.

---

## DSA — Digital Services Act (Reglement 2022/2065)

### Structure Reglementaire par Taille

Le DSA cree une pyramide d'obligations proportionnelles a la taille et a l'impact de la plateforme :

```
Tres Grandes Plateformes (VLOP)              > 45M utilisateurs actifs UE
et Tres Grands Moteurs (VLOSE)                ↓ Obligations maximales
        |
Grandes Plateformes                           1000-45M utilisateurs UE
d'hebergement                                 ↓ Obligations etendues
        |
Plateformes d'hebergement standard            < 1000 utilisateurs UE
        |
Services d'intermediation (caching, conduit)  ↓ Obligations minimales
        |
Micro-entreprises et PME                      EXEMPTEES de la plupart
```

### Obligations Communes (toutes les plateformes)

**Point de contact unique** : Nom et coordonnees d'un point de contact pour les autorites et les utilisateurs (different du DPO RGPD — peut etre la meme personne mais mission distincte).

**Rapport de transparence** : Publication annuelle du nombre de signalements recus, des decisions de moderation, des injonctions recues des autorites.

**Conditions d'utilisation claires** : Information intelligible sur les restrictions de contenu et les consequences.

**Systeme de signalement** : Permettre aux utilisateurs de signaler des contenus potentiellement illegaux de maniere simple.

### Obligations des Plateformes d'Hebergement

**Mecanisme de "notice and action"** : Traiter les signalements de contenus illegaux promptement. Notifier l'utilisateur de la decision prise. Permettre une contestation.

**Trusted Flaggers** : Organisations designees dont les signalements sont traites en priorite (associations de lutte contre la haine en ligne, autorites, ONG).

**Transparence publicitaire** : Identifier clairement les publicites, indiquer l'annonceur, permettre de voir pourquoi on est cible.

**Interdiction de publicite ciblee** : Pas de ciblage base sur les donnees sensibles (religion, sante, orientation sexuelle). Pas de ciblage des mineurs.

### Obligations Specifiques aux VLOP/VLOSE

**Evaluation des risques systemiques** (annuelle) :
- Risques de diffusion de contenus illegaux
- Risques pour les droits fondamentaux
- Risques pour le discours civique et les processus electoraux
- Risques pour la sante publique et la securite
- Risques pour la violence envers les femmes et les mineurs

**Audit independant** (annuel) : Par un organisme certifie selon les criteres de la Commission. Cout estime pour les grandes plateformes : 1-5M EUR/an.

**Acces aux donnees pour la recherche** : Obligation de fournir aux chercheurs academiques accredites l'acces aux donnees pour etudier les risques systemiques. Revolution pour la recherche sur les reseaux sociaux.

**Rapport de transparence detaille** : Tous les 6 mois, incluant les metriques de moderation par categorie, par pays, par type de contenu.

**Mecanisme de recommandation alternatif** : Offrir aux utilisateurs au moins une option de recommandation de contenu non basee sur le profilage comportemental.

### Sanctions DSA

- Jusqu'a **6% du CA mondial annuel** pour les violations
- Jusqu'a **1% du CA annuel** pour les informations incorrectes ou incompletes fournies a la Commission

---

## CCPA & Reglements Non-Europeens

### CCPA / CPRA (Californie)

**Similitudes avec le RGPD** :
- Droit d'acces, de suppression, de correction, de portabilite
- Droit de ne pas etre discrimine pour l'exercice de ses droits
- Information sur la collecte et l'utilisation des donnees

**Differences cles** :
- S'applique aux entreprises repondant a des seuils (CA > 25M USD OU > 100k consommateurs traites) — les petites entreprises sont exemptees
- Concept de "vente" de donnees (opt-out requis) — notion plus large qu'en RGPD
- Pas d'obligation de base legale comme le RGPD — mais transparence requise
- "Sensitive personal information" : categorie etendue (race, religion, sante, communications privees, localisation precise, orientation sexuelle)
- "Right to limit" : limiter l'utilisation des donnees sensibles

**Pour une entreprise francaise ayant des clients californiens** :
Si les seuils sont atteints, implementation d'un lien "Do Not Sell or Share My Personal Information" visible sur le site, et d'une politique de confidentialite conforme CCPA en plus du RGPD.

### Convergence Mondiale

Un mouvement global vers des lois de protection des donnees similaires au RGPD :
- **Bresil** : LGPD (2020) — tres proche du RGPD
- **Chine** : PIPL (2021) — principes similaires, mais obligations de localisation strictes
- **Inde** : DPDPA (2023) — en cours d'implementation
- **Canada** : Loi 25 (Quebec, 2023), reforme PIPEDA en cours
- **Japon** : APPI amende (2022)

Pour les entreprises internationales : le RGPD comme standard de base est generalement une approche efficace car il est souvent plus strict que les reglements nationaux.

---

## Checklist de Conformite Reglementaire

### RGPD + DMA + DSA — Audit Rapide

**RGPD (toutes organisations)**
- [ ] Registre de traitement a jour
- [ ] Politique de confidentialite mise a jour et accessible
- [ ] CMP cookies conforme (bouton refuser au meme niveau qu'accepter)
- [ ] DPO designe (si obligatoire) ou point de contact RGPD
- [ ] Procedure demandes droits operationnelle (< 30 jours)
- [ ] Procedure violation de donnees (72h CNIL)
- [ ] DPA signes avec tous les sous-traitants
- [ ] Formation RGPD des equipes traitant des donnees personnelles

**DMA (si acheteur/vendeur sur plateformes gatekeeper)**
- [ ] Verifier les nouvelles obligations des gatekeepers applicables
- [ ] Explorer les nouvelles API d'acces aux donnees
- [ ] Securiser les conditions contractuelles avec les plateformes (MFN clauses)

**DSA (si plateforme d'hebergement)**
- [ ] Point de contact designe et publie
- [ ] Mecanisme de signalement en place
- [ ] Rapport de transparence publie
- [ ] Publicites identifiees clairement (sans ciblage sur donnees sensibles)
- [ ] Si VLOP/VLOSE : evaluation des risques, audit programme
