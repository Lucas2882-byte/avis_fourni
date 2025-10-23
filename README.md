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

L'application utilise trois bases de données SQLite :

1. **fiches.db** : Base de données des fiches (copie en lecture seule)
   - Contient toutes les tables `fiches_*` avec les informations des fiches
   - **Important** : Cette base doit être incluse dans le dépôt Git

2. **comptes_fournisseurs.db** : Stocke les comptes des fournisseurs (générée automatiquement)
   - Table `fournisseurs` : id, nom_utilisateur, mot_de_passe_hash
   - Créée automatiquement au premier lancement

3. **avis_fournisseurs.db** : Stocke les avis donnés par les fournisseurs (générée automatiquement)
   - Table `avis_fiches` : id, fiche_id, table_name, fournisseur_id, avis_text, note, date_avis
   - Contrainte unique : Un fournisseur ne peut donner qu'un seul avis par fiche
   - Créée automatiquement au premier lancement

## 🔗 Structure autonome

L'application est complètement autonome et contient sa propre copie de la base de données des fiches. Les bases de données des comptes et des avis sont générées automatiquement lors du premier lancement et ne doivent pas être versionnées (elles sont dans .gitignore).

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
