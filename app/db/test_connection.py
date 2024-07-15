from japoreporting import retrieve_kombinasi_yang_utama

if __name__ == "__main__":
    kombinasi_jari = "loop_loop_whorl_arch"  # Replace with a valid value
    result = retrieve_kombinasi_yang_utama(kombinasi_jari)
    if result:
        print("Result found:")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("No results found")
