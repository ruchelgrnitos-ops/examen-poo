PROJET : Système de gestion d'inscription et de génération de notes
===============================================================

Technologies :
- Python 3
- Programmation Orientée Objet (POO)
- Tkinter
- Excel avec openpyxl

INSTALLATION
------------

1. Installer Python 3.
2. Ouvrir un terminal dans ce dossier.
3. Installer la bibliothèque Excel :

   pip install -r requirements.txt

4. Lancer l'application :

   python main.py

FONCTIONNALITES
---------------

- Ajouter et supprimer des étudiants.
- Ajouter et supprimer des matières.
- Enregistrer/modifier les notes.
- Calculer automatiquement la moyenne pondérée.
- Attribuer automatiquement une mention.
- Afficher les résultats dans Tkinter.
- Exporter les résultats et le détail des notes vers Excel.

FORMULE
-------

Moyenne = Somme(Note × Coefficient) / Somme(Coefficients)

MENTIONS
--------

< 10       : Ajourné
10 à 11.99 : Passable
12 à 13.99 : Assez bien
14 à 15.99 : Bien
>= 16      : Très bien

REMARQUE
--------

Les données sont conservées en mémoire pendant l'exécution.
L'export Excel crée un fichier .xlsx, mais ne constitue pas encore
une sauvegarde automatique des données de l'application.
