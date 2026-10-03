---
no: 7
slug: where-time-and-money-leak
date: 2026-10-03
category: Pratique
tags: Mémoire · Coûts · Efficacité au travail
title: Les trois endroits où fuient le temps et l'argent quand on travaille avec l'IA
summary: On répète chaque fois la même explication, on attend que ça finisse, et on paie pour des données que personne ne lit. Voici ces trois fuites et comment les colmater.
---
> Cet article a été rédigé en brouillon avec l'IA, puis relu par l'éditeur. Il s'appuie sur des textes externes, indiqués tout en bas.

Avec les outils d'IA, le temps et l'argent fuient généralement non parce qu'ils sont lents, mais **à cause de la façon de les utiliser**. Voici les trois endroits que nous contrôlons.

## 1. La répétition des mêmes explications

Si vous réécrivez la présentation du projet depuis le début à chaque nouvelle conversation, c'est la première fuite. La solution est simple : consigner l'objectif du projet, les interdits et le vocabulaire dans **un seul document d'instructions** toujours lu en premier. Ce document doit rester court. S'il s'allonge, comme nous l'avons dit dans un article précédent, il finit au contraire par s'estomper. Nous le faisons avec un classeur de documents de projet et un document d'instructions, et nous veillons à ne pas dépasser une page.

## 2. Le temps d'attente

Si vous lancez une tâche longue, comme une compilation, un déploiement ou une conversion en masse, et restez à regarder l'écran, c'est la deuxième fuite. Le principe de base est de **lancer les tâches longues en arrière-plan et de confier autre chose entre-temps**. Exécutées l'une après l'autre, les tâches prennent la somme de leurs durées ; en parallèle, seulement la durée de la plus longue. Pour les travaux dont le résultat est long, comme une recherche, mieux vaut les confier à un exécutant distinct et **ne lui demander que le résumé** : votre écran de travail reste net.

## 3. Le coût de données que personne ne lit

Le texte dont nous nous sommes inspirés souligne que, si l'on fournit à un agent de codage des fichiers de journaux ou de gros vidages en bloc, la plus grande partie n'est que répétitions et espaces inutiles pour le modèle, et ne fait que coûter de l'argent. Nous n'avons pas pu vérifier ce que l'outil présenté dans ce texte permet réellement d'économiser, donc nous ne promettons aucun effet. Le principe, lui, s'applique même sans outil : **un long texte craché par une machine, c'est d'abord à une personne de n'en extraire que la partie utile avant de le fournir.** Pour un journal d'erreurs, vingt lignes avant et après l'erreur suffisent souvent.

## Liste de contrôle

- Combien de fois avez-vous répété la même explication cette semaine ?
- Vous est-il arrivé de rester bloqué à attendre une tâche longue ?
- Avez-vous déjà fourni un long journal ou un tableau en entier ?

Si vous répondez « oui » à une seule de ces trois questions, commencez par corriger cette ligne.

## Textes lus en parallèle

Cet article reprend la problématique des textes ci-dessous, réécrite selon le point de vue et les critères de notre équipe. Nous n'en avons suivi ni les phrases ni la structure, et nous avons signalé comme tels les chiffres cités par les textes d'origine que nous n'avons pas pu vérifier à la source. Certains textes d'origine ne s'ouvrent en intégralité qu'après connexion ; nous les avons lus sur la base de la partie publique.

- [Trois façons d'éliminer les temps d'attente de Claude, un simple copier-coller (en coréen) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-wait)
- [Les tarifs des agents de codage : vous vous faites plumer les yeux ouverts (en coréen) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-headroom)

Autres sources consultées pour recouper:

- [Prompt caching (Claude Platform Docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) — en anglais
- [Effective context engineering for AI agents (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — en anglais
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma Research)](https://research.trychroma.com/context-rot) — en anglais
