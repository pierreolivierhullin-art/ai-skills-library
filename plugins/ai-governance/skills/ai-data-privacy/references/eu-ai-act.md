# EU AI Act — Classification, Obligations & Conformite

## Vue d'Ensemble

L'EU AI Act (Reglement (UE) 2024/1689) est le premier cadre reglementaire contraignant au monde sur l'intelligence artificielle. Il s'applique a tous les systemes IA mis sur le marche ou en service dans l'UE, independamment du lieu d'etablissement du fournisseur. Son approche est basee sur le risque : les obligations sont proportionnelles a l'impact potentiel du systeme sur les droits fondamentaux et la sante des personnes.

---

## Champ d'Application

### Qui est concerne ?

**Fournisseur** (Provider) : Toute entite qui developpe un systeme IA ou un modele GPAI et le met sur le marche ou en service. Obligations les plus etendues.

**Deploiement** (Deployer) : Toute entite qui utilise un systeme IA fourni par un tiers dans ses propres activites professionnelles. Obligations de supervision et d'information des utilisateurs.

**Importateur** : Entite UE qui importe des systemes IA de pays tiers.

**Distributeur** : Toute entite qui met a disposition un systeme IA sur le marche sans le modifier.

**Cas particulier** : Systemes IA utilises en usage interne uniquement (deployed by and for the same legal entity) → allegements potentiels, mais obligations de surveillance humaine maintenues pour les IA a risque eleve.

### Exemptions

- Systemes a usage militaire, national security, defense
- Recherche scientifique (sous conditions)
- Open source (sous conditions — les modeles GPAI open source ont des obligations allegees sauf si risque systemique)
- Usage purement personnel non professionnel

---

## Classification Detaillee

### Risque Inacceptable — Interdit (Article 5)

**Manipulation comportementale subliminale** : techniques affectant le comportement d'une personne sans qu'elle en soit consciente, portant atteinte a sa capacite de decision. Ex : publicite subliminale, dark patterns cognitifs exploitant des biais inconscients.

**Exploitation de la vulnerabilite** : IA qui exploite l'age, le handicap ou la situation sociale defavorisee pour influencer une decision. Ex : systeme ciblant les personnes en difficultés financieres pour des prets predateurs.

**Scoring social public** : evaluation et classement des personnes physiques par des autorites publiques sur la base de leur comportement social. Ex : systeme de credit social a la chinoise.

**Prediction d'infractions** : IA predisant le risque criminal sur la base de profiling, sans acte objectif ni comportement specifique.

**Base de donnees de reconnaissance faciale par scraping** : compilation de bases de donnees de reconnaissance faciale par scraping non cible (ex: Clearview AI).

**Reconnaissance d'emotions** (avec exceptions) :
- Au travail et dans l'education → interdit
- Exception : usage medical (neurologie, psychiatrie) ou securite (detecter la somnolence des conducteurs)

**Identification biometrique en temps reel dans l'espace public** :
- Principe : interdit
- Exceptions tres encadrees : recherche d'un suspect de crime grave, prevention de menaces terroristes, recherche de victimes. Requiert autorisation judiciaire ou de l'autorite de controle.

### Risque Eleve — Obligations Strictes (Annexe III)

**Categorisation complete** :

```
ANNEXE III — Systemes IA a risque eleve

1. COMPOSANTS DE SECURITE
   1.a — Gestion du trafic routier
   1.b — Alimentation en eau, gaz, chauffage, electricite
   1.c — Infrastructures critiques (finance, sante)

2. EDUCATION ET FORMATION
   2.a — Acces ou admission aux etablissements d'enseignement
   2.b — Evaluation des acquis (notation automatisee)
   2.c — Surveillance des examens

3. EMPLOI ET GESTION RH
   3.a — Recrutement et selection (CV screening, entretiens IA)
   3.b — Decisions affectant les conditions de travail (promotion, licenciement)
   3.c — Evaluation des performances

4. ACCES AUX SERVICES ESSENTIELS
   4.a — Credit scoring et evaluation de solvabilite
   4.b — Souscription d'assurance
   4.c — Evaluation d'eligibilite aux prestations sociales
   4.d — Services d'urgence (priorisation des appels)

5. APPLICATION DE LA LOI
   5.a — Evaluation du risque individuel de recidive
   5.b — Evaluation de la fiabilite des preuves
   5.c — Profilage des personnes lors d'enquetes penales
   5.d — Detection et reconnaissance d'emotions

6. MIGRATION ET ASILE
   6.a — Evaluation du risque lié a l'immigration irreguliere
   6.b — Examen des demandes d'asile
   6.c — Controles aux frontieres

7. ADMINISTRATION DE LA JUSTICE
   7.a — Assistance aux autorites judiciaires pour la recherche
   7.b — IA d'aide a la decision judiciaire

8. PARTICIPATION DEMOCRATIQUE
   8.a — Influence sur les elections (ciblage electoral par IA)
   8.b — Influence sur les referendums
```

### Obligations Detaillees pour les IA a Risque Eleve

**Article 9 — Systeme de gestion des risques** :
- Processus continu tout au long du cycle de vie
- Identification et analyse des risques connus et previsibles
- Mesures de gestion des risques proportionnees
- Tests d'adequation avant mise sur le marche

**Article 10 — Gouvernance des donnees d'entrainement** :
- Pratiques de gouvernance documentees
- Examen des biais potentiels
- Mesures pour identifier et corriger les biais
- Lacunes et incertitudes documentees

**Article 11 — Documentation technique** (cf. Annexe IV) :
```
Contenu minimum de la documentation technique :
1. Description generale du systeme IA (capacites, limitations)
2. Description des elements du systeme (architecture, algorithmes, donnees)
3. Description des processus de developpement
4. Description des performances (metriques, tests realisés)
5. Gestion des risques
6. Mesures de cybersecurite
7. Instructions d'utilisation
```

**Article 12 — Journalisation automatique (logs)** :
- Enregistrement automatique des evenements tout au long du cycle de vie
- Niveaux de robustesse des logs proportionnels au risque
- Conservation des logs en accord avec les durees d'utilisation legale

**Article 13 — Transparence** :
- Documentation claire et comprehensible pour les deployers
- Information sur les capacites et limitations
- Niveau de precision et metriques de performance
- Conditions de maintenance

**Article 14 — Surveillance humaine** :
- Le systeme doit etre concevable pour permettre la surveillance humaine
- Les deployers doivent nommer des personnes habilitees a superviser
- Capacite d'intervention, deconnexion ou remplacement par decisions humaines

**Article 15 — Robustesse, precision, cybersecurite** :
- Niveau de precision adequat au cas d'usage
- Robustesse aux erreurs, fautes ou inconsistances
- Resistance aux manipulations (prompt injection, data poisoning)

**Article 17 — Systeme de management de la qualite** :
- Politiques de conformite documentees
- Procedures de gestion des ressources
- Procedures de gestion des donnees
- Procedures de gestion des risques
- Procedures post-marche (surveillance, incidents)

**Article 43 — Evaluation de la conformite** :
- Pour la plupart des cas : auto-evaluation avec documentation
- Pour certains cas sensibles (biometrie, infrastructures critiques) : evaluation par un organisme notifie tiers (Notified Body)

**Article 49 — Declaration de conformite UE et marquage CE** :
- Declaration signable par le representant autorise
- Marquage CE obligatoire sur les systemes a risque eleve

### Risque Limite — Transparence

**Chatbots et agents conversationnels** :
Obligation d'informer les utilisateurs qu'ils interagissent avec un systeme IA, SAUF si c'est evident dans le contexte. L'information doit etre donnee au plus tard au debut de l'interaction.

**Deep fakes et contenu synthetique** :
Les contenus generes par IA qui representent des personnes reelles ou des evenements fictifs doivent etre clairement labellises comme tels. Standards techniques en cours (C2PA — Coalition for Content Provenance and Authenticity).

**IA d'emotion et biometrie limitee** :
Notification aux personnes concernees de maniere appropriee.

### GPAI — General Purpose AI Models (Articles 51-55)

**Modeles IA a usage general** : modeles entraine sur de grandes quantites de donnees avec une haute generalite (LLMs, modeles de diffusion d'image).

**Obligations de base pour tous les GPAI** :
- Documentation technique
- Politique d'utilisation acceptable
- Conformite copyright (signaler si systeme d'opt-out pour le training)
- Cooperation avec les fournisseurs en aval

**Modeles a risque systemique** (puissance de calcul > 10^25 FLOPs) :
- Evaluation adversariale (red teaming)
- Reporting des incidents serieux a la Commission europeenne
- Cybersecurite renforcee
- Rapport sur la consommation energetique

---

## Timeline et Mise en Application

### Planning d'Entree en Vigueur

| Date | Evenement |
|---|---|
| 1er aout 2024 | Entree en vigueur du reglement |
| 2 fevrier 2025 | IA interdites (Article 5) applicables |
| 2 aout 2025 | GPAI (Articles 51-55) applicables |
| 2 aout 2026 | IA a risque eleve (Annexe III) applicables |
| 2 aout 2027 | Systemes existants (mis sur marche avant aout 2026) applicables |

### Autorites de Surveillance

**Au niveau europeen** :
- **AI Office** (Commission europeenne) : surveillance des GPAI et modeles a risque systemique
- **European AI Board** : coordination des autorites nationales

**Au niveau national** :
- France : **CNIL** (pour les applications touchant aux donnees personnelles) + autorite nationale IA en cours de designation
- Chaque Etat membre designe sa propre autorite de surveillance

---

## Checklist de Conformite EU AI Act

### Pour les Fournisseurs de Systemes IA a Risque Eleve

**Phase de developpement**
- [ ] Systeme classe "a risque eleve" (verification Annexe III)
- [ ] Systeme de gestion des risques documente (Article 9)
- [ ] Gouvernance des donnees d'entrainement documentee (Article 10)
- [ ] Documentation technique Annexe IV reddigee (Article 11)
- [ ] Architecture de journalisation en place (Article 12)

**Phase de mise en conformite**
- [ ] Documentation de transparence pour les deployers (Article 13)
- [ ] Mecanismes de surveillance humaine concus (Article 14)
- [ ] Tests de robustesse et precision realises (Article 15)
- [ ] Systeme de management qualite etabli (Article 17)
- [ ] Evaluation de conformite realisee (Article 43)
- [ ] Declaration de conformite UE signee (Article 49)
- [ ] Marquage CE apprime si applicable

**Post-deploiement**
- [ ] Systeme de surveillance post-marche en place
- [ ] Procedure de reporting incidents serieux
- [ ] Registre EU des systemes IA a risque eleve (inscription)

### Pour les Deployers

- [ ] Instructions du fournisseur appliquees
- [ ] Personnes responsables de la surveillance humaine designees
- [ ] Monitoring de l'utilisation conforme aux instructions
- [ ] Procedure de notification du fournisseur en cas de risque/incident
- [ ] Information des utilisateurs sur l'utilisation de l'IA

---

## Sanctions EU AI Act

| Type de violation | Amende maximale |
|---|---|
| Violations des interdictions (Article 5) | 35 millions EUR ou 7% du CA mondial |
| Autres violations (risque eleve, GPAI) | 15 millions EUR ou 3% du CA mondial |
| Informations incorrectes fournies | 7.5 millions EUR ou 1% du CA mondial |
| Reductions pour PME et start-ups | Proportionnel, plafond inferieur |
