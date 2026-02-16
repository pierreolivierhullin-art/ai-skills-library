# Word Avance — Styles, Automatisation, Champs, Macros & Fonctions Professionnelles

## Overview

Ce document de reference couvre les fonctionnalites avancees de Microsoft Word pour un usage professionnel : hierarchie de styles, Quick Parts et Building Blocks, codes de champ, macros VBA, publipostage avance, documents maitres, comparaison et combinaison de documents, suivi des modifications, verificateur d'accessibilite, mode plan, references croisees et gestion bibliographique. Utiliser ce guide comme fondation pour exploiter pleinement la puissance de Word au-dela de l'usage basique de traitement de texte, et pour concevoir des documents robustes, maintenables et automatisables a l'echelle de l'organisation.

---

## Hierarchie de Styles — Fondation de Tout Document Professionnel

### Comprendre le systeme de styles de Word

Le systeme de styles de Word est la pierre angulaire de tout document professionnel. Un style est un ensemble nomme de proprietes de formatage (police, taille, couleur, espacement, retrait, encadrement, etc.) qui peut etre applique en un clic a un paragraphe, un caractere ou un tableau. Les styles se repartissent en quatre categories :

**Styles de paragraphe** : ils s'appliquent a l'ensemble du paragraphe et controlent la police, la taille, l'espacement avant/apres, l'interligne, les retraits, l'alignement, les enchacements (eviter veuve/orpheline, solidarite avec le paragraphe suivant). Les styles de titre (Heading 1 a Heading 9) sont des styles de paragraphe qui definissent la structure hierarchique du document.

**Styles de caractere** : ils s'appliquent a une selection de texte a l'interieur d'un paragraphe. Exemples : Emphasis (italique semantique), Strong (gras semantique), Subtle Reference, Book Title. Utiliser les styles de caractere plutot que le formatage direct (Ctrl+I, Ctrl+B) pour garantir la coherence et permettre les modifications globales.

**Styles de tableau** : ils definissent l'apparence des tableaux (bordures, couleurs d'alternance, en-tetes). Word propose des styles de tableau pre-configures (Grid Table, List Table, Plain Table) qui peuvent etre personnalises.

**Styles lies** : ils combinent un style de paragraphe et un style de caractere. Quand on applique le style a l'ensemble du paragraphe, c'est le style de paragraphe qui s'active. Quand on l'applique a une selection de texte, c'est le style de caractere.

### Creer et modifier des styles

#### Methode 1 — A partir du formatage existant
1. Formater un paragraphe avec les proprietes souhaitees (police, taille, espacement, etc.).
2. Selectionner le paragraphe.
3. Dans le volet Styles, cliquer sur "Creer un style" et lui donner un nom descriptif.
4. Definir les proprietes supplementaires : style du paragraphe suivant, raccourci clavier, mise a jour automatique.

#### Methode 2 — A partir de la boite de dialogue Modifier le style
1. Dans le volet Styles, cliquer droit sur un style existant > Modifier.
2. Ajuster les proprietes : police, taille, couleur, espacement, retrait.
3. Cliquer sur "Format" en bas a gauche pour acceder aux proprietes avancees : paragraphe, tabulations, bordure, langue, encadrement, numerotation.
4. Cocher "Ajouter a la galerie des styles rapides" pour un acces rapide.
5. Choisir "Nouveaux documents bases sur ce modele" pour sauvegarder dans le template.

### Hierarchie et heritage des styles

Chaque style peut etre "Base sur" un autre style. Le style enfant herite de toutes les proprietes du style parent et peut en modifier certaines. Cette hierarchie permet de creer une cascade coherente :

```
Normal (police de base, taille, interligne)
├── Heading 1 (herite de Normal + taille 16pt, gras, espacement avant 24pt)
│   ├── Heading 2 (herite de Heading 1 + taille 14pt, couleur differente)
│   │   └── Heading 3 (herite de Heading 2 + taille 12pt, italique)
├── List Bullet (herite de Normal + retrait gauche, puce)
├── List Number (herite de Normal + retrait gauche, numerotation)
├── Quote (herite de Normal + retrait gauche/droit, italique)
└── Caption (herite de Normal + taille 10pt, gras)
```

Modifier le style Normal (changer la police de Calibri a Arial, par exemple) impacte automatiquement tous les styles qui en heritent. C'est la puissance de la cascade : une seule modification propage le changement a l'ensemble du document.

### Bonnes pratiques de gestion des styles

- **Limiter le nombre de styles** : un document professionnel standard necessite 10 a 15 styles. Chaque style supplementaire ajoute de la complexite sans valeur. Les styles necessaires : Normal, Heading 1-4, List Bullet, List Number, Quote, Caption, Table styles, et eventuellement 2-3 styles metiers specifiques.
- **Nommer les styles de facon explicite** : utiliser des noms descriptifs pour les styles personnalises (ex. : "Legal Clause", "Technical Note", "Warning Box") plutot que des noms generiques ("Style 1", "Mon Style").
- **Definir le style du paragraphe suivant** : configurer la propriete "Style du paragraphe suivant" pour fluidifier la saisie. Apres un Heading 1, le paragraphe suivant doit automatiquement passer en Normal. Apres un List Bullet, le paragraphe suivant reste en List Bullet.
- **Ne jamais utiliser le formatage direct** : appuyer sur Ctrl+B pour mettre en gras un titre au lieu de lui appliquer le style Heading est un anti-pattern majeur. Le formatage direct ("overrides") masque le style sous-jacent et cree des inconsistances invisibles.
- **Utiliser l'Inspecteur de styles** : l'Inspecteur de styles (Ctrl+Shift+Alt+S puis bouton Inspecteur) permet de voir exactement quel style est applique a un paragraphe et quel formatage direct le recouvre. Utiliser cet outil pour diagnostiquer les problemes de mise en forme.

---

## Quick Parts & Building Blocks — Blocs de Construction Reutilisables

### Concept et utilite

Les Quick Parts (Blocs de construction) sont des elements de contenu pre-formates et reutilisables que l'on peut inserer en quelques clics dans un document. Ils permettent de standardiser et d'accelerer la production documentaire en stockant des fragments de contenu recurrents : en-tetes de lettres, clauses contractuelles, mentions legales, blocs de signature, tableaux pre-formates, pages de garde.

### Types de Building Blocks

| Type | Description | Galerie | Utilisation typique |
|---|---|---|---|
| **Quick Parts** | Fragments de contenu generiques | Quick Parts | Clauses, blocs de texte recurrents |
| **AutoText** | Fragments de texte avec formatage | AutoText | Formules de politesse, mentions legales |
| **Cover Pages** | Pages de garde pre-formatees | Cover Pages | Premieres pages de rapports |
| **Headers & Footers** | En-tetes et pieds de page | Headers / Footers | En-tetes avec logo, pieds avec pagination |
| **Page Numbers** | Formats de numerotation | Page Numbers | Numerotation personnalisee |
| **Tables** | Tableaux pre-formates | Tables | Tableaux de bord, tableaux de donnees |
| **Text Boxes** | Zones de texte pre-formatees | Text Boxes | Encadres, avertissements, callouts |
| **Watermarks** | Filigranes | Watermarks | Confidentiel, Brouillon, Specimen |
| **Equations** | Formules mathematiques | Equations | Equations recurrentes |
| **Bibliographies** | Formats de bibliographie | Bibliography | Styles de citation |

### Creer un Building Block

1. Selectionner le contenu a sauvegarder (texte, image, tableau, ou combinaison).
2. Aller dans l'onglet Insertion > Quick Parts > Enregistrer la selection dans la galerie Quick Parts.
3. Remplir la boite de dialogue :
   - **Nom** : nom descriptif du bloc (ex. : "Clause de confidentialite NDA")
   - **Galerie** : categorie de classement (Quick Parts, AutoText, etc.)
   - **Categorie** : sous-categorie personnalisable (ex. : "Juridique", "Commercial")
   - **Description** : explication de l'usage du bloc
   - **Enregistrer dans** : Building Blocks.dotx (disponible dans tous les documents) ou un template specifique (disponible uniquement dans les documents bases sur ce template)
   - **Options** : "Inserer le contenu uniquement", "Inserer le contenu dans son propre paragraphe", ou "Inserer le contenu dans sa propre page"

### Gestion a l'echelle de l'organisation

Pour deployer des Building Blocks a l'echelle de l'organisation :
- Creer un fichier Building Blocks.dotx centralise contenant tous les blocs standards.
- Deployer ce fichier via Group Policy dans le dossier `%APPDATA%\Microsoft\Document Building Blocks\[Langue]\16\` de chaque poste utilisateur.
- Alternativement, stocker les blocs dans le template d'entreprise (Normal.dotm ou un template de departement) et deployer le template via SharePoint ou Group Policy.
- Documenter chaque bloc (nom, categorie, contenu, usage) dans un catalogue accessible aux utilisateurs.

---

## Codes de Champ — Informations Dynamiques et Logique dans les Documents

### Comprendre les codes de champ

Les codes de champ sont des instructions que Word execute pour inserer des informations dynamiques dans le document. Contrairement au texte statique, le contenu d'un champ se met a jour automatiquement (ou sur commande) lorsque le document est ouvert, imprime ou que l'utilisateur appuie sur F9.

### Champs essentiels pour l'usage professionnel

| Champ | Syntaxe | Description | Exemple de resultat |
|---|---|---|---|
| **DATE** | `{ DATE \@ "dd/MM/yyyy" }` | Date du jour au format specifie | 16/02/2026 |
| **CREATEDATE** | `{ CREATEDATE \@ "dd MMMM yyyy" }` | Date de creation du document | 10 janvier 2026 |
| **SAVEDATE** | `{ SAVEDATE \@ "dd/MM/yyyy HH:mm" }` | Date et heure de derniere sauvegarde | 15/02/2026 14:30 |
| **AUTHOR** | `{ AUTHOR }` | Auteur du document (propriete) | Jean Dupont |
| **FILENAME** | `{ FILENAME \p }` | Nom du fichier avec chemin complet | C:\Documents\rapport.docx |
| **NUMPAGES** | `{ NUMPAGES }` | Nombre total de pages | 42 |
| **PAGE** | `{ PAGE }` | Numero de la page courante | 7 |
| **DOCPROPERTY** | `{ DOCPROPERTY "Version" }` | Valeur d'une propriete personnalisee | 2.1 |
| **IF** | `{ IF { MERGEFIELD Montant } > 10000 "Approbation requise" "Standard" }` | Logique conditionnelle | Approbation requise |
| **REF** | `{ REF _Ref123456789 \h }` | Reference croisee a un signet | voir section 3.2 |
| **SEQ** | `{ SEQ Figure }` | Numerotation sequentielle | Figure 5 |
| **TOC** | `{ TOC \o "1-3" \h }` | Table des matieres des niveaux 1 a 3 | (table des matieres) |
| **STYLEREF** | `{ STYLEREF "Heading 1" }` | Derniere occurrence du style dans la page | Chapitre 3 |
| **MERGEFIELD** | `{ MERGEFIELD Prenom }` | Champ de publipostage | Marie |

### Inserer et manipuler des champs

- **Inserer un champ** : Ctrl+F9 cree les accolades de champ. Taper le code du champ entre les accolades. Ne jamais taper les accolades manuellement au clavier — elles doivent etre generees par Ctrl+F9.
- **Alterner affichage** : Alt+F9 bascule entre l'affichage du code de champ et le resultat. Utile pour deboguer.
- **Mettre a jour un champ** : F9 met a jour le champ selectionne. Ctrl+A puis F9 met a jour tous les champs du document.
- **Verrouiller un champ** : Ctrl+F11 verrouille un champ pour empecher sa mise a jour. Ctrl+Shift+F11 pour deverrouiller.

### Champs avances — DOCPROPERTY et proprietes personnalisees

Les proprietes personnalisees du document permettent de stocker des metadonnees metiers (numero de projet, client, version, classification, statut) qui peuvent etre affichees dans le document via le champ DOCPROPERTY :

1. Aller dans Fichier > Proprietes > Proprietes avancees > onglet Personnalise.
2. Ajouter une propriete : Nom = "Client", Type = Texte, Valeur = "Acme Corp".
3. Dans le document, inserer un champ : `{ DOCPROPERTY "Client" }`.
4. Le champ affiche "Acme Corp" et se met a jour si la propriete est modifiee.

Cette technique permet de creer des templates ou les informations contextuelles (client, projet, version, date) sont saisies une seule fois dans les proprietes et affichees automatiquement partout dans le document (page de garde, en-tete, pied de page, mentions).

---

## Macros VBA — Automatiser les Taches Repetitives

### Quand utiliser les macros

Les macros VBA (Visual Basic for Applications) permettent d'automatiser des sequences d'actions repetitives dans Word. Utiliser les macros pour :
- Appliquer une sequence de formatage complexe en un clic
- Nettoyer le formatage parasite (espaces doubles, sauts de page manuels, formatage direct)
- Inserer des structures complexes (tableaux pre-remplis, blocs de contenu conditionnel)
- Automatiser les verifications de qualite (verifier les styles appliques, detecter les images sans texte alternatif)
- Exporter ou importer des donnees depuis/vers Excel ou des bases de donnees

### Exemples de macros essentielles

#### Macro 1 — Nettoyer le formatage direct
```vba
Sub CleanDirectFormatting()
    ' Supprime tout formatage direct du document
    ' Conserve uniquement le formatage defini par les styles
    Selection.WholeStory
    Selection.ClearFormatting
    ' Restaure les styles
    Dim para As Paragraph
    For Each para In ActiveDocument.Paragraphs
        If para.Style = ActiveDocument.Styles("Normal") Then
            ' Verifie que le style Normal est correctement applique
            para.Range.Font.Reset
            para.Range.ParagraphFormat.Reset
        End If
    Next para
    MsgBox "Formatage direct supprime.", vbInformation
End Sub
```

#### Macro 2 — Remplacer les espaces doubles
```vba
Sub FixDoubleSpaces()
    ' Remplace tous les doubles espaces par des espaces simples
    With ActiveDocument.Content.Find
        .Text = "  "
        .Replacement.Text = " "
        .Forward = True
        .Wrap = wdFindContinue
        .MatchCase = False
        .MatchWholeWord = False
        Do While .Execute(Replace:=wdReplaceAll)
        Loop
    End With
    MsgBox "Espaces doubles corriges.", vbInformation
End Sub
```

#### Macro 3 — Inserer un bloc de signature
```vba
Sub InsertSignatureBlock()
    Dim rng As Range
    Set rng = Selection.Range
    rng.InsertAfter vbCr & vbCr
    rng.Collapse wdCollapseEnd
    rng.Text = "Fait a _____________, le { DATE \@ ""dd/MM/yyyy"" }" & vbCr & vbCr
    rng.InsertAfter "Nom : _________________________" & vbCr
    rng.InsertAfter "Fonction : _____________________" & vbCr
    rng.InsertAfter "Signature : " & vbCr & vbCr
    rng.Style = ActiveDocument.Styles("Normal")
End Sub
```

### Securite des macros

- **Ne jamais activer les macros provenant de sources non fiables.** Les macros VBA peuvent contenir du code malveillant (virus de macro).
- Configurer le niveau de securite des macros dans Fichier > Options > Centre de gestion de la confidentialite > Parametres des macros.
- Pour les macros de l'organisation, utiliser un **certificat numerique** pour signer les macros et configurer les postes pour n'accepter que les macros signees par ce certificat.
- Stocker les macros de l'organisation dans un **template global** (Normal.dotm ou un template complementaire .dotm) deploye de maniere centralisee.

---

## Publipostage Avance — Production en Serie Personnalisee

### Architecture du publipostage

Le publipostage (mail merge) permet de produire en serie des documents personnalises (lettres, enveloppes, etiquettes, emails, repertoires) en fusionnant un document principal (le template de publipostage) avec une source de donnees (fichier Excel, base Access, liste SharePoint, contacts Outlook).

### Source de donnees — Bonnes pratiques

| Critere | Bonne pratique | Anti-pattern |
|---|---|---|
| **Structure** | Une ligne par enregistrement, une colonne par champ | Donnees en vrac sans structure |
| **En-tetes** | Noms de colonnes explicites, sans espaces ni caracteres speciaux | Colonnes nommees "Col1", "Donnee" |
| **Types** | Formater les dates en format date, les nombres en format nombre | Tout en texte brut |
| **Completude** | Pas de cellules vides pour les champs obligatoires | Donnees manquantes non gerees |
| **Nettoyage** | Donnees nettoyees avant utilisation (doublons, erreurs de saisie) | Donnees brutes non verifiees |

### Regles de publipostage avancees

Word offre des regles conditionnelles pour personnaliser le contenu du document fusionne en fonction des donnees :

- **IF...THEN...ELSE** : `{ IF { MERGEFIELD Civilite } = "M." "Monsieur" "Madame" }` — affiche "Monsieur" ou "Madame" selon la valeur du champ Civilite.
- **SKIP RECORD IF** : `{ SKIPIF { MERGEFIELD Montant } = "0" }` — saute l'enregistrement si le montant est zero. Utile pour filtrer les destinataires.
- **NEXT RECORD** : `{ NEXT }` — passe a l'enregistrement suivant sans creer de nouveau document. Utilise pour les etiquettes et les repertoires.
- **MERGESEQ** : `{ MERGESEQ }` — affiche le numero sequentiel de l'enregistrement dans la fusion (1, 2, 3...).
- **MERGEREC** : `{ MERGEREC }` — affiche le numero de l'enregistrement dans la source de donnees.

### Publipostage avec conditions complexes

Pour des logiques conditionnelles complexes (plus de 2 niveaux), imbriquer les champs IF ou combiner avec les proprietes du document :

```
{ IF { MERGEFIELD Montant } > 50000
    "Ce contrat est soumis a l'approbation du Directeur Financier.
     { IF { MERGEFIELD TypeClient } = "Public"
         "Les regles des marches publics s'appliquent."
         "Les conditions generales de vente standard s'appliquent."
     }"
    "Ce contrat releve de la procedure standard."
}
```

### Publipostage vers differentes sorties

| Sortie | Methode | Usage typique |
|---|---|---|
| **Nouveau document** | Fusionner vers un nouveau document | Revue avant impression, archivage |
| **Imprimante** | Fusionner directement vers l'imprimante | Production de masse sans revision |
| **Email** | Fusionner vers Outlook | Envoi personnalise par email |
| **Enveloppes** | Fusionner vers des enveloppes formatees | Expedition postale |
| **Etiquettes** | Fusionner vers une planche d'etiquettes | Etiquettes d'adresse, badges |
| **PDF individuels** | Macro VBA pour generer un PDF par enregistrement | Archivage individuel, envoi numerique |

---

## Documents Maitres — Gerer les Documents Longs

### Concept et architecture

Un document maitre (Master Document) est un conteneur qui reunit plusieurs sous-documents (sub-documents) en un seul document logique. Chaque sous-document est un fichier Word independant qui peut etre edite separement. Le document maitre permet de :
- Gerer des documents volumineux (200+ pages) sans problemes de performance
- Repartir la redaction entre plusieurs auteurs (chacun travaille sur son sous-document)
- Generer une table des matieres, un index et une numerotation de pages continus sur l'ensemble des sous-documents

### Utilisation recommandee

1. Creer le document maitre en mode Plan (Affichage > Plan).
2. Definir la structure avec les titres principaux (Heading 1).
3. Pour chaque section, utiliser "Inserer un sous-document" ou "Creer un sous-document" a partir d'un titre existant.
4. Chaque sous-document est enregistre comme un fichier .docx independant dans le meme repertoire.
5. La table des matieres, les references croisees et la numerotation fonctionnent a travers l'ensemble des sous-documents.

### Precautions avec les documents maitres

Les documents maitres ont une reputation de fragilite dans Word. Suivre ces regles pour eviter les problemes :
- **Toujours travailler en mode Plan** pour manipuler les sous-documents.
- **Ne jamais renommer ou deplacer** les sous-documents sans mettre a jour les liens dans le document maitre.
- **Sauvegarder frequemment** et maintenir des copies de sauvegarde.
- **Eviter d'editer le document maitre et les sous-documents simultanement**.
- **Utiliser un template commun** pour le document maitre et tous les sous-documents afin de garantir la coherence des styles.

---

## Comparaison et Combinaison de Documents

### Comparer deux versions

La fonction Comparer (onglet Revision > Comparer) permet de comparer deux versions d'un document et de generer un document resultant qui affiche toutes les differences sous forme de marques de revision (Track Changes) :

1. Selectionner le document original et le document revise.
2. Configurer les options de comparaison : insertions, suppressions, deplacements, formatage, commentaires, en-tetes/pieds de page, champs, tableaux.
3. Choisir ou afficher les modifications : dans le document original, le document revise, ou un nouveau document.
4. Le resultat est un document avec des marques de revision que l'on peut accepter ou rejeter individuellement.

### Combiner des revisions

La fonction Combiner (onglet Revision > Combiner) permet de fusionner les revisions de plusieurs relecteurs dans un seul document :

1. Choisir le document original.
2. Ajouter successivement les documents revises par chaque relecteur.
3. Word combine toutes les modifications en attribuant chaque changement a son auteur.
4. Le document resultant contient toutes les marques de revision de tous les relecteurs, identifiees par auteur et par couleur.

### Cas d'usage professionnels

- **Revue contractuelle** : comparer la version envoyee au client avec la version retournee pour identifier toutes les modifications apportees.
- **Audit de conformite** : comparer un document avec le template de reference pour detecter les ecarts.
- **Consolidation de feedback** : combiner les retours de 3-5 relecteurs dans un seul document pour faciliter l'integration.

---

## Suivi des Modifications (Track Changes)

### Configuration optimale

- **Activer le suivi** : onglet Revision > Suivi des modifications (Ctrl+Shift+E).
- **Options d'affichage** : configurer les options d'affichage des marques de revision (insertions en souligne, suppressions en barre, couleur par auteur).
- **Volet de revision** : afficher le volet de revision (vertical ou horizontal) pour naviguer facilement entre les modifications.
- **Affichage simplifie** : basculer entre "Toutes les marques", "Balisage simple", "Aucune marque" et "Original" pour visualiser le document a differents niveaux de detail.

### Bonnes pratiques de revision

- **Un relecteur, un passage** : chaque relecteur fait un seul passage de relecture. Les allers-retours multiples creent une accumulation de marques de revision difficile a gerer.
- **Commenter plutot que reecrire** : quand la modification proposee est complexe ou sujette a discussion, utiliser un commentaire pour expliquer l'intention plutot que de reecrire directement.
- **Accepter/Rejeter methodiquement** : traiter les modifications une par une (Accepter/Rejeter + Suivante) plutot que de tout accepter en bloc. Chaque modification merite une decision explicite.
- **Version finale propre** : avant de distribuer le document final, accepter toutes les modifications restantes, supprimer tous les commentaires et verifier qu'aucune marque de revision residuelle ne subsiste (Revision > Verifier le document).

---

## Mode Plan et Structure du Document

### Utiliser le mode Plan efficacement

Le mode Plan (Affichage > Plan) offre une vue structurelle du document basee sur les styles de titres. Il permet de :
- **Visualiser la structure** : voir la hierarchie des titres de niveau 1 a 9, avec la possibilite de plier/deplier les sections.
- **Reorganiser** : deplacer des sections entieres (avec tout leur contenu) par glisser-deposer ou avec les fleches haut/bas.
- **Promouvoir/Retrograder** : changer le niveau d'un titre (Heading 2 > Heading 1 ou inversement) avec les fleches gauche/droite.
- **Naviguer rapidement** : dans un document long, le mode Plan permet de localiser instantanement une section.

### Volet de navigation

Le volet de navigation (Affichage > Volet de navigation ou Ctrl+F) offre une vue permanente de la structure du document dans un panneau lateral. Il permet de :
- Naviguer vers n'importe quel titre en un clic.
- Reorganiser les sections par glisser-deposer.
- Rechercher du texte, des tableaux, des images, des commentaires, des notes de bas de page.

---

## References Croisees

### Types de references croisees

Les references croisees permettent de creer des renvois automatiques vers d'autres elements du document. Contrairement aux renvois manuels ("voir page 12"), les references croisees se mettent a jour automatiquement lorsque le document est reorganise :

| Element reference | Exemple | Options d'affichage |
|---|---|---|
| **Titre** | "voir Chapitre 3 — Analyse" | Texte du titre, numero de page, "ci-dessus"/"ci-dessous" |
| **Figure** | "voir Figure 5" | Legende entiere, numero uniquement, numero de page |
| **Tableau** | "voir Tableau 2" | Legende entiere, numero uniquement, numero de page |
| **Equation** | "voir Equation (3)" | Legende entiere, numero uniquement |
| **Note de bas de page** | "voir note 7" | Numero de la note, numero de page |
| **Signet** | "voir Annexe A" | Texte du signet, numero de page |
| **Paragraphe numerote** | "voir clause 4.2.1" | Numero du paragraphe, texte, numero de page |

### Inserer et maintenir les references croisees

1. Aller dans Insertion > Reference croisee.
2. Selectionner le type de reference (titre, figure, tableau, signet, etc.).
3. Choisir l'element cible et l'option d'affichage.
4. Cocher "Inserer comme lien hypertexte" pour permettre la navigation par clic.
5. Mettre a jour toutes les references : Ctrl+A puis F9.

---

## Gestion Bibliographique

### Sources et citations dans Word

Word integre un gestionnaire de sources bibliographiques (onglet References > Gerer les sources) qui permet de :
- Creer et stocker des references bibliographiques (livres, articles, sites web, rapports).
- Inserer des citations dans le texte selon un style de citation (APA 7th, Chicago, IEEE, MLA, etc.).
- Generer automatiquement la bibliographie a partir des citations inserees.

### Workflow de gestion bibliographique

1. **Ajouter les sources** : pour chaque source, renseigner le type (livre, article, site web), les auteurs, le titre, l'annee, l'editeur, le DOI, etc.
2. **Inserer les citations** : positionner le curseur a l'endroit souhaite, aller dans References > Inserer une citation, selectionner la source. Word insere la citation au format du style choisi (ex. : "(Dupont, 2025)" en APA).
3. **Generer la bibliographie** : aller dans References > Bibliographie et choisir un format. La bibliographie est generee automatiquement a partir de toutes les citations inserees.
4. **Mettre a jour** : ajouter de nouvelles citations et mettre a jour la bibliographie en un clic.

### Integrations avec des gestionnaires de references externes

Pour les besoins avances (plusieurs milliers de references, collaboration entre chercheurs, import depuis PubMed/Scopus/Web of Science), utiliser un gestionnaire de references externe :
- **Zotero** : gratuit, open source, plugin Word performant, synchronisation cloud.
- **Mendeley** : gratuit (version de base), integration avec Elsevier/Scopus.
- **EndNote** : payant, reference dans le monde academique, fonctionnalites avancees.

Ces outils s'integrent a Word via des plugins qui ajoutent un onglet dedie et permettent d'inserer des citations et de generer des bibliographies directement depuis la base de references.

---

## Verificateur d'Accessibilite

### Utilisation

Le verificateur d'accessibilite de Word (onglet Revision > Verifier l'accessibilite) analyse le document et detecte les problemes d'accessibilite classes en trois niveaux :

- **Erreurs** (bloquantes) : images sans texte alternatif, tableaux sans en-tetes, document sans titre.
- **Avertissements** (importants) : contraste insuffisant, ordre de lecture incorrect, en-tetes de tableau repetes.
- **Conseils** (ameliorations) : texte de lien hypertexte generique ("cliquez ici"), objets groupes, diapositives sans titre.

### Points de verification essentiels

- **Texte alternatif** : chaque image, graphique, SmartArt et objet flottant doit avoir un texte alternatif descriptif qui decrit le contenu et la fonction de l'element visuel.
- **Structure des titres** : utiliser les styles de titres dans l'ordre hierarchique (H1, H2, H3) sans sauter de niveau.
- **Tableaux** : definir la premiere ligne comme en-tete de colonne. Eviter les cellules fusionnees qui compliquent la navigation au lecteur d'ecran.
- **Liens hypertexte** : utiliser un texte de lien descriptif ("Consulter le rapport annuel 2025") plutot que l'URL brute ou "cliquez ici".
- **Contraste** : garantir un ratio de contraste d'au moins 4.5:1 entre le texte et l'arriere-plan.

---

## Fonctionnalites Avancees Complementaires

### Index

L'index permet de creer un repertoire alphabetique des termes importants du document avec renvoi aux pages correspondantes :
1. Marquer les entrees d'index : selectionner le terme, aller dans References > Marquer l'entree (Alt+Shift+X).
2. Configurer l'entree : entree principale, sous-entree, reference croisee, plage de pages.
3. Inserer l'index : References > Inserer un index, choisir le format et le nombre de colonnes.

### Table des illustrations

La table des illustrations genere automatiquement un repertoire de toutes les figures, tableaux ou equations du document, a condition que chaque element ait une legende inseree via References > Inserer une legende.

### Sections et sauts de section

Les sauts de section permettent de diviser le document en sections independantes avec des parametres de mise en page differents :
- **Saut de section page suivante** : la nouvelle section commence sur la page suivante. Utilise pour changer l'orientation (portrait/paysage), les marges, les en-tetes/pieds de page.
- **Saut de section continu** : la nouvelle section commence au meme endroit sur la page. Utilise pour changer le nombre de colonnes.
- **Saut de section page paire/impaire** : la nouvelle section commence sur la prochaine page paire ou impaire. Utilise pour les documents imprimes en recto-verso (chapitres commencant toujours sur la page de droite).

Chaque section peut avoir ses propres en-tetes/pieds de page, marges, orientation, numerotation de pages et nombre de colonnes. Utiliser le bouton "Lier au precedent" dans l'en-tete/pied de page pour controler l'heritage entre sections.

---

## Raccourcis Clavier Essentiels

| Raccourci | Action |
|---|---|
| Ctrl+Shift+S | Appliquer un style |
| Alt+Ctrl+1/2/3 | Appliquer Heading 1/2/3 |
| Ctrl+Shift+N | Appliquer le style Normal |
| Ctrl+F9 | Inserer un code de champ |
| Alt+F9 | Alterner affichage codes de champ / resultats |
| F9 | Mettre a jour les champs selectionnes |
| Ctrl+Shift+E | Activer/desactiver le suivi des modifications |
| Ctrl+A, F9 | Mettre a jour tous les champs du document |
| Ctrl+Shift+F5 | Definir un signet |
| Alt+Shift+X | Marquer une entree d'index |
| Alt+Ctrl+F | Inserer une note de bas de page |
| Alt+Ctrl+D | Inserer une note de fin |
| Ctrl+Shift+L | Appliquer le style Liste a puces |

---

## Integration avec Microsoft 365 et Copilot (2025-2026)

### Word dans Microsoft 365

Word dans l'ecosysteme Microsoft 365 offre des fonctionnalites cloud avancees :
- **Co-edition en temps reel** : plusieurs utilisateurs editent simultanement le meme document stocke sur OneDrive ou SharePoint. Chaque utilisateur voit les modifications des autres en temps reel avec des indicateurs de presence.
- **Historique des versions** : chaque modification est enregistree avec l'auteur et l'horodatage. Possibilite de restaurer n'importe quelle version anterieure.
- **Commentaires et @mentions** : les commentaires peuvent mentionner des collegues avec @nom, declenchant une notification par email et Teams.
- **Integration Teams** : ouvrir et co-editer des documents Word directement dans Teams sans changer d'application.

### Copilot dans Word

Microsoft Copilot (base sur GPT-4 et les donnees Microsoft Graph) integre des capacites d'IA generative directement dans Word :
- **Redaction assistee** : generer des premiers jets, reformuler des paragraphes, ajuster le ton (formel, informel, technique).
- **Synthese** : resumer un document long en quelques paragraphes ou en liste a puces.
- **Transformation** : transformer un document Word en presentation PowerPoint, ou un email en rapport structure.
- **Extraction d'informations** : poser des questions sur le contenu du document et obtenir des reponses contextualisees.
- **Mise en forme intelligente** : Copilot peut appliquer des styles, creer des tableaux et structurer le document selon les bonnes pratiques.

L'enjeu pour les organisations est de former les utilisateurs a utiliser Copilot efficacement (qualite des prompts, verification des contenus generes, respect de la confidentialite des donnees) et de definir des politiques d'usage claires.
