from datetime import  date, datetime
import sqlite3






class Citoyen :
    def __init__(self, nom, prenom, nationalite, date_naissance: date, date_mort = "vivant",adresse = ""):
        self.nom = nom
        self.prenom = prenom
        self.nationalite = nationalite
        self.date_naissance = date_naissance
        self.date_mort = date_mort
        self.adresse = adresse

    def nom_complet(self):
        """Retourne le nom complet de la personne."""
        return f"{self.nom} {self.prenom}"

    def definir_age(self):
        """
        Calcule l'age d'une personne en fonction de son age et de la date du jour


        """
        if not isinstance(self.date_naissance, str):
            raise TypeError("format doit etre str YYYY-MM-DD")

        date_naissance = datetime.strptime(self.date_naissance, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - date_naissance.year
        if today < date(today.year, date_naissance.month, date_naissance.day):
            age -= 1
        return age



    def ajouter_citoyen(self):
        try:
            connexion = sqlite3.connect("enquete.db")
            cursor = connexion.cursor()
            age = self.definir_age() #faire la conversion avant enregistrement
            self.date_naissance = datetime.strptime(self.date_naissance, "%Y-%m-%d")

            cursor.execute(
                """
                INSERT INTO citoyen(nom, prenom, nationalite,  date_naissance, date_mort,adresse, age)
                VALUES (?, ?, ?, ?, ?, ?,?)
                """, (self.nom, self.prenom,self.nationalite, self.date_naissance, self.date_mort, self.adresse, age )
            )
            connexion.commit()
            connexion.close()
            print(f"Le citoyen {self.nom_complet()} à été enregistré")
        except sqlite3.OperationalError as e:
            print(e)


    @staticmethod
    def recupere_liste_citoyen():
        connexion = sqlite3.connect("../interf/enquete.db")
        cursor = connexion.cursor()
        cursor.execute("""SELECT * FROM citoyen""")
        tuples = cursor.fetchall()
        connexion.close()
        citoyens = []
        for c in tuples:
            print(c)
            citoyens.append(
                Citoyen(
                    nom=c[1],prenom=c[2], nationalite=c[3],
                    date_naissance=c[4], date_mort=c[5],adresse=c[6]
                ))



        return citoyens


class Criminel(Citoyen) :
    def __init__(self, cId, nom, prenom, nationalite, adresse, date_naissance, antecedents, statut):
        super().__init__( nom, prenom, nationalite, date_naissance, adresse)
        self.cId = cId #clé étrangère qui lie au citoyen
        self.antecedents = antecedents
        self.statut = statut

    def creer_criminel(self):
        """sauvegarder le criminel dans la db """
        try:
            connexion = sqlite3.connect("enquete.db")
            cursor = connexion.cursor()

            cursor.execute(
                """
                INSERT INTO criminel(cId, statut)
                VALUES (?, ?)
                """, (self.cId, self.statut)
            )
            connexion.commit()
            connexion.close()
            print(f"Le criminel {self.nom_complet()} à été enregistré")
        except sqlite3.OperationalError as e:
            print(e)

    def afficher_antecedents(self):
        """afficher les antécédents du criminel depuis db criminel_enquete"""
        try:
            connexion = sqlite3.connect("db/enquete.db")
            cursor = connexion.cursor()

            cursor.execute("SELECT * FROM criminel_enquete WHERE cId = ?", (self.cId,))
            result = cursor.fetchall()
            connexion.close()

            if result:
                antecedents = result[0]
                print(f"Antécédents de {self.nom_complet()} : {antecedents}")
            else:
                print(f"Aucun antécédent trouvé pour {self.nom_complet()}")
        except sqlite3.OperationalError as e:
            print(e)

    def modifier_criminel(self, statut):
        """Modifier informations du criminel"""

        try:
            connexion = sqlite3.connect("db/enquete.db")
            cursor = connexion.cursor()

            query = """UPDATE criminel SET statut = ? WHERE cId = ?"""
            cursor.execute(query, (statut, self.cId))
            connexion.commit()
            connexion.close()

            self.statut = statut
            print(f"Le statut de {self.nom_complet()} a été modifier")
        except sqlite3.OperationalError as e:
            print(e)











class Victime(Citoyen):
    pass

class Temoin(Citoyen):
    pass

class Suspect(Citoyen):
    pass

class Expert(Citoyen):
    pass

class Inspecteur(Citoyen):
    pass
