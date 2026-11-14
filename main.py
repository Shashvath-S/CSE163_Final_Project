"""
Runs the files in order of this project
"""

import download_acs
import clean_data
import test_data
import test_cleaned_data
import create_plots
import validity


def main():
    print("1. Fetch and Download data")
    download_acs.main()
    print("2. Clean data")
    clean_data.main()
    print("3. Test Cleaning Logic of data")
    test_cleaned_data.main()
    print("4. Test Data against Hand Picked data")
    test_data.main()
    print("5. Create Plots")
    create_plots.main()
    print("6. Check Validity of data")
    validity.main()


if __name__ == "__main__":
    main()
