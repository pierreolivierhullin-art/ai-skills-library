# Etudes de Cas — AI Data Privacy & Gouvernance en Pratique

## Vue d'Ensemble

Ces etudes de cas illustrent des implementations reelles de gouvernance IA dans des contextes regulatoires varies : classification EU AI Act dans le secteur RH, audit de biais dans le credit scoring, documentation model cards dans la sante, et conformite GPAI pour un fournisseur de LLM.

---

## Cas 1 — Classification EU AI Act pour un Systeme de Screening RH

### Contexte

Scale-up tech (400 employes, 3 000 candidatures/mois). Un systeme de screening de CV base sur le ML analyse automatiquement les candidatures et attribue un score de pertinence avant qu'un recruteur ne les examine. La DRH souhaite savoir si ce systeme est concerne par l'EU AI Act et quelles obligations s'appliquent.

### Analyse de Classification

**Etape 1 — Verification de l'applicabilite** :
- Le systeme est-il un "systeme IA" au sens de l'EU AI Act ? OUI : algorithme ML avec capacite de generation de contenu (score de pertinence et explication) base sur des donnees d'entrainement.
- La scale-up met-elle ce systeme sur le marche ou l'utilise-t-elle en interne ? Usage interne — le systeme n'est pas commercialise. Les obligations de "fournisseur" allégées, mais obligations de "deployer" maintenus.

**Etape 2 — Classification du niveau de risque** :
Consulter l'Annexe III : categorie 3 — "emploi, gestion des ressources humaines" :
- 3.a : "IA destinee a etre utilise pour le recrutement ou la selection de personnes physiques, notamment pour faire passer des annonces d'emploi, analyser et filtrer les candidatures..." → **RISQUE ELEVE CONFIRME**.

**Etape 3 — Obligations applicables** :

En tant que deployer d'un systeme a risque eleve fourni par un tiers (SaaS RH) :
- Verifier que le fournisseur SaaS est conforme EU AI Act (declaration de conformite, marquage CE)
- Utiliser le systeme conformement aux instructions du fournisseur
- Assurer la surveillance humaine : les scores ne peuvent pas etre le seul critere — un recruteur humain valide toutes les decisions
- Informer les candidats de l'utilisation d'un systeme IA dans le processus de selection
- Conserver des logs des decisions et de leur contexte

**Etape 4 — Actions implementees** :

1. **Information candidats** : Ajout dans la politique de confidentialite et dans la confirmation de candidature d'une mention explicite sur l'utilisation d'un systeme IA de pre-qualification.

2. **Surveillance humaine** : Procedure documentee — aucun candidat n'est elimine sur la seule base du score IA. Tous les scores > 0.4 sont revus par un recruteur.

3. **Droit d'explication** : Les candidats peuvent demander une explication sur les criteres de selection (conformite Article 86 RGPD — droit de ne pas faire l'objet d'une decision purement automatisee).

4. **Audit fournisseur** : Demande de la declaration de conformite EU AI Act au fournisseur SaaS. Le fournisseur ayant 24 mois pour se conformer (deadline aout 2026), accord signé avec engagement de conformite avant deploiement post-aout 2026.

5. **Audit de biais** : Premiere analyse de biais realisee en interne sur 6 mois de donnees : taux de selection par genre et par universite d'origine. Ecart detectable sur les candidats issus d'ecoles moins connues (7.2% de taux de pre-selection vs 14.8% pour les grandes ecoles). Decision : ajout d'une revue humaine systematique pour ce segment.

### Lecons

- La classification EU AI Act n'est pas toujours evidente — les systemes qui "influencent" une decision sans la prendre directement tombent quand meme dans la categorie a risque eleve
- La surveillance humaine n'est pas un vague principe : elle doit etre documentee, formalisee, et auditee
- L'audit de biais a revele un biais contre les ecoles moins connues qui n'etait pas apparent sans analyse systematique

---

## Cas 2 — Audit de Biais dans un Modele de Credit Scoring (Banque Cooperatve)

### Contexte

Banque cooperative regionale (380 000 membres, 4.2 milliards EUR d'encours credit). Le modele de credit scoring a risque de particuliers (LightGBM, en production depuis 2022) fait l'objet d'une revue annuelle obligatoire. Un signalement interne evoque une possible discrimination a l'egard des residents de certaines zones geographiques.

### Processus d'Audit

**Phase 1 — Identification des groupes proteges** :
Consultation avec le DPO, la direction juridique et le service compliance. Groupes retenus :
- Genre (homme/femme)
- Age (< 30 ans, 30-45 ans, 45-60 ans, > 60 ans)
- Zone geographique (Rural/Periurbain/Urbain) — non directement protege mais proxy potentiel de l'origine

**Phase 2 — Extraction et analyse** :

Dataset : 45 000 decisions de credit sur les 12 derniers mois avec labels reels (defaut ou non a 12 mois).

```
Taux d'approbation par zone :
- Urbain (n=28 400) : 74.3%
- Periurbain (n=12 100) : 71.8%
- Rural (n=4 500) : 66.1%

Ecart Urbain/Rural : 8.2 points
Test de significativite : p < 0.001 — ecart statistiquement significatif
```

**Phase 3 — Analyse causale** :

Question : cet ecart est-il justifie par le risque reel, ou reflete-t-il une discrimination ?

Methode : comparer le taux de defaut reel par zone pour les credits accordes, a iso-score de risque.

```
Taux de defaut reel a 12 mois :
- Urbain : 3.2% (pour les approuves avec score 0.3-0.4)
- Periurbain : 3.4%
- Rural : 3.1%

Conclusion : les taux de defaut reels sont similaires entre zones.
L'ecart de 8.2 points d'approbation n'est PAS justifie par le risque reel.
```

**Phase 4 — Identification de la source du biais** :

Analyse SHAP et analyse des features : la variable "ratio credit/revenu" est partiellement correlée avec la zone geographique (les revenus ruraux sont historiquement moins eleves dans la zone de la banque). Le modele a appris un pattern géographique implicite via cette variable.

**Phase 5 — Mitigation** :

Option retenue : seuil de decision differencie par zone geographique (post-processing).

Justification : Cette approche preserve le modele principal (plus simple a maintenir) tout en corrigeant le biais systematique identifies.

Apres calibration : ecart residuel de 1.8 points — non significatif statistiquement.

**Phase 6 — Documentation et Reporting** :

Rapport d'audit presente au :
- Comite des risques (direction)
- DPO et service compliance
- CNIL (dans le cadre de la conformite RGPD pour les decisions automatisees)
- Commissaires aux comptes (dans le rapport de conformite ESG)

### Resultats

- Biais confirme et corrige avant qu'il n'y ait plainte ou controle regulatoire
- La CNIL, informée pro-activement, a salue la demarche : "bonne pratique de gouvernance algorithmique"
- Le rapport d'audit a ete utilise pour justifier la conformite dans le questionnaire ESG de la banque
- Impact financier : ~1 200 dossiers supplementaires approuves par an en zone rurale, pour un encours estime de 18M EUR

---

## Cas 3 — Model Cards et Conformite EU AI Act dans le Secteur Sante

### Contexte

Editeur de logiciels medicaux (200 employes) proposant un systeme d'aide a la decision pour la detection de la pneumonie sur radiographies thoraciques. Le systeme est utilise dans 45 hopitaux. Analyse : le systeme est-il un dispositif medical et/ou soumis a l'EU AI Act ?

### Double Qualification : MDR + EU AI Act

Le systeme est qualifie a la fois :
- **Dispositif medical IA (AI-MDR)** : au sens du Reglement (UE) 2017/745 (MDR), classe IIa — deja certifie CE au moment de l'audit EU AI Act
- **Systeme IA a risque eleve** au sens EU AI Act : categorie 5 (dispositifs medicaux contenant des composantes IA) — Annexe I de l'EU AI Act

Bonne nouvelle : l'EU AI Act prevoit un mecanisme de "safe harbour" pour les dispositifs medicaux deja certifies MDR. Les obligations EU AI Act sont considerees satisfaites si les exigences MDR sont respectees, sous conditions.

### Model Card Implementée

La model card creee est particulierement detaillee compte tenu du contexte medical :

**Performances par sous-groupe** (extrait) :

| Population | AUC | Sensibilite | Specificite |
|---|---|---|---|
| Adultes 18-65 ans | 0.946 | 91.2% | 89.7% |
| Personnes agees > 65 ans | 0.921 | 88.4% | 91.3% |
| Enfants < 15 ans | 0.887 | 84.1% | 88.2% |
| IMC > 30 (obesity) | 0.903 | 85.3% | 90.1% |
| Radiographies basse qualite | 0.842 | 78.6% | 85.4% |

**Facteurs de risque identifies** :
- Performance significativement inferieure sur les patients pediatriques (modele entraine a 78% sur des adultes)
- Usage deconseille comme seul outil de diagnostic pour les < 15 ans
- Obligation de double lecture humaine pour les radiographies basse qualite

**Conformite EU AI Act — Documentation** :
- Article 11 (documentation technique) : satisfait via la documentation MDR enrichie
- Article 13 (transparence) : manuel d'utilisation mis a jour avec les limitations par sous-groupe
- Article 14 (surveillance humaine) : le systeme ne "decide" pas — il fournit une aide (score de probabilite). La decision finale reste au radiologue. Cette architecture satisfait le principe de surveillance humaine.
- Article 15 (robustesse) : tests de robustesse aux variations d'equipment (differents fabricants de scanners) documentes

### Lecons

- La double qualification MDR + EU AI Act n'est pas redondante : le MDR couvre la securite du dispositif, l'EU AI Act couvre la gouvernance IA (biais, transparence, surveillance humaine)
- Les model cards medicales doivent couvrir les sous-populations cliniquement pertinentes — pas seulement des attributs socio-demographiques
- Le "safe harbour" MDR/EU AI Act simplifie la conformite mais exige de verifier que la documentation MDR couvre bien toutes les exigences EU AI Act

---

## Cas 4 — Conformite GPAI pour un Fournisseur de LLM (Startup IA)

### Contexte

Startup francaise (60 employes) ayant developpe un LLM specialise dans le traitement de documents juridiques. Le modele est integre dans une API consommee par des cabinets d'avocats et des departements juridiques d'entreprises. Question : le modele est-il soumis aux obligations GPAI de l'EU AI Act ?

### Analyse GPAI

**Criteres de qualification GPAI (Article 51)** :
- Le modele est-il un "modele IA a usage general" ? OUI : entraine sur un large corpus, avec une haute generalite, utilisable dans de multiples contextes (extraction d'information, analyse de contrats, generation de resumes, Q&A juridique).
- Puissance de calcul d'entrainement > 10^25 FLOPs (risque systemique) ? NON — le modele est de taille moyenne (7B parametres, training sur 500 GPU-heures). Pas de risque systemique.

**Obligations GPAI standard applicables** :

1. **Documentation technique** : Schema de l'architecture, description du corpus d'entrainement, performances, evaluation.

2. **Politique d'utilisation acceptable** (Terms of Use) :
```
Usages autorises :
- Analyse et extraction d'information dans des documents juridiques
- Generation de resumes de contrats
- Q&A sur des bases documentaires juridiques avec citations
- Aide a la redaction de correspondance juridique standard

Usages interdits :
- Utilisation comme seul fondement d'une decision judiciaire
- Substitution a l'avis d'un avocat qualifie
- Traitement de donnees personnelles sans base legale RGPD
- Formation de personnes sans supervision
- Deploiement dans des systemes autonomes de decision legale
```

3. **Conformite copyright** : Le corpus d'entrainement a ete constitue de :
- Jurisprudences et textes de loi (domaine public)
- Contrats commerciaux anonymises (consentement obtenu)
- Bases de donnees juridiques licenciees (Dalloz, LexisNexis — licence training)
Le registre du droit d'auteur et les accords de licence sont documentes.

4. **Cooperation aval** : Les deployers (cabinets d'avocats) recoivent la documentation technique et les instructions d'utilisation. Systeme de notification si une mise a jour majeure change les performances.

**Point de vigilance : classification des deploiements** :

Un cabinet d'avocat qui integre ce LLM dans un systeme automatise de triage des affaires pourrait faire basculer le systeme integre dans la categorie "risque eleve" (categorie 7 — administration de la justice). Dans ce cas, le cabinet d'avocat (deployer devenant en realite fournisseur d'un systeme derive) devrait respecter les obligations du risque eleve.

Mesure prise : clause contractuelle avec les clients imposant de notifier l'editeur en cas d'integration dans un systeme a risque eleve, et de respecter les obligations correspondantes.

### Resultats

- Conformite GPAI documentee avant la deadline d'aout 2025
- Avantage commercial : premier acteur LegalTech francais avec documentation GPAI complete — argument de vente aupres des grands cabinets avec departements compliance
- Audit externe par un cabinet specialise EU AI Act : conformite validee, rapport utilise dans les appels d'offres publics
