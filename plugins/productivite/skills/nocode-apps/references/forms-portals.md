# Formulaires & Portails — Tally, Typeform, JotForm, Portails Clients & Workflows

## Overview

Ce document de reference couvre les form builders modernes et les portails no-code, de la conception de formulaires avances a la mise en place de portails clients et fournisseurs self-service. Il fournit les bases pratiques, les patterns d'integration et les approches de conformite necessaires pour transformer la collecte de donnees et l'interaction avec les parties prenantes externes. Utiliser ce guide pour choisir le form builder adapte, concevoir des formulaires a haute conversion, integrer les soumissions dans des workflows automatises et deployer des portails professionnels.

---

## Form Builders Modernes — Vue d'Ensemble

### Evolution du marche

Le marche des form builders a evolue significativement entre 2020 et 2026. Les formulaires ne sont plus de simples collecteurs de donnees : ils sont devenus des points d'entree dans des workflows complets, des experiences interactives a haute conversion et des interfaces de saisie intelligentes avec logique conditionnelle, calculs et integrations temps reel.

Les tendances structurantes :
- **Conversational forms** : formulaires presentes question par question (Typeform, Tally) plutot qu'en un seul bloc.
- **AI-powered forms** : generation automatique de formulaires a partir d'une description, reponses suggerees par IA, analyse automatique des soumissions.
- **Form-as-app** : les formulaires deviennent des micro-applications avec logique, calculs, paiements et integrations.
- **Accessibility-first** : conformite WCAG 2.1 AA comme standard, navigation clavier complete, lecteurs d'ecran supportes.
- **Privacy-by-design** : conformite GDPR native, consentement granulaire, hebergement EU, anonymisation.

### Comparaison des Form Builders

| Critere | Tally | Typeform | JotForm | Google Forms | Microsoft Forms |
|---|---|---|---|---|---|
| **Positionnement** | Forms minimaliste et genereux | Forms conversationnels premium | Forms tout-en-un | Forms basique gratuit | Forms Microsoft 365 |
| **Modele de pricing** | Genereux free tier, Pro $29/mois | $29-99/mois | Free + plans payes | Gratuit | Inclus Microsoft 365 |
| **UX/Design** | Epure, rapide, elegant | Best-in-class conversationnel | Fonctionnel, riche | Basique, fonctionnel | Basique, integre |
| **Logique conditionnelle** | Oui (avancee) | Oui (avancee) | Oui (avancee) | Basique | Basique |
| **Calculs** | Oui (formules) | Oui (calculator) | Oui (widgets calcul) | Non | Non |
| **Paiements** | Stripe natif | Stripe natif | PayPal, Square, Stripe | Non | Non |
| **File uploads** | Oui (genereux) | Oui (limite) | Oui (genereux) | Oui (Google Drive) | Oui (OneDrive) |
| **Integrations** | Webhooks, Zapier, Make, Notion, Airtable | Webhooks, Zapier, HubSpot, Slack | 100+ integrations natives | Google Sheets natif | Excel natif |
| **API** | Oui | Oui | Oui | Limitee | Limitee |
| **GDPR** | Oui (EU hosting) | Oui (EU option) | Oui (EU option) | Sous GCP terms | Sous Microsoft terms |
| **Branding** | Logo removable (Pro) | Logo removable (Pro) | Logo removable (paye) | Google branding | Microsoft branding |

---

## Tally — Analyse Approfondie

### Positionnement

Tally est un form builder minimaliste lance en 2020 qui a rapidement gagne en popularite grace a son free tier extremement genereux (formulaires illimites, soumissions illimitees, logique conditionnelle, file uploads — tout gratuit). Son interface epuree rappelle Notion : on tape directement dans le formulaire comme dans un document.

### Fonctionnalites cles

#### Blocs de contenu

Tally propose des blocs que l'on place dans le formulaire comme des elements de page :

| Bloc | Fonction | Usage |
|---|---|---|
| **Short text** | Reponse courte (une ligne) | Nom, email, titre |
| **Long text** | Reponse longue (multi-lignes) | Description, commentaires |
| **Number** | Valeur numerique | Quantite, montant, age |
| **Multiple choice** | Choix unique parmi options | Selection de categorie |
| **Checkboxes** | Choix multiples | Tags, preferences |
| **Dropdown** | Menu deroulant | Liste longue d'options |
| **Date** | Selecteur de date | Deadline, date de naissance |
| **Rating** | Notation etoiles (1-5, 1-10) | Satisfaction, evaluation |
| **Linear scale** | Echelle numerique | NPS, Likert |
| **File upload** | Upload de fichier | CV, justificatif, photo |
| **Signature** | Signature manuscrite | Contrats, validations |
| **Payment** | Paiement Stripe | Inscription payante, don |
| **Hidden fields** | Champs invisibles pre-remplis | Tracking, UTM, source |
| **Calculated fields** | Champs calcules (formules) | Devis, scores, totaux |

#### Logique conditionnelle

Tally supporte la logique conditionnelle avancee :

- **Conditional blocks** : afficher ou masquer un bloc selon la reponse a une question precedente.
- **Conditional pages** : diriger vers differentes pages du formulaire selon les reponses.
- **Multiple conditions** : combiner plusieurs conditions avec AND/OR.
- **Value-based conditions** : conditions basees sur des valeurs numeriques (>, <, =, between).

Exemple de logique conditionnelle :
```
Question 1: Type de demande ? [Support / Commercial / Partenariat]
  Si "Support" → Page 2A: Formulaire de support (produit, urgence, description)
  Si "Commercial" → Page 2B: Formulaire commercial (entreprise, budget, timeline)
  Si "Partenariat" → Page 2C: Formulaire partenariat (domaine, proposition)
Toutes les reponses → Page 3: Informations de contact
```

#### Calculs et formules

Tally permet de creer des champs calcules qui affichent un resultat base sur les reponses :

```
// Devis automatique
Quantite (nombre) x Prix unitaire (nombre) = Total (calculated field)

// Score de qualification
IF(Taille entreprise > 50 AND Budget > 10000, "Qualifie", "A evaluer")

// Estimation de delai
IF(Complexite = "Simple", "5 jours",
  IF(Complexite = "Moyenne", "15 jours", "30 jours"))
```

### Integrations Tally

| Integration | Type | Configuration |
|---|---|---|
| **Webhooks** | HTTP POST a chaque soumission | URL + payload JSON automatique |
| **Notion** | Creation de page dans une database | Mapping des champs vers les proprietes |
| **Airtable** | Creation de record dans une table | Mapping des champs vers les colonnes |
| **Google Sheets** | Ajout de ligne dans un Sheet | Mapping automatique des colonnes |
| **Slack** | Message dans un canal | Template de message personnalisable |
| **Zapier / Make** | Connexion a 5 000+ apps | Trigger sur soumission |
| **Email notification** | Email a chaque soumission | Template personnalisable, destinataires multiples |

---

## Typeform — Analyse Approfondie

### Positionnement

Typeform est le pionnier du formulaire conversationnel (une question a la fois). Son approche UX premium genere des taux de completion significativement superieurs aux formulaires traditionnels (jusqu'a 2-3x selon Typeform). Son design est reconnaissable et professionnel.

### Fonctionnalites differenciantes

#### Logic jumps et branching

Typeform excelle dans la logique de branchement complexe :

- **Logic jumps** : naviguer vers differentes questions selon les reponses (if/then/else).
- **Calculator** : variable numerique incrementee ou modifiee par les reponses. Permet de calculer des scores, des devis et des evaluations.
- **Hidden fields** : pre-remplir des champs via l'URL (UTM, source, ID utilisateur).
- **Recall information** : inserer dynamiquement les reponses precedentes dans les questions suivantes ("Merci {prenom}, parlons maintenant de...").
- **Endings** : differentes pages de fin selon le score ou les reponses (redirection conditionnelle).

#### Variables et Calculator

Le systeme de variables de Typeform permet de construire des logiques de scoring et de calcul :

```
Variable: score_qualification (nombre, initial = 0)

Question 1: Taille de l'entreprise ?
  < 10 employes → score_qualification + 1
  10-50 employes → score_qualification + 3
  50-200 employes → score_qualification + 5
  > 200 employes → score_qualification + 8

Question 2: Budget annuel ?
  < 5K → score_qualification + 1
  5K-20K → score_qualification + 3
  20K-100K → score_qualification + 5
  > 100K → score_qualification + 8

Ending:
  Si score_qualification >= 10 → "Prospect qualifie" (redirect vers calendly)
  Si score_qualification 5-9 → "Prospect a nurture" (redirect vers newsletter)
  Si score_qualification < 5 → "Non qualifie" (redirect vers ressources gratuites)
```

#### Typeform pour les enquetes

Typeform est particulierement adapte aux enquetes et aux recherches utilisateur :

- **NPS (Net Promoter Score)** : question de notation 0-10, suivie d'une question ouverte conditionnelle (si score < 7 : "Que pourrions-nous ameliorer ?", si score >= 9 : "Qu'est-ce que vous appreciez le plus ?").
- **CSAT (Customer Satisfaction Score)** : echelle de satisfaction 1-5 ou 1-7 avec suivi conditionnel.
- **CES (Customer Effort Score)** : mesure de l'effort percu par le client pour resoudre un probleme.
- **Research interviews** : formulaire de screening avec logique conditionnelle pour qualifier les participants et planifier les entretiens (integration Calendly).

### Integrations Typeform

| Integration | Type | Points forts |
|---|---|---|
| **HubSpot** | CRM natif | Creation/mise a jour de contacts et deals directement |
| **Salesforce** | CRM natif | Mapping avance des champs vers les objets Salesforce |
| **Zapier** | iPaaS | 5 000+ applications, trigger sur soumission |
| **Make** | iPaaS | Scenarios complexes avec conditions et boucles |
| **Slack** | Notification | Message formate dans un canal a chaque soumission |
| **Google Sheets** | Data export | Ajout de ligne automatique avec mapping de colonnes |
| **Mailchimp** | Email marketing | Ajout a une liste avec tags selon les reponses |
| **Webhooks** | HTTP POST | Payload JSON complet, headers customisables |

---

## JotForm — Analyse Approfondie

### Positionnement

JotForm est le form builder le plus riche en fonctionnalites, avec plus de 10 000 templates et 100+ integrations natives. Son approche tout-en-un couvre les formulaires, les signatures electroniques, les PDF, les paiements et les approbations.

### Fonctionnalites differenciantes

- **JotForm Tables** : base de donnees visuelle integree pour stocker et gerer les soumissions (similaire a Airtable Lite).
- **JotForm Approvals** : workflow d'approbation multi-niveaux directement dans JotForm.
- **JotForm Sign** : signature electronique juridiquement valable.
- **JotForm PDF Editor** : generation automatique de PDF a partir des soumissions (contrats, devis, factures).
- **JotForm Apps** : creation d'applications mobiles a partir de formulaires (sans code).
- **Widgets** : 400+ widgets (calculs, e-commerce, conditions avancees, scheduling, maps).
- **Prefill** : pre-remplissage avance via URL, via integration ou via record existant.

### Cas d'usage specifiques JotForm

- **Formulaires de commande** : catalogue produits, panier, calcul du total, paiement integre.
- **Demandes d'approbation** : demande → manager → RH → validation, avec notifications a chaque etape.
- **Contrats et signatures** : formulaire de collecte d'informations → generation PDF → signature electronique.
- **Inscription avec paiement** : formulaire d'inscription → calcul du prix → paiement Stripe/PayPal → confirmation.
- **Formulaires medicaux** : conformite HIPAA (plan Healthcare), signatures patient, upload de documents.

---

## Google Forms et Microsoft Forms

### Google Forms

**Forces** : gratuit, integration native Google Sheets, collaboration en temps reel, quizzes et tests, add-ons pour etendre les fonctionnalites.

**Limites** : design basique et non personnalisable, logique conditionnelle limitee (section-based uniquement), pas de calculs, pas de paiements, branding Google non removable, pas d'API de soumission directe.

**Quand utiliser** : enquetes internes rapides, quizzes et evaluations, collecte de donnees basique dans un environnement Google, formulaires temporaires ne necessitant pas de branding.

### Microsoft Forms

**Forces** : inclus dans Microsoft 365 (pas de cout supplementaire), integration native Excel et Power Automate, quizzes et evaluations avec notation automatique, branching basique.

**Limites** : design tres basique, fonctionnalites limitees comparees aux form builders specialises, pas de calculs ni de paiements, branding Microsoft non removable.

**Quand utiliser** : organisations Microsoft 365, enquetes internes, quizzes de formation, collecte de donnees alimentant des workflows Power Automate.

---

## Fonctionnalites Avancees des Formulaires

### Logique conditionnelle — Patterns

#### Pattern 1 — Formulaire de qualification (Lead Scoring)

```
Page 1: Identification
  - Nom, Email, Entreprise

Page 2: Qualification
  - Taille de l'entreprise (< 10 / 10-50 / 50-200 / > 200)
  - Budget annuel pour le projet (< 5K / 5K-20K / 20K-100K / > 100K)
  - Timeline (< 1 mois / 1-3 mois / 3-6 mois / > 6 mois)
  - Decision maker ? (Oui / Non / Influenceur)

Page 3: Routing conditionnel
  SI score >= 10 → "Planifier un appel" (embed Calendly)
  SI score 5-9 → "Telecharger notre guide" (lien PDF)
  SI score < 5 → "Decouvrir nos ressources" (lien blog)
```

#### Pattern 2 — Formulaire multi-etapes avec sauvegarde

```
Etape 1: Informations generales (sauvegardees apres soumission partielle)
Etape 2: Details du projet (affichage conditionnel selon type)
Etape 3: Documents (upload avec validation de format et taille)
Etape 4: Recapitulatif (affichage en lecture seule des reponses)
Etape 5: Validation (checkbox de consentement + soumission)

Barre de progression: 1/5 → 2/5 → 3/5 → 4/5 → 5/5
Sauvegarde automatique a chaque etape (Typeform / JotForm)
```

#### Pattern 3 — Devis automatique

```
Question 1: Type de service ? [A / B / C]
  A → prix_base = 500
  B → prix_base = 1000
  C → prix_base = 2000

Question 2: Quantite ? [1-100]
  quantite = reponse

Question 3: Options supplementaires ? [Option X (+200€) / Option Y (+500€)]
  options = somme des options selectionnees

Champ calcule: Total = prix_base × quantite + options
Affichage: "Votre devis estimatif : {Total} EUR HT"
```

### Paiements dans les formulaires

Les form builders modernes integrent les paiements directement :

| Plateforme | Processeur | Fonctionnalites |
|---|---|---|
| **Tally** | Stripe | Paiement unique, montant fixe ou calcule |
| **Typeform** | Stripe | Paiement unique, montant fixe ou variable |
| **JotForm** | Stripe, PayPal, Square | Paiement, abonnement, panier multi-produits |

**Pattern de paiement dans un formulaire** :
1. Collecte des informations (contact, choix de produit/service).
2. Calcul du montant (formule basee sur les reponses).
3. Affichage du recapitulatif avec le montant total.
4. Champ de paiement Stripe (numero de carte, expiration, CVC).
5. Confirmation de paiement et generation du recu.
6. Declenchement du workflow post-paiement (email de confirmation, creation de record, notification).

### File Uploads — Bonnes Pratiques

- **Limiter les formats acceptes** : specifier les extensions autorisees (PDF, JPG, PNG, DOCX) pour eviter les fichiers malveillants.
- **Limiter la taille** : definir une taille maximale par fichier (ex. 10 MB) et un nombre maximum de fichiers.
- **Nommer les fichiers** : utiliser un nommage automatique base sur les reponses (ex. `{nom}_{date}_{document_type}.pdf`).
- **Stocker dans un service dedie** : configurer le stockage dans Google Drive, Dropbox ou S3 plutot que dans le form builder directement.
- **Scanner les fichiers** : pour les formulaires publics, envisager un scan antivirus automatique via une automation.

---

## Form-to-Workflow Patterns

### Pattern 1 — Formulaire → Airtable → Notification

```
[Tally Form] --webhook--> [Make]
                             |
                    [Create record in Airtable]
                             |
                    [Send Slack notification]
                             |
                    [Send confirmation email to submitter]
```

**Implementation** :
1. Configurer le webhook Tally vers Make.
2. Dans Make, parser les donnees JSON recues.
3. Creer un record dans la table Airtable correspondante.
4. Poster un message dans le canal Slack de l'equipe avec les details.
5. Envoyer un email de confirmation au soumetteur avec un resume.

### Pattern 2 — Formulaire → Approbation → Action

```
[JotForm Form] --submit--> [JotForm Approvals]
                                |
                    [Manager recoit notification email]
                                |
                    +-- Approuve → [Create record + notify submitter]
                    +-- Refuse → [Notify submitter with reason]
                    +-- Demande modification → [Reopen form for submitter]
```

**Cas d'usage** : demandes de conge, demandes d'achat, demandes d'acces, soumissions de contenu.

### Pattern 3 — Formulaire → CRM → Sequence email

```
[Typeform] --integration--> [HubSpot CRM]
                                |
                    [Create/update Contact]
                    [Set properties based on responses]
                    [Assign to sales rep based on score]
                                |
                    +-- Score >= 8 → Enroll in "Hot Lead" sequence
                    +-- Score 4-7 → Enroll in "Nurturing" sequence
                    +-- Score < 4 → Add to newsletter list
```

### Pattern 4 — Formulaire → Generation de document

```
[Tally Form] --webhook--> [Make]
                             |
                    [Map data to Google Docs template]
                    [Generate PDF from template]
                    [Store PDF in Google Drive]
                    [Send PDF to submitter by email]
                    [Create record in Airtable with PDF link]
```

**Cas d'usage** : generation de devis, de contrats, de certificats, de rapports.

---

## Portails Clients et Fournisseurs

### Types de portails

| Type | Description | Plateforme recommandee |
|---|---|---|
| **Portail client** | Espace securise pour les clients : suivi de commandes, documents, support | Softr, Bubble |
| **Portail fournisseur** | Espace pour les fournisseurs : soumission de catalogues, suivi de commandes | Softr, AppSheet |
| **Portail self-service** | Base de connaissances, FAQ, soumission de tickets, suivi | Softr, Notion (public) |
| **Portail employe** | Intranet : annuaire, ressources, demandes, actualites | Softr, Notion, AppSheet |
| **Portail partenaire** | Espace pour les partenaires : resources, leads, co-marketing | Softr, Bubble |

### Architecture d'un portail client avec Softr + Airtable

```
[Client] --> [Softr Portal]
                |
                +-- Page d'accueil (dashboard avec KPIs)
                +-- Mes projets (list block filtre par client connecte)
                +-- Detail projet (detail block avec taches, documents, timeline)
                +-- Soumettre une demande (form block → cree record dans Airtable)
                +-- Mes documents (list block filtre → attachments Airtable)
                +-- Mon profil (detail block du record utilisateur)
                |
            [Airtable Backend]
                |
                +-- Table Clients (email, nom, entreprise, role)
                +-- Table Projets (linked to Clients)
                +-- Table Taches (linked to Projets)
                +-- Table Documents (linked to Projets, attachments)
                +-- Table Demandes (linked to Clients, status workflow)
```

### Securite des portails

#### Authentification

| Methode | Description | Niveau de securite | Plateformes |
|---|---|---|---|
| **Email + Password** | Login classique | Standard | Softr, Bubble |
| **Magic Link** | Lien de connexion envoye par email | Standard+ (pas de mot de passe a memoriser) | Softr, Bubble |
| **Google SSO** | Connexion via compte Google | Eleve (si Google Workspace) | Softr, Bubble, AppSheet |
| **SSO SAML/OIDC** | Single Sign-On entreprise | Eleve | Softr Enterprise, Bubble, Retool |
| **MFA** | Authentification multi-facteurs | Tres eleve | Bubble (via plugin), Retool |

#### Controle d'acces dans les portails

1. **Page-level** : certaines pages sont reservees a certains roles (ex. page "Administration" visible uniquement par les admins).
2. **Data-level** : les donnees affichees sont filtrees selon l'utilisateur connecte (ex. un client ne voit que SES projets).
3. **Field-level** : certains champs sont masques pour certains roles (ex. la marge n'est pas visible par le client).
4. **Action-level** : certaines actions sont reservees a certains roles (ex. seul l'admin peut supprimer un record).

### Portail avec Airtable Interface Designer

Airtable Interface Designer peut servir de portail interne leger :

**Avantages** :
- Pas de plateforme supplementaire — tout est dans Airtable.
- Temps de construction minimal — quelques heures.
- Securite geree par les permissions Airtable.

**Limites** :
- Acces limite aux utilisateurs Airtable (necessite une licence par utilisateur pour les portails externes).
- Design contraint par les elements d'interface disponibles.
- Pas de custom domain ni de branding avance.

**Quand utiliser** : portails internes pour les equipes qui utilisent deja Airtable, dashboards operationnels, vues de saisie guidee pour les utilisateurs non-techniques.

---

## Embedding et Integration de Formulaires

### Methodes d'embedding

| Methode | Description | Avantages | Limites |
|---|---|---|---|
| **iFrame** | Integrer le formulaire dans une page via `<iframe>` | Simple, isole du site parent | Hauteur fixe, scroll potentiel, CORS |
| **Script embed** | Script JS fourni par le form builder | Adaptatif, meilleure integration visuelle | Dependance au CDN du form builder |
| **Popup/Modal** | Formulaire affiche dans une fenetre modale | Non-intrusif, bon pour les CTA | Bloqueurs de popup, UX mobile |
| **Slider** | Formulaire qui glisse depuis le cote de la page | Discret, bon pour le feedback | Peut etre ignore par les utilisateurs |
| **Full-page** | Page dediee hebergee par le form builder | Meilleure UX, pas de conflit CSS | L'utilisateur quitte le site |
| **API** | Construire un formulaire custom et soumettre via API | Controle total du design | Necessite du developpement |

### Pre-remplissage via URL

La plupart des form builders supportent le pre-remplissage des champs via des parametres d'URL :

```
// Tally
https://tally.so/r/abc123?nom=Jean+Dupont&email=jean@example.com&source=newsletter

// Typeform
https://form.typeform.com/to/abc123#nom=Jean+Dupont&email=jean@example.com

// Google Forms
https://docs.google.com/forms/d/abc123/viewform?usp=pp_url&entry.123456=Jean+Dupont
```

**Cas d'usage** :
- Pre-remplir le nom et l'email depuis un lien dans une campagne email.
- Passer des parametres UTM pour le tracking marketing.
- Pre-remplir un formulaire de modification avec les valeurs existantes du record.

---

## Form Analytics et Optimisation

### Metriques cles

| Metrique | Definition | Benchmark |
|---|---|---|
| **Taux de vue** | Nombre de personnes qui voient le formulaire / total visiteurs | Depend du placement |
| **Taux de debut** | Nombre de personnes qui commencent le formulaire / nombre de vues | > 50% |
| **Taux de completion** | Soumissions / debuts | > 60% (standard), > 80% (excellent) |
| **Taux d'abandon** | 1 - taux de completion | < 40% |
| **Point d'abandon** | Question ou etape ou les utilisateurs abandonnent le plus | Identifier et simplifier |
| **Temps de completion** | Temps moyen entre le debut et la soumission | < 5 min pour les formulaires standards |
| **Taux de soumissions qualifiees** | Soumissions exploitables / total soumissions | > 80% |

### Strategies d'optimisation

1. **Reduire le nombre de champs** : chaque champ supplementaire reduit le taux de completion de 3-5%. Ne demander que les informations strictement necessaires.
2. **Utiliser la logique conditionnelle** : masquer les champs non pertinents selon les reponses precedentes. L'utilisateur ne voit que ce qui le concerne.
3. **Decouper en etapes** : un formulaire de 20 champs en 4 etapes de 5 champs a un meilleur taux de completion qu'un formulaire de 20 champs sur une seule page.
4. **Barre de progression** : afficher la progression ("Etape 2/4") pour motiver les utilisateurs a continuer.
5. **Valeurs par defaut intelligentes** : pre-remplir les champs avec les valeurs les plus courantes ou les informations connues.
6. **Validation en temps reel** : valider les champs au fur et a mesure de la saisie, pas uniquement a la soumission.
7. **Texte d'aide contextuel** : ajouter des descriptions sous les champs pour guider la saisie sans surcharger l'interface.
8. **Call-to-action clair** : le bouton de soumission doit decrire l'action ("Envoyer ma demande") plutot qu'un generique ("Soumettre").
9. **Mobile-first** : tester le formulaire sur mobile en priorite — la majorite des soumissions viennent de smartphones.
10. **A/B testing** : tester differentes versions du formulaire (ordre des questions, formulation, nombre d'etapes) pour optimiser le taux de completion.

---

## Accessibilite des Formulaires

### Standards WCAG 2.1 AA

Les formulaires doivent respecter les criteres d'accessibilite WCAG 2.1 niveau AA :

- **Labels explicites** : chaque champ doit avoir un label visible et associe via l'attribut `for/id` ou `aria-label`.
- **Navigation clavier** : le formulaire doit etre entierement navigable au clavier (Tab, Enter, Espace, fleches).
- **Messages d'erreur clairs** : les erreurs doivent identifier le champ en erreur et decrire clairement le probleme.
- **Contraste suffisant** : ratio de contraste minimum de 4.5:1 pour le texte, 3:1 pour les elements interactifs.
- **Focus visible** : l'indicateur de focus doit etre clairement visible sur chaque element interactif.
- **Structure semantique** : utiliser les balises HTML semantiques (form, fieldset, legend, label, input).
- **Texte alternatif** : les images decoratives dans le formulaire doivent avoir un attribut alt vide, les images informatives un alt descriptif.

### Conformite par plateforme

| Plateforme | Conformite WCAG | Navigation clavier | Screen reader | Notes |
|---|---|---|---|---|
| **Tally** | AA (bonne) | Oui | Oui | Structure semantique propre |
| **Typeform** | Partielle | Oui | Partielle | Le format conversationnel peut etre desorientant pour les lecteurs d'ecran |
| **JotForm** | AA (bonne) | Oui | Oui | Mode accessible explicite disponible |
| **Google Forms** | AA (bonne) | Oui | Oui | Google investit dans l'accessibilite |
| **Microsoft Forms** | AA (bonne) | Oui | Oui | Microsoft investit dans l'accessibilite |

---

## Conformite GDPR pour les Formulaires

### Exigences legales

Tout formulaire collectant des donnees personnelles de residents de l'UE doit respecter le RGPD :

1. **Base legale** : identifier la base legale du traitement (consentement, interet legitime, execution de contrat).
2. **Consentement explicite** : si la base legale est le consentement, il doit etre libre, specifique, eclaire et univoque. Pas de case pre-cochee.
3. **Information prealable** : informer l'utilisateur sur l'identite du responsable de traitement, la finalite, la duree de conservation, les droits (acces, rectification, suppression, portabilite).
4. **Minimisation des donnees** : ne collecter que les donnees strictement necessaires a la finalite declaree.
5. **Duree de conservation** : definir et appliquer une duree de conservation pour les donnees collectees.
6. **Droit de suppression** : permettre aux personnes de demander la suppression de leurs donnees.
7. **Sous-traitants** : s'assurer que le form builder et les outils d'integration sont conformes GDPR (DPA signe, hebergement EU possible).

### Checklist GDPR pour les formulaires

- [ ] Lien vers la politique de confidentialite visible dans le formulaire.
- [ ] Case de consentement non pre-cochee pour chaque finalite distincte (newsletter, marketing, partage avec tiers).
- [ ] Texte d'information clair et comprehensible avant la soumission.
- [ ] Confirmation double (double opt-in) pour les inscriptions newsletter.
- [ ] Duree de conservation definie dans le registre des traitements.
- [ ] Processus de suppression des donnees sur demande documente.
- [ ] DPA (Data Processing Agreement) signe avec le form builder.
- [ ] Hebergement des donnees en UE si possible (Tally : EU natif, Typeform : option EU, JotForm : option EU).
- [ ] Registre des traitements mis a jour avec le formulaire.
- [ ] Evaluation d'impact (PIA) si les donnees sont sensibles (sante, opinions politiques, donnees biometriques).

---

## Checklist de Conception d'un Formulaire

1. **Definir l'objectif** : quel est le but exact du formulaire ? Quelle action doit suivre la soumission ?
2. **Identifier les champs necessaires** : lister tous les champs, puis eliminer ceux qui ne sont pas strictement necessaires.
3. **Structurer en etapes logiques** : regrouper les champs par theme et creer des etapes si > 8 champs.
4. **Configurer la logique conditionnelle** : masquer les champs non pertinents, router vers les bonnes etapes.
5. **Ajouter les validations** : champs obligatoires, formats (email, telephone), valeurs min/max.
6. **Configurer les integrations** : ou vont les donnees ? (Airtable, CRM, email, Slack).
7. **Personnaliser le design** : branding (logo, couleurs), textes d'aide, messages d'erreur.
8. **Configurer la page de confirmation** : message de remerciement, email de confirmation, redirection.
9. **Tester** : soumettre le formulaire soi-meme, tester sur mobile, tester la logique conditionnelle.
10. **Verifier la conformite GDPR** : consentement, information, politique de confidentialite.
11. **Deployer et monitorer** : taux de completion, points d'abandon, qualite des soumissions.
12. **Iterer** : optimiser en continu selon les metriques et le feedback des utilisateurs.
