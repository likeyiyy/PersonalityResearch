import os
from typing import List

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

if __name__ == "__main__":
    print(all_word_list)
