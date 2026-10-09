class Matiere:
    def __init__(self, code, nom, coef):
        self.code = code
        self.nom = nom
        self.coef = float(coef)

    def afficher(self):
        return f"{self.code} - {self.nom} (Coef. {self.coef:g})"
