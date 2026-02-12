# Études de cas — Risk Management

## Cas 1 : Mise en place d'un cadre ERM dans une ETI industrielle

### Contexte
ArmorPrécision, ETI industrielle (1 200 personnes, 180M€ CA), fournisseur de rang 2 pour l'aéronautique et la défense. La gestion des risques est fragmentée — chaque fonction gère ses risques en silo sans coordination.

### Problème
En 2024, trois incidents convergent : interruption de production de 3 semaines (défaillance d'un fournisseur unique de titane, perte de 4,2M€), cyberattaque ransomware paralysant les systèmes pendant 5 jours (coût 1,1M€), et non-conformité identifiée lors d'un audit client menaçant 35M€ de CA annuel. Les donneurs d'ordres (Airbus, Thales) exigent un cadre ERM conforme ISO 31000.

### Approche
1. **Cadrage et gouvernance** : Adoption d'ISO 31000, création d'un comité des risques trimestriel, définition de l'appétence au risque en 5 catégories.
2. **Identification et évaluation** : 12 ateliers, 85 collaborateurs impliqués, registre de 78 risques évalués sur probabilité, impact et vitesse.
3. **Plans de mitigation et KRIs** : Risk owner pour chaque risque critique, 25 KRIs automatisés alimentés par l'ERP et les systèmes IT, dashboard Power BI.
4. **Diversification fournisseurs** : Qualification de 8 nouveaux fournisseurs pour les matériaux critiques, réduction de la dépendance de 100% à 35%.
5. **Cyber-résilience** : Segmentation réseau, EDR, backup 3-2-1, exercice de simulation semestriel.

### Résultat
- Risques critiques réduits de 12 à 4 grâce aux actions de mitigation
- Zéro interruption de production non planifiée sur 12 mois
- Audit client réussi — maintien du statut fournisseur agréé (+8M€ CA additionnel)
- Coût des incidents réduit de 72% (de 6,1M€ à 1,7M€)

### Leçons apprises
- L'ERM doit être porté par le DG, pas délégué au Risk Manager — sa présence aux ateliers signale l'importance stratégique.
- Les KRIs automatisés transforment le registre de risques en outil vivant — un registre mis à jour manuellement est un exercice de conformité.
- La diversification des fournisseurs est un investissement, pas un coût (ratio prévention/sinistre de 1 pour 23).

---

## Cas 2 : Activation d'un Plan de Continuité d'Activité lors d'une crise majeure

### Contexte
NordServices, groupe de services aux entreprises (2 800 personnes, 320M€ CA), opère sur 450 sites clients en France (nettoyage industriel, sécurité, facility management). Activité 24/7 sur les sites critiques (hôpitaux, sites Seveso).

### Problème
Le 15 janvier 2025, une crue centenale provoque des inondations majeures : siège social inondé (datacenter détruit), 180 collaborateurs dans l'impossibilité de se rendre au bureau, 35 sites clients en zone impactée dont 3 hôpitaux et 2 sites Seveso exigeant une continuité de service.

### Approche
1. **Activation cellule de crise** : Mobilisation en visioconférence à 06h00, déclenchement du mode de travail dégradé, activation du site de repli à Villeneuve-d'Ascq.
2. **Continuité sites critiques** : Priorisation en 3 niveaux (rouge/orange/vert), redéploiement de 120 agents des sites verts vers les 5 sites critiques, activation des accords de réciprocité avec 2 prestataires partenaires.
3. **Restauration IT** : Basculement vers l'infrastructure cloud de secours (backup J-1), restauration complète en 72h.
4. **Communication de crise** : Communication proactive clients dès J1, point quotidien sites critiques, communiqué de presse à 14h00, SMS quotidien aux 2 800 collaborateurs.
5. **RETEX et amélioration** : Retour d'expérience complet sur 2 jours, 18 actions d'amélioration identifiées et planifiées.

### Résultat
- Continuité de service maintenue sur les 5 sites critiques sans interruption
- Systèmes IT restaurés en 72h (vs RTO cible 48h — écart identifié comme action d'amélioration)
- Perte de CA limitée à 1,2M€ (4,4% du CA mensuel) vs 6-8M€ estimés sans PCA
- Aucun client critique n'a résilié — 2 renouvellements avec extension de périmètre

### Leçons apprises
- Le tabletop exercise ne suffit pas — il faut tester les procédures techniques en réel (le basculement cloud a pris 72h au lieu de 48h à cause de la bande passante).
- Les accords de réciprocité doivent être contractualisés ET testés — les interlocuteurs opérationnels chez les partenaires n'avaient jamais été informés.
- La communication proactive transforme une crise en opportunité de confiance (NPS post-crise +20 points pour les clients contactés tôt).

---

## Cas 3 : Déploiement d'un programme de conformité Sapin II

### Contexte
MéridianIngénierie, bureau d'études (650 personnes, 110M€ CA), spécialisé dans les infrastructures en France et Afrique francophone. 30% du CA provient de zones à haut risque de corruption. Soumis à Sapin II et aux exigences des bailleurs internationaux (Banque Mondiale, AFD).

### Problème
Un audit de l'AFA révèle : pas de cartographie des risques de corruption, code de conduite non déployé (65% des collaborateurs ne l'ont jamais lu), pas de dispositif d'alerte, due diligence tiers défaillante (agents commerciaux non vérifiés), et 12 paiements suspects identifiés. Délai de mise en conformité : 12 mois.

### Approche
1. **Cartographie des risques** : 15 ateliers couvrant tous les processus exposés, 45 scénarios évalués, 8 risques critiques identifiés (concentrés sur les opérations africaines).
2. **Code de conduite et formation** : Code anticorruption de 20 pages avec 15 cas pratiques, formation obligatoire (e-learning 2h pour tous, présentiel 1 jour pour les 80 collaborateurs les plus exposés).
3. **Dispositif d'alerte** : Plateforme de signalement externe en 4 langues, comité d'évaluation des alertes, investigation des 12 paiements suspects.
4. **Due diligence tiers** : Screening automatisé (sanctions, PEP, médias) pour tous les tiers, investigation approfondie pour les agents commerciaux et partenaires (1 agent résilié pour opacité).
5. **Contrôles comptables renforcés** : Suppression des catégories de dépenses vagues, double validation > 5K€ dans les filiales, audit semestriel.

### Résultat
- Contrôle AFA de suivi positif — aucune sanction prononcée
- 97% des collaborateurs formés (score moyen au test : 84%)
- 14 alertes reçues en 12 mois, 3 ayant conduit à des mesures correctives
- Éligibilité Banque Mondiale restaurée — premier contrat post-conformité de 4,2M€ remporté

### Leçons apprises
- La cartographie doit être spécifique et opérationnelle, pas générique — basée sur les processus réels de l'entreprise.
- Les agents commerciaux dans les zones à risque sont le maillon le plus critique — la due diligence tiers est la première ligne de défense.
- La conformité Sapin II est un investissement commercial : le programme a coûté 480K€, l'éligibilité restaurée représente 18M€ de CA potentiel annuel.
