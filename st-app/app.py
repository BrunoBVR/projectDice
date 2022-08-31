import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

import streamlit as st

st.title("Playing dice!")

# np.random.seed(28)

# Start of form to get initial values

# Choose number of dice to roll
with st.sidebar:
    with st.form("my_form"):
        ND = st.slider("Number of dice:", 1, 5, 2, 1)

        # Choose number of dice rolls
        N = st.slider("Initial number of rolls:", 10, 100, 20, 10)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit Initial Conditions")

# Delete all the items in Session state when submitting new initial conditions
if submitted:
    for key in st.session_state.keys():
        del st.session_state[key]


# "Roll" those ND dice and store their value and their sum.
# The array 'dice_rolls' will store all results with a size (N, ND).
# The array 'dice_sum' will be an N dimensional array with the sum of each collective dice roll.
# dice_rolls = np.random.randint(1, 7, size=(N, ND))
# dice_sum = np.sum(dice_rolls, axis=1)

if "dice_rolls" not in st.session_state:
    st.session_state.dice_rolls = np.random.randint(1, 7, size=(N, ND))

if "count" not in st.session_state:
    st.session_state.count = 0

dice_sum = np.sum(st.session_state.dice_rolls, axis=1)

col1, col2 = st.columns([1, 3])

with col1:
    # We want to give the user the option to roll a dice again and append the result to 'dice_rolls'
    if st.button("New roll"):
        new_roll = np.random.randint(1, 7, size=(1, ND))
        st.session_state.count += 1

        for i in range(ND):
            image = Image.open(f"st-app/dice_faces_hd/{new_roll[0][i]}.png")
            st.image(image)

        # Appending new roll to stack of rolls
        st.session_state.dice_rolls = np.append(
            st.session_state.dice_rolls, new_roll, axis=0
        )

        # Updating the sum
        dice_sum = np.sum(st.session_state.dice_rolls, axis=1)

with col2:
    # Showing the histogram
    st.subheader(
        f"Sum of rolled dice: {ND} dice - {N + st.session_state.count} dice rolls"
    )

    hist_values, bin_edges = np.histogram(
        dice_sum, bins=6 * ND - ND + 1, range=(ND, 6 * ND)
    )

    data = pd.DataFrame({"sum": list(range(ND, 6 * ND + 1)), "counts": hist_values})

    st.bar_chart(data, x="sum", y="counts")

    # fig = plt.figure(figsize=(10, 8))
    # sns.barplot(data=data, x="sum", y="counts")
    # plt.xlabel("Dice Sum", fontsize=22)
    # plt.ylabel("Frequency", fontsize=22)
    # st.pyplot(fig)

# Plotting individual die data
# Creating a dataframe wih dice_rolls for plotting
cols = []
for c in range(1, ND + 1):
    cols.append(f"D{c}")

rolls_data = pd.DataFrame(st.session_state.dice_rolls, columns=cols)

# Plotting individual dice distribution
ind_cols = st.columns(ND)

st.subheader("Individual die results distribution")

for i, c in enumerate(ind_cols):
    with c:
        st.caption(f"D{i+1}")
        hist_values = np.histogram(rolls_data[f"D{i+1}"], bins=6, range=(1, 6))[0]
        data = pd.DataFrame({"side": list(range(1, 7)), "counts": hist_values})

        st.bar_chart(data, x="side", y="counts")
