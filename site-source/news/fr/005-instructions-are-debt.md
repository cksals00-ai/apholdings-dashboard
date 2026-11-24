---
no: 5
slug: instructions-are-debt
date: 2026-10-03
category: Analyse
tags: Consignes · Prompts · Nettoyage
title: Les consignes données à l'IA sont une dette, pas un actif — pourquoi nous les effaçons chaque trimestre pour voir
summary: Croire que l'IA devient plus intelligente à mesure que l'on empile des règles est peut-être une erreur. Voici comment réduire les consignes et mesurer que cela ne pose pas de problème.
---
> Cet article a été rédigé en brouillon avec l'IA, puis relu par l'éditeur. Il s'appuie sur des textes externes, indiqués tout en bas.

Quand nous confions du travail à l'IA, chaque erreur nous pousse à ajouter une règle : « pas de tableaux », « vouvoiement », « cite tes sources ». Quelques mois plus tard, le document de consignes compte vingt, trente lignes, et nous l'appelons un actif. Pourtant, nous avons rarement vérifié que ces règles servent vraiment à quelque chose.

## Les règles s'ajoutent facilement, leur effet se vérifie difficilement

L'article dont nous nous sommes inspirés avance ceci : quand un modèle s'améliore, des règles autrefois nécessaires ne le sont plus, et une règle devenue inutile n'est pas inoffensive, car **elle alourdit la masse de ce qu'il faut respecter et finit par brouiller même les règles importantes**. Il s'appuie sur une étude de benchmark selon laquelle le taux de respect baisse à mesure que le nombre d'instructions augmente. Nous n'avons toutefois pas pu vérifier ce chiffre jusqu'à la source : retenons seulement qu'« une telle étude existe ». En pratique, la direction compte davantage. **Plus il y a de règles, plus l'IA peut en omettre discrètement une partie, et nous ne savons pas ce qui manque.**

## Nos critères de nettoyage

1. **Une fois par trimestre, nous vidons entièrement les consignes.** Nous relançons la même tâche sans consignes et regardons le résultat.
2. **Nous les réintroduisons ligne par ligne en observant la différence.** Si le résultat ne change pas avec une ligne, nous la supprimons.
3. **Nous nous méfions des règles sans « pourquoi ».** Une règle dont on ne sait pas expliquer la raison est souvent la trace d'un incident unique.
4. **Nous posons des critères plutôt que des interdits.** Une seule ligne « le lecteur de ce texte est telle personne » change plus de choses que dix lignes de « ne fais pas ».
5. **Nous ne supprimons pas les règles sur les actions irréversibles.** Celles sur la suppression, le paiement, l'envoi et la publication restent, quelles que soient les performances.

## En résumé

Les consignes ne sont pas un patrimoine à entasser, mais un équipement qui coûte de l'entretien. Mieux vaut essayer de les réduire et, si cela ne change rien, en rester là : c'est plus léger et plus sûr.

## Textes lus en parallèle

Cet article reprend la problématique des textes ci-dessous, réécrite selon le point de vue et les critères de notre équipe. Nous n'en avons suivi ni les phrases ni la structure, et nous avons signalé comme tels les chiffres cités par les textes d'origine que nous n'avons pas pu vérifier à la source. Certains textes d'origine ne s'ouvrent en intégralité qu'après connexion ; nous les avons lus sur la base de la partie publique.

- [L'IA n'est pas devenue bête — ce sont les consignes écrites il y a six mois qui la freinent (en coréen) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-claude-md-rules)

Autres sources consultées pour recouper:

- [How Many Instructions Can LLMs Follow at Once? (IFScale, arXiv)](https://arxiv.org/abs/2507.11538) — en anglais
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma Research)](https://research.trychroma.com/context-rot) — en anglais
- [Effective context engineering for AI agents (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — en anglais
- [Lost in the Middle: How Language Models Use Long Contexts (arXiv)](https://arxiv.org/abs/2307.03172) — en anglais
