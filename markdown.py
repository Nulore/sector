from databank import databank
import stringer
import time

debug = True

def log(value: object):
    if debug:
        print(value)

def main():
    start = time.process_time()

    for bank_key in databank.keys():
        bank = databank[bank_key]
        with open(f"{bank_key}.md", "w") as file:
            file.write(f"# {bank_key.capitalize()}s\n")
            for data_key in bank.keys():
                if bank_key == "faction":
                    message = stringer.anti_ansi(stringer.faction(data_key))
                    file.write(message + "\n\n")
                    log(message)

                if bank_key == "weapon":
                    message = stringer.anti_ansi(stringer.weapon(data_key))
                    file.write(message + "\n\n")
                    log(message)

                if bank_key == "species":
                    message = stringer.anti_ansi(stringer.species(data_key))
                    file.write(message + "\n\n")
                    log(message)

    end = time.process_time()

    print(f"finished in {end - start}s")

if __name__ == "__main__":
    main()