# Bias & Fairness -- Detection, Metrics & Mitigation

Reference complete sur les biais algorithmiques et l'equite en machine learning. Couvre la taxonomie des biais, les metriques de fairness, les techniques de detection et les strategies d'attenuation a chaque etape du pipeline ML. Ce document sert de guide operationnel pour les equipes data science, les auditeurs et les responsables de gouvernance IA.

---

## Taxonomie Complete des Biais Algorithmiques

### Biais lies aux donnees (Data Bias)

#### Selection Bias (Biais de selection)

Le biais de selection survient quand les donnees d'entrainement ne sont pas representatives de la population cible. Il se manifeste sous plusieurs formes :

- **Sampling bias** : L'echantillon de donnees surrepresente ou sous-represente certains segments. Exemple : un modele de detection de fraude entraine sur des transactions de clients urbains performera mal sur les profils ruraux. Detecter en comparant la distribution de l'echantillon avec la distribution connue de la population cible. Corriger par stratified sampling ou importance weighting.

- **Survivorship bias** : Les donnees ne contiennent que les cas "survivants". Exemple classique : un modele de credit entraine uniquement sur les personnes ayant obtenu un credit dans le passe ignore systematiquement le profil des personnes rejetees. Corriger par reject inference (techniques d'imputation pour les cas rejetes) ou collecte active de donnees pour les populations sous-representees.

- **Exclusion bias** : Certaines populations sont systematiquement exclues des donnees par design. Exemple : un dataset medical excluant les personnes sans assurance sante. Diagnostiquer en listant exhaustivement les criteres d'inclusion/exclusion et en evaluant quelles populations sont exclues.

- **Non-response bias** : Les personnes qui ne repondent pas aux enquetes different systematiquement des repondants. Corriger par post-stratification weighting ou modeles de propension a repondre.

#### Measurement Bias (Biais de mesure)

Le biais de mesure resulte d'erreurs systematiques dans la facon dont les variables sont mesurees ou collectees :

- **Proxy discrimination** : Utilisation de variables apparemment neutres qui sont fortement correlees avec des attributs proteges. Le code postal peut servir de proxy pour l'ethnicite ou le revenu. L'adresse email (domaine professionnel vs gratuit) peut servir de proxy pour le statut socio-economique. Detecter par analyse de correlation (Pearson, Cramer's V) entre chaque feature et les attributs proteges. Appliquer un seuil de correlation maximal (typiquement |r| < 0.3) ou utiliser des techniques de decorrelation.

- **Label bias** : Les labels d'entrainement refletent les biais des annotateurs ou du processus d'annotation. Exemple : dans un systeme de detection de discours haineux, les annotateurs peuvent avoir des seuils de tolerance differents selon la langue ou la culture. Corriger par multi-annotator agreement (kappa de Cohen > 0.7), guidelines d'annotation claires et standardisees, et audits inter-annotateurs reguliers.

- **Feature engineering bias** : Le choix des features introduit implicitement des biais. Certaines features peuvent etre systematiquement moins fiables pour certains sous-groupes (reconnaissance faciale avec moins de points de reference pour les peaux sombres). Auditer la qualite de chaque feature par sous-groupe.

#### Representation Bias (Biais de representation)

Le biais de representation survient quand certains groupes sont sous-representes dans les donnees d'entrainement :

- **Class imbalance by subgroup** : Les donnees peuvent etre equilibrees globalement mais desequilibrees au sein de sous-groupes specifiques. Un dataset de 50/50 homme/femme peut avoir 80/20 senior/junior pour les femmes. Analyser les distributions conjointes, pas seulement marginales.

- **Geographic/linguistic representation** : Les modeles NLP entraines majoritairement sur des donnees anglophones performent mal sur d'autres langues. Les modeles de vision entraines sur des images occidentales performent mal sur des contextes culturels differents. Mesurer la representation geographique et linguistique du dataset.

- **Temporal representation** : Les donnees refletent un moment specifique qui peut ne plus etre representatif. Les modeles entraines sur des donnees pre-pandemiques peuvent etre biaises pour les comportements post-pandemiques. Verifier la date de collecte et la pertinence temporelle.

#### Historical Bias (Biais historique)

Le biais historique est le plus insidieux car il reflete des inegalites structurelles reelles dans les donnees. Meme avec des donnees parfaitement representatives et des mesures exactes, le modele peut reproduire et amplifier des discriminations historiques :

- Donnees de recrutement refletant des decennies de discrimination a l'embauche.
- Donnees de recidive penale refletant un policing disproportionne de certaines communautes.
- Donnees salariales refletant les inegalites de genre historiques.

La correction du biais historique necessite une approche causale : distinguer les correlations refletant des inegalites structurelles de celles refletant des differences legitimes. Utiliser des causal directed acyclic graphs (DAGs) pour modeliser les relations causales et identifier les chemins discriminatoires. Consulter systematiquement des experts du domaine et des representants des communautes affectees.

#### Aggregation Bias (Biais d'agregation)

L'aggregation bias survient quand un modele unique est applique a des populations heterogenes qui auraient beneficie de modeles distincts. Exemple : un modele de diagnostic medical entraine sur une population globale peut etre imprecis pour des sous-groupes ayant des presentations cliniques differentes (symptomes cardiaques differents chez les femmes vs les hommes). Diagnostiquer en comparant les performances du modele global avec des modeles specifiques par sous-groupe.

#### Evaluation Bias (Biais d'evaluation)

Les benchmarks et jeux de test utilises pour evaluer les modeles peuvent eux-memes etre biaises. Les datasets d'evaluation standard (ImageNet, COCO, GLUE) presentent des biais demographiques et culturels documentes. Toujours completer les benchmarks standard par des evaluations specifiques sur les populations cibles. Construire des jeux de test representatifs de la population de deploiement reelle.

---

## Metriques de Fairness -- Definitions et Calculs

### Group Fairness Metrics

#### Demographic Parity (Statistical Parity)

**Definition** : La probabilite d'un outcome positif doit etre identique pour tous les groupes.

```
P(Y_hat = 1 | A = a) = P(Y_hat = 1 | A = b)  pour tous les groupes a, b

Ratio de parite : min(P(Y=1|A=a), P(Y=1|A=b)) / max(P(Y=1|A=a), P(Y=1|A=b))
Seuil acceptable : ratio >= 0.8 (regle des 4/5e de l'EEOC)
```

**Quand l'utiliser** : Quand l'objectif est l'egalite d'acces a une ressource (recrutement, credit, logement) independamment des taux de base. Quand les labels historiques sont eux-memes biaises. Quand la regulation l'exige (disparate impact analysis aux Etats-Unis).

**Limites** : Ignore les differences de taux de base entre groupes. Peut forcer des predictions sous-optimales si les taux de base different legitimement. Incompatible avec la calibration si les taux de base different (theorem de Chouldechova).

#### Equalized Odds (Egalite des chances)

**Definition** : Les taux de vrais positifs (TPR) et de faux positifs (FPR) doivent etre identiques pour tous les groupes.

```
P(Y_hat = 1 | Y = 1, A = a) = P(Y_hat = 1 | Y = 1, A = b)  [Equal TPR]
P(Y_hat = 1 | Y = 0, A = a) = P(Y_hat = 1 | Y = 0, A = b)  [Equal FPR]
```

**Quand l'utiliser** : Quand les labels sont fiables et que l'equite doit se mesurer conditionnellement a l'outcome reel. Cas typiques : diagnostic medical (meme sensibilite et specificite pour tous les groupes), justice predictive (meme taux de faux positifs pour tous les groupes).

**Variante relaxee -- Equal Opportunity** : Exiger uniquement l'egalite des TPR (pas des FPR). Convient quand le cout du faux negatif est plus important que celui du faux positif (ne pas manquer un patient malade).

#### Predictive Parity (Calibration)

**Definition** : La valeur predictive positive doit etre identique pour tous les groupes.

```
P(Y = 1 | Y_hat = 1, A = a) = P(Y = 1 | Y_hat = 1, A = b)

Equivalemment : parmi les individus predits positifs, la proportion de vrais positifs
est la meme dans tous les groupes.
```

**Quand l'utiliser** : Quand la confiance dans la prediction doit etre interpretable uniformement. Un score de risque de 80% doit signifier la meme chose pour tous les groupes. Essentiel pour les modeles de scoring (credit scoring, risk scoring).

**Limites** : Compatible avec des taux de selection differents entre groupes. Peut coexister avec un impact disparate significatif.

#### Calibration by Group

**Definition** : Pour chaque seuil de score, la proportion d'outcomes positifs reels doit etre identique entre groupes.

```
P(Y = 1 | Score = s, A = a) = P(Y = 1 | Score = s, A = b)  pour tout score s

Verifier via des calibration curves separees par groupe.
Utiliser des tests statistiques (Hosmer-Lemeshow par groupe) pour valider.
```

### Individual Fairness Metrics

#### Lipschitz Fairness

**Definition** : Des individus similaires doivent recevoir des predictions similaires. Formellement, la fonction de decision doit satisfaire une condition de Lipschitz :

```
d_outcome(f(x_i), f(x_j)) <= L * d_input(x_i, x_j)

Ou d_input est une metrique de similarite "task-relevant" entre individus
et d_outcome est la distance entre les predictions.
```

Le defi principal est de definir la metrique de similarite d_input de maniere appropriee. Des approches recentes utilisent le metric learning pour apprendre cette metrique a partir de jugements d'experts.

#### Counterfactual Fairness

**Definition** : La prediction pour un individu ne doit pas changer si l'on modifie contrefactuellement son attribut protege tout en maintenant les autres attributs causalement independants.

```
P(Y_hat_A=a | X = x) = P(Y_hat_A=b | X = x)

Necessite un modele causal (DAG) specifiant les relations entre
attributs proteges, features et outcome.
```

### Impossibility Theorems

Les theoremes d'impossibilite demontrent qu'il est generalement impossible de satisfaire simultanement plusieurs definitions de fairness :

**Theorem de Chouldechova (2017)** : Pour un classifieur binaire, il est impossible de satisfaire simultanement la calibration (predictive parity) et l'egalite des taux de faux positifs et faux negatifs (equalized odds), sauf si les taux de base sont identiques entre groupes.

**Theorem de Kleinberg-Mullainathan-Raghavan (2016)** : Trois proprietes -- calibration within groups, balance for the positive class, balance for the negative class -- ne peuvent etre satisfaites simultanement sauf dans des cas triviaux.

**Implication pratique** : Le choix de la metrique de fairness est un choix de valeurs, pas un choix technique. Il doit etre fait explicitement par les parties prenantes (ethiciens, juristes, representants des communautes affectees) et documente dans la model card.

---

## Techniques de Detection des Biais

### Pre-deployment Detection

#### Analyse exploratoire des donnees (EDA for Fairness)

Conduire une EDA specifiquement orientee equite avant tout entrainement :

1. **Distribution analysis** : Calculer la representation de chaque groupe protege dans le dataset. Verifier que chaque sous-groupe a une taille suffisante pour un apprentissage fiable (regle heuristique : au moins 100 exemples par sous-groupe par classe).

2. **Label rate analysis** : Comparer les taux de labels positifs entre groupes. Un ecart significatif peut indiquer un biais historique ou un biais de labeling.

3. **Feature distribution analysis** : Comparer la distribution de chaque feature entre groupes. Utiliser des tests statistiques (KS test, chi-square) pour identifier les features dont la distribution differe significativement entre groupes.

4. **Proxy detection** : Calculer la mutual information ou la correlation entre chaque feature et chaque attribut protege. Identifier les features qui sont des proxies des attributs proteges (correlation > 0.3).

5. **Intersectional analysis** : Ne pas se limiter aux attributs proteges individuels. Analyser les intersections (genre x age, ethnicite x revenu). Les biais intersectionnels sont souvent plus severes que les biais marginaux.

#### Bias Auditing Tools

| Outil | Langage | Specialite | Metriques supportees |
|---|---|---|---|
| **Fairlearn** | Python | Fairness-aware ML complet | 10+ metriques de groupe, mitigation |
| **AIF360** (IBM) | Python | Toolkit complet biais | 70+ metriques, 11 algorithmes mitigation |
| **Aequitas** | Python | Audit de biais | Metriques de groupe, rapports automatises |
| **What-If Tool** | TensorFlow | Exploration interactive | Visualisation, counterfactuals, slicing |
| **Responsible AI Toolbox** | Python | Ecosysteme Microsoft | Error analysis, fairness, explainability |
| **Google PAIR** | Python | Fairness indicators | Integration TFX, metriques TF |

### Post-deployment Detection

#### Monitoring en production

Deployer un pipeline de monitoring continu des metriques de fairness :

1. **Real-time fairness metrics** : Calculer les metriques de fairness sur des fenetres glissantes (horaire, quotidienne, hebdomadaire). Comparer avec les baselines etablies lors de la validation.

2. **Drift detection by subgroup** : Monitorer le data drift (input distribution) et le concept drift (prediction distribution) separement par sous-groupe. Un drift affectant disproportionnellement un sous-groupe est un signal d'alerte.

3. **Outcome monitoring** : Quand les outcomes reels sont disponibles (apres un delai), recalculer les metriques d'equite sur les donnees de production. Comparer avec les metriques de validation.

4. **Complaint analysis** : Analyser les reclamations et contestations des utilisateurs par sous-groupe. Une surrepresentation de reclamations d'un sous-groupe est un indicateur de biais potentiel.

5. **A/B testing for fairness** : Lors de la mise a jour d'un modele, mesurer l'impact differrentiel sur les sous-groupes via des A/B tests avec des metriques de fairness comme criteres de decision.

---

## Strategies d'Attenuation des Biais

### Pre-processing (Sur les donnees)

Intervenir sur les donnees avant l'entrainement pour reduire les biais :

#### Reweighting (Reponderation)

Assigner des poids differents aux exemples d'entrainement pour compenser les desequilibres. Calculer les poids pour que les distributions ponderees satisfassent la demographic parity :

```
w(x, a, y) = P(Y=y) * P(A=a) / P(Y=y, A=a)

Ou a est l'attribut protege, y le label, et w le poids.
Implementer avec Fairlearn ou AIF360.
```

Avantage : simple, ne modifie pas les donnees brutes. Limite : peut degrader la performance globale si les poids sont tres desequilibres.

#### Resampling (Re-echantillonnage)

Sous-echantillonner les groupes surrepresentes ou sur-echantillonner les groupes sous-representes. Variantes : stratified sampling, SMOTE adapte par sous-groupe. Attention a ne pas creer du surapprentissage (overfitting) par sur-echantillonnage.

#### Relabeling

Modifier les labels d'entrainement pour les exemples proches de la frontiere de decision quand les labels sont supposes biaises. Utiliser la confiance du modele et la proximite a la frontiere de decision pour identifier les candidats au relabeling. Approche risquee : documenter exhaustivement les criteres et les cas modifies.

#### Disparate Impact Remover

Transformer les features pour supprimer la correlation avec les attributs proteges tout en preservant le maximum d'information utile. Approche geometrique : projeter les features dans un espace orthogonal aux attributs proteges. Implementer avec AIF360 (DisparateImpactRemover).

#### Data Augmentation equitable

Generer des exemples synthetiques pour les sous-groupes sous-representes. Utiliser des techniques generatives (GANs, diffusion models) conditionnees par les attributs proteges. Verifier que les donnees synthetiques sont realistes et ne creent pas de nouveaux biais.

### In-processing (Pendant l'entrainement)

Modifier l'algorithme d'entrainement pour integrer des contraintes d'equite :

#### Adversarial Debiasing

Entrainer un modele adversarial qui tente de predire l'attribut protege a partir des representations internes du modele principal. Le modele principal est penalise s'il encode l'attribut protege :

```
Loss = Loss_task - lambda * Loss_adversary

Ou Loss_adversary est la capacite d'un reseau adversarial a predire
l'attribut protege a partir de la representation latente.
Le modele principal apprend donc des representations qui ne contiennent
pas d'information sur l'attribut protege.
```

#### Fairness Constraints in Optimization

Ajouter des contraintes d'equite directement dans le probleme d'optimisation :

```
minimize    Loss_task(theta)
subject to  |P(Y_hat=1|A=a) - P(Y_hat=1|A=b)| <= epsilon   [Demographic Parity]
            |FPR_a - FPR_b| <= epsilon                        [Equal FPR]
            |TPR_a - TPR_b| <= epsilon                        [Equal TPR]

Utiliser des approches Lagrangiennes pour convertir les contraintes
en penalites dans la fonction de perte.
Frameworks : Fairlearn (ExponentiatedGradient, GridSearch), AIF360.
```

#### Prejudice Remover Regularizer

Ajouter un terme de regularisation qui penalise la mutual information entre les predictions et les attributs proteges. L'intensite de la regularisation (parametre eta) controle le compromis equite-performance.

#### Fair Representation Learning

Apprendre des representations latentes qui sont informatives pour la tache mais independantes des attributs proteges. Approches : Variational Fair Autoencoders, Fair Adversarial Networks, Contrastive Fair Representations. Avantage : les representations equitables peuvent etre reutilisees pour plusieurs taches en aval.

### Post-processing (Apres l'entrainement)

Ajuster les predictions du modele apres l'entrainement pour satisfaire les contraintes d'equite :

#### Threshold Optimization

Appliquer des seuils de decision differents par groupe pour equaliser les metriques de fairness :

```
Pour chaque groupe a, trouver le seuil t_a qui satisfait la contrainte d'equite :

Demographic Parity : trouver t_a tel que P(Score > t_a | A = a) = target_rate
Equalized Odds : trouver t_a tel que TPR_a = TPR_target et FPR_a = FPR_target

Implementer avec Fairlearn (ThresholdOptimizer).
```

Avantage : ne modifie pas le modele, simple a implementer et a expliquer. Limite : les seuils differents par groupe peuvent etre percus comme discriminatoires (traitement explicitement different).

#### Calibrated Equalized Odds

Post-processing qui trouve la transformation optimale des predictions pour satisfaire equalized odds tout en minimisant la perte de calibration. Algorithme : resoudre un programme lineaire pour trouver les probabilites de randomisation par groupe et par outcome.

#### Reject Option Classification

Pour les predictions proches de la frontiere de decision (incertaines), modifier la prediction en faveur du groupe defavorise. Intuition : les predictions incertaines sont celles ou la correction a le moins d'impact sur la performance globale.

---

## Disparate Impact Analysis

### Framework juridique et quantitatif

L'analyse d'impact disparate (disparate impact analysis) est un cadre juridique et statistique pour detecter la discrimination indirecte. Origine : Griggs v. Duke Power Co. (1971), formalisee par l'EEOC (Equal Employment Opportunity Commission).

#### Regle des 4/5e (Four-Fifths Rule)

```
Disparate Impact Ratio = (Selection Rate for Disadvantaged Group) / (Selection Rate for Advantaged Group)

Si le ratio < 0.8 (80%), il y a presomption de disparate impact.
Ce seuil est un signal d'alerte, pas une preuve definitive.
```

#### Tests statistiques complementaires

- **Test du chi-carre** : Tester l'independance entre la decision et l'attribut protege.
- **Test exact de Fisher** : Pour les petits echantillons.
- **Regression logistique** : Controler pour les variables legitimes et tester l'effet residuel de l'attribut protege.
- **Causal inference** : Utiliser des methodes causales (do-calculus, front-door criterion) pour distinguer discrimination directe et indirecte.

### Processus d'analyse d'impact disparate

1. Definir la decision etudiee et les groupes proteges pertinents.
2. Calculer les taux de selection par groupe.
3. Appliquer la regle des 4/5e et les tests statistiques.
4. Si disparate impact detecte, analyser les causes (features, donnees, modele).
5. Evaluer si la pratique est justifiee par une necessite metier (business necessity defense).
6. Si justifiee, verifier qu'il n'existe pas d'alternative moins discriminatoire.
7. Documenter l'analyse complete dans la model card.

---

## Outils et Frameworks

### Ecosysteme Python pour le Fairness ML

```python
# Exemple : Audit de fairness complet avec Fairlearn
from fairlearn.metrics import MetricFrame, selection_rate, false_positive_rate, false_negative_rate
from fairlearn.reductions import ExponentiatedGradient, DemographicParity

# Etape 1 : Mesurer les metriques de fairness
metrics = {
    "selection_rate": selection_rate,
    "false_positive_rate": false_positive_rate,
    "false_negative_rate": false_negative_rate,
}
metric_frame = MetricFrame(
    metrics=metrics,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sensitive_test
)
print(metric_frame.by_group)
print(f"Selection rate ratio: {metric_frame.ratio()}")

# Etape 2 : Mitigation via ExponentiatedGradient
mitigator = ExponentiatedGradient(
    estimator=base_estimator,
    constraints=DemographicParity()
)
mitigator.fit(X_train, y_train, sensitive_features=sensitive_train)
y_pred_fair = mitigator.predict(X_test)

# Etape 3 : Re-evaluer apres mitigation
metric_frame_fair = MetricFrame(
    metrics=metrics,
    y_true=y_test,
    y_pred=y_pred_fair,
    sensitive_features=sensitive_test
)
print(f"Selection rate ratio after mitigation: {metric_frame_fair.ratio()}")
```

```python
# Exemple : Audit avec AIF360
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from aif360.algorithms.preprocessing import Reweighing
from aif360.algorithms.inprocessing import PrejudiceRemover

# Etape 1 : Creer le dataset AIF360
dataset = BinaryLabelDataset(
    df=df,
    label_names=["outcome"],
    protected_attribute_names=["gender", "race"]
)

# Etape 2 : Mesurer les metriques sur le dataset
metric = BinaryLabelDatasetMetric(
    dataset,
    unprivileged_groups=[{"gender": 0}],
    privileged_groups=[{"gender": 1}]
)
print(f"Disparate Impact: {metric.disparate_impact()}")
print(f"Statistical Parity Difference: {metric.statistical_parity_difference()}")

# Etape 3 : Pre-processing mitigation
rw = Reweighing(
    unprivileged_groups=[{"gender": 0}],
    privileged_groups=[{"gender": 1}]
)
dataset_rw = rw.fit_transform(dataset)
```

### Integration dans le pipeline MLOps

Integrer les checks de fairness dans le pipeline CI/CD du modele :

1. **Pre-commit** : Validation des datasheets for datasets.
2. **Training pipeline** : Calcul automatique des metriques de fairness sur le jeu de validation.
3. **Model registry gate** : Le modele ne peut etre promu que si les metriques de fairness sont dans les seuils definis.
4. **Deployment gate** : Validation finale avec shadow deployment et comparaison des metriques de fairness avec le modele en production.
5. **Production monitoring** : Dashboards de fairness en temps reel avec alertes.

### Checklist de Fairness Audit

- [ ] Les attributs proteges pertinents sont identifies et documentes
- [ ] Les metriques de fairness sont choisies et justifiees par les parties prenantes
- [ ] Les seuils d'acceptabilite sont definis et documentes
- [ ] L'EDA for fairness est realisee (distributions, label rates, correlations, proxies)
- [ ] L'analyse intersectionnelle est conduite
- [ ] Les metriques de fairness sont calculees sur le jeu de test
- [ ] Les ecarts sont analyses et documentes
- [ ] Les actions de mitigation sont implementees si necessaire
- [ ] L'impact de la mitigation sur la performance globale est mesure
- [ ] L'analyse d'impact disparate (4/5e rule) est realisee
- [ ] Les resultats sont documentes dans la model card
- [ ] Le monitoring de fairness en production est configure
- [ ] Les procedures de rollback sont definies
- [ ] L'audit par une partie independante est planifie
