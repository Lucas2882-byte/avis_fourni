# 🏢 Avis Fournisseurs

Application Streamlit de gestion d'avis pour fournisseurs - Identique à l'application principale avec des identifiants personnalisés.

## 🔐 Identifiants de connexion

Cette application dispose de deux comptes utilisateurs :

- **Fournisseur 1**
  - Nom d'utilisateur : `fourni1`
  - Mot de passe : `avisfourni1!`

- **Fournisseur 2**
  - Nom d'utilisateur : `fourni2`
  - Mot de passe : `avisfourni2!`

## ✨ Fonctionnalités

Cette application est une copie complète de l'application `gestion-fiches-main` avec toutes ses fonctionnalités :

- **Gestion des fiches** : Création, modification et suppression de fiches
- **Catégories multiples** : Support de différentes catégories de services
- **Gestion des avis** : Système complet de gestion des textes d'avis
- **Dashboard** : Suivi global des avis par jour et par utilisateur
- **Carte des fiches** : Répartition géographique des fiches par localité
- **Backfill automatique** : Calcul automatique des prochains avis
- **Synchronisation GitHub** : Upload/download automatique des bases de données

## 🗃️ Bases de données

L'application utilise trois bases de données SQLite :

1. **comptes.db** : Comptes utilisateurs (fourni1 et fourni2)
2. **fiches.db** : Données des fiches par catégorie
3. **fiches_final.db** : Textes des avis

## 📊 Interface

L'interface comprend plusieurs sections :

1. **Page de connexion** : Authentification avec les identifiants fournis
2. **Section Admin** : Gestion des catégories, backfill, et dashboard
3. **Gestion des fiches** : Ajout, modification, suppression de fiches
4. **Gestion des avis** : Gestion des textes d'avis par catégorie
5. **Interface utilisateur** : Sélection de localité et traitement des fiches

## 🚀 Lancement

L'application se lance automatiquement avec Streamlit sur le port 5000.

## 💡 Notes importantes

- Les mots de passe sont hashés avec SHA-256
- L'interface utilise un thème sombre personnalisé
- Les bases de données sont synchronisées automatiquement avec GitHub (si configuré)
