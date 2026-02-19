# Privacy Engineering — Privacy by Design & PETs

## Vue d'Ensemble

Le privacy engineering est la discipline qui integre la protection de la vie privee dans les systemes techniques des la conception, plutot que de l'ajouter comme une couche a posteriori. Il combine les principes du privacy by design avec des techniques concretes (anonymisation, pseudonymisation, chiffrement, minimisation) et des methodes de modelisation des menaces specifiques aux donnees personnelles.

---

## Privacy by Design — Implementation Technique

### Les 7 Principes en Pratique

**Principe 1 — Proactif** :

Integrer une analyse de confidentialite (PIA legere) a chaque nouveau projet lors du "kick-off" technique. Questions obligatoires :
- Ce projet traite-t-il des donnees personnelles ?
- Quelle est la base legale ?
- Une DPIA est-elle requise ?

Template "3 questions de confidentialite en kick-off" :
```
1. Quelles donnees personnelles allons-nous collecter ou traiter ?
   → Si la reponse est "aucune", documenter et clore l'analyse
2. Pourquoi en avons-nous besoin ? (finalite)
   → Si pas de finalite claire, ne pas collecter
3. Combien de temps ? (retention)
   → Definir la duree et implémenter la suppression automatique
```

**Principe 2 — Vie privee par defaut** :

Implementer les parametres les plus protecteurs par defaut :
- Profil public → defaut PRIVE
- Partage de localisation → defaut DESACTIVE
- Emails marketing → defaut OPT-OUT
- Cookies analytics → defaut REFUSE
- Visibilite des donnees autres utilisateurs → defaut MINIMUM

```python
# Exemple : création de compte avec paramètres privacy-first par défaut
DEFAULT_PRIVACY_SETTINGS = {
    "profile_visibility": "private",       # Pas "public"
    "location_tracking": False,             # Pas True
    "marketing_emails": False,              # Opt-out par defaut
    "analytics_cookies": False,             # Pas True
    "data_sharing_partners": False,         # Jamais par defaut
    "search_engine_indexing": False,        # Controle utilisateur
}
```

**Principe 3 — Integre dans la conception** :

Privacy User Stories dans le product backlog :
```
US-PRIV-001 : En tant que DPO, je veux que chaque nouveau traitement de donnees
personnelles soit documenté dans le registre avant sa mise en production.

US-PRIV-002 : En tant qu'utilisateur, je veux pouvoir supprimer mon compte et
toutes mes donnees associees en moins de 5 clics, avec confirmation par email.

US-PRIV-003 : En tant qu'administrateur, je veux voir un log d'audit de tous les
acces aux donnees personnelles sensibles dans les 90 derniers jours.
```

**Principe 4 — Minimisation active** :

Audit regulier des donnees collectees :
```sql
-- Identifier les colonnes "potentiellement excessives"
SELECT
    table_name,
    column_name,
    data_type,
    last_modified,  -- Si disponible : quand a-t-on derniere fois lu cette colonne ?
FROM information_schema.columns
WHERE table_schema = 'production'
    AND column_name IN (
        'birth_date', 'gender', 'address', 'phone',
        'nationality', 'ip_address', 'device_id'
    )
ORDER BY table_name, column_name;
```

---

## Techniques de Protection des Donnees

### 1. Pseudonymisation vs Anonymisation

**Distinction critique** :

| Technique | Definition RGPD | Toujours des donnees personnelles ? |
|---|---|---|
| **Pseudonymisation** | Remplacement des identifiants par un pseudonyme, avec cle de correspondance separee | OUI — reversible par le RT |
| **Anonymisation** | Transformation irreversible rendant impossible la re-identification | NON — sort du champ RGPD |

**Tests de l'anonymisation** (Article 29 Working Party Opinion 05/2014) :
- **Singling out** : peut-on isoler un individu dans le dataset ?
- **Linkability** : peut-on relier deux enregistrements concernant le meme individu ?
- **Inference** : peut-on deduire des informations sur un individu ?
Un dataset est vraiment anonyme uniquement si les 3 tests sont satisfaits.

**Pseudonymisation en pratique** :
```python
import hashlib
import hmac
import os

def pseudonymize_email(email: str, secret_key: bytes) -> str:
    """
    Pseudonymisation deterministe avec HMAC-SHA256
    La meme email donne toujours le meme pseudonyme (utile pour les jointures)
    Le secret_key est le moyen de re-identification — stocker separement
    """
    return hmac.new(secret_key, email.lower().encode(), hashlib.sha256).hexdigest()

# Usage
SECRET_KEY = os.environ.get('PSEUDONYMIZATION_KEY').encode()
pseudo = pseudonymize_email("user@example.com", SECRET_KEY)
# Resultat : "7a3f9b2c..." — non reversible sans la cle
```

### 2. k-Anonymite et Differential Privacy

**k-Anonymite** : un enregistrement est k-anonyme si au moins k-1 autres enregistrements ont les memes valeurs sur les quasi-identifiants (age, zip code, genre).

Exemple : si k=5, chaque combinaison (age_range, region, genre) apparait au moins 5 fois. Impossible d'identifier un individu unique.

```python
# Generalisation pour k-anonymite
def generalize_age(age: int) -> str:
    """Remplacer l'age exact par une tranche"""
    if age < 25:
        return "18-24"
    elif age < 35:
        return "25-34"
    elif age < 45:
        return "35-44"
    else:
        return "45+"

def generalize_zipcode(zipcode: str) -> str:
    """Conserver seulement les 2 premiers chiffres du code postal"""
    return zipcode[:2] + "xxx"
```

**Differential Privacy** : technique mathematique qui ajoute du "bruit calibre" aux statistiques pour proteger les individus tout en preservant l'utilite des agregats.

```python
import numpy as np

def dp_mean(values: list, epsilon: float = 1.0, sensitivity: float = 1.0) -> float:
    """
    Moyenne avec Differential Privacy (mecanisme Laplace)
    epsilon : budget de confidentialite (plus petit = plus prive, moins precis)
    sensitivity : variation max de la moyenne si on ajoute/retire un individu
    """
    true_mean = np.mean(values)
    noise = np.random.laplace(loc=0, scale=sensitivity/epsilon)
    return true_mean + noise

# Utilisation
ages = [25, 32, 45, 28, 56, 33, 41]
noisy_mean = dp_mean(ages, epsilon=0.5)
# Le bruit protege les individus mais la moyenne reste approximativement juste
```

### 3. Chiffrement des Donnees

**Chiffrement at rest** :

```python
from cryptography.fernet import Fernet
import base64
import os

class EncryptedField:
    """Chiffrement/dechiffrement transparent pour les champs sensibles"""

    def __init__(self, key: bytes = None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, plaintext: str) -> str:
        return self.cipher.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        return self.cipher.decrypt(ciphertext.encode()).decode()

# En base de donnees : stocker le ciphertext
# La cle est dans un secret manager (AWS Secrets Manager, HashiCorp Vault)
```

**Chiffrement en transit** : TLS 1.2+ obligatoire, TLS 1.3 prefere. HSTS (HTTP Strict Transport Security) active. Certificate pinning pour les apps mobiles critiques.

**Chiffrement de bout en bout (E2EE)** : Utilisable pour les messageries et documents sensibles. Signal Protocol (utilise par WhatsApp, Signal) ou PGP pour les emails.

### 4. Tokenisation

Remplacer une valeur sensible (numero de carte bancaire, IBAN, SSN) par un token opaque sans valeur intrinseque. Le mapping token → valeur est stocke dans un "token vault" separe et hautement securise.

Utilisation principale : PCI DSS (donnees de carte bancaire) — les marchands stockent uniquement des tokens, pas les numeros de carte. Même en cas de breach, les tokens sont inutilisables.

### 5. Donnees Synthetiques

Generer des donnees fictives statistiquement similaires aux donnees reelles, pour les environnements de developpement et de test.

Outils : Mimesis (Python), Faker (Python/JS), Gretel.ai (ML-based synthetic data), CTGAN (tabular GANs).

```python
from faker import Faker
import pandas as pd

fake = Faker('fr_FR')

def generate_synthetic_customers(n: int) -> pd.DataFrame:
    """Generer des clients fictifs pour les tests"""
    return pd.DataFrame({
        'nom': [fake.last_name() for _ in range(n)],
        'prenom': [fake.first_name() for _ in range(n)],
        'email': [fake.email() for _ in range(n)],
        'telephone': [fake.phone_number() for _ in range(n)],
        'adresse': [fake.address() for _ in range(n)],
        'date_naissance': [fake.date_of_birth(minimum_age=18, maximum_age=80) for _ in range(n)],
        'revenu_annuel': [fake.random_int(min=20000, max=120000, step=1000) for _ in range(n)],
    })

# Usage : remplacer les vrais clients par des synthetiques dans les envts de dev
df_test = generate_synthetic_customers(1000)
```

---

## LINDDUN — Privacy Threat Modeling

LINDDUN est un framework de modelisation des menaces specifique a la vie privee, analogue a STRIDE pour la securite.

### Les 7 Categories de Menaces LINDDUN

| Lettre | Menace | Description |
|---|---|---|
| **L**inkability | Liaison | Relier differents morceaux d'information sur un individu |
| **I**dentifiability | Identification | Identifier un individu dans un dataset |
| **N**on-repudiation | Non-repudiabilite | Impossible pour un individu de nier une action |
| **D**etectability | Detectabilite | Detecter qu'un individu est dans le systeme |
| **D**isclosure of information | Divulgation | Acces non autorise aux donnees personnelles |
| **U**nawareness | Manque de conscience | L'individu ne sait pas ce qu'il se passe avec ses donnees |
| **N**on-compliance | Non-conformite | Violation des lois et regulations |

### Processus d'Analyse LINDDUN

1. **Creer un DFD** (Data Flow Diagram) du systeme : entites, processus, data stores, flux
2. **Pour chaque flux ou store** : evaluer la pertinence de chaque categorie LINDDUN
3. **Prioriser par risque** : probabilite × impact sur la vie privee
4. **Definir des contre-mesures** : technologiques (chiffrement, minimisation) et organisationnelles (formation, processus)

---

## DPIA — Methodologie Complete

### Quand est-ce obligatoire

Criteres du G29 (Article 29 Working Party) — DPIA obligatoire si >= 2 criteres :
1. Evaluation/scoring (credit scoring, profiling)
2. Decision automatisee avec effet legal ou significatif
3. Surveillance systematique
4. Donnees sensibles ou tres personnelles (sante, finances, localisation)
5. Traitement a grande echelle
6. Combinaison de datasets
7. Personnes vulnerables (enfants, patients, employes)
8. Usage innovant de technologie (biometrie, IA)
9. Transfert hors UE avec risque eleve
10. Exclusion du benefice d'un service

### Structure de la DPIA (conforme CNIL)

```
1. DESCRIPTION DU TRAITEMENT
   1.1 Contexte et finalites
   1.2 Donnees traitees
   1.3 Personnes concernees
   1.4 Destinataires
   1.5 Durees de conservation
   1.6 Ressources et processus impliques

2. NECESSITE ET PROPORTIONNALITE
   2.1 La finalite est-elle legitime ?
   2.2 Les donnees collectees sont-elles minimales ?
   2.3 La duree de conservation est-elle proportionnee ?
   2.4 Les droits des personnes sont-ils garantis ?

3. EVALUATION DES RISQUES
   Pour chaque risque :
   - Acces non autorise (confidentialite)
   - Modification non desiree (integrite)
   - Disparition (disponibilite)

   Pour chaque risque : identifier les menaces, evaluer la gravite
   et la vraisemblance, calculer le niveau de risque (faible/moyen/eleve/critique)

4. MESURES POUR TRAITER LES RISQUES
   Pour chaque risque eleve : mesures techniques ET organisationnelles
   Risque residuel apres mesures : acceptable ou non ?

5. VALIDATION
   Avis du DPO : [favorable / defavorable / avec reserves]
   Date et signature
   Consultation CNIL si risque residuel reste eleve
```
