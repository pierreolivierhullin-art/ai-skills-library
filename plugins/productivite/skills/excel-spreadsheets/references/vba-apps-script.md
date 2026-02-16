# VBA & Apps Script — Automation, Macros, Custom Functions & Integration

## Introduction

**FR** — Ce guide de reference couvre l'automatisation des tableurs via VBA (Visual Basic for Applications) pour Excel et Apps Script pour Google Sheets. Il detaille les fondamentaux de chaque langage, les patrons d'automatisation courants (boucles, fichiers, formulaires, emails), la gestion des erreurs, la creation de fonctions personnalisees, les strategies d'integration (APIs, bases de donnees, systemes externes), la securite, et les strategies de migration entre les deux environnements. L'objectif est de fournir les cles pour transformer des taches manuelles repetitives en processus automatises fiables et maintenables.

**EN** — This reference guide covers spreadsheet automation via VBA (Visual Basic for Applications) for Excel and Apps Script for Google Sheets. It details the fundamentals of each language, common automation patterns (loops, files, forms, emails), error handling, custom function creation, integration strategies (APIs, databases, external systems), security, and migration strategies between both environments.

---

## 1. VBA Fundamentals

### Architecture VBA

VBA s'execute dans l'environnement Visual Basic Editor (VBE), accessible via Alt+F11 dans Excel. Le code est organise en modules, classes, et formulaires (UserForms).

**Structure d'un projet VBA :**

```
VBAProject (MonClasseur.xlsm)
├── Microsoft Excel Objects
│   ├── ThisWorkbook        (evenements au niveau classeur)
│   ├── Feuil1 (Donnees)    (evenements au niveau feuille)
│   └── Feuil2 (Dashboard)
├── Modules
│   ├── Module1             (procedures et fonctions generales)
│   ├── modUtilities        (fonctions utilitaires)
│   └── modExport           (procedures d'export)
├── Class Modules
│   └── clsDataProcessor    (classes personnalisees)
└── Forms
    └── frmParametres       (formulaires utilisateur)
```

### Types de procedures

```vba
' Sub : procedure qui execute des actions (pas de valeur de retour)
Sub GenererRapport()
    ' Code ici
End Sub

' Function : retourne une valeur (utilisable dans les cellules)
Function CalculerMarge(prixVente As Double, cout As Double) As Double
    CalculerMarge = (prixVente - cout) / prixVente
End Function

' Property : accesseur de classe
Property Get Nom() As String
    Nom = mNom
End Property
```

### Variables et types

```vba
' Declaration explicite (TOUJOURS activer Option Explicit)
Option Explicit

Sub ExempleVariables()
    ' Types fondamentaux
    Dim nom As String
    Dim age As Long              ' Preferer Long a Integer (pas de limite 32K)
    Dim montant As Double
    Dim estActif As Boolean
    Dim dateDebut As Date

    ' Objets Excel
    Dim ws As Worksheet
    Dim rng As Range
    Dim wb As Workbook
    Dim tbl As ListObject

    ' Affectation
    Set ws = ThisWorkbook.Worksheets("Donnees")
    Set rng = ws.Range("A1:D100")
    Set tbl = ws.ListObjects("tbl_Ventes")

    nom = "Rapport Mensuel"
    age = 25
    montant = 1500.75
    estActif = True
    dateDebut = Date
End Sub
```

### Navigation dans le modele objet Excel

```vba
' Hierarchie : Application > Workbook > Worksheet > Range

' Acceder a une feuille
Dim ws As Worksheet
Set ws = ThisWorkbook.Worksheets("Donnees")

' Acceder a une cellule
ws.Range("A1").Value = "Hello"
ws.Cells(1, 1).Value = "Hello"    ' Ligne 1, Colonne 1

' Acceder a une table structuree
Dim tbl As ListObject
Set tbl = ws.ListObjects("tbl_Ventes")
Dim colMontant As Range
Set colMontant = tbl.ListColumns("Montant").DataBodyRange

' Derniere ligne avec donnees
Dim lastRow As Long
lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row

' Derniere colonne avec donnees
Dim lastCol As Long
lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column

' Plage dynamique
Dim dataRange As Range
Set dataRange = ws.Range("A1").CurrentRegion    ' Region contigue
```

---

## 2. Common VBA Patterns

### Pattern 1 — Boucle sur les lignes d'un tableau

```vba
Sub TraiterDonnees()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("Donnees")

    Dim tbl As ListObject
    Set tbl = ws.ListObjects("tbl_Ventes")

    Dim row As ListRow
    For Each row In tbl.ListRows
        Dim montant As Double
        montant = row.Range.Cells(1, tbl.ListColumns("Montant").Index).Value

        If montant > 10000 Then
            row.Range.Cells(1, tbl.ListColumns("Statut").Index).Value = "VIP"
        End If
    Next row
End Sub
```

### Pattern 2 — Optimisation de performance

```vba
Sub TraitementRapide()
    ' TOUJOURS desactiver les mises a jour ecran et calcul pour les operations en masse
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False

    On Error GoTo Cleanup    ' S'assurer de reactiver meme en cas d'erreur

    ' --- Traitement ici ---
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("Donnees")

    ' Lire toutes les donnees en une fois dans un tableau (BEAUCOUP plus rapide que cellule par cellule)
    Dim data As Variant
    data = ws.Range("A1:D10000").Value    ' Tableau 2D en memoire

    Dim i As Long
    For i = 2 To UBound(data, 1)
        ' Traiter en memoire (pas d'acces aux cellules)
        If data(i, 3) > 1000 Then
            data(i, 4) = "Important"
        Else
            data(i, 4) = "Standard"
        End If
    Next i

    ' Ecrire toutes les donnees en une fois
    ws.Range("A1:D10000").Value = data

Cleanup:
    ' TOUJOURS reactiver
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Application.EnableEvents = True
End Sub
```

### Pattern 3 — Operations sur les fichiers

```vba
Sub ConsoliderFichiersCSV()
    Dim dossierPath As String
    dossierPath = ThisWorkbook.Path & "\Donnees\"

    Dim fichier As String
    fichier = Dir(dossierPath & "*.csv")

    Dim wsOutput As Worksheet
    Set wsOutput = ThisWorkbook.Worksheets("Consolidation")
    Dim ligneSortie As Long
    ligneSortie = 2    ' Ligne 1 = en-tetes

    Do While fichier <> ""
        ' Ouvrir le CSV
        Dim wb As Workbook
        Set wb = Workbooks.Open(dossierPath & fichier, ReadOnly:=True)

        ' Copier les donnees (sans en-tete)
        Dim lastRow As Long
        lastRow = wb.Sheets(1).Cells(wb.Sheets(1).Rows.Count, "A").End(xlUp).Row

        If lastRow > 1 Then
            Dim dataRange As Range
            Set dataRange = wb.Sheets(1).Range("A2:D" & lastRow)
            dataRange.Copy wsOutput.Cells(ligneSortie, 1)
            ligneSortie = ligneSortie + lastRow - 1
        End If

        wb.Close SaveChanges:=False
        fichier = Dir()    ' Fichier suivant
    Loop

    MsgBox "Consolidation terminee : " & (ligneSortie - 2) & " lignes importees."
End Sub
```

### Pattern 4 — Export PDF

```vba
Sub ExporterEnPDF()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("Rapport")

    Dim filePath As String
    filePath = ThisWorkbook.Path & "\Exports\Rapport_" & Format(Date, "YYYY-MM-DD") & ".pdf"

    ' Configurer la mise en page
    With ws.PageSetup
        .Orientation = xlLandscape
        .FitToPagesWide = 1
        .FitToPagesTall = False
        .PrintArea = ws.UsedRange.Address
    End With

    ' Exporter
    ws.ExportAsFixedFormat _
        Type:=xlTypePDF, _
        Filename:=filePath, _
        Quality:=xlQualityStandard, _
        IncludeDocProperties:=False, _
        IgnorePrintAreas:=False, _
        OpenAfterPublish:=False

    MsgBox "PDF exporte : " & filePath
End Sub
```

### Pattern 5 — UserForm (Formulaire de saisie)

```vba
' --- Dans le module du UserForm (frmSaisie) ---

Private Sub btnValider_Click()
    ' Validation
    If txtNom.Text = "" Then
        MsgBox "Le nom est obligatoire.", vbExclamation
        txtNom.SetFocus
        Exit Sub
    End If

    If Not IsNumeric(txtMontant.Text) Then
        MsgBox "Le montant doit etre numerique.", vbExclamation
        txtMontant.SetFocus
        Exit Sub
    End If

    ' Ecrire dans la table
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("Donnees")
    Dim tbl As ListObject
    Set tbl = ws.ListObjects("tbl_Saisies")

    Dim newRow As ListRow
    Set newRow = tbl.ListRows.Add
    newRow.Range.Cells(1, 1).Value = txtNom.Text
    newRow.Range.Cells(1, 2).Value = CDbl(txtMontant.Text)
    newRow.Range.Cells(1, 3).Value = cboCategorie.Value
    newRow.Range.Cells(1, 4).Value = Now()

    ' Reinitialiser
    txtNom.Text = ""
    txtMontant.Text = ""
    MsgBox "Enregistrement ajoute.", vbInformation
End Sub

Private Sub btnFermer_Click()
    Unload Me
End Sub

' --- Dans un module standard ---
Sub OuvrirFormulaire()
    frmSaisie.Show
End Sub
```

---

## 3. Error Handling in VBA

### Structure de gestion d'erreurs

```vba
Sub ProcedureRobuste()
    On Error GoTo ErrorHandler

    ' Code principal
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("Donnees")

    ' Operation risquee
    Dim valeur As Double
    valeur = ws.Range("A1").Value / ws.Range("B1").Value

    ' Si tout va bien
    Exit Sub

ErrorHandler:
    Select Case Err.Number
        Case 11    ' Division par zero
            MsgBox "Erreur : division par zero en cellule B1.", vbExclamation
        Case 9     ' Index hors limites
            MsgBox "Erreur : la feuille n'existe pas.", vbExclamation
        Case Else
            MsgBox "Erreur inattendue #" & Err.Number & ": " & Err.Description, vbCritical
    End Select

    ' Optionnel : journaliser l'erreur
    Call LogError(Err.Number, Err.Description, "ProcedureRobuste")
End Sub
```

### Logging des erreurs

```vba
Sub LogError(errNum As Long, errDesc As String, errSource As String)
    Dim wsLog As Worksheet

    On Error Resume Next
    Set wsLog = ThisWorkbook.Worksheets("ErrorLog")
    If wsLog Is Nothing Then
        Set wsLog = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
        wsLog.Name = "ErrorLog"
        wsLog.Range("A1:D1").Value = Array("Date", "Numero", "Description", "Source")
    End If
    On Error GoTo 0

    Dim nextRow As Long
    nextRow = wsLog.Cells(wsLog.Rows.Count, "A").End(xlUp).Row + 1

    wsLog.Cells(nextRow, 1).Value = Now()
    wsLog.Cells(nextRow, 2).Value = errNum
    wsLog.Cells(nextRow, 3).Value = errDesc
    wsLog.Cells(nextRow, 4).Value = errSource
End Sub
```

### Debugging techniques

| Technique | Raccourci | Usage |
|---|---|---|
| **Breakpoint** | F9 | Arreter l'execution a une ligne specifique |
| **Step Into** | F8 | Executer ligne par ligne |
| **Step Over** | Shift+F8 | Executer sans entrer dans les sous-procedures |
| **Immediate Window** | Ctrl+G | Tester des expressions et afficher des valeurs (`Debug.Print`) |
| **Watch Window** | Menu Debug | Surveiller la valeur d'une variable en temps reel |
| **Locals Window** | Menu View | Voir toutes les variables locales |

---

## 4. Apps Script Fundamentals

### Architecture Apps Script

Google Apps Script est base sur JavaScript (ES6+). Il s'execute dans le cloud Google et a acces natif a tous les services Google (Sheets, Drive, Gmail, Calendar, etc.).

**Types de projets :**
- **Container-bound** : Lie a un fichier Google (Sheets, Docs, Slides). Acces via Extensions → Apps Script
- **Standalone** : Projet independant dans Google Drive. Ideal pour les bibliotheques partagees

**Structure d'un projet Apps Script :**

```
Mon Projet Apps Script
├── Code.gs           (script principal)
├── Utils.gs          (fonctions utilitaires)
├── Triggers.gs       (configuration des declencheurs)
├── appsscript.json   (manifest — permissions, scopes)
└── HTML files        (interfaces web personnalisees)
    └── sidebar.html
```

### Manipulation de Google Sheets

```javascript
// Acceder au spreadsheet actif
function exempleBasique() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("Donnees");

  // Lire une cellule
  const valeur = sheet.getRange("A1").getValue();

  // Lire une plage (retourne un tableau 2D)
  const data = sheet.getRange("A1:D100").getValues();

  // Ecrire une valeur
  sheet.getRange("E1").setValue("Resultat");

  // Ecrire un tableau (BEAUCOUP plus rapide que cellule par cellule)
  const output = data.map(row => [row[0] * 2]);
  sheet.getRange("E1:E100").setValues(output);

  // Derniere ligne avec donnees
  const lastRow = sheet.getLastRow();

  // Ajouter une ligne
  sheet.appendRow(["Nouveau", 42, new Date(), "Actif"]);
}
```

### Performance optimization dans Apps Script

```javascript
// MAUVAIS : acces cellule par cellule (tres lent — chaque appel = requete reseau)
function lent() {
  const sheet = SpreadsheetApp.getActiveSheet();
  for (let i = 1; i <= 1000; i++) {
    const val = sheet.getRange(i, 1).getValue();  // 1000 requetes
    sheet.getRange(i, 2).setValue(val * 2);         // 1000 requetes de plus
  }
}

// BON : lecture/ecriture en lot (rapide — 2 requetes seulement)
function rapide() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const data = sheet.getRange(1, 1, 1000, 1).getValues();  // 1 requete
  const output = data.map(row => [row[0] * 2]);
  sheet.getRange(1, 2, 1000, 1).setValues(output);          // 1 requete
}
```

### Differences syntaxiques cles VBA vs Apps Script

| Concept | VBA | Apps Script (JavaScript) |
|---|---|---|
| **Declaration variable** | `Dim x As Long` | `let x = 0` ou `const x = 0` |
| **Boucle For** | `For i = 1 To 10 ... Next i` | `for (let i = 0; i < 10; i++) { }` |
| **Boucle For Each** | `For Each item In collection` | `for (const item of array) { }` ou `.forEach()` |
| **Condition** | `If ... Then ... ElseIf ... End If` | `if (...) { } else if (...) { }` |
| **Fonction** | `Function f(x) As Long` | `function f(x) { return ...; }` |
| **Tableaux** | `Dim arr(1 To 10)` | `const arr = []` |
| **Objets** | `Set ws = ...` | `const sheet = ...` |
| **Erreurs** | `On Error GoTo` | `try { } catch (e) { }` |
| **Output debug** | `Debug.Print` | `Logger.log()` ou `console.log()` |

---

## 5. Apps Script Triggers & Automation

### Types de declencheurs

```javascript
// --- Declencheurs simples (fonctions reservees) ---

// Se declenche a l'ouverture du classeur
function onOpen(e) {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu("Outils personnalises")
    .addItem("Generer rapport", "genererRapport")
    .addItem("Envoyer par email", "envoyerEmail")
    .addSeparator()
    .addItem("Parametres", "ouvrirParametres")
    .addToUi();
}

// Se declenche a chaque modification
function onEdit(e) {
  const range = e.range;
  const sheet = range.getSheet();

  // Si modification dans la colonne Statut de la feuille Taches
  if (sheet.getName() === "Taches" && range.getColumn() === 4) {
    // Ajouter un timestamp dans la colonne E
    const row = range.getRow();
    sheet.getRange(row, 5).setValue(new Date());

    // Si statut = "Termine", colorier la ligne en vert
    if (range.getValue() === "Termine") {
      sheet.getRange(row, 1, 1, 5).setBackground("#d4edda");
    }
  }
}

// --- Declencheurs installes (plus puissants, necessitent autorisation) ---

function creerDeclencheurs() {
  // Declencheur temporel : executer chaque jour a 8h
  ScriptApp.newTrigger("rapportQuotidien")
    .timeBased()
    .everyDays(1)
    .atHour(8)
    .create();

  // Declencheur sur modification (avec acces complet a l'evenement)
  ScriptApp.newTrigger("surModification")
    .forSpreadsheet(SpreadsheetApp.getActive())
    .onChange()
    .create();

  // Declencheur sur soumission de formulaire
  ScriptApp.newTrigger("surReponseFormulaire")
    .forSpreadsheet(SpreadsheetApp.getActive())
    .onFormSubmit()
    .create();
}
```

### Pattern : Rapport automatique quotidien

```javascript
function rapportQuotidien() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheetData = ss.getSheetByName("Ventes");
  const data = sheetData.getDataRange().getValues();

  // Calculer les KPIs
  const aujourdHui = new Date();
  const debutMois = new Date(aujourdHui.getFullYear(), aujourdHui.getMonth(), 1);

  let totalMois = 0;
  let nbVentes = 0;

  for (let i = 1; i < data.length; i++) {
    const dateVente = new Date(data[i][0]);
    if (dateVente >= debutMois) {
      totalMois += data[i][3];
      nbVentes++;
    }
  }

  const moyenne = nbVentes > 0 ? totalMois / nbVentes : 0;

  // Construire l'email
  const sujet = `Rapport Ventes - ${Utilities.formatDate(aujourdHui, "Europe/Paris", "dd/MM/yyyy")}`;
  const corps = `
    <h2>Rapport de ventes quotidien</h2>
    <table border="1" cellpadding="8">
      <tr><td><b>Total du mois</b></td><td>${totalMois.toFixed(2)} EUR</td></tr>
      <tr><td><b>Nombre de ventes</b></td><td>${nbVentes}</td></tr>
      <tr><td><b>Vente moyenne</b></td><td>${moyenne.toFixed(2)} EUR</td></tr>
    </table>
    <p><a href="${ss.getUrl()}">Ouvrir le classeur</a></p>
  `;

  MailApp.sendEmail({
    to: "equipe@example.com",
    subject: sujet,
    htmlBody: corps
  });
}
```

---

## 6. Custom Functions

### Custom Functions en VBA

Les fonctions VBA sont utilisables directement dans les cellules Excel comme des formules natives :

```vba
' Fonction utilisable en cellule : =CalculerTTC(B2, 0.20)
Function CalculerTTC(montantHT As Double, tauxTVA As Double) As Double
    CalculerTTC = montantHT * (1 + tauxTVA)
End Function

' Fonction de nettoyage de texte
Function NettoyerTexte(texte As String) As String
    Dim result As String
    result = Trim(texte)
    result = WorksheetFunction.Clean(result)

    ' Supprimer les espaces multiples
    Do While InStr(result, "  ") > 0
        result = Replace(result, "  ", " ")
    Loop

    NettoyerTexte = result
End Function

' Fonction de validation SIRET (14 chiffres, cle Luhn)
Function ValiderSIRET(siret As String) As Boolean
    If Len(siret) <> 14 Then
        ValiderSIRET = False
        Exit Function
    End If

    If Not siret Like "##############" Then
        ValiderSIRET = False
        Exit Function
    End If

    ' Algorithme de Luhn
    Dim total As Long
    Dim i As Long
    For i = 1 To 14
        Dim digit As Long
        digit = CInt(Mid(siret, i, 1))
        If i Mod 2 = 0 Then
            digit = digit * 2
            If digit > 9 Then digit = digit - 9
        End If
        total = total + digit
    Next i

    ValiderSIRET = (total Mod 10 = 0)
End Function
```

### Custom Functions en Apps Script

```javascript
/**
 * Calcule le montant TTC a partir du HT et du taux de TVA.
 *
 * @param {number} montantHT Le montant hors taxes.
 * @param {number} tauxTVA Le taux de TVA (ex: 0.20 pour 20%).
 * @return {number} Le montant TTC.
 * @customfunction
 */
function CALCULER_TTC(montantHT, tauxTVA) {
  if (typeof montantHT !== "number" || typeof tauxTVA !== "number") {
    throw new Error("Les parametres doivent etre numeriques.");
  }
  return montantHT * (1 + tauxTVA);
}

/**
 * Valide un numero SIRET francais (14 chiffres).
 *
 * @param {string} siret Le numero SIRET a valider.
 * @return {boolean} TRUE si valide, FALSE sinon.
 * @customfunction
 */
function VALIDER_SIRET(siret) {
  siret = String(siret).trim();
  if (siret.length !== 14 || !/^\d{14}$/.test(siret)) return false;

  let total = 0;
  for (let i = 0; i < 14; i++) {
    let digit = parseInt(siret[i]);
    if (i % 2 === 1) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }
    total += digit;
  }
  return total % 10 === 0;
}

/**
 * Extrait le domaine d'une adresse email.
 *
 * @param {string} email L'adresse email.
 * @return {string} Le domaine.
 * @customfunction
 */
function EXTRACT_DOMAIN(email) {
  if (!email || typeof email !== "string") return "";
  const parts = email.split("@");
  return parts.length === 2 ? parts[1] : "Format invalide";
}
```

---

## 7. Integration Patterns

### Pattern 1 — Appel API REST (Apps Script)

```javascript
function importerDonneesAPI() {
  const url = "https://api.example.com/v1/sales";
  const options = {
    method: "get",
    headers: {
      "Authorization": "Bearer " + PropertiesService.getScriptProperties().getProperty("API_KEY"),
      "Content-Type": "application/json"
    },
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(url, options);

  if (response.getResponseCode() !== 200) {
    Logger.log("Erreur API : " + response.getResponseCode());
    return;
  }

  const data = JSON.parse(response.getContentText());

  // Ecrire dans le classeur
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("API_Data");
  sheet.clear();

  // En-tetes
  const headers = Object.keys(data[0]);
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Donnees
  const rows = data.map(item => headers.map(h => item[h]));
  sheet.getRange(2, 1, rows.length, headers.length).setValues(rows);

  Logger.log(rows.length + " enregistrements importes.");
}
```

### Pattern 2 — Appel API REST (VBA)

```vba
Sub ImporterDonneesAPI()
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")

    Dim url As String
    url = "https://api.example.com/v1/sales"

    http.Open "GET", url, False
    http.setRequestHeader "Authorization", "Bearer " & Range("param_ApiKey").Value
    http.setRequestHeader "Content-Type", "application/json"
    http.Send

    If http.Status <> 200 Then
        MsgBox "Erreur API : " & http.Status & " - " & http.statusText
        Exit Sub
    End If

    ' Parser le JSON (necessite une bibliotheque JSON — ex: VBA-JSON)
    Dim json As Object
    Set json = JsonConverter.ParseJson(http.responseText)

    ' Ecrire les donnees
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("API_Data")
    ws.Cells.Clear

    Dim row As Long
    row = 2

    Dim item As Object
    For Each item In json
        ws.Cells(row, 1).Value = item("id")
        ws.Cells(row, 2).Value = item("date")
        ws.Cells(row, 3).Value = item("amount")
        row = row + 1
    Next item

    MsgBox (row - 2) & " enregistrements importes."
End Sub
```

### Pattern 3 — Email automation (Apps Script)

```javascript
function envoyerRappels() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Factures");
  const data = sheet.getDataRange().getValues();
  const aujourdHui = new Date();

  let nbEnvoyes = 0;

  for (let i = 1; i < data.length; i++) {
    const email = data[i][1];         // Colonne B : email
    const echeance = new Date(data[i][3]); // Colonne D : date echeance
    const statut = data[i][4];        // Colonne E : statut
    const montant = data[i][2];       // Colonne C : montant

    // Envoyer un rappel si echeance depassee et non payee
    if (statut !== "Paye" && echeance < aujourdHui) {
      const joursRetard = Math.floor((aujourdHui - echeance) / (1000 * 60 * 60 * 24));

      MailApp.sendEmail({
        to: email,
        subject: `Rappel facture - ${joursRetard} jours de retard`,
        htmlBody: `
          <p>Bonjour,</p>
          <p>Nous vous rappelons que votre facture de <b>${montant.toFixed(2)} EUR</b>
          est en retard de <b>${joursRetard} jours</b>.</p>
          <p>Merci de proceder au reglement dans les plus brefs delais.</p>
        `
      });

      // Marquer comme rappele
      sheet.getRange(i + 1, 6).setValue(new Date());
      sheet.getRange(i + 1, 7).setValue("Rappel envoye");
      nbEnvoyes++;
    }
  }

  Logger.log(nbEnvoyes + " rappels envoyes.");
}
```

### Pattern 4 — Integration Google Drive (Apps Script)

```javascript
function exporterVersGoogleDrive() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("Rapport");

  // Creer un PDF du classeur
  const pdfBlob = ss.getAs("application/pdf");
  pdfBlob.setName("Rapport_" + Utilities.formatDate(new Date(), "Europe/Paris", "yyyy-MM-dd") + ".pdf");

  // Sauvegarder dans un dossier Drive
  const folderId = "1AbC_dEfG_HIjKlMnOpQrStUv";  // ID du dossier Drive
  const folder = DriveApp.getFolderById(folderId);
  const file = folder.createFile(pdfBlob);

  Logger.log("PDF cree : " + file.getUrl());

  // Partager avec des destinataires
  file.addEditor("collegue@example.com");
  file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
}
```

### Pattern 5 — Connexion base de donnees (VBA via ADODB)

```vba
Sub ImporterDepuisSQL()
    Dim conn As Object
    Set conn = CreateObject("ADODB.Connection")

    Dim connStr As String
    connStr = "Driver={SQL Server};Server=monserveur;Database=mabase;Trusted_Connection=Yes;"

    conn.Open connStr

    Dim rs As Object
    Set rs = CreateObject("ADODB.Recordset")

    Dim sql As String
    sql = "SELECT ClientID, Nom, CA_Total FROM dbo.Clients WHERE CA_Total > 10000 ORDER BY CA_Total DESC"

    rs.Open sql, conn

    ' Ecrire les donnees dans Excel
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("SQL_Import")
    ws.Cells.Clear

    ' En-tetes
    Dim col As Long
    For col = 0 To rs.Fields.Count - 1
        ws.Cells(1, col + 1).Value = rs.Fields(col).Name
    Next col

    ' Donnees — CopyFromRecordset est extremement rapide
    ws.Range("A2").CopyFromRecordset rs

    rs.Close
    conn.Close

    MsgBox "Import termine."
End Sub
```

---

## 8. Security Considerations

### Securite VBA

| Risque | Mitigation |
|---|---|
| **Macros malveillantes** | Activer la signature numerique des macros. Configurer le Trust Center pour n'autoriser que les macros signees |
| **Mots de passe en clair** | Ne JAMAIS stocker de mots de passe ou cles API dans le code VBA. Utiliser des variables d'environnement ou le Credential Manager Windows |
| **Injection SQL** | Utiliser des requetes parametrees (ADODB.Command avec Parameters), jamais la concatenation directe |
| **Acces fichiers** | Valider les chemins de fichiers. Limiter les operations aux dossiers autorises |
| **Code VBA visible** | Proteger le projet VBA par mot de passe (protection faible — ne pas compter dessus pour la securite reelle) |

### Securite Apps Script

| Risque | Mitigation |
|---|---|
| **Permissions excessives** | Declarer le minimum de scopes OAuth dans appsscript.json. Reviser les permissions avant publication |
| **Cles API exposees** | Stocker les cles dans PropertiesService (Script Properties), jamais en dur dans le code |
| **Donnees sensibles** | Chiffrer les donnees sensibles. Utiliser les labels de classification Google Drive |
| **Triggers non surveilles** | Auditer les triggers installes regulierement (`ScriptApp.getProjectTriggers()`) |
| **Partage de scripts** | Utiliser des bibliotheques Apps Script pour le code partage, avec controle d'acces |

### Bonnes pratiques communes

1. **Option Explicit (VBA) / Strict mode** : Toujours activer pour eviter les erreurs de frappe dans les noms de variables
2. **Validation des entrees** : Valider tout input utilisateur (formulaires, parametres, donnees importees)
3. **Journalisation** : Logger les operations sensibles (exports, envois d'emails, modifications en masse)
4. **Sauvegarde** : Versionner le code (Git pour Apps Script via clasp, sauvegarde manuelle pour VBA)
5. **Revue de code** : Faire relire les macros par un pair avant deploiement en production

---

## 9. Migration VBA ↔ Apps Script

### Strategie de migration

```
Phase 1 : Inventaire
├── Lister toutes les macros VBA (modules, classes, forms)
├── Classifier par complexite (simple, moyenne, complexe)
├── Identifier les dependances (COM, fichiers locaux, ADODB)
└── Evaluer la faisabilite de migration pour chaque macro

Phase 2 : Mapping des equivalences
├── Objets Excel → Services Google Sheets
├── FileSystemObject → DriveApp
├── Outlook → GmailApp / MailApp
├── ADODB → JDBC / UrlFetchApp
├── UserForms → HTML Service (sidebars, dialogs)
└── COM/ActiveX → APIs REST via UrlFetchApp

Phase 3 : Migration par priorite
├── Migrer d'abord les macros simples (formules custom, formatage)
├── Puis les macros d'integration (email, fichiers)
├── Enfin les macros complexes (UserForms, bases de donnees)
└── Certaines macros ne sont pas migrables (COM, fichiers locaux specifiques)
```

### Table de correspondance

| VBA | Apps Script | Notes |
|---|---|---|
| `ThisWorkbook` | `SpreadsheetApp.getActiveSpreadsheet()` | |
| `Worksheets("Nom")` | `ss.getSheetByName("Nom")` | |
| `Range("A1").Value` | `sheet.getRange("A1").getValue()` | Appels reseau, minimiser |
| `Cells(r, c)` | `sheet.getRange(r, c)` | Indexation 1-based dans les deux cas |
| `MsgBox` | `SpreadsheetApp.getUi().alert()` | ou `Browser.msgBox()` |
| `InputBox` | `SpreadsheetApp.getUi().prompt()` | |
| `Application.FileDialog` | `DriveApp.getFileById()` ou HTML picker | Pas d'acces au systeme de fichiers local |
| `Debug.Print` | `Logger.log()` ou `console.log()` | |
| `Timer` | `new Date().getTime()` | Pour mesurer les performances |
| `CreateObject("MSXML2.XMLHTTP")` | `UrlFetchApp.fetch()` | Plus simple dans Apps Script |
| `ADODB.Connection` | `Jdbc.getConnection()` | Pour Google Cloud SQL |
| `UserForm` | `HtmlService.createHtmlOutput()` | Affiche un sidebar ou dialog |

### Limitations de la migration

- **Pas d'acces au systeme de fichiers local** : Apps Script fonctionne dans le cloud. Les operations sur des fichiers locaux necessitent Google Drive
- **Pas de COM/ActiveX** : Les objets COM (Outlook, Word, SAP) ne sont pas disponibles. Utiliser les APIs Google ou des APIs REST equivalentes
- **Quota de temps d'execution** : Apps Script a une limite de 6 minutes par execution (30 minutes pour Google Workspace). Les macros VBA longues doivent etre decoupees
- **Latence reseau** : Chaque appel `getValue/setValue` est un appel reseau. Optimiser en utilisant `getValues/setValues` en lot
- **UserForms** : Les UserForms VBA doivent etre recreees en HTML/CSS/JavaScript avec le HTML Service. C'est souvent la partie la plus couteuse de la migration

---

## 10. Advanced Automation Patterns

### Pattern : Traitement conditionnel par lot (VBA)

```vba
Sub TraitementParLot()
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual

    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("Donnees")

    Dim tbl As ListObject
    Set tbl = ws.ListObjects("tbl_Commandes")

    Dim nbTraitees As Long
    Dim nbErreurs As Long

    Dim row As ListRow
    For Each row In tbl.ListRows
        On Error Resume Next

        Dim statut As String
        statut = row.Range.Cells(1, tbl.ListColumns("Statut").Index).Value

        If statut = "En attente" Then
            ' Traiter la commande
            Dim montant As Double
            montant = row.Range.Cells(1, tbl.ListColumns("Montant").Index).Value

            ' Appliquer la logique metier
            If montant > 0 Then
                row.Range.Cells(1, tbl.ListColumns("Statut").Index).Value = "Traitee"
                row.Range.Cells(1, tbl.ListColumns("Date_Traitement").Index).Value = Now()
                nbTraitees = nbTraitees + 1
            End If
        End If

        If Err.Number <> 0 Then
            nbErreurs = nbErreurs + 1
            Call LogError(Err.Number, Err.Description, "TraitementParLot - Ligne " & row.Index)
            Err.Clear
        End If

        On Error GoTo 0
    Next row

    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic

    MsgBox "Traitement termine." & vbCrLf & _
           "Traitees : " & nbTraitees & vbCrLf & _
           "Erreurs : " & nbErreurs
End Sub
```

### Pattern : Workflow multi-etapes (Apps Script)

```javascript
function workflowComplet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  try {
    // Etape 1 : Importer les donnees
    Logger.log("Etape 1 : Import des donnees...");
    importerDonneesAPI();

    // Etape 2 : Nettoyer et transformer
    Logger.log("Etape 2 : Nettoyage...");
    nettoyerDonnees();

    // Etape 3 : Calculer les KPIs
    Logger.log("Etape 3 : Calcul des KPIs...");
    calculerKPIs();

    // Etape 4 : Generer le rapport
    Logger.log("Etape 4 : Generation du rapport...");
    genererRapport();

    // Etape 5 : Envoyer par email
    Logger.log("Etape 5 : Envoi par email...");
    envoyerRapport();

    // Etape 6 : Archiver
    Logger.log("Etape 6 : Archivage...");
    archiverVersGoogleDrive();

    Logger.log("Workflow termine avec succes.");

  } catch (error) {
    Logger.log("ERREUR dans le workflow : " + error.message);

    // Notification d'erreur
    MailApp.sendEmail({
      to: "admin@example.com",
      subject: "ERREUR - Workflow Excel automatise",
      body: "Erreur : " + error.message + "\n\nStack : " + error.stack
    });
  }
}
```

### Pattern : Generation de documents (Apps Script + Google Docs)

```javascript
function genererContrats() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Clients");
  const data = sheet.getDataRange().getValues();
  const templateId = "1AbCdEfGhIjKlMnOpQrStUvWxYz";  // ID du template Google Docs

  for (let i = 1; i < data.length; i++) {
    const client = {
      nom: data[i][0],
      adresse: data[i][1],
      montant: data[i][2],
      date: Utilities.formatDate(new Date(), "Europe/Paris", "dd/MM/yyyy")
    };

    // Copier le template
    const copie = DriveApp.getFileById(templateId).makeCopy(
      `Contrat_${client.nom}_${client.date}`
    );

    // Ouvrir et remplacer les placeholders
    const doc = DocumentApp.openById(copie.getId());
    const body = doc.getBody();

    body.replaceText("{{NOM}}", client.nom);
    body.replaceText("{{ADRESSE}}", client.adresse);
    body.replaceText("{{MONTANT}}", client.montant.toFixed(2));
    body.replaceText("{{DATE}}", client.date);

    doc.saveAndClose();

    // Convertir en PDF
    const pdf = copie.getAs("application/pdf");
    const dossierOutput = DriveApp.getFolderById("folder_id_here");
    dossierOutput.createFile(pdf);

    Logger.log("Contrat genere pour : " + client.nom);
  }
}
```
