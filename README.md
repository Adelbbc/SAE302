# SAE302


Titre : " - Jeu Quiz"
Equipe : Adel Moussa Evan
Date : 14 janvier 2025

2. Introduction
Présentation générale :
Objectif : Développer un jeu quiz interactif sur le thème des jeux vidéo.
Fonctionnalités principales :
Choix des thèmes, chronomètre, score, classement des meilleurs joueurs.
Collaboration en équipe à 3 pour concevoir une solution technique et ludique.

3. Organisation de l'équipe
Méthodes de travail :
GitHub : Versionnement et partage du code entre les membres.
Trello : Gestion des tâches (en cours, terminées, bugs à résoudre).
Travail collaboratif : Répartition des tâches pour maximiser l'efficacité.

4. Technologies et bibliothèques utilisées
Langue : Python.
Bibliothèques :
socket: Communication client/serveur via TCP/UDP.
threading: Gestion des connexions multiples.
sqlite3: Gestion des données (questions, scores, utilisateurs).
Tkinter : Interface graphique du client.
PIL(ImageTk) : Affichage des images dans l'application.

5. Description du jeu Quiz
Thèmes disponibles :
Action, RPG, Aventure et mode Aléatoire.
Questions :
Types de questions : 4 choix possibles, chronomètre de 15 secondes.
Score calculé en fonction des bonnes réponses.
Affichage des résultats :
Score final affiché à la fin de chaque partie.
Tableau des meilleurs scores accessible depuis le menu principal.

6. Base de données (SQLite)
Structure :
Tableau scores: Nom du joueur et son score.
Classement des scores :
Récupération des 10 meilleurs scores triés par ordre décroissant grâce à une requête SQL.
Exemple de classement affiché :
réduction
Copier le code
1. Moussa - 15 points  
2. Evan - 13 points  
3. Adel - 12 points  


Avantage : Stockage persistant des partitions pour un classement durable.

7. Méthodes de développement
Architecture client/serveur :
Le serveur gère les questions et stocke les partitions.
Le client affiche l'interface et interagit avec le joueur.
Gestion des connexions :
Chaque joueur connecté est géré par un thread distinct côté serveur.



9. Conclusion et perspectives
Résultats obtenus :
Jeu fonctionnel avec une expérience fluide.
Classement dynamique des meilleurs scores.
Améliorations envisagées :
Ajouter des thèmes supplémentaires.
Implémenter un mode multijoueur en temps réel.
Optimisation de l'interface graphique pour une meilleure expérience.








commande obesolete  pour lancer lancienne version  l'  app.py sur le cmd >flask run

nouvelle version dans \quizz2\dist\quiz_client
lancer le quiz en cliquant dessus
