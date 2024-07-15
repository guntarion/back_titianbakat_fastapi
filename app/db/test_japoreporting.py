import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.japoreporting import retrieve_kombinasi_yang_utama, retrieve_kombinasi_non_utama


def test_retrieve_kombinasi_yang_utama():
    kombinasi_jari = input("Enter kombinasiJariUtama: ")
    result = retrieve_kombinasi_yang_utama(kombinasi_jari)

    if result:
        print("Result found:")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("No results found")


def test_retrieve_kombinasi_non_utama():
    kombinasi_jari = input("Enter kombinasiJariNonUtama: ")
    result = retrieve_kombinasi_non_utama(kombinasi_jari)

    if result:
        print("Result found:")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("No results found")


if __name__ == "__main__":
    test_retrieve_kombinasi_yang_utama()
    # test_retrieve_kombinasi_non_utama()
