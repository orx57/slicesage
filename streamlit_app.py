import streamlit as st

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
    
    # Entrée pour le temps d'impression en minutes
    temps_impression = st.number_input("Temps d'impression (en minutes)", min_value=0, step=1)

    # Entrée pour le filament utilisé en grammes
    filament_utilise = st.number_input("Filament utilisé (en grammes)", min_value=0.0, step=0.1)

    # Calcul simple (exemple)
    # Vous pouvez ajouter des calculs ici pour estimer le coût basé sur les entrées
    if st.button("Calculer le coût"):
        # Exemple de calcul : coût fictif basé sur le temps et le filament
        cout_temps = temps_impression * 0.05  # Coût par minute
        cout_filament = filament_utilise * 0.02  # Coût par gramme
        cout_total = cout_temps + cout_filament

        st.write(f"Coût estimé de l'impression : {cout_total:.2f} €")

elif menu == "Calculateur Avancé":
    st.header("Calculateur Avancé")
    st.write("Bienvenue dans le calculateur avancé. Utilisez cet outil pour des estimations plus détaillées.")
    # Code pour le calculateur avancé ici

# Vous pouvez ajouter d'autres sections au menu à l'avenir