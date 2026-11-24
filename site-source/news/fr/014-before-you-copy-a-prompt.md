---
no: 14
slug: before-you-copy-a-prompt
date: 2026-10-03
category: Pratique
tags: Prompts · Champs à remplir · Vérification des sources
title: Avant d'utiliser un prompt reçu — vérifier la source et remplir six lignes
summary: Pourquoi un prompt posté par quelqu'un d'autre ne marche-t-il pas quand on le colle tel quel ? Comment choisir des sources officielles, et six lignes préalables valables pour tout prompt.
---
> Cet article a été rédigé en brouillon avec l'IA, puis relu par l'éditeur. Il s'appuie sur des textes externes, indiqués tout en bas.

Il est courant de récupérer un prompt dans un commentaire sur les réseaux sociaux. Le faire est une bonne habitude, mais il y a **de nombreux cas où il ne suffit pas de le coller tel quel**. Voici nos critères.

## Regarder d'abord la source

Autant que possible, nous consultons d'abord les ressources officielles de l'entreprise qui a créé l'outil. Le texte dont nous nous sommes inspirés explique avoir ouvert la bibliothèque officielle de prompts publiée par Anthropic et l'avoir classée en trois groupes : ce qui marche directement dans la fenêtre de chat, ce qui exige de coller des documents, et ce qui demande des outils de développement. Cette idée de classement est utile. Il faut d'abord déterminer **si le prompt fonctionne dans mon environnement** pour gagner du temps.

## Les présupposés qui disparaissent en route

En traduisant un prompt étranger en coréen, il arrive que le présupposé « cet outil me connaît déjà » disparaisse. L'IA d'une nouvelle fenêtre de conversation ne me connaît pas. Elle pose alors des questions ou déroule des généralités banales. Le texte dont nous nous sommes inspirés explique avoir découvert ce problème en le faisant tourner lui-même. Nous pouvons rencontrer le même problème : **avant d'écrire le prompt, nous renseignons d'abord ce que l'IA ignore.**

## Six lignes préalables valables pour tout prompt

Pour un prompt qui traite d'une idée d'entreprise, remplissez d'abord les six lignes suivantes.

1. Ce que j'ai déjà fait contre rémunération (une tâche, pas un titre)
2. Ce que les gens me demandent souvent
3. Le temps disponible par semaine
4. L'argent disponible dès maintenant
5. Les personnes que je peux déjà joindre
6. Le montant visé et l'échéance

## Exiger explicitement « n'en garde qu'un »

Si l'on pose une question large à l'IA, elle énumère largement. L'énumération est sûre, alors que choisir engage une responsabilité. C'est pourquoi nous exigeons, à la fin de chaque étape, **« n'en garde qu'un, avec la raison en une phrase »**. Il faut que les candidats passent de cinq à un pour accéder à l'étape suivante.

## Dernière vérification

N'insérez pas d'informations personnelles dans un prompt reçu, et vérifiez séparément la source des chiffres et des faits du résultat.

## Textes lus en parallèle

Cet article reprend la problématique des textes ci-dessous, réécrite selon le point de vue et les critères de notre équipe. Nous n'en avons suivi ni les phrases ni la structure, et nous avons signalé comme tels les chiffres cités par les textes d'origine que nous n'avons pas pu vérifier à la source. Certains textes d'origine ne s'ouvrent en intégralité qu'après connexion ; nous les avons lus sur la base de la partie publique.

- [Les 52 prompts officiels de l'entreprise qui a créé Claude, tous ouverts et classés (en coréen) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-prompt-library)
- [Dites « fais-moi gagner de l'argent » et Claude vous repose des questions (en coréen) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-money-chain)

Autres sources consultées pour recouper:

- [LLM01: Prompt Injection (OWASP GenAI Security Project)](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — en anglais
- [Prompt injection (Wikipedia)](https://en.wikipedia.org/wiki/Prompt_injection) — en anglais
- [Prompt engineering overview (Anthropic Docs)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — en anglais
