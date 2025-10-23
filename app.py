import streamlit as st
st.set_page_config(page_title="Avis Fournisseurs", layout="wide")

# Initialisation session state
if "connecte" not in st.session_state:
    st.session_state.connecte = False
if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = None
if "fournisseur_id" not in st.session_state:
    st.session_state.fournisseur_id = None

import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import hashlib
import os

# Style général
theme_css = '''
<style>
    html, body, [data-testid="stApp"] {
        background-color: #0e1117 !important;
        color: white !important;
    }
    label, .stSelectbox label, .css-1cpxqw2 {
        color: white !important;
    }
    button[kind="secondary"] {
        color: white !important;
        background-color: #0e1117 !important;
        border: 1px solid #555 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }
    button[kind="secondary"]:hover {
        background-color: #1a1f25 !important;
        border-color: #888 !important;
    }
</style>
'''
st.markdown(theme_css, unsafe_allow_html=True)

# Fonctions d'authentification
def hasher_mot_de_passe(mdp):
    return hashlib.sha256(mdp.encode()).hexdigest()

def verifier_fournisseur(nom, mot_de_passe):
    conn = sqlite3.connect("comptes_fournisseurs.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT id, mot_de_passe_hash FROM fournisseurs WHERE nom_utilisateur = ?", (nom,))
    row = cursor.fetchone()
    conn.close()

    if row:
        fournisseur_id, hash_stocke = row
        if hasher_mot_de_passe(mot_de_passe) == hash_stocke:
            return True, fournisseur_id
    return False, None

# Initialisation des bases de données
def init_databases():
    # Base des comptes fournisseurs
    conn_comptes = sqlite3.connect("comptes_fournisseurs.db", check_same_thread=False)
    cursor_comptes = conn_comptes.cursor()
    
    cursor_comptes.execute("""
        CREATE TABLE IF NOT EXISTS fournisseurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_utilisateur TEXT UNIQUE,
            mot_de_passe_hash TEXT
        )
    """)
    
    # Créer deux fournisseurs par défaut si la table est vide
    cursor_comptes.execute("SELECT COUNT(*) FROM fournisseurs")
    if cursor_comptes.fetchone()[0] == 0:
        # Fournisseur 1: username "fournisseur1", password "pass1"
        # Fournisseur 2: username "fournisseur2", password "pass2"
        cursor_comptes.execute(
            "INSERT INTO fournisseurs (nom_utilisateur, mot_de_passe_hash) VALUES (?, ?)",
            ("fournisseur1", hasher_mot_de_passe("pass1"))
        )
        cursor_comptes.execute(
            "INSERT INTO fournisseurs (nom_utilisateur, mot_de_passe_hash) VALUES (?, ?)",
            ("fournisseur2", hasher_mot_de_passe("pass2"))
        )
    
    conn_comptes.commit()
    conn_comptes.close()
    
    # Base des avis fournisseurs
    conn_avis = sqlite3.connect("avis_fournisseurs.db", check_same_thread=False)
    cursor_avis = conn_avis.cursor()
    
    cursor_avis.execute("""
        CREATE TABLE IF NOT EXISTS avis_fiches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fiche_id INTEGER,
            table_name TEXT,
            fournisseur_id INTEGER,
            avis_text TEXT,
            note INTEGER,
            date_avis TEXT,
            UNIQUE(fiche_id, table_name, fournisseur_id)
        )
    """)
    
    conn_avis.commit()
    conn_avis.close()

# Initialiser les bases
init_databases()

# Connexion à la base des fiches (copie locale dans le même dossier)
conn_fiches = sqlite3.connect("fiches.db", check_same_thread=False)
cursor_fiches = conn_fiches.cursor()

# Connexion à la base des avis fournisseurs
conn_avis_fournisseurs = sqlite3.connect("avis_fournisseurs.db", check_same_thread=False)
cursor_avis_fournisseurs = conn_avis_fournisseurs.cursor()

# Charger les catégories depuis la base fiches
def charger_categories():
    cursor_fiches.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'fiches_%'")
    fiches_tables = [row[0] for row in cursor_fiches.fetchall()]
    
    category_map = {}
    for ft in fiches_tables:
        cat = ft.replace("fiches_", "").replace("_", " ").upper()
        category_map[cat] = ft
    
    return category_map

category_map = charger_categories()

# Interface principale
st.markdown("<h1 style='text-align:center;'>🏢 Avis Fournisseurs</h1>", unsafe_allow_html=True)

# Authentification
if not st.session_state.connecte:
    st.subheader("🔐 Connexion Fournisseur")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        nom = st.text_input("Nom d'utilisateur")
        mdp = st.text_input("Mot de passe", type="password")
        
        st.markdown("""
        <div style='background:#2c2f33;padding:14px;border-radius:10px;margin:10px 0;'>
            <p style='color:#9ca3af;font-size:13px;margin:0;'>
                ℹ️ <b>Comptes par défaut :</b><br>
                • Fournisseur 1 : <code>fournisseur1</code> / <code>pass1</code><br>
                • Fournisseur 2 : <code>fournisseur2</code> / <code>pass2</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Se connecter", use_container_width=True):
            valide, fournisseur_id = verifier_fournisseur(nom, mdp)
            if valide:
                st.session_state.connecte = True
                st.session_state.utilisateur = nom
                st.session_state.fournisseur_id = fournisseur_id
                st.success(f"Bienvenue {nom} 👋")
                st.rerun()
            else:
                st.error("Identifiants incorrects ❌")
    st.stop()

# Interface connectée
st.markdown(f"### 👤 Connecté en tant que : **{st.session_state.utilisateur}**")

col1, col2 = st.columns([5, 1])
with col2:
    if st.button("🚪 Déconnexion"):
        st.session_state.connecte = False
        st.session_state.utilisateur = None
        st.session_state.fournisseur_id = None
        st.rerun()

st.markdown("---")

# Sélection de catégorie
st.subheader("📁 Sélectionner une catégorie")
categories = list(category_map.keys())

if categories:
    categorie_selectionnee = st.selectbox("Catégorie", categories)
    table_name = category_map[categorie_selectionnee]
    
    st.markdown("---")
    
    # Récupérer toutes les fiches de cette catégorie
    cursor_fiches.execute(f"""
        SELECT id, nom_de_la_fiche, lien_fiche, bref_descriptif, localite 
        FROM {table_name}
        ORDER BY id
    """)
    fiches = cursor_fiches.fetchall()
    
    if fiches:
        st.subheader(f"📋 Fiches de la catégorie {categorie_selectionnee} ({len(fiches)} fiche(s))")
        
        for fiche in fiches:
            fiche_id, nom_fiche, lien_fiche, bref_descriptif, localite = fiche
            
            # Vérifier si le fournisseur a déjà donné un avis
            cursor_avis_fournisseurs.execute("""
                SELECT avis_text, note, date_avis 
                FROM avis_fiches 
                WHERE fiche_id = ? AND table_name = ? AND fournisseur_id = ?
            """, (fiche_id, table_name, st.session_state.fournisseur_id))
            
            avis_existant = cursor_avis_fournisseurs.fetchone()
            
            with st.expander(f"📄 {nom_fiche or f'Fiche #{fiche_id}'} - {localite or 'Sans localité'}", expanded=False):
                col_info, col_avis = st.columns([1, 1])
                
                with col_info:
                    st.markdown("#### 📝 Informations")
                    
                    if bref_descriptif:
                        st.markdown(f"""
                        <div style="background:#2c2f33;padding:12px;border-radius:8px;margin:8px 0;">
                            <div style="color:#9ca3af;font-size:11px;text-transform:uppercase;margin-bottom:4px;">
                                Description
                            </div>
                            <div style="color:#ffffff;font-size:13px;line-height:1.5;">
                                {bref_descriptif.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if lien_fiche:
                        st.markdown(f"🔗 [Voir la fiche]({lien_fiche})")
                
                with col_avis:
                    st.markdown("#### 💬 Votre avis")
                    
                    if avis_existant:
                        avis_text, note, date_avis = avis_existant
                        st.markdown(f"""
                        <div style="background:#1a472a;padding:12px;border-radius:8px;margin:8px 0;border-left:4px solid #10b981;">
                            <div style="color:#10b981;font-size:11px;text-transform:uppercase;margin-bottom:6px;">
                                ✅ Avis déjà donné le {date_avis}
                            </div>
                            <div style="color:#ffffff;font-size:13px;margin-bottom:8px;">
                                <b>Note :</b> {note}/5 ⭐
                            </div>
                            <div style="color:#ffffff;font-size:13px;line-height:1.5;">
                                {avis_text}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"✏️ Modifier l'avis", key=f"modifier_{table_name}_{fiche_id}"):
                            # Réinitialiser pour permettre modification
                            cursor_avis_fournisseurs.execute("""
                                DELETE FROM avis_fiches 
                                WHERE fiche_id = ? AND table_name = ? AND fournisseur_id = ?
                            """, (fiche_id, table_name, st.session_state.fournisseur_id))
                            conn_avis_fournisseurs.commit()
                            st.rerun()
                    
                    else:
                        # Formulaire pour donner un avis
                        note = st.slider(
                            "Note (1-5)", 
                            min_value=1, 
                            max_value=5, 
                            value=3,
                            key=f"note_{table_name}_{fiche_id}"
                        )
                        
                        avis_text = st.text_area(
                            "Votre commentaire",
                            placeholder="Donnez votre avis sur cette fiche...",
                            key=f"avis_{table_name}_{fiche_id}",
                            height=100
                        )
                        
                        if st.button(f"✅ Soumettre l'avis", key=f"submit_{table_name}_{fiche_id}"):
                            if avis_text.strip():
                                date_avis = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                cursor_avis_fournisseurs.execute("""
                                    INSERT OR REPLACE INTO avis_fiches 
                                    (fiche_id, table_name, fournisseur_id, avis_text, note, date_avis)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                """, (fiche_id, table_name, st.session_state.fournisseur_id, avis_text, note, date_avis))
                                
                                conn_avis_fournisseurs.commit()
                                st.success("✅ Avis enregistré avec succès !")
                                st.rerun()
                            else:
                                st.warning("⚠️ Veuillez écrire un commentaire")
                
                st.markdown("---")
                
                # Afficher les avis des deux fournisseurs
                st.markdown("#### 👥 Tous les avis")
                
                cursor_avis_fournisseurs.execute("""
                    SELECT f.nom_utilisateur, a.avis_text, a.note, a.date_avis
                    FROM avis_fiches a
                    JOIN fournisseurs f ON a.fournisseur_id = f.id
                    WHERE a.fiche_id = ? AND a.table_name = ?
                    ORDER BY a.date_avis DESC
                """, (fiche_id, table_name))
                
                tous_avis = cursor_avis_fournisseurs.fetchall()
                
                if tous_avis:
                    for nom_four, texte_avis, note_four, date_four in tous_avis:
                        couleur = "#1e40af" if nom_four == st.session_state.utilisateur else "#374151"
                        st.markdown(f"""
                        <div style="background:{couleur};padding:10px;border-radius:6px;margin:6px 0;">
                            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                                <span style="color:#ffffff;font-weight:bold;font-size:12px;">
                                    {nom_four}
                                </span>
                                <span style="color:#fbbf24;font-size:12px;">
                                    {"⭐" * note_four}
                                </span>
                            </div>
                            <div style="color:#d1d5db;font-size:11px;margin-bottom:6px;">
                                {date_four}
                            </div>
                            <div style="color:#ffffff;font-size:13px;">
                                {texte_avis}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Aucun avis pour le moment")
    
    else:
        st.info("📭 Aucune fiche dans cette catégorie")

else:
    st.warning("⚠️ Aucune catégorie disponible")

# Statistiques en bas de page
st.markdown("---")
st.subheader("📊 Mes statistiques")

col_stat1, col_stat2, col_stat3 = st.columns(3)

# Nombre total de fiches
total_fiches = 0
for table in category_map.values():
    cursor_fiches.execute(f"SELECT COUNT(*) FROM {table}")
    total_fiches += cursor_fiches.fetchone()[0]

# Nombre d'avis donnés par le fournisseur
cursor_avis_fournisseurs.execute("""
    SELECT COUNT(*) FROM avis_fiches WHERE fournisseur_id = ?
""", (st.session_state.fournisseur_id,))
mes_avis = cursor_avis_fournisseurs.fetchone()[0]

# Note moyenne
cursor_avis_fournisseurs.execute("""
    SELECT AVG(note) FROM avis_fiches WHERE fournisseur_id = ?
""", (st.session_state.fournisseur_id,))
note_moy = cursor_avis_fournisseurs.fetchone()[0]
note_moy = round(note_moy, 1) if note_moy else 0

with col_stat1:
    st.markdown(f"""
    <div style="background:#2c2f33;padding:20px;border-radius:10px;text-align:center;">
        <div style="font-size:32px;font-weight:bold;color:#3b82f6;">
            {total_fiches}
        </div>
        <div style="color:#9ca3af;font-size:14px;margin-top:8px;">
            Fiches totales
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown(f"""
    <div style="background:#2c2f33;padding:20px;border-radius:10px;text-align:center;">
        <div style="font-size:32px;font-weight:bold;color:#10b981;">
            {mes_avis}
        </div>
        <div style="color:#9ca3af;font-size:14px;margin-top:8px;">
            Avis donnés
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_stat3:
    st.markdown(f"""
    <div style="background:#2c2f33;padding:20px;border-radius:10px;text-align:center;">
        <div style="font-size:32px;font-weight:bold;color:#fbbf24;">
            {note_moy} ⭐
        </div>
        <div style="color:#9ca3af;font-size:14px;margin-top:8px;">
            Note moyenne
        </div>
    </div>
    """, unsafe_allow_html=True)
