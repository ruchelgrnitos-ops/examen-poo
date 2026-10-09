from etudiant import Etudiant
from matiere import Matiere
from note import Note

class Inscription:
    def __init__(self):
        self.etudiants = {}
        self.matieres = {}
        self.notes = []

    def ajouter_etudiant(self, matricule, nom, prenom, filiere):
        if matricule in self.etudiants:
            raise ValueError("Ce matricule existe déjà.")
        self.etudiants[matricule] = Etudiant(matricule, nom, prenom, filiere)

    def supprimer_etudiant(self, matricule):
        if matricule not in self.etudiants:
            raise ValueError("Étudiant introuvable.")
        del self.etudiants[matricule]
        self.notes = [n for n in self.notes if n.etudiant.matricule != matricule]

    def ajouter_matiere(self, code, nom, coef):
        if code in self.matieres:
            raise ValueError("Ce code matière existe déjà.")
        coef = float(coef)
        if coef <= 0:
            raise ValueError("Le coefficient doit être supérieur à 0.")
        self.matieres[code] = Matiere(code, nom, coef)

    def supprimer_matiere(self, code):
        if code not in self.matieres:
            raise ValueError("Matière introuvable.")
        del self.matieres[code]
        self.notes = [n for n in self.notes if n.matiere.code != code]

    def ajouter_note(self, matricule, code_matiere, valeur):
        if matricule not in self.etudiants:
            raise ValueError("Étudiant introuvable.")
        if code_matiere not in self.matieres:
            raise ValueError("Matière introuvable.")
        valeur = float(valeur)
        if not 0 <= valeur <= 20:
            raise ValueError("La note doit être comprise entre 0 et 20.")

        # Une seule note par étudiant et par matière : on la remplace.
        for n in self.notes:
            if n.etudiant.matricule == matricule and n.matiere.code == code_matiere:
                n.valeur = valeur
                return

        self.notes.append(Note(
            self.etudiants[matricule],
            self.matieres[code_matiere],
            valeur
        ))

    def notes_etudiant(self, matricule):
        return [n for n in self.notes if n.etudiant.matricule == matricule]

    def resultat_etudiant(self, matricule):
        if matricule not in self.etudiants:
            raise ValueError("Étudiant introuvable.")
        notes = self.notes_etudiant(matricule)
        moyenne = Note.moyenne_ponderee(notes)
        return moyenne, Note.mention(moyenne)
