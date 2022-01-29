import pandas

nato_alphabet = pandas.read_csv("./nato_phonetic_alphabet.csv")

nato_alphabet_dict = {row.letter:row.code for (index, row) in nato_alphabet.iterrows()}

def output_nato():
    response = input("Enter a word: ").upper()
    try: 
        nato_output = [nato_alphabet_dict[letter] for letter in response]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        output_nato()
    else:
        print(f"{nato_output}")

output_nato()
