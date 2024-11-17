# import packages
import numpy as np 
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import streamlit as st
import time

# prepare data
df = pd.read_csv('nasa.csv')

# train models
@st.cache_data
def train_models(df):

    label_encoder = LabelEncoder()
    df.apply(LabelEncoder().fit_transform)

    X = df[['Relative Velocity km per hr', 'Inclination', 'Eccentricity']]
    
    # miss distance (km) decision tree
    y = df[['Miss Dist.(kilometers)']].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    dtree_missdist = DecisionTreeClassifier()
    dtree_missdist.fit(X_train,y_train)

    # absolute magnitude (km) decision tree
    y = df[['Absolute Magnitude']].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    dtree_mag = DecisionTreeClassifier()
    dtree_mag.fit(X_train,y_train)

    return dtree_missdist, dtree_mag

def run_asteroids():
    dtree_missdist, dtree_mag = train_models(df)

    if 'section' not in st.session_state:
        st.session_state.section = 'story'

    # story
    if st.session_state.section == 'story':
        st.title("Asteroid Attack")
        st.image("https://images.vexels.com/content/301767/preview/space-kawaii-alien-cartoon-character-e54455.png")
        # Story Section 1
        st.write("""
        Welcome evil alien scientist! You are from the planet Zorkon-9, and your goal is to destroy Earth.
        Using your advanced alien technology, you can launch asteroids toward Earth by setting their
        relative velocity, inclination, and eccentricity. But beware—Earth's defenses are monitoring
        these parameters, and you must carefully aim to hit Earth and maximize destruction.
        """)

        # Story Section 2
        st.write("""
        Choose your asteroid's parameters carefully:
        - **Relative Velocity**: The speed at which the asteroid travels.
        - **Inclination**: The angle of the asteroid's trajectory relative to Earth's equatorial plane.
        - **Eccentricity**: How elongated the asteroid's orbit is.
        """)

        # Launch Prompt
        st.write("""
        Are you ready to unleash destruction on Earth? Press the button below to learn more about asteroid parameters!
        """)

    
        

        if st.button("Asteroids 101"):
            st.session_state.section = 'asteroids'
        
        
    elif st.session_state.section == 'asteroids':
        st.title("Relative Velocity")
        st.markdown("""
    - **Affects the trajectory of the asteroid and the time it takes to pass Earth.**
    - **Higher relative velocity generally results in shorter interaction times, reducing gravitational deflection.**
    """)
        st.title("Eccentricity")
        st.markdown("""
    - **Describes the shape of the orbit.**
    - **e = 0 : Circular orbit**
    - **0 < e < 1 : Elliptical orbit**
    - **e = 1 : Parabolic orbit**
    - **e > 1 : Hyperbolic escape trajectory**
        """)
        st.title("Inclination")
        st.markdown("""
    - **The angle between the asteroid's orbital plane and Earth's orbital plane.**
    - **Higher inclination generally means the asteroid is less likely to cross Earth's path, increasing miss distance.**
    """)
        if st.button("Launch Asteroid!"):
            st.session_state.section = 'inputs'

    elif st.session_state.section == 'inputs':

        # user inputs
        relative_velocity = st.number_input("Relative Velocity: ")
        inclination = st.number_input("Inclination: ")
        eccentricity = st.number_input("Eccentricity: ")


        if relative_velocity != 0 and inclination != 0 and eccentricity != 0:
            # model predictions
            X_user = [[relative_velocity, inclination, eccentricity]]
            abs_mag = dtree_mag.predict(X_user)
            miss_dist = dtree_missdist.predict(X_user)

            st.write("Launching . . .")
            st.write("Your asteroid was this far from earth: ", str(abs_mag[0]), " km.")
            # classify asteroid risk
            if abs_mag < 16 and miss_dist < 7500:
                st.write("You have accomplished your mission, evil scientist! Your asteroid was on point and shattered the Earth into pieces! You are crowned emporer of the alien race!")
                st.image("https://dailygalaxy.com/wp-content/uploads/2024/09/Could-a-Nuclear-Explosion-Redirect-an-Asteroid-New-Research-Says-Yes.jpg")
            elif abs_mag < 16 and miss_dist < 50000:
                st.write("Impressive, evil scientist! Your asteroid has caused mass destruction throughout the North American continent! It is a blow the humans will never recover from!")
                st.image("https://i0.wp.com/newspaceeconomy.ca/wp-content/uploads/2024/06/newspaceeconomy_picture_of_an_asteroid_striking_earth_cinematic_66f0fde4-b492-478a-8815-e063ac2ec0dd-1.png?w=1024&quality=80&ssl=1")
            elif 16 <= abs_mag < 22 and miss_dist < 100000:
                st.write("Hmmf. Not too bad, evil scientist. But, your asteroid has only scared the little humans and sailed through Earth's orbit. DO BETTER.")
                st.image("https://c02.purpledshub.com/uploads/sites/48/2024/06/chances-asteroid-hitting-earth.jpg?w=1880&webp=1")
            elif abs_mag >= 22 and miss_dist < 384400: 
                st.write("You have failed your mission, evil scientist! The asteroid you launched has barely touched Earth's orbit.")
                st.image("https://images.indianexpress.com/2024/09/asteroid-hitting-earth_32e2f4.jpg?w=640")
            elif abs_mag >= 25 or miss_dist >= 7500000:
                st.write("You have failed your mission, evil scientist! The asteroid you launched has harmlessly sailed past Earth.")
                st.image("https://images.indianexpress.com/2024/09/asteroid-hitting-earth_32e2f4.jpg?w=640")
            else:
                st.write("You have failed your mission, evil scientist! The asteroid you launched has harmlessly sailed past Earth.")
                st.image("https://images.indianexpress.com/2024/09/asteroid-hitting-earth_32e2f4.jpg?w=640")
                
        if st.button("Asteroids 101"):
            st.session_state.section = 'asteroids'

run_asteroids()

if st.button("Another fun game!"):
    st.write("[The roles reverse . . . click here to turn back human and protect your planet from alien invasions!](https://replit.com/join/bbcgxuqkvh-sayanapudi)")
