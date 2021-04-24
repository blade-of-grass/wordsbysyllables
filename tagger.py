import json
import sys

input_filename = sys.argv[1]
output_filename = sys.argv[2]

if input_filename == output_filename:
    # prevent overwriting
    print("input filename cannot be the same as output filename")
    quit()


part_of_speech_mapping = {
    "N": "noun",
    "P": "noun",
    "h": "noun",
    "V": "verb",
    "t": "verb",
    "i": "verb",
    "A": "adjective",
    "v": "adverb",
    "C": "conjunction",
    "P": "preposition",
    "!": "interjection",
    "r": "noun",
    "D": "article",
    "I": "article",
    "o": "noun",
}

input_file = open(input_filename, "r")
output_file = open(output_filename, "w")

index = 0

while input_file.readable:
    dictionary = {"msg": ""}
    for line in input_file:
        dictionary["msg"] += line.replace("\n", " ")
        index += 1
        if index % 10 == 0:
            break

    json = dictionary["msg"]
    dictionary["msg"] = ""


print("msg: " + dictionary["msg"])

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
