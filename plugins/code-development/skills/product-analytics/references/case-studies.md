# Études de cas — Product Analytics & Instrumentation

## Cas 1 : Implémentation d'un tracking plan structuré

### Contexte
TaskFlow, SaaS de gestion de tâches B2B (30 personnes, 8 développeurs), compte 15K utilisateurs actifs mensuels. L'application React/Node.js utilise Google Analytics (GA4) et quelques événements Mixpanel ajoutés ad hoc par différents développeurs au fil du temps. L'équipe produit (3 PMs) demande régulièrement des données qui n'existent pas ou sont contradictoires.

### Problème
Le tracking est chaotique : 180 événements existent dans Mixpanel dont 60% ne sont plus émis (code mort), 30% utilisent des naming conventions différentes (`button_click`, `ButtonClicked`, `btn-click`), et les propriétés sont inconsistantes (un même événement a `user_id` dans une page et `userId` dans une autre). Le PM demande "quel est notre taux d'activation ?" — personne ne peut répondre car l'événement d'activation n'existe pas. Le data analyst passe 70% de son temps à nettoyer les données au lieu de les analyser.

### Approche
1. **Audit et nettoyage** : Inventaire complet des 180 événements existants. Classification : 35 événements utiles et corrects (gardés), 45 utiles mais mal nommés (à corriger), 100 inutiles (à supprimer). Suppression du code de tracking mort.
2. **Tracking plan structuré** : Conception d'un tracking plan de 50 événements avec la convention Object-Action (Title Case) : `Task Created`, `Project Viewed`, `Subscription Started`, etc. Chaque événement documenté avec : propriétés (nom, type, valeurs attendues), déclencheur, owner, et priorité (P1/P2/P3).
3. **Schéma validé en CI** : Le tracking plan est stocké en JSON Schema dans le repo. Un middleware de validation vérifie chaque événement émis en développement. Le pipeline CI échoue si un événement ne respecte pas le schéma (nom, propriétés obligatoires, types).
4. **Migration vers PostHog** : Remplacement de GA4 + Mixpanel par PostHog (self-hosted) comme outil unique. Event tracking, funnel analysis, retention, session replay, et feature flags dans un seul outil. Implémentation hybride : tracking client-side pour les interactions UX, server-side pour les événements business critiques (paiement, abonnement).

### Résultat
- 50 événements propres et documentés (vs 180 chaotiques) — 100% conformes au schéma
- Le data analyst consacre 80% de son temps à l'analyse (vs 30% avant) — nettoyage automatisé
- Temps de réponse aux questions produit passé de "3-5 jours" à "15 minutes" (dashboards self-service)
- Taux d'activation défini et mesuré pour la première fois : 32% (seuil identifié : complétion de 3 tâches en J1)
- Coût analytics réduit de 40% (un outil au lieu de deux, self-hosted)
- Zéro événement non-conforme en production grâce à la validation CI

### Leçons apprises
- Le tracking plan est le fondement de tout — sans lui, chaque événement ajouté augmente le chaos. Investir 2 semaines de planification économise des mois de nettoyage.
- La validation de schéma en CI est le garde-fou le plus efficace — elle empêche la régression du tracking plan automatiquement.
- PostHog self-hosted offre un excellent rapport fonctionnalités/coût pour les startups — analytics, session replay, feature flags et expérimentation dans un seul outil.

---

## Cas 2 : Culture d'expérimentation A/B testing

### Contexte
ShopDirect, e-commerce D2C de produits cosmétiques (50 personnes), réalise 12M€ de CA annuel avec un site Next.js. L'équipe fait des "tests A/B" depuis 6 mois avec Google Optimize (déprécié) puis Optimizely, mais les résultats sont décevants : sur 20 tests lancés, 15 sont "non-conclusifs" et 3 ont été stoppés prématurément.

### Problème
L'analyse des tests échoués révèle des problèmes méthodologiques graves : aucun calcul de sample size préalable (tests lancés avec 500 visiteurs quand 5000 sont nécessaires), peeking systématique (vérification quotidienne et arrêt dès que p < 0.05 — inflation du taux de faux positifs à 30%+), pas de guardrail metrics (un test a augmenté le taux de clic de 20% mais réduit le taux de conversion de 15%), et pas de suivi post-test (impossible de mesurer l'impact réel).

### Approche
1. **Framework d'expérimentation rigoureux** : Template obligatoire pour chaque test : hypothèse (If/Then/Because), primary metric, guardrail metrics, MDE (Minimum Detectable Effect) souhaité, sample size calculé (calculateur Evan Miller), durée estimée. Review par le data analyst avant le lancement.
2. **Migration vers Statsig** : Remplacement d'Optimizely par Statsig (warehouse-native). Assignment server-side pour la consistance (pas de flickering). Bayesian analysis pour des résultats plus intuitifs (probabilité de victoire au lieu de p-values). Guardrail metrics automatisées.
3. **Séquentiel testing** : Adoption du sequential testing (GroupSequential) qui permet de vérifier les résultats à intervalles réguliers sans inflater le faux positif. Les tests sont "monitorés" en continu avec des bornes de décision prédéfinies.
4. **Culture d'expérimentation** : Chaque squad doit avoir au moins 1 test actif en permanence. Résultats partagés en weekly all-hands avec apprentissages (y compris les tests négatifs). "Test of the Month" pour les insights les plus impactants.

### Résultat
- Tests conclusifs passés de 25% (5/20) à 70% (14/20) — sample size correct dès le départ
- Taux de faux positifs réduit de ~30% à < 5% (fin du peeking, sequential testing)
- 5 tests gagnants implémentés en 6 mois avec un impact cumulé de +18% sur le taux de conversion
- Revenue uplift mesuré : +1.8M€ annualisé attribuable aux tests A/B
- Guardrail metrics : zéro test déployé avec une régression non détectée sur le revenue par session
- Temps moyen d'un test réduit de 6 semaines à 3 semaines (sample size optimisé par le sequential testing)

### Leçons apprises
- Le calcul de sample size AVANT le lancement est la différence entre un test scientifique et une opinion déguisée — 80% des tests "non-conclusifs" échouent par manque de trafic.
- Le sequential testing est le meilleur compromis entre rigueur et vitesse — il permet de monitorer sans inflater les erreurs.
- Partager les tests perdants est aussi important que les tests gagnants — les apprentissages négatifs évitent de répéter les mêmes erreurs.

---

## Cas 3 : Migration vers une analytics privacy-first conforme RGPD

### Contexte
SantéPlus, plateforme de téléconsultation (60 personnes, 500K utilisateurs), utilise Google Analytics (GA4), Hotjar (session replay), et 8 scripts de remarketing tiers. Un CMP (Consent Management Platform) Axeptio est installé mais mal configuré : les scripts se chargent avant le consentement dans certains cas.

### Problème
Un contrôle CNIL révèle une non-conformité : les cookies analytics et marketing sont déposés avant le consentement utilisateur (violation de l'article 82 de la loi Informatique et Libertés). L'entreprise reçoit une mise en demeure avec un délai de 3 mois pour se mettre en conformité. De plus, 35% du trafic est bloqué par les adblockers (GA4 et Hotjar sont bloqués), rendant les données incomplètes. L'équipe produit prend des décisions sur 65% des données réelles.

### Approche
1. **Audit complet des traceurs** : Inventaire de tous les scripts, cookies et pixels via le rapport CNIL cookie (outil Cookiebot en audit mode). Résultat : 23 cookies dont 8 déposés avant consentement. Classification : 4 strictement nécessaires (exemptés), 6 analytics, 13 marketing/remarketing.
2. **PostHog self-hosted + exemption CNIL** : Remplacement de GA4 par PostHog self-hosted sur l'infrastructure propre de l'entreprise (Docker sur AWS, données en EU). Configuration conforme aux lignes directrices CNIL pour l'exemption analytics first-party : pas de cross-site tracking, données anonymisées après 25 mois, pas de transfert hors UE. Cette configuration est exemptée de consentement.
3. **Server-side tracking** : Migration du tracking client-side vers le server-side pour les événements business critiques. Le SDK PostHog côté serveur (Node.js) enregistre les conversions, les inscriptions et les abonnements — invisible aux adblockers, 100% de couverture.
4. **Suppression des scripts marketing** : Suppression de 8 scripts de remarketing (Google Ads, Meta Pixel, etc.) remplacés par le Conversions API (server-to-server) de Meta et Google qui n'utilise pas de cookies tiers. Les 5 scripts restants (chat, support) sont conditionnés au consentement via Axeptio correctement configuré.

### Résultat
- Conformité CNIL validée — mise en demeure levée après l'audit de remediation
- Couverture de données passée de 65% à 97% (server-side + exemption CNIL = pas de blocage)
- Cookies tiers réduits de 23 à 4 (strictement nécessaires uniquement sans consentement)
- PostHog self-hosted coûte 60% de moins que GA4 Premium + Hotjar combinés
- Taux de consentement analytics : non applicable (exemption CNIL) — 100% des visiteurs trackés en analytics
- Décisions produit basées sur 97% des données au lieu de 65% — précision des métriques significativement améliorée

### Leçons apprises
- L'exemption CNIL pour l'analytics first-party est un avantage stratégique majeur — elle permet de tracker 100% des visiteurs sans consentement, à condition de respecter les conditions strictes.
- Le server-side tracking est la solution définitive aux adblockers — pour les événements business critiques, il doit être la méthode par défaut.
- Les scripts marketing tiers sont la principale source de non-conformité RGPD — les Conversions APIs server-to-server offrent les mêmes fonctionnalités sans cookies tiers.
