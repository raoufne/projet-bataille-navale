import pygame
import os

class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.sons_actifs = True
            self.sons = {}
            self.son_en_cours = None  
            self.musique_active = False
        except:
            self.sons_actifs = False
            print("⚠️ Pygame non disponible. Sons désactivés.")
    
    def charger_son(self, nom, fichier):
        if not self.sons_actifs:
            return
        try:
            if os.path.exists(fichier):
                self.sons[nom] = pygame.mixer.Sound(fichier)
        except:
            print(f"⚠️ Impossible de charger {fichier}")
    
    def jouer_son(self, nom, volume=1.0):
        if self.sons_actifs and nom in self.sons:
            try:
                if self.son_en_cours is not None:
                    self.son_en_cours.stop()
                
                self.sons[nom].set_volume(volume)
                self.sons[nom].play()
                
                self.son_en_cours = self.sons[nom]
            except:
                pass
    
    def arreter_sons(self):
        if self.sons_actifs and self.son_en_cours is not None:
            try:
                self.son_en_cours.stop()
                self.son_en_cours = None
            except:
                pass
    
    def jouer_musique(self, fichier, volume=0.5, boucle=True):
        if not self.sons_actifs:
            return
        try:
            if os.path.exists(fichier):
                pygame.mixer.music.load(fichier)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1 if boucle else 0)
                self.musique_active = True
        except:
            print(f"⚠️ Impossible de charger la musique {fichier}")
    
    def arreter_musique(self):
        if self.sons_actifs and self.musique_active:
            try:
                pygame.mixer.music.stop()
                self.musique_active = False
            except:
                pass
    
    def baisser_musique(self, volume=0.2):
        if self.sons_actifs and self.musique_active:
            try:
                pygame.mixer.music.set_volume(volume)
            except:
                pass
    
    def monter_musique(self, volume=0.5):
        if self.sons_actifs and self.musique_active:
            try:
                pygame.mixer.music.set_volume(volume)
            except:
                pass

sound_manager = SoundManager()

def initialiser_sons():
    sound_manager.charger_son("hit", "sounds/hit.wav")
    sound_manager.charger_son("bonus", "sounds/bonus.wav")
    sound_manager.charger_son("miss", "sounds/miss.wav")
    sound_manager.charger_son("error", "sounds/error.wav")
    sound_manager.charger_son("victory", "sounds/victory.wav")
    sound_manager.charger_son("defeat", "sounds/defeat.wav")
    sound_manager.charger_son("unlock", "sounds/unlock.wav")

def jouer_son(nom, volume=1.0):
    sound_manager.jouer_son(nom, volume)

def arreter_sons():
    sound_manager.arreter_sons()

def jouer_musique_menu():
    sound_manager.jouer_musique("sounds/menu_theme.mp3", volume=0.5, boucle=True)

def jouer_musique_jeu():
    sound_manager.baisser_musique(0.2)

def arreter_musique():
    sound_manager.arreter_musique()