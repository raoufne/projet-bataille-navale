import pytermgui as ptg
from grille import Grille
from bateau import PorteAvion, Croiseur, Torpilleur, SousMarin
from score_helper import load_highscores, save_highscores

JAUNE = "#FCBA03"
MARRON = "#8C6701"
GRIS = "#4D4940"
NOIR = "#242321"

DIFFICULTES = {
    "C": {"nom": "Facile", "desc": "4 bateaux, coups illimités"},
    "B": {"nom": "Moyen", "desc": "4 bateaux, 40 coups max"},
    "A": {"nom": "Difficile", "desc": "4 bateaux, 40 coups, repositionnement"}
}

def configurer_theme():
    ptg.tim.alias("texte", "#cfc7b0")
    ptg.tim.alias("titre", f"bold {JAUNE}")
    ptg.tim.alias("bouton", f"bold @{GRIS} texte")
    ptg.tim.alias("bouton.actif", "inverse bouton")
    
    ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
    ptg.boxes.ROUNDED.set_chars_of(ptg.Container)
    
    ptg.Button.styles.label = "bouton"
    ptg.Button.styles.highlight = "bouton.actif"
    ptg.Label.styles.value = "texte"
    ptg.Window.styles.border__corner = "#C2B280"


class BatailleNavale:
    def __init__(self, manager):
        self.manager = manager
        self.en_jeu = False
        self.victoires_difficile = 0
        self.difficultes = dict(DIFFICULTES)
        self.scores = load_highscores()
        
        self.grille = None
        self.bateaux = []
        self.coups = 0
        self.max_coups = 0
        self.diff = "C"
        self.cases_tirees = []
        self.bateaux_coules = []
        self.bateaux_touches = []
        
        self.label_grille = None
        self.label_info = None
        self.label_msg = None
        self.input_x = None
        self.input_y = None
        
        self.creer_interface()
    
    def creer_interface(self):
        entete = ptg.Window(
            "[titre] ⚓ Bataille Navale ⚓ ",
            box="EMPTY",
            is_persistant=True
        )
        entete.styles.fill = f"@{MARRON}"
        self.manager.add(entete)
        
        pied = ptg.Window(
            ptg.Splitter(
                ptg.Button("Nouvelle Partie", lambda *_: self.menu_difficulte()),
                ptg.Button("Quitter", lambda *_: self.confirmer_quitter())
            ),
            box="EMPTY",
            is_persistant=True
        )
        pied.styles.fill = f"@{NOIR}"
        self.manager.add(pied, assign="footer")
        
        self.label_info = ptg.Label("Choisissez 'Nouvelle Partie'\npour commencer", width=28, wrap=True)
        self.input_x = ptg.InputField("", prompt="Ligne : ")
        self.input_y = ptg.InputField("", prompt="Colonne : ")
        
        panneau = ptg.Window(
            "[titre]Informations",
            "",
            self.label_info,
            "",
            ptg.Label("[210]Coordonnées (1-10):"),
            self.input_x,
            self.input_y,
            "",
            ptg.Button("🎯 Tirer", lambda *_: self.tirer()),
            box="SINGLE",
            is_persistant=True
        )
        self.manager.add(panneau, assign="body_right")
        
        self.label_grille = ptg.Label("Commencez une partie!", width=60, wrap=True)
        self.label_msg = ptg.Label("", width=60, wrap=True)
        
        principal = ptg.Window(
            "[titre]Grille de Jeu",
            "",
            self.label_grille,
            "",
            self.label_msg,
            vertical_align=ptg.VerticalAlignment.TOP,
            overflow=ptg.Overflow.SCROLL,
            is_persistant=True
        )
        self.manager.add(principal, assign="body")
    
    def menu_difficulte(self):
        boutons = [
            ptg.Button("Facile", lambda *_: self.demarrer("C", modal)),
            ptg.Button("Moyen", lambda *_: self.demarrer("B", modal)),
            ptg.Button("Difficile", lambda *_: self.demarrer("A", modal))
        ]
        
        if "Z" in self.difficultes:
            boutons.append(ptg.Button("🔥 Extrême", lambda *_: self.demarrer("Z", modal)))
        
        modal = ptg.Window(
            "[titre]Choisissez la Difficulté",
            "",
            *boutons,
            box="DOUBLE"
        ).center()
        
        self.manager.add(modal)
    
    def demarrer(self, diff, modal=None):
        if modal:
            modal.close()
        
        self.diff = diff
        self.grille = Grille(8, 10)
        self.bateaux = [PorteAvion(0, 0), Croiseur(0, 0), Torpilleur(0, 0), SousMarin(0, 0)]
        
        if diff == "Z":
            self.grille = Grille(int(8 * 1.5), int(10 * 1.5))
            self.bateaux.append(SousMarin(0, 0))
        
        positions = []
        for b in self.bateaux:
            b.position_alea(self.grille, positions)
            positions.extend(b.positions)
        
        self.coups = 0
        self.cases_tirees = []
        self.bateaux_coules = []
        self.bateaux_touches = []
        self.max_coups = 81 if diff == "C" else 40
        self.en_jeu = True
        
        self.rafraichir_grille()
        self.mettre_a_jour_stats()
        self.label_msg.value = "🎲 Entrez X et Y puis cliquez Tirer !"
    
    def tirer(self):
        if not self.en_jeu:
            self.label_msg.value = "⚠️ Aucune partie en cours"
            return
        
        val_x = self.input_x.value.strip()
        val_y = self.input_y.value.strip()
        
        if not val_x or not val_y:
            self.label_msg.value = "⚠️ Entrez les deux coordonnées"
            return
        
        try:
            x = int(val_x) - 1
            y = int(val_y) - 1
        except:
            self.label_msg.value = "⚠️ Entrez des nombres valides"
            return
        
        if not (0 <= x < self.grille.nb_lignes and 0 <= y < self.grille.nb_colonnes):
            self.label_msg.value = "🚫 Hors de la grille !"
            return
        
        if (x, y) in self.cases_tirees:
            self.label_msg.value = "⛔ Déjà tiré ici !"
            return
        
        self.cases_tirees.append((x, y))
        self.coups += 1
        
        bateau_touche = None
        for b in self.bateaux:
            if b not in self.bateaux_coules and (x, y) in b.positions:
                bateau_touche = b
                break
        
        if bateau_touche:
            self.grille.tirer(x, y, touche='💣')
            
            if bateau_touche.coule(self.grille):
                self.bateaux_coules.append(bateau_touche)
                self.grille.ajoute(bateau_touche)
                
                if len(self.bateaux_coules) != len(self.bateaux):
                    message = f"🎯 Coulé {bateau_touche.marque} !"
                    if self.diff == 'Z':
                        self.coups -= 5
                        message += " (+5 coups bonus)"
                    elif self.diff == 'A':
                        self.coups -= 1
                        message += " (+1 coup bonus)"
                    self.label_msg.value = message
            else:
                if bateau_touche not in self.bateaux_touches:
                    self.bateaux_touches.append(bateau_touche)
                self.label_msg.value = "🔥 Touché ! Continuez..."
        else:
            self.grille.tirer(x, y)
            self.label_msg.value = "💧 Plouf !"
        
        if self.diff in ["A", "Z"]:
            occupees = list(self.cases_tirees)
            for b_temp in self.bateaux_touches:
                for pos in b_temp.positions:
                    if pos not in self.cases_tirees:
                        occupees.append(pos)
            
            for b in self.bateaux:
                if b not in self.bateaux_touches and b not in self.bateaux_coules:
                    b.position_alea(self.grille, occupees)
                    occupees.extend(b.positions)
        
        self.rafraichir_grille()
        self.mettre_a_jour_stats()
        
        if len(self.bateaux_coules) == len(self.bateaux):
            self.victoire()
        elif self.coups >= self.max_coups:
            self.defaite()
    
    def rafraichir_grille(self):
        if self.grille and self.label_grille:
            self.label_grille.value = str(self.grille)
    
    def mettre_a_jour_stats(self):
        meilleur = self.scores.get(self.diff)
        info = f"[{self.difficultes[self.diff]['nom']}]\n{self.difficultes[self.diff]['desc']}\n\n"
        info += f"🏆 Record : {meilleur if meilleur else 'Aucun'}\n"
        info += f"Coups : {self.coups}/{self.max_coups if self.max_coups < 81 else '∞'}\n"
        info += f"Bateaux coulés : {len(self.bateaux_coules)}/{len(self.bateaux)}"
        self.label_info.value = info
    
    def victoire(self):
        self.en_jeu = False
        msg = f"🏁 VICTOIRE !\n\nTous les bateaux ont été détruits !\nCoups utilisés : {self.coups}"
        
        meilleur = self.scores.get(self.diff)
        if not meilleur or self.coups < meilleur:
            self.scores[self.diff] = self.coups
            save_highscores(self.scores)
            msg += f"\n\n🏆 Nouveau record pour {self.difficultes[self.diff]['nom']} !"
        
        if self.diff == "A":
            self.victoires_difficile += 1
            if self.victoires_difficile == 2 and "Z" not in self.difficultes:
                self.difficultes["Z"] = {"nom": "Extrême", "desc": "Grille plus grande, 5 bateaux, 40 coups, repositionnement"}
                msg += "\n\n🎊 Difficulté EXTRÊME débloquée !"
        
        self.label_msg.value = msg
        self.modal_rejouer()
    
    def defaite(self):
        self.en_jeu = False
        
        for b in self.bateaux:
            if b not in self.bateaux_coules:
                self.grille.ajoute(b)
        
        self.rafraichir_grille()
        
        msg = f"❌ GAME OVER !\n\nVous avez épuisé vos {self.max_coups} coups\n"
        msg += f"Bateaux coulés : {len(self.bateaux_coules)}/{len(self.bateaux)}\n\n"
        msg += "Les bateaux restants sont révélés sur la grille"
        self.label_msg.value = msg
        
        self.victoires_difficile = 0
        if "Z" in self.difficultes:
            del self.difficultes["Z"]
        
        self.modal_rejouer()
    
    def modal_rejouer(self):
        modal = ptg.Window(
            "[titre]Partie Terminée",
            "",
            ptg.Label("Voulez-vous rejouer ?"),
            "",
            ptg.Button("Oui", lambda *_: (modal.close(), self.menu_difficulte())),
            ptg.Button("Non", lambda *_: (modal.close(), self.manager.stop())),
            box="DOUBLE"
        ).center()
        self.manager.add(modal)
    
    def confirmer_quitter(self):
        modal = ptg.Window(
            "[titre]Confirmer",
            "",
            ptg.Label("Voulez-vous vraiment quitter ?"),
            "",
            ptg.Button("Oui", lambda *_: self.manager.stop()),
            ptg.Button("Non", lambda *_: modal.close()),
            box="DOUBLE"
        ).center()
        self.manager.add(modal)



configurer_theme()

with ptg.WindowManager() as manager:
    layout = ptg.Layout()
    layout.add_slot("Header", height=1)
    layout.add_break()
    layout.add_slot("Body")
    layout.add_slot("Body right", width=0.28)
    layout.add_break()
    layout.add_slot("Footer", height=1)
    
    manager.layout = layout
    BatailleNavale(manager)

ptg.tim.print(f"[{JAUNE}]Au revoir ! 👋")