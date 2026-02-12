# Explainability & Transparency -- XAI Methods, Model Cards & Regulatory Compliance

Reference complete sur l'explicabilite et la transparence des systemes d'IA. Couvre les methodes d'IA explicable (XAI), l'interpretabilite intrinseque et post-hoc, les standards de documentation (model cards, datasheets for datasets), les exigences reglementaires (RGPD article 22, EU AI Act), et les bonnes pratiques de communication transparente. Ce document sert de guide operationnel pour les equipes techniques, les responsables de gouvernance et les equipes juridiques.

---

## Fondements de l'Explicabilite

### Interpretabilite vs Explicabilite

Distinguer ces deux concepts souvent confondus :

- **Interpretabilite (Interpretability)** : Capacite d'un humain a comprendre le mecanisme interne du modele. Un modele est interpretable quand sa structure est suffisamment simple pour etre comprise directement (regression lineaire, arbre de decision, regles logiques). L'interpretabilite est une propriete intrinseque du modele.

- **Explicabilite (Explainability)** : Capacite a fournir des explications comprehensibles des predictions d'un modele, independamment de sa complexite interne. Un modele black-box (deep learning, ensemble) peut etre rendu explicable via des methodes post-hoc (SHAP, LIME). L'explicabilite est un processus applique au modele.

- **Transparence (Transparency)** : Concept plus large englobant l'interpretabilite, l'explicabilite, et la documentation complete du systeme (donnees, choix de conception, limites, conditions d'utilisation). La transparence est une propriete du systeme sociotechnique dans son ensemble.

### Spectre d'interpretabilite des modeles

| Modele | Interpretabilite | Quand privilegier |
|---|---|---|
| **Regles logiques / Systemes experts** | Maximale | Reglementation stricte, audit obligatoire |
| **Regression lineaire / logistique** | Tres elevee | Decisions financieres regulees, sante |
| **Arbre de decision (profondeur limitee)** | Elevee | Decisions operationnelles, explicabilite client |
| **GAM (Generalized Additive Models)** | Elevee | Compromis performance-interpretabilite |
| **EBM (Explainable Boosting Machine)** | Elevee | Alternative performante aux modeles boite noire |
| **Random Forest** | Moyenne | Feature importance disponible, pas d'explication locale |
| **Gradient Boosting (XGBoost, LightGBM)** | Faible | Haute performance, necessite SHAP/LIME |
| **Reseaux de neurones profonds** | Tres faible | Taches complexes (vision, NLP), necessite XAI |
| **LLMs (GPT, Claude, Llama)** | Minimale | Generation de texte, raisonnement, necessite des guardrails |

### Quand privilegier l'interpretabilite intrinseque

Privilegier un modele intrinsequement interpretable dans ces situations :

- **Decisions a fort impact sur les individus** : credit, sante, justice, emploi. Le droit a l'explication (RGPD article 22) impose de pouvoir expliquer la logique de la decision.
- **Domaines ou la confiance est critique** : medecine, aviation, nucleaire. Les experts doivent pouvoir valider le raisonnement du modele.
- **Exigences reglementaires** : le EU AI Act classe certains usages comme "haut risque" avec des obligations de transparence renforcees.
- **Debugging et amelioration** : les modeles interpretables sont plus faciles a debugger et a ameliorer iterativement.

Recommandation : toujours commencer par un modele interpretable comme baseline. Ne passer a un modele complexe que si le gain de performance est significatif (> 2-3 points de metrique metier) et justifie le cout additionnel en explicabilite.

---

## Methodes XAI Post-hoc

### SHAP (SHapley Additive exPlanations)

SHAP est la methode XAI la plus rigoureuse theoriquement. Elle repose sur les valeurs de Shapley issues de la theorie des jeux cooperatifs.

#### Fondements theoriques

La valeur de Shapley d'une feature i mesure sa contribution marginale moyenne a la prediction, en considerant toutes les coalitions possibles de features :

```
phi_i = sum over S subset of N\{i} [ |S|!(|N|-|S|-1)! / |N|! * (v(S union {i}) - v(S)) ]

Ou :
- N est l'ensemble de toutes les features
- S est un sous-ensemble de features ne contenant pas i
- v(S) est la prediction du modele avec les features de S
- phi_i est la contribution de la feature i
```

Proprietes mathematiques garanties (axiomes de Shapley) :

- **Efficiency** : la somme des valeurs SHAP egalise la difference entre la prediction et la valeur de base (prediction moyenne).
- **Symmetry** : deux features avec la meme contribution recoivent la meme valeur SHAP.
- **Dummy** : une feature sans contribution a une valeur SHAP de zero.
- **Additivity** : pour un ensemble de modeles, les valeurs SHAP sont additives.

#### Variantes de SHAP

| Variante | Modeles cibles | Complexite | Precision |
|---|---|---|---|
| **KernelSHAP** | Tout modele (model-agnostic) | O(2^M) approxime par sampling | Approximation, variance |
| **TreeSHAP** | Tree-based (XGBoost, RF, LightGBM) | O(TLD^2) polynomial | Exacte |
| **DeepSHAP** | Reseaux de neurones (PyTorch, TF) | O(forward pass) | Approximation (DeepLIFT) |
| **LinearSHAP** | Modeles lineaires | O(M) lineaire | Exacte |
| **PartitionSHAP** | Tout modele, features groupees | Hierarchique | Approximation |
| **GPUTreeSHAP** | Tree-based sur GPU | Accelere GPU | Exacte |

#### Implementation pratique SHAP

```python
import shap

# TreeSHAP pour un modele XGBoost
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Explications globales
shap.summary_plot(shap_values, X_test)                    # Bee swarm plot
shap.summary_plot(shap_values, X_test, plot_type="bar")   # Feature importance globale

# Explication locale d'une prediction specifique
shap.waterfall_plot(shap.Explanation(
    values=shap_values[idx],
    base_values=explainer.expected_value,
    data=X_test.iloc[idx],
    feature_names=X_test.columns
))

# Dependence plot (relation feature-SHAP value)
shap.dependence_plot("feature_name", shap_values, X_test)

# SHAP interaction values (pour detecter les interactions entre features)
shap_interaction = explainer.shap_interaction_values(X_test)
shap.summary_plot(shap_interaction, X_test)
```

#### Limites et precautions d'usage de SHAP

- **Correlations entre features** : Quand les features sont correlees, les valeurs SHAP peuvent etre trompeuses. KernelSHAP conditionne sur des distributions marginales (pas conditionnelles), ce qui peut creer des echantillons irrealistes. Preferer TreeSHAP (qui utilise les distributions conditionnelles) ou utiliser shap.maskers.Partition pour grouper les features correlees.
- **Cout computationnel** : KernelSHAP est exponentiel en nombre de features. Pour les grands datasets, utiliser le sampling ou les variantes optimisees. Pour les modeles deep learning, DeepSHAP est une approximation rapide mais moins precise.
- **Interpretation causale** : Les valeurs SHAP mesurent des contributions, pas des effets causaux. Une feature avec une valeur SHAP elevee peut etre un proxy correle plutot qu'une cause. Ne pas communiquer les SHAP values comme des explications causales sans verification.
- **Stabilite** : KernelSHAP est stochastique ; les explications varient entre les executions. Utiliser un nombre suffisant d'echantillons (nsamples >= 2 * n_features + 2048) et fixer la seed pour la reproductibilite.

### LIME (Local Interpretable Model-agnostic Explanations)

LIME genere des explications locales en approximant le modele complexe par un modele simple (lineaire) dans le voisinage de la prediction a expliquer.

#### Algorithme

```
1. Selectionner l'instance x a expliquer.
2. Generer des perturbations z autour de x (echantillonnage local).
3. Obtenir les predictions du modele f(z) pour chaque perturbation.
4. Ponderer les perturbations par leur proximite a x (kernel exponential).
5. Entrainer un modele interpretable g (regression lineaire, arbre)
   sur les perturbations ponderees.
6. Les coefficients de g sont les explications locales.

Formellement :
explanation(x) = argmin_g [ L(f, g, pi_x) + Omega(g) ]
Ou L est la fidelite locale, pi_x est le kernel de proximite,
et Omega est la complexite du modele interpretable g.
```

#### Variantes de LIME

- **LIME Tabular** : Pour les donnees tabulaires. Perturbations par echantillonnage a partir de la distribution des features.
- **LIME Text** : Pour les donnees textuelles. Perturbations par suppression de mots ou tokens.
- **LIME Image** : Pour les images. Perturbations par masquage de super-pixels (segmentation).

#### Implementation pratique LIME

```python
import lime
import lime.lime_tabular

# Creer l'explainer LIME
explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=X_train.columns,
    class_names=["Reject", "Accept"],
    mode="classification",
    discretize_continuous=True
)

# Generer une explication locale
exp = explainer.explain_instance(
    data_row=X_test.iloc[idx].values,
    predict_fn=model.predict_proba,
    num_features=10,
    num_samples=5000
)

# Visualiser
exp.show_in_notebook()
exp.as_list()  # Liste des features avec leur poids
```

#### Limites et precautions d'usage de LIME

- **Instabilite** : Les explications LIME sont sensibles au processus de perturbation aleatoire. Deux executions sur la meme instance peuvent produire des explications differentes. Augmenter num_samples (>= 5000) et verifier la stabilite par repetition.
- **Choix du kernel** : Le kernel de proximite (largeur) influence fortement les explications. Un kernel trop large produit des explications globales (perte de localite). Un kernel trop etroit produit des explications instables.
- **Fidelite locale** : L'approximation lineaire peut etre inadequate si la frontiere de decision est fortement non-lineaire dans le voisinage. Verifier le R-squared de l'approximation (> 0.7).
- **Independance des features** : LIME suppose implicitement l'independance des features pour le sampling. Pour des features fortement correlees, les perturbations peuvent etre irrealistes.

### Attention Maps & Saliency Methods

Pour les modeles de deep learning (transformers, CNNs), les methodes de saliency exploitent la structure interne du modele :

#### Attention-based Explanations

```python
# Extraire les poids d'attention d'un modele transformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model = AutoModelForSequenceClassification.from_pretrained("model_name", output_attentions=True)
tokenizer = AutoTokenizer.from_pretrained("model_name")

inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
attentions = outputs.attentions  # Tuple de tenseurs (layer, batch, head, seq, seq)

# Agreger les attentions (attention rollout)
import torch
def attention_rollout(attentions):
    result = torch.eye(attentions[0].size(-1))
    for attention in attentions:
        attention_heads_fused = attention.mean(dim=1).squeeze(0)  # Moyenne sur les tetes
        attention_heads_fused = (attention_heads_fused + torch.eye(attention_heads_fused.size(-1))) / 2
        result = torch.matmul(attention_heads_fused, result)
    return result[0]  # Attention du token [CLS] vers tous les tokens
```

**Precaution critique** : Le debat academique sur la fiabilite des attention weights comme explications est non resolu. Jain & Wallace (2019) montrent que les attention weights ne correlent pas toujours avec les feature importances. Wiegreffe & Pinter (2019) nuancent cette conclusion. Ne pas utiliser les attention weights comme seule source d'explication. Les combiner avec des methodes plus robustes (SHAP, Integrated Gradients).

#### Integrated Gradients

Methode axiomatiquement rigoureuse pour les modeles differentiables. Satisfait les axiomes de sensibilite et d'invariance d'implementation :

```python
# Integrated Gradients avec Captum (PyTorch)
from captum.attr import IntegratedGradients

ig = IntegratedGradients(model)
attributions = ig.attribute(
    inputs=input_tensor,
    baselines=baseline_tensor,  # Typiquement un input "neutre" (zeros, padding)
    n_steps=200,                # Plus de steps = plus de precision
    internal_batch_size=32
)
```

### Counterfactual Explanations

Les explications contrefactuelles repondent a la question : "Quel changement minimal dans les features aurait conduit a une decision differente ?"

#### Algorithme

```
Trouver x_cf = argmin_x' [ distance(x, x') ]
  sous contrainte : f(x') != f(x)                [decision differente]
  et              : x' est plausible/actionnable  [dans le manifold des donnees]

Exemple de sortie :
"Votre demande de credit a ete refusee. Si votre revenu annuel avait ete
de 35 000 EUR au lieu de 28 000 EUR, et si vous n'aviez pas eu d'incident
de paiement dans les 12 derniers mois, la demande aurait ete acceptee."
```

#### Frameworks pour les counterfactuals

| Framework | Specialite | Methode |
|---|---|---|
| **DiCE** (Microsoft) | Counterfactuals divers et actionnables | Optimisation avec contraintes de diversite |
| **Alibi** (Seldon) | Counterfactuals et prototypes | Multiple methodes (Wachter, prototype) |
| **CARLA** | Benchmark de counterfactuals | Comparaison systematique de methodes |
| **Contrastive Explanations** | Explications "pourquoi A plutot que B" | Pertinent negatives |

#### Proprietes d'un bon counterfactual

- **Proximite** : Le counterfactual doit etre aussi proche que possible de l'instance originale.
- **Sparsity** : Le nombre de features modifiees doit etre minimal (idealement 1-3).
- **Plausibilite** : Le counterfactual doit etre realiste (dans le manifold des donnees).
- **Actionnabilite** : Les changements doivent etre realisables par la personne concernee (ne pas suggerer de changer l'age ou l'ethnicite).
- **Diversite** : Fournir plusieurs counterfactuals pour donner plusieurs voies d'action.
- **Causal consistency** : Les changements doivent respecter les relations causales entre features.

---

## Model Cards

### Standard et objectif

Les model cards (Mitchell et al., 2019) sont des documents standardises qui accompagnent les modeles de machine learning deployes. Elles servent de "notice" du modele, documentant ses capacites, ses limites, ses conditions d'utilisation et ses considerations ethiques.

### Structure d'une Model Card

#### 1. Model Details

```markdown
## Model Details
- **Nom du modele** : [nom unique et versionne]
- **Version** : [numero de version, date de publication]
- **Type de modele** : [architecture, algorithme]
- **Developpe par** : [equipe, organisation]
- **Date d'entrainement** : [date]
- **Licence** : [licence d'utilisation]
- **Contact** : [email, equipe responsable]
- **Citation** : [reference pour citer le modele]
```

#### 2. Intended Use

```markdown
## Intended Use
- **Cas d'usage primaire** : [description precise]
- **Utilisateurs vises** : [profils des utilisateurs]
- **Cas d'usage hors perimetre** : [usages explicitement non supportes]
  - NE PAS utiliser pour [usage a risque 1]
  - NE PAS utiliser pour [usage a risque 2]
```

#### 3. Factors & Metrics

```markdown
## Factors
- **Groupes pertinents** : [demographics, phenotypes, conditions]
- **Facteurs instrumentaux** : [environnement, materiel, temporalite]
- **Facteurs environnementaux** : [contexte social, conditions de deploiement]

## Metrics
- **Metriques de performance** : [accuracy, F1, AUC, etc.]
- **Metriques de fairness** : [demographic parity ratio, equalized odds diff, etc.]
- **Seuils de decision** : [seuils utilises et leur justification]
```

#### 4. Evaluation Data & Results

```markdown
## Evaluation Data
- **Datasets** : [noms, tailles, sources]
- **Pre-processing** : [transformations appliquees]
- **Justification** : [pourquoi ces datasets representent les conditions d'usage]

## Results
| Metrique | Global | Groupe A | Groupe B | Ecart |
|---|---|---|---|---|
| Accuracy | 0.92 | 0.94 | 0.88 | 0.06 |
| FPR | 0.05 | 0.03 | 0.08 | 0.05 |
| Selection Rate | 0.45 | 0.48 | 0.40 | 0.08 |
```

#### 5. Ethical Considerations & Limitations

```markdown
## Ethical Considerations
- **Risques identifies** : [liste des risques ethiques]
- **Strategies de mitigation** : [actions prises]
- **Biais residuels** : [biais connus non resolus et leur impact]

## Limitations
- **Limites connues** : [conditions ou le modele performe mal]
- **Hors distribution** : [populations/contextes non couverts]
- **Recommandations** : [precautions d'usage]
```

### Template de Model Card complet

Utiliser les templates fournis par les outils :

- **Hugging Face Model Cards** : Template integre dans le Hub, avec champs structures et metadonnees YAML.
- **Google Model Cards Toolkit** : Librairie Python pour generer des model cards programmatiquement avec visualisations automatiques.
- **Fiddler AI** : Plateforme de model monitoring avec generation automatique de model cards.

---

## Datasheets for Datasets

### Standard et objectif

Les datasheets for datasets (Gebru et al., 2021) documentent la provenance, la composition, la collecte, le pre-processing et les considerations ethiques des datasets utilises pour l'entrainement des modeles. Elles sont l'equivalent des fiches de donnees de securite (Safety Data Sheets) dans l'industrie chimique.

### Sections d'une Datasheet

#### Motivation

- Pourquoi ce dataset a-t-il ete cree ?
- Par qui et pour quelle tache ?
- Qui a finance la collecte ?

#### Composition

- Que contient le dataset (instances, features, labels) ?
- Quelle est la taille du dataset ?
- Les donnees sont-elles un echantillon representatif ? De quelle population ?
- Les donnees contiennent-elles des informations sensibles ou des donnees personnelles ?
- Les donnees contiennent-elles des identifiants directs ou indirects ?

#### Collection Process

- Comment les donnees ont-elles ete collectees (capteurs, API, scraping, enquete, annotation) ?
- Qui a collecte les donnees ?
- Sur quelle periode ?
- Les personnes concernees ont-elles ete informees et ont-elles donne leur consentement ?
- Un comite d'ethique a-t-il approuve la collecte (IRB, CNIL) ?

#### Preprocessing / Cleaning / Labeling

- Quelles transformations ont ete appliquees (nettoyage, normalisation, anonymisation) ?
- Comment les labels ont-ils ete attribues (automatiquement, manuellement, crowdsourcing) ?
- Quel est l'accord inter-annotateurs (kappa de Cohen, Fleiss) ?
- Les donnees brutes sont-elles disponibles ?

#### Uses

- Pour quelles taches le dataset a-t-il ete utilise ?
- Pour quelles taches ne devrait-il PAS etre utilise ?
- Y a-t-il des taches pour lesquelles le dataset pourrait etre nuisible ?

#### Distribution & Maintenance

- Comment le dataset est-il distribue (licence, acces) ?
- Qui maintient le dataset ?
- Le dataset sera-t-il mis a jour ? A quelle frequence ?
- Comment signaler des erreurs ou des problemes ?

---

## Conformite Reglementaire

### RGPD Article 22 -- Droit a l'explication

L'article 22 du RGPD (Reglement General sur la Protection des Donnees) etablit le droit de ne pas faire l'objet d'une decision fondee exclusivement sur un traitement automatise, y compris le profilage, produisant des effets juridiques ou significatifs.

#### Exigences pratiques

1. **Droit a l'information** (Articles 13-14) : Informer les personnes de l'existence d'un traitement automatise, de la logique sous-jacente, de l'importance et des consequences envisagees.

2. **Droit d'acces** (Article 15) : Fournir des informations utiles sur la logique de la decision sur demande de la personne concernee.

3. **Droit d'opposition et de contestation** : Permettre a la personne de contester la decision et d'obtenir une intervention humaine.

4. **Exceptions** : La decision automatisee est autorisee si elle est necessaire a la conclusion ou l'execution d'un contrat, autorisee par le droit, ou fondee sur le consentement explicite. Dans tous les cas, des mesures appropriees de protection doivent etre mises en place.

#### Implementation technique

```
Strategie de conformite RGPD Article 22 :

1. Classification des decisions :
   +-- Decision automatisee avec effet juridique/significatif ?
       +-- Oui --> Droit a l'explication applicable
       |   +-- Exception applicable (contrat, loi, consentement) ?
       |   |   +-- Oui --> Mettre en place les mesures de protection
       |   |   +-- Non --> Intervention humaine obligatoire
       +-- Non --> Bonne pratique de fournir des explications

2. Niveaux d'explication a fournir :
   +-- Niveau 1 (information prealable) : Logique generale du systeme
   +-- Niveau 2 (sur demande) : Facteurs principaux de la decision individuelle
   +-- Niveau 3 (contestation) : Explication detaillee + intervention humaine
```

### EU AI Act -- Obligations de transparence

Le EU AI Act (Reglement europeen sur l'intelligence artificielle, entre en vigueur progressivement 2024-2026) impose des obligations de transparence proportionnelles au niveau de risque :

#### Systemes a haut risque (Annexe III)

Obligations de transparence renforcees pour les systemes d'IA a haut risque (credit scoring, recrutement, justice, sante, education, infrastructure critique) :

- **Documentation technique detaillee** : Description du systeme, de son objectif, de ses capacites et limites (article 11).
- **Record-keeping** : Logs automatiques pour assurer la tracabilite (article 12).
- **Transparence et information** : Instructions d'utilisation claires, incluant les caracteristiques de performance et les limites connues (article 13).
- **Controle humain** : Mesures de supervision humaine appropriees (article 14).
- **Exactitude, robustesse et cybersecurite** : Niveaux de performance declares et maintenus (article 15).

#### Obligations de transparence generales (Article 52)

Pour tous les systemes d'IA interagissant avec des personnes :

- Informer les personnes qu'elles interagissent avec un systeme d'IA (sauf si c'est evident).
- Pour les systemes de reconnaissance des emotions ou de categorisation biometrique : informer les personnes concernees.
- Pour les deep fakes : etiqueter clairement le contenu comme genere artificiellement.

---

## Transparency Reports

### Structure d'un rapport de transparence IA

Un rapport de transparence IA documente periodiquement (annuellement ou semestriellement) les pratiques de l'organisation en matiere d'IA responsable :

1. **Inventaire des systemes d'IA** : Liste de tous les systemes d'IA deployes, leur classification de risque, et leur statut de conformite.

2. **Metriques de fairness agreges** : Metriques de fairness moyennes et extremes sur l'ensemble du portefeuille de modeles. Evolution temporelle.

3. **Incidents et actions correctives** : Nombre d'incidents ethiques, nature, gravite, actions correctives prises, delais de resolution.

4. **Audits et evaluations** : Nombre d'audits realises (internes et externes), resultats agregees, actions en cours.

5. **Consultations et engagement** : Consultations des parties prenantes, retours des utilisateurs, plaintes recues et traitees.

6. **Formation et sensibilisation** : Nombre de collaborateurs formes a l'ethique de l'IA, contenu des formations, metriques d'engagement.

7. **Recherche et innovation** : Contributions a la recherche en AI ethics, participation a des groupes de travail, outils developpes.

### Outils de reporting

- **Model Card Toolkit (Google)** : Generation programmatique de model cards avec visualisations.
- **FactSheets (IBM)** : Documentation automatisee des modeles dans le pipeline ML.
- **Datasheets.ai** : Plateforme collaborative pour la redaction de datasheets.
- **MLflow** : Tracking des experiences avec metadonnees de fairness et d'explicabilite.
- **Weights & Biases** : Logging des metriques de fairness et des explications dans les runs d'entrainement.

---

## Layered Explainability -- Adapter l'explication a l'audience

### Principe

Fournir des explications a plusieurs niveaux de sophistication selon l'audience :

| Audience | Niveau | Contenu | Format |
|---|---|---|---|
| **Data Scientists** | Technique | SHAP values, feature interactions, model internals | Notebooks, SHAP plots, dashboards |
| **Decideurs metier** | Managerial | Feature importance globale, regles principales, cas limites | Rapports synthetiques, tableaux de bord |
| **Utilisateurs finaux** | Actionnable | Raisons principales de la decision, contrefactuels | Langage naturel, recours possibles |
| **Regulateurs** | Compliance | Model card, datasheet, metriques de fairness, logs | Documentation formelle, rapports d'audit |
| **Personnes affectees** | Droit | Facteurs determinants, alternatives, droit de contestation | Communication claire, non technique |

### Implementation

```python
# Generer des explications multi-niveaux
def explain_prediction(model, instance, level="user"):
    shap_values = explainer.shap_values(instance)

    if level == "technical":
        return {
            "shap_values": shap_values,
            "base_value": explainer.expected_value,
            "feature_interactions": explainer.shap_interaction_values(instance),
            "confidence": model.predict_proba(instance)
        }

    elif level == "business":
        top_features = get_top_features(shap_values, n=5)
        return {
            "decision": model.predict(instance),
            "confidence": model.predict_proba(instance).max(),
            "key_factors": top_features,
            "model_card_link": "/docs/model-card-v2.1"
        }

    elif level == "user":
        top_positive = get_top_features(shap_values, n=3, direction="positive")
        top_negative = get_top_features(shap_values, n=3, direction="negative")
        counterfactual = generate_counterfactual(model, instance)
        return {
            "decision": format_decision(model.predict(instance)),
            "reasons_for": format_reasons(top_positive),
            "reasons_against": format_reasons(top_negative),
            "what_if": format_counterfactual(counterfactual),
            "how_to_contest": "/support/contest-decision"
        }
```

---

## Checklist Explainability & Transparency

- [ ] Le niveau d'interpretabilite requis est defini en fonction du risque et de la reglementation
- [ ] Un modele interpretable a ete evalue comme baseline avant d'utiliser un modele complexe
- [ ] Les methodes XAI appropriees sont selectionnees et implementees
- [ ] Les limites des methodes XAI choisies sont documentees et communiquees
- [ ] Les explications sont validees avec des utilisateurs representatifs
- [ ] La model card est redigee et maintenue a jour
- [ ] Le datasheet for dataset est redige pour chaque dataset utilise
- [ ] La conformite RGPD article 22 est evaluee et documentee
- [ ] Le niveau de risque EU AI Act est evalue et les obligations correspondantes identifiees
- [ ] Les explications sont fournies a plusieurs niveaux (technique, metier, utilisateur)
- [ ] Un mecanisme de contestation des decisions est disponible
- [ ] Le rapport de transparence est publie periodiquement
