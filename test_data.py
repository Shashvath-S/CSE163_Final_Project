import geopandas as gpd
import pandas as pd
from clean_data import (
    LANGUAGE_PATH,
    HEARING_PATH,
    TIGER_PATH,
    OUTPUT_PATH,
    MIN_POPULATION_SIZE,
    LANGUAGE_ALL,
    SPANISH_LIMITED,
    ASIAN_PACFIC_LIMITED,
    ALL_HEARING_VARS,
    HEARING_DIFFICULTY_VARS,
)


def pick_high_tracts(cleaned_data):
    random_tract = cleaned_data["GEOID"].iloc[0]
    high_spanish_tract = cleaned_data.sort_values(
        "Spanish_limited_percent", ascending=False
    )["GEOID"].iloc[0]
    high_AAPI_tract = cleaned_data.sort_values("AAPI_limited_percent", ascending=False)[
        "GEOID"
    ].iloc[0]
    near_min_pop_cutoff = cleaned_data.sort_values("language_total_65", ascending=True)[
        "GEOID"
    ].iloc[0]
    return [random_tract, high_spanish_tract, high_AAPI_tract, near_min_pop_cutoff]


def show_tract_data(geoid, language_raw_df, hearing_raw_df, cleaned_data):
    language_geoid_row = language_raw_df[language_raw_df["GEOID"] == geoid]
    hearing_geoid_row = hearing_raw_df[hearing_raw_df["GEOID"] == geoid]
    cleaned_geoid_row = cleaned_data[cleaned_data["GEOID"] == geoid]

    print("GEOID: ", geoid)
    print("LANGUAGE")
    print(language_geoid_row[[LANGUAGE_ALL] + SPANISH_LIMITED + ASIAN_PACFIC_LIMITED])
    print("HEARING")
    print(hearing_geoid_row[HEARING_DIFFICULTY_VARS + ALL_HEARING_VARS])
    print("CLEANED DATA")
    print(
        cleaned_geoid_row[
            [
                "Spanish_limited_percent",
                "AAPI_limited_percent",
                "hearing_difficulty_percent",
                "language_total_65",
            ]
        ]
    )
    print()


def count_missing_data(df, columns):
    for column in columns:
        missing_data = df[df[column] < 0]
        print(column, " missing data: ", len(missing_data))


def main():
    language_raw_data = pd.read_csv(LANGUAGE_PATH, dtype={"GEOID": str})
    hearing_raw_data = pd.read_csv(HEARING_PATH, dtype={"GEOID": str})
    cleaned_data = gpd.read_file(OUTPUT_PATH)
    print(cleaned_data["GEOID"].dtype, cleaned_data["GEOID"].iloc[0])
    print(language_raw_data["GEOID"].dtype, language_raw_data["GEOID"].iloc[0])

    for geoid in pick_high_tracts(cleaned_data):
        show_tract_data(geoid, language_raw_data, hearing_raw_data, cleaned_data)

    count_missing_data(
        language_raw_data, [LANGUAGE_ALL] + SPANISH_LIMITED + ASIAN_PACFIC_LIMITED
    )
    count_missing_data(hearing_raw_data, ALL_HEARING_VARS + HEARING_DIFFICULTY_VARS)
    small_tracts = language_raw_data[
        language_raw_data[LANGUAGE_ALL] < MIN_POPULATION_SIZE
    ]
    print("Tracts under ", MIN_POPULATION_SIZE, " for language: ", len(small_tracts))

    tracts = gpd.read_file(TIGER_PATH)
    tracts = tracts[tracts["COUNTYFP"] == "033"]
    no_acs = tracts[~tracts["GEOID"].isin(cleaned_data["GEOID"])]
    print("King County TIGER tracts: ", len(tracts))
    print("TIGER tracts not in cleaned data", len(no_acs))


if __name__ == "__main__":
    main()
