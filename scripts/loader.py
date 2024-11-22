import os
from typing import List
import json


first_level_word_list: List[str] = []
with open(os.path.join("resources", "first_level_word_list.txt"), "r") as file:
    content = file.read()
    for line in content.splitlines():
        first_level_word_list.append(line.split(" ")[1])

second_level_word_list: List[str] = []
with open(os.path.join("resources", "second_level_word_list.txt"), "r") as file:
    content = file.read()
    for line in content.splitlines():
        second_level_word_list.append(line.split(" ")[1])

third_level_word_list: List[str] = []
with open(os.path.join("resources", "third_level_word_list.txt"), "r") as file:
    content = file.read()
    for line in content.splitlines():
        third_level_word_list.append(line.split(" ")[1])


all_word_list: List[str] = first_level_word_list + second_level_word_list + third_level_word_list

xinhua_word_list: List[str] = []
with open("resources/word.json", "r") as file:
    data = json.load(file)
    for item in data:
        xinhua_word_list.append(item["word"])

all_word_list.extend(xinhua_word_list)
all_word_list = list(set(all_word_list))

all_ci = []

with open("resources/ci.json", "r") as file:
    data = json.load(file)
    for item in data:
        all_ci.append(item["ci"])

all_ci = list(set(all_ci))

if __name__ == "__main__":
    print(f"all_word_list: {len(all_word_list)}")
    print(f"xinhua_word_list: {len(xinhua_word_list)}")
    print(f"all_ci: {len(all_ci)}")
