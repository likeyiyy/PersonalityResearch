import json
from loader import all_word_list

with open("resources/PosthumousTitle.json", "r") as file:
    posthumous_title_dict = json.load(file)

upper_titles = posthumous_title_dict["上"]
middle_titles = posthumous_title_dict["中"]
lower_titles = posthumous_title_dict["下"]

all_titles = upper_titles + middle_titles + lower_titles

for title in all_titles:
    if title not in all_word_list:
        print(title)
