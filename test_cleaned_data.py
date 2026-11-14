import pandas as pd
from clean_data import clean_language_data, clean_hearing_data
import numpy as np


def build_language_row(geoid, total, l50, l51, l52, l60, l61, l62):
    return {
        "GEOID": geoid,
        "B16004_046E": total,
        "B16004_050E": l50,
        "B16004_051E": l51,
        "B16004_052E": l52,
        "B16004_060E": l60,
        "B16004_061E": l61,
        "B16004_062E": l62,
    }


def build_hearing_row(geoid, h15, h18, h34, h37, h16, h19, h35, h38):
    return {
        "GEOID": geoid,
        "B18102_015E": h15,
        "B18102_018E": h18,
        "B18102_034E": h34,
        "B18102_037E": h37,
        "B18102_016E": h16,
        "B18102_019E": h19,
        "B18102_035E": h35,
        "B18102_038E": h38,
    }


def main():
    custom_language_df = pd.DataFrame(
        [
            build_language_row("53033032221", 622, 0, 0, 0, 32, 0, 0),
            build_language_row("53033008900", 882, 26, 229, 165, 1, 2, 35),
            build_language_row("53033009100", 957, 0, 0, 0, 105, 43, 549),
            build_language_row("53033007405", 102, 0, 0, 0, 0, 0, 0),
        ]
    )

    custom_hearing_df = pd.DataFrame(
        [
            build_hearing_row("53033032221", 200, 61, 224, 137, 6, 10, 0, 0),
            build_hearing_row("53033008900", 371, 135, 170, 126,
                              17, 103, 16, 15),
            build_hearing_row("53033009100", 134, 260, 387, 166, 0, 28, 0, 50),
            build_hearing_row("53033007405", 24, 0, 19, 59, 0, 0, 19, 0),
        ]
    )

    result_df = clean_language_data(custom_language_df).merge(
        clean_hearing_data(custom_hearing_df), on="GEOID"
    )

    expected_result = {
        "53033032221": (0.0, (32 / 622) * 100, (16 / 622) * 100),
        "53033008900": (((420 / 882) * 100, (38 / 882) * 100,
                        (151 / 802) * 100)),
        "53033009100": (0.0, (697 / 957) * 100, (78 / 947) * 100),
        "53033007405": (0.0, 0.0, (19 / 102) * 100),
    }

    for geoid, (Spanish, AAPI, hearing_percent) in expected_result.items():
        row = result_df[result_df["GEOID"] == geoid].iloc[0]
        assert np.isclose(row["Spanish_limited_percent"], Spanish)
        assert np.isclose(row["AAPI_limited_percent"], AAPI)
        assert np.isclose(row["hearing_difficulty_percent"], hearing_percent)

    print("All tests passed!")


if __name__ == "__main__":
    main()
