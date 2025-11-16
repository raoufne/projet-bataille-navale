import importlib.util
import sys

versions = {
    "1": ("main_v1", "Version 1 - Terminal Simple"),
    "2": ("main2_v2", "Version 2 - Interface PyTermGUI"),
    "3": ("main_v3", "Version 3 - Interface Tkinter"),
}

print("\n⚓ BATAILLE NAVALE - Sélecteur de Version ⚓\n")
for key, (_, nom) in versions.items():
    print(f"[{key}] {nom}")

while True:
    choix = input("\nChoisissez une version (1, 2 ou 3) : ").strip()
    
    if choix in versions:
        module_name, nom = versions[choix]
        spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        print(f"\n▶️  Lancement de {nom}...\n")
        spec.loader.exec_module(module)
    else:
        print("❌ Choix invalide !")

