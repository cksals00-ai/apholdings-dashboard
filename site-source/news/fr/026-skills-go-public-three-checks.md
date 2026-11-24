---
no: 26
slug: skills-go-public-three-checks
date: 2026-10-23
category: Analyse
tags: Agent Skills · Anthropic · Linux Foundation · AAIF · version d'API · Railway · clés d'API
title: Les skills sont devenus une « norme commune » — le don d'Agent Skills à une fondation, la première nouvelle version d'API en trois ans et des clés volées : les trois choses que nous avons vérifiées
summary: Le 22 octobre, Anthropic a remis la norme Agent Skills à l'AAIF, sous l'égide de la Linux Foundation ; la veille, l'API Claude recevait sa première nouvelle version depuis 2023 ; et le même jour, l'hébergeur Railway annonçait que des variables d'environnement contenant les clés d'API de ses clients avaient pu fuiter. Nous avons lu ces trois nouvelles différentes du point de vue d'« un seul dossier de skill » et noté l'ordre dans lequel nous avons vérifié le nôtre.
---
> Cet article a été rédigé avec une IA (Claude) et relu par un éditeur. Anthropic, au centre de cet article, est l'entreprise qui fabrique le Claude que nous avons utilisé pour l'écrire, et notre propre entreprise conçoit et utilise plusieurs skills internes : nous avons donc un intérêt à déclarer. C'est pourquoi les chiffres annoncés par les entreprises sont signalés comme « annoncés par l'entreprise », et au lieu de juger si c'est bien ou mal, nous ne consignons que l'ordre dans lequel nous avons réellement vérifié notre propre travail. Ceci n'est pas un avis d'investissement sur une entreprise.

Cette semaine, trois nouvelles concernant les « pièces » des agents d'IA sont tombées en trois jours. L'une porte sur un format (le format des skills a quitté les mains d'une entreprise pour une fondation), l'autre sur une version (l'API Claude a reçu une nouvelle version après trois ans), la troisième sur des clés (des clés d'API confiées à un hébergeur ont pu fuiter). Lues séparément, ce sont des nouvelles différentes. Vues depuis la position de quelqu'un qui fait tourner un dossier de skill, elles convergent vers la même question : qu'y a-t-il dans mon dossier, et de quoi dépend-il ? Lisez cet article comme la suite du NO.8 (quand les skills atteignent dix mille) et du NO.20 (l'ordre des vérifications avant d'installer).

## 1. Le format — le format des skills est passé à une fondation (faits)

Le 22 octobre, Anthropic a annoncé le don de la norme Agent Skills à l'Agentic AI Foundation (AAIF), sous l'égide de la Linux Foundation. Selon l'annonce, le don couvre la norme elle-même, le nom et le logo « Agent Skills », l'organisation GitHub et le domaine agentskills.io. L'AAIF est une fondation créée par Anthropic avec Block et OpenAI, et Anthropic lui avait déjà remis MCP (Model Context Protocol).

Le communiqué de presse de la Linux Foundation indique que quatre projets ont été accueillis le même jour : Agent Skills d'Anthropic, Open Responses d'OpenAI (une spécification d'appel de modèles commune à plusieurs fournisseurs), OpenEnv de Hugging Face (partage d'environnements d'apprentissage par renforcement) et OpenSandbox d'Alibaba (bacs à sable pour agents). Le nombre de projets gérés par la fondation est passé de 3 à son lancement en décembre 2025 à 10.

Le site de la spécification (agentskills.io) définit un skill en quelques lignes. **Un skill est un dossier contenant un fichier SKILL.md.** Ce fichier contient un nom et une description (les champs minimaux) ainsi que des instructions ; des scripts, des documents de référence et des modèles peuvent se trouver dans le même dossier si nécessaire. Au démarrage, l'agent ne lit que le nom et la description ; quand une tâche correspondante arrive, il lit l'intégralité des instructions ; pendant l'exécution, il ouvre les scripts ou les fichiers de référence. La spécification appelle ces trois étapes la « divulgation progressive » (progressive disclosure).

Les chiffres d'échelle sont ceux annoncés par Anthropic : plus de 70 produits d'agents ont adopté le format (ChatGPT, Cursor, GitHub Copilot et VS Code sont cités en exemple), environ 1 million de skills ont été publiés et il y aurait eu environ 280 millions d'installations. Le média allemand MIXED a ajouté qu'il s'agit des comptages de l'entreprise, et non de nombres d'utilisateurs vérifiés de manière indépendante. Nous adoptons la même position.

La gouvernance figure aussi dans l'annonce. Des ingénieurs d'Anthropic, de Google, d'OpenAI et d'autres entreprises maintiendront la norme à titre individuel, et non comme représentants de leur société ; les mainteneurs principaux sont David Soria Parra et Mahesh Murag. On peut l'utiliser et y contribuer sans être membre de la fondation. L'annonce liste aussi trois points « à venir » : des publications versionnées, une procédure officielle pour proposer des modifications de la spécification, et **des recommandations de sécurité pour ceux qui écrivent et installent des skills**. Comme l'a relevé MIXED, ces trois points sont encore des propositions, pas des réalisations.

## 2. La version — l'API Claude reçoit sa première nouvelle version en trois ans (faits)

La veille, le 21 octobre, une nouvelle version de l'API Claude, « 2026-10-21 », est sortie. La liste des versions dans la documentation d'Anthropic ne comporte que trois entrées — 2023-01-01, 2023-06-01 et maintenant 2026-10-21 — soit la première nouvelle version en trois ans et quatre mois. Le compte destiné aux développeurs (@ClaudeDevs) a indiqué que les nouveaux SDK et la CLI utilisent cette version par défaut (nous n'avons pas pu ouvrir directement la publication sur X ; nous l'avons confirmée par le résumé de l'agrégateur coréen promppy et par la documentation officielle d'Anthropic).

Parmi les changements listés dans le guide de migration, voici ceux qu'une petite équipe risque de rencontrer tout de suite :

- **Les trois paramètres temperature, top_p et top_k disparaissent.** Les envoyer, même avec leurs valeurs par défaut, renvoie une erreur 400. Le guide précise que « le code qui s'appuyait sur une temperature basse pour obtenir des réponses cohérentes perd cet effet, et aucun autre réglage ne le remplace ».
- **L'en-tête d'authentification change.** Le nouveau SDK envoie la clé sous la forme Authorization: Bearer au lieu de X-Api-Key. Un proxy ou une passerelle intermédiaire qui lit l'ancien en-tête doit être mis à jour.
- Placer un bloc document directement dans un message assistant, ou des citations dans un bloc text d'un message user, renvoie une erreur 400.
- Plusieurs noms de champs de réponse de l'API d'administration changent (roles → role_ids, name → display_name, etc.).
- Le SDK Python utilise la nouvelle version à partir de 2.0.0. La licence du SDK et de la CLI passe à Apache 2.0.

Le point important est que **l'ancienne version n'est pas coupée immédiatement**. Le guide indique que les SDK existants continuent d'envoyer l'en-tête 2023-06-01, de sorte que l'on peut rester sur sa version actuelle, et aucune date de fin pour 2023-06-01 n'est écrite nulle part. « Pas de date de fin » et « maintenue pour toujours » sont deux affirmations différentes ; nous ne consignons que la première comme confirmée.

## 3. Les clés — des clés d'API confiées à un hébergeur ont pu fuiter (faits)

Le même 21 octobre, l'hébergeur d'applications Railway a publié un avis de sécurité sur son blog officiel. En substance : ce matin-là, il a détecté une activité anormale dans les systèmes qui stockent les variables d'environnement de ses clients, et l'enquête indique qu'**un tiers non autorisé a pu accéder à des variables d'environnement chiffrées et, pour certaines, en obtenir le contenu déchiffré**. Les variables d'environnement contiennent en général des clés d'API et des identifiants de bases de données et de registres. Railway écrit qu'il considère cet incident comme « faisant partie d'une série d'attaques visant récemment des entreprises de plateforme », dans le but de compromettre des fournisseurs d'inférence d'IA.

L'entreprise a pris trois mesures : prévenir les fournisseurs en amont pour qu'ils révoquent les clés de manière préventive, suspendre tous les déploiements, et prévenir par e-mail les comptes concernés au fur et à mesure de leur confirmation. Aux utilisateurs, malgré une analyse initiale suggérant que l'impact pourrait se limiter à une partie d'entre eux, Railway recommande fortement de **remplacer immédiatement toutes les variables d'environnement (y compris les clés d'API et les identifiants de registres privés) et d'examiner les journaux de ces services à la recherche d'une utilisation inhabituelle**. L'avis ne contient aucun chiffre, ni nombre de comptes touchés ni nombre de variables exposées.

Autour de cet incident circulent, sur les réseaux sociaux et dans certains médias, des affirmations selon lesquelles « les clés volées deviennent immédiatement de l'argent sur le marché noir », « il existe une demande pour produire des données d'entraînement destinées à la distillation » ou « des centaines de milliers de dollars ont été siphonnés de portefeuilles de cryptomonnaies ». Nous n'avons pu confirmer aucune de ces affirmations à partir de documents de Railway ou d'autorités d'enquête ; dans cet article, nous n'allons donc pas au-delà de « de telles affirmations existent ».

## Là où les trois nouvelles se rejoignent dans un même dossier (interprétation)

Un dossier de skill est léger : un SKILL.md et quelques scripts. Mais ce dossier léger repose sur trois choses.

Premièrement, **le format**. La structure du dossier et les champs nom et description doivent suivre la spécification pour être lisibles par d'autres produits d'agents. Tant que la spécification vivait dans une entreprise, la règle était « quand ils changent, on suit ». Maintenant qu'elle est dans une fondation, cela devient « on surveille les versions et la procédure de proposition, et on suit ». Jusqu'à ce que les publications versionnées et les recommandations de sécurité promises par la fondation existent réellement, cela ne change en pratique pas grand-chose par rapport à aujourd'hui.

Deuxièmement, **la version de l'API que les scripts appellent**. Si un script à l'intérieur d'un skill transmet temperature, ou passe par un proxy qui lit l'en-tête X-Api-Key, ce skill casse silencieusement au moment où l'on met à jour le SDK. Un skill n'est pas quelque chose qui s'arrête à « ça marchait à l'installation » ; c'est quelque chose qu'il faut refaire tourner chaque fois que la version de l'API en dessous change.

Troisièmement, **où se trouvent les clés que les scripts utilisent**. Même si vous n'avez jamais écrit de clé dans le skill lui-même, si la clé se trouve dans les variables d'environnement du serveur qui exécute le skill, et que ce serveur est chez un hébergeur, alors des clés peuvent fuiter depuis un endroit sans rapport avec votre dossier — comme dans cet incident Railway. Nous pensons que c'est aussi pour cela que la fondation a placé « des recommandations de sécurité pour ceux qui écrivent et installent des skills » parmi ses premières tâches (ce lien est notre interprétation, pas une raison énoncée par la fondation).

## Si c'était nous — les trois choses que nous avons vérifiées dans nos dossiers de skills (pratique)

Notre entreprise conçoit des skills internes (politique des écrans d'application, procédures d'analyse de données, vérification d'articles, etc.) au format SKILL.md. Voici l'ordre dans lequel nous les avons réellement vérifiés après les nouvelles de cette semaine.

1. **Vérification du format.** Nous avons confirmé que le SKILL.md de chaque skill possède un name et une description, et que la description dit en une ligne « quand sortir ce skill ». Ce sont les deux champs minimaux exigés par la spécification, et les deux seuls que l'agent lit au démarrage. Quand la fondation publiera une version numérotée, nous avons décidé d'inscrire ce numéro dans le document de référence de chaque dossier de skill.
2. **Vérification de la version.** Nous avons cherché les chaînes temperature, top_p, top_k et X-Api-Key dans les scripts des dossiers de skills. Si l'une d'elles apparaît, le skill va sur la liste « à corriger avant de mettre à jour le SDK ». Nous ne mettons pas le SDK à jour tout de suite ; nous le ferons quand la liste à corriger sera vide. Si une date de fin pour l'ancienne version est annoncée, nous avancerons le calendrier.
3. **Vérification des clés.** Nous avons cherché à nouveau pour nous assurer qu'aucune clé n'est écrite nulle part dans les dossiers de skills ni dans le dépôt, et nous avons dressé la liste des endroits où se trouvent les clés (variables d'environnement d'un hébergeur, gestionnaire de secrets). Les clés confiées à un prestataire extérieur sont classées « clés qui fuient avec lui s'il est compromis », et nous avons vérifié que des alertes d'utilisation et des plafonds de dépense sont en place. Nous avons jugé que « examiner les journaux à la recherche d'une utilisation inhabituelle », recommandé par Railway, n'est utile que si cela arrive sous forme d'alerte en temps normal, et non après un incident.

Ces trois vérifications valent la peine d'être faites une fois par trimestre, même sans nouvelle. Dans le NO.5, nous avons écrit que « les instructions sont une dette, pas un actif » ; il en va de même des dossiers de skills. Plus les dossiers se multiplient, plus il y a à vérifier sur les trois axes du format, de la version et des clés.

## Ce que nous n'avons pas pu confirmer dans cette nouvelle

- Les plus de 70 plateformes, environ 1 million de skills et environ 280 millions d'installations annoncés par Anthropic sont des comptages de l'entreprise ; nous n'avons trouvé aucune vérification indépendante.
- Nous n'avons pas pu ouvrir la publication originale de @ClaudeDevs sur X ; la nouvelle version de l'API a été confirmée par la documentation officielle d'Anthropic (liste des versions et guide de migration). Nous n'avons pas pu confirmer dans la documentation les numéros exacts de nouvelle version majeure des SDK dans d'autres langages que Python.
- La documentation ne donne pas de date de fin pour la version 2023-06-01. Nous avons seulement confirmé qu'il n'y en a pas.
- L'ampleur de l'incident Railway (nombre de comptes et de variables), l'auteur de l'attaque et le lien avec d'autres compromissions de plateformes ne figurent pas dans l'avis de Railway, et nous n'avons pas pu confirmer les chiffres des médias et des réseaux sociaux (pertes de portefeuilles, etc.).
- Pour l'article du 20 octobre du site de référence Learn:US (comment installer en sécurité des skills créés par d'autres), nous n'avons lu que le résumé public de la liste et n'avons pas pu ouvrir le corps du texte.

## Lu en parallèle

Nous avons ouvert directement des sources de natures différentes. Annonces d'entreprises et de fondation, documentation officielle, médias et blogs personnels sont listés séparément.

Annonces d'entreprises et de fondation :

- [Donating Agent Skills to the Agentic AI Foundation (Anthropic)](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) — anglais, annonce d'entreprise (chiffres comptés par l'entreprise)
- [Agentic AI Foundation Announces Four New Projects: Agent Skills, Open Responses, OpenEnv, and OpenSandbox (Linux Foundation)](https://www.linuxfoundation.org/press/agentic-ai-foundation-announces-four-new-projects-agent-skills-open-responses-openenv-and-opensandbox) — anglais, communiqué de presse de la fondation
- [Security Disclosure: Wednesday October 21st (Railway)](https://blog.railway.com/p/security-disclosure-wednesday-october-21st) — anglais, avis d'entreprise

Documentation officielle et spécification :

- [Agent Skills Overview (agentskills.io)](https://agentskills.io/) — anglais, site de la spécification
- [Versions (Claude Platform Docs)](https://platform.claude.com/docs/en/api/versioning) — anglais, documentation officielle
- [Migrating to API version 2026-10-21 (Claude Platform Docs)](https://platform.claude.com/docs/en/api/migration-2026-10-21) — anglais, documentation officielle

Presse et résumés :

- [Anthropic hands its widely used AI skills standard to an independent foundation (MIXED)](https://mixed-news.com/en/anthropic-agent-skills-agentic-ai-foundation/) — anglais, média (souligne les limites des chiffres de l'entreprise)
- [Anthropic publie la nouvelle version 2026-10-21 de l'API Claude (promppy)](https://www.promppy.com/item/2535081) — coréen, agrégateur de résumés par IA (source d'origine : publication sur X)
- [Incident Railway, vol de clés d'API d'IA (promppy)](https://www.promppy.com/item/2535863) — coréen, agrégateur de résumés par IA (source d'origine : publication sur X, contient des affirmations non confirmées)

Blogs personnels et sites de praticiens :

- [Donating Agent Skills to the Agentic AI Foundation (Simon Willison)](https://simonwillison.net/2026/Oct/22/donating-agent-skills/) — anglais, blog personnel (retour sur une prédiction de décembre 2025)
- [Trois skills à mettre dans Claude avant de commencer la journée (Learn:US)](https://learn.bizni.us/) — coréen, site de praticiens (résumé public seulement)
