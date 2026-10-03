---
no: 3
slug: ai-reads-the-label
date: 2026-10-03
category: Pratique
tags: Connecteur · MCP · Vérification des ingrédients · Safelist
title: Quand l'IA lit la liste d'ingrédients à votre place — comment nous l'avons empêchée de dire « sans danger »
summary: Connecter un outil externe à un assistant IA fait passer ses réponses de l'« impression » à la « preuve ». Voici la règle que nous avons fixée en créant le connecteur Safelist : ne dire que « non repéré ».
---
> Cet article a été rédigé en brouillon avec l'IA, puis relu par l'éditeur. Safelist n'est pas un outil de diagnostic.

## Le problème : la réponse plausible est la plus dangereuse

Si l'on demande à une IA « Ce biscuit contient du lait et du blé ? », elle répond en général de façon plausible. Mais lorsqu'elle répond de mémoire, elle ignore qu'un produit a changé : elle affirme la présence d'un ingrédient absent ou passe à côté d'un ingrédient présent. Quand il s'agit d'alimentation, les deux erreurs posent problème.

## La solution : la connecter à un outil externe

Les assistants IA actuels peuvent se brancher à des outils externes via des « connecteurs » (en termes techniques, un standard de connexion comme MCP). À chaque question, au lieu de fouiller sa mémoire, l'IA interroge directement des données publiques et transmet le résultat. Le connecteur Safelist consulte les ingrédients d'un aliment dans les données publiques du ministère coréen de la Sécurité des aliments et des médicaments (MFDS), et indique s'ils contiennent les composants que l'utilisateur évite.

## Les trois règles que nous avons fixées

1. **Ne jamais dire « sans danger ».** L'outil ne peut aller plus loin que « les éléments à éviter n'ont pas été repérés ». Une contamination en cours de fabrication ou une erreur d'étiquetage ne peuvent pas se savoir à partir des données.
2. **Vérifier d'abord les ingrédients à éviter.** Ceux-ci diffèrent d'un enfant à l'autre : nous fixons donc le critère avant toute recherche.
3. **Ne pas effacer l'avertissement.** La mention en fin de réponse, « Ce n'est pas un diagnostic · Selon une base de données publique · La décision finale revient au parent », est conservée même dans un résumé.

## Généralisation : un cadre valable pour toute tâche

Le même cadre fonctionne bien au-delà des listes d'ingrédients.

- Pour une question où un chiffre ou un fait compte, **la confier à un outil de consultation.**
- Ce que l'outil ne sait pas, **le lui faire dire.**
- Ne formuler de conclusion que **dans la limite de ce que disent les données.**

Ce qui rend l'IA digne de confiance, ce n'est pas un modèle plus gros, mais une conception qui lui fait dire qu'elle ne sait pas ce qu'elle ne sait pas.

## L'essayer soi-même

L'application Safelist et le connecteur IA sont présentés dans la page Safelist du site. [Découvrir AP Safe](/en/products/safe/)
