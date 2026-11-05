import geopandas as gpd
import pandas as pd

LANGUAGE_PATH = "data/b16004_raw.csv"
HEARING_PATH = "data/b18102_raw.csv"
TIGER_PATH = "data/tl_2024_53_tract/tl_2024_53_tract.shp"
OUTPUT_PATH = "data/cleaned_tracts.gpkg"
MIN_POPULATION_SIZE = 100

LANGUAGE_ALL = "B16004_046E"

SPANISH_LIMITED = ["B16004_050E", "B16004_051E", "B16004_052E"]

ASIAN_PACFIC_LIMITED = ["B16004_060E", "B16004_061E", "B16004_062E"]

ALL_HEARING_VARS = ["B18102_015E", "B18102_018E",
                    "B18102_034E", "B18102_037E"]

HEARING_DIFFICULTY_VARS = ["B18102_016E", "B18102_019E",
                           "B18102_035E", "B18102_038E"]


def remove_missing_data(df, columns):
    for column in columns:
        df = df[df[column] >= 0]
    return df


def clean_language_data(df):
    all_languages = df[LANGUAGE_ALL]
    spanish = df[SPANISH_LIMITED].sum(axis=1)
    asian_pacific = df[ASIAN_PACFIC_LIMITED].sum(axis=1)

    final_df = pd.DataFrame()
    final_df["GEOID"] = df["GEOID"]
    final_df["language_total_65"] = all_languages
    final_df["Spanish_limited_percent"] = (spanish / all_languages) * 100
    final_df["AAPI_limited_percent"] = (asian_pacific / all_languages) * 100
    return final_df


def clean_hearing_data(df):
    all_hearing = df[ALL_HEARING_VARS].sum(axis=1)
    hearing_difficulty = df[HEARING_DIFFICULTY_VARS].sum(axis=1)

    final_df = pd.DataFrame()
    final_df["GEOID"] = df["GEOID"]
    final_df["hearing_total_65"] = all_hearing
    final_df["hearing_difficulty_percent"] = (hearing_difficulty
                                              / all_hearing) * 100
    return final_df


language_raw_data = pd.read_csv(LANGUAGE_PATH, dtype={"GEOID": str})
# read GEOID as string to prevent leading zeros from being deleted
hearing_raw_data = pd.read_csv(HEARING_PATH, dtype={"GEOID": str})

print("Raw Language data length: ", len(language_raw_data))
print("Raw Hearing data length: ", len(hearing_raw_data))


all_language_columns = [LANGUAGE_ALL] + SPANISH_LIMITED + ASIAN_PACFIC_LIMITED
all_hearing_coulmns = ALL_HEARING_VARS + HEARING_DIFFICULTY_VARS

language_data = remove_missing_data(language_raw_data, all_language_columns)
hearing_data = remove_missing_data(hearing_raw_data, all_hearing_coulmns)

print("After removal of missing data language: ", len(language_data))
print("After removal of missing data hearing: ", len(hearing_data))

cleaned_language_data = clean_language_data(language_data)
cleaned_hearing_data = clean_hearing_data(hearing_data)


acs = cleaned_language_data.merge(cleaned_hearing_data, on="GEOID")

acs = acs[(acs["language_total_65"] >= MIN_POPULATION_SIZE)
          & (acs["hearing_total_65"] >= MIN_POPULATION_SIZE)]
print("After removing tracts with population less than "
      + str(MIN_POPULATION_SIZE) + ": ", len(acs))

tracts = gpd.read_file(TIGER_PATH)
tracts = tracts[tracts["COUNTYFP"] == "033"]
tracts = tracts[["GEOID", "geometry"]]
merge_tiger_acs = tracts.merge(acs, on="GEOID")

merge_tiger_acs.to_file(OUTPUT_PATH, driver="GPKG")
