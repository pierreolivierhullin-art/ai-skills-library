# Études de cas — IT / Systèmes d'information

## Cas 1 : Migration cloud stratégique d'un groupe industriel

### Contexte
IndustriAer, équipementier aéronautique de 2 800 personnes, gère 180 serveurs physiques dans deux datacenters vieillissants (12 et 15 ans). Le budget IT est de 18,2M€ dont 72% en run. Les projets d'IA et IoT sont bloqués par les contraintes d'infrastructure.

### Problème
Les datacenters approchent leur fin de vie (mise aux normes : 4,5M€ sans gain fonctionnel), le PRA est inadéquat (RPO 24h, RTO 72h), et le ratio run/build de 72/28 ne laisse pas de place à l'innovation. La direction exige un rééquilibrage à 55/45 en 3 ans.

### Approche
1. **Audit applicatif et stratégie des 6R** : Classification des 120 applications (Retain, Retire, Rehost, Replatform, Refactor, Repurchase). 18 retirées, 42 rehébergées, 28 replatformées, 12 refactorées, 8 remplacées par du SaaS, 12 conservées on-premise.
2. **Landing Zone Azure** : Infrastructure cloud fondationnelle en IaC (Terraform), réseau hub-spoke, guardrails de sécurité, FinOps dès le jour 1.
3. **Migration en 4 vagues** : Apps non-critiques → apps métier → ERP SAP → apps industrielles, avec rollback prévu à chaque étape.
4. **Modernisation PRA** : Azure Site Recovery pour les apps critiques (RPO 15 min, RTO 2h), tests trimestriels automatisés.
5. **Montée en compétences** : 25 certifications Azure visées, 3 recrutements cloud senior, communautés de pratiques internes.

### Résultat
- Ratio run/build passé de 72/28 à 58/42
- Économie annuelle de 1,8M€ sur l'infrastructure
- RPO réduit de 24h à 15 min, RTO de 72h à 2h
- Projets IA/IoT débloqués et lancés dans les 6 mois post-migration

### Leçons apprises
- La stratégie des 6R évite le piège du lift & shift généralisé — l'investissement initial dans l'analyse est toujours rentabilisé.
- La Landing Zone est le fondement non-négociable — sans elle, le cloud devient ingérable.
- Le FinOps doit être lancé dès le jour 1, pas après la migration.

---

## Cas 2 : Implémentation ITSM/ITIL dans un groupe de distribution

### Contexte
MegaRetail, groupe de distribution alimentaire (380 magasins, 42 000 collaborateurs), gère 4 500 tickets/mois. Le service desk traite tous les incidents avec la même priorité, il n'existe pas de CMDB, et 34% des incidents sont liés à des changements non coordonnés.

### Problème
Le MTTR global est de 14,2h, les incidents P1 (caisses bloquées) mettent 4,8h à être résolus (perte de 3 200€/h par magasin), et la maturité ITSM est à 1,5/5 sur le modèle CMM.

### Approche
1. **Matrice de priorisation** : 4 niveaux (P1 : 1h, P2 : 4h, P3 : 1 jour, P4 : 3 jours), validée avec les directions métier.
2. **ServiceNow ITSM** : Déploiement des modules Incident, Problem, Change et Knowledge Management avec workflows automatisés.
3. **CMDB et auto-découverte** : Inventaire automatique des actifs IT avec impact maps reliant les CI aux services métier.
4. **Change Management** : CAB hebdomadaire, calendrier des changements avec fenêtres de déploiement, plans de rollback obligatoires.
5. **Knowledge Management** : Capitalisation systématique, chaque incident résolu génère un article de connaissance.

### Résultat
- MTTR global réduit de 14,2h à 5,1h (-64%)
- MTTR P1 (caisses) passé de 4,8h à 47 minutes
- Incidents liés aux changements réduits de 34% à 8%
- Maturité ITSM passée de 1,5/5 à 3,2/5

### Leçons apprises
- La matrice de priorisation est la première décision — c'est une décision de gouvernance, pas technique.
- La CMDB est un investissement continu, pas un projet — elle devient obsolète en 3 mois sans maintenance.
- Le Change Management génère le ROI le plus rapide de toutes les pratiques ITIL.

---

## Cas 3 : Programme de gouvernance cybersécurité dans une ETI financière

### Contexte
FinSecure Gestion, société de gestion d'actifs (280 personnes, 12 Md€ d'encours), est soumise au RGPD, DORA, NIS2. L'équipe sécurité compte 4 personnes. Un audit révèle un score NIST CSF de 1,8/5 et 47 écarts DORA.

### Problème
Pas de SOC ni de SIEM, 68 applications SaaS non validées, 23 systèmes d'authentification différents, taux de clic phishing de 34%. La conformité DORA est exigée sous 14 mois.

### Approche
1. **Cartographie et analyse de risques EBIOS RM** : Inventaire des actifs, classification par sensibilité, identification de 28 risques majeurs dont 8 inacceptables.
2. **SMSI ISO 27001** : IAM centralisé (Azure AD + MFA), chiffrement, plan de réponse aux incidents cyber.
3. **SOC hybride** : SOC managé 24/7 + 2 analystes internes, SIEM Microsoft Sentinel, 85 règles de détection, EDR sur tout le parc.
4. **Conformité DORA** : Traitement des 47 écarts, registre des risques TIC, tests de résilience, renforcement des contrats prestataires.
5. **Sensibilisation continue** : E-learning mensuel, phishing simulé trimestriel, 15 Security Champions dans les équipes.

### Résultat
- Score NIST CSF passé de 1,8/5 à 3,4/5
- 44/47 écarts DORA remédiés — conformité validée
- Taux de clic phishing réduit de 34% à 7%
- MTTD des incidents : 2,4h (vs non mesuré avant)

### Leçons apprises
- La conformité réglementaire est un accélérateur — elle permet d'obtenir le budget et le sponsorship nécessaires.
- Le SOC hybride (prestataire 24/7 + interne pour le contexte métier) est le modèle optimal pour les ETI.
- La sensibilisation continue (micro-formations mensuelles) bat la formation annuelle — le changement nécessite une exposition répétée.
