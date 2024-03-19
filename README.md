Ce programme est un jeu de casse briques basique. Au lancement, l'utilisateur doit input entrée ou echap pour jouer
ou quitter, respectivement. En selectionnant jouer, une grille de briques, une raquette representee par un rectangle et une balle blanche apparaissent a l'ecran, et l'utilisateur doit appuyer sur espace pour lancer le jeu. Les commandes de jeu sont egalement affichees (p pour mettre le jeu en pause et a et d pour deplacer la raquette). une fois la touche espace pressée, le texte disparait, la balle se met en mouvement et on peut deplacer la raquette. la balle rebondit sur les murs et la raquette, mais le jeu s'arrete si elle touche le bas de l'ecran. le but est donc de tenir assez longtemps pour que la balle touche toutes les briques, qui disparaissent une fois touchées. Chaque brique detruite augmente la vitesse de la balle, creant de la difficulté.

Le jeu a ete code avec le module Tkinter, notamment les fonctions de canevas.

Classes

Game(tk.Frame)

la classe principale, heritant de la classe du widget Frame de Tkinter, contient toutes les variables et methodes permettant le fonctionnement du programme. Cree un canevas, cree une raquette, gere le mainloop, cree la balle et les briques, gere la pause, les conditions de victoire et le checking de collision. elle appellera les fonctions des GameObject.

GameObject(object)

La classe regroupant les attributs et methodes communs a tous les objets(getCoords,move,delete), Tous les objets heritent de GameObject.

Paddle(GameObject)

Classe specifique a l'objet Paddle(raquette) qui contient les attributs de la raquette et la methode de deplacement.

Ball(GameObject)

Classe specifique a la balle, contient les attributs de la balle et les methodes de deplacement et de collision.

Brick(GameObject)

Classe specifique aux briques, ne contient pas de methodes specifiques.

Chaque classe appelle la fonction super() pour initialiser les attributs de la classe GameObject.

La balle se deplace dans 4 directions, et sa vitesse augmente a chaque brique touchée.

La fonction mainloop de tkinter est appelée via la classe Game.
Les noms de fonctions sont explicites a leur fonctionnement.