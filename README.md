# 🏢 Avis Fournisseurs

Application Streamlit permettant à deux fournisseurs de se connecter et de donner des avis sur les fiches du système principal.

## 📋 Fonctionnalités

### Pour les fournisseurs :
- **Authentification sécurisée** : Connexion avec nom d'utilisateur et mot de passe
- **Visualisation des fiches** : Parcourir toutes les fiches par catégorie
- **Système d'avis** : Donner une note (1-5 étoiles) et un commentaire sur chaque fiche
- **Modification des avis** : Possibilité de modifier ses propres avis
- **Consultation des avis** : Voir tous les avis des deux fournisseurs
- **Statistiques personnelles** : Suivi du nombre d'avis donnés et de la note moyenne

## 🔐 Comptes par défaut

L'application crée automatiquement deux comptes fournisseurs :

- **Fournisseur 1**
  - Nom d'utilisateur : `fournisseur1`
  - Mot de passe : `pass1`

- **Fournisseur 2**
  - Nom d'utilisateur : `fournisseur2`
  - Mot de passe : `pass2`

## 🗃️ Base de données

L'application utilise deux bases de données SQLite :

1. **comptes_fournisseurs.db** : Stocke les comptes des fournisseurs
   - Table `fournisseurs` : id, nom_utilisateur, mot_de_passe_hash

2. **avis_fournisseurs.db** : Stocke les avis donnés par les fournisseurs
   - Table `avis_fiches` : id, fiche_id, table_name, fournisseur_id, avis_text, note, date_avis
   - Contrainte unique : Un fournisseur ne peut donner qu'un seul avis par fiche

## 🔗 Lien avec l'application principale

L'application lit les fiches depuis la base de données de l'application principale (`gestion-fiches-main/fiches.db`) mais ne les modifie jamais. Elle crée uniquement ses propres avis dans sa base de données séparée.

## 📊 Interface

1. **Page de connexion** : Authentification du fournisseur
2. **Sélection de catégorie** : Choisir une catégorie de fiches
3. **Liste des fiches** : Affichage de toutes les fiches de la catégorie avec :
   - Informations sur la fiche (nom, description, localité)
   - Formulaire pour donner/modifier un avis
   - Liste de tous les avis des fournisseurs
4. **Statistiques** : Panneau de statistiques en bas de page

## 🚀 Utilisation

1. Se connecter avec un compte fournisseur
2. Sélectionner une catégorie dans la liste déroulante
3. Parcourir les fiches et donner des avis
4. Consulter les statistiques personnelles

## 💡 Caractéristiques techniques

- **Framework** : Streamlit
- **Base de données** : SQLite
- **Sécurité** : Mots de passe hashés avec SHA-256
- **Interface** : Thème sombre personnalisé
