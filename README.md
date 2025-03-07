# Résolution de l'équation de Black-Scholes via la transformation en l'équation de la chaleur

## Introduction

L'équation de Black-Scholes (BS) est une équation aux dérivées partielles (EDP) fondamentale en finance, utilisée pour modéliser l'évolution du prix d'une option sur un marché financier. Dans sa version sans dividendes, pour une option européenne de type "call", elle s'écrit :

$$
\frac{\partial C}{\partial t} + \frac{\sigma^2 S^2}{2} \frac{\partial^2 C}{\partial S^2} + r S \frac{\partial C}{\partial S} - r C = 0
$$

où :
- $C = C(S, t)$ est le prix de l'option,
- $S$ est le prix de l'actif sous-jacent,
- $t$ est le temps,
- $r$ est le taux d'intérêt sans risque,
- $\sigma$ est la volatilité de l'actif.

Les conditions aux limites associées à une option européenne de type "call" sur l'intervalle de temps $[0, T]$ sont :

$$
\begin{cases}
C(0, t) = 0 & \forall t \in [0, T] \\
\lim_{S \to +\infty} (C(S, t) - S) = 0 & \forall t \in [0, T] \\
C(S, T) = \max \{ S - E, 0 \}
\end{cases}
$$

où $E$ est le prix d'exercice et $T$ est le temps d'expiration de l'option.

L'objectif est de résoudre cette EDP en la transformant en une forme plus simple, l'équation de la chaleur, qui bénéficie de solutions analytiques bien établies.

---

## Transformation de l'équation de Black-Scholes

### 1. Changement de variables

Pour simplifier l'équation de Black-Scholes et la rapprocher de l'équation de la chaleur, nous introduisons les substitutions suivantes :

$$
t = T - \frac{2\tau}{\sigma^2}, \quad x = \ln \left( \frac{S}{E} \right), \quad C(S, t) = E \tilde{C}(x, \tau)
$$

Ces changements permettent de reformuler les termes dépendant de $S$ et de travailler avec des coefficients constants.

### 2. Dérivation de l'équation transformée

En substituant ces variables dans l'équation initiale et en calculant les dérivées partielles, on obtient :

$$
\frac{\partial \tilde{C}}{\partial \tau} = \frac{\partial^2 \tilde{C}}{\partial x^2} + (k - 1) \frac{\partial \tilde{C}}{\partial x} - k \tilde{C}
$$

où $k = \frac{2r}{\sigma^2}$. Cette équation ressemble à l'équation de la chaleur, mais inclut des termes supplémentaires de convection et de réaction.

### 3. Passage à l'équation de la chaleur standard

Pour éliminer ces termes additionnels et obtenir l'équation de la chaleur classique, nous posons :

$$
\tilde{C}(x, \tau) = e^{\alpha x + \beta \tau} \hat{C}(x, \tau)
$$

Les constantes $\alpha$ et $\beta$ sont déterminées pour annuler les termes indésirables :

$$
\alpha = \frac{1 - k}{2}, \quad \beta = \alpha^2 + (k - 1) \alpha - k
$$

Après cette transformation, l'équation se réduit à :

$$
\frac{\partial \hat{C}}{\partial \tau} = \frac{\partial^2 \hat{C}}{\partial x^2}
$$

qui est l'équation de la chaleur standard.

### 4. Condition initiale

La condition finale $C(S, T) = \max \{ S - E, 0 \}$ devient une condition initiale pour $\hat{C}(x, 0)$ :

$$
\hat{C}(x, 0) = \max \left( e^{\frac{(k + 1) x}{2}} - e^{\frac{(k - 1) x}{2}}, 0 \right)
$$

---

## Solution analytique

La solution de l'équation de la chaleur avec cette condition initiale s'exprime par convolution avec le noyau de la chaleur :

$$
\hat{C}(x, \tau) = \frac{1}{\sqrt{4 \pi \tau}} \int_{-\infty}^{+\infty} \hat{C}(y, 0) e^{-\frac{(x - y)^2}{4 \tau}} \, dy
$$

En revenant aux variables originales et après simplification, on obtient une expression explicite pour $C(S, t)$, souvent exprimée à l'aide de la fonction de répartition de la loi normale standard $N$.

---

## Calcul du Delta

Le **delta** ($\delta$) d'une option est une mesure essentielle en finance, définie comme la dérivée partielle du prix de l'option par rapport au prix de l'actif sous-jacent :

$$
\delta = \frac{\partial C}{\partial S}
$$

Il indique la sensibilité du prix de l'option aux variations de $S$ et est crucial pour la gestion des risques, notamment dans la couverture delta.

### Expression du prix de l'option

Après résolution, le prix de l'option dans ce cadre s'écrit :

$$
C(S,t) = \frac{S}{E} N(d_1) - \frac{e^{-r(T - t)}}{2} N(d_2)
$$

où :

$$
d_1 = \frac{\ln\left(\frac{S}{E}\right)}{\sigma \sqrt{T - t}} - (k + 1) \sigma \sqrt{T - t}, \quad d_2 = \frac{\ln\left(\frac{S}{E}\right)}{\sigma \sqrt{T - t}} - (k - 1) \sigma \sqrt{T - t}
$$

avec $k = \frac{2r}{\sigma^2}$, $N(\cdot)$ la fonction de répartition de la loi normale standard, et $n(\cdot) = N'(\cdot)$ sa densité.

### Dérivation de $\delta$

En dérivant $C(S,t)$ par rapport à $S$ à l'aide des règles de dérivation (produit et chaîne), on obtient :

$$
\delta(S,t) = \frac{\partial C}{\partial S} = \frac{N(d_1)}{E} + \frac{n(d_1)}{E \sigma \sqrt{T - t}} - \frac{e^{-r(T - t)}}{2} \frac{n(d_2)}{S \sigma \sqrt{T - t}}
$$

Cette expression, plus complexe que le delta classique $N(d_1)$ du modèle Black-Scholes standard, reflète les ajustements issus des transformations spécifiques de ce projet.

---

## Conclusion

Ce travail illustre la transformation de l'équation de Black-Scholes en équation de la chaleur via des changements de variables et des substitutions. La solution analytique obtenue permet de calculer le prix d'une option européenne et de dériver des quantités clés comme le **delta** ($\delta$), indispensable pour la gestion des risques financiers. Ces techniques constituent une base robuste pour des applications en finance, telles que l'évaluation des options et la couverture delta.
