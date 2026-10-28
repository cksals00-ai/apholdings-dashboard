---
no: 31
slug: genie-4-world-models-what-we-can-use
date: 2026-10-28
category: Analyse
tags: Modèles de monde · Genie 4 · Google DeepMind · Production vidéo · Influenceurs IA
title: Google a construit un « monde qui a du son » — ce que Genie 4 montre de l'état des modèles de monde, comment lire une annonce sans chiffres, et ce qu'une petite équipe vidéo doit faire maintenant
summary: Le 27 octobre, Google DeepMind a dévoilé son modèle de monde Genie 4. On se déplace en temps réel dans un monde créé à partir d'une ligne de texte, on change la météo, la caméra et les personnages à la voix, et pour la première fois le modèle génère la musique, les sons d'ambiance et les dialogues en même temps que l'image. Mais le billet officiel ne contient pas un seul chiffre — ni résolution, ni durée, ni latence — et seuls des « testeurs de confiance » peuvent l'utiliser pour l'instant. Nous avons mis côte à côte les chiffres publiés pour son prédécesseur Genie 3, le modèle du concurrent Runway et le rachat de World Labs par AMD pour mesurer où en sont les modèles de monde. Puis nous avons noté ce qu'une équipe comme la nôtre, qui produit des vidéos d'influenceuse IA, doit faire tout de suite avec cette nouvelle — et ce qu'elle ne doit pas faire.
---
> Cet article a été rédigé avec l'aide d'une IA (Claude) et vérifié par un éditeur. Anthropic, qui développe Claude, est en concurrence avec Google, sujet de cet article, et notre entreprise est cliente payante de Claude comme des outils d'IA de Google. Les performances et fonctions annoncées par une entreprise sont signalées comme « ce que l'entreprise a annoncé », et pour tout chiffre absent du billet officiel nous indiquons quel média l'a rapporté. Cet article n'est pas une recommandation d'achat ou de vente d'actions.

L'expression « modèle de monde » s'est répandue à partir du titre d'un article de 2018 de David Ha et Jürgen Schmidhuber. L'idée : un agent apprend un modèle compressé de la façon dont son environnement change dans l'espace et le temps, s'entraîne d'abord dans ce « rêve », puis transfère ce qu'il a appris dans l'environnement réel. Huit ans plus tard, le 27 octobre, Google DeepMind a annoncé avoir poussé cette idée jusqu'à « se déplacer en temps réel dans un monde construit à partir d'une ligne de texte, corriger le monde en lui parlant, et l'entendre ». L'annonce est éblouissante, mais sans chiffres. Cet article comble ce vide avec les chiffres publiés du prédécesseur et des concurrents.

## 1. Genie 4 — ce que l'entreprise a annoncé (faits)

Google DeepMind a publié Genie 4 sur son blog le 27 octobre (auteurs Raia Hadsell, Diego Rivas et Hang Qi). Les caractéristiques décrites par l'entreprise sont les suivantes.

- **Il produit le son en même temps que le monde.** L'entreprise écrit que Genie 4 est « notre premier modèle de monde en temps réel à générer l'audio nativement ». Chaque monde a son ambiance sonore et sa musique, et les personnages tiennent des dialogues qui s'adaptent aux entrées et aux événements.
- **On le corrige à la voix pendant qu'il tourne.** Pendant que la simulation s'exécute, on peut changer la scène en langage naturel — « fais pleuvoir », « recule la caméra », « ajoute une personne » — et Gemini adapte chaque instruction à la scène environnante tout en faisant avancer le monde.
- **Physique et mouvement humain.** Il imite des phénomènes physiques comme l'aérodynamique et les collisions, et l'entreprise affirme que les personnages réagissent à leur environnement et bougent naturellement.
- **Gemini joue le « réalisateur ».** Gemini 3.8 Flash observe la scène, découpe l'objectif en étapes, vérifie sur les images reçues que chaque étape est accomplie, et révise le plan quand le monde change ou qu'un utilisateur intervient. Dans une expérience de robotique, Gemini 4 Argon découpe une tâche en étapes qu'il envoie à Genie comme des sous-titres ; l'exemple montre l'humanoïde Apollo d'Apptronik jouant aux dames.
- **Qui peut l'utiliser.** Pour l'instant, c'est un aperçu de recherche réservé aux « testeurs de confiance ». L'entreprise annonce un déploiement progressif aux abonnés Google AI Ultra via Project Genie et aux partenaires en accès anticipé de l'API Gemini et d'AI Studio ; aucune date de sortie générale. La liste d'attente de Project Genie est ouverte.
- **Elle a écrit elle-même ses limites.** L'entreprise indique que « les détails visuels et la permanence des objets peuvent encore dériver avec le temps », surtout dans les sessions longues, après plusieurs modifications ou en se déplaçant dans la scène, et classe les interactions physiques complexes, la précision de l'audio en temps réel, le texte lisible, la précision spatiale et la cohérence à long terme comme « en cours de recherche ». Sa propre formule : « un modèle expérimental précoce ». Toute vidéo et tout audio générés portent un filigrane SynthID.

Le billet liste aussi les domaines explorés par les testeurs. Des cinéastes l'utilisent comme « mode brouillon » pour enchaîner plusieurs prises en changeant caméra, lumière, dialogues et action ; des photojournalistes transforment une photo d'archive 2D en environnement où l'on se déplace ; des développeurs de jeux testent rapidement styles visuels et règles par la parole ; des partenaires en entreprise génèrent vite des scénarios.

**Ce qui manque au billet officiel.** Ni la résolution, ni le nombre d'images par seconde, ni la durée tenue par session, ni la latence, ni aucune mesure de cohérence ne figurent dans le billet de DeepMind ou sur le blog officiel de Google. TechCrunch, sur la base d'un briefing, rapporte qu'il « maintient une scène cohérente jusqu'à deux minutes, le double de Genie 3 », et le média coréen DigitalToday cite TechCrunch pour le même chiffre. Autrement dit, « deux minutes » vient d'une seule filière de presse et d'aucun document officiel. Ce que TechCrunch rapporte de l'ingénieur de DeepMind Rivas est plus franc que n'importe quel chiffre : l'étape où l'interaction en temps réel a le plus de valeur est « l'idéation et le storyboard », et « l'expérience produit de bout en bout n'est pas encore claire ».

## 2. Les chiffres sont chez le prédécesseur et les concurrents (faits)

Quand un billet officiel n'a pas de chiffres, nous plaçons à côté l'annonce précédente de la même entreprise et les chiffres publiés des concurrents.

- **Genie 3 (Google DeepMind, 5 août 2025).** Le billet officiel avait des chiffres : résolution 720p, 24 images par seconde, navigation en temps réel, « des environnements largement cohérents pendant plusieurs minutes » et « une mémoire visuelle remontant jusqu'à une minute ». C'était un aperçu de recherche limité, ouvert à un petit groupe d'universitaires et de créateurs. Les limites listées alors : l'éventail d'actions possibles pour les agents, les interactions entre plusieurs agents indépendants, la reproduction exacte de lieux réels, l'affichage de texte, et « des minutes, pas des heures ». Il est frappant que la liste des limites de Genie 4 soit presque identique. Le son et le « réalisateur » ont été ajoutés ; les limites sont restées.
- **Runway GWM Worlds 2 (3 septembre 2026).** Le modèle de monde de l'entreprise de génération vidéo Runway est aussi un aperçu de recherche. Les chiffres de son billet officiel : 720p, 24 images par seconde, génération sans durée fixe, audio à 48 kHz. Les dialogues sont traités comme une « action » saisie en texte. Ses limites déclarées : « le temps réel échange la fidélité contre la vitesse », « les rotations rapides de caméra dégradent textures et géométrie », « la mémoire à long terme est imparfaite », « les images de référence ne valent que pour la première image ». Runway a donc ajouté le son environ deux mois avant Google, mais le « premier » de Google est qualifié par son propre critère — « parmi les modèles de monde en temps réel » — si bien que les deux affirmations ne se contredisent pas forcément. Nous n'avons aucun moyen de comparer les critères des deux entreprises.
- **Rachat de World Labs par AMD (28 septembre 2026, communication d'AMD).** Le fabricant de puces AMD a annoncé l'acquisition de World Labs, fondée par Fei-Fei Li, dans une opération entièrement en actions valorisée à environ 8,2 milliards de dollars. Le document décrit World Labs comme une entreprise de « modèles d'intelligence spatiale » qui génère, reconstruit et simule des environnements 3D interactifs à partir de texte, d'images et de vidéo, et mentionne aussi une technologie de simulation pour l'apprentissage des robots. Fei-Fei Li deviendra vice-présidente exécutive et directrice scientifique d'AMD à la clôture, prévue d'ici fin 2026. Le document n'emploie pas l'expression « modèle de monde ».

TechCrunch mentionne aussi une information du Wall Street Journal selon laquelle Amazon négocierait le rachat de Decart pour environ 7 milliards de dollars, et l'acquisition de Third Dimension par Rivian, mais nous n'avons pas trouvé de source officielle et ne les traitons pas ici.

## Comment lire une annonce sans chiffres (interprétation)

Premièrement, **« premier » et « le plus » ne sont vrais qu'à l'intérieur du critère choisi par l'entreprise.** Le « premier à générer l'audio nativement » de Google porte la condition « modèle de monde en temps réel », et Runway a sorti en aperçu un modèle de monde en temps réel avec son environ deux mois plus tôt. Aucun des deux n'a tort ; les deux entreprises ont tracé des lignes différentes. Les superlatifs d'une annonce se lisent une fois cette ligne trouvée.

Deuxièmement, **là où un chiffre manque, le chiffre du prédécesseur est le plafond.** Si Genie 3 était en 720p, 24 ips et « plusieurs minutes », et que le billet de Genie 4 ne donne aucun chiffre, rien ne permet de supposer que la résolution ou la durée a nettement augmenté. Les « deux minutes » rapportées par la presse ne sont d'ailleurs pas loin des « plusieurs minutes » de Genie 3. La lecture prudente : le vrai progrès de cette version est dans les fonctions — **son, pilotage, réalisation** — et non dans les chiffres.

Troisièmement, **le paragraphe « limites » survit au paragraphe « fonctions »** — même conclusion que l'article d'hier (NO.30). Que les listes de limites de Genie 3 et Genie 4 soient presque identiques signifie que ces problèmes n'ont pas été résolus en un an et deux mois, et qu'on pourra chercher les mêmes points en premier dans l'annonce de la génération suivante. Du texte illisible, des objets qui changent plus la simulation dure, un son imprécis : pour qui livre réellement de la vidéo, ces trois points comptent plus que les fonctions.

Quatrièmement, notre propre interprétation. Là où vont les modèles de monde en ce moment, ce n'est **pas la « vidéo finie », mais le « terrain d'entraînement des robots et des agents » et le « storyboard pour les humains ».** Google a mis en avant un exemple robotique, AMD a inscrit la simulation pour l'apprentissage des robots dans les motifs du rachat, et Rivas a désigné « l'idéation et le storyboard » comme l'étape la plus utile. L'idée de 2018 — « s'entraîner dans le rêve » — est intacte. Une petite équipe vidéo qui lirait cette nouvelle comme « la génération vidéo s'est améliorée » se trompe d'adresse.

## Si c'était nous — trois choses qu'une équipe de vidéos d'influenceuse IA fait cette semaine (pratique)

1. **Garder les modèles de monde et les modèles de génération vidéo dans des cases séparées.** Nos vidéos de Ria sont faites aujourd'hui avec des modèles de génération vidéo (script → scène → montage). Genie 4 n'est pas un outil qui remplace cette case ; c'est un **« mode brouillon » pour enchaîner plusieurs prises par la parole avant de fixer une scène.** C'est la case que Google décrit avec son exemple de « mode brouillon pour cinéastes » et que Rivas appelle « l'étape du storyboard ». Nous l'inscrivons donc comme candidat uniquement dans la case « idéation de scène » de notre chaîne de production, jamais dans la case « rendu final ». Rivas lui-même a dit que transformer les prototypes en ressources finies est « encore loin ».
2. **S'inscrire sur la liste d'attente, mais ne pas changer le flux de travail.** La liste d'attente de Project Genie et l'accès anticipé à l'API Gemini ne coûtent rien à demander. Mais comme seuls les « testeurs de confiance » y ont accès aujourd'hui et qu'il n'y a aucun chiffre officiel, nous ne lions aucune étape de production à cet outil avant son arrivée. Quand il arrive, nous passons nos dix scènes (présentation de boutique par Ria, scène d'explication d'une étiquette d'ingrédients, scène de comparaison de chaussures de basket, etc.) par la méthode de test du NO.17 et notons d'abord trois points : **le texte est-il lisible, le personnage reste-t-il identique en deux minutes, le son colle-t-il à la scène.** Les trois limites écrites par l'entreprise elle-même sont notre grille de contrôle.
3. **Aligner le filigrane sur notre mention.** Chaque sortie de Genie 4 porte un filigrane SynthID. Notre politique vidéo pour Ria exige déjà de « mentionner le personnage IA », donc la direction est la même. Mais un filigrane est une marque lue par les plateformes et notre mention est une marque lue par les gens ; aucun ne remplace l'autre. Nous écrivons la règle dès maintenant : si une scène faite avec un modèle de monde entre dans la vidéo, la mention en sous-titre gagne « une partie de cette scène est une simulation IA ». Écrire la règle avant l'arrivée de l'outil coûte toujours moins cher.

## Ce que nous n'avons pas retenu cette fois

Les deux annonces d'Anthropic du 27 octobre (premiers résultats dans le développement de médicaments, extension de la coopération avec la General Services Administration américaine) et l'exclusivité d'Axios « la FTC exige le témoignage de dirigeants d'Anthropic » ont été écartées : le conflit d'intérêts est important et elles ne sont pas encore recoupées. Nous n'avons pas encore lu les trois billets d'OpenAI du 26 octobre (coopération académique, cas CodeRabbit, « Le monde du travail en expansion de ChatGPT »). L'attaque de la chaîne d'approvisionnement LiteLLM 1.107.0 (21 octobre, confirmée dans le rapport d'incident de l'entreprise) et la faille de la bibliothèque de compression Brotli divulguée par OpenAI sont d'une autre nature et feront l'objet du prochain article, « la chaîne d'approvisionnement des outils d'IA ». Pour Amazon–Decart et Rivian–Third Dimension, nous n'avons pas trouvé de source officielle.

## Ce que nous n'avons pas pu confirmer

- La résolution, le nombre d'images par seconde, la durée tenue et la latence de Genie 4 ne figurent pas dans le billet officiel. « Jusqu'à deux minutes, le double de Genie 3 » vient de TechCrunch (repris par DigitalToday) et nous n'avons pu le confirmer dans aucun document officiel.
- « Premier modèle de monde en temps réel à générer l'audio nativement » est le critère propre de l'entreprise, et nous n'avons pas pu vérifier en quoi il diffère de celui de Runway GWM Worlds 2 (3 septembre).
- Nous n'avons pas utilisé Genie 4 nous-mêmes. Toutes les descriptions de fonctions viennent du billet de l'entreprise et de la couverture du briefing ; nous n'avons trouvé aucune mesure indépendante.
- Le calendrier pour Project Genie et l'API Gemini n'est donné que comme « progressif » et « dans les prochaines semaines » (TechCrunch) ; nous n'avons pas pu fixer de date.

## Ce que nous avons lu en parallèle

Nous avons ouvert directement des sources de natures différentes. Elles sont classées en documents officiels d'entreprise, communications réglementaires, articles scientifiques, presse et nos articles précédents.

Documents officiels d'entreprise :

- [Genie 4: A new generation of world simulation (Google DeepMind)](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/) — anglais, annonce officielle (fonctions, limites, disponibilité ; aucun chiffre)
- [We're announcing Genie 4, our new world model for real-time interactive simulation (Google)](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/introducing-genie-4/) — anglais, blog officiel de Google (ordre de déploiement)
- [Genie 3: A new frontier for world models (Google DeepMind)](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) — anglais, annonce officielle du prédécesseur (720p, 24 ips, « plusieurs minutes », une minute de mémoire)
- [Introducing GWM Worlds 2 (Runway)](https://runway.com/research/introducing-gwm-worlds-2) — anglais, billet de recherche officiel d'un concurrent (720p, 24 ips, audio 48 kHz, limites)

Communications réglementaires :

- [AMD to Acquire World Labs to Advance the Future of AI Compute (AMD Investor Relations)](https://ir.amd.com/news-events/press-releases/detail/1299/amd-to-acquire-world-labs-to-advance-the-future-of-ai-compute) — anglais, communication d'entreprise (environ 8,2 milliards de dollars en actions, clôture prévue)

Articles scientifiques :

- [World Models — David Ha, Jürgen Schmidhuber (arXiv, 2018)](https://arxiv.org/abs/1803.10122v1) — anglais, point de départ de la notion de « modèle de monde »

Presse :

- [Google's Genie 4 world model adds audio, more realistic worlds, and real-time steering (TechCrunch)](https://techcrunch.com/2026/10/27/googles-genie-4-world-model-adds-audio-more-realistic-worlds-and-real-time-steering/) — anglais, média tech (briefing, « deux minutes », propos de Rivas, contexte de marché)
- [Google DeepMind Rolls Out Genie 4 World Model in Research Preview (Unite.AI)](https://www.unite.ai/google-deepmind-rolls-out-genie-4-world-model-in-research-preview/) — anglais, média IA (recoupement du billet officiel, comparaison avec Genie 3)
- [Google DeepMind unveils Genie 4 world model, targeting robots and film production (DigitalToday, édition anglaise)](https://www.digitaltoday.co.kr/en/view/120253/google-deepmind-unveils-genie-4-world-model-targeting-robots-and-film-production) — anglais, média coréen (citant TechCrunch)

Nos articles précédents :

- [Le prix d'usage divisé par deux, le coût de fabrication en milliards par mois (AP News NO.30)](https://www.apholdings.kr/ko/news/half-price-terra-and-the-s1-compute-bill/) — coréen, comment lire « les limites qu'une entreprise écrit elle-même »
- [Quelle IA pour quelle tâche — les usages déclarés par les entreprises et notre méthode de test (AP News NO.17)](https://www.apholdings.kr/ko/news/which-ai-for-which-job/) — coréen, notre méthode de test par tâche
