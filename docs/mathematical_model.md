
# Modèle Mathématique pour l'Optimisation des Horaires de Transport Public

## 1. Ensembles et Indices

- B : Ensemble des bus, indexé par _b_
- S : Ensemble des arrêts, indexé par _s_
- T : Ensemble des périodes temporelles, indexé par _t_
- R : Ensemble des routes possibles, indexé par r

## 2. Paramètres

- c_b : Capacité du bus b
- **d_{s,t}** : Demande à l'arrêt _s_ pendant la période t
- tt_{s1,s2} : Temps de trajet entre les arrêts _s1_ et _s2_
- m_b : Temps de maintenance minimal requis pour le bus _b_
- [t^{min}_s, t^{max}_s] : Fenêtre temporelle de service pour l'arrêt s
- w_{max} : Temps d'attente maximum acceptable

## 3. Variables de Décision

x_{b,s,t} = {
    1 si le bus b dessert l'arrêt s au temps t
    0 sinon
}

y_{b,r} = {
    1 si le bus b est assigné à la route r
    0 sinon
}

w_{s,t} : Temps d'attente à l'arrêt s au temps t

## 4. Fonction Objectif

Minimiser Z = ∑_{s∈S} ∑_{t∈T} w_{s,t} × d_{s,t}

## 5. Contraintes

### 5.1 Contraintes de Capacité
∑_{b∈B} x_{b,s,t} × c_b ≥ d_{s,t}  ∀s∈S, ∀t∈T

### 5.2 Contraintes de Temps de Trajet
x_{b,s1,t1} + x_{b,s2,t2} ≤ 1  
∀b∈B, ∀s1,s2∈S, ∀t1,t2∈T où |t2-t1| < tt_{s1,s2}

### 5.3 Contraintes de Maintenance
∑_{s∈S} ∑_{t∈[t',t'+m_b]} x_{b,s,t} = 0  
∀b∈B, ∀t'∈T où un service de maintenance est requis

### 5.4 Contraintes de Fenêtre Temporelle
x_{b,s,t} = 0  ∀b∈B, ∀s∈S, ∀t∉[t^{min}_s, t^{max}_s]

### 5.5 Contraintes de Temps d'Attente Maximum
w_{s,t} ≤ w_{max}  ∀s∈S, ∀t∈T

### 5.6 Contraintes de Conservation du Flux
∑_{r∈R} y_{b,r} ≤ 1  ∀b∈B

## 6. Complexité

Ce problème est NP-difficile car il combine plusieurs aspects complexes :
- Problème de routage de véhicules (VRP)
- Planification avec contraintes temporelles
- Optimisation multi-objectif (temps d'attente, utilisation des ressources)

## 7. Approche de Résolution

La résolution utilise cinq métaheuristiques :
1. Recuit Simulé (RS)
2. Algorithme Génétique (AG)
3. Recherche Taboue (RT)
4. Optimisation par Colonies de Fourmis (ACO)
5. Optimisation par Essaim Particulaire (PSO)

Chaque méthode sera appliquée avec les paramètres spécifiques définis dans l'implémentation.