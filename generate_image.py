import matplotlib.pyplot as plt
import numpy as np

# 1. Définition des données
# On commence très près de 0 (0.005) pour montrer l'asymptote sans erreur mathématique
x = np.linspace(0.005, 4, 1000) 
y = 2*x + 1 - np.log(x)

# 2. Création du graphique
plt.figure(figsize=(10, 6))

# Tracer la fonction f(x)
plt.plot(x, y, label=r'$f(x) = 2x + 1 - \ln(x)$', color='blue', linewidth=2)

# Tracer l'asymptote verticale (x=0)
plt.axvline(x=0, color='red', linestyle='--', label='Asymptote verticale (x=0)')

# Optionnel : Marquer le minimum (x=0.5)
x_min = 0.5
y_min = 2*x_min + 1 - np.log(x_min)
plt.plot(x_min, y_min, 'go', label=f'Minimum ({x_min}, {y_min:.2f})')

# 3. Mise en forme
plt.title("Courbe de la fonction $f(x) = 2x + 1 - \ln(x)$")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()

# Ajuster les limites pour bien voir la courbe (l'asymptote monte très haut)
plt.ylim(0, 10)
plt.xlim(-0.5, 4.5)

# 4. Enregistrer l'image
nom_fichier = 'courbe_fonction.jpg'
plt.savefig(nom_fichier, dpi=300)
print(f"L'image a été enregistrée sous le nom : {nom_fichier}")
