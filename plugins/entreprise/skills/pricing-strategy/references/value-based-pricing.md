# Pricing Value-Based -- Methodologie et Mise en Oeuvre

## Overview

Ce document de reference couvre la methodologie du pricing value-based : de la quantification de la valeur creee pour le client a la segmentation par willingness-to-pay, jusqu'a la fixation du prix optimal. Il presente les outils de mesure les plus robustes (Van Westendorp, Conjoint Analysis, Gabor-Granger), leur implementation pratique, et fournit du code Python operationnel pour analyser les donnees de willingness-to-pay. Utiliser ce guide chaque fois qu'une reflexion tarifaire doit etre ancree dans la valeur creee plutot que dans les couts ou la concurrence.

---

## Key Concepts

### Le Paradigme Value-Based vs les Approches Traditionnelles

Trois philosophies de pricing coexistent. Comprendre leurs differences fondamentales avant de choisir.

**Cost-plus pricing** : Prix = Cout de revient + Marge cible. Simple a calculer, mais ignore totalement la valeur percue par le client. Mene systematiquement a du money left on the table quand la valeur creee est elevee, et a des pertes de competitivite quand les couts sont eleves.

**Competitive pricing** : Prix = Prix concurrent +/- ecart positionnel. Utile comme reference externe, mais creer une course vers le bas dans les marches commoditises. Suppose implicitement que le concurrent a raison -- ce qui est rarement justifie.

**Value-based pricing** : Prix = Valeur creee pour le client x Fraction capturee. Necessite de comprendre en profondeur ce que le client gagne grace au produit (economie de temps, reduction de risque, augmentation du chiffre d'affaires, reduction de couts). Complexe a implementer, mais seule approche qui maximise durablement la marge et aligne le prix sur la proposition de valeur.

La grande majorite des entreprises pratique du cost-plus ou du competitive pricing par defaut. Le passage au value-based est un changement culturel, pas seulement un changement de methode.

### Economic Value to Customer (EVC)

L'EVC est la formule centrale du value-based pricing. Elle quantifie le prix maximum qu'un client rationnel devrait accepter de payer.

**Formule EVC** :

```
EVC = Prix de reference + Valeur differentielle positive - Valeur differentielle negative
```

Ou :

- **Prix de reference** : prix de la meilleure alternative disponible pour le client (concurrent, solution interne, statu quo).
- **Valeur differentielle positive** : gains supplementaires apportes par votre solution vs l'alternative (productivite, revenus, qualite, conformite).
- **Valeur differentielle negative** : surcouts ou desavantages de votre solution vs l'alternative (cout d'implementation, courbe d'apprentissage, risque de migration).

**Extension avec valeur emotionnelle** :

```
EVC etendu = Prix de reference + Valeur differentielle fonctionnelle + Valeur emotionnelle/strategique
```

La valeur emotionnelle ou strategique inclut : la reduction d'anxiete (SLA garanti, certifications securite), le statut (etre client d'un leader reconnu), la flexibilite strategique (ne pas etre lock-in). Cette composante est souvent ignoree mais peut representer 20-40% de l'EVC total en B2B.

**Regle de partage de la valeur** : capturer entre 10% et 50% de l'EVC. En dessous de 10%, le produit est sous-tarifie. Au-dessus de 50%, le client a l'impression d'etre exploite et cherche des alternatives. Le sweet spot est autour de 20-30% pour la plupart des marches B2B.

---

## Frameworks & Methods

### Van Westendorp Price Sensitivity Meter (PSM)

La methode Van Westendorp est le standard pour mesurer la willingness-to-pay sans exposer le client a des prix specifiques. Elle repose sur 4 questions posees dans un survey.

#### Les 4 Questions Exactes

Poser ces questions dans cet ordre, en montrant le produit mais sans mentionner de prix :

1. **Trop cher** : "A quel prix ce produit/service vous semblerait-il trop cher, au point que vous refuseriez de l'acheter ?"
2. **Cher mais acceptable** : "A quel prix ce produit/service vous semblerait-il cher, mais vous l'acheteriez quand meme ?"
3. **Bon marche** : "A quel prix ce produit/service vous semblerait-il bon marche, une bonne affaire ?"
4. **Trop bon marche** : "A quel prix ce produit/service vous semblerait-il si bon marche que vous douteriez de sa qualite ?"

#### Construction des Courbes PSM

Pour chaque prix sur l'axe X, calculer le pourcentage cumulatif de repondants qui ont cite ce prix ou moins pour chaque question. Inverser les courbes "trop cher" et "cher mais acceptable" (100% - cumul).

Les 4 courbes resultantes se croisent en des points specifiques :

| Point | Definition | Signification |
|---|---|---|
| **PMC** Point of Marginal Cheapness | Intersection "trop bon marche" et "bon marche" | Prix en-dessous duquel la qualite est percue comme douteuse |
| **PME** Point of Marginal Expensiveness | Intersection "trop cher" et "cher mais acceptable" | Prix au-dessus duquel l'achat devient rare |
| **OPP** Optimal Price Point | Intersection "trop cher" et "trop bon marche" | Prix avec le moins de rejet |
| **IDP** Indifference Price Point | Intersection "bon marche" et "cher mais acceptable" | Prix "normal" percu par le marche |

**Acceptable Price Range (APR)** : la plage entre PMC et PME. Le prix optimal se situe dans cet intervalle.

#### Taille d'Echantillon et Conditions

Minimum 50 repondants pour un signal statistique valide. Recommande : 100-200 pour segmenter par profil. Les repondants doivent etre des acheteurs potentiels reels ou des utilisateurs du produit -- pas des personnes sans lien avec le besoin adresse. Eviter les biais de desirabilite en posant les questions de facon neutre.

### Conjoint Analysis

La conjoint analysis mesure les trade-offs que les clients font entre les attributs du produit, dont le prix. Elle est plus sophistiquee que le Van Westendorp car elle capture les preferences dans un contexte de choix reel.

**Full-profile conjoint** : le repondant note ou classe des profils de produits complets (combinaison de plusieurs attributs). Approprie pour 4-6 attributs maximum. Au-dela, la charge cognitive devient trop elevee.

**Choice-Based Conjoint (CBC)** : le repondant choisit entre 2-4 options a chaque question (comme un vrai acte d'achat). Plus realiste, plus robuste statistiquement. Necessite un logiciel dedie (Qualtrics, Sawtooth, conjoint.ly).

**Resultats utiles de la conjoint** :
- Part-worth utilities : la valeur relative de chaque niveau de chaque attribut.
- Relative importance : quelle proportion de la decision d'achat est expliquee par le prix vs les autres attributs.
- Willingness-to-pay par attribut : combien le client paie en plus pour chaque feature.
- Market share simulation : simuler l'impact d'un changement de prix sur la part de marche.

### Gabor-Granger

La methode Gabor-Granger presente directement differents prix et demande l'intention d'achat a chaque niveau. Simple, rapide, mais biaisee par l'effet d'ancrage si les prix sont presentes dans l'ordre croissant.

**Protocol correct** : presenter les prix dans un ordre aleatoire, pas croissant. Utiliser une echelle d'intention : "Definitivement oui / Probablement oui / Probablement non / Definitivement non". Combiner "Definitivement oui" et "Probablement oui" pour calculer la probabilite d'achat a chaque prix.

**Courbe de demande Gabor-Granger** : tracer la probabilite d'achat en fonction du prix. Le prix optimal est celui qui maximise le revenu attendu = Prix x Probabilite d'achat.

---

## Tools & Implementation

### Code Python -- Analyse Van Westendorp

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyse_van_westendorp(df):
    """
    df doit contenir 4 colonnes :
    - 'trop_cher' : prix Q1 (trop cher pour acheter)
    - 'cher_acceptable' : prix Q2 (cher mais acceptable)
    - 'bon_marche' : prix Q3 (bonne affaire)
    - 'trop_bon_marche' : prix Q4 (trop bon marche, qualite douteuse)
    """
    # Definir l'axe des prix
    prix_min = df[['trop_cher', 'cher_acceptable', 'bon_marche', 'trop_bon_marche']].min().min()
    prix_max = df[['trop_cher', 'cher_acceptable', 'bon_marche', 'trop_bon_marche']].max().max()
    prix_range = np.arange(prix_min, prix_max + 1, 1)

    n = len(df)
    resultats = pd.DataFrame({'prix': prix_range})

    # Calcul des pourcentages cumulatifs
    resultats['pct_trop_cher'] = [100 - (df['trop_cher'] <= p).sum() / n * 100 for p in prix_range]
    resultats['pct_cher_acceptable'] = [100 - (df['cher_acceptable'] <= p).sum() / n * 100 for p in prix_range]
    resultats['pct_bon_marche'] = [(df['bon_marche'] <= p).sum() / n * 100 for p in prix_range]
    resultats['pct_trop_bon_marche'] = [(df['trop_bon_marche'] <= p).sum() / n * 100 for p in prix_range]

    # Identification des points cles
    def trouver_intersection(y1, y2, x):
        diff = np.abs(np.array(y1) - np.array(y2))
        idx = np.argmin(diff)
        return x[idx]

    OPP = trouver_intersection(
        resultats['pct_trop_cher'], resultats['pct_trop_bon_marche'], prix_range
    )
    IDP = trouver_intersection(
        resultats['pct_bon_marche'], resultats['pct_cher_acceptable'], prix_range
    )
    PMC = trouver_intersection(
        resultats['pct_trop_bon_marche'], resultats['pct_bon_marche'], prix_range
    )
    PME = trouver_intersection(
        resultats['pct_trop_cher'], resultats['pct_cher_acceptable'], prix_range
    )

    # Trace des courbes
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(prix_range, resultats['pct_trop_cher'], label='Trop cher', color='red', linewidth=2)
    ax.plot(prix_range, resultats['pct_cher_acceptable'], label='Cher mais acceptable', color='orange', linewidth=2)
    ax.plot(prix_range, resultats['pct_bon_marche'], label='Bon marche', color='green', linewidth=2)
    ax.plot(prix_range, resultats['pct_trop_bon_marche'], label='Trop bon marche', color='blue', linewidth=2)

    for point, label, color in [(PMC, f'PMC: {PMC}', 'blue'),
                                 (PME, f'PME: {PME}', 'red'),
                                 (OPP, f'OPP: {OPP}', 'purple'),
                                 (IDP, f'IDP: {IDP}', 'green')]:
        ax.axvline(x=point, color=color, linestyle='--', alpha=0.7)
        ax.annotate(label, xy=(point, 50), fontsize=9, color=color,
                    xytext=(point + 2, 55))

    ax.set_xlabel('Prix (EUR/mois)')
    ax.set_ylabel('% de repondants')
    ax.set_title('Van Westendorp Price Sensitivity Meter')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('van_westendorp_psm.png', dpi=150)
    plt.show()

    return {
        'OPP': OPP, 'IDP': IDP, 'PMC': PMC, 'PME': PME,
        'acceptable_price_range': (PMC, PME),
        'recommandation': f"Prix optimal entre {PMC} et {PME} EUR/mois. OPP a {OPP} EUR/mois."
    }

# Exemple d'utilisation avec donnees simulees
np.random.seed(42)
n_repondants = 120
donnees = pd.DataFrame({
    'trop_cher':        np.random.normal(350, 80, n_repondants).clip(100, 700).astype(int),
    'cher_acceptable':  np.random.normal(250, 60, n_repondants).clip(80, 500).astype(int),
    'bon_marche':       np.random.normal(150, 40, n_repondants).clip(50, 300).astype(int),
    'trop_bon_marche':  np.random.normal(80,  30, n_repondants).clip(20, 200).astype(int),
})
resultats = analyse_van_westendorp(donnees)
print(resultats)
```

### Segmentation Value-Based et Personas Pricing

Identifier les segments en fonction de leur willingness-to-pay, pas uniquement de leur taille ou secteur. Trois dimensions de segmentation a croiser :

**Intensite d'usage** : les gros utilisateurs ont generalement un EVC plus eleve car ils capturent plus de valeur. Concevoir des metriques de valeur qui capturent cette intensite (nombre de transactions, volume de donnees, nombre d'utilisateurs actifs).

**Profil de douleur** : quel probleme specifique le produit resout-il pour ce segment ? La meme fonctionnalite a un EVC different pour une PME (gain de temps) et un grand compte (reduction de risque de conformite).

**Sophistication de l'acheteur** : un acheteur technique comprend mieux la valeur fonctionnelle (ROI mesurable). Un acheteur business valorise davantage la reduction de risque et la valeur strategique. Adapter le message et la justification du prix en consequence.

### Cas B2B -- ROI Selling et Value Calculator

En B2B, le price justification passe par la demonstration du ROI. Construire un Value Calculator : un tableur ou outil interactif que le commercial partage avec le prospect pour quantifier la valeur ensemble.

**Template Value Calculator B2B** :

| Categorie | Indicateur | Valeur actuelle | Avec la solution | Gain annuel |
|---|---|---|---|---|
| Productivite | Heures/semaine sur tache X | 10h | 2h | 8h x salaire x 52 semaines |
| Erreurs/retraitement | Taux d'erreur actuel | 5% | 0.5% | Cout de correction x volume |
| Revenus | Taux de conversion | 2.1% | 2.8% | Delta x volume x panier moyen |
| Conformite | Amendes potentielles | 50 000 EUR/an | 0 EUR | 50 000 EUR |
| **Total valeur annuelle** | | | | **XXX EUR** |
| **Prix solution** | | | | **YYY EUR** |
| **ROI** | | | | **(XXX - YYY) / YYY x 100%** |
| **Payback period** | | | | **YYY / (XXX/12) mois** |

### Exemple Concret -- EVC Complet SaaS B2B

**Contexte** : SaaS de gestion des notes de frais pour entreprises de 200-500 salaries. Alternative principale : processus manuel (tableur Excel + validations email).

**Calcul EVC** :

- Prix de reference : 0 EUR/mois (solution interne Excel, cout cache non conscient)
- Valeur differentielle positive :
  - Temps comptable economise : 20h/mois x 45 EUR/h = 900 EUR/mois
  - Reduction des erreurs de remboursement : 2% de 50 000 EUR/mois de notes = 1 000 EUR/mois
  - Gain du salarie sur soumission : 15 min/note x 100 notes/mois x 30 EUR/h = 750 EUR/mois
  - Conformite TVA recuperee : +1.5% sur 50 000 EUR = 750 EUR/mois
  - Total valeur differentielle positive : **3 400 EUR/mois**
- Valeur emotionnelle/strategique :
  - Reduction du stress audit : non quantifie mais reel pour le CFO
  - Satisfaction employee : ++ (remboursements en 48h vs 3 semaines)
  - Estimation valeur emotionnelle : 300-500 EUR/mois
- Valeur differentielle negative :
  - Implementation et migration : 2 000 EUR one-time soit ~170 EUR/mois sur 12 mois
  - Formation equipe : 500 EUR one-time soit ~42 EUR/mois
  - Total valeur differentielle negative : **~212 EUR/mois**

**EVC = 0 + 3 400 + 400 - 212 = 3 588 EUR/mois**

**Prix optimal (20-30% de l'EVC)** : 718 - 1 077 EUR/mois

**Prix de marche constate** : 3-8 EUR/utilisateur/mois, soit pour 300 utilisateurs : 900 - 2 400 EUR/mois. Le haut de fourchette (8 EUR/utilisateur) capture environ 22% de l'EVC -- coherent avec la theorie.

**Lecon** : la plupart des editeurs de ce segment se positionnent a 3-4 EUR/utilisateur par peur du marche, alors que leur EVC justifierait 8-10 EUR. Le value-based pricing revele le gap de sous-tarification.

---

## Common Mistakes

**Confondre prix optimal et prix maximum** : l'OPP du Van Westendorp n'est pas le prix auquel il faut se fixer, c'est le centre de gravite perceptuel. Ajuster selon les objectifs de volume vs marge.

**Ignorer les segments dans le PSM** : un PSM agrege cache des segments tres differents. Segmenter systematiquement : petites vs grandes entreprises, early adopters vs mainstream, usage intensif vs occasionnel.

**Calculer l'EVC sans valider avec les clients** : l'EVC theorique est un point de depart, pas une verite. Valider les hypotheses de valeur avec des entretiens clients et des donnees d'usage reelles.

**Fixer le prix une seule fois** : le pricing est un processus continu. Revoir l'EVC et le Van Westendorp au minimum tous les 12-18 mois, et a chaque lancement de feature majeure ou changement de marche.

**Negliger le prix de reference** : si le client n'a pas de solution actuelle, le prix de reference est 0 et l'EVC est construit uniquement sur la valeur differentielle. Dans ce cas, l'education du marche sur la valeur est prioritaire avant la fixation du prix.
