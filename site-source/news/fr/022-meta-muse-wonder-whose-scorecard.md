---
no: 22
slug: meta-muse-wonder-whose-scorecard
date: 2026-10-15
category: Analyse
tags: Meta · Muse Wonder · Évaluation des modèles · Évaluation indépendante · Paramètres d'entraînement
title: Muse Wonder, le premier modèle de pointe de Meta — qui a noté, et trois points à vérifier avant de l'utiliser
summary: Meta a lancé le 12 octobre son premier modèle de classe frontière. Nous plaçons les scores annoncés par l'entreprise à côté de ceux d'un évaluateur indépendant, puis passons en revue le prix, l'accès et les paramètres d'entraînement : trois points à vérifier avant de l'utiliser dans notre travail.
---
> Cet article a été rédigé avec l'IA (Claude) et relu par un éditeur. Anthropic, qui fabrique les modèles Claude cités ici en comparaison, fabrique aussi l'outil que nous avons utilisé pour écrire : nous avons donc un intérêt dans le sujet. Les chiffres annoncés par les entreprises sont signalés comme tels, et les évaluations indépendantes sont indiquées à part. Ceci n'est pas un avis d'investissement sur une entreprise ou une action.

Le lundi 12 octobre, les Superintelligence Labs de Meta ont publié deux modèles, Muse Wonder et Muse Wonder Full, que Meta présente comme ses premiers modèles de classe frontière. Ce qui compte dans cette actualité, ce n'est pas tant les scores eux-mêmes que la question de savoir qui les a mesurés, et dans quelles conditions.

## Ce qui est sorti (fait)

- Muse Wonder est disponible via l'API de modèles de Meta et Muse Code, son outil de programmation. Le prix de l'API est de 4 dollars par million de jetons en entrée et de 20 dollars par million de jetons en sortie (0,20 dollar pour l'entrée mise en cache, selon l'évaluateur indépendant Artificial Analysis).
- Muse Wonder Full est réservé aux abonnés de Muse Code. Il n'est pas proposé via l'API (TechCrunch). Selon la page des abonnements Muse Code de Meta, Full est inclus dans les deux formules supérieures sur quatre (Power et Maximum), et LetsDataScience et DataNorth rapportent que ces deux formules coûtent 50 et 200 dollars par mois.
- Les deux modèles ont une fenêtre de contexte d'un million de jetons, acceptent texte, image, vidéo et audio en entrée, et produisent du texte (Artificial Analysis).
- Nous n'avons pas pu confirmer si les poids des deux modèles sont téléchargeables (seul LetsDataScience affirme qu'ils ne le sont pas). Decrypt souligne que Meta a de fait mis fin à sa gamme Llama, dont les poids étaient publiés.

## Lire le tableau des scores

**Annoncé par l'entreprise.** Sur son propre « Personal Superintelligence Index », Meta affirme que Wonder Full obtient 59,1, devant Opus 5.5 (55,2) et GPT-6 Astra (54,5), et qu'il mène aussi sur le test de mémoire MemoryBench avec environ 85,5 (affirmations de Meta rapportées par Decrypt ; iThome et Latent Space donnent les mêmes chiffres). Decrypt note que ces deux mesures ont été créées par Meta et que la formule de l'indice n'est pas publiée.

**Évaluation indépendante.** Sur l'indice général d'Artificial Analysis (v4.3, effort maximal), Wonder Full obtient 56, Wonder 52, et le modèle précédent de Meta, Muse Spark 1.3, 48. Sur le même indice, Opus 5.5 obtient 58, Sonnet 5.5 56 et GPT-6 Astra 53 (vérifié directement sur le classement d'Artificial Analysis, chaque modèle à son réglage le plus élevé). Selon la mesure indépendante, le modèle se situe donc autour de la troisième place, ce qui ne correspond pas au « devant » de l'indice maison.

**En regardant de plus près.** Dans le même article, Artificial Analysis écrit que sur son indice d'agents de programmation, Wonder Full obtient 68, au niveau de Claude Code avec Sonnet 5.5 et au-dessus d'Opus 5.5 (66). En revanche, sur le test de connaissances AA-Omniscience, Full obtient 30 et Wonder 25, bien en dessous d'Opus 5.5 (46) et de GPT-6 Astra (43). Le taux d'invention (hallucination) est plutôt bas, 23 % pour Full et 27 % pour Wonder, mais parmi les modèles à 45 points ou plus sur l'indice, le plus bas est celui de Gemini 4 Argon, à 15 %.

## Trois points à vérifier avant l'utilisation (interprétation)

**1. Le coût par travail terminé.** À prix du jeton égal, le coût d'un travail peut différer. Le coût mesuré par Artificial Analysis pour un même ensemble de tâches est de 4,52 dollars pour Wonder, 5,98 pour Opus 5.5, 5,46 pour Sonnet 5.5, 3,26 pour GPT-6 Astra, 1,99 pour Gemini 4 Argon et 0,72 pour GPT-6.1 Sol. Il juge Wonder plus cher que la plupart des modèles d'intelligence comparable. Des articles disent que son prix égale celui d'Opus 5.5 (Decrypt), mais le chiffre que nous regardons est le coût par travail, pas le prix unitaire.

**2. Où on peut l'utiliser.** Le modèle le mieux noté, Wonder Full, ne fonctionne que dans un abonnement : on ne peut donc pas le brancher à nos automatisations par API. Ce qui est accessible par API, c'est Wonder, un cran plus bas en score.

**3. Où vont votre code et vos textes.** D'après la page des abonnements Muse Code de Meta, les abonnements sont par défaut en « mode Contributor » : Meta peut utiliser vos requêtes, votre code, vos fichiers, votre contexte et les réponses reçues pour entraîner ses futurs modèles, en échange de davantage d'usage. La page indique qu'une fois le mode désactivé, votre contenu futur n'est pas utilisé pour l'entraînement, mais elle ne dit pas ce qu'il advient du contenu déjà envoyé : nous n'avons donc pas pu le confirmer. Ce mode n'existe pas pour Wonder via l'API, et le contenu en mode standard ne serait pas utilisé pour l'entraînement. Nous n'avons pas pu ouvrir nous-mêmes les conditions d'utilisation de Meta : vérifiez les conditions et l'écran des paramètres avant utilisation.

## Ce que nous n'avons pas pu confirmer

Nous n'avons pas pu ouvrir directement l'annonce officielle ni la fiche du modèle de Meta. Les éléments « annoncés par l'entreprise » ci-dessus ont été confirmés par les articles de TechCrunch, Decrypt, iThome et d'autres. Les abonnements et les paramètres d'entraînement ont été vérifiés en ouvrant directement la page des abonnements Muse Code de Meta. Decrypt indique que le rapport de sécurité complet promis par Meta n'est pas encore publié. Simon Willison, utilisateur au quotidien, écrit que Wonder propose six niveaux de raisonnement (de minimal à max) et que ses dessins semblent meilleurs que ceux du modèle précédent, mais il précise lui-même qu'il s'agit d'un test informel fondé sur un seul type de dessin. Il ne faut pas le lire comme un score.

## Notre analyse

**Fait :** Meta a sorti un modèle de pointe accessible uniquement par son API et ses abonnements ; les indicateurs de l'entreprise et les indicateurs indépendants donnent des images différentes ; le modèle le plus haut est réservé aux abonnés ; et le réglage par défaut de l'abonnement utilise votre contenu pour l'entraînement.

**Interprétation :** À chaque nouveau modèle, « il est premier » et « il est troisième » apparaissent en même temps. Les deux peuvent être vrais, car les tests diffèrent par leur auteur et par les réglages utilisés.

**Ce que nous ferions :** Nous ne changeons pas de modèle pour un chiffre. Nous faisons tourner 20 de nos propres tâches (brouillons de scripts, descriptions de produits, tri de commentaires) dans les mêmes conditions, nous notons le « coût par travail » et le « nombre de corrections », et nous ne publions qu'après vérification par une personne. Les informations clients et les documents non publiés ne vont dans aucun réglage pouvant servir à l'entraînement.

## Lectures associées

Nous avons ouvert directement des sources de natures différentes. Les chiffres sont ceux de chaque source.

- [Meta releases its first frontier model, Muse Wonder (TechCrunch)](https://techcrunch.com/2026/10/12/meta-releases-its-first-frontier-model-muse-wonder) — anglais, article de presse
- [Muse Wonder / Wonder Full evaluation (Artificial Analysis)](https://artificialanalysis.ai/articles/muse-wonder) — anglais, évaluateur indépendant
- [Meta Muse Wonder and the frontier AI race (Decrypt)](https://decrypt.co/380768/meta-muse-wonder-zuckerberg-frontier-ai-race) — anglais, article de presse (indicateurs de l'entreprise et indépendants)
- [Meta's best model skips API, coding plan trains on your code (LetsDataScience)](https://letsdatascience.com/blog/metas-best-model-skips-api-coding-plan-trains-on-your-code) — anglais, abonnements et paramètres d'entraînement
- [llm-meta-ai 0.2 (Simon Willison)](https://simonwillison.net/2026/Oct/12/llm-meta-ai/) — anglais, blog d'un utilisateur
- [Meta releases Muse Wonder, its first frontier-class AI model (AI Weekly)](https://aiweekly.co/alerts/meta-releases-muse-wonder-its-first-frontier-class-ai-model) — anglais, lettre d'information (résumé d'autres médias)
- [Muse Code Subscriptions (Meta)](https://dev.meta.ai/docs/muse-code/subscriptions) — anglais, page officielle de Meta
- [Models Leaderboard (Artificial Analysis)](https://artificialanalysis.ai/leaderboards/models) — anglais, classement de l'évaluateur indépendant
- [Meta's Muse Wonder (DataNorth)](https://datanorth.ai/news/metas-muse-wonder) — anglais, analyse (formules et paramètres d'entraînement)
- [Article sur Muse Wonder (iThome)](https://www.ithome.com.tw/news/179608) — chinois traditionnel, article de presse
