# Études de cas — Opérations / Excellence opérationnelle

## Cas 1 : Transformation Lean d'une usine de production

### Contexte
PlastiTech, fabricant de composants plastiques techniques (180 personnes, 25M€ CA), fournit l'industrie automobile et l'électronique. L'usine principale tourne en 3×8 avec 12 lignes de production.

### Problème
Le taux de rendement synthétique (TRS/OEE) moyen est de 62% (vs 85% benchmark sectoriel), le taux de rebut atteint 8%, et les délais de livraison dérapent : 75% OTIF (On-Time In-Full) vs 95% contractuel. Deux clients majeurs menacent de transférer leurs commandes.

### Approche
1. **Diagnostic Lean** : Value Stream Mapping sur les 3 lignes les plus critiques, identifiant 45% de temps de non-valeur ajoutée (attentes, déplacements, surproduction).
2. **5S et management visuel** : Déploiement systématique sur les 12 lignes, avec audits hebdomadaires et scoring visible.
3. **SMED** : Réduction des temps de changement de série de 45 minutes à 12 minutes sur les 5 machines critiques.
4. **Kaizen continu** : Formation de 25 opérateurs au problem solving A3, mise en place de gemba walks quotidiennes par les managers.
5. **Flux tiré** : Passage d'un système de production push à un système kanban pour les 20 références les plus volumineuses.

### Résultat
- TRS passé de 62% à 81% en 12 mois
- Taux de rebut réduit de 8% à 2,5%
- OTIF amélioré de 75% à 93%
- Coûts de production réduits de 12% (économie de 850K€/an)

### Leçons apprises
- Le SMED est le quick win le plus impactant en production — réduire les changements de série libère de la capacité immédiatement.
- Les gemba walks quotidiennes par les managers changent la culture plus vite que n'importe quelle formation.
- Le flux tiré (kanban) fonctionne pour les références à haute rotation, mais le flux poussé reste pertinent pour les petites séries.

---

## Cas 2 : Résilience supply chain post-crise

### Contexte
MédiEquip, distributeur d'équipements médicaux (350 personnes, 120M€ CA), importe 70% de ses produits d'Asie (Chine, Malaisie, Vietnam). Les perturbations supply chain de 2021-2023 ont mis en lumière des vulnérabilités critiques.

### Problème
Les ruptures de stock touchent 15% des références actives, les lead times fournisseurs ont doublé (de 8 à 16 semaines), et les coûts de transport maritime ont triplé. Le taux de service client est tombé à 82% (vs 96% avant la crise).

### Approche
1. **Cartographie des risques supply chain** : Identification des dépendances critiques (fournisseur unique, route maritime unique, matière première unique) sur les 500 références top.
2. **Dual sourcing** : Qualification de fournisseurs alternatifs (Turquie, Inde, Europe de l'Est) pour les 50 références les plus critiques.
3. **Stock de sécurité intelligent** : Modélisation probabiliste des lead times variables, recalcul dynamique des stocks de sécurité par catégorie de risque.
4. **Nearshoring partiel** : Relocalisation de 20% des volumes en Europe (Portugal, Pologne) pour les références à forte rotation.
5. **Tour de contrôle supply chain** : Dashboard temps réel avec alertes prédictives (retards fournisseurs, congestion portuaire, risques météo).

### Résultat
- Taux de service client remonté de 82% à 95%
- Ruptures de stock réduites de 15% à 4% des références
- Lead time moyen réduit de 16 à 10 semaines (grâce au nearshoring)
- Coût total supply chain stabilisé malgré l'inflation (+3% vs +18% avant intervention)

### Leçons apprises
- Le dual sourcing coûte plus cher à court terme mais offre une résilience inestimable — c'est une assurance, pas un coût.
- Les stocks de sécurité statiques sont obsolètes — la modélisation dynamique basée sur la variabilité réelle est indispensable.
- Le nearshoring n'est viable que pour les références à forte rotation et à faible sensibilité prix.

---

## Cas 3 : Optimisation de la gestion des SLA dans une ESN

### Contexte
InfoServices, ESN de 600 personnes, gère le support IT de 15 clients grands comptes avec des SLA contractuels stricts. L'entreprise traite 5 200 tickets par mois avec 12 agents de support L1/L2.

### Problème
Le taux de respect des SLA critiques (P1) est de 61% (vs 95% contractuel), générant 1,8M€ de pénalités annuelles. Deux clients majeurs menacent de résilier. Le MTTR (Mean Time To Resolve) est de 14,2 heures en moyenne.

### Approche
1. **Matrice de priorisation** : Redéfinition de la matrice Impact × Urgence avec 4 niveaux de priorité et des SLA différenciés (P1 : 1h, P2 : 4h, P3 : 1 jour, P4 : 3 jours).
2. **Déploiement ITSM** : Migration vers ServiceNow avec workflows automatisés, routage intelligent et escalade automatique.
3. **Knowledge base** : Création de 800 articles de résolution pour les incidents récurrents, accessible en self-service.
4. **Problem management** : Identification et correction des 20% de problèmes racines générant 80% des incidents.
5. **Capacity planning** : Modèle de staffing flexible avec pool de consultants en renfort lors des pics.

### Résultat
- Respect SLA P1 passé de 61% à 94,2%
- MTTR global réduit de 14,2h à 5,1h (-64%)
- Pénalités SLA réduites de 1,8M€ à 180K€
- Satisfaction client : 4,1/5 (vs 2,8/5 avant)

### Leçons apprises
- La matrice de priorisation est la décision la plus impactante — sans elle, aucun processus ne fonctionne.
- Le knowledge management réduit le MTTR de 35% à lui seul.
- Le problem management est le levier le plus sous-estimé — éliminer les causes racines vaut mieux qu'optimiser la vitesse de résolution.
