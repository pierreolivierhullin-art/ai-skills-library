# Templates & Automatisation Documentaire — Conception, Gouvernance & Production en Serie

## Overview

Ce document de reference couvre la conception, le deploiement, la gouvernance et l'exploitation des templates documentaires, ainsi que les techniques et outils d'automatisation de la production documentaire. Il traite des principes de design de templates, de la gouvernance a l'echelle de l'organisation, de la conformite de marque, des workflows de publipostage avances, des outils de generation documentaire (Documill, PandaDoc, document assembly), du contenu conditionnel, des documents pilotes par les donnees et de la production en serie. Utiliser ce guide pour industrialiser la production documentaire et garantir la qualite, la coherence et l'efficacite a l'echelle de l'organisation.

---

## Principes de Conception de Templates

### Qu'est-ce qu'un template professionnel

Un template (modele de document) est un fichier pre-configure qui sert de base a la creation de nouveaux documents. Contrairement a un document ordinaire, un template contient :

- **Les styles** : palette de styles pre-definis conformes a la charte graphique (titres, corps de texte, listes, citations, legendes, tableaux).
- **La mise en page** : marges, en-tetes, pieds de page, sauts de section, orientation.
- **Les blocs de construction** : Quick Parts, AutoText, blocs de contenu reutilisables.
- **Les metadonnees** : proprietes pre-renseignees (categorie, classification, template version).
- **Les instructions** : texte d'aide, zones de remplissage, controles de contenu (Content Controls).
- **Les protections** : sections protegees, controles de contenu verrouilles, restrictions d'edition.

### Les 7 regles d'or du template design

#### Regle 1 — Un template par type de document
Chaque type de document recurrent (rapport trimestriel, proposition commerciale, compte-rendu de reunion, note interne, contrat, attestation) doit disposer de son propre template. Eviter les templates "fourre-tout" qui tentent de couvrir plusieurs types de documents avec des sections optionnelles complexes.

#### Regle 2 — Styles exhaustifs et auto-suffisants
Le template doit contenir tous les styles necessaires a la creation du document, sans que l'utilisateur ait besoin de creer de nouveaux styles ou d'utiliser du formatage direct. Chaque element du document (titre principal, sous-titre, corps de texte, liste a puces, liste numerotee, citation, legende, en-tete de tableau, cellule de tableau, note de bas de page) doit avoir un style dedie.

#### Regle 3 — Instructions de remplissage claires
Le template doit guider l'utilisateur avec des instructions claires. Utiliser :
- **Texte d'aide** : texte en gris ou en italique indiquant ce qu'il faut saisir dans chaque section ("[Inserer le titre du rapport ici]", "[Decrire les objectifs du projet]").
- **Controles de contenu** : zones de saisie structurees (texte enrichi, texte brut, liste deroulante, date, image) qui guident la saisie et peuvent etre rendues obligatoires.
- **Commentaires de template** : commentaires expliquant les conventions et les regles a suivre pour chaque section.

#### Regle 4 — Page de garde integree
Pour les documents formels (rapports, propositions, etudes), integrer une page de garde pre-formatee avec les zones de saisie pour le titre, le sous-titre, l'auteur, la date, la version, le logo et les mentions obligatoires. La page de garde utilise un saut de section pour avoir ses propres en-tetes/pieds de page (sans numerotation de page, sans en-tete).

#### Regle 5 — En-tetes et pieds de page configures
Les en-tetes et pieds de page doivent etre pre-configures avec :
- Le logo de l'organisation (en resolution appropriee, ancre correctement).
- Les champs dynamiques (numero de page, nombre total de pages, date, nom de fichier).
- Les mentions obligatoires (classification, confidentialite, version).
- La gestion des sections (premiere page differente, pages paires/impaires si impression recto-verso).

#### Regle 6 — Metadonnees et proprietes pre-configurees
Le template doit pre-renseigner les proprietes du document :
- Proprietes standard : categorie, societe, responsable.
- Proprietes personnalisees : type de document, version du template, classification.
- Proprietes utilisees par les champs DOCPROPERTY dans le document (affichage automatique de la version, du client, du projet).

#### Regle 7 — Documentation du template
Chaque template doit etre accompagne d'une documentation decrivant :
- Son usage prevu (quel type de document, quel contexte).
- Les styles disponibles et quand les utiliser.
- Les conventions de remplissage (que mettre dans chaque section).
- Le processus de mise a jour et le contact du mainteneur.
- Les restrictions et protections en place.

---

## Controles de Contenu (Content Controls)

### Types de controles de contenu

Les controles de contenu de Word sont des zones de saisie structurees qui guident l'utilisateur et peuvent etre liees a des proprietes du document ou des donnees XML :

| Type | Description | Usage typique |
|---|---|---|
| **Texte enrichi** | Zone de saisie avec formatage | Corps de texte, descriptions longues |
| **Texte brut** | Zone de saisie sans formatage | Noms, references, codes |
| **Liste deroulante** | Selection dans une liste pre-definie | Classification, departement, statut |
| **Zone de liste modifiable** | Liste deroulante avec saisie libre | Categories avec option "Autre" |
| **Selecteur de date** | Calendrier pour selection de date | Dates de debut, fin, echeance |
| **Case a cocher** | Case a cocher binaire | Oui/Non, options multiples |
| **Image** | Zone d'insertion d'image | Logo, photo, signature |
| **Bloc de construction** | Selection d'un Building Block | Clauses contractuelles, blocs predifinis |
| **Groupe** | Conteneur qui regroupe d'autres controles | Sections protegees avec zones editables |

### Configuration avancee des controles

Chaque controle de contenu peut etre configure avec les proprietes suivantes :
- **Titre et balise** : identification unique du controle (utilisee pour le mapping XML et les macros).
- **Style** : style applique automatiquement au contenu saisi dans le controle.
- **Texte d'aide** : texte affiche quand le controle est vide (guide l'utilisateur).
- **Suppression impossible** : le controle ne peut pas etre supprime par l'utilisateur.
- **Modification impossible** : le contenu du controle ne peut pas etre modifie (lecture seule).
- **Mappage XML** : le controle est lie a un element d'une partie XML personnalisee du document.

### Mapping XML et integration de donnees

Les controles de contenu peuvent etre lies a des parties XML personnalisees (Custom XML Parts) du document, ce qui permet :
- De pre-remplir les controles a partir de donnees XML externes (importees par un add-in ou un script).
- De mettre a jour automatiquement le contenu des controles lorsque les donnees XML changent.
- D'extraire les donnees saisies dans les controles sous forme XML structuree pour alimentation d'un systeme d'information.

Cette approche est la base du **document assembly** avance : un programme genere les donnees XML, les insere dans le template Word, et les controles de contenu affichent automatiquement les donnees correspondantes.

---

## Gouvernance des Templates a l'Echelle de l'Organisation

### Le catalogue de templates

Maintenir un catalogue centralise de tous les templates de l'organisation :

| Champ | Description | Exemple |
|---|---|---|
| **ID** | Identifiant unique du template | TPL-RPT-001 |
| **Nom** | Nom descriptif | Rapport d'activite trimestriel |
| **Categorie** | Type de document | Rapports |
| **Departement** | Departement proprietaire | Direction Generale |
| **Version** | Version du template | 3.2 |
| **Date de creation** | Date de creation initiale | 2024-01-15 |
| **Derniere mise a jour** | Date de derniere modification | 2026-01-10 |
| **Mainteneur** | Responsable du template | Direction Communication |
| **Emplacement** | Chemin d'acces | SharePoint/Templates/Rapports/ |
| **Statut** | Actif, En revision, Deprecie | Actif |
| **Documentation** | Lien vers le guide d'utilisation | [Lien] |

### Processus de gouvernance

#### Creation d'un nouveau template
1. **Demande formelle** : le demandeur soumet une demande de creation de template au gestionnaire documentaire (formulaire standardise : type de document, volume estimatif, public cible, elements de charte a integrer).
2. **Analyse de besoin** : le gestionnaire verifie qu'aucun template existant ne couvre le besoin. Si un template similaire existe, evaluer s'il peut etre adapte.
3. **Conception** : le designer de template (souvent la Direction Communication ou un prestataire specialise) cree le template en respectant la charte graphique, les standards documentaires et les regles d'accessibilite.
4. **Revue et validation** : le template est revise par les parties prenantes (Communication, Juridique, IT, representants metiers). Chaque partie prenante valide les aspects relevant de son perimetre.
5. **Test** : le template est teste par des utilisateurs representatifs sur des cas reels. Les retours sont integres.
6. **Deploiement** : le template est publie dans le catalogue, deploye via le mecanisme centralise et communique aux utilisateurs.

#### Modification d'un template existant
1. **Demande de modification** : le demandeur ou le mainteneur identifie un besoin de modification (evolution de la charte, nouveau besoin metier, correction de bug).
2. **Impact assessment** : evaluer l'impact de la modification sur les documents existants bases sur ce template.
3. **Modification et test** : appliquer la modification, tester sur des documents existants et nouveaux.
4. **Increment de version** : incrementer le numero de version (mineure pour les ajustements, majeure pour les changements structurels).
5. **Communication** : informer les utilisateurs de la mise a jour et des eventuels impacts.

#### Deprecation d'un template
1. **Decision de deprecation** : un template est deprecie quand il n'est plus conforme aux standards, qu'il est remplace par un nouveau template, ou que le type de document n'est plus produit.
2. **Periode de transition** : maintenir le template deprecie en lecture seule pendant 6 mois avec un avertissement redirigeant vers le nouveau template.
3. **Archivage** : archiver le template deprecie dans un repertoire dedie (non accessible aux utilisateurs courants).

### Deploiement des templates

#### Dans Microsoft 365 / SharePoint
- **Bibliotheque de templates SharePoint** : creer une bibliotheque de documents dediee aux templates sur SharePoint. Configurer les templates comme "Modeles" dans les types de contenu de la bibliotheque.
- **Organisation Assets Library** : configurer la bibliotheque SharePoint comme "Organisation Assets Library" pour que les templates apparaissent directement dans Word (Fichier > Nouveau > Modeles d'organisation).
- **Group Policy** : deployer les templates dans le dossier de modeles personnalises de Word via Group Policy (`HKCU\Software\Microsoft\Office\16.0\Word\Options\PersonalTemplates`).

#### Dans Google Workspace
- **Templates Google Docs** : creer les templates dans Google Docs et les soumettre a l'approbation de l'administrateur Workspace.
- **Google Workspace Admin** : l'administrateur peut approuver les templates pour qu'ils apparaissent dans la galerie de templates accessible a tous les utilisateurs du domaine.
- **Shared Drives** : stocker les templates dans un Shared Drive dedie avec des permissions en lecture seule pour les utilisateurs.

---

## Conformite de Marque (Brand Compliance)

### Elements de charte graphique dans les templates

| Element | Specifications typiques | Implementation dans le template |
|---|---|---|
| **Logo** | Format (SVG/PNG), zone d'exclusion, taille minimale | Image ancree dans l'en-tete, taille fixe |
| **Couleurs** | Palette primaire et secondaire (codes Hex/RGB/CMYK) | Jeu de couleurs personnalise (Theme Colors) |
| **Typographie** | Police primaire et secondaire, tailles, graisses | Jeu de polices personnalise (Theme Fonts) |
| **Espacements** | Interlignes, espacements avant/apres titres | Proprietes de paragraphe dans les styles |
| **Marges** | Marges de page, marges d'en-tete/pied | Configuration de mise en page |
| **Iconographie** | Style d'icones, pictogrammes autorises | Building Blocks ou bibliotheque d'images |

### Themes Word et coherence visuelle

Les themes Word permettent de definir un ensemble coherent de couleurs, de polices et d'effets que l'on peut appliquer a n'importe quel document :

- **Couleurs du theme** : 12 couleurs (4 texte/arriere-plan + 6 accent + 2 lien hypertexte) qui se declinent en 10 nuances chacune. Toutes les couleurs utilisees dans les styles, les graphiques et les SmartArt doivent provenir du theme pour garantir la coherence.
- **Polices du theme** : une police pour les titres (Headings) et une pour le corps (Body). Tous les styles doivent utiliser les polices du theme (et non des polices codees en dur).
- **Effets du theme** : styles d'ombres, reflexions, contours appliques aux formes et aux images.

Creer un theme personnalise (onglet Creation > Themes > Enregistrer le theme actif) et le deployer avec les templates pour garantir que tous les documents de l'organisation utilisent la meme palette visuelle.

---

## Publipostage Avance et Production en Serie

### Architecture d'un workflow de publipostage

```
1. SOURCE DE DONNEES
   ├── Fichier Excel / CSV (donnees statiques)
   ├── Base de donnees Access / SQL (donnees dynamiques)
   ├── Liste SharePoint (donnees collaboratives)
   ├── CRM (Salesforce, HubSpot — via export ou connecteur)
   └── API REST (donnees temps reel via middleware)

2. TEMPLATE DE PUBLIPOSTAGE
   ├── Document principal avec MERGEFIELD
   ├── Regles conditionnelles (IF, SKIPIF, NEXTIF)
   ├── Blocs de construction conditionnels
   └── Mise en forme des champs (format date, nombre, texte)

3. MOTEUR DE FUSION
   ├── Word natif (interface graphique)
   ├── VBA / COM Automation (programmation)
   ├── Power Automate (workflow cloud)
   └── Outil tiers (Documill, PandaDoc, etc.)

4. SORTIE
   ├── Documents Word individuels
   ├── PDF individuels
   ├── Emails personnalises (via Outlook)
   ├── Enveloppes / etiquettes
   └── Archivage automatise (SharePoint, DMS)
```

### Formatage avance des champs de fusion

Les champs MERGEFIELD acceptent des commutateurs de format pour controler l'affichage des donnees fusionnees :

| Commutateur | Syntaxe | Exemple | Resultat |
|---|---|---|---|
| **Format date** | `\@ "dd MMMM yyyy"` | `{ MERGEFIELD DateContrat \@ "dd MMMM yyyy" }` | 15 fevrier 2026 |
| **Format nombre** | `\# "#.##0,00"` | `{ MERGEFIELD Montant \# "#.##0,00 €" }` | 12.500,00 EUR |
| **Majuscules** | `\* Upper` | `{ MERGEFIELD Nom \* Upper }` | DUPONT |
| **Minuscules** | `\* Lower` | `{ MERGEFIELD Email \* Lower }` | jean@acme.com |
| **Premiere lettre** | `\* FirstCap` | `{ MERGEFIELD Ville \* FirstCap }` | Paris |
| **Chaque mot** | `\* Caps` | `{ MERGEFIELD NomComplet \* Caps }` | Jean Pierre Dupont |

### Production de PDF individuels par VBA

Pour generer un PDF individuel par enregistrement fusionne (cas d'usage frequent : attestations, certificats, factures) :

```vba
Sub MailMergeToPDF()
    Dim i As Long
    Dim outputPath As String
    outputPath = "C:\Documents\Output\"

    With ActiveDocument.MailMerge
        .Destination = wdSendToNewDocument
        For i = 1 To .DataSource.RecordCount
            .DataSource.FirstRecord = i
            .DataSource.LastRecord = i
            .Execute Pause:=False

            ' Generer le nom de fichier a partir des donnees
            Dim fileName As String
            fileName = outputPath & "Document_" & Format(i, "000") & ".pdf"

            ' Exporter en PDF
            ActiveDocument.ExportAsFixedFormat _
                OutputFileName:=fileName, _
                ExportFormat:=wdExportFormatPDF, _
                OptimizeFor:=wdExportOptimizeForPrint

            ActiveDocument.Close SaveChanges:=False
        Next i
    End With
    MsgBox "Generation terminee : " & i - 1 & " PDF crees.", vbInformation
End Sub
```

---

## Outils de Generation Documentaire

### Panorama des solutions

| Outil | Type | Points forts | Limites | Prix indicatif |
|---|---|---|---|---|
| **Word natif (Mail Merge)** | Integre | Gratuit, familier, flexible | Limite aux capacites Word | Inclus dans Microsoft 365 |
| **Power Automate** | Workflow cloud | Integration Microsoft 365, no-code | Templates Word uniquement | A partir de 12.50 EUR/mois/utilisateur |
| **Documill** | SaaS | Templates avances, logique complexe | Cout, courbe d'apprentissage | Sur devis |
| **PandaDoc** | SaaS | Propositions commerciales, e-signature integree | Oriente vente, cout par utilisateur | A partir de 19 USD/mois/utilisateur |
| **Templafy** | Enterprise | Gouvernance de templates, brand compliance | Cout enterprise | Sur devis |
| **DocuSign Gen** | SaaS | Generation + signature integree | Ecosysteme DocuSign requis | Sur devis |
| **Windward Studios** | Enterprise | Logique conditionnelle tres avancee | Complexite, cout | Sur devis |
| **Pandoc** | Open source | Multi-format, ligne de commande | Technique, pas d'interface graphique | Gratuit |
| **Python + python-docx** | Dev | Flexibilite maximale, programmation | Necessite des competences dev | Gratuit |

### Power Automate pour la generation documentaire

Power Automate (anciennement Microsoft Flow) permet de creer des workflows automatises de generation documentaire dans l'ecosysteme Microsoft 365 :

#### Workflow type : generer un contrat depuis un formulaire

```
1. Declencheur : soumission d'un formulaire Microsoft Forms
   └── Donnees : nom du client, type de contrat, montant, date

2. Action : Remplir un template Word (connecteur Word Online)
   ├── Template stocke sur SharePoint
   ├── Mapping des champs du formulaire vers les Content Controls du template
   └── Generation du document Word rempli

3. Action : Convertir en PDF (connecteur Word Online)
   └── Conversion du document genere en PDF

4. Action : Envoyer pour signature (connecteur DocuSign ou Adobe Sign)
   ├── Destinataire(s) de signature
   ├── Zones de signature positionnees
   └── Message personnalise

5. Action : Archiver (connecteur SharePoint)
   ├── Enregistrement du PDF signe dans la bibliotheque d'archivage
   ├── Mise a jour des metadonnees (statut, date de signature)
   └── Notification au demandeur
```

### PandaDoc — Propositions commerciales automatisees

PandaDoc est specialise dans la generation de propositions commerciales, devis et contrats avec signature electronique integree :

- **Templates visuels** : editeur de templates drag-and-drop avec blocs de contenu (texte, images, tableaux de prix, signatures).
- **Tableaux de prix dynamiques** : catalogues de produits/services avec calcul automatique (quantites, remises, taxes, totaux).
- **Contenu conditionnel** : sections qui s'affichent ou se masquent en fonction de variables (type de client, montant, region).
- **Integration CRM** : connexion native avec Salesforce, HubSpot, Pipedrive pour pre-remplir les documents a partir des donnees CRM.
- **Workflow d'approbation** : circuit de validation interne avant envoi au client.
- **Signature electronique** : signature legalement contraignante integree directement dans le document.
- **Analytics** : suivi de l'ouverture, du temps de lecture, des sections consultees.

### Documill — Generation documentaire avancee

Documill est une plateforme de generation documentaire enterprise qui va au-dela du publipostage simple :

- **Logique conditionnelle avancee** : sections, paragraphes, phrases et mots qui s'affichent ou se masquent selon des conditions complexes (combinaisons AND/OR, comparaisons numeriques, correspondances de texte).
- **Boucles et repetitions** : generer des blocs de contenu pour chaque element d'une liste (lignes d'un tableau, clauses d'un contrat, items d'une facture).
- **Calculs** : operations arithmetiques dans le document (sommes, moyennes, pourcentages, TVA).
- **Multi-format** : generation simultanee en Word, PDF, HTML, email a partir du meme template.
- **Integration Salesforce** : connecteur natif pour generer des documents directement depuis Salesforce a partir des donnees de l'objet.

---

## Contenu Conditionnel et Document Assembly

### Principes du document assembly

Le document assembly est la technique de generation de documents complexes dont le contenu varie en fonction de donnees, de regles metier et de choix utilisateur. Contrairement au publipostage (qui remplace des champs par des valeurs), le document assembly construit le document en assemblant des blocs de contenu selon une logique conditionnelle.

### Niveaux de contenu conditionnel

| Niveau | Description | Exemple | Implementation |
|---|---|---|---|
| **Mot/Expression** | Un mot ou une expression change selon une condition | "Monsieur" / "Madame" | Champ IF simple |
| **Phrase** | Une phrase entiere s'affiche ou non | Mention RGPD si client EU | Champ IF avec texte |
| **Paragraphe** | Un paragraphe entier conditionnel | Clause de non-concurrence si cadre | Champ IF ou Building Block conditionnel |
| **Section** | Une section complete (titre + contenu) | Chapitre fiscal selon pays | Document assembly avance |
| **Document** | Le template entier change | Contrat francais vs. contrat anglais | Selection de template |

### Techniques de contenu conditionnel dans Word

#### Methode 1 — Champs IF imbriques
Pour les conditions simples (2-3 niveaux), utiliser les champs IF de Word :
```
{ IF { DOCPROPERTY "TypeClient" } = "Particulier"
    "Conformement aux dispositions du Code de la consommation..."
    "Conformement aux conditions generales de vente B2B..."
}
```

#### Methode 2 — Building Blocks conditionnels avec macros
Pour les blocs de contenu plus complexes, combiner les Building Blocks avec des macros VBA qui inserent le bon bloc selon les conditions :
```vba
Sub InsertConditionalClause()
    Dim clientType As String
    clientType = ActiveDocument.CustomDocumentProperties("TypeClient").Value

    Select Case clientType
        Case "Particulier"
            Selection.Range.InsertAutoText "Clause_Consommateur"
        Case "PME"
            Selection.Range.InsertAutoText "Clause_PME"
        Case "GrandeEntreprise"
            Selection.Range.InsertAutoText "Clause_GrandCompte"
    End Select
End Sub
```

#### Methode 3 — Custom XML Parts et transformations
Pour les documents tres complexes avec de nombreuses conditions, utiliser les Custom XML Parts :
1. Definir un schema XML qui capture toutes les variables du document.
2. Creer le template avec des Content Controls mappes sur les elements XML.
3. Generer le fichier XML a partir de l'application metier.
4. Injecter le XML dans le template (via Open XML SDK ou un outil de document assembly).
5. Les Content Controls affichent automatiquement les valeurs correspondantes.

---

## Documents Pilotes par les Donnees (Data-Driven Documents)

### Architecture d'un systeme de documents data-driven

```
1. SOURCE DE DONNEES
   ├── Base de donnees (SQL Server, PostgreSQL, MySQL)
   ├── API REST (microservices, SaaS)
   ├── CRM (Salesforce, HubSpot, Dynamics)
   ├── ERP (SAP, Oracle, Odoo)
   └── Fichiers structures (JSON, XML, CSV)

2. COUCHE DE TRANSFORMATION
   ├── ETL / Integration (Power Automate, Zapier, Mulesoft)
   ├── Logique metier (regles de calcul, conditions, validations)
   └── Formatage (dates, nombres, devises, traductions)

3. MOTEUR DE GENERATION
   ├── Open XML SDK (.NET)
   ├── python-docx (Python)
   ├── Apache POI (Java)
   ├── Pandoc (multi-format, ligne de commande)
   ├── Carbone.io (Node.js)
   └── Solutions SaaS (Documill, Windward, DocuSign Gen)

4. TEMPLATE
   ├── Template Word avec Content Controls
   ├── Template Markdown avec variables Jinja2
   ├── Template LaTeX avec commandes personnalisees
   └── Template HTML avec moteur de templates

5. SORTIE
   ├── Documents individualises (1 document par enregistrement)
   ├── Document composite (1 document avec toutes les donnees)
   ├── Multi-format (Word + PDF + HTML + Email)
   └── Archivage avec metadonnees
```

### Python + python-docx : generation programmatique

La bibliotheque python-docx permet de creer et manipuler des documents Word par programmation :

```python
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json

def generate_report(data, template_path, output_path):
    """Genere un rapport personnalise a partir d'un template et de donnees."""
    doc = Document(template_path)

    # Remplacer les placeholders dans les paragraphes
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in paragraph.text:
                for run in paragraph.runs:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, str(value))

    # Remplacer dans les en-tetes et pieds de page
    for section in doc.sections:
        for paragraph in section.header.paragraphs:
            for key, value in data.items():
                placeholder = f"{{{{{key}}}}}"
                if placeholder in paragraph.text:
                    for run in paragraph.runs:
                        if placeholder in run.text:
                            run.text = run.text.replace(placeholder, str(value))

    # Generer un tableau dynamique
    if 'items' in data:
        table = doc.add_table(rows=1, cols=4, style='Table Grid')
        headers = ['Reference', 'Description', 'Quantite', 'Montant']
        for i, header in enumerate(headers):
            table.rows[0].cells[i].text = header

        for item in data['items']:
            row = table.add_row()
            row.cells[0].text = item['ref']
            row.cells[1].text = item['description']
            row.cells[2].text = str(item['qty'])
            row.cells[3].text = f"{item['amount']:.2f} EUR"

    doc.save(output_path)

# Utilisation
data = {
    "client": "Acme Corp",
    "date": "16 fevrier 2026",
    "reference": "PROP-2026-042",
    "items": [
        {"ref": "SRV-001", "description": "Conseil strategique", "qty": 5, "amount": 2500.00},
        {"ref": "SRV-002", "description": "Formation equipe", "qty": 2, "amount": 1800.00}
    ]
}
generate_report(data, "template_proposition.docx", "proposition_acme.docx")
```

### Pandoc : conversion et generation multi-format

Pandoc est l'outil de reference pour la conversion entre formats documentaires. Il permet de generer des documents Word, PDF, HTML, EPUB et LaTeX a partir de sources Markdown, avec des templates et des variables personnalisables :

```bash
# Generer un rapport Word a partir de Markdown avec un template
pandoc rapport.md \
  --from markdown \
  --to docx \
  --reference-doc=template_entreprise.docx \
  --metadata title="Rapport Q1 2026" \
  --metadata author="Direction Generale" \
  --metadata date="2026-02-16" \
  --output rapport_q1_2026.docx

# Generer un PDF via LaTeX avec des variables
pandoc rapport.md \
  --from markdown \
  --to pdf \
  --template=template_rapport.latex \
  --variable documentclass=report \
  --variable fontsize=11pt \
  --variable geometry=margin=2.5cm \
  --variable lang=fr \
  --output rapport_q1_2026.pdf

# Conversion batch : tous les fichiers Markdown d'un repertoire
for f in *.md; do
  pandoc "$f" --to docx --reference-doc=template.docx -o "${f%.md}.docx"
done
```

---

## Production en Serie — Industrialiser la Generation

### Workflow de production en serie

| Etape | Action | Outil | Verification |
|---|---|---|---|
| 1 | Preparer la source de donnees | Excel / Base de donnees | Completude, doublons, format |
| 2 | Valider le template | Word / Outil de generation | Champs corrects, styles conformes |
| 3 | Configurer le mapping | Outil de generation | Correspondance champs-donnees |
| 4 | Test sur echantillon | Outil de generation | 5-10 documents de test |
| 5 | Revue qualite | Humain | Verification visuelle et contenu |
| 6 | Lancement production | Outil de generation | Monitoring de la generation |
| 7 | Controle post-production | Automatise + humain | Verification aleatoire, comptage |
| 8 | Distribution | Email / SharePoint / DMS | Confirmation de reception |
| 9 | Archivage | DMS / SharePoint | Metadonnees, retention |

### Indicateurs de performance de la production documentaire

| Indicateur | Definition | Cible |
|---|---|---|
| **Temps de creation** | Temps moyen pour creer un document d'un type donne | Divise par 3 avec templates, par 10 avec automatisation |
| **Taux de conformite** | % de documents conformes a la charte et aux standards | > 95 % |
| **Taux d'erreur** | % de documents contenant des erreurs (contenu, formatage) | < 2 % |
| **Taux d'utilisation des templates** | % de documents crees a partir d'un template officiel | > 90 % |
| **Volume automatise** | % du volume documentaire genere automatiquement | > 50 % (niveau 4 de maturite) |
| **Cout par document** | Cout moyen de production d'un document (temps humain + outils) | En baisse continue |
| **Satisfaction utilisateur** | Score de satisfaction des utilisateurs sur les templates et outils | > 80 % |

### Gestion des erreurs en production en serie

En production de masse, les erreurs se multiplient par le volume. Mettre en place des controles systematiques :

- **Validation des donnees en amont** : verifier la completude, le format et la coherence des donnees avant de lancer la generation. Rejeter les enregistrements invalides.
- **Test sur echantillon** : generer 5 a 10 documents de test couvrant les cas limites (donnees longues, caracteres speciaux, champs vides, conditions aux limites).
- **Controle post-generation** : verifier automatiquement les documents generes (nombre de pages, presence des sections attendues, taille du fichier, format de sortie).
- **Verification aleatoire** : revue humaine d'un echantillon statistiquement significatif (5-10 % du volume ou racine carree du nombre de documents, selon la methode).
- **Rollback** : en cas d'erreur systematique detectee, pouvoir regenerer l'ensemble du lot a partir des donnees corrigees sans impact sur les documents deja distribues.

---

## Templates Specifiques par Domaine

### Templates juridiques et contractuels

Les templates juridiques ont des exigences specifiques :
- **Numerotation des clauses** : numerotation hierarchique automatique (1. / 1.1 / 1.1.1) via les listes a niveaux multiples.
- **Definitions** : section de definitions avec renvois automatiques (chaque terme defini est reference par un signet et utilisable via des references croisees).
- **Clauses optionnelles** : mecanisme pour activer/desactiver des clauses selon le type de contrat (contenu conditionnel).
- **Paraphes et signatures** : zones de signature et de paraphe en pied de page, avec compteur de pages ("Page X sur Y").
- **Annexes** : systeme d'annexes avec numerotation independante et references croisees depuis le corps du contrat.

### Templates financiers et rapports

Les templates de rapports financiers necessitent :
- **Tableaux de donnees** : templates de tableaux pre-formates pour les etats financiers (bilan, compte de resultat, flux de tresorerie).
- **Graphiques dynamiques** : graphiques lies a des tableaux Excel integres, mis a jour automatiquement.
- **Mentions legales** : mentions obligatoires (auditeurs, perimetre de consolidation, avertissements).
- **Multilinguisme** : templates bilingues ou multilingues pour les organisations internationales.

### Templates techniques et scientifiques

Les templates techniques requierent :
- **Equations** : integration d'equations mathematiques via l'editeur d'equations de Word ou MathType.
- **Code** : zones de code avec police monospace et coloration syntaxique (via styles personnalises).
- **Figures et legendes** : numerotation automatique des figures, tableaux et equations avec references croisees.
- **Bibliographie** : gestion bibliographique avancee (Zotero, Mendeley, EndNote).
- **Annexes techniques** : systeme d'annexes avec numerotation specifique.
