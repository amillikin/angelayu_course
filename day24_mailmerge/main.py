NAME_PLACEHOLDER = "[name]"

try:
    with open("./Input/Names/invited_names.txt",
              mode="r",
              encoding="UTF-8") as reader:
        name_list = reader.readlines()
except FileNotFoundError:
    print("invited_names.txt not found.")

try:
    with open("./Input/Letters/starting_letter.txt",
              mode="r",
              encoding="UTF-8") as reader:
        letter_body = reader.read()
        for name in name_list:
            name_stripped = name.strip()
            filled_letter = letter_body.replace(NAME_PLACEHOLDER, name_stripped)
            try:
                with open(f"./Output/ReadyToSend/letter_for_{name_stripped}.txt",
                          mode="w",
                          encoding="UTF-8") as writer:
                    writer.write(filled_letter)
            except IOError:
                pass
except FileExistsError:
    print("starting_letter.txt not found.")
