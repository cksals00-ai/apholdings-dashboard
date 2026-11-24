---
no: 17
slug: which-ai-for-which-job
date: 2026-10-03
category: Pratique
tags: Choix du modèle · Recommandations par tâche · Coût · Test en direct
title: Quelle IA pour quelle tâche — les usages indiqués par les entreprises elles-mêmes et le test que nous utilisons
summary: Documents, code, voix, images, traitement en masse. Nous avons réuni les usages recommandés dans les sources officielles de chaque entreprise, et décrit comment savoir en 30 minutes si cela convient à votre travail.
---
> Cet article a été rédigé en brouillon avec l'IA (Claude), puis relu par l'éditeur. Anthropic, qui a créé Claude, y figure aussi ; nous nous sommes donc appuyés uniquement sur **les documents que chaque entreprise a écrits sur son propre produit**, et il ne s'agit pas de résultats de tests indépendants qui les comparent. Nous ne disons pas que l'un est meilleur que l'autre.

Il est difficile de répondre en une ligne à « Quelle IA est la meilleure pour cette tâche ? ». En revanche, **les usages que chaque entreprise recommande** figurent dans sa documentation officielle. Nous les avons regroupés par tâche.

## Ce que les entreprises recommandent selon la tâche

- **Documents courants, présentations, tableurs, correction de bogues bien délimités :** Anthropic présente Claude Sonnet 5.5 pour ces usages. C'est le plus rapide et le moins cher.
- **Longs travaux de développement complexes (grande migration de code, audit) :** Anthropic recommande Opus 5.5, et OpenAI GPT-6.1 Sol (codage, utilisation de l'ordinateur, travail professionnel). Les deux ont publié, dans leurs propres annonces, des scores pour cet usage.
- **Longs travaux de développement, agents qui travaillent automatiquement :** la documentation de Google présente Gemini 3.8 Flash pour cet usage.
- **Assistant vocal, synthèse vocale :** Google indique Gemini 3.8 Live pour les conversations vocales à faible latence et Gemini 3.8 Flash TTS pour la synthèse vocale expressive.
- **Images :** Google indique Nano Banana Pro pour la résolution 4K et les compositions complexes comportant du texte, et Nano Banana 2 pour la production rapide en grande quantité.
- **Travaux où le prix compte le plus et où les volumes sont importants :** la documentation d'Anthropic propose de commencer avec un petit modèle de classe Haiku puis de monter en gamme si cela ne suffit pas ; Google indique Gemini 3.1 Flash-Lite.

## Changer de modèle n'est pas la seule façon de réduire le coût

La documentation d'Anthropic recommande, avant de changer de modèle, d'essayer d'**ajuster l'intelligence, la vitesse et le coût avec le « réglage d'effort (effort) »**. De plus, les deux entreprises proposent un « cache » qui fait fortement baisser le prix lorsque la même entrée est réutilisée (0,10 dollar chez OpenAI, 0,20 dollar chez Anthropic, par million de tokens). L'effet est important si l'on joint chaque fois les mêmes consignes.

## Le test en 30 minutes

Nous avons raccourci, à notre manière, la marche à suivre proposée par la documentation d'Anthropic.

1. Choisissez trois tâches que vous faites chaque semaine (par exemple : mettre en forme un compte rendu de réunion, rédiger un brouillon de réponse à un client, mettre un tableau au propre).
2. Préparez un document réel pour chacune, sans informations personnelles.
3. Donnez la même consigne, à l'identique, aux deux outils.
4. Notez trois choses : l'exactitude, le nombre de points à corriger et le temps passé.
5. Si les scores sont proches, choisissez le moins cher ; si le travail ne tolère aucune erreur, choisissez celui qui a le meilleur score.

## Notre lecture

**Les faits :** les entreprises répartissent les usages dans leurs recommandations, et les scores viennent de leurs propres évaluations.

**Interprétation :** il n'y a pas de « meilleure IA », il y a « l'IA la moins chère qui convient à mon travail ». Les scores annoncés par les entreprises ne sont qu'un point de départ ; le critère, c'est le résultat vérifié avec nos propres documents.

**À notre place :** nous ne confierions pas tout à un seul outil : un petit modèle pour les tâches légères, un grand modèle seulement pour les tâches difficiles. Et nous referions le même test tous les trois mois, parce que les modèles évoluent vite.

## Textes lus en parallèle

Tout le contenu a été vérifié en ouvrant directement les documents officiels ci-dessous. Les scores et les usages sont les affirmations de chaque entreprise.

- [Choosing a model (Anthropic Docs)](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) — en anglais
- [Claude Sonnet 5.5 (Anthropic)](https://www.anthropic.com/claude-sonnet-5-5) — en anglais
- [Introducing GPT-6.1 Sol (OpenAI)](https://openai.com/index/introducing-gpt-6-1-sol/) — en anglais
- [Gemini models (Google AI for Developers)](https://ai.google.dev/gemini-api/docs/models) — en anglais
