from loader import all_word_list

index = 1
for word1 in all_word_list:
    for word2 in all_word_list:
        print(f"{index}. {word1}{word2}")
        index += 1
