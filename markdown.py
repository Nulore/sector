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
        for data_key in bank.keys():
            if bank_key == "faction":
                log(stringer.anti_ansi(stringer.faction(data_key)))
            if bank_key == "weapon":
                log(stringer.anti_ansi(stringer.weapon(data_key)))
            if bank_key == "species":
                log(stringer.anti_ansi(stringer.species(data_key)))
        
    end = time.process_time()

    print(f"finished in {end - start}s")

if __name__ == "__main__":
    main()