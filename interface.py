import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from inscription import Inscription
from excel import exporter_excel

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des inscriptions et des notes")
        self.geometry("1050x680")
        self.minsize(900, 600)
        self.gestion = Inscription()

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.creer_interface()
        self.actualiser_tout()

    def creer_interface(self):
        titre = ttk.Label(
            self,
            text="SYSTÈME DE GESTION D'INSCRIPTION ET DE NOTES",
            font=("Arial", 18, "bold")
        )
        titre.pack(pady=(15, 5))

        sous = ttk.Label(
            self,
            text="Python • Programmation Orientée Objet • Tkinter • Excel",
            font=("Arial", 10)
        )
        sous.pack(pady=(0, 12))

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=15, pady=10)

        self.tab_etudiants = ttk.Frame(self.tabs, padding=12)
        self.tab_matieres = ttk.Frame(self.tabs, padding=12)
        self.tab_notes = ttk.Frame(self.tabs, padding=12)
        self.tab_resultats = ttk.Frame(self.tabs, padding=12)

        self.tabs.add(self.tab_etudiants, text="👨‍🎓 Étudiants")
        self.tabs.add(self.tab_matieres, text="📚 Matières")
        self.tabs.add(self.tab_notes, text="📝 Notes")
        self.tabs.add(self.tab_resultats, text="📊 Résultats")

        self.creer_tab_etudiants()
        self.creer_tab_matieres()
        self.creer_tab_notes()
        self.creer_tab_resultats()

    def champ(self, parent, row, label, width=25):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        e = ttk.Entry(parent, width=width)
        e.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        return e

    def creer_tab_etudiants(self):
        form = ttk.LabelFrame(self.tab_etudiants, text="Ajouter un étudiant", padding=12)
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)

        self.e_mat = self.champ(form, 0, "Matricule")
        self.e_nom = self.champ(form, 1, "Nom")
        self.e_prenom = self.champ(form, 2, "Prénom")
        self.e_filiere = self.champ(form, 3, "Filière")

        ttk.Button(form, text="Ajouter", command=self.ajouter_etudiant).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        box = ttk.LabelFrame(self.tab_etudiants, text="Liste des étudiants", padding=8)
        box.pack(fill="both", expand=True, pady=12)

        cols = ("matricule", "nom", "prenom", "filiere")
        self.tree_etudiants = ttk.Treeview(box, columns=cols, show="headings")
        titres = {
            "matricule": "Matricule", "nom": "Nom",
            "prenom": "Prénom", "filiere": "Filière"
        }
        for c in cols:
            self.tree_etudiants.heading(c, text=titres[c])
            self.tree_etudiants.column(c, width=170)
        self.tree_etudiants.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(box, orient="vertical", command=self.tree_etudiants.yview)
        sb.pack(side="right", fill="y")
        self.tree_etudiants.configure(yscrollcommand=sb.set)

        ttk.Button(
            self.tab_etudiants, text="Supprimer l'étudiant sélectionné",
            command=self.supprimer_etudiant
        ).pack(anchor="e")

    def creer_tab_matieres(self):
        form = ttk.LabelFrame(self.tab_matieres, text="Ajouter une matière", padding=12)
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)

        self.m_code = self.champ(form, 0, "Code")
        self.m_nom = self.champ(form, 1, "Nom de la matière")
        self.m_coef = self.champ(form, 2, "Coefficient")

        ttk.Button(form, text="Ajouter", command=self.ajouter_matiere).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        box = ttk.LabelFrame(self.tab_matieres, text="Liste des matières", padding=8)
        box.pack(fill="both", expand=True, pady=12)

        cols = ("code", "nom", "coef")
        self.tree_matieres = ttk.Treeview(box, columns=cols, show="headings")
        for c, title, width in [
            ("code", "Code", 160), ("nom", "Matière", 350), ("coef", "Coefficient", 160)
        ]:
            self.tree_matieres.heading(c, text=title)
            self.tree_matieres.column(c, width=width)
        self.tree_matieres.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(box, orient="vertical", command=self.tree_matieres.yview)
        sb.pack(side="right", fill="y")
        self.tree_matieres.configure(yscrollcommand=sb.set)

        ttk.Button(
            self.tab_matieres, text="Supprimer la matière sélectionnée",
            command=self.supprimer_matiere
        ).pack(anchor="e")

    def creer_tab_notes(self):
        form = ttk.LabelFrame(self.tab_notes, text="Enregistrer une note", padding=12)
        form.pack(fill="x")

        ttk.Label(form, text="Étudiant").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_etudiant = ttk.Combobox(form, state="readonly", width=45)
        self.combo_etudiant.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form, text="Matière").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_matiere = ttk.Combobox(form, state="readonly", width=45)
        self.combo_matiere.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form, text="Note / 20").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.n_valeur = ttk.Entry(form, width=20)
        self.n_valeur.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(form, text="Enregistrer / Modifier", command=self.ajouter_note).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        box = ttk.LabelFrame(self.tab_notes, text="Notes enregistrées", padding=8)
        box.pack(fill="both", expand=True, pady=12)

        cols = ("matricule", "etudiant", "matiere", "coef", "note")
        self.tree_notes = ttk.Treeview(box, columns=cols, show="headings")
        for c, title, width in [
            ("matricule", "Matricule", 130),
            ("etudiant", "Étudiant", 230),
            ("matiere", "Matière", 230),
            ("coef", "Coef.", 80),
            ("note", "Note", 90)
        ]:
            self.tree_notes.heading(c, text=title)
            self.tree_notes.column(c, width=width)
        self.tree_notes.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(box, orient="vertical", command=self.tree_notes.yview)
        sb.pack(side="right", fill="y")
        self.tree_notes.configure(yscrollcommand=sb.set)

    def creer_tab_resultats(self):
        top = ttk.Frame(self.tab_resultats)
        top.pack(fill="x", pady=(0, 10))

        ttk.Button(
            top, text="↻ Actualiser", command=self.actualiser_resultats
        ).pack(side="left", padx=4)

        ttk.Button(
            top, text="📗 Exporter vers Excel", command=self.exporter
        ).pack(side="right", padx=4)

        box = ttk.LabelFrame(self.tab_resultats, text="Résultats", padding=8)
        box.pack(fill="both", expand=True)

        cols = ("matricule", "nom", "prenom", "filiere", "moyenne", "mention")
        self.tree_resultats = ttk.Treeview(box, columns=cols, show="headings")
        for c, title, width in [
            ("matricule", "Matricule", 130),
            ("nom", "Nom", 150),
            ("prenom", "Prénom", 150),
            ("filiere", "Filière", 180),
            ("moyenne", "Moyenne", 100),
            ("mention", "Mention", 150)
        ]:
            self.tree_resultats.heading(c, text=title)
            self.tree_resultats.column(c, width=width)
        self.tree_resultats.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(box, orient="vertical", command=self.tree_resultats.yview)
        sb.pack(side="right", fill="y")
        self.tree_resultats.configure(yscrollcommand=sb.set)

    def ajouter_etudiant(self):
        try:
            vals = [x.get().strip() for x in [self.e_mat, self.e_nom, self.e_prenom, self.e_filiere]]
            if not all(vals):
                raise ValueError("Tous les champs sont obligatoires.")
            self.gestion.ajouter_etudiant(*vals)
            for e in [self.e_mat, self.e_nom, self.e_prenom, self.e_filiere]:
                e.delete(0, "end")
            self.actualiser_tout()
            messagebox.showinfo("Succès", "Étudiant ajouté avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_etudiant(self):
        sel = self.tree_etudiants.selection()
        if not sel:
            messagebox.showwarning("Attention", "Sélectionnez un étudiant.")
            return
        matricule = self.tree_etudiants.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirmation", f"Supprimer l'étudiant {matricule} ?"):
            try:
                self.gestion.supprimer_etudiant(matricule)
                self.actualiser_tout()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def ajouter_matiere(self):
        try:
            vals = [self.m_code.get().strip(), self.m_nom.get().strip(), self.m_coef.get().strip()]
            if not all(vals):
                raise ValueError("Tous les champs sont obligatoires.")
            self.gestion.ajouter_matiere(*vals)
            for e in [self.m_code, self.m_nom, self.m_coef]:
                e.delete(0, "end")
            self.actualiser_tout()
            messagebox.showinfo("Succès", "Matière ajoutée avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_matiere(self):
        sel = self.tree_matieres.selection()
        if not sel:
            messagebox.showwarning("Attention", "Sélectionnez une matière.")
            return
        code = self.tree_matieres.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirmation", f"Supprimer la matière {code} ?"):
            try:
                self.gestion.supprimer_matiere(code)
                self.actualiser_tout()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def ajouter_note(self):
        try:
            etu = self.combo_etudiant.get()
            mat = self.combo_matiere.get()
            if not etu or not mat:
                raise ValueError("Sélectionnez un étudiant et une matière.")
            matricule = etu.split(" | ")[0]
            code = mat.split(" | ")[0]
            valeur = self.n_valeur.get().strip()
            self.gestion.ajouter_note(matricule, code, valeur)
            self.n_valeur.delete(0, "end")
            self.actualiser_tout()
            messagebox.showinfo("Succès", "Note enregistrée.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def actualiser_etudiants(self):
        for item in self.tree_etudiants.get_children():
            self.tree_etudiants.delete(item)
        for e in self.gestion.etudiants.values():
            self.tree_etudiants.insert("", "end", values=(
                e.matricule, e.nom, e.prenom, e.filiere
            ))
        self.combo_etudiant["values"] = [
            f"{e.matricule} | {e.nom} {e.prenom}"
            for e in self.gestion.etudiants.values()
        ]

    def actualiser_matieres(self):
        for item in self.tree_matieres.get_children():
            self.tree_matieres.delete(item)
        for m in self.gestion.matieres.values():
            self.tree_matieres.insert("", "end", values=(
                m.code, m.nom, f"{m.coef:g}"
            ))
        self.combo_matiere["values"] = [
            f"{m.code} | {m.nom}" for m in self.gestion.matieres.values()
        ]

    def actualiser_notes(self):
        for item in self.tree_notes.get_children():
            self.tree_notes.delete(item)
        for n in self.gestion.notes:
            self.tree_notes.insert("", "end", values=(
                n.etudiant.matricule,
                f"{n.etudiant.prenom} {n.etudiant.nom}",
                f"{n.matiere.code} - {n.matiere.nom}",
                f"{n.matiere.coef:g}",
                f"{n.valeur:.2f}"
            ))

    def actualiser_resultats(self):
        for item in self.tree_resultats.get_children():
            self.tree_resultats.delete(item)
        for e in self.gestion.etudiants.values():
            moyenne, mention = self.gestion.resultat_etudiant(e.matricule)
            self.tree_resultats.insert("", "end", values=(
                e.matricule, e.nom, e.prenom, e.filiere,
                f"{moyenne:.2f}", mention
            ))

    def actualiser_tout(self):
        self.actualiser_etudiants()
        self.actualiser_matieres()
        self.actualiser_notes()
        self.actualiser_resultats()

    def exporter(self):
        chemin = filedialog.asksaveasfilename(
            title="Enregistrer les résultats Excel",
            defaultextension=".xlsx",
            filetypes=[("Fichier Excel", "*.xlsx")]
        )
        if not chemin:
            return
        try:
            exporter_excel(self.gestion, chemin)
            messagebox.showinfo("Export terminé", f"Fichier Excel créé :\n{chemin}")
        except Exception as e:
            messagebox.showerror("Erreur Excel", str(e))

if __name__ == "__main__":
    app = Application()
    app.mainloop()
