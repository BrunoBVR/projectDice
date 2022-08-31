import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(28)

# Choose number of dice to roll
ND = 5

# Choose number of dice rolls
N = 5

# "Roll" those ND dice and store their value and their sum
# The array 'dice_rolls' will store all results with a size (N, ND).
# The array 'dice_sum' will be an N dimensional array with the sum of each collective dice roll
dice_rolls = np.random.randint(1, 7, size=(N, ND))
dice_sum = np.sum(dice_rolls, axis=1)

# We want to give the user the option to roll a dice again and append the result to 'dice_rolls'
new_roll = np.random.randint(1, 7, size=(1, ND))

# Appending new roll to stack of rolls
dice_rolls = np.append(dice_rolls, new_roll, axis=0)

# Printing the sum, including new roll
dice_sum = np.sum(dice_rolls, axis=1)

# Creating a dataframe wih dice_rolls for plotting
cols = []
for c in range(1, ND + 1):
    cols.append(f"D{c}")

data = pd.DataFrame(dice_rolls, columns=cols)
data_sum = pd.DataFrame(dice_sum, columns=["sum"])

# Plotting individual dice distribution
fig, ax = plt.subplots(nrows=1, ncols=ND, figsize=(12, 4))

for i, die in enumerate(cols):
    sns.histplot(data=data, x=die, label=die, kde=True, ax=ax[i])
    ax[i].legend()

plt.legend()
plt.tight_layout()
plt.savefig("test.png")

# Plotting sum histrogram
plt.clf()
plt.figure(figsize=(6, 4))
sns.histplot(data=data_sum, x="sum", label="Sum", kde=True)
plt.legend()
plt.tight_layout()
plt.savefig("hist_test.png")
