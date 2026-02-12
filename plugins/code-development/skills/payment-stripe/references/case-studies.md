# Études de cas — Payment Stripe

## Cas 1 : Stripe Connect pour une marketplace de services

### Contexte
ProConnect, marketplace de freelances tech (35 personnes), met en relation des entreprises avec des développeurs et designers indépendants. L'application Next.js gère 2000 freelances et 500 entreprises clientes. Les paiements étaient gérés manuellement : les entreprises payaient ProConnect par virement, ProConnect redistribuait aux freelances par virement bancaire avec un délai de 15-30 jours.

### Problème
Le processus de paiement manuel génère 3 ETP de charge administrative (réconciliation, virements, facturation). Les freelances se plaignent des délais de paiement (15-30 jours vs 7 jours chez les concurrents). 25% des freelances ont quitté la plateforme en citant les paiements comme raison principale. La comptabilité est approximative : 5% d'écarts de réconciliation en moyenne. L'absence de paiement intégré empêche le scoring des freelances et la gestion des litiges.

### Approche
1. **Stripe Connect Express** : Implémentation de Stripe Connect en mode Express — les freelances créent un compte Stripe via un onboarding simplifié (KYC géré par Stripe). ProConnect collecte les paiements des entreprises et distribue automatiquement aux freelances. Commission de 15% retenue automatiquement.
2. **Webhook-driven architecture** : 12 événements Stripe gérés par des handlers idempotents : `payment_intent.succeeded` (activer la mission), `transfer.created` (notifier le freelance), `account.updated` (vérifier le statut KYC), `payout.failed` (alerter et retenter). Chaque handler utilise une clé d'idempotence basée sur `event.id` + `event.type`.
3. **Split payments** : Configuration des paiements avec `transfer_data` pour le split automatique : 85% au freelance (via son compte Connect), 15% à ProConnect. Les taxes (Stripe Tax) sont calculées automatiquement en fonction de la localisation du freelance et de l'entreprise.
4. **Instant payouts** : Activation des Instant Payouts pour les freelances éligibles — paiement en < 30 minutes au lieu de T+2. Option premium facturée 1% supplémentaire.

### Résultat
- Délai de paiement freelance réduit de 15-30 jours à T+2 standard, < 30 min en instant
- Charge administrative réduite de 3 ETP à 0.3 ETP (automatisation quasi-complète)
- Écarts de réconciliation éliminés — Stripe est la source de vérité comptable
- Rétention freelance améliorée de 75% à 92% — les paiements rapides sont le facteur #1
- Revenu de la commission Stripe automatisée : +15% de marge nette (suppression des coûts de traitement manuel)
- Instant payouts adopté par 40% des freelances — source de revenus supplémentaire (1% de frais)

### Leçons apprises
- Stripe Connect Express est le meilleur compromis pour les marketplaces : onboarding simple pour les vendeurs, KYC géré par Stripe, et contrôle suffisant pour la plateforme.
- L'architecture webhook-driven avec idempotence est non-négociable pour les paiements — un événement non traité ou traité deux fois peut générer des pertes financières directes.
- Les Instant Payouts sont un levier de rétention et de monétisation puissant — les freelances sont prêts à payer pour recevoir leur argent immédiatement.

---

## Cas 2 : Migration vers le usage-based billing pour un SaaS API

### Contexte
APIMetrics, SaaS B2B d'analytics d'API (25 personnes), propose un monitoring d'API avec 3 tiers de pricing fixe : Starter (49€/mois, 10K requêtes), Pro (199€/mois, 100K requêtes), Enterprise (499€/mois, 1M requêtes). L'application est développée en Node.js avec une base PostgreSQL et utilise Stripe pour les abonnements.

### Problème
Le pricing fixe crée deux problèmes : les petits clients (2K requêtes/mois) trouvent le Starter trop cher et churned (taux de churn 8%/mois), tandis que les gros clients (5M requêtes/mois) exploitent le tier Enterprise à 499€ pour un usage qui devrait coûter 2500€+. L'analyse montre que 30% des clients Enterprise consomment 10× plus que ce que le tier couvre. Le revenu par requête est 10× plus élevé sur le Starter que sur l'Enterprise — le pricing pénalise la croissance des clients.

### Approche
1. **Metered billing Stripe** : Migration vers un modèle hybride : base fixe (plateforme) + variable (par requête). Création de Stripe Prices avec `recurring.usage_type: 'metered'` et `tiers_mode: 'graduated'` — les tranches dégressives (0-100K: 0.005€, 100K-1M: 0.003€, 1M+: 0.001€) récompensent la croissance.
2. **Usage reporting pipeline** : Implémentation d'un pipeline de reporting d'usage : les requêtes API sont comptées en temps réel (Redis HyperLogLog), agrégées toutes les heures, et reportées à Stripe via `stripe.subscriptionItems.createUsageRecord()`. Facturation en fin de période (arrears).
3. **Customer Portal self-service** : Déploiement du Stripe Customer Portal pour que les clients gèrent eux-mêmes leur abonnement : historique de facturation, méthodes de paiement, export de factures. Un dashboard in-app affiche la consommation en temps réel et la facture estimée.
4. **Migration progressive** : Les clients existants sont migrés par vagues avec une garantie de prix : si le nouveau modèle coûte plus cher que l'ancien pendant les 3 premiers mois, la différence est créditée. Communication proactive avec les 50 plus gros clients.

### Résultat
- ARPU (Average Revenue Per User) augmenté de 35% — les gros consommateurs paient proportionnellement à leur usage
- Churn des petits clients réduit de 8% à 2.5%/mois — l'entrée de gamme commence à 15€/mois
- Net Revenue Retention passé de 95% à 118% — les clients qui grandissent génèrent naturellement plus de revenu
- Nombre de clients augmenté de 40% (barrière d'entrée plus basse)
- Zéro client perdu pendant la migration (garantie de prix efficace)
- Revenue recognition conforme IFRS 15 grâce à Stripe Revenue Recognition

### Leçons apprises
- Le usage-based pricing aligne les intérêts du SaaS et du client — le client ne paie que ce qu'il consomme, le SaaS grandit avec l'usage du client.
- Le pipeline de reporting d'usage est le composant critique — une erreur de comptage génère des factures incorrectes et de la perte de confiance. Investir dans la fiabilité (idempotence, reconciliation).
- La migration de pricing est un exercice de communication autant que technique — la garantie de prix élimine la peur du changement.

---

## Cas 3 : Expansion internationale avec Adaptive Pricing

### Contexte
LearnUp, plateforme EdTech de cours en ligne (40 personnes), réalise 90% de son CA en France. L'offre est en euros avec des prix fixes : 19€/mois (individuel), 99€/mois (équipe), 299€/mois (entreprise). L'application Next.js utilise Stripe Checkout pour les abonnements.

### Problème
L'expansion internationale stagne : le taux de conversion au Brésil est de 0.8% (vs 3.5% en France), au Japon 1.2%, aux US 2.1%. L'analyse révèle que 19€/mois représente 2% du salaire médian en France mais 8% au Brésil. Les utilisateurs internationaux abandonnent massivement au moment du paiement (60% d'abandon au checkout vs 25% en France). De plus, les frais de change augmentent les coûts pour les clients non-EUR.

### Approche
1. **Adaptive Pricing Stripe** : Activation de l'Adaptive Pricing qui affiche automatiquement les prix dans la devise locale du client (BRL, JPY, USD, GBP, etc.). Stripe ajuste les montants en fonction du pouvoir d'achat local, pas seulement du taux de change. Les prix sont arrondis aux paliers psychologiques de chaque marché.
2. **Payment methods locaux** : Activation des méthodes de paiement locales via le Payment Element unifié : Boleto et PIX (Brésil), Konbini (Japon), ACH Direct Debit (US), SEPA (Europe), iDEAL (Pays-Bas). Le Payment Element affiche automatiquement les méthodes pertinentes selon la localisation.
3. **Stripe Tax multi-juridictions** : Activation de Stripe Tax avec `automatic_tax: { enabled: true }` pour gérer automatiquement la TVA EU, GST, sales tax US par État. Stripe calcule, collecte et verse les taxes dans chaque juridiction.
4. **Localized Checkout** : Personnalisation du Stripe Checkout avec la locale du client (langue, devise, méthodes de paiement). Ajout de "social proof" localisé ("12,000 utilisateurs au Brésil", "500 entreprises au Japon").

### Résultat
- Taux de conversion global (hors France) passé de 1.4% à 3.8% (×2.7)
- Brésil : conversion de 0.8% à 3.2% (×4) — PIX représente 60% des paiements
- Japon : conversion de 1.2% à 3.5% (×2.9) — Konbini représente 35% des paiements
- US : conversion de 2.1% à 4.1% (×2) — ACH réduit les frais de transaction de 40%
- Revenue international passé de 10% à 35% du CA total en 6 mois
- Abandon checkout international réduit de 60% à 22% (proche du taux français)
- Compliance fiscale automatisée — Stripe Tax gère 40+ juridictions sans effort manuel

### Leçons apprises
- L'Adaptive Pricing est le levier de conversion international le plus puissant — afficher le bon prix dans la bonne devise avec le bon pouvoir d'achat multiplie les conversions par 2-4×.
- Les méthodes de paiement locales sont indispensables — dans certains marchés (Brésil, Japon), la carte bancaire n'est pas la méthode dominante.
- Stripe Tax automatise un problème de compliance qui coûterait des dizaines de milliers d'euros en expertise comptable — c'est un multiplicateur de vitesse d'expansion.
