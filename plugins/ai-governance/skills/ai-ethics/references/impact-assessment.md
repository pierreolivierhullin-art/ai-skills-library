# Impact Assessment -- Algorithmic, Social & Environmental

Reference complete sur l'evaluation d'impact des systemes d'IA. Couvre l'Algorithmic Impact Assessment (AIA), l'evaluation de l'impact social, l'impact environnemental (empreinte carbone, CodeCarbon), la consultation des parties prenantes, le monitoring continu et l'audit. Ce document sert de guide operationnel pour les responsables de gouvernance IA, les equipes techniques, les risk managers et les regulateurs.

---

## Algorithmic Impact Assessment (AIA)

### Definition et objectif

L'Algorithmic Impact Assessment (AIA) -- ou evaluation d'impact algorithmique -- est un processus systematique et structure visant a identifier, evaluer et attenuer les risques lies au deploiement d'un systeme de decision algorithmique. L'AIA est l'equivalent pour l'IA de l'etude d'impact sur la vie privee (Privacy Impact Assessment / AIPD) du RGPD, mais avec un perimetre elargi couvrant l'equite, la transparence, la responsabilite et les impacts sociaux.

### Quand conduire une AIA

Conduire une AIA est obligatoire ou fortement recommande dans les cas suivants :

- **Obligatoire** : Systemes classes "haut risque" par le EU AI Act (Annexe III), systemes de decision automatisee au sens de l'article 22 du RGPD, systemes soumis a des reglementations sectorielles (finance, sante, emploi).
- **Fortement recommande** : Tout systeme affectant des individus ou des groupes, systemes utilisant des donnees personnelles ou des proxies d'attributs proteges, systemes deployes a grande echelle.
- **Screening rapide** : Pour les systemes a risque faible, un screening initial permet de determiner si une AIA complete est necessaire.

### Framework AIA en 5 phases

#### Phase 1 -- Cadrage et classification du risque

```
Questionnaire de screening initial :

1. Le systeme prend-il ou influence-t-il des decisions affectant des individus ?
   +-- Non --> AIA simplifiee (documentation minimale)
   +-- Oui --> Question 2

2. La decision a-t-elle un impact juridique ou significatif sur les individus ?
   +-- Non --> AIA legere (documentation standard)
   +-- Oui --> Question 3

3. Le systeme utilise-t-il des donnees personnelles ou des proxies
   d'attributs proteges ?
   +-- Non --> AIA standard
   +-- Oui --> Question 4

4. Le systeme est-il classe "haut risque" (EU AI Act Annexe III) ?
   +-- Non --> AIA standard
   +-- Oui --> AIA complete avec evaluation de conformite

Classification du risque (echelle 1-5) :
  1 - Minimal   : Pas d'impact sur les individus
  2 - Faible     : Impact limite, facilement reversible
  3 - Modere    : Impact significatif mais maitrisable
  4 - Eleve      : Impact important sur les droits ou les opportunites
  5 - Critique   : Impact potentiellement irreversible sur les droits fondamentaux
```

#### Phase 2 -- Identification des impacts

Identifier systematiquement les impacts potentiels du systeme sur les dimensions suivantes :

**Impacts sur les individus** :

| Dimension | Questions cles | Exemples de risques |
|---|---|---|
| **Droits fondamentaux** | Le systeme peut-il affecter la dignite, la liberte, l'egalite ? | Discrimination, atteinte a la vie privee, restriction de liberte |
| **Equite et non-discrimination** | Le systeme peut-il traiter certains groupes de maniere defavorable ? | Biais algorithmiques, impact disparate, exclusion |
| **Autonomie et agency** | Le systeme reduit-il la capacite de choix des individus ? | Manipulation, nudging excessif, dependance |
| **Vie privee** | Le systeme collecte-t-il ou infere-t-il des donnees sensibles ? | Surveillance, profilage, inference d'attributs sensibles |
| **Securite** | Le systeme peut-il causer des dommages physiques ou psychologiques ? | Decisions medicales erronees, vehicules autonomes, stress |
| **Acces aux services** | Le systeme peut-il limiter l'acces a des services essentiels ? | Refus de credit, d'assurance, d'emploi, de logement |

**Impacts sur les groupes et la societe** :

| Dimension | Questions cles | Exemples de risques |
|---|---|---|
| **Cohesion sociale** | Le systeme peut-il renforcer les inegalites existantes ? | Concentration de richesse, exclusion numerique, fracture sociale |
| **Democratie** | Le systeme peut-il affecter les processus democratiques ? | Desinformation, manipulation electorale, bulles informationnelles |
| **Marche du travail** | Le systeme peut-il deplacer des emplois ou modifier les conditions de travail ? | Automatisation, surveillance des employes, gig economy |
| **Environnement** | Le systeme a-t-il un impact environnemental significatif ? | Consommation energetique, emissions carbone |
| **Concentration du pouvoir** | Le systeme renforce-t-il la concentration du pouvoir economique ou politique ? | Monopoles de donnees, asymetrie d'information |

#### Phase 3 -- Evaluation des risques

Pour chaque impact identifie, evaluer :

```
Matrice d'evaluation des risques :

Risque = Probabilite x Severite x Reversibilite

Probabilite :
  1 - Improbable       : Circonstances exceptionnelles
  2 - Peu probable     : Pourrait se produire rarement
  3 - Possible         : Se produira probablement dans certains cas
  4 - Probable         : Se produira dans la majorite des cas
  5 - Quasi-certain    : Se produira systematiquement

Severite :
  1 - Negligeable      : Impact insignifiant
  2 - Mineure          : Desagrement temporaire
  3 - Moderee         : Impact significatif mais gerable
  4 - Majeure          : Impact grave sur les droits ou les opportunites
  5 - Critique         : Impact potentiellement irreversible

Reversibilite :
  1 - Totalement reversible
  2 - Largement reversible avec effort modere
  3 - Partiellement reversible avec effort significatif
  4 - Difficilement reversible
  5 - Irreversible

Score de risque = Probabilite x Severite x (Reversibilite / 5)
Seuils : < 5 = faible, 5-15 = modere, 15-30 = eleve, > 30 = critique
```

#### Phase 4 -- Mesures d'attenuation

Pour chaque risque identifie comme modere ou superieur, definir des mesures d'attenuation :

| Strategie | Description | Exemples |
|---|---|---|
| **Elimination** | Supprimer la source du risque | Ne pas utiliser l'IA pour cette decision, supprimer les features a risque |
| **Substitution** | Remplacer par une approche moins risquee | Modele interpretable au lieu de boite noire, human-in-the-loop |
| **Controles techniques** | Ajouter des mesures techniques de protection | Contraintes de fairness, differential privacy, adversarial training |
| **Controles proceduraux** | Ajouter des processus de supervision | Audits periodiques, monitoring continu, comite d'ethique |
| **Information** | Informer et former les parties prenantes | Model cards, formation des operateurs, communication aux utilisateurs |

#### Phase 5 -- Documentation et suivi

Produire un rapport d'AIA structure contenant :

```markdown
# Rapport d'Algorithmic Impact Assessment

## 1. Identification du systeme
- Nom, version, responsable
- Description du systeme et de son objectif
- Population affectee et contexte de deploiement

## 2. Classification du risque
- Resultat du screening initial
- Niveau de risque attribue (1-5)
- Justification de la classification

## 3. Inventaire des impacts
- Tableau des impacts identifies par dimension
- Impacts positifs attendus
- Impacts negatifs potentiels

## 4. Evaluation des risques
- Matrice de risque (probabilite x severite x reversibilite)
- Risques residuels apres mitigation
- Risques inacceptables identifies

## 5. Mesures d'attenuation
- Pour chaque risque : strategie d'attenuation, responsable, echeance
- Budget et ressources alloues
- Indicateurs de suivi

## 6. Plan de monitoring
- Metriques suivies en production
- Frequence des audits
- Seuils d'alerte et procedures d'escalade

## 7. Consultation des parties prenantes
- Parties prenantes consultees
- Synthese des retours
- Actions prises en reponse

## 8. Approbation et revue
- Approbateurs (comite d'ethique, direction, juridique)
- Date de la prochaine revue
- Conditions de declenchement d'une revue anticipee
```

---

## Evaluation d'Impact Social

### Methodologie d'evaluation d'impact social

L'evaluation d'impact social va au-dela de l'AIA en examinant les effets a moyen et long terme du systeme d'IA sur la societe :

#### Impact sur l'emploi et les competences

Evaluer l'impact du systeme sur l'emploi en utilisant le framework suivant :

```
Matrice d'impact emploi :

1. Taches automatisees :
   +-- Quelles taches humaines le systeme automatise-t-il ?
   +-- Quel pourcentage du temps de travail est affecte ?
   +-- Quels profils de poste sont les plus impactes ?

2. Taches augmentees :
   +-- Quelles taches humaines le systeme ameliore-t-il ?
   +-- Quel gain de productivite est attendu ?
   +-- Quelles nouvelles competences sont necessaires ?

3. Taches creees :
   +-- Quels nouveaux roles le systeme genere-t-il ?
   +-- Quelles competences sont requises pour ces roles ?
   +-- Un plan de formation/requalification est-il prevu ?

4. Impact net :
   +-- Bilan emplois supprimes vs crees
   +-- Plan de transition pour les postes supprimes
   +-- Mecanismes d'accompagnement (formation, reconversion)
```

#### Impact sur l'accessibilite et l'inclusion

Verifier que le systeme ne cree pas de nouvelles barrieres d'acces :

- **Accessibilite numerique** : Le systeme est-il accessible aux personnes handicapees (WCAG 2.1 AA) ? Les explications sont-elles disponibles dans des formats accessibles (texte alternatif, audio, braille) ?
- **Accessibilite linguistique** : Le systeme supporte-t-il les langues des populations servies ? Les biais linguistiques sont-ils evalues ?
- **Accessibilite economique** : Le systeme ne cree-t-il pas de dependance technologique couteuse ?
- **Fracture numerique** : Le systeme ne desavantage-t-il pas les personnes ayant un acces limite au numerique ?

#### Impact sur les droits fondamentaux

Conduire une evaluation formelle de l'impact sur les droits fondamentaux (Fundamental Rights Impact Assessment -- FRIA), requise par le EU AI Act pour les systemes a haut risque deployes par des entites publiques :

| Droit fondamental | Risques potentiels | Evaluation |
|---|---|---|
| **Dignite humaine** (Art. 1 Charte UE) | Deshumanisation, traitement degradant | Score : 1-5 |
| **Non-discrimination** (Art. 21) | Discrimination directe ou indirecte | Score : 1-5 |
| **Vie privee** (Art. 7) | Surveillance, profilage, inference | Score : 1-5 |
| **Protection des donnees** (Art. 8) | Collecte excessive, traitement illicite | Score : 1-5 |
| **Liberte d'expression** (Art. 11) | Censure, chilling effect | Score : 1-5 |
| **Egalite** (Art. 20) | Traitement inegal | Score : 1-5 |
| **Droits de l'enfant** (Art. 24) | Protection insuffisante des mineurs | Score : 1-5 |
| **Acces a la justice** (Art. 47) | Decisions opaques, absence de recours | Score : 1-5 |

---

## Impact Environnemental

### Empreinte carbone de l'IA

L'entrainement et l'inference des modeles d'IA consomment des quantites significatives d'energie et generent des emissions de carbone. L'evaluation de l'empreinte carbone est une composante essentielle de l'AI ethics.

#### Ordres de grandeur

| Modele / Activite | Energie (kWh) | CO2 (tonnes) | Equivalent |
|---|---|---|---|
| **Entrainement GPT-3** (175B) | ~1,287,000 | ~552 | 5 vols NY-SF aller-retour |
| **Entrainement GPT-4** (estime) | ~50,000,000+ | ~10,000+ | Centaines de foyers/an |
| **Entrainement BERT** (base) | ~1,507 | ~0.65 | 1 vol NY-SF |
| **Entrainement ResNet-50** | ~118 | ~0.05 | 100 km en voiture |
| **Fine-tuning LLM 7B** | ~100-500 | ~0.04-0.2 | 50-250 km en voiture |
| **1M queries GPT-4** | ~900 | ~0.4 | 1 vol Paris-NY |
| **1M queries modele classique** | ~1-10 | ~0.001-0.005 | Negligeable |

#### Facteurs determinants

L'empreinte carbone depend de plusieurs facteurs :

- **Taille du modele** : Relation superlineaire entre la taille du modele et l'energie d'entrainement. Doubler la taille peut multiplier l'energie par 3-4x.
- **Duree d'entrainement** : Nombre d'epochs, taille du dataset, critere d'arret.
- **Materiel** : GPU/TPU utilise, efficacite energetique (PUE du datacenter).
- **Source d'energie** : L'intensite carbone varie de 20 gCO2/kWh (nucleaire, renouvelable) a 900 gCO2/kWh (charbon).
- **Localisation du datacenter** : Le choix du datacenter affecte directement l'empreinte via le mix energetique local et le refroidissement.

### Mesure avec CodeCarbon

CodeCarbon est une librairie Python open-source qui mesure l'empreinte carbone du code de machine learning en temps reel :

```python
# Installation
# pip install codecarbon

# Usage basique -- decorator
from codecarbon import track_emissions

@track_emissions(project_name="model_training_v2", output_dir="./emissions")
def train_model():
    # Code d'entrainement standard
    model.fit(X_train, y_train)
    return model

model = train_model()
# Genere automatiquement un fichier emissions.csv avec :
# - timestamp, duration, energy_consumed (kWh)
# - emissions (kgCO2eq), emissions_rate
# - gpu_model, cpu_model, region, country

# Usage avance -- context manager
from codecarbon import EmissionsTracker

tracker = EmissionsTracker(
    project_name="experiment_42",
    measure_power_secs=15,        # Frequence de mesure (secondes)
    tracking_mode="process",       # 'process' ou 'machine'
    log_level="warning",
    output_dir="./carbon_logs",
    country_iso_code="FRA"         # Pour le mix energetique
)

tracker.start()
# Phase 1 : pre-processing
preprocess_data()
emissions_preprocess = tracker.flush()  # Sauvegarder l'emission intermediaire

# Phase 2 : entrainement
train_model()
emissions_training = tracker.flush()

# Phase 3 : evaluation
evaluate_model()
total_emissions = tracker.stop()

print(f"Pre-processing: {emissions_preprocess:.4f} kgCO2")
print(f"Training: {emissions_training:.4f} kgCO2")
print(f"Total: {total_emissions:.4f} kgCO2")
```

### Autres outils de mesure d'impact environnemental

| Outil | Specialite | Methode |
|---|---|---|
| **CodeCarbon** | Mesure en temps reel du CO2 | Power measurement + carbon intensity |
| **ML CO2 Impact** | Estimateur rapide | Formulaire web, estimation par hardware et duree |
| **Carbontracker** | Tracking PyTorch/TF | Measurement power, prediction de l'entrainement total |
| **Experiment Impact Tracker** | Suivi d'experiences | Integration avec MLflow, W&B |
| **Green Algorithms** | Calculateur en ligne | Estimation basee sur le type de calcul |
| **LLMCarbon** | Specifique aux LLMs | Estimation pour l'entrainement et l'inference |

### Strategies de reduction de l'empreinte carbone

#### Optimisation de l'entrainement

- **Early stopping** : Arreter l'entrainement quand la performance plateau. Economie typique : 20-40% d'energie.
- **Transfer learning et fine-tuning** : Reutiliser des modeles pre-entraines au lieu d'entrainer from scratch. Economie : 90-99% par rapport a l'entrainement complet.
- **Knowledge distillation** : Entrainer un modele compact a reproduire les predictions d'un gros modele. Le modele distille consomme typiquement 10-100x moins d'energie a l'inference.
- **Pruning** : Supprimer les parametres non essentiels du modele. Reduction typique : 50-90% des parametres avec < 2% de perte de performance.
- **Mixed precision training** : Utiliser des formats numeriques reduits (FP16, BF16, INT8). Acceleration 2-3x avec reduction proportionnelle de l'energie.
- **Efficient architectures** : Privilegier les architectures efficientes (EfficientNet, MobileNet, DistilBERT) plutot que les modeles massifs quand la tache le permet.

#### Optimisation de l'inference

- **Quantization** : Reduire la precision des poids du modele (FP32 -> INT8, INT4). Reduction de la taille du modele de 2-4x et acceleration proportionnelle.
- **Batching** : Regrouper les requetes d'inference pour maximiser l'utilisation du GPU. Gain d'efficacite typique : 3-10x.
- **Caching** : Cacher les resultats d'inference pour les requetes repetees (semantic caching pour les LLMs).
- **Edge deployment** : Deployer les modeles au plus pres des utilisateurs pour reduire la latence et les transferts reseau.
- **Model serving optimization** : Utiliser des runtimes optimises (ONNX Runtime, TensorRT, vLLM) pour maximiser le throughput par watt.

#### Choix d'infrastructure

- **Datacenter vert** : Privilegier les regions avec un mix energetique a faible intensite carbone. AWS (us-west-2, eu-north-1), GCP (europe-west1, us-central1), Azure (Sweden Central, France Central).
- **Spot instances** : Utiliser des instances spot/preemptible pour l'entrainement (moins cheres et reutilisent la capacite inutilisee).
- **Right-sizing** : Ne pas surdimensionner l'infrastructure. Un GPU A100 est inutile pour un modele de regression logistique.
- **Carbon-aware scheduling** : Planifier les entrainements aux heures ou l'intensite carbone est la plus basse (nuit, week-end, periodes de forte production renouvelable).

### Reporting environnemental

Integrer l'impact environnemental dans la model card :

```markdown
## Environmental Impact

| Metrique | Valeur |
|---|---|
| **Hardware** | 4x NVIDIA A100 80GB |
| **Duree d'entrainement** | 72 heures |
| **Energie consommee** | 2,880 kWh |
| **Emissions CO2** | 432 kgCO2eq |
| **Region datacenter** | eu-west-1 (Irlande) |
| **Intensite carbone** | 150 gCO2/kWh |
| **Energie inference (par 1K requetes)** | 0.5 kWh |
| **Outil de mesure** | CodeCarbon v2.4 |
| **Strategies d'optimisation appliquees** | Mixed precision, early stopping, distillation |
```

---

## Consultation des Parties Prenantes

### Identification des parties prenantes

Utiliser le stakeholder mapping pour identifier toutes les parties prenantes affectees par le systeme d'IA :

```
Cartographie des parties prenantes :

Cercle 1 -- Directement affectees :
  +-- Personnes faisant l'objet de decisions automatisees
  +-- Utilisateurs finaux du systeme
  +-- Operateurs humains supervisant le systeme

Cercle 2 -- Indirectement affectees :
  +-- Communautes dont les membres sont affectes
  +-- Organisations concurrentes ou partenaires
  +-- Regulateurs et autorites de controle

Cercle 3 -- Parties prenantes elargies :
  +-- Societe civile et ONG
  +-- Chercheurs et academiques
  +-- Medias et opinion publique
  +-- Generations futures (pour les impacts long terme)
```

### Methodes de consultation

| Methode | Quand l'utiliser | Avantages | Limites |
|---|---|---|---|
| **Ateliers participatifs** | Phase de conception | Engagement profond, co-creation | Cout, echantillon limite |
| **Enquetes et sondages** | Evaluation d'impact a grande echelle | Representativite, quantitatif | Superficiel, biais de reponse |
| **Entretiens individuels** | Populations vulnerables, sujets sensibles | Profondeur, adaptation | Cout, non generalizable |
| **Focus groups** | Exploration de perceptions et preoccupations | Dynamique de groupe, emergence | Domination par certains participants |
| **Consultations publiques** | Deploiements a grande echelle, secteur public | Legitimite democratique | Auto-selection des participants |
| **Comites consultatifs** | Gouvernance continue | Expertise, suivi dans le temps | Risque de capture, representativite |
| **Bug bounties ethiques** | Detection de biais et de failles | Diversite des perspectives | Cout, coordination |

### Principes de consultation ethique

- **Inclusivite** : S'assurer que les populations les plus affectees et les plus vulnerables sont representees. Ne pas se limiter aux parties prenantes les plus accessibles.
- **Accessibilite** : Adapter le format et le langage au public. Fournir des compensations pour le temps des participants.
- **Transparence** : Expliquer clairement l'objectif de la consultation, comment les retours seront utilises, et quelles decisions sont deja prises.
- **Impact reel** : La consultation doit avoir un impact reel sur les decisions. Documenter comment chaque retour a ete traite (accepte, rejete avec justification, integre partiellement).
- **Retour aux participants** : Communiquer les resultats de la consultation et les decisions prises aux participants.

---

## Monitoring Continu et Audit

### Architecture de monitoring ethique

Deployer une infrastructure de monitoring dediee aux metriques ethiques en complement du monitoring de performance classique :

```
Pipeline de monitoring ethique :

1. Data Collection Layer :
   +-- Predictions du modele (inputs, outputs, scores de confiance)
   +-- Attributs proteges (si disponibles) ou proxies
   +-- Outcomes reels (quand disponibles, avec delai)
   +-- Feedback utilisateurs et reclamations

2. Metrics Computation Layer :
   +-- Fairness metrics sur fenetres glissantes (1h, 24h, 7j, 30j)
   +-- Drift detection par sous-groupe
   +-- Calibration par sous-groupe
   +-- Taux de reclamation par sous-groupe

3. Alerting Layer :
   +-- Seuils d'alerte pour chaque metrique de fairness
   +-- Alertes de drift disproportionne
   +-- Escalade automatique vers le comite d'ethique
   +-- Procedures de rollback automatique

4. Dashboard Layer :
   +-- Tableaux de bord de fairness en temps reel
   +-- Rapports periodiques automatises
   +-- Vue historique et tendances
```

### Frequence d'audit

| Type de systeme | Audit interne | Audit externe | Revue AIA |
|---|---|---|---|
| **Haut risque (EU AI Act)** | Mensuel | Trimestriel | Annuel + sur evenement |
| **Risque modere** | Trimestriel | Semestriel | Annuel |
| **Risque faible** | Semestriel | Annuel | Bisannuel |
| **Post-incident** | Immediat | Dans les 30 jours | Revision immediate |

### Processus d'audit ethique

```
Processus d'audit ethique standardise :

1. Preparation :
   +-- Definir le perimetre de l'audit
   +-- Collecter la documentation (model card, datasheet, AIA, logs)
   +-- Constituer l'equipe d'audit (technique, ethique, juridique, metier)

2. Evaluation technique :
   +-- Reproduire les metriques de performance et de fairness
   +-- Tester la robustesse (adversarial testing)
   +-- Verifier l'explicabilite (generation et validation des explications)
   +-- Auditer les donnees (representativite, qualite, consentement)

3. Evaluation de gouvernance :
   +-- Verifier la documentation (model card, datasheet, AIA)
   +-- Evaluer les processus de supervision humaine
   +-- Verifier les mecanismes de recours
   +-- Auditer les logs et la tracabilite

4. Evaluation d'impact :
   +-- Revoir les incidents signales depuis le dernier audit
   +-- Evaluer les reclamations recues
   +-- Mesurer l'impact reel vs l'impact prevu dans l'AIA
   +-- Consulter les parties prenantes

5. Rapport et actions :
   +-- Rediger le rapport d'audit (constats, risques, recommandations)
   +-- Definir le plan d'action corrective (responsable, echeance, priorite)
   +-- Suivre la mise en oeuvre des actions correctives
   +-- Communiquer les resultats aux parties prenantes
```

### Registre des incidents ethiques

Maintenir un registre structure de tous les incidents ethiques detectes :

```markdown
## Registre des Incidents Ethiques

| ID | Date | Systeme | Severite | Description | Impact | Cause racine | Action corrective | Statut | Responsable |
|---|---|---|---|---|---|---|---|---|---|
| ETH-001 | 2026-01-15 | Credit-Score-v3 | Majeure | Disparate impact detecte sur le genre | FPR 2.3x plus eleve pour les femmes | Proxy bias (secteur d'activite) | Suppression feature, re-entrainement | Resolu | J. Dupont |
| ETH-002 | 2026-01-22 | Recrutement-NLP | Moderee | Biais linguistique detecte | Score 15% plus bas pour les candidats non-natifs | Training data bias | Augmentation donnees, re-evaluation | En cours | M. Martin |
```

---

## Cadres Reglementaires Internationaux

### Vue d'ensemble des cadres reglementaires

| Juridiction | Cadre | Statut | Focus principal |
|---|---|---|---|
| **UE** | EU AI Act | En vigueur (2024-2027) | Classification de risque, obligations par niveau |
| **UE** | RGPD Article 22 | En vigueur (2018) | Decisions automatisees, droit a l'explication |
| **France** | Loi Informatique et Libertes | En vigueur | Protection des donnees, decisions automatisees |
| **Canada** | Directive on Automated Decision-Making | En vigueur (2019) | Secteur public, AIA obligatoire |
| **USA** | NYC Local Law 144 | En vigueur (2023) | Bias audit pour les outils de recrutement automatises |
| **USA** | NIST AI RMF | Volontaire (2023) | Risk management framework |
| **USA** | Blueprint for an AI Bill of Rights | Volontaire (2022) | 5 principes : securite, non-discrimination, vie privee, transparence, alternatives humaines |
| **Chine** | AI regulations (multiples) | En vigueur | Recommandation algorithmique, deep fakes, IA generative |
| **Bresil** | AI Act (projet) | En discussion | Approche basee sur les risques, similaire EU |
| **Singapour** | AI Verify | Volontaire (2022) | Framework de test et de gouvernance |
| **OCDE** | AI Principles | Volontaire (2019) | 5 principes, reference internationale |
| **UNESCO** | Recommendation on AI Ethics | Volontaire (2021) | 10 principes, 4 domaines d'action |

### Tendances reglementaires 2025-2026

- **Convergence globale** : Les cadres reglementaires convergent vers une approche basee sur les risques inspiree du EU AI Act.
- **Obligations de transparence** : Obligations croissantes de disclosure pour les systemes d'IA generative (watermarking, labeling).
- **Audits obligatoires** : Tendance vers l'obligation d'audits independants pour les systemes a haut risque.
- **Responsabilite civile** : La directive europeenne sur la responsabilite en matiere d'IA clarifie les regimes de responsabilite.
- **Droits des travailleurs** : Reglementations emergentes sur l'utilisation de l'IA dans le cadre de l'emploi (surveillance, management algorithmique).

---

## Checklist Impact Assessment

- [ ] Le screening de risque initial est realise
- [ ] Le niveau de risque est attribue et justifie
- [ ] Les impacts sur les individus sont identifies et evalues
- [ ] Les impacts sociaux sont identifies et evalues
- [ ] L'impact environnemental est mesure (CodeCarbon ou equivalent)
- [ ] Les strategies de reduction de l'empreinte carbone sont appliquees
- [ ] L'empreinte carbone est documentee dans la model card
- [ ] Les parties prenantes sont identifiees et cartographiees
- [ ] La consultation des parties prenantes est conduite
- [ ] Les retours des parties prenantes sont documentes et traites
- [ ] Les mesures d'attenuation sont definies pour chaque risque significatif
- [ ] Le rapport d'AIA est redige et approuve
- [ ] Le monitoring ethique est deploye en production
- [ ] Les seuils d'alerte et procedures de rollback sont definis
- [ ] Les audits periodiques sont planifies
- [ ] Le registre des incidents ethiques est maintenu
- [ ] La conformite reglementaire est evaluee pour chaque juridiction pertinente
- [ ] La date de prochaine revue de l'AIA est fixee
