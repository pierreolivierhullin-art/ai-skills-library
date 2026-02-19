# Etudes de Cas — Data Privacy & Compliance en Pratique

## Vue d'Ensemble

Ces etudes de cas illustrent la mise en conformite RGPD dans des contextes reels : startup e-commerce, scale-up SaaS, groupe industriel, et une violation de donnees geree en 72h.

---

## Cas 1 — Mise en Conformite RGPD d'une Startup E-Commerce (12 Semaines)

### Contexte

Startup e-commerce B2C (35 employes, 180 000 clients, CA 8M EUR). Aucune conformite RGPD en place 3 ans apres la creation. Catalyseur : audit d'un investisseur entrant en serie A — la conformite RGPD est dans les conditions precedentes au closing.

**Situation initiale** :
- Pas de registre de traitement
- Politique de confidentialite generique (copier-coller d'un template)
- Google Analytics sans consentement (cookies deposes automatiquement)
- Donnees clients conservees indefiniment (depuis la creation)
- Sous-traitants (Shopify, Klaviyo, Stripe) sans DPA signes
- Pas de procedure de reponse aux droits

### Programme de Conformite (12 semaines)

**Semaines 1-3 — Audit et cartographie** :
- Inventaire de toutes les donnees collectees : 23 traitements identifies
- Cartographie des flux : donnees clients → Shopify → Klaviyo (email) → Google Analytics → Meta Pixel → Stripe → Colissimo
- Identification des bases legales manquantes : le Meta Pixel sans consentement etait la non-conformite la plus grave (publicite comportementale)

**Semaines 4-6 — Actions prioritaires (quick fixes)** :
- Mise en place d'un CMP (Axeptio, 49 EUR/mois) : desactivation du Meta Pixel et Google Analytics jusqu'au consentement
- Signature des DPA avec Shopify, Klaviyo, Stripe, Mailchimp
- Nouvelle politique de confidentialite redigee avec un avocat RGPD (2 500 EUR)
- Adresse email rgpd@startup.fr operationnelle avec procedure de traitement

**Semaines 7-10 — Registre et procedures** :
- Registre de traitement complet : 23 fiches redigees
- Politique de retention : purge des donnees > 3 ans apres dernier achat
- Procedure violation de donnees : playbook 72h cree et test simulation realisé
- Formation de l'equipe (2h en ligne) : fondamentaux RGPD, signalement incident

**Semaines 11-12 — Validation et documentation** :
- Revue par un DPO externe (journee conseil)
- Document de preuve de conformite pour l'investisseur
- Roadmap de conformite continue (registre a maintenir, DPIAs pour les prochains projets)

### Resultats

**Impact sur l'investissement** : condition levee, closing realise. Le DPO externe a calcule le risque residuel comme "faible" — suffisant pour les due diligences.

**Impact metier** (effets secondaires positifs) :
- Taux d'opt-in cookies analytics : 68% (vs attente de 50%) — la CMP bien designee a converti plus que prevu
- Nettoyage de la base email : 42 000 emails purges (> 3 ans d'inactivite) → amelioration du taux de delivrabilite de 12 points

**Couts** :
- DPO externe (30 jours) : 18 000 EUR
- Avocat RGPD (politique + DPA) : 4 500 EUR
- CMP : 600 EUR/an
- Temps interne (chef de projet 50%, 12 semaines) : ~18 000 EUR valorise
- **Total** : ~41 000 EUR pour une startup serie A — investissement negligeable vs risque d'amende (jusqu'a 4% CA = 320 000 EUR) et benefice sur le closing

---

## Cas 2 — Gestion d'une Violation de Donnees en 72h (Scale-up SaaS)

### Contexte

Scale-up SaaS B2B (120 employes, 3 000 clients entreprises, donnees RH et paie). Vendredi 17h23 : alerte de monitoring — un endpoint API non documente est accessible publiquement sans authentification. Analyse rapide : des donnees de configuration de clients (noms des entreprises, noms des administrateurs, emails) sont exposees. Pas de mots de passe ni de donnees de paie — mais des donnees personnelles clairement exposees.

### Chronologie de la Gestion de Crise

**J0 (vendredi) — H+0 a H+4** :
- 17h23 : alerte detectee par le systeme de monitoring (spike de requetes sur un endpoint inhabituel)
- 17h35 : confirmation — l'endpoint retourne des donnees reelles
- 17h40 : coupure de l'endpoint (acces desactive)
- 18h00 : cellule de crise constituee (CTO, DPO, CEO, Responsable Juridique)
- 18h30 : analyse forensique — l'endpoint a ete cree lors d'un hotfix 3 semaines plus tot, jamais teste en securite
- 20h00 : estimation du perimetre — 847 records exposes (noms entreprise, nom/email admin)
- 20h30 : premiere notification CNIL (provisoire, perimetre a confirmer)

**J1 (samedi) — H+24 a H+48** :
- Analyse complete des logs : aucune donnee de paie, aucun mot de passe. Volume confirme : 847 records. Acces externe : 3 IPs distinctes ont requete l'endpoint (dont une IP connue d'un scanner de securite automatique).
- Evaluation du risque : risque "limite" (pas de donnees tres sensibles, pas de mots de passe) → information individuelle des personnes NON obligatoire, mais recommandee par le DPO pour maintenir la confiance.
- Redaction du message client : ton transparent, explication factuelle, mesures prises, contact direct.
- Decision : informer les 847 contacts administrateurs directement par email.

**J2 (dimanche)** :
- Envoi de l'email a tous les administrateurs concernes (18h00)
- Mise a jour du support (FAQ disponible)
- Preparation du rapport complet pour la CNIL

**J3 (lundi)** :
- Notification CNIL complete (avec le rapport detaille)
- Conférence de presse interne pour les 120 employes
- Appels sortants vers les 15 plus grands clients (gestes commerciaux)
- Post-mortem interne : creation d'une checklist de securite obligatoire avant tout hotfix

### Resultats

**Reponse CNIL** (6 semaines plus tard) : "Prise en compte. Pas de suites en raison de la bonne gestion de l'incident, de la notification rapide, et des mesures correctives mises en place."

**Impact clients** :
- 12 clients ont contacte le support (aucune resiliation)
- NPS apres l'incident : -3 points sur le trimestre (impact limite)
- 2 clients ont demande un audit de securite complet (pris en charge gratuitement)

**Lecons** :
- La transparence rapide a ete le principal facteur de preservation de la confiance
- La notification CNIL provisoire (J0) a ete cruciale — mieux vaut une notification incomplete a temps qu'une notification complete hors delai
- Le post-mortem a revele une faille de processus (hotfixes sans review securite) qui aurait pu generer des incidents bien plus graves

---

## Cas 3 — Privacy by Design dans un Projet ML (Banque)

### Contexte

Banque de detail (2.3M clients). Projet de credit scoring par ML — le modele utilise l'historique de transactions pour predire la probabilite de defaut. Contraintes : RGPD (base legale, minimisation, droits), directive europenne sur le credit (obligation d'expliquer le refus), et sensibilite interne a la discrimination algorithmique.

### Implementation Privacy by Design

**Etape 1 — DPIA avant developpement** :
8 criteres G29 sur 10 sont valides (scoring, decision automatisee, donnees financieres, grande echelle, personnes vulnerables potentielles...). DPIA obligatoire.

La DPIA a identifie 3 risques majeurs :
- Discrimination indirecte (variables proxy de l'origine ou de la religion)
- Biais historique (credits historiquement refuses a certains segments)
- Re-identification par combinaison des features

**Etape 2 — Minimisation des donnees** :
Feature selection rigoureux : eliminer toutes les variables avec un risque de proxy discriminatoire (code postal → quartier → origine ethnique probable). Test systematique avec Fairlearn avant d'inclure chaque feature.

Variables exclues malgre leur pouvoir predictif : localisation granulaire, transactions dans certains commerces (lieux de culte, etc.), frequence des appels au service client.

**Etape 3 — Pseudonymisation du dataset d'entrainement** :
Le modele est entraine sur des customer_id pseudonymises — la table de correspondance est stockee separement, accessible uniquement au DPO et au RSSI.

**Etape 4 — Explicabilite integree (droit Article 22)** :
Le RGPD (Article 22) et la directive credit europeenne imposent de pouvoir expliquer un refus de credit. SHAP values calculees pour chaque decision → les 3 principaux facteurs sont presentés au client en langage clair.

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_customer)

# Traduction en langage clair
def explain_decision(shap_values, feature_names, threshold=0.0):
    top_factors = sorted(
        zip(feature_names, shap_values),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:3]

    explanations = {
        'utilisation_credit': "Votre taux d'utilisation de credit est eleve",
        'retards_paiement': "Vous avez eu des retards de paiement recents",
        'anciennete_compte': "La duree de votre historique bancaire est limitee",
    }
    return [explanations.get(f, f) for f, v in top_factors if v < threshold]
```

**Etape 5 — Audit de biais trimestriel** :
Rapport automatique tous les trimestres sur : taux d'accord par segment (age range, region), comparaison avec le taux de defaut reel. Alerte si ecart > 5 points entre segments similaires sur le plan du risque.

### Resultats

- Modele en production depuis 18 mois, aucune plainte reglementaire
- CNIL a realise un controle formel 6 mois apres le deploiement : conformite validee
- Audit de biais Q4 : aucun ecart significatif identifie
- Satisfaction clients (explication refus) : 72% comprennent "bien" ou "tres bien" la raison du refus (vs 23% avant avec un message generique)

---

## Cas 4 — Programme de Conformite Multi-Pays pour un Groupe Industriel

### Contexte

Groupe industriel (8 000 salaries, presences en France, Allemagne, Italie, Pologne, Maroc, USA). DPO groupe nomme. Objectif : conformite RGPD harmonisee groupe + gestion des specificites nationales + conformite CCPA pour la filiale US.

### Architecture de Gouvernance

**Modele hub-and-spoke** :
- DPO groupe (Paris) : politiques et standards communs, registre groupe consolide, formation, veille reglementaire
- Data Protection Coordinators (DPC) dans chaque filiale : application locale, registre filiale, premier point de contact

**Specificites nationales prises en compte** :
- **Allemagne** : droits syndicaux plus etendus (betriebsrat doit valider certains traitements RH), loi BDSG complementaire
- **Italie** : Garante (autorite italienne) plus restrictive sur le monitoring des employes
- **Pologne** : UODO (autorite polonaise) avec positions specifiques sur les donnees RH
- **Maroc** : CNDP (Commission Nationale de controle de la Protection des Donnees a caractere Personnel) — obligations de notification des traitements
- **USA (filiale)** : CCPA applicable (CA 85M USD > seuil 25M USD)

**Outils de gouvernance** :
- OneTrust pour le registre de traitement groupe (1 instance, acces par filiale)
- Politique de confidentialite groupe + addendums locaux (5 langues)
- Formation e-learning obligatoire annuelle (meme module, traduit)
- Tableau de bord conformite groupe (statut par filiale, incidents, droits en cours)

### Resultats apres 24 mois

| Indicateur | Valeur |
|---|---|
| Taux de completion formation annuelle | 94% des employes |
| Demandes de droits traitees en < 30 jours | 98% |
| Violations notifiees aux autorites | 3 (toutes gestion classée sans suite) |
| Amendes RGPD | 0 |
| Budget programme (annuel) | 380 000 EUR (DPO + DPC + outils + formation) |
