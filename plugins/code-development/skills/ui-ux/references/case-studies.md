# Études de cas — UI/UX Design, Design Systems & Accessibility

## Cas 1 : Construction d'un design system from scratch

### Contexte
CareConnect, éditeur SaaS de télémédecine (70 personnes, 12 développeurs frontend), gère 3 produits : une app patient (React Native), un portail médecin (Next.js), et un back-office admin (React + Vite). Chaque produit a été développé indépendamment avec ses propres composants, styles et conventions. L'équipe design (3 designers Figma) produit des maquettes qui divergent entre les produits.

### Problème
Le bouton primaire existe en 7 variantes différentes à travers les 3 produits (couleurs, border-radius, padding, typographie). Une modification de la charte graphique (demandée par le marketing) nécessite des changements dans 45 fichiers à travers 3 repositories. Le temps de développement d'une nouvelle feature est rallongé de 30% car chaque développeur recrée des composants existants. L'accessibilité est inconsistante : le portail médecin est WCAG AA, l'app patient échoue sur 12 critères.

### Approche
1. **Design tokens W3C** : Définition de 150+ tokens (couleurs, typographie, spacing, elevation, border-radius, motion) en format W3C Design Tokens. Source unique dans Figma Variables, exportée via Style Dictionary vers CSS custom properties, Swift constants et Kotlin constants.
2. **Atomic design avec shadcn/ui** : Construction du design system en couches atomiques. Les atoms (Button, Input, Badge, Avatar) utilisent shadcn/ui comme base avec Radix UI pour les primitives accessibles. Les molecules (SearchBar, FormField, Card) composent les atoms. Les organisms (DataTable, Modal, Navigation) composent les molecules.
3. **Storybook comme documentation vivante** : Chaque composant est documenté dans Storybook avec : toutes les variantes, les états (default, hover, focus, disabled, error), les exemples d'usage do/don't, les specs d'accessibilité (rôles ARIA, navigation clavier), et les interactions testées (Testing Library).
4. **Pipeline design-to-code** : Workflow automatisé : Figma Variables → export JSON → Style Dictionary → CSS/Swift/Kotlin → publish npm package → consommé par les 3 produits. Les designers modifient les tokens dans Figma, le pipeline propage automatiquement.

### Résultat
- 85 composants partagés entre les 3 produits (vs composants dupliqués)
- Temps de développement d'une nouvelle page réduit de 40% (composants réutilisables)
- Modification de charte graphique : 1 changement de token → propagation automatique aux 3 produits en < 1h
- Conformité WCAG 2.2 AA sur les 3 produits (vs 1 sur 3 avant)
- Onboarding d'un nouveau designer : 3 jours (vs 3 semaines) grâce à la documentation Storybook
- Design consistency score (audit interne) passé de 45% à 94%

### Leçons apprises
- Les design tokens sont le fondement non-négociable d'un design system multi-produit — sans eux, la cohérence est impossible à maintenir.
- shadcn/ui + Radix comme base offre le meilleur compromis : composants accessibles par défaut ET entièrement personnalisables (copier, pas installer).
- Le design system est un produit — il nécessite un owner, une roadmap, des releases versionnées, et du feedback utilisateur (les développeurs).

---

## Cas 2 : Remédiation accessibilité WCAG 2.2 AA

### Contexte
ServicePlus, plateforme de services à la personne (50 personnes), sert 100K utilisateurs mensuels dont 15% ont plus de 65 ans. L'application web React est visuellement aboutie mais n'a jamais fait l'objet d'un audit d'accessibilité. L'European Accessibility Act (EAA) entre en vigueur en juin 2025 et s'applique à l'entreprise.

### Problème
Un audit WCAG 2.2 AA commandé à un cabinet spécialisé révèle 87 non-conformités : contraste insuffisant sur 40% des textes (ratio 2.8:1 au lieu de 4.5:1), navigation clavier impossible sur les formulaires multi-étapes, lecteur d'écran incapable de comprendre le tableau de bord (absence de landmarks, rôles ARIA manquants, images décoratives sans alt=""), et un carousel auto-playing sans possibilité de pause. Le score Lighthouse Accessibility est de 42/100.

### Approche
1. **Priorisation par impact** : Classification des 87 non-conformités en 3 niveaux : P1 (bloquant, 23 items — navigation clavier, contraste critique, formulaires inaccessibles), P2 (majeur, 35 items — ARIA, landmarks, images), P3 (mineur, 29 items — focus visible, reflow, timing). Sprint 0 dédié aux P1.
2. **Refonte des composants de base** : Remplacement des composants custom (Select, Modal, Tabs, Datepicker) par des composants Radix UI headless, intrinsèquement accessibles. Ajout de focus management programmatique dans les modals et les formulaires multi-étapes.
3. **Tests d'accessibilité automatisés** : Intégration d'axe-core dans le pipeline CI (via @axe-core/react en dev, axe-playwright dans les tests E2E). Quality gate : zéro violation critique/sérieuse autorisée. Storybook accessibility addon pour la vérification visuelle pendant le développement.
4. **Tests avec utilisateurs réels** : Sessions de test avec 5 utilisateurs utilisant des technologies d'assistance (VoiceOver sur Mac, NVDA sur Windows, TalkBack sur Android). Les retours corrigent des problèmes non détectés par les outils automatisés : ordre de lecture illogique, instructions verbales manquantes, interactions confuses au lecteur d'écran.

### Résultat
- Score Lighthouse Accessibility passé de 42 à 98/100
- 87 non-conformités réduites à 3 (toutes P3, en cours de correction)
- Conformité WCAG 2.2 AA validée par l'audit de suivi — prêt pour l'EAA
- Taux de complétion des formulaires pour les utilisateurs 65+ passé de 45% à 78% (+73%)
- Taux de rebond global réduit de 8% — l'accessibilité améliore l'UX pour tous
- Satisfaction utilisateur (CSAT) des 65+ passée de 3.2/5 à 4.5/5

### Leçons apprises
- Les composants headless (Radix, Headless UI) résolvent 60% des problèmes d'accessibilité "by default" — investir dans la migration plutôt que dans le patching.
- Les outils automatisés (axe-core) ne détectent que 30-40% des problèmes d'accessibilité — les tests avec des utilisateurs réels utilisant des technologies d'assistance sont indispensables.
- L'accessibilité améliore l'UX pour TOUS les utilisateurs, pas seulement les personnes en situation de handicap — c'est un argument business, pas seulement légal.

---

## Cas 3 : Optimisation Core Web Vitals pour le SEO

### Contexte
TravelNow, plateforme de réservation de voyages (40 personnes), génère 70% de son trafic via le SEO. L'application Next.js (App Router) affiche des pages de destination riches avec des images haute résolution, des cartes interactives, des avis clients et des widgets de pricing. Le site utilise Tailwind CSS et charge 15 scripts tiers (analytics, chat, remarketing).

### Problème
Google dégrade le ranking SEO en raison de Core Web Vitals médiocres : LCP de 5.8s (seuil : 2.5s), INP de 380ms (seuil : 200ms), CLS de 0.35 (seuil : 0.1). Les données CrUX (Chrome UX Report) montrent que seulement 25% des utilisateurs ont une expérience "good". Le trafic organique a chuté de 22% en 3 mois. L'analyse montre que les images non optimisées (JPEG 2-5MB), les scripts tiers bloquants, et l'hydratation JavaScript massive sont les principaux responsables.

### Approche
1. **Image optimization** : Migration de toutes les images vers le composant `next/image` avec format AVIF/WebP automatique, lazy loading natif, et placeholder blur (LQIP). Les images hero utilisent `priority` pour le preload. Taille maximale : 200KB pour les images above-the-fold. CDN d'images (Cloudinary) avec responsive srcset.
2. **Script tiers management** : Audit des 15 scripts tiers avec Web Vitals attribution. 5 scripts supprimés (inutilisés), 7 migrés vers `next/script` avec strategy="lazyOnload", les 3 scripts critiques (analytics first-party) chargés avec strategy="afterInteractive". Implémentation d'un Partytown worker pour isoler les scripts tiers du main thread.
3. **INP optimization** : Identification des interactions lentes via les Long Animation Frames (LoAF) API. Le widget de pricing recalcule à chaque interaction — migration vers `useDeferredValue` et `startTransition` pour les mises à jour non-urgentes. Les event handlers lourds sont déportés dans des Web Workers.
4. **CLS elimination** : Réservation d'espace pour toutes les images (aspect-ratio CSS), web fonts avec `font-display: optional` et size-adjust pour éliminer le FOUT, placeholders pour les contenus dynamiques (avis, pricing), et suppression des publicités qui provoquent des layout shifts.

### Résultat
- LCP passé de 5.8s à 1.9s (÷3, dans le "good" threshold)
- INP passé de 380ms à 120ms (÷3, dans le "good" threshold)
- CLS passé de 0.35 à 0.04 (÷9, dans le "good" threshold)
- Pourcentage d'utilisateurs avec expérience "good" passé de 25% à 88%
- Trafic organique : +35% en 2 mois après l'amélioration (récupération + gain de ranking)
- Taux de conversion : +12% (corrélation directe avec la vitesse de chargement)

### Leçons apprises
- Les images non optimisées sont le responsable #1 du LCP — next/image + AVIF + CDN résout 80% du problème.
- Les scripts tiers sont le principal destructeur de performance — auditer chaque script et questionner sa nécessité avant de l'optimiser.
- L'INP (Interaction to Next Paint) est le Core Web Vital le plus difficile à optimiser — il nécessite une compréhension fine du main thread et l'utilisation de `startTransition` / Web Workers.
