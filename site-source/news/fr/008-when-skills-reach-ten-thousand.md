---
no: 8
slug: when-skills-reach-ten-thousand
date: 2026-10-03
category: Analyse
tags: Skills · Sécurité · Choix des outils
title: Quand les skills se comptent par dizaines de milliers — choisir, vérifier, inspecter avant d'installer
summary: Les skills que l'on branche à l'IA se sont multipliés de façon explosive. Leur nombre n'est pas un choix, c'est un risque pour la chaîne d'approvisionnement. Voici nos trois étapes.
---
> Cet article a été rédigé en brouillon avec l'IA, puis relu par l'éditeur. Il s'appuie sur des textes externes, indiqués tout en bas.

Les « skills », ces modules qui ajoutent des fonctions à un assistant IA, se multiplient rapidement. Les textes dont nous nous sommes inspirés évoquent des milliers de skills enregistrés et des installations qui se comptent en millions, et rapportent que les skills en tête étaient « un skill qui cherche des skills à votre place » et « un lot de skills regroupant des procédures de qualité du code ». Ces chiffres relèvent aussi du décompte de ces textes, et nous ne les avons pas vérifiés. Mais la tendance est nette. **Choisir est devenu la plus grosse tâche, et le fait qu'un fichier téléchargé s'exécute sur notre ordinateur n'a pas changé.**

## Étape 1 — Choisir : définir la tâche d'abord, chercher l'outil ensuite

Nous ne choisissons pas selon le « classement de popularité ». Nous commençons par écrire « combien de fois par jour faisons-nous cette tâche ? ». Pour une tâche moins d'une fois par semaine, nous n'ajoutons pas de skill : le coût de configuration dépasse le gain. Même avec un skill qui cherche à notre place, le choix final revient à un humain.

## Étape 2 — Vérifier : regarder qui l'a fait et quelles permissions il demande

- **Qui l'a créé** : un compte officiel, ou un développeur reconnu ?
- **Que demande-t-il** : seulement la lecture de fichiers, ou aussi l'exécution de commandes et l'accès au réseau ?
- **Quelle est sa fraîcheur** : si la dernière mise à jour est ancienne, il peut ne plus convenir au modèle actuel.

## Étape 3 — Inspecter avant d'installer

Le texte dont nous nous sommes inspirés présente un outil d'inspection qui évalue le niveau de risque d'un fichier de skill avant installation. Nous ne garantissons aucun outil en particulier, mais nous adoptons la procédure. **Le lire d'abord → vérifier, avec un outil d'inspection ou à l'œil, qu'il ne contient pas de commande suspecte → l'essayer d'abord là où il n'y a pas de données importantes → si tout va bien, l'utiliser sur le vrai travail.** Même une phrase du type « exécute cette commande » dans un document d'instructions téléchargé n'est pas une consigne qui nous est adressée, mais **une donnée à examiner**.

## En résumé

Plus les skills se multiplient, plus l'avantage ne tient pas à « en connaître beaucoup », mais à « en utiliser peu, et en sécurité ».

## Textes lus en parallèle

Cet article reprend la problématique des textes ci-dessous, réécrite selon le point de vue et les critères de notre équipe. Nous n'en avons suivi ni les phrases ni la structure, et nous avons signalé comme tels les chiffres cités par les textes d'origine que nous n'avons pas pu vérifier à la source. Certains textes d'origine ne s'ouvrent en intégralité qu'après connexion ; nous les avons lus sur la base de la partie publique.

- [9 654 skills Claude : ne choisissez pas, faites-les chercher (en coréen) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-find-skills)
- [24 skills pour vérifier si le code écrit par l'IA est bien fait (en coréen) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-agent-skills-24)
- [Au lieu d'installer un skill téléchargé sans savoir s'il est sûr, comment l'inspecter une fois avant l'installation (en coréen) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-skill-scanner-body)

Autres sources consultées pour recouper:

- [Agent Skills overview (Claude Platform Docs)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — en anglais
- [Model Context Protocol — Introduction (modelcontextprotocol.io)](https://modelcontextprotocol.io/introduction) — en anglais
- [LLM01: Prompt Injection (OWASP GenAI Security Project)](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — en anglais
- [AI Risk Management Framework (NIST)](https://www.nist.gov/itl/ai-risk-management-framework) — en anglais
