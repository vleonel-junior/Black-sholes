import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.stats import norm
from scipy.special import erfc
from mpl_toolkits.mplot3d import Axes3D

# Paramètres du modèle
E = 100  # Prix d'exercice
r = 0.06  # Taux d'intérêt sans risque (6%)
sigma = 0.3  # Volatilité (30%)
T = 1.0  # Maturité en années

# Fonction N(x) - répartition de la loi normale standard
def N(x):
    return norm.cdf(x)


# Définition de k  
def k_value(r, sigma):
    return ((2 * r) / (sigma**2))

# Fonction de calcul du prix d'option Call selon votre formulation
def custom_call_model(S, t):
    if T - t <= 0:
        return np.maximum(S - E, 0)  # À l'échéance
    
    k = k_value(r, sigma)
    
    term1_arg = (np.log(S/E) / (sigma * np.sqrt(T-t))) - ((k+1) * sigma * np.sqrt(T-t))
    term2_arg = (np.log(S/E) / (sigma * np.sqrt(T-t))) - ((k-1) * sigma * np.sqrt(T-t))
    
    term1 = (S/E) * N(term1_arg)
    term2 = (np.exp(-r*(T-t))/2) * N(term2_arg)
    
    return (term1 - term2)  # Formule de Black-Scholes

# Création des grilles de données
S_values = np.linspace(0, 200, 20)  # Valeurs de S entre 0 et 200
t_values = np.linspace(0, 0.99, 20)  # Valeurs de t entre 0 et 0.99 (près de T)
S_grid, t_grid = np.meshgrid(S_values, t_values)

# Calcul des prix d'options pour chaque combinaison (S,t)
C_values = np.zeros_like(S_grid)
for i in range(len(t_values)):
    for j in range(len(S_values)):
        C_values[i, j] = custom_call_model(S_values[j], t_values[i])

# Création du graphique 3D
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Surface 3D
surf = ax.plot_surface(S_grid, t_grid, C_values, cmap='viridis',
                       linewidth=0, antialiased=True, alpha=0.8)

# Étiquettes et titre
ax.set_xlabel('S', fontsize=12)
ax.set_ylabel('t/T', fontsize=12)
ax.set_zlabel('C', fontsize=12)
ax.set_title('Prix de l\'option Call en fonction de S et t (E=100, r=6%, σ=0,3)', fontsize=14)

# Ajout d'une barre de couleur
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
cbar.set_label('Prix de l\'option', fontsize=12)

# Ajuster la vue
ax.view_init(elev=30, azim=-130)

plt.tight_layout()
plt.show()