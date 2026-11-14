import pandas as pd
import requests

# import geopandas
# import matplotlib
# import seaborn
# import scipy
from dotenv import load_dotenv
import os

load_dotenv()

"""Fetches ACS 2020-2024 tables B16004 and B18102 for King County tracts."""

CENSUS_URL = "https://api.census.gov/data/2024/acs/acs5"
GEO_PARAMS = {"for": "tract:*", "in": "state:53 county:033"}

LANGUAGE_VARS = [
    "B16004_046E",
    "B16004_050E",
    "B16004_051E",
    "B16004_052E",
    "B16004_060E",
    "B16004_061E",
    "B16004_062E",
]
ALL_HEARING_VARS = ["B18102_015E", "B18102_018E", "B18102_034E", "B18102_037E"]
HEARING_DIFFICULTY_VARS = ["B18102_016E", "B18102_019E",
                           "B18102_035E", "B18102_038E"]


def get_acs(variables: list[str], key: str) -> pd.DataFrame:
    """Requests the given ACS variables for every King County tract
    and returns a DataFrame with a GEOID column for merging."""
    params = {"get": "NAME," + ",".join(variables), "key": key, **GEO_PARAMS}
    # Unpacks the GEO_PARAMS variable, allows for cleaner and reusable code
    # Below code requests CENSUS_URL with environment variable key
    # Creates the GEOID necessary to compare with the TIGER data
    response = requests.get(CENSUS_URL, params=params)
    response.raise_for_status()
    rows = response.json()
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df["GEOID"] = df["state"] + df["county"] + df["tract"]
    return df


key = os.environ.get("CENSUS_API_KEY").strip()
lang = get_acs(LANGUAGE_VARS, key)
hearing = get_acs(ALL_HEARING_VARS + HEARING_DIFFICULTY_VARS, key)
os.makedirs("data", exist_ok=True)
lang.to_csv("data/b16004_raw.csv", index=False)
hearing.to_csv("data/b18102_raw.csv", index=False)
# Verify shapes
print("B16004:", lang.shape, "B18102:", hearing.shape)
# prints (495, 9) and (495, 13) respectively
