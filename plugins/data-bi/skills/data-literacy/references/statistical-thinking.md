# Statistical Thinking — Frameworks, Critical Thinking & Common Fallacies

## Overview

Ce document de reference couvre les fondamentaux de la pensee statistique pour les professionnels non-data : les concepts essentiels pour interpreter correctement les donnees, identifier les erreurs de raisonnement courantes, et prendre des decisions eclairees. Il ne s'agit pas d'un cours de statistiques formelles, mais d'un guide de pensee critique appliquee aux donnees dans un contexte business. Utiliser ce guide pour ancrer chaque analyse dans la rigueur intellectuelle, meme (et surtout) quand les resultats semblent evidents.

This reference covers the fundamentals of statistical thinking for non-data professionals: essential concepts for correctly interpreting data, identifying common reasoning errors, and making informed decisions. This is not a formal statistics course but a guide to critical thinking applied to data in a business context.

---

## Data Literacy Frameworks

### Le modele a 4 competences

La data literacy repose sur quatre competences distinctes et complementaires :

**1. Data Reading (Lecture des donnees)**
La capacite a lire et comprendre les donnees presentees dans des tableaux, graphiques et rapports. Cela inclut :
- Identifier le type de graphique et comprendre comment le lire (axes, echelles, legendes).
- Comprendre les unites de mesure et les periodes couvertes.
- Distinguer les donnees brutes des donnees transformees (moyennes, pourcentages, indices).
- Identifier ce qui est presente et ce qui est absent (selections, filtres, exclusions).

**2. Data Working (Manipulation des donnees)**
La capacite a manipuler et preparer les donnees pour l'analyse. Cela inclut :
- Filtrer, trier et grouper des donnees dans un tableur ou un outil BI.
- Comprendre les joins et les relations entre tables.
- Effectuer des calculs basiques (taux de croissance, part de marche, moyenne ponderee).
- Detecter et traiter les valeurs aberrantes et les donnees manquantes.

**3. Data Analysis (Analyse des donnees)**
La capacite a extraire du sens des donnees par l'analyse. Cela inclut :
- Identifier des tendances, des patterns et des anomalies.
- Comparer des groupes et des periodes de maniere rigoureuse.
- Formuler et tester des hypotheses avec les donnees disponibles.
- Evaluer la significativite et la robustesse des conclusions.

**4. Data Communication (Communication des donnees)**
La capacite a communiquer des insights data de maniere claire et persuasive. Cela inclut :
- Choisir le bon format de visualisation pour le message.
- Structurer un argument fonde sur les donnees.
- Adapter le niveau de detail a l'audience.
- Formuler des recommandations actionnables.

### Le framework DIKW (Data-Information-Knowledge-Wisdom)

Comprendre la hierarchie de la valeur des donnees :

| Niveau | Definition | Exemple |
|---|---|---|
| **Data** | Faits bruts, non traites | "4,523 commandes le 15 janvier" |
| **Information** | Donnees contextualisees et structurees | "Les commandes du 15 janvier sont 23% au-dessus de la moyenne" |
| **Knowledge** | Information interpretee avec expertise | "Ce pic correspond a notre campagne email + un jour de soldes" |
| **Wisdom** | Capacite a prendre la bonne decision | "Planifier les prochaines campagnes email pendant les periodes de soldes pour maximiser le ROI" |

L'objectif de la data literacy est de permettre a chaque collaborateur de remonter cette pyramide — de la donnee brute a la decision sage.

### Les niveaux de maturite individuelle

**Niveau 0 — Data-Averse**
Evite les donnees, se fie a l'intuition et a l'experience. Perçoit les donnees comme menacantes ou inaccessibles. Intervention necessaire : sensibilisation, destigmatisation, formation introductive.

**Niveau 1 — Data-Aware**
Comprend l'importance des donnees mais ne sait pas les utiliser. Peut lire un graphique simple mais ne peut pas challenger les conclusions. Intervention : formation aux bases de la lecture de donnees.

**Niveau 2 — Data-Literate**
Peut lire, interpreter et communiquer avec les donnees. Pose les bonnes questions, identifie les limites evidentes. Peut utiliser un outil BI en self-service. Intervention : perfectionnement, cas pratiques, mentorat.

**Niveau 3 — Data-Fluent**
Integre les donnees naturellement dans chaque decision. Peut construire des analyses, challenger les methodologies, et former les autres. Candidat ideal pour le role de data champion. Intervention : leadership, contribution aux standards, enseignement.

---

## Statistical Concepts for Non-Data Roles

### Les metriques fondamentales

**Moyenne, mediane, mode — et pourquoi la mediane est souvent meilleure**

La moyenne est la metrique la plus utilisee et la plus mal utilisee. Elle est sensible aux valeurs extremes (outliers) et peut etre trompeuse pour les distributions asymetriques.

Exemple : dans une equipe de 10 personnes ou 9 gagnent 40K EUR et 1 gagne 400K EUR, le salaire moyen est 76K EUR — un chiffre qui ne represente personne. La mediane (40K EUR) est beaucoup plus representative.

**Regle pratique** : utiliser la mediane pour les donnees asymetriques (salaires, durees, montants de transactions) et la moyenne pour les donnees symetriques (temperatures, scores normalises).

**Percentiles et distribution**
Les percentiles decoupent les donnees en centiles. Le p50 est la mediane, le p95 est la valeur en-dessous de laquelle se trouvent 95% des observations. En performance (temps de reponse, duree de livraison), le p95 ou p99 est plus important que la moyenne : il represente l'experience des utilisateurs les plus defavorises.

**Taux et proportions**
Toujours preciser le denominateur. "100 reclamations" est un nombre absolu sans sens. "100 reclamations pour 50,000 commandes (0.2%)" est une information. Comparer les taux, pas les nombres absolus, quand les denominateurs different.

**Taux de croissance**
Le taux de croissance simple [(Vn - Vn-1) / Vn-1] est trompeur pour les comparaisons sur des bases differentes. Une croissance de 100% sur une base de 10 est moins significative qu'une croissance de 5% sur une base de 10,000. Toujours contextualiser avec la base.

### Variabilite et dispersion

**Ecart-type et variance**
La moyenne seule ne suffit jamais. Deux datasets peuvent avoir la meme moyenne avec des dispersions radicalement differentes. L'ecart-type mesure la dispersion autour de la moyenne : plus il est grand, plus les donnees sont dispersees.

Exemple business : deux campagnes marketing ont un ROI moyen de 3x. La campagne A a un ecart-type de 0.2 (resultats predictibles), la campagne B a un ecart-type de 2.5 (resultats tres variables). La campagne A est probablement preferable malgre le meme ROI moyen.

**Coefficient de variation (CV)**
Le ratio ecart-type / moyenne, exprime en pourcentage. Permet de comparer la variabilite entre des metriques d'echelles differentes. Un CV > 100% signale une dispersion extreme.

### Correlation et regression

**Coefficient de correlation (r)**
Mesure la force et la direction d'une relation lineaire entre deux variables. Varie de -1 (correlation negative parfaite) a +1 (correlation positive parfaite). r = 0 signifie absence de relation lineaire (mais pas necessairement absence de relation).

**Interpretation pratique** :
- |r| < 0.3 : correlation faible
- 0.3 < |r| < 0.7 : correlation moderee
- |r| > 0.7 : correlation forte

**R-carre (R2)**
Le pourcentage de variance expliquee par le modele. R2 = 0.64 signifie que le modele explique 64% de la variation observee. Ne pas confondre avec la qualite predictive — un R2 eleve sur les donnees d'entrainement peut masquer un overfitting.

**Regression : quand l'utiliser**
La regression lineaire est l'outil de base pour quantifier une relation. Utiliser pour :
- Estimer l'impact d'une variable sur une autre ("chaque jour de retard de livraison est associe a une baisse de 2.3 points de NPS").
- Controler pour les variables confondantes ("apres controle de la taille de l'entreprise et du secteur, le prix n'a pas d'effet significatif sur le churn").
- Faire des projections (avec prudence et intervalles de confiance).

---

## Critical Thinking with Data

### Le framework CRAP (Critical Review of Analytical Products)

Pour chaque analyse ou rapport recu, appliquer systematiquement ces quatre questions :

**C — Currency (Actualite)**
Les donnees sont-elles a jour ? Quelle est la date de derniere mise a jour ? Les conclusions sont-elles encore valides dans le contexte actuel ? Des donnees de 6 mois dans un marche volatile peuvent etre obsoletes.

**R — Reliability (Fiabilite)**
Quelle est la source des donnees ? Comment ont-elles ete collectees ? Y a-t-il des biais de selection, de mesure ou de survie ? La taille de l'echantillon est-elle suffisante ?

**A — Authority (Autorite)**
Qui a realise l'analyse ? A-t-elle ete revue par un pair (peer review) ? Y a-t-il des conflits d'interet ? L'analyste avait-il une conclusion predeterminee ?

**P — Purpose (Objectif)**
Pourquoi cette analyse a-t-elle ete realisee ? Est-ce pour informer ou pour convaincre ? Les donnees ont-elles ete selectionnees pour soutenir une these (cherry-picking) ?

### Les 10 questions a poser a toute analyse

1. **Quelle est la source des donnees ?** Donnees internes (CRM, analytics) vs externes (enquetes, donnees publiques). Chaque source a ses biais.
2. **Quelle est la taille de l'echantillon ?** N = 15 n'est pas N = 15,000. Les petits echantillons produisent des resultats instables.
3. **Quelle periode est couverte ?** Les tendances courtes peuvent etre du bruit. Demander une vue plus longue.
4. **Quelles sont les exclusions ?** Quelles donnees ont ete filtrees ? Pourquoi ? Les exclusions peuvent changer radicalement les conclusions.
5. **Correlation ou causalite ?** L'analyse montre-t-elle une association ou un lien causal ? Quel est le mecanisme explicatif ?
6. **Quels sont les confounders potentiels ?** Y a-t-il des variables cachees qui pourraient expliquer la relation observee ?
7. **Les resultats sont-ils statistiquement significatifs ?** La difference observee est-elle reelle ou pourrait-elle etre du au hasard ?
8. **Quelle est la taille de l'effet ?** Un resultat peut etre statistiquement significatif mais pratiquement negligeable.
9. **Les resultats sont-ils reproductibles ?** Si on refait l'analyse avec d'autres donnees ou une autre methode, obtient-on les memes conclusions ?
10. **Qui beneficie de cette conclusion ?** Chercher les incitations qui pourraient biaiser l'analyse.

---

## Common Fallacies & Misinterpretations

### Correlation vs Causation — La mere de toutes les erreurs

**Le probleme** : le cerveau humain est programme pour detecter des patterns et inferer des causalites. Quand deux variables sont correlees, nous concluons instinctivement que l'une cause l'autre.

**Les trois explications alternatives a une correlation** :
1. **Causalite inversee** : A ne cause pas B, c'est B qui cause A. ("Les pays avec plus d'hopitaux ont plus de maladies" — parce que les maladies causent la construction d'hopitaux, pas l'inverse.)
2. **Variable confondante** : un facteur C cause a la fois A et B. ("Les ventes de glaces sont correlees aux noyades" — parce que la chaleur cause les deux.)
3. **Hasard** : avec suffisamment de variables testees, certaines correlations apparaitront par pur hasard (probleme des comparaisons multiples). Avec 100 variables non reliees, on trouvera ~5 correlations "significatives" par hasard au seuil de 5%.

**Comment etablir une causalite** :
- **Experimentation randomisee (A/B test)** : la methode gold standard. Assigner aleatoirement les sujets a un groupe test et un groupe controle.
- **Quasi-experimentation** : difference-in-differences, regression discontinuity, variables instrumentales quand l'experimentation n'est pas possible.
- **Criteres de Bradford Hill** : force de l'association, consistance, specificite, temporalite, gradient biologique, plausibilite, coherence, experimentation, analogie.

**Langage a utiliser** :
- Correlation : "X est associe a Y", "X co-varie avec Y"
- Causalite : "X cause Y", "X provoque Y" (uniquement avec evidence experimentale ou quasi-experimentale)

### Survivorship Bias — Le biais du survivant

**Le probleme** : analyser uniquement les "survivants" (succes, clients actifs, entreprises existantes) en ignorant ceux qui ont echoue ou disparu. Cela conduit a des conclusions faussement optimistes.

**Exemples classiques** :
- Analyser les traits communs des startups a succes sans etudier les startups qui ont echoue avec les memes traits.
- Etudier la satisfaction client en ne sondant que les clients actifs (les insatisfaits sont partis).
- Evaluer la performance d'un portefeuille de fonds en excluant les fonds fermes (survivorship bias des fonds d'investissement).
- Analyser les fonctionnalites des produits reussis sans examiner les produits echecs qui avaient les memes fonctionnalites.

**Comment l'eviter** :
- Toujours demander : "Quels sont les cas qui ne sont PAS dans mes donnees ?" (churned customers, projets abandonnes, produits retires).
- Inclure les "morts" dans l'analyse (cohorte complete, pas seulement les survivants).
- Analyser les causes d'attrition/echec avec autant de rigueur que les causes de succes.

### Simpson's Paradox — Le paradoxe de Simpson

**Le probleme** : une tendance observee dans plusieurs groupes separes s'inverse quand les groupes sont combines. C'est l'un des paradoxes les plus deroutants et les plus dangereux en analytics.

**Exemple classique — Admissions a Berkeley (1973)** :
- Donnees agreagees : les femmes avaient un taux d'admission inferieur aux hommes (semble discriminatoire).
- Donnees par departement : dans la plupart des departements, les femmes avaient un taux d'admission egal ou superieur aux hommes.
- Explication : les femmes candidataient davantage dans les departements les plus selectifs.

**Exemple business** :
- Donnees agreagees : le produit A a un meilleur taux de conversion que le produit B.
- Donnees par canal : sur chaque canal (web, mobile, store), le produit B a un meilleur taux de conversion que A.
- Explication : le produit A est surrepresente sur le canal web qui a un taux de conversion de base plus eleve.

**Comment l'eviter** :
- Toujours desagreger les donnees par les dimensions pertinentes avant de conclure.
- Quand une tendance globale contredit les tendances par sous-groupe, investiguer la composition des sous-groupes.
- Presenter les resultats par sous-groupe ET au global, en expliquant les divergences.

### Autres biais et sophismes frequents

**Base Rate Neglect (Negligence du taux de base)**
Ignorer la probabilite a priori quand on interprete un resultat. Exemple : un test de fraude avec 99% de precision semble excellent, mais si le taux de fraude reel est de 0.1%, la majorite des alertes seront des faux positifs (theoreme de Bayes). Toujours demander : "Quel est le taux de base du phenomene ?"

**Cherry-Picking (Cueillette selective)**
Selectionner les donnees ou periodes qui soutiennent la conclusion souhaitee en ignorant celles qui la contredisent. Signe d'alerte : une analyse qui ne presente que des donnees favorables sans discussion des resultats contraires. Exiger la vue complete.

**Anchoring Bias (Biais d'ancrage)**
Le premier chiffre presente influence disproportionnellement l'interpretation des chiffres suivants. Annoncer "le marche est de 50 milliards" avant de presenter une opportunite de 5 millions change la perception. Etre conscient de l'ordre de presentation des chiffres et de leur effet d'ancrage.

**Ecological Fallacy (Erreur ecologique)**
Inferer des conclusions au niveau individuel a partir de donnees au niveau agrege. "Les regions avec un revenu moyen eleve votent X" ne signifie pas que les individus riches de ces regions votent X. Les correlations au niveau agrege ne se transferent pas necessairement au niveau individuel.

**Regression to the Mean (Regression vers la moyenne)**
Apres une performance extreme (tres bonne ou tres mauvaise), la performance suivante tend a se rapprocher de la moyenne. Cela ne signifie pas que l'intervention entre les deux mesures a eu un effet. Un commercial qui a un mois exceptionnellement bon aura probablement un mois suivant plus moyen, avec ou sans intervention du management.

**Texas Sharpshooter Fallacy (Sophisme du tireur texan)**
Trouver un pattern dans les donnees apres coup et pretendre que c'etait l'hypothese de depart. Equivalent de dessiner la cible autour des impacts de balles. L'exploration de donnees (data dredging) genere des "decouvertes" qui sont en realite du bruit statistique. Distinguer les analyses exploratoires (generation d'hypotheses) des analyses confirmatoires (test d'hypotheses).

---

## Data-Driven Decision Making

### Le spectrum Decision-Making

Toutes les decisions ne necessitent pas le meme niveau d'analyse data :

| Type de decision | Approche recommandee | Niveau de rigueur data |
|---|---|---|
| **Reversible, faible impact** | Intuition + donnees legeres | Faible — decider vite, mesurer apres |
| **Reversible, impact moyen** | Donnees descriptives + experience | Moyen — dashboard, tendances |
| **Irreversible, impact eleve** | Analyse rigoureuse + experimentation | Eleve — A/B test, modele predictif |
| **Irreversible, impact strategique** | Analyse multi-scenario + comite | Tres eleve — scenarios, sensitivites, peer review |

La cle est de calibrer l'investissement analytique a l'importance et la reversibilite de la decision. Sur-analyser les decisions mineures est aussi couteux que sous-analyser les decisions majeures.

### Le cycle Hypothese-Experimentation-Mesure

**1. Formuler une hypothese claire et falsifiable**
- Mauvais : "On devrait ameliorer l'onboarding."
- Bon : "Reduire le nombre d'etapes d'onboarding de 7 a 3 augmentera le taux de completion de 45% a 70%."

**2. Designer l'experimentation**
- A/B test si possible (randomisation, taille d'echantillon suffisante, metrique primaire definie a l'avance).
- Quasi-experimentation si l'A/B test n'est pas possible (before/after avec controle, difference-in-differences).

**3. Definir les criteres de decision a l'avance**
- Quel seuil de significativite ? (generalement p < 0.05, mais a adapter au contexte)
- Quelle taille d'effet minimale est business-significative ? (Minimum Detectable Effect)
- Combien de temps durer l'experimentation ? (calculer la puissance statistique)

**4. Mesurer et interpreter**
- Respecter la duree prevue — ne pas s'arreter prematurement sur un resultat "significatif" (peeking problem).
- Presenter les intervalles de confiance, pas seulement le point estimate.
- Verifier les sous-groupes pour le paradoxe de Simpson.

**5. Decider et documenter**
- Prendre la decision selon les criteres definis a l'avance.
- Documenter le resultat et le raisonnement pour l'apprentissage organisationnel.
- Si le resultat est non-significatif, c'est aussi un resultat : il evite de gaspiller des ressources sur une initiative sans impact.

---

## Hypothesis Testing Basics

### Concepts fondamentaux (sans jargon)

**Test d'hypothese en langage courant** :
Un test d'hypothese repond a la question : "La difference que j'observe est-elle reelle ou due au hasard ?"

**Hypothese nulle (H0)** : "Il n'y a pas de difference / pas d'effet." C'est l'hypothese par defaut que le test cherche a rejeter.

**Hypothese alternative (H1)** : "Il y a une difference / un effet." C'est ce qu'on cherche a demontrer.

**p-value** : la probabilite d'observer un resultat aussi extreme (ou plus) si l'hypothese nulle est vraie. p = 0.03 signifie : "Si il n'y avait reellement pas de difference, il y aurait 3% de chances d'observer un ecart aussi grand par hasard."
- p < 0.05 : conventionnellement considere comme "statistiquement significatif" (mais ce seuil est arbitraire).
- p < 0.01 : evidence plus forte.
- p > 0.05 : on ne peut pas rejeter l'hypothese nulle (ce qui ne prouve pas qu'elle est vraie).

**Attention aux erreurs d'interpretation de la p-value** :
- La p-value N'EST PAS la probabilite que l'hypothese nulle soit vraie.
- La p-value N'EST PAS la probabilite que le resultat soit du au hasard.
- Un p < 0.05 NE SIGNIFIE PAS que l'effet est important — il peut etre statistiquement significatif mais negligeable en pratique.

### Erreurs de Type I et Type II

| | H0 est vraie (pas d'effet reel) | H0 est fausse (effet reel existe) |
|---|---|---|
| **Rejeter H0** | Erreur Type I (faux positif) - probabilite = alpha | Decision correcte (puissance) |
| **Ne pas rejeter H0** | Decision correcte | Erreur Type II (faux negatif) - probabilite = beta |

- **Type I (faux positif)** : conclure qu'il y a un effet alors qu'il n'y en a pas. Consequence : investir dans une initiative sans impact. Controle par le seuil alpha (generalement 5%).
- **Type II (faux negatif)** : manquer un effet reel. Consequence : abandonner une initiative qui aurait fonctionne. Controle par la taille d'echantillon et la puissance statistique (generalement viser 80% de puissance).

### Significativite statistique vs significativite pratique

La significativite statistique repond a : "L'effet est-il reel ?"
La significativite pratique repond a : "L'effet est-il suffisamment grand pour justifier l'action ?"

Avec un echantillon suffisamment grand, TOUTE difference devient statistiquement significative, meme un effet minuscule. Toujours completer avec la taille d'effet :
- "Le nouveau design augmente le taux de conversion de 0.02% (p < 0.001)" — statistiquement significatif mais probablement sans impact business.
- "Le nouveau design augmente le taux de conversion de 3.5% (p = 0.04)" — statistiquement et pratiquement significatif.

### Intervalles de confiance — plus utiles que les p-values

Un intervalle de confiance a 95% donne la fourchette de valeurs dans laquelle se situe probablement le vrai effet. Plus informatif qu'un simple oui/non du test d'hypothese :
- "L'effet est une augmentation de 3.5% [IC 95% : 0.8% - 6.2%]" — on est raisonnablement confiants que l'effet est positif, avec une fourchette de magnitude.
- "L'effet est une augmentation de 1.2% [IC 95% : -2.1% - 4.5%]" — l'intervalle inclut zero, l'effet pourrait etre nul.

Privilegier les intervalles de confiance dans les communications business : ils transmettent a la fois la direction, la magnitude et l'incertitude.
