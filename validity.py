import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from clean_data import OUTPUT_PATH

COLS = ["Spanish_limited_percent",
        "AAPI_limited_percent",
        "hearing_difficulty_percent"]


def plot_hist(df):
    for col in COLS:
        fig, ax = plt.subplots()
        sns.histplot(data=df, x=col, ax=ax)
        ax.set_title(f"Distribution of {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Number of Tracts")
        fig.savefig(f"plots/{col}_hist.png")
        plt.close(fig)


def zero_count(df):
    for col in COLS:
        zeros = df[df[col] == 0]
        print(f"{col} zeros: {len(zeros)}")


def tests(df, language_col):
    x = df[language_col]
    y = df["hearing_difficulty_percent"]
    pearson_corr = stats.pearsonr(x, y)
    spearman_corr = stats.spearmanr(x, y)
    print(f"Current: {language_col}")
    print(f"Pearson r = {pearson_corr[0]}, p = {pearson_corr[1]}")
    print(f"Spearman rho = {spearman_corr[0]}, p = {spearman_corr[1]}")


def main():
    df = gpd.read_file(OUTPUT_PATH)
    plot_hist(df)
    zero_count(df)
    print(df[COLS].skew())
    tests(df, "Spanish_limited_percent")
    tests(df, "AAPI_limited_percent")


if __name__ == "__main__":
    main()
