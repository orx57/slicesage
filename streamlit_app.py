import streamlit as st
import pandas as pd
import altair as alt
from math import ceil

# Titre de l'application
st.title("SliceSage 🌱")

# Menu de navigation dans la barre latérale
menu = st.sidebar.radio(
    "Navigation",
    ("Calculateur Simple", "Calculateur Avancé")
)

# Affichage du contenu en fonction de la sélection du menu
if menu == "Calculateur Simple":
    st.header("Calculateur Simple")
    st.write("Bienvenue dans le calculateur simple. Ici, vous pouvez estimer rapidement le coût de vos impressions 3D.")

    # Texte explicatif pour l'utilisateur
    st.write("Ce calculateur estime le coût de production en se basant sur une estimation des moyennes du prix du kilogramme de filament, "
             "de la consommation d'énergie de l'impression, et du prix du kWh.")
    
    # Entrée pour le temps d'impression en minutes avec une description
    temps_impression = st.number_input(
        "Temps d'impression (en minutes)",
        min_value=0,
        step=1,
        help="Entrez le temps total d'impression en minutes."
    )

    # Entrée pour le filament utilisé en grammes avec une description
    filament_utilise = st.number_input(
        "Filament utilisé (en grammes)",
        min_value=0,
        step=1,
        help="Entrez la quantité de filament utilisé en grammes."
    )

    # Calcul simple (exemple)
    if st.button("Calculer le coût"):
        # Exemple de calcul : coût fictif basé sur le temps et le filament
        cout_energie = temps_impression * 120 * 0.2516 / 60 / 1000  # Pour 120 Watts et au prix moyen du kWh en France en octobre 2024
        cout_filament = filament_utilise * 0.0198  # Coût par gramme moyen en France en 2024
        cout_total = cout_energie + cout_filament

        st.write(f"Coût estimé de l'impression : {cout_total:.2f} €")

elif menu == "Calculateur Avancé":
    st.header("Calculateur Avancé")
    st.write("Bienvenue dans le calculateur avancé. Utilisez cet outil pour des estimations plus détaillées.")

    # Texte explicatif pour l'utilisateur
    st.write("Utilisez les **Paramètres Ajustables** dans la barre de gauche pour personnaliser votre calcul. "
             "Cela vous permet de prendre en compte des variables telles que le coût du filament, la coût de l'énergie, "
             "et d'autres facteurs influençant le coût de production.")

    # Saisie des données utilisateur avec des descriptions
    temps_impression = st.number_input(
        "Temps d'impression (en minutes)",
        min_value=0,
        step=1,
        help="Entrez le temps total d'impression en minutes."
    )
    filament_utilise = st.number_input(
        "Filament utilisé (en grammes)",
        min_value=0,
        step=1,
        help="Entrez la quantité de filament utilisé en grammes."
    )

    # Paramètres ajustables avec des descriptions
    st.sidebar.header("Paramètres Ajustables")
    cout_filament_kg = st.sidebar.number_input(
        "Coût du filament par kg (€)",
        value=26.21,
        help="Entrez le coût du filament par kilogramme."
    )
    marge_filament = st.sidebar.number_input(
        "Marge du filament (%)",
        value=5.0,
        help="Entrez la marge appliquée au coût du filament."
    )
    consommation_electrique = st.sidebar.number_input(
        "Consommation électrique (watts)",
        value=120,
        help="Entrez la consommation électrique de l'imprimante en watts."
    )
    cout_kwh = st.sidebar.number_input(
        "Coût par kWh (€)",
        value=0.27,
        help="Entrez le coût de l'électricité par kilowattheure."
    )
    cout_main_oeuvre_h = st.sidebar.number_input(
        "Coût horaire de la main-d'œuvre (€)",
        value=11.88,
        help="Entrez le coût horaire de la main-d'œuvre."
    )
    temps_pretraitement = st.sidebar.number_input(
        "Temps de prétraitement (minutes)",
        value=5,
        help="Entrez le temps de prétraitement en minutes."
    )
    temps_posttraitement = st.sidebar.number_input(
        "Temps de post-traitement (minutes)",
        value=5,
        help="Entrez le temps de post-traitement en minutes."
    )
    cout_machine = st.sidebar.number_input(
        "Coût de la machine (€)",
        value=452.77,
        help="Entrez le coût total de la machine."
    )
    duree_amortissement = st.sidebar.number_input(
        "Durée d'amortissement (années)",
        value=3,
        help="Entrez la durée d'amortissement de la machine en années."
    )
    utilisation_journaliere = st.sidebar.number_input(
        "Utilisation quotidienne de la machine (heures)",
        value=2,
        help="Entrez le nombre d'heures d'utilisation quotidienne de la machine."
    )
    cout_maintenance = st.sidebar.number_input(
        "Coût de maintenance (%)",
        value=5,
        help="Entrez le pourcentage de coût de maintenance annuel."
    )
    autres_couts = st.sidebar.number_input(
        "Autres coûts (€)",
        value=0,
        help="Entrez tout autre coût supplémentaire."
    )
    marge_beneficiaire = st.sidebar.number_input(
        "Marge bénéficiaire (%)",
        value=40.0,
        help="Entrez la marge bénéficiaire souhaitée."
    )
    tva = st.sidebar.number_input(
        "TVA (%)",
        value=20.0,
        help="Entrez le taux de TVA applicable."
    )

    # Calculs
    if st.button("Calculer"):
        # Convertir le temps en heures
        minutes_machine = temps_impression
        temps_main_oeuvre = temps_pretraitement + temps_posttraitement
        
        # Coût de la machine
        cout_machine_reel = cout_machine + cout_machine / 100 * cout_maintenance
        couts_machine = cout_machine_reel / duree_amortissement / 365 / utilisation_journaliere / 60 * minutes_machine
        
        # Coût de l'énergie
        couts_energie = minutes_machine * consommation_electrique * cout_kwh / 60 / 1000
        
        # Coût du filament
        filament_utilise_total = ceil(filament_utilise + filament_utilise / 100 * marge_filament)
        couts_filament = filament_utilise_total * cout_filament_kg / 1000
        
        # Coût de la main-d'œuvre
        couts_main_oeuvre = temps_main_oeuvre / 60 * cout_main_oeuvre_h
        
        # Somme de tous les coûts
        tous_les_couts = couts_main_oeuvre + couts_filament + couts_energie + couts_machine + autres_couts
        
        # Marge et taxes
        marge = tous_les_couts / 100 * marge_beneficiaire
        net = tous_les_couts + marge
        taxe = net / 100 * tva
        cout_total = net + taxe

        # Affichage des coûts
        st.write(f"Coût estimé de l'impression : {tous_les_couts:.2f} €")
        st.write(f"Prix total : {cout_total:.2f} €")

        # Préparation des données pour le tableau
        resultats = {
            "Description": [
                "Coût de la Main-d'œuvre", "Coût d'Amortissement de la Machine", "Coût du Filament", 
                "Coût de l'Énergie", "Autres Coûts", "Somme de Tous les Coûts", 
                "Marge Bénéficiaire", "Total Net", "Taxe", "Total Brut"
            ],
            "Montant (€)": [
                f"{couts_main_oeuvre:.2f}", f"{couts_machine:.2f}", f"{couts_filament:.2f}", 
                f"{couts_energie:.2f}", f"{autres_couts:.2f}", f"{tous_les_couts:.2f}", 
                f"{marge:.2f}", f"{net:.2f}", f"{taxe:.2f}", f"{cout_total:.2f}"
            ],
            "Pourcentage (%)": [
                int((couts_main_oeuvre / cout_total) * 100), int((couts_machine / cout_total) * 100), 
                int((couts_filament / cout_total) * 100), int((couts_energie / cout_total) * 100), 
                int((autres_couts / cout_total) * 100), int((tous_les_couts / cout_total) * 100), 
                int((marge / cout_total) * 100), int((net / cout_total) * 100), 
                int((taxe / cout_total) * 100), 100
            ]
        }

        # Affichage du tableau sans numéros de ligne
        df_resultats = pd.DataFrame(resultats)
        st.dataframe(df_resultats, hide_index=True)

        # Création du graphique avec Altair
        df_chart = pd.DataFrame({
            "Description": resultats["Description"][:-1],  # Exclure "Brut"
            "Montant (€)": [float(val) for val in resultats["Montant (€)"][:-1]]
        })

        chart = alt.Chart(df_chart).mark_bar().encode(
            x=alt.X('Montant (€):Q', title='Montant (€)'),
            y=alt.Y('Description:N', sort='-x', title=''),
            tooltip=['Description', 'Montant (€)']
        ).properties(
            title='Répartition des coûts'
        )

        # Affichage du graphique
        st.altair_chart(chart, use_container_width=True)

st.caption(
    """Auteur : orx57 ([GitHub](https://github.com/orx57)) · Octobre 2024
    """
)
