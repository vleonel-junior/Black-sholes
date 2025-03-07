import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.stats import norm
from mpl_toolkits.mplot3d import Axes3D

# Paramètres du modèle Black-Scholes
E = 100       # Prix d'exercice (strike price)
r = 0.06      # Taux d'intérêt sans risque annuel (6%)
sigma = 0.3   # Volatilité annuelle du sous-jacent (30%)
T = 1.0       # Échéance en années (1 an)

# Fonction N(x) - fonction de répartition de la loi normale centrée réduite
def N(x):
    """Calcule la fonction de répartition de la loi normale standard N(0,1)"""
    return norm.cdf(x)

# Fonction n(x) - densité de probabilité de la loi normale centrée réduite
def n(x):
    """Calcule la fonction de densité de la loi normale standard N(0,1)"""
    return (1/np.sqrt(2*np.pi)) * np.exp(-0.5*x**2)

# Calcul du paramètre k selon la définition fournie
def k_value(r, sigma):
    """Calcule la valeur du paramètre k selon la formule k = 2r/σ²"""
    return (2 * r) / (sigma**2)

# Fonction pour calculer le Delta de l'option Call selon la formule exacte
def call_delta(S, t):
    """
    Calcule le Delta (δ = ∂C/∂S) d'une option call européenne selon la formule:
    δ = (1/E)·N(d₁) + (1/(E·σ·√(T-t)))·n(d₁) - (e^(-r·(T-t))/(2·S·σ·√(T-t)))·n(d₂)
    
    Paramètres:
    -----------
    S : float
        Prix du sous-jacent
    t : float
        Temps actuel (0 ≤ t ≤ T)
        
    Retourne:
    ---------
    float
        Valeur du Delta
    """
    
    # Calcul du paramètre k
    k = k_value(r, sigma)
    
    # Temps restant jusqu'à l'échéance (tau)
    tau = T - t
    
    # Calcul des arguments d₁ et d₂
    d1 = (np.log(S/E) / (sigma * np.sqrt(tau))) - ((k+1) * sigma * np.sqrt(tau))
    d2 = (np.log(S/E) / (sigma * np.sqrt(tau))) - ((k-1) * sigma * np.sqrt(tau))
    
    # Calcul des trois termes de l'expression du delta
    term1 = (1/E) * N(d1)                                  # Premier terme avec N(d₁)
    term2 = (1/(E*sigma*np.sqrt(tau))) * n(d1)             # Deuxième terme avec n(d₁)
    term3 = (np.exp(-r*tau)/(2*S*sigma*np.sqrt(tau))) * n(d2)  # Troisième terme avec n(d₂)
    
    # Delta complet = somme des termes (selon la formule fournie)
    delta = term1 + term2 - term3
        
    return delta

# Création d'une grille de données pour la visualisation
# Plage de prix du sous-jacent centrée autour du prix d'exercice
S_values = np.linspace(0, 200, 20)  

# Plage temporelle évitant t=0 et t=T pour prévenir les singularités numériques
t_values = np.linspace(0.01, 0.99, 20)  

# Création des maillages pour la représentation 3D
S_grid, t_grid = np.meshgrid(S_values, t_values)

# Calcul des valeurs du delta pour chaque point de la grille
delta_values = np.zeros_like(S_grid)
for i in range(len(t_values)):
    for j in range(len(S_values)):
        delta_values[i, j] = call_delta(S_values[j], t_values[i])

# Visualisation 3D
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Surface 3D représentant le Delta
surf = ax.plot_surface(S_grid, t_grid, delta_values, cmap='viridis',
                      linewidth=0, antialiased=True, alpha=0.8)

# Paramètres du graphique
ax.set_xlabel('S', fontsize=12)
ax.set_ylabel('t/T', fontsize=12)
ax.set_zlabel('δ', fontsize=12)
ax.set_title('Delta (δ) de l\'option Call en fonction de S et t\n(E=100, r=6%, σ=0.3)', fontsize=14)

# Barre de couleur pour la représentation des valeurs
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=3)
cbar.set_label('Valeur du Delta (δ)', fontsize=12)

# Ajustement de l'angle de vue pour une meilleure visualisation
ax.view_init(elev=30, azim=-45)

# Optimisation de l'affichage
plt.tight_layout()
plt.show()