# Term Sheets et Valorisation — Mecanismes et Negociation

## Vue d'Ensemble

Le term sheet est le document non-contraignant qui definit les termes principaux d'un investissement. Il precede les documents juridiques definitifs (Pacte d'Actionnaires, SPA). Comprendre ses clauses est critique — certaines sont standards, d'autres peuvent significativement impacter le contrôle et le rendement des fondateurs lors d'un exit.

---

## Structure d'un Term Sheet

### Partie 1 — Economic Terms (Termes Economiques)

#### Valorisation

**Pre-money valuation** : valeur de la societe AVANT l'investissement.
**Post-money valuation** : valeur APRES = Pre-money + Investissement.

```
Exemple :
Pre-money : 8 000 000 EUR
Investissement : 2 000 000 EUR
Post-money : 10 000 000 EUR
Part de l'investisseur : 2M / 10M = 20%
```

**Comment les VCs determinent la valorisation en early stage** :
- Comparables (deals recents dans le secteur, au meme stage)
- Multiple d'ARR (ex : 10x ARR pour SaaS Serie A → 200K ARR = 2M EUR pre-money)
- Perception de la traction et du potentiel (tres subjectif en pre-seed)
- Competition entre investisseurs (le meilleur levier de fondateur)

#### Liquidation Preference

Clause determinant l'ordre et le montant que les investisseurs reccoivent en cas de vente de la societe.

**1x Non-Participating (Standard)** :
L'investisseur recoit EN PREMIER soit 1x son investissement, soit sa participation au pro-rata de la vente — il choisit le plus avantageux.

```
Exemple :
Investissement : 2M EUR pour 20%
Vente : 15M EUR

Option A : 1x preference = 2M EUR
Option B : 20% de 15M = 3M EUR
→ L'investisseur choisit l'Option B (3M EUR)

Vente : 5M EUR

Option A : 1x preference = 2M EUR
Option B : 20% de 5M = 1M EUR
→ L'investisseur choisit l'Option A (2M EUR) — protection downside
```

**1x Participating (A Eviter)** :
L'investisseur recoit 1x son investissement EN PREMIER, PUIS participe au pro-rata du reste.

```
Vente : 15M EUR
Step 1 : l'investisseur recoit 2M EUR (preference)
Step 2 : l'investisseur recoit 20% × 13M = 2.6M EUR
Total investisseur : 4.6M EUR

→ Les fondateurs reccoivent 15M - 4.6M = 10.4M
→ VS 12M EUR avec une preference 1x non-participating
```

**Multiple preference (2x, 3x — a absolument refuser)** :
L'investisseur recoit 2x ou 3x son investissement avant quiconque.

**Regles de negociation** :
- Standard marche : 1x non-participating. Tout ce qui est au-dela est defavorable pour les fondateurs.
- Si le VC insiste sur participating : demander un cap (ex : participating mais plafonné quand il recoit 3x son investissement).

#### Option Pool (ESOP)

Pool de stock-options reserve pour les futurs employes.

**Piege du pre-money option pool** :
Si l'option pool est créé AVANT la levee (pre-money), il dilue les fondateurs — pas les investisseurs.

```
Pre-money : 8M EUR
Fondateurs : 100%
Option pool cree : 10% (pre-money)
Fondateurs post-option pool : 90%

Apres levee de 2M EUR pour 20% (post-money) :
Fondateurs : 72%
Investisseurs : 20%
Option pool : 8%
```

**Contre-proposition** : option pool post-money (cree apres la levee — dilue tous les actionnaires proportionnellement). Ou negocier la taille du pool (10% vs 15%).

---

### Partie 2 — Control Terms (Termes de Contrôle)

#### Board Composition

Le Board of Directors prend les decisions strategiques majeures.

**Standard Serie A** : 5 membres
- 2 fondateurs
- 1 VC lead
- 1 independant (choisi conjointement)
- 1 observateur VC (sans droit de vote)

**Serie B+** : souvent 7 membres (addition d'un second VC et d'un second independant)

**Pieges** :
- Eviter que les investisseurs aient une majorite au board
- Negocier soigneusement les droits de veto (quelles decisions requierent l'accord du board vs de l'assemblee generale)

#### Droits de Vote

**Actions ordinaires** : 1 action = 1 vote.

**Actions de preference** (des investisseurs) : peuvent avoir des droits speciaux — veto sur certaines decisions.

**Decisions typiquement soumises au veto investisseur** (raisonnables) :
- Emission de nouvelles actions
- Vente de la societe
- Modification des statuts
- Dividendes

**Decisions a ne PAS conceder en veto** :
- Decisions operationnelles (embauches, produit, pricing)
- Budget annuel (sauf si tres significatif)
- Changement de CEO (negotiable mais a eviter)

#### Drag-Along Rights

Si une majorite d'actionnaires agree a vendre la societe, les actionnaires minoritaires SONT OBLIGES de vendre aussi.

**Usage** : eviter qu'un petit actionnaire bloque une vente attractive pour tous.

**Threshold standard** : 75-80% des actions doivent approuver avant que le drag-along s'applique.

#### Tag-Along Rights

Si un actionnaire majoritaire vend ses actions, les minoritaires ont le droit de PARTICIPER a la vente dans les memes conditions.

**Usage** : protege les minoritaires contre une vente "clandestine" qui ne leur beneficierait pas.

---

### Partie 3 — Anti-Dilution

**Contexte** : si votre societe leve un round suivant a une valorisation inferieure (down round), les investisseurs precedents voient leur participation diluee. L'anti-dilution les protege.

**Broad-Based Weighted Average (Standard, Acceptable)** :
Ajuste le prix de conversion de facon proportionnelle a la taille du down round. Impact modere.

```
Formule simplifiee :
Nouveau prix = Ancien prix × (Shares avant + Investissement nouveau / Nouveau prix)
               ÷ (Shares avant + Investissement nouveau / Ancien prix)
```

**Full Ratchet (A Refuser) ** :
L'investisseur precedent recoit des actions au nouveau prix reduit, comme s'il avait investi au nouveau prix depuis le debut. Impact potentiellement devastateur sur la cap table.

```
Exemple :
Serie A : 10M EUR pre-money, 2M levés pour 20%
Down round Serie B : 5M EUR pre-money, 3M levés

Full ratchet : l'investisseur Serie A recoit des actions supplementaires
comme si son 2M EUR avait ete investi a 5M EUR pre-money.
Résultat : fondateurs dilues massivement.
```

**Negociation** : refuser le full ratchet systematiquement. Si le VC insiste, proposer un broad-based avec un cap temporel (ex : ne s'applique que sur les 24 premiers mois).

---

## Mecanismes de Valorisation Avances

### SAFE (Simple Agreement for Future Equity)

Instrument de financement pre-seed/seed cree par Y Combinator. Pas d'actions, pas de dette — le SAFE convertit en actions lors du prochain tour qualifiant.

**Avantages** :
- Pas de valorisation a negocier (ou avec un simple plafond)
- Clos en 1-2 semaines (vs 2-3 mois pour un tour classique)
- Pas d'interets (vs obligations convertibles)

**Termes d'un SAFE** :
- **Valuation Cap** : la valorisation maximale a laquelle le SAFE convertit. Ex : cap de 5M EUR → si la Serie A est a 10M EUR pre-money, le SAFE convertit comme si la valeur etait 5M EUR (les detenteurs de SAFE recoivent plus d'actions).
- **Discount** : reduction sur le prix du prochain tour. Ex : 20% discount → le SAFE convertit a 80% du prix de la Serie A.
- **MFN (Most Favoured Nation)** : si un SAFE suivant est emis a de meilleures conditions, le SAFE MFN s'aligne.

**Exemple de conversion SAFE** :
```
SAFE : 500K EUR avec cap a 5M EUR
Serie A : 2M EUR levés a 10M EUR pre-money (prix par action : 10€)

Conversion SAFE :
- Sans cap : converti a 10€ / action → 50 000 actions
- Avec cap 5M EUR : converti a 5€ / action → 100 000 actions (favorise le SAFE holder)
```

### Obligations Convertibles (OC)

Similaire aux SAFE mais ce sont des dettes : portent des interets (typiquement 5-8%) et ont une maturite (24-36 mois).

**Avantage pour l'investisseur** : si la societe echoue, l'OC est prioritaire sur les actionnaires en liquidation.

**Usage** : moins frequent en France depuis l'essor des BSPCE et des SAFEs, mais encore utilise par certains family offices.

---

## Cap Table Modeling

### Simulation d'une Levee

```python
# Simulation simple de cap table

class CapTable:
    def __init__(self):
        self.shareholders = {}
        self.total_shares = 0

    def add_shareholder(self, name, shares):
        self.shareholders[name] = shares
        self.total_shares += shares

    def raise_round(self, investor_name, investment, pre_money_valuation):
        """Simuler une levee de fonds."""
        price_per_share = pre_money_valuation / self.total_shares
        new_shares = investment / price_per_share

        self.shareholders[investor_name] = new_shares
        self.total_shares += new_shares

        print(f"\nAprès levée de {investment:,.0f} EUR à {pre_money_valuation:,.0f} EUR pre-money:")
        print(f"Post-money valuation: {pre_money_valuation + investment:,.0f} EUR")
        print(f"Prix par action: {price_per_share:.2f} EUR")
        print(f"\nCap table:")
        for name, shares in self.shareholders.items():
            pct = shares / self.total_shares * 100
            print(f"  {name}: {shares:,.0f} actions ({pct:.1f}%)")

# Exemple
cap_table = CapTable()
cap_table.add_shareholder("Fondateur A", 4_000_000)
cap_table.add_shareholder("Fondateur B", 3_500_000)
cap_table.add_shareholder("ESOP Pool", 500_000)

cap_table.raise_round("Business Angel Seed", 500_000, 4_000_000)
cap_table.raise_round("VC Serie A", 3_000_000, 12_000_000)
```

---

## Checklist de Negociation d'un Term Sheet

**Points non-negociables (a refuser)** :
- [ ] Participating preference (sauf avec cap raisonnable)
- [ ] Full ratchet anti-dilution
- [ ] Majorite du board pour les investisseurs
- [ ] Veto sur les decisions operationnelles

**Points a negocier attentivement** :
- [ ] Taille du option pool (negocier post-money)
- [ ] Seuil du drag-along (demander 80%+ vs 50%)
- [ ] Composition du board et selection de l'independant
- [ ] Definition des "qualified financing" pour la conversion des SAFEs

**Points habituellement standards** :
- [ ] Pro-rata rights (investisseurs au round suivant)
- [ ] Information rights (etats financiers trimestriels)
- [ ] 1x non-participating preference
- [ ] ROFR (Right of First Refusal) sur les cessions secondaires
