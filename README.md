# Projet Bataille Navale en Python 🚢

## Description globale

Ce projet est l'**Évaluation Finale** du module, visant à mettre en œuvre les meilleures pratiques de développement logiciel abordées : la **programmation orientée objet (POO)** en Python, l'utilisation d'un **environnement virtuel**, le **contrôle de version (SCM)**, et la mise en place de **tests unitaires**.

Il en résulte une version complète et interactive du jeu classique de la **Bataille Navale**, disponible en plusieurs interfaces.

---

## 🎲 Principe du Jeu

Le but est de **couler quatre types de bateaux** placés aléatoirement sur la grille. Le jeu prend en charge un système de **High Score** et différentes **difficultés**.

### Les Navires
Quatre bateaux doivent être coulés :

| Navire | Longueur | Marqueur |
| :--- | :--- | :--- |
| **Porte-avions** | 4 | `🚢` |
| **Croiseur** | 3 | `⛴` |
| **Torpilleur** | 2 | `🚣` |
| **Sous-marin** | 2 | `🐟` |

### Niveaux de Difficulté
Le jeu propose trois niveaux de difficulté qui affectent le nombre de coups et la mécanique du jeu :

| Difficulté | Nom | Description |
| :--- | :--- | :--- |
| **C** | Facile | Grille standard, 4 bateaux, coups illimités. |
| **B** | Moyen | Grille standard, 4 bateaux, **40 coups maximum**. |
| **A** | Difficile | Grille standard, 4 bateaux, **40 coups maximum**. **Les bateaux se repositionnent aléatoirement après chaque tir manqué (plouf)**, rendant la traque très ardue. |

> **EASTER EGG :** Si vous maîtrisez la difficulté **Difficile**, quelque chose d'excitant pourrait vous attendre ! 😉

---

## 🛠️ Fonctionnalités et Organisation

### Architecture du Projet
Le projet est architecturé autour de la POO, permettant une gestion modulaire de la Grille et des Bateaux. Il intègre un système de **placement aléatoire sécurisé** et une gestion des **High Scores** stockés dans le répertoire `data/`.

### Interfaces Utilisateur (UI)
Afin d'explorer différentes librairies et environnements, le jeu est disponible en trois versions :

1.  **Terminal Standard (`main_v1.py`)** : Version simple basée sur l'invite de commande standard.
2.  **PyTermGUI (`main_v2.py`)** : Interface pseudo-graphique dans le terminal.
    > *Note :* Initialement instable pour la gestion des entrées utilisateur sur Windows (faute du module), cette version a été principalement développée et testée dans un environnement Linux.
3.  **Tkinter (`main_v3.py`)** : L'interface la plus avancée. Elle intègre des **effets sonores** et utilise uniquement la **souris** pour interagir avec la grille, sans aucune saisie au clavier.
    > *Note :* Cette version a été développée après des problèmes de stabilité avec PyTermGUI, mais elle pourrait présenter des instabilités sur certains environnements Unix/macOS (faute du module).

### Outils et Pratiques
* **Environnement Virtuel** : Isolation des dépendances.
* **Tests Unitaires** : Utilisation de **`pytest`** pour garantir la fiabilité du code.
* **Contrôle de Source (SCM)** : Suivi des modifications via Git avec des commits réguliers.

---

## 🚀 Exécution

Pour exécuter le jeu et lancer les tests, suivez les étapes ci-dessous.

### 1. Cloner le Dépôt

```bash

git clone https://github.com/raoufne/projet-bataille-navale

cd bataille-navale-python

```

### 2. Configurer l'Environnement Virtuel

Il est fortement recommandé d'utiliser un environnement virtuel.



```bash

# Créer l'environnement virtuel (nommé 'venv' ici)

python -m venv venv



# Activer l'environnement virtuel

source venv/bin/activate  # Sous Linux/macOS

# ou

.\venv\Scripts\activate  # Sous Windows PowerShell

```



### 3. Installer les Dépendances

Les dépendances se trouvent dans requirements.txt.



```bash

pip install -r requirements.txt

```

Pour MacOS il faut aussi :

```bash

brew install python3-tk
brew install python-tk

```

Pour Linux il faut aussi :

```bash

sudo apt install fonts-noto-color-emoji

sudo apt-get install python3-tk
sudo apt-get install python-tk

```

### 4. Exécuter le Jeu

Une fois l'environnement activé et les dépendances installées, exécutez le script principal :



```bash

python launcher.py

```



### 5. Lancer les Tests

Assurez-vous que l'environnement virtuel est activé et que pytest est installé (via requirements.txt).



```bash

pytest

```



## Version

v1.0.0



## Licence

MIT License



## Auteur

Raouf Nechmi