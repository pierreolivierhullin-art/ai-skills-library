# Data Protection

Reference complete de la protection des donnees personnelles et du RGPD (2024-2026). Couvre le registre des traitements, Privacy by Design, les analyses d'impact (DPIA/AIPD), les droits des personnes concernees, les relations CNIL, les Data Processing Agreements, les transferts internationaux et le reglement ePrivacy.

---

## RGPD — Architecture et Principes Fondamentaux

### Les 7 principes du RGPD (Article 5)

Tout traitement de donnees personnelles doit respecter ces principes fondamentaux :

1. **Liceite, loyaute et transparence** : traiter les donnees de maniere licite (base legale valide), loyale (pas de traitement cache) et transparente (information claire des personnes)
2. **Limitation des finalites** : collecter les donnees pour des finalites determinees, explicites et legitimes. Ne pas les reutiliser de maniere incompatible avec ces finalites
3. **Minimisation des donnees** : ne collecter que les donnees strictement necessaires aux finalites poursuivies. Ne pas collecter "au cas ou"
4. **Exactitude** : maintenir les donnees exactes et a jour. Mettre en place des mecanismes de rectification
5. **Limitation de la conservation** : definir des durees de conservation proportionnees aux finalites. Supprimer ou anonymiser les donnees au-dela de ces durees
6. **Integrite et confidentialite** : garantir la securite des donnees par des mesures techniques et organisationnelles appropriees
7. **Responsabilite (accountability)** : etre en mesure de demontrer la conformite a tout moment. Documenter, tracer, auditer

### Les 6 bases legales (Article 6)

Chaque traitement doit reposer sur l'une de ces bases legales :

| Base legale | Cas d'usage | Points d'attention |
|---|---|---|
| **Consentement** | Marketing direct, cookies non essentiels, newsletter | Libre, specifique, eclaire, univoque. Retirable a tout moment. Preuve conservee |
| **Execution d'un contrat** | Livraison, facturation, SAV, gestion de compte | Strictement necessaire a l'execution. Ne couvre pas le marketing |
| **Obligation legale** | Conservation comptable, declarations fiscales, KYC | Identifier la disposition legale precise |
| **Interets vitaux** | Urgences medicales, securite des personnes | Usage exceptionnel |
| **Mission d'interet public** | Administration, recherche publique | Avec base legale explicite |
| **Interet legitime** | Securite IT, prevention fraude, prospection B2B | Test de mise en balance (legitimate interest assessment). Droit d'opposition |

### Le consentement — Exigences detaillees

Pour etre valide au sens du RGPD, le consentement doit etre :

- **Libre** : pas de consequence negative en cas de refus, pas de desequilibre de pouvoir (prudence dans la relation employeur-employe), pas de couplage avec un service (granularite)
- **Specifique** : un consentement par finalite. Ne pas regrouper plusieurs finalites dans un seul consentement
- **Eclaire** : informer clairement de l'identite du responsable, des finalites, des donnees collectees, du droit de retrait, des transferts eventuels
- **Univoque** : acte positif clair (case a cocher non pre-cochee, declaration orale enregistree). Le silence ou l'inaction ne vaut pas consentement

Pour les cookies et traceurs : appliquer les recommandations CNIL (deliberation du 17 septembre 2020) :
- Accepter et refuser doivent etre presentes de maniere equivalente (pas de dark pattern)
- Informer sur chaque finalite (mesure d'audience, publicite ciblee, reseaux sociaux, etc.)
- Permettre le retrait du consentement aussi facilement que son octroi
- Renouveler le consentement tous les 13 mois maximum (recommandation CNIL)

---

## Registre des Traitements (Article 30)

### Contenu obligatoire du registre

Le registre des traitements est le document central de la conformite RGPD. Il doit contenir pour chaque traitement :

**Pour le responsable de traitement :**
- Nom et coordonnees du responsable de traitement (et du representant et du DPO le cas echeant)
- Finalites du traitement
- Categories de personnes concernees
- Categories de donnees a caractere personnel
- Categories de destinataires
- Transferts vers un pays tiers (avec garanties appropriees)
- Delais de suppression prevus (durees de conservation)
- Description des mesures de securite techniques et organisationnelles

**Pour le sous-traitant :**
- Nom et coordonnees du sous-traitant et de chaque responsable de traitement pour lequel il agit
- Categories de traitements effectues pour le compte de chaque responsable
- Transferts vers un pays tiers
- Description des mesures de securite

### Methodologie de construction

1. **Inventaire initial** : recenser tous les traitements par direction/service (RH, marketing, finance, IT, commercial). Utiliser des interviews et l'analyse des systemes d'information
2. **Cartographie des flux** : pour chaque traitement, tracer les flux de donnees (collecte, stockage, transfert, archivage, suppression)
3. **Documentation** : renseigner chaque fiche de traitement avec les informations requises
4. **Validation** : faire valider chaque fiche par le responsable operationnel et le DPO
5. **Mise a jour continue** : integrer la mise a jour du registre dans les processus de gestion de projet (tout nouveau projet impliquant des donnees personnelles doit faire l'objet d'une fiche de traitement)

### Outils de gestion du registre

| Outil | Type | Segment | Points forts |
|---|---|---|---|
| **OneTrust** | SaaS | ETI / Grand groupe | Completude, automatisation, veille reglementaire |
| **Didomi** | SaaS | Startup / PME | Consent management, UX, prix |
| **Witik** | SaaS (FR) | PME / ETI | Registre + DPIA + formation, conformite CNIL |
| **DPOrganizer** | SaaS | Mid-market | Cartographie des donnees, collaboration |
| **Dastra** | SaaS (FR) | PME / ETI | Registre complet, approche francaise, integration |

---

## Privacy by Design (Article 25)

### Les 7 principes fondateurs (Ann Cavoukian)

1. **Proactif, pas reactif** : anticiper et prevenir les risques plutot que les corriger apres coup
2. **Protection par defaut** : configurer les parametres les plus protecteurs par defaut (opt-in, pas opt-out)
3. **Integre dans la conception** : la protection des donnees fait partie integrante de l'architecture du systeme, pas un ajout posterieur
4. **Fonctionnalite complete** : positive-sum, pas zero-sum. La protection des donnees ne doit pas degrader la fonctionnalite
5. **Securite de bout en bout** : protection tout au long du cycle de vie des donnees (collecte, traitement, stockage, suppression)
6. **Visibilite et transparence** : les pratiques doivent etre verifiables et auditables
7. **Respect de l'utilisateur** : centrer la conception sur les interets de la personne concernee

### Checklist Privacy by Design pour les projets

Integrer cette checklist dans chaque cycle de developpement :

**Phase de conception :**
- [ ] Finalites du traitement identifiees et documentees
- [ ] Base legale determinee et justifiee
- [ ] Minimisation des donnees : chaque champ collecte est-il strictement necessaire ?
- [ ] Durees de conservation definies pour chaque categorie de donnees
- [ ] Pseudonymisation ou anonymisation evaluee
- [ ] Sous-traitants identifies, DPA en place
- [ ] Transferts internationaux identifies et encadres

**Phase de developpement :**
- [ ] Chiffrement des donnees au repos (AES-256) et en transit (TLS 1.3)
- [ ] Controles d'acces par role (RBAC) ou attribut (ABAC) implementes
- [ ] Journalisation des acces aux donnees personnelles
- [ ] Mecanisme de consentement operationnel (si applicable)
- [ ] Fonctionnalites d'exercice des droits (acces, rectification, suppression, portabilite)
- [ ] Purge automatique a l'expiration des durees de conservation

**Phase de mise en production :**
- [ ] DPIA realisee si traitement a risque (voir section suivante)
- [ ] Registre des traitements mis a jour
- [ ] Politique de confidentialite mise a jour
- [ ] Formation des equipes operationnelles
- [ ] Procedure de notification de violation en place

---

## DPIA / AIPD — Analyse d'Impact (Article 35)

### Quand realiser une DPIA

Une DPIA est obligatoire lorsque le traitement est "susceptible d'engendrer un risque eleve pour les droits et libertes des personnes physiques". La CNIL a publie une liste de traitements necessitant une DPIA :

- Evaluation ou scoring (y compris profilage)
- Decision automatisee avec effet juridique ou effet significatif similaire
- Surveillance systematique a grande echelle
- Donnees sensibles ou hautement personnelles a grande echelle
- Croisement ou combinaison de jeux de donnees
- Donnees de personnes vulnerables (enfants, patients, employes)
- Usage innovant de technologies (IA, biometrie, IoT)
- Traitement empechant les personnes d'exercer un droit ou de beneficier d'un service

Regle pratique : si le traitement coche 2 criteres ou plus de la liste ci-dessus, realiser une DPIA.

### Methodologie DPIA (methode CNIL / PIA)

La CNIL propose un outil PIA (Privacy Impact Assessment) en 4 etapes :

**1. Description du traitement :**
- Contexte, enjeux, finalites
- Donnees traitees, personnes concernees
- Supports, logiciels, flux de donnees
- Durees de conservation

**2. Evaluation de la necessite et de la proportionnalite :**
- La finalite est-elle determinee, explicite et legitime ?
- Les donnees collectees sont-elles adequates, pertinentes et limitees ?
- Les durees de conservation sont-elles proportionnees ?
- Les personnes sont-elles correctement informees ?
- Les droits des personnes sont-ils effectivement exercables ?

**3. Evaluation des risques pour les personnes :**

Pour chaque risque, evaluer :
- La gravite (negligeable, limitee, importante, maximale)
- La vraisemblance (negligeable, limitee, importante, maximale)

Risques types :
- Acces illegitime aux donnees (violation de confidentialite)
- Modification non desiree des donnees (violation d'integrite)
- Disparition des donnees (violation de disponibilite)

**4. Plan d'action :**
- Mesures existantes et mesures supplementaires prevues
- Plan de mise en oeuvre avec responsables et delais
- Risque residuel apres mesures

### DPIA et Intelligence Artificielle

L'EU AI Act (reglement (UE) 2024/1689) et le RGPD convergent pour exiger des evaluations d'impact renforcees pour les systemes d'IA :

- Les systemes d'IA "a haut risque" (article 6 EU AI Act) doivent faire l'objet d'une evaluation de conformite avant mise sur le marche
- Tout traitement utilisant un profilage automatise avec des effets significatifs necessite une DPIA
- Documenter la logique algorithmique, les donnees d'entrainement, les biais potentiels et les mesures correctives
- Prevoir un controle humain (human-in-the-loop) pour les decisions automatisees avec effet juridique (article 22 RGPD)

---

## Droits des Personnes Concernees (Articles 15-22)

### Tableau des droits

| Droit | Article | Delai de reponse | Points d'attention |
|---|---|---|---|
| **Acces** | Art. 15 | 1 mois | Fournir une copie des donnees + informations sur le traitement |
| **Rectification** | Art. 16 | 1 mois | Corriger les donnees inexactes, completer les donnees incompletes |
| **Effacement** (droit a l'oubli) | Art. 17 | 1 mois | Exceptions : obligation legale, archivage d'interet public, defense en justice |
| **Limitation** | Art. 18 | 1 mois | Geler le traitement pendant la verification de l'exactitude ou de la liceite |
| **Portabilite** | Art. 20 | 1 mois | Format structure, couramment utilise, lisible par machine (CSV, JSON) |
| **Opposition** | Art. 21 | 1 mois | Droit absolu pour la prospection. Test de mise en balance pour l'interet legitime |
| **Decision automatisee** | Art. 22 | 1 mois | Droit a ne pas faire l'objet d'une decision purement automatisee avec effet juridique |

### Processus de gestion des demandes

1. **Reception et identification** : verifier l'identite du demandeur (piece d'identite si doute raisonnable, sans exiger d'informations supplementaires disproportionnees)
2. **Qualification** : identifier le droit exerce, verifier si des exceptions s'appliquent
3. **Traitement** : collecter les donnees dans tous les systemes concernes, preparer la reponse
4. **Reponse** : repondre dans le delai d'1 mois (prolongeable de 2 mois en cas de complexite ou de nombre eleve de demandes, avec information du demandeur dans le mois initial)
5. **Documentation** : enregistrer la demande, la reponse et les actions realisees dans le registre des demandes
6. **Gratuitement** : l'exercice des droits est gratuit. Possibilite de facturer des frais raisonnables en cas de demandes manifestement infondees ou excessives

### Recommandations operationnelles

- Mettre en place un formulaire en ligne dedie pour les demandes de droits (accessible depuis la politique de confidentialite)
- Centraliser la gestion des demandes aupres du DPO ou d'un point de contact unique
- Automatiser la recherche de donnees dans les systemes (API internes, requetes multi-bases)
- Prevoir un workflow d'escalade pour les cas complexes (demande d'effacement en conflit avec une obligation legale de conservation)
- Documenter les refus motives et informer le demandeur de son droit de saisir la CNIL

---

## Relations CNIL

### Interagir avec la CNIL

**Notification de violations (articles 33-34) :**

Procedure en cas de violation de donnees :
1. **Detection et qualification** (immediatement) : evaluer si l'incident constitue une violation de donnees personnelles (acces non autorise, perte, destruction, modification)
2. **Evaluation du risque** (< 24h) : determiner le niveau de risque pour les personnes (nature des donnees, nombre de personnes, consequences possibles)
3. **Notification CNIL** (72h maximum) : si la violation est susceptible d'engendrer un risque pour les droits et libertes. Utiliser le teleservice de notification sur le site de la CNIL. Informations requises : nature de la violation, categories et nombre de personnes, consequences probables, mesures prises
4. **Information des personnes** (sans delai injustifie) : si la violation est susceptible d'engendrer un risque eleve. Informer les personnes de maniere claire et comprehensible
5. **Documentation** : consigner chaque violation dans le registre des violations (meme celles non notifiees a la CNIL)

**Controles CNIL :**

Types de controles :
- Controle sur place (verification dans les locaux)
- Controle en ligne (verification a distance)
- Controle sur audition (convocation)
- Controle sur pieces (demande de documents)

Preparation :
- Designer un interlocuteur unique pour les controles CNIL
- Preparer un dossier de conformite a jour (registre, DPIA, DPA, politique de confidentialite, preuves de consentement, procedures de notification)
- Former les equipes d'accueil au comportement a adopter (cooperer, ne pas mentir, demander du temps si necessaire, ne pas fournir de documents non demandes)

### Sanctions CNIL — Echelle

| Categorie | Amende maximale | Exemples |
|---|---|---|
| **Tier 1** (art. 83.4) | 10 M EUR ou 2% du CA mondial | Privacy by Design, registre, DPO, DPIA, notification de violation |
| **Tier 2** (art. 83.5) | 20 M EUR ou 4% du CA mondial | Bases legales, droits des personnes, transferts, consentement |

Sanctions recentes significatives en France : Criteo (40 M EUR, 2023), Clearview AI (20 M EUR, 2022), Google (150 M EUR, 2022 — cookies), Amazon (746 M EUR, 2021 — Luxembourg). La tendance est a l'augmentation des montants et a la frequence des controles.

---

## Data Processing Agreements (Article 28)

### Clauses obligatoires d'un DPA

Le DPA entre le responsable de traitement et le sous-traitant doit inclure :

- Objet et duree du traitement
- Nature et finalite du traitement
- Type de donnees personnelles et categories de personnes concernees
- Obligations et droits du responsable de traitement
- Obligations du sous-traitant :
  - Traiter les donnees uniquement sur instruction documentee du responsable
  - Garantir la confidentialite (engagement des personnels)
  - Mettre en oeuvre les mesures de securite appropriees (article 32)
  - Ne pas recruter de sous-traitant ulterieur sans autorisation prealable
  - Assister le responsable pour les demandes de droits
  - Assister le responsable pour les DPIA et les consultations prealables
  - Supprimer ou restituer les donnees en fin de contrat
  - Mettre a disposition les informations necessaires pour audits et inspections

### Clauses supplementaires recommandees

- **Localisation des donnees** : preciser les pays de traitement et de stockage
- **Sous-traitance ulterieure** : liste exhaustive des sous-traitants ulterieurs, procedure de notification en cas de changement, droit d'objection
- **Mesures de securite** : detailler les mesures techniques (chiffrement, pseudonymisation, controle d'acces, sauvegarde) et organisationnelles (formation, politique interne, audit)
- **Notification de violations** : delai de notification au responsable (idealement < 24h, maximum 48h apres decouverte)
- **Transferts internationaux** : identifier les transferts et appliquer les mecanismes adequats (CCT, adequation)
- **Droit d'audit** : droit du responsable de realiser ou faire realiser des audits, avec modalites pratiques (preavis, frequence, rapports de certification acceptes comme alternative)

---

## Transferts Internationaux (Chapitre V)

### Mecanismes de transfert

**1. Decision d'adequation (article 45) :**
Les transferts vers les pays reconnus comme offrant un niveau de protection adequat ne necessitent pas de garantie supplementaire. Pays actuellement reconnus : Andorre, Argentine, Canada (organisations commerciales), Iles Feroe, Guernesey, Israel, Ile de Man, Japon, Jersey, Nouvelle-Zelande, Republique de Coree, Suisse, Royaume-Uni, Uruguay, Etats-Unis (Data Privacy Framework, decision d'adequation du 10 juillet 2023).

**2. Clauses Contractuelles Types (CCT/SCC) (article 46.2.c) :**
Les CCT adoptees par la Commission europeenne (decision d'execution 2021/914 du 4 juin 2021) sont le mecanisme le plus utilise. Deux scenarios couverts :
- Module 1 : Responsable de traitement vers responsable de traitement
- Module 2 : Responsable de traitement vers sous-traitant
- Module 3 : Sous-traitant vers sous-traitant
- Module 4 : Sous-traitant vers responsable de traitement

Obligations complementaires post-Schrems II (arret CJUE C-311/18 du 16 juillet 2020) :
- Realiser un **Transfer Impact Assessment (TIA)** : evaluer si la legislation du pays importateur permet aux autorites publiques d'acceder aux donnees de maniere disproportionnee
- Mettre en place des **mesures supplementaires** si necessaire : chiffrement de bout en bout (ou la cle reste sous controle de l'exportateur), pseudonymisation avant transfert, split ou multi-party processing

**3. Binding Corporate Rules (BCR) (article 47) :**
Pour les transferts intra-groupe. Procedure longue (12-18 mois d'approbation) mais solution perenne pour les multinationales. Approuvees par l'autorite chef de file dans le cadre du mecanisme de coherence.

**4. Derogations (article 49) :**
Utilisation limitee et ponctuelle : consentement explicite, execution d'un contrat, interets vitaux, motifs importants d'interet public, constatation ou exercice de droits en justice.

### EU-US Data Privacy Framework

Le DPF (decision d'adequation du 10 juillet 2023) permet les transferts vers les organisations americaines auto-certifiees. Points cles :
- Verifier que l'importateur est bien inscrit sur la liste DPF (dataprivacyframework.gov)
- Le DPF offre des garanties supplementaires par rapport au Privacy Shield annule (executive order 14086, mecanisme de recours DPRC)
- Risque de remise en cause : comme le Safe Harbor et le Privacy Shield, le DPF pourrait etre invalide par la CJUE. Preparer un plan B (CCT + TIA + mesures supplementaires)

---

## ePrivacy et Marketing Electronique

### Directive ePrivacy et droit francais (loi Informatique et Libertes)

La directive ePrivacy (2002/58/CE, modifiee en 2009) et sa transposition en droit francais (article 82 de la loi Informatique et Libertes) encadrent :

- **Cookies et traceurs** : consentement prealable requis sauf exceptions (cookies strictement necessaires, mesure d'audience sous conditions). Appliquer les lignes directrices CNIL du 17 septembre 2020
- **Prospection commerciale electronique** : opt-in prealable pour les particuliers (B2C). Exception pour les clients existants (soft opt-in) si produits/services analogues. Opt-out pour les professionnels (B2B), mais bonne pratique de privilegier l'opt-in
- **Confidentialite des communications electroniques** : protection du contenu et des metadonnees des communications

### Reglement ePrivacy (en discussion)

Le projet de reglement ePrivacy, en discussion depuis 2017, vise a remplacer la directive et a s'aligner sur le RGPD. Points cles du projet :
- Extension du champ aux services OTT (WhatsApp, Messenger, etc.)
- Harmonisation des regles sur les cookies au niveau europeen
- Renforcement de la protection des metadonnees
- Sanctions alignees sur le RGPD (4% du CA mondial)

---

## State of the Art (2024-2026)

### Enforcement et tendances CNIL

- **Augmentation des sanctions** : la CNIL et les autorites europeennes prononcent des amendes de plus en plus significatives. L'EDPB coordonne les actions paneuropeennes sur les grandes plateformes. En France, la procedure simplifiee de sanction permet a la CNIL de traiter plus rapidement les dossiers courants (amendes jusqu'a 20 000 EUR).

- **Focus sur l'IA** : la CNIL a publie en 2024 ses recommandations sur l'application du RGPD aux systemes d'IA (fiches pratiques IA et donnees personnelles). Points cles : base legale pour l'entrainement (interet legitime possible avec mise en balance rigoureuse), information des personnes, droit d'opposition pour les donnees de training, DPIA obligatoire pour les systemes a risque.

- **Cookies et consentement** : renforcement des controles sur les bannieres de consentement (dark patterns, refus aussi facile que l'acceptation). Les solutions de consent management platform (CMP) conformes aux specifications TCF v2.2 de l'IAB Europe deviennent un standard operationnel.

### EU AI Act et protection des donnees

Le reglement sur l'intelligence artificielle (EU AI Act, publie en juin 2024, application progressive 2024-2027) cree de nouvelles obligations qui s'articulent avec le RGPD :

- **Systemes a haut risque** : evaluation de conformite, gestion des risques, gouvernance des donnees, transparence, controle humain, robustesse, cybersecurite
- **IA generative** (modeles GPAI) : obligations de transparence, respect du droit d'auteur, divulgation des donnees d'entrainement (synthese)
- **Pratiques interdites** : scoring social, exploitation de vulnerabilites, biometrie en temps reel (avec exceptions limitees)
- **Articulation RGPD/AI Act** : le AI Act ne remplace pas le RGPD. Les deux reglements s'appliquent cumulativement. La DPIA RGPD et l'evaluation de conformite AI Act doivent etre coherentes

### Data Governance Act et Data Act

- **Data Governance Act** (DGA, applicable depuis septembre 2023) : encadre la reutilisation des donnees du secteur public, les services d'intermediation de donnees et l'altruisme des donnees
- **Data Act** (applicable a partir de septembre 2025) : droit d'acces et de portabilite des donnees generees par les objets connectes (IoT), encadrement de l'acces des autorites publiques aux donnees, regles pour les fournisseurs de cloud (portabilite, interoperabilite)

### Privacy Enhancing Technologies (PETs)

Technologies emergentes pour concilier exploitation des donnees et protection de la vie privee :

- **Differential privacy** : ajouter du bruit statistique aux donnees pour proteger les individus tout en preservant l'utilite analytique. Deploye par Apple, Google, US Census Bureau
- **Federated learning** : entrainer des modeles d'IA sans centraliser les donnees brutes (le modele va aux donnees, pas l'inverse). Utilise pour Google Keyboard, recherche medicale
- **Homomorphic encryption** : effectuer des calculs sur des donnees chiffrees sans les dechiffrer. Encore en phase de maturation pour les usages a grande echelle
- **Secure multi-party computation (SMPC)** : plusieurs parties calculent conjointement un resultat sans reveler leurs donnees respectives
- **Synthetic data** : generer des donnees synthetiques qui reproduisent les caracteristiques statistiques des donnees reelles sans contenir de donnees personnelles. Utilise pour le test, le developpement et l'entrainement de modeles IA
- **Zero-knowledge proofs** : prouver qu'une affirmation est vraie sans reveler l'information sous-jacente (ex. : prouver qu'un utilisateur a plus de 18 ans sans reveler sa date de naissance)

### Transferts internationaux post-DPF

- Le Data Privacy Framework est en place mais reste fragile juridiquement. Les entreprises prudentes maintiennent un "plan B" base sur les CCT avec TIA et mesures supplementaires
- La CJUE pourrait etre saisie d'une contestation du DPF (NOYB et d'autres ONG ont annonce une veille active)
- Le Royaume-Uni post-Brexit beneficie d'une decision d'adequation (expiration en juin 2025, renouvellement attendu) mais la divergence progressive du droit britannique cree une incertitude
- Les nouvelles lois extra-europeennes (LGPD bresilienne, PIPL chinoise, DPDP Act indien) multiplient les exigences de localisation et de conformite, rendant la gestion des transferts de plus en plus complexe pour les multinationales
