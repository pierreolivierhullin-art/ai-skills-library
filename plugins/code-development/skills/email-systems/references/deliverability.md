# Délivrabilité Email — SPF, DKIM, DMARC et Réputation d'Envoi

> Référence complète pour garantir que les emails arrivent en boîte de réception. Couvre l'authentification DNS (SPF, DKIM, DMARC), la gestion de la réputation d'envoi, le warm-up des nouvelles IPs, les listes de blocage, les feedback loops et les métriques clés.

---

## SPF — Sender Policy Framework

### Syntaxe et mécanismes

Le SPF permet aux serveurs de réception de vérifier que l'IP expéditrice est autorisée à envoyer pour le domaine déclaré dans l'en-tête `Mail From`.

```
v=spf1 [mécanismes] [modificateurs] [qualificateur-all]
```

**Mécanismes courants :**

| Mécanisme | Description | Exemple |
|-----------|-------------|---------|
| `include:` | Inclure les IPs d'un autre enregistrement SPF | `include:_spf.resend.com` |
| `ip4:` | Autoriser une IPv4 ou un CIDR | `ip4:203.0.113.5` ou `ip4:203.0.113.0/24` |
| `ip6:` | Autoriser une IPv6 | `ip6:2001:db8::1` |
| `a:` | Autoriser les IPs du record A du domaine | `a:mail.monapp.fr` |
| `mx:` | Autoriser les IPs des enregistrements MX | `mx` |
| `redirect=` | Déléguer complètement à un autre enregistrement | `redirect=_spf.autredomaine.fr` |

**Qualificateurs `all` :**
- `~all` — SoftFail : les emails non listés sont acceptés mais marqués (recommandé pendant la migration)
- `-all` — HardFail : les emails non listés doivent être rejetés (recommandé en production)
- `+all` — Passer tout le monde (ne jamais utiliser — inutile)
- `?all` — Neutre (éviter — pas de protection)

**Exemple complet avec plusieurs ESPs :**

```dns
; SPF record pour monapp.fr avec Resend, SendGrid et un serveur SMTP dédié
monapp.fr. IN TXT "v=spf1 include:_spf.resend.com include:sendgrid.net ip4:198.51.100.25 -all"
```

**Limite des 10 lookups DNS :** Le SPF autorise au maximum 10 lookups DNS récursifs. Chaque `include:` consomme 1 lookup, plus les lookups récursifs de l'enregistrement inclus. Utiliser SPF Flattening (outil comme dmarcian ou easydmarc) pour consolider les IPs en records `ip4:` directs si la limite est atteinte.

```bash
# Vérifier le nombre de lookups SPF avec MXToolbox
# https://mxtoolbox.com/spf.aspx
# Ou en ligne de commande :
dig TXT monapp.fr | grep spf
```

### Gérer plusieurs ESPs

Quand plusieurs services envoient depuis le même domaine, lister tous leurs `include:` dans un seul enregistrement SPF. Ne jamais créer deux enregistrements SPF TXT pour le même domaine — seul le premier sera utilisé.

```dns
; INCORRECT — deux enregistrements SPF sur le même domaine
monapp.fr. IN TXT "v=spf1 include:_spf.resend.com -all"
monapp.fr. IN TXT "v=spf1 include:sendgrid.net -all"  ; ignoré

; CORRECT — un seul enregistrement fusionné
monapp.fr. IN TXT "v=spf1 include:_spf.resend.com include:sendgrid.net -all"
```

---

## DKIM — DomainKeys Identified Mail

### Processus de signature

DKIM ajoute une signature cryptographique à chaque email sortant. Le serveur récepteur récupère la clé publique dans le DNS et vérifie la signature.

**Flux de signature :**
1. Le serveur d'envoi calcule un hash du corps de l'email (body canonicalization)
2. Il calcule un hash des en-têtes sélectionnés (header canonicalization)
3. Il signe ces hashes avec la clé privée RSA (2048 bits minimum) ou Ed25519
4. La signature est ajoutée dans l'en-tête `DKIM-Signature`
5. Le serveur récepteur récupère la clé publique via `selector._domainkey.domaine.fr`
6. Il vérifie la signature — si elle est valide, l'email n'a pas été altéré en transit

### Canonicalization

```
; DKIM-Signature header example
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
  d=monapp.fr; s=resend;
  h=from:to:subject:date:message-id:content-type;
  bh=<hash-du-body>;
  b=<signature-base64>
```

- `c=relaxed/relaxed` — Canonicalization header/body. `relaxed` tolère les espaces blancs normalisés (plus robuste). `simple` est strict et peut échouer si des équipements réseau modifient les en-têtes.
- `h=` — Liste des en-têtes signés. Inclure au minimum : `from`, `to`, `subject`, `date`, `message-id`.
- `s=` — Selector : identifie quelle clé publique utiliser dans le DNS.

### CNAME vs TXT records

| Type | Avantage | Inconvénient | Recommandé pour |
|------|----------|--------------|-----------------|
| **CNAME** | Rotation de clé automatique par l'ESP | Dépendance à l'ESP pour les clés | Resend, SendGrid, Postmark (ils gèrent) |
| **TXT** | Contrôle total, clé autogérée | Rotation manuelle obligatoire | Serveurs SMTP auto-hébergés |

```dns
; DKIM avec CNAME (délégation à Resend) — recommandé
resend._domainkey.monapp.fr. IN CNAME resend._domainkey.resend.com.

; DKIM avec TXT (clé publique directement)
mail2024._domainkey.monapp.fr. IN TXT "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A..."
```

### Rotation des clés et selector management

Effectuer la rotation des clés DKIM tous les 6 à 12 mois. La procédure sans interruption de service :

1. Générer une nouvelle paire de clés RSA 2048 bits
2. Publier la nouvelle clé publique dans le DNS avec un nouveau selector (`mail2025._domainkey`)
3. Attendre la propagation DNS (TTL — généralement 24-48h)
4. Configurer l'ESP pour signer avec le nouveau selector
5. Conserver l'ancienne clé publique dans le DNS pendant 48h (pour les emails déjà en transit)
6. Supprimer l'ancien selector DNS

```bash
# Générer une paire de clés DKIM (openssl)
openssl genrsa -out dkim_private.pem 2048
openssl rsa -in dkim_private.pem -pubout -out dkim_public.pem

# Extraire la clé publique au format DKIM TXT
openssl rsa -in dkim_private.pem -pubout -outform der | base64 | tr -d '\n'
```

---

## DMARC — Domain-Based Message Authentication

### Syntaxe du record DMARC

```dns
_dmarc.monapp.fr. IN TXT "v=DMARC1; p=reject; pct=100; rua=mailto:dmarc-rua@monapp.fr; ruf=mailto:dmarc-ruf@monapp.fr; adkim=s; aspf=s; fo=1"
```

**Paramètres clés :**

| Paramètre | Valeurs | Description |
|-----------|---------|-------------|
| `p=` | `none`, `quarantine`, `reject` | Politique appliquée aux emails qui échouent |
| `pct=` | 0–100 | Pourcentage des emails soumis à la politique |
| `rua=` | `mailto:...` | Adresse pour les rapports agrégés (quotidiens) |
| `ruf=` | `mailto:...` | Adresse pour les rapports forensiques (par email) |
| `adkim=` | `r` (relaxed), `s` (strict) | Alignement DKIM : strict = même domaine exact |
| `aspf=` | `r` (relaxed), `s` (strict) | Alignement SPF |
| `fo=` | `0`, `1`, `d`, `s` | Conditions d'envoi des rapports forensiques |
| `ri=` | entier (secondes) | Intervalle de reporting (défaut : 86400 = 24h) |

### Progression DMARC recommandée

Ne jamais passer directement à `p=reject`. Suivre cette progression sur 4 à 8 semaines :

```dns
; Semaine 1-2 : Surveillance pure, aucun impact sur la délivrance
_dmarc.monapp.fr. IN TXT "v=DMARC1; p=none; rua=mailto:dmarc@monapp.fr"

; Semaine 3-4 : Quarantaine sur 10% — identifier les faux positifs
_dmarc.monapp.fr. IN TXT "v=DMARC1; p=quarantine; pct=10; rua=mailto:dmarc@monapp.fr"

; Semaine 5 : Quarantaine sur 100%
_dmarc.monapp.fr. IN TXT "v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc@monapp.fr"

; Semaine 6+ : Rejet complet — protection maximale contre le spoofing
_dmarc.monapp.fr. IN TXT "v=DMARC1; p=reject; pct=100; rua=mailto:dmarc@monapp.fr; ruf=mailto:dmarc-ruf@monapp.fr"
```

### Analyse des rapports XML DMARC

Les rapports agrégés (RUA) sont envoyés au format XML compressé (`.xml.gz`). Utiliser un outil comme dmarcian, EasyDMARC ou Postmark DMARC pour les parser.

```xml
<!-- Exemple de rapport agrégé DMARC -->
<feedback>
  <report_metadata>
    <org_name>Google Inc.</org_name>
    <date_range>
      <begin>1700000000</begin>
      <end>1700086400</end>
    </date_range>
  </report_metadata>
  <policy_published>
    <domain>monapp.fr</domain>
    <p>reject</p>
  </policy_published>
  <record>
    <row>
      <source_ip>198.51.100.1</source_ip>
      <count>1523</count>
      <policy_evaluated>
        <disposition>none</disposition>
        <dkim>pass</dkim>
        <spf>pass</spf>
      </policy_evaluated>
    </row>
    <row>
      <!-- IP inconnue qui essaie d'usurper le domaine -->
      <source_ip>203.0.113.99</source_ip>
      <count>47</count>
      <policy_evaluated>
        <disposition>reject</disposition>
        <dkim>fail</dkim>
        <spf>fail</spf>
      </policy_evaluated>
    </row>
  </record>
</feedback>
```

### BIMI — Brand Indicators for Message Identification

BIMI affiche le logo de l'entreprise dans les clients email supportés (Gmail, Yahoo, Apple Mail). Prérequis : DMARC `p=quarantine` ou `p=reject` avec `pct=100`.

```dns
; Record BIMI
default._bimi.monapp.fr. IN TXT "v=BIMI1; l=https://monapp.fr/logo-bimi.svg; a=https://monapp.fr/vmc.pem"
```

- `l=` — URL du logo au format SVG Tiny PS (spécification stricte)
- `a=` — URL du VMC (Verified Mark Certificate) — requis par Gmail, émis par DigiCert ou Entrust (~$1500/an)
- Le logo doit être hébergé sur HTTPS, au format SVG Tiny PS, < 32 KB

---

## Google Postmaster Tools

Enregistrer le domaine d'envoi sur [postmaster.google.com](https://postmaster.google.com) pour surveiller la réputation.

### Métriques clés

- **Domain Reputation** : Low / Medium / High / Very High — indicateur synthétique de la confiance Gmail dans le domaine
- **IP Reputation** : réputation des IPs d'envoi (importante si IPs dédiées)
- **Spam Rate** : pourcentage d'emails marqués comme spam par les utilisateurs Gmail. Garder sous 0.10% ; alerte critique à 0.30%
- **Authentication** : taux SPF/DKIM/DMARC passant
- **Delivery Errors** : taux d'erreurs 4xx/5xx lors de la connexion SMTP
- **Feedback Loop** : volume des signalements spam enrichi pour les grands expéditeurs

```
Interpréter le spam rate Gmail :
< 0.10%  → Excellent — continuer ainsi
0.10-0.30% → Attention — analyser le contenu et le ciblage
> 0.30%  → Critique — Gmail peut throttler ou bloquer les envois
> 0.08%  → Seuil de conformité Google Bulk Sender Guidelines (2024)
```

---

## Microsoft SNDS — Smart Network Data Services

[Inscription SNDS](https://sendersupport.olc.protection.outlook.com/snds/) — surveiller la réputation spécifiquement pour Outlook/Hotmail/Live.

**Métriques SNDS :**
- **Complaint Rate** : taux de plaintes utilisateurs Outlook
- **Trap Hits** : emails arrivant sur des adresses pièges (honeypots Microsoft)
- **Data color** : Vert (< 0.3% plaintes, 0 pièges), Jaune, Rouge

Outlook utilise le programme JMRP (Junk Mail Reporting Program) pour le feedback loop — s'inscrire séparément via le portail Microsoft.

---

## Warm-Up Plan — Nouvelles IPs et Nouveaux Domaines

Toute nouvelle IP ou nouveau domaine d'envoi doit être "réchauffé" progressivement. Les filtres antispam font confiance aux IPs avec un historique positif établi sur plusieurs semaines.

### Plan de warm-up sur 4 semaines

| Jour | Volume quotidien | Engagement cible | Segments prioritaires |
|------|-----------------|-----------------|----------------------|
| 1 | 50 | > 50% ouverture | Meilleurs clients (90j actifs) |
| 2–3 | 100 | > 40% | Actifs 60j |
| 4–7 | 250 | > 35% | Actifs 90j |
| 8–14 | 1 000 | > 30% | Actifs 180j |
| 15–21 | 5 000 | > 25% | Actifs 12 mois |
| 22–30 | 10 000 | > 20% | Liste complète segmentée |
| 30+ | Volume nominal | > 15% | Envois réguliers |

**Règles du warm-up :**
- Commencer par les abonnés les plus engagés (ouvrent régulièrement)
- Ne jamais envoyer de cold outreach pendant le warm-up
- Surveiller Google Postmaster Tools quotidiennement
- Si le spam rate monte au-dessus de 0.08%, réduire le volume de 50% immédiatement et attendre 48h

---

## Listes de Blocage (Blocklists)

### Principales blocklists

| Blocklist | Impact | Comment vérifier | Comment se faire retirer |
|-----------|--------|-----------------|--------------------------|
| **Spamhaus SBL/XBL/PBL** | Très élevé — bloque la majorité des récepteurs | `dig <ip>.zen.spamhaus.org` | [spamhaus.org/removal](https://www.spamhaus.org/removal/) |
| **Barracuda BRBL** | Élevé | [barracudacentral.org/lookups](https://www.barracudacentral.org/lookups) | Formulaire de suppression en ligne |
| **URIBL/SURBL** | Moyen — bloque les domaines dans les URLs | [uribl.com/lookup](https://uribl.com/lookup.shtml) | Contacter uribl.com |
| **Spamhaus DBL** | Élevé — domaines dans les emails | `dig <domaine>.dbl.spamhaus.org` | Via portail Spamhaus |
| **MXToolbox** | Agrégateur de 100+ blocklists | [mxtoolbox.com/blacklists](https://mxtoolbox.com/blacklists.aspx) | Retrait auprès de chaque liste |

```bash
# Vérifier une IP dans les principales blocklists
# Via MXToolbox CLI ou API
curl "https://api.mxtoolbox.com/api/v1/Lookup/blacklist/?argument=198.51.100.25&Authorization=API_KEY"

# Vérification manuelle Spamhaus
dig 25.100.51.198.zen.spamhaus.org TXT
; Réponse 127.0.0.x = listé, NXDOMAIN = propre
```

### Procédure de retrait d'une blocklist

1. Identifier la cause (source de spam, compromission de compte, configuration incorrecte)
2. Corriger le problème à la source avant de demander le retrait
3. Soumettre la demande via le formulaire officiel de chaque blocklist
4. Documenter les mesures correctives prises (les opérateurs de blocklist peuvent demander des preuves)
5. Délai typique : 24-72h pour Spamhaus, jusqu'à 2 semaines pour Barracuda

---

## Feedback Loops (FBL)

Les feedback loops transmettent les signalements spam des utilisateurs à l'expéditeur sous forme de rapports ARF (Abuse Reporting Format).

### Yahoo/AOL FBL

S'inscrire via [senders.yahoo.com](https://senders.yahoo.com). Prérequis : DKIM configuré sur le domaine. Yahoo envoie un rapport ARF pour chaque signalement spam.

```
; Email ARF reçu via FBL Yahoo
From: feedback@arf.mail.yahoo.com
Subject: FBL Complaint Report
Content-Type: multipart/report; report-type=feedback-report

; Le rapport inclut : l'email original + les headers suffisants pour identifier
; l'abonné via le List-Unsubscribe-Post ou l'ID de tracking
```

### Microsoft JMRP

S'inscrire via [sendersupport.olc.protection.outlook.com/snds/JMRP.aspx](https://sendersupport.olc.protection.outlook.com/snds/JMRP.aspx). Fonctionne par plage d'IPs.

**Traitement automatique des FBL :**

```typescript
// Traitement automatique des rapports FBL
async function traiterRapportFBL(arfEmail: string): Promise<void> {
  // Extraire l'email plaignant du rapport ARF
  const emailDestinataire = extraireDestinataire(arfEmail);

  if (!emailDestinataire) {
    logger.warn('FBL reçu sans destinataire identifiable');
    return;
  }

  // Ajouter à la liste de suppression immédiatement
  await suppressionList.ajouter(emailDestinataire, {
    raison: 'PLAINTE_FBL',
    source: 'yahoo_fbl',
    date: new Date(),
  });

  // Désabonner de tous les types de marketing
  await preferences.désabonnerTout(emailDestinataire);

  logger.info(`FBL traité : ${emailDestinataire} ajouté à la suppression`);
}
```

---

## Gestion des Bounces

### Types de bounces

**Hard bounce (permanent) :**
- Adresse email inexistante (code SMTP 550, 551, 553)
- Domaine inexistant (code SMTP 550)
- Compte fermé
- Action : désactiver l'adresse **immédiatement** et ne plus jamais envoyer

**Soft bounce (temporaire) :**
- Boîte de réception pleine (code SMTP 452)
- Serveur temporairement indisponible (code SMTP 421, 450)
- Message trop volumineux (code SMTP 552)
- Action : retry avec backoff exponentiel pendant 24-72h, puis désactiver si persiste

### Seuils critiques

```
Bounce rate total :     < 2%    → Acceptable
                        2-5%    → Attention — nettoyer la liste
                        > 5%    → Critique — les ESPs peuvent suspendre le compte

Hard bounce rate :      < 0.5%  → Acceptable
                        > 1%    → Critique — liste de mauvaise qualité

Soft bounce rate :      < 3%    → Acceptable
                        > 5%    → Vérifier les domaines bloqueurs
```

```typescript
// Politique de retry pour les soft bounces
const retryPolicy = {
  maxAttempts: 3,
  delays: [
    1000 * 60 * 5,    // 5 minutes
    1000 * 60 * 60,   // 1 heure
    1000 * 60 * 60 * 24, // 24 heures
  ],
  onFinalFailure: async (email: string, smtpCode: number) => {
    if (smtpCode >= 550) {
      // Hard bounce — désactiver immédiatement
      await suppressionList.ajouter(email, 'HARD_BOUNCE');
    } else {
      // Soft bounce persistant — désactiver provisoirement
      await suppressionList.ajouter(email, 'SOFT_BOUNCE_PERSISTANT');
    }
  },
};
```

---

## Métriques de Délivrabilité

### Inbox rate vs delivered rate

```
Delivered rate = (Envoyés - Bounces) / Envoyés × 100
  → Mesure : l'email a été accepté par le serveur récepteur
  → Ne garantit PAS l'arrivée en boîte de réception

Inbox rate = (Arrivés en inbox) / (Envoyés - Bounces) × 100
  → Mesure : l'email est arrivé en boîte principale (pas spam)
  → Nécessite un outil tiers (GlockApps, Litmus, EmailOnAcid, Postmaster Tools)
```

### Tableau de bord des métriques clés

| Métrique | Excellent | Acceptable | Alerte |
|----------|-----------|------------|--------|
| Inbox rate | > 95% | 90-95% | < 90% |
| Spam placement | < 1% | 1-5% | > 5% |
| Hard bounce | < 0.5% | 0.5-2% | > 2% |
| Soft bounce | < 2% | 2-5% | > 5% |
| Spam rate Gmail | < 0.05% | 0.05-0.10% | > 0.10% |
| Complaint rate | < 0.05% | 0.05-0.15% | > 0.15% |
| Open rate (général) | > 30% | 20-30% | < 20% |

### Sender Score

[Sender Score](https://www.senderscore.org) (Return Path/Validity) attribue un score de 0 à 100 aux IPs d'envoi. Un score supérieur à 80 est requis pour une bonne délivrabilité. Les facteurs principaux : historique de plaintes, bounces, volumes d'envoi, présence sur les blocklists.

---

## Checklist Délivrabilité

Vérifier avant la mise en production :

1. SPF configuré avec `-all` en production (pas `~all`)
2. DKIM avec clé RSA 2048 bits minimum — vérifier via `dig TXT selector._domainkey.domaine.fr`
3. DMARC au minimum `p=none` avec rua configuré pour collecter les rapports
4. MX record configuré pour le domaine d'envoi (requis par certains filtres)
5. PTR record (reverse DNS) configuré pour l'IP d'envoi si IP dédiée
6. Unsubscribe link dans chaque email marketing (obligatoire RGPD et CAN-SPAM)
7. List-Unsubscribe header dans les en-têtes HTTP (`List-Unsubscribe-Post: List-Unsubscribe=One-Click`)
8. Google Postmaster Tools enregistré et surveillance activée
9. Processus de traitement des bounces et FBL automatisé
10. Liste de suppression vérifiée avant chaque envoi
