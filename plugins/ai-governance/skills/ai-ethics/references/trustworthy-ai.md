# Trustworthy AI -- EU Requirements, Human Oversight, Privacy & Accountability

Reference complete sur l'IA digne de confiance (Trustworthy AI). Couvre les 7 exigences de l'UE pour une IA de confiance, les mecanismes de supervision humaine, la robustesse et la securite, l'IA respectueuse de la vie privee (federated learning, differential privacy), les frameworks de responsabilite et le EU AI Act. Ce document sert de guide operationnel pour les responsables de gouvernance IA, les equipes techniques, les juristes et les risk managers.

---

## EU Trustworthy AI -- Les 7 Exigences

Le High-Level Expert Group on Artificial Intelligence (AI HLEG) de la Commission europeenne a defini en 2019 les lignes directrices pour une IA digne de confiance. Ces 7 exigences constituent le cadre de reference europeen et influencent directement le EU AI Act.

### Exigence 1 -- Human Agency and Oversight

#### Principes

L'IA doit soutenir l'autonomie humaine et la prise de decision, pas la remplacer. Les systemes d'IA doivent permettre aux humains de prendre des decisions eclairees et de conserver un controle significatif.

#### Niveaux de supervision humaine

| Niveau | Description | Cas d'usage | Implementation |
|---|---|---|---|
| **Human-in-the-Loop (HITL)** | L'humain valide chaque decision avant execution | Decisions a fort impact individuel (credit, sante, justice) | File de validation, interface de revue, approbation obligatoire |
| **Human-on-the-Loop (HOTL)** | L'humain supervise en continu et peut intervenir | Decisions semi-automatisees, systemes a risque modere | Dashboards de monitoring, alertes, capacite d'override |
| **Human-in-Command (HIC)** | L'humain definit les objectifs et les limites, supervise le systeme a haut niveau | Gouvernance strategique, systemes autonomes encadres | Comites de gouvernance, audits, kill switches |

#### Implementation du Human-in-the-Loop

```
Architecture HITL pour decisions a fort impact :

1. Systeme IA genere une recommandation + score de confiance + explication
2. Routage vers revue humaine :
   +-- Confiance >= seuil_haut ET pas de flag d'alerte
   |   --> Revue humaine optionnelle (echantillonnage qualite)
   +-- Confiance entre seuil_bas et seuil_haut
   |   --> Revue humaine systematique avec recommandation IA
   +-- Confiance < seuil_bas OU flag d'alerte
       --> Revue humaine obligatoire sans recommandation IA
       (eviter l'anchoring bias)

3. L'humain peut :
   +-- Accepter la recommandation
   +-- Modifier la recommandation (avec justification)
   +-- Rejeter la recommandation (avec justification)
   +-- Escalader vers un comite

4. Feedback loop :
   +-- Les decisions humaines alimentent le re-entrainement
   +-- Les desaccords homme-machine sont analyses
   +-- Les seuils de confiance sont recalibres periodiquement
```

#### Risques de l'automation bias

L'automation bias est la tendance des humains a suivre systematiquement la recommandation de la machine, rendant la supervision humaine inefficace. Strategies de mitigation :

- **Ne pas montrer la recommandation IA en premier** : Demander au superviseur humain de former son propre jugement avant de voir la recommandation.
- **Varier la presentation** : Alterner les cas ou l'IA a raison et ceux ou elle a tort (pour les exercices d'entrainement).
- **Metriques de desaccord** : Monitorer le taux de desaccord homme-machine. Un taux < 5% est un signal d'alerte d'automation bias.
- **Rotation et temps de decision** : Eviter la fatigue decisionnelle par la rotation des operateurs et des temps de decision adequats.
- **Formation continue** : Former les superviseurs aux biais cognitifs, aux limites du modele et aux cas limites.

### Exigence 2 -- Technical Robustness and Safety

#### Robustesse face aux attaques adversariales

Les modeles d'IA sont vulnerables aux attaques adversariales -- des perturbations imperceptibles des inputs qui provoquent des predictions erronees :

**Types d'attaques** :

| Type | Description | Exemple | Defense |
|---|---|---|---|
| **Evasion** | Modification des inputs a l'inference | Image perturbee qui trompe un classifieur | Adversarial training, input sanitization |
| **Poisoning** | Contamination des donnees d'entrainement | Injection de donnees biaisees dans le training set | Data validation, anomaly detection |
| **Model extraction** | Vol du modele par queries repetees | Reconstruction d'un modele proprietaire | Rate limiting, watermarking, query auditing |
| **Data extraction** | Extraction de donnees d'entrainement | Membership inference attack | Differential privacy, regularization |
| **Prompt injection** | Manipulation des instructions d'un LLM | Injection de directives malveillantes | Input filtering, output validation, guardrails |

**Strategies de defense** :

- **Adversarial training** : Entrainer le modele sur des exemples adversariaux generes automatiquement. Augmente la robustesse mais peut degrader la performance nominale de 1-3%.
- **Input validation** : Detecter les inputs anomaux avant l'inference (out-of-distribution detection, statistical tests). Rejeter ou flagger les inputs suspects.
- **Ensemble defenses** : Utiliser des ensembles de modeles avec des architectures differentes. Les attaques transferables entre modeles differents sont plus difficiles a creer.
- **Certified defenses** : Methodes qui fournissent des garanties mathematiques de robustesse dans un rayon epsilon autour de chaque input (randomized smoothing, IBP -- Interval Bound Propagation).
- **Red teaming** : Conduire regulierement des exercices de red teaming specifiques a l'IA pour identifier les vulnerabilites. Inclure des attaques adversariales, du prompt injection testing et des tests de robustesse.

#### Fiabilite et fallback

Concevoir des mecanismes de fallback pour les cas ou le modele echoue :

```
Strategie de fallback en couches :

1. Confidence thresholding :
   +-- Score de confiance > seuil_high --> Prediction automatisee
   +-- Score de confiance entre seuil_low et seuil_high --> Prediction + flag
   +-- Score de confiance < seuil_low --> Fallback vers :
       +-- Modele de fallback (plus simple, plus robuste)
       +-- Regle metier deterministe
       +-- Intervention humaine
       +-- Refus de predire avec message explicatif

2. Input anomaly detection :
   +-- Input in-distribution --> Processus normal
   +-- Input out-of-distribution --> Fallback + alerte

3. Monitoring des metriques de production :
   +-- Metriques dans les limites --> Fonctionnement normal
   +-- Drift detecte --> Alerte + augmentation du taux de supervision
   +-- Degradation significative --> Rollback automatique vers version precedente
```

### Exigence 3 -- Privacy and Data Governance

#### Privacy-Preserving AI

##### Federated Learning (Apprentissage federe)

Le federated learning permet d'entrainer un modele sur des donnees distribuees sans centraliser les donnees brutes :

```
Architecture Federated Learning :

1. Serveur central envoie le modele global aux participants
2. Chaque participant entraine le modele sur ses donnees locales
3. Chaque participant envoie les mises a jour (gradients ou poids) au serveur
4. Le serveur agregue les mises a jour (FedAvg, FedProx, SCAFFOLD)
5. Le nouveau modele global est redistribue
6. Repeter jusqu'a convergence

Variantes :
+-- Cross-device FL : millions de devices (mobiles, IoT)
|   Challenges : heterogeneite, disponibilite, communication
+-- Cross-silo FL : quelques organisations (hopitaux, banques)
    Challenges : heterogeneite des donnees, confidentialite inter-organismes
```

**Frameworks** :

| Framework | Developpe par | Specialite |
|---|---|---|
| **Flower** | Flower Labs | Framework unifie, flexible, production-ready |
| **PySyft** | OpenMined | Privacy-preserving ML, integration PyTorch |
| **TensorFlow Federated** | Google | Integration TF, simulation et production |
| **FATE** | WeBank | Cross-silo FL pour la finance |
| **NVFlare** | NVIDIA | FL pour la sante et les donnees sensibles |
| **FedML** | FedML Inc | Multi-plateforme, edge et cloud |

**Risques residuels du federated learning** :

- **Gradient inversion attacks** : Il est possible de reconstruire partiellement les donnees d'entrainement a partir des gradients partages. Mitigation : ajout de bruit (differential privacy), compression des gradients (gradient compression), secure aggregation (cryptographie).
- **Model poisoning** : Un participant malveillant peut envoyer des mises a jour empoisonnees. Mitigation : robust aggregation (median, trimmed mean, Krum), anomaly detection sur les mises a jour.
- **Free-rider problem** : Certains participants beneficient du modele sans contribuer reellement. Mitigation : contribution scoring, incentive mechanisms.

##### Differential Privacy (Confidentialite differentielle)

La differential privacy fournit des garanties mathematiques sur la protection de la vie privee des individus dans le dataset :

```
Definition formelle (epsilon-differential privacy) :

Pour tout sous-ensemble de sorties S et pour tout couple de datasets
D et D' differant d'un seul individu :

P(M(D) in S) <= e^epsilon * P(M(D') in S)

Ou :
- M est le mecanisme (algorithme) utilise
- epsilon est le budget de privacy (plus petit = plus protege)
- delta est la probabilite de violation (pour (epsilon, delta)-DP)

Interpretation : la presence ou l'absence d'un individu dans le dataset
modifie au plus les probabilites de sortie d'un facteur e^epsilon.
```

**Implementation pratique** :

```python
# Differential Privacy avec Opacus (PyTorch)
from opacus import PrivacyEngine

# Attacher le PrivacyEngine au modele et a l'optimizer
privacy_engine = PrivacyEngine()
model, optimizer, data_loader = privacy_engine.make_private_with_epsilon(
    module=model,
    optimizer=optimizer,
    data_loader=train_loader,
    epochs=num_epochs,
    target_epsilon=1.0,       # Budget de privacy
    target_delta=1e-5,        # Probabilite de violation
    max_grad_norm=1.0         # Clipping des gradients
)

# Entrainement standard -- Opacus ajoute automatiquement le bruit
for epoch in range(num_epochs):
    for batch in data_loader:
        optimizer.zero_grad()
        loss = criterion(model(batch.data), batch.target)
        loss.backward()
        optimizer.step()

# Verifier le budget de privacy consomme
epsilon = privacy_engine.get_epsilon(delta=1e-5)
print(f"Epsilon consomme : {epsilon}")
```

**Choix du budget epsilon** :

| Epsilon | Niveau de protection | Impact performance | Cas d'usage |
|---|---|---|---|
| 0.1 - 1.0 | Tres forte protection | Degradation significative (5-15%) | Donnees medicales, genetiques |
| 1.0 - 5.0 | Protection forte | Degradation moderee (2-5%) | Donnees financieres, personnelles |
| 5.0 - 10.0 | Protection moderee | Degradation faible (< 2%) | Donnees comportementales, analytics |
| > 10.0 | Protection faible | Impact negligeable | Statistiques agregees, tendances |

##### Autres techniques de privacy-preserving AI

- **Secure Multi-Party Computation (SMPC)** : Permet a plusieurs parties de calculer conjointement une fonction sans reveler leurs donnees respectives. Protocoles : secret sharing (Shamir, additive), garbled circuits, oblivious transfer. Tres couteux en communication et en calcul.

- **Homomorphic Encryption (HE)** : Permet d'effectuer des calculs sur des donnees chiffrees sans les dechiffrer. Variantes : partially HE (Paillier -- addition uniquement), somewhat HE (nombre limite d'operations), fully HE (FHE -- toutes les operations). FHE est 10^4 a 10^6 fois plus lent que le calcul en clair mais les progres sont rapides (librairies SEAL, TFHE, Concrete).

- **Trusted Execution Environments (TEE)** : Enclaves materielles securisees (Intel SGX, ARM TrustZone, AMD SEV) qui isolent le calcul et les donnees. Offrent de bonnes performances mais dependent de la securite du hardware.

- **Synthetic Data Generation** : Generer des donnees synthetiques qui preservent les proprietes statistiques du dataset original sans contenir de donnees personnelles. Valider avec des metriques de fidelite statistique et de privacy (membership inference attacks sur les donnees synthetiques).

### Exigence 4 -- Transparency

Voir le fichier de reference detaille : [Explainability & Transparency](./explainability-transparency.md).

Les elements cles de la transparence couvrent :

- **Tracabilite** : Documenter les donnees, les processus et les decisions tout au long du cycle de vie.
- **Explicabilite** : Fournir des explications adaptees au public cible.
- **Communication** : Informer les parties prenantes des capacites et des limites du systeme.

### Exigence 5 -- Diversity, Non-discrimination and Fairness

Voir le fichier de reference detaille : [Bias & Fairness](./bias-fairness.md).

Les elements cles couvrent :

- **Eviter les biais injustes** : Detection et attenuation des biais algorithmiques.
- **Accessibilite** : Concevoir des systemes accessibles a tous, y compris les personnes handicapees (WCAG pour les interfaces, multilinguisme).
- **Participation des parties prenantes** : Impliquer des representants divers dans la conception et l'evaluation.

### Exigence 6 -- Societal and Environmental Well-being

#### Impact social

- Evaluer l'impact sur l'emploi (deplacement de postes, creation de nouveaux roles, besoin de requalification).
- Evaluer l'impact sur la cohesion sociale (renforcement ou reduction des inegalites).
- Evaluer l'impact sur la democratie et les droits fondamentaux.
- Evaluer l'impact sur la sante mentale (addiction, manipulation, desinformation).

#### Impact environnemental

Voir le fichier de reference detaille : [Impact Assessment](./impact-assessment.md) pour les methodes de mesure de l'empreinte carbone.

Les modeles d'IA ont un impact environnemental significatif :

| Phase | Empreinte | Strategies de reduction |
|---|---|---|
| **Entrainement** | 60-80% de l'empreinte totale | Distillation, pruning, early stopping, choix de datacenter vert |
| **Inference** | 20-40% (cumule sur la duree de vie) | Quantization, caching, batching, edge deployment |
| **Stockage** | Variable | Compression, nettoyage des checkpoints, lifecycle management |
| **Donnees** | Significatif pour les gros datasets | Data-efficient methods, transfer learning, few-shot |

### Exigence 7 -- Accountability

#### Frameworks de responsabilite

La responsabilite (accountability) se decline en plusieurs dimensions :

- **Auditabilite** : Capacite a examiner et evaluer les algorithmes, les donnees et les processus de decision. Implique le logging exhaustif, la versioning des modeles et des donnees, et la reproductibilite des resultats.

- **Responsabilite juridique** : Identification claire des personnes et organisations responsables du systeme d'IA a chaque etape (developpeur, deployer, utilisateur). Le EU AI Act introduit une chaine de responsabilite explicite.

- **Mecanismes de recours** : Procedures accessibles et effectives pour contester les decisions automatisees. Droit a une intervention humaine, droit d'exprimer son point de vue, droit d'obtenir une explication.

- **Reporting et communication** : Publication reguliere de rapports de transparence, de model cards, et de metriques de fairness. Communication proactive sur les incidents et les mesures correctives.

---

## EU AI Act -- Cadre Reglementaire

### Classification des risques

Le EU AI Act classe les systemes d'IA en quatre categories de risque :

```
Pyramide de risque EU AI Act :

Risque inacceptable (Interdit - Article 5)
  +-- Manipulation subliminale
  +-- Exploitation de vulnerabilites (age, handicap)
  +-- Social scoring par les autorites publiques
  +-- Identification biometrique en temps reel dans l'espace public
      (sauf exceptions securitaires strictes)

Haut risque (Annexe III - Articles 6-51)
  +-- Biometrie et categorisation
  +-- Infrastructure critique (transport, energie, eau)
  +-- Education et formation professionnelle
  +-- Emploi et gestion du personnel
  +-- Acces aux services essentiels (credit, assurance, aide sociale)
  +-- Repression et justice
  +-- Migration et controle des frontieres
  +-- Administration de la justice et processus democratiques

Risque limite (Articles 52)
  +-- Chatbots et systemes d'interaction
  +-- Deep fakes et contenu genere
  +-- Systemes de reconnaissance des emotions
  +-- Systemes de categorisation biometrique

Risque minimal
  +-- La majorite des systemes d'IA
  +-- Codes de conduite volontaires
```

### Obligations pour les systemes a haut risque

| Obligation | Article | Description | Implementation |
|---|---|---|---|
| **Risk management** | Art. 9 | Systeme de gestion des risques tout au long du cycle de vie | Registre des risques, evaluation continue |
| **Data governance** | Art. 10 | Qualite, representativite, absence de biais des donnees | Datasheets, audits de donnees |
| **Documentation technique** | Art. 11 | Documentation detaillee avant mise sur le marche | Model cards etendues |
| **Record-keeping** | Art. 12 | Logging automatique des operations | Systemes de logging, retention |
| **Transparency** | Art. 13 | Instructions d'utilisation claires | Documentation utilisateur |
| **Human oversight** | Art. 14 | Mesures de supervision humaine | HITL/HOTL/HIC |
| **Accuracy & robustness** | Art. 15 | Performance, robustesse, cybersecurite | Tests, adversarial testing |
| **Conformity assessment** | Art. 43 | Evaluation de conformite | Auto-evaluation ou par tiers |
| **Registration** | Art. 51 | Enregistrement dans la base UE | Base de donnees europeenne |

### Calendrier d'application

```
Timeline EU AI Act :

Aout 2024  : Entree en vigueur du reglement
Fevrier 2025 : Interdictions (risque inacceptable) applicables
Aout 2025  : Obligations pour les modeles GPAI (General Purpose AI)
Aout 2026  : Obligations pour les systemes a haut risque (Annexe III)
Aout 2027  : Toutes les obligations applicables
```

### General Purpose AI (GPAI) -- Obligations specifiques

Le EU AI Act introduit des obligations specifiques pour les modeles d'IA a usage general (foundation models, LLMs) :

- **Tous les modeles GPAI** : Documentation technique, respect du droit d'auteur, publication d'un resume des donnees d'entrainement.
- **Modeles GPAI a risque systemique** (> 10^25 FLOPs d'entrainement) : Evaluation et attenuation des risques systemiques, red teaming, reporting des incidents graves, cybersecurite, reporting de l'empreinte energetique.

---

## Frameworks d'Audit et de Certification

### ALTAI (Assessment List for Trustworthy AI)

L'ALTAI est un outil d'auto-evaluation developpe par le AI HLEG pour evaluer la conformite aux 7 exigences. Il se presente sous la forme d'un questionnaire structure :

```
Structure ALTAI (par exigence) :

Pour chaque exigence :
1. L'exigence a-t-elle ete consideree dans la conception ?     [Oui/Non/Partiellement]
2. Quelles mesures ont ete mises en place ?                     [Description]
3. Comment sont-elles evaluees ?                                 [Metriques/Processus]
4. Quels sont les risques residuels identifies ?                 [Liste]
5. Quelles sont les actions d'amelioration planifiees ?          [Plan d'action]
```

### Standards ISO

| Standard | Scope | Statut |
|---|---|---|
| **ISO/IEC 42001** | Systeme de management de l'IA | Publie (2023) |
| **ISO/IEC 23894** | Risk management pour l'IA | Publie (2023) |
| **ISO/IEC 24027** | Bias in AI systems and AI aided decision making | Publie (2021) |
| **ISO/IEC 24028** | Trustworthiness in AI | Publie (2020) |
| **ISO/IEC 24029** | Assessment of robustness of neural networks | Publie (2021) |
| **ISO/IEC 42005** | AI system impact assessment | Publie (2024) |
| **ISO/IEC 42006** | Requirements for bodies auditing AI | Publie (2024) |

### NIST AI Risk Management Framework (AI RMF)

Le NIST AI RMF 1.0 (2023) fournit un cadre de gestion des risques IA structure en 4 fonctions :

1. **GOVERN** : Etablir la culture et les structures de gouvernance IA.
2. **MAP** : Cartographier les contextes d'utilisation, les parties prenantes et les risques.
3. **MEASURE** : Mesurer les risques identifies avec des metriques appropriees.
4. **MANAGE** : Gerer les risques par des actions de mitigation, de monitoring et de communication.

---

## Checklist Trustworthy AI

- [ ] Les 7 exigences de l'UE sont evaluees pour chaque systeme d'IA
- [ ] Le niveau de risque EU AI Act est determine
- [ ] Les obligations correspondantes sont identifiees et planifiees
- [ ] Le mecanisme de supervision humaine est defini (HITL/HOTL/HIC)
- [ ] Les risques d'automation bias sont evalues et mitiges
- [ ] La robustesse face aux attaques adversariales est testee
- [ ] Les mecanismes de fallback sont implementes
- [ ] Les techniques de privacy-preserving AI sont evaluees
- [ ] Le budget de privacy (epsilon) est defini et justifie
- [ ] L'empreinte environnementale est mesuree et optimisee
- [ ] Les mecanismes de recours sont disponibles et accessibles
- [ ] L'ALTAI est complete pour chaque systeme
- [ ] La conformite aux standards ISO pertinents est evaluee
- [ ] Le registre des systemes d'IA est maintenu a jour
