import json
import sys
import subprocess

input_filename = sys.argv[1]
output_filename = sys.argv[2]

if input_filename == output_filename:
    # prevent overwriting
    print("input filename cannot be the same as output filename")
    quit()

parts_of_speech = {
    "N": "noun",
    "P": "plural",
    "h": "noun_phrase",
    "V": "verb_participle",
    "t": "verb_transitive",
    "i": "verb_intransitive",
    "A": "adjective",
    "v": "adverb",
    "C": "conjunction",
    "P": "preposition",
    "!": "interjection",
    "r": "pronoun",
    "D": "definite_article",
    "I": "indefinite_article",
    "o": "nominative",
}

input_file = open(input_filename, "r")
output_file = open(output_filename, "w")

lines = input_file.readlines()

index = 0
words = []
for line in lines:
    words.append(line.strip())
    index += 1
    if index % 10 == 0 or index == len(lines):
        body = {"msg": " ".join(words)}
        words = []

        response = subprocess.run(["curl", "-H", "Content-Type: application/json", "--request", "POST", "--data",
                json.dumps(body), "https://victorribeiro.com/pos/word.php"], universal_newlines=True, stdout=subprocess.PIPE)

        items = json.loads(response.stdout)

        for item in items:
            info = [ item["word"] ]
            if item["pos"] == None:
                info.append("null")
            else:
                for character in item["pos"]:
                    if character in parts_of_speech.keys():
                        info.append(parts_of_speech[character])

            if len(info) == 1:
                info.append("null")

            output_file.write(" ".join(info) + "\n")


input_file.close()
output_file.close()

# sample
# request: curl -H "Content-Type: application/json" --request POST --data "{\"msg\": \"that\"}" https://victorribeiro.com/pos/word.php
# response: [{"word":"that","suggestion":"an","pos":"DC"}]

# 1. read command line args for input & output files
# 2. post list of 10 words to https://victorribeiro.com/pos/
# 3. map the "pos" field of each element to a defined part of speech
# 4. iterate on the next 10
# 5. go back to step 2 until no words are left
# 6. write to the output file
