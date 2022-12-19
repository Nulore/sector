from databank import databank
import stringer
import time
import os

debug = True

def log(value: object):
    if debug:
        print(value)

def main():
    start = time.process_time()

    for bank_key in databank.keys():
        bank = databank[bank_key]

        cur_path = os.path.dirname(__file__)

        if not os.path.exists("build"):
            os.makedirs("build")
            log("build/ non-existent, creating.")
        
        new_path = os.path.relpath(f'.\\build\\{bank_key}.md', cur_path)
        
        if not os.path.exists(new_path):
            open(new_path, "x")
            log(f"created new file {bank_key}.md")

        with open(new_path, "w") as file:
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