class Etudiant:
    def __init__(self, matricule, nom, prenom, filiere):
        self.matricule = matricule
        self.nom = nom
        self.prenom = prenom
        self.filiere = filiere

    def s_inscrire(self):
        return f"{self.prenom} {self.nom} est inscrit(e) en {self.filiere}."

    def afficher(self):
        return f"{self.matricule} - {self.nom} {self.prenom} - {self.filiere}"
