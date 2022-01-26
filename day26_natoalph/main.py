import pandas

nato_alphabet = pandas.read_csv("./nato_phonetic_alphabet.csv")

nato_alphabet_dict = {row.letter:row.code for (index, row) in nato_alphabet.iterrows()}

response = input("Enter a word: ").upper()

nato_output = [nato_alphabet_dict[letter] for letter in response]

print(f"{nato_output}")
