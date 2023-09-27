import csv
import random
import json
from tqdm import tqdm

def read_librispeech_ground_truth(input_csv_file):
  ground_truths = []

  with open(input_csv_file, "r") as input_csv:
    reader = csv.reader(input_csv)
    next(reader)

    for row in tqdm(reader):
      _, _, file_path, _, ground_truth = row
      ground_truth = ground_truth.lower()
      ground_truths.append(ground_truth)

  return ground_truths

# List of sentences to apply phonetic errors to
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "She sells seashells by the seashore.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
]

# Phonetic error rules
phonetic_rules = [
    "Substitute “th” sound",
    "Substitute “th” for “s”, “z”, “f”, or “v”",
    "Vowel Sound Confusion",
    "Similar Vowel Substitution",
    "Common Diphthong Confusion",
    "Short-Long Vowel Confusion",
    "Rhotic Vowel Confusion",
    "Front-Back Vowel Confusion",
    "Monophthong-Diphthong Confusion",
    "Flap-Tap Confusion",
]

# Function to apply a phonetic error to a word
def apply_phonetic_error(modified_word, error_rule):
  if "Substitute “th” sound" in error_rule:
    # Example: Replace "th" with "s"
    modified_word = modified_word.replace("th", "s")

  elif "Substitute “th” for “s”, “z”, “f”, or “v”" in error_rule:
    # Example: Replace "th" with "s", "z", "f", or "v"
    substitutes = {"s", "z", "f", "v"}
    modified_word = modified_word.replace("th", random.choice(list(substitutes)))

  elif "Vowel Sound Confusion" in error_rule:
    # Example: Replace "e" with "i" or "a" with "e"
    vowel_map = {"e": "i", "i": "e", "a": "e", "e": "a"}
    modified_word = "".join([vowel_map.get(char, char) for char in modified_word])

  elif "Similar Vowel Substitution" in error_rule:
    # Example: Replace "e" with "i" or "a" with "e"
    vowel_map = {"e": "i", "i": "e", "a": "e", "e": "a"}
    modified_word = "".join([vowel_map.get(char, char) for char in modified_word])

  elif "Common Diphthong Confusion" in error_rule:
    # Example: Replace "ei" with "i" or "ai" with "a"
    modified_word = modified_word.replace("ei", "i").replace("ai", "a")

  elif "Short-Long Vowel Confusion" in error_rule:
    # Example: Replace a short vowel with a long vowel of similar quality
    vowel_map = {"e": "ee", "i": "ee", "a": "aa", "o": "oo", "u": "oo"}
    modified_word = "".join([vowel_map.get(char, char) for char in modified_word])

  elif "Rhotic Vowel Confusion" in error_rule:
    # Example: Replace non-rhotic vowel with a similar-sounding rhotic vowel
    vowel_map = {"o": "aw", "aw": "o"}
    modified_word = "".join([vowel_map.get(char, char) for char in modified_word])

  elif "Front-Back Vowel Confusion" in error_rule:
    # Example: Replace a front vowel with a similar-sounding back vowel
    vowel_map = {"e": "a", "i": "u", "a": "e", "u": "i"}
    modified_word = "".join([vowel_map.get(char, char) for char in modified_word])

  elif "Monophthong-Diphthong Confusion" in error_rule:
    # Example: Replace a monophthong with a similar-sounding diphthong or vice versa
    diphthongs = {"ei": "i", "ai": "a", "ou": "oo", "oo": "ou"}
    modified_word = "".join([diphthongs.get(modified_word[i:i+2], modified_word[i:i+2]) if i < len(modified_word) - 1 else char for i, char in enumerate(modified_word)])

  elif "Flap-Tap Confusion" in error_rule:
    # Example: Replace a flap or tap with a different sound
    flap_tap_map = {"t": "d", "d": "t", "r": "l", "l": "r"}
    modified_word = "".join([flap_tap_map.get(char, char) for char in modified_word])

  return modified_word

# Apply phonetic errors to the list of sentences
sentences_with_errors = []
applied_errors = []
max_errors_per_sentence = 1  # Change this to set the maximum number of errors

# Choose phonetic errors for the whole sentence
sentences = read_librispeech_ground_truth("../../phonetic-error-corrector/librispeech_csv_files/dev-clean.csv")
print(f"Read {len(sentences)} sentences")

for sentence in sentences:
    words = sentence.split()
    num_errors = 0
    while num_errors < max_errors_per_sentence:
      chosen_rule = random.sample(phonetic_rules, max_errors_per_sentence)
      random_index = random.randint(0, len(words) - 1)
      random_word = words[random_index]
      modified_word = apply_phonetic_error(words[random_index], chosen_rule)
      if modified_word != random_word:
        num_errors += 1
        words[random_index] = modified_word
        applied_errors.append(chosen_rule)

    modified_sentence = " ".join(words)
    sentences_with_errors.append(modified_sentence)

# Print the sentences with errors
data = []
i = 0
for sentence, sentence_with_error, errors_for_sentence in zip(sentences, sentences_with_errors, applied_errors):
    # print(f"Original: {sentence}")
    # print(f"With Error: {sentence_with_error}")
    # print(f"Applied Errors: {errors_for_sentence}")
    # print()
    # if len(data) == 1061: break
    if len(data) == 500: break
    if i > 1061:
      data_point = {
        "instruction": "Detect and correct phonetic and grammatical errors in this sentence",
        "input": sentence_with_error,
        "output": sentence,
        "applied_errors": errors_for_sentence
      }
      data.append(data_point)
    i += 1
with open('nacgec_dev_instruct_zh.json', 'w') as json_file:
  json.dump(data, json_file)
