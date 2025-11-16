import tkinter as tk
from tkinter import messagebox
from grille import Grille
from bateau import PorteAvion, Croiseur, Torpilleur, SousMarin
from score_helper import load_highscores, save_highscores
from sound_helper import initialiser_sons, jouer_son, jouer_musique_menu, jouer_musique_jeu, arreter_musique


class BatailleNavaleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚢 Bataille Navale")
        self.root.configure(bg='#1e3a5f')
        
        initialiser_sons()
        self.g = None
        self.liste_bateaux = []
        self.coups = 0
        self.max_coups = 0
        self.cases_deja_tirees = []
        self.bateaux_coules = []
        self.bateaux_touches = []
        self.diff = None
        self.gagne = 0
        self.partie_en_cours = False
        self.scores = load_highscores()
        
        self.difficultes = {
            "C": {"nom": "Facile", "desc": "Grille standard, 4 bateaux, coups illimités."},
            "B": {"nom": "Moyen", "desc": "Grille standard, 4 bateaux, 40 coups maximum."},
            "A": {"nom": "Difficile", "desc": "Grille standard, 4 bateaux, 40 coups, les bateaux se repositionnent après chaque tir."}
        }
        
        self.afficher_menu_difficulte()
    
    def afficher_menu_difficulte(self):
        jouer_musique_menu()

        for widget in self.root.winfo_children():
            widget.destroy()
        
        title = tk.Label(self.root, text="⚓ BATAILLE NAVALE ⚓", 
                        font=("Arial", 28, "bold"), bg="#1a1a2e", fg="#00d4ff")
        title.pack(pady=30)
        
        diff_frame = tk.Frame(self.root, bg='#1e3a5f')
        diff_frame.pack(pady=20)
        
        tk.Label(diff_frame, text="Choisissez votre difficulté :", 
                font=("Arial", 16), bg='#1e3a5f', fg="white").pack(pady=10)
        
        for cle, info in self.difficultes.items():
            btn_frame = tk.Frame(diff_frame, bg="#16213e", relief=tk.RAISED, borderwidth=2)
            btn_frame.pack(pady=10, padx=20, fill=tk.X)
            
            btn = tk.Button(btn_frame, text=f"{info['nom']}", 
                          font=("Arial", 14, "bold"), bg="#0f3460", fg="white",
                          activebackground="#00d4ff", activeforeground="black",
                          width=15, height=2,
                          command=lambda d=cle: self.demarrer_partie(d))
            btn.pack(side=tk.LEFT, padx=10, pady=10)
            
            desc = tk.Label(btn_frame, text=info['desc'], 
                          font=("Arial", 10), bg="#16213e", fg="#aaaaaa")
            desc.pack(side=tk.LEFT, padx=10)
            
            best = self.scores.get(cle)
            if best is not None:
                score_label = tk.Label(btn_frame, text=f"🏆 Record: {best} coups", 
                                      font=("Arial", 10, "bold"), bg="#16213e", fg="#ffd700")
                score_label.pack(side=tk.RIGHT, padx=10)
    
    def demarrer_partie(self, difficulte):
        jouer_musique_jeu()
        self.diff = difficulte
        self.g = Grille(8, 10)
        self.liste_bateaux = [PorteAvion(0, 0), Croiseur(0, 0), Torpilleur(0, 0), SousMarin(0, 0)]
        
        if self.diff == 'C':
            self.max_coups = self.g.nb_lignes * self.g.nb_colonnes + 1
        elif self.diff == 'B':
            self.max_coups = self.g.nb_lignes * self.g.nb_colonnes // 2
        elif self.diff == 'A':
            self.max_coups = self.g.nb_lignes * self.g.nb_colonnes // 2
        elif self.diff == 'Z':
            self.g = Grille(int(self.g.nb_lignes * 1.5), int(self.g.nb_colonnes * 1.5))
            self.liste_bateaux.append(SousMarin(0, 0))
            self.max_coups = 40
        
        positions_occupees = []
        for b in self.liste_bateaux:
            b.position_alea(self.g, positions_occupees)
            positions_occupees.extend(b.positions)
        
        self.coups = 0
        self.cases_deja_tirees = []
        self.bateaux_coules = []
        self.bateaux_touches = []
        self.partie_en_cours = True
        
        self.creer_grille_graphique()
    
    def creer_grille_graphique(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        info_frame = tk.Frame(self.root, bg="#16213e", height=80)
        info_frame.pack(expand=True, pady=10, padx=10)
        
        self.coups_label = tk.Label(info_frame, text=f"Coups: {self.coups}/{self.max_coups if self.max_coups < 80 else '∞'}", 
                                    font=("Arial", 14, "bold"), bg="#16213e", fg="white")
        self.coups_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.diff_label = tk.Label(info_frame, text=f"Difficulté: {self.difficultes[self.diff]['nom']}", 
                                   font=("Arial", 14, "bold"), bg="#16213e", fg="#00d4ff")
        self.diff_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.bateaux_label = tk.Label(info_frame, 
                                      text=f"Bateaux coulés: {len(self.bateaux_coules)}/{len(self.liste_bateaux)}", 
                                      font=("Arial", 14, "bold"), bg="#16213e", fg="white")
        self.bateaux_label.pack(side=tk.LEFT, padx=20, pady=10)        

        self.message_label = tk.Label(self.root, text="Cliquez sur une case pour tirer!", 
                                     font=("Arial", 12), bg='#1e3a5f', fg="white")
        self.message_label.pack(pady=10)

        grid_container = tk.Frame(self.root, bg="#16213e", relief=tk.RAISED, borderwidth=2)
        grid_container.pack(pady=10)
        
        self.frame_grille = tk.Frame(grid_container, bg="#16213e")
        self.frame_grille.pack(padx=10, pady=10)

        tk.Label(self.frame_grille, text="", bg="#16213e", width=3).grid(row=0, column=0)
        for col in range(self.g.nb_colonnes):
            tk.Label(self.frame_grille, text=str(col + 1), font=('Arial', 10, 'bold'),
                    bg="#16213e", fg='white', width=3).grid(row=0, column=col + 1, pady=3)
        
        self.boutons_grille = {}
        for ligne in range(self.g.nb_lignes):
            tk.Label(self.frame_grille, text=chr(ord('A') + ligne), font=('Arial', 10, 'bold'),
                    bg="#16213e", fg='white', width=3).grid(row=ligne + 1, column=0, padx=3)
            
            for col in range(self.g.nb_colonnes):
                btn = tk.Button(self.frame_grille, text='🌊', font=('Arial', 14),
                               width=3, height=1, bg='#3498db', 
                               relief=tk.RAISED, cursor="crosshair",
                               command=lambda l=ligne, c=col: self.tirer_case(l, c))
                btn.grid(row=ligne + 1, column=col + 1, padx=1, pady=1)
                self.boutons_grille[(ligne, col)] = btn
      
        control_frame = tk.Frame(self.root, bg='#1e3a5f')
        control_frame.pack(pady=10)

        self.btn_nouvelle_partie = tk.Button(control_frame, text="🔄 Nouvelle Partie", 
                                             command=self.confirmer_quitter,
                                             font=('Arial', 11, 'bold'), bg='#4a90e2', fg='white',
                                             padx=15, pady=8, cursor="hand2", relief=tk.RAISED)
        self.btn_nouvelle_partie.pack(side=tk.LEFT, padx=5)

        self.btn_quitter = tk.Button(control_frame, text="❌ Quitter", 
                                     command=self.quitter_app,
                                     font=('Arial', 11, 'bold'), bg='#e74c3c', fg='white',
                                     padx=15, pady=8, cursor="hand2", relief=tk.RAISED)
        self.btn_quitter.pack(side=tk.LEFT, padx=5)
    
    def confirmer_quitter(self):
        if self.partie_en_cours:
            if messagebox.askyesno("Confirmation", "Voulez-vous vraiment abandonner la partie en cours ?"):
                self.gagner = 0
                if 'Z' in self.difficultes:
                    del self.difficultes['Z']
                self.afficher_menu_difficulte()
        else:
            self.afficher_menu_difficulte()
    
    def quitter_app(self):
        if self.partie_en_cours:
            if messagebox.askyesno("Confirmation", "Voulez-vous vraiment quitter le jeu ?"):
                self.root.quit()
        else:
            self.root.quit()
    
    def tirer_case(self, ligne, colonne):
        if not self.partie_en_cours:
            return
        
        if (ligne, colonne) in self.cases_deja_tirees:
            self.message_label.config(text="⛔ Vous avez déjà tiré ici !", fg="#e94560")
            jouer_son("error", volume=0.5)

            return
        
        self.cases_deja_tirees.append((ligne, colonne))
        self.coups += 1
        
        touche_bateau = None
        for b in self.liste_bateaux:
            if b in self.bateaux_coules:
                continue
            if (ligne, colonne) in b.positions:
                touche_bateau = b
                break
        
        if touche_bateau:
            self.g.tirer(ligne, colonne, touche='💣')
            jouer_son("hit", volume=0.5)

            if touche_bateau.coule(self.g):
                self.bateaux_coules.append(touche_bateau)
                self.g.ajoute(touche_bateau)
                self.afficher_bateau_coule(touche_bateau)
                if len(self.bateaux_coules) != len(self.liste_bateaux):
                    message=f"🎯 Bravo ! Vous avez coulé le bateau {touche_bateau.marque} ! "
                    if self.diff == 'Z':
                        self.coups -= 5
                        message += "(5 coups supplimentaires)"
                        jouer_son("bonus", volume=0.7)

                    elif self.diff == 'A':
                        self.coups -= 1
                        message += "(1 coup supplimentaire)"
                        jouer_son("bonus", volume=0.7)              
                    self.message_label.config(text=message, fg="#00ff00")
      
            else:
                self.boutons_grille[(ligne, colonne)].config(text='💣', bg='#e74c3c', state='disabled', relief=tk.SUNKEN)
                self.message_label.config(text="🔥 Touché ! Continuez...", fg="#ff9900")
                self.bateaux_touches.append(touche_bateau)
        else:
            self.g.tirer(ligne, colonne)
            self.boutons_grille[(ligne, colonne)].config(text='X', bg='#34495e', state='disabled', relief=tk.SUNKEN)
            jouer_son("miss", volume=0.5)
            self.message_label.config(text="💧 Plouf ! Dans l'eau...", fg="#00d4ff")
        
        if self.diff in ['A', 'Z']:
            positions_occupees = list(self.cases_deja_tirees) + [pos for b_temps in self.bateaux_touches for pos in b_temps.positions if pos not in self.cases_deja_tirees]
            for b in self.liste_bateaux:
                if b not in self.bateaux_touches and b not in self.bateaux_coules:
                    b.position_alea(self.g, positions_occupees)
                    positions_occupees.extend(b.positions)

        self.coups_label.config(text=f"Coups: {self.coups}/{self.max_coups if self.max_coups < 80 else '∞'}")
        self.bateaux_label.config(text=f"Bateaux coulés: {len(self.bateaux_coules)}/{len(self.liste_bateaux)}")

        self.verifier_fin_partie()
    
    def afficher_bateau_coule(self, bateau):
        for ligne, colonne in bateau.positions:
            if (ligne, colonne) in self.boutons_grille:
                self.boutons_grille[(ligne, colonne)].config(text=bateau.marque, bg="#55EB64", state='disabled', fg='white', relief=tk.SUNKEN)
    
    def verifier_fin_partie(self):
        if len(self.bateaux_coules) == len(self.liste_bateaux):
            self.partie_en_cours = False
            self.gerer_victoire()
        elif self.coups >= self.max_coups:
            self.partie_en_cours = False
            self.gerer_defaite()
    
    def gerer_victoire(self):
        message = f"🏁 Félicitations !\nTous les bateaux ont été détruits !\n\nNombre de coups : {self.coups}"
        
        best = self.scores.get(self.diff)
        if best is None or self.coups < best:
            self.scores[self.diff] = self.coups
            save_highscores(self.scores)
            message += f"\n\n🏆 Nouveau record pour {self.difficultes[self.diff]['nom']} !"
        
        arreter_musique()
        jouer_son("victory", volume=0.8)        
        messagebox.showinfo("🎉 Victoire !", message)    
        if self.diff == 'A':
            self.gagne += 1
            if self.gagne == 2 and 'Z' not in self.difficultes:
                self.difficultes["Z"] = {
                    "nom": "Extrême",
                    "desc": "Grille plus grande, repositionnement et 40 coups maximum, 5 bateaux !"
                }
                jouer_son("unlock", volume=0.8)
                messagebox.showinfo("Déblocage !", "🎉 Vous avez débloqué la difficulté EXTRÊME !")
    
    def gerer_defaite(self):
        self.gagne = 0
        if 'Z' in self.difficultes:
            del self.difficultes['Z']
        arreter_musique()
        jouer_son("defeat", volume=0.7)
        messagebox.showwarning("GAME OVER", f"❌ Game Over ! Vous avez épuisé vos {self.max_coups} coups.")
        
        for b in self.liste_bateaux:
            if b not in self.bateaux_coules:
                self.g.ajoute(b)
                for ligne, colonne in b.positions:
                    if (ligne, colonne) in self.boutons_grille:
                        self.boutons_grille[(ligne, colonne)].config(text=b.marque, bg="#f02525")
        for (ligne, colonne) in self.boutons_grille:
            self.boutons_grille[(ligne, colonne)].config(state='disabled')                
    

root = tk.Tk()
app = BatailleNavaleGUI(root)
root.mainloop()