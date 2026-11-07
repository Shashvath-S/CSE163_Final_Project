import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

tracts = gpd.read_file("data/cleaned_tracts.gpkg")

print(tracts["Spanish_limited_percent"].describe())
print(tracts["AAPI_limited_percent"].describe())
print(tracts["hearing_difficulty_percent"].describe())


fig, ax = plt.subplots()

sns.scatterplot(data=tracts, x="Spanish_limited_percent", y="hearing_difficulty_percent", ax=ax)
ax.set_xlabel("Spanish Limited English (%)")
ax.set_ylabel("Hearing Difficulty (%)")
ax.set_title("Hearing Difficulty vs. Spanish Limited English")
fig.savefig("plots/spanish_vs_hearing.png")

fig, ax = plt.subplots()

sns.scatterplot(data=tracts, x="AAPI_limited_percent", y="hearing_difficulty_percent", ax=ax)
ax.set_xlabel("AAPI Limited English (%)")
ax.set_ylabel("Hearing Difficulty (%)")
ax.set_title("Hearing Difficulty vs. Spanish Limited English")
fig.savefig("plots/AAPI_vs_hearing.png")

fig, ax = plt.subplots()

tracts.plot(column="hearing_difficulty_percent", ax=ax, legend=True, cmap="OrRd")
ax.set_title("Hearing Difficulty among adults 65+ in King County, Washington")
ax.set_axis_off()
fig.savefig("plots/hearing_map.png")