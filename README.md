# Programmation Orientée Objet en C et C++

## Description globale

Ce module a pour objectif d’introduire la programmation orientée objet (POO) en partant des bases du langage C, puis en évoluant progressivement vers C++, langage orienté objet par excellence.
Il permet de comprendre comment la programmation structurée mène naturellement à la programmation orientée objet.

## Description du module

Révision des concepts fondamentaux du C (pointeurs, structures, fonctions, gestion mémoire)

Transition vers la POO avec C++

Concepts clés en C++ : classes, objets, encapsulation, héritage, polymorphisme, etc.

Mise en pratique via des exercices et projets

## Exécution

Compiler un fichier C++ :

```bash
g++ main.cpp -o programme
```

 Exécuter :

```bash
./programme
```

Assure-toi d’avoir un compilateur C/C++ installé (comme gcc/g++ ou clang).

## Version

v1.0.0 

## Licence

MIT License

## Auteur

Raouf Nechmi


# Projet Bataille Navale en Python 🚢
## Description globale
Ce projet est l'Évaluation Finale du module, visant à mettre en œuvre les meilleures pratiques de développement logiciel abordées, à savoir : la programmation orientée objet (POO) en Python, l'utilisation d'un environnement virtuel, le contrôle de version (SCM) et la mise en place de tests unitaires.

Le projet consiste à créer une version du jeu classique de la Bataille Navale.

## Fonctionnalités et Organisation du Projet
Le projet intègre les éléments suivants :

Programmation Orientée Objet (POO) : Utilisation de classes et d'objets pour modéliser le plateau de jeu, les navires, les joueurs, etc.

Environnement Virtuel : Isolation des dépendances du projet.

Tests Unitaires : Utilisation de pytest pour garantir la fiabilité du code.

Contrôle de Source (SCM) : Suivi des modifications via Git avec des commits réguliers.


## Exécution
Pour exécuter le jeu et lancer les tests, suivez les étapes ci-dessous.

1. Cloner le Dépôt
```bash
git clone <https://github.com/raoufne/projet-bataille-navale>
cd bataille-navale-python
```
2. Configurer l'Environnement Virtuel
Il est fortement recommandé d'utiliser un environnement virtuel.

```bash
# Créer l'environnement virtuel (nommé 'venv' ici)
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate  # Sous Linux/macOS
# ou
.\venv\Scripts\activate  # Sous Windows PowerShell
```

3. Installer les Dépendances
Les dépendances se trouvent dans requirements.txt.

```bash
pip install -r requirements.txt
```

4. Exécuter le Jeu
Une fois l'environnement activé et les dépendances installées, exécutez le script principal :

```bash
python3 main.py
```

5. Lancer les Tests
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