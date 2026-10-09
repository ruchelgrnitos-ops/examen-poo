class Note:
    def __init__(self, etudiant, matiere, valeur):
        self.etudiant = etudiant
        self.matiere = matiere
        self.valeur = float(valeur)

    def calculer_moyenne(self):
        return self.valeur

    @staticmethod
    def moyenne_ponderee(notes):
        if not notes:
            return 0.0
        total = sum(n.valeur * n.matiere.coef for n in notes)
        coefs = sum(n.matiere.coef for n in notes)
        return total / coefs if coefs else 0.0

    @staticmethod
    def mention(moyenne):
        if moyenne < 10:
            return "Ajourné"
        if moyenne < 12:
            return "Passable"
        if moyenne < 14:
            return "Assez bien"
        if moyenne < 16:
            return "Bien"
        return "Très bien"
