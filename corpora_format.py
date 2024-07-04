import json

with open('razdel_corpora.txt', encoding='cp1251') as corpora_text_file:
    corpora_text_data = corpora_text_file.readlines()
    corpora_text_data = [line.rstrip('\n') for line in corpora_text_data]

number = 1

corpora = list()
print(len(corpora_text_data))
for line in corpora_text_data:
    line_dict = dict()

    line_dict["number"] = str(number)
    splited_line = line.split('| |')
    line_dict["text"] = ' '.join(splited_line)
    line_dict["list_of_sentences"] = splited_line

    corpora += [line_dict]
    number += 1

with open('razdel_corpora.json', encoding='utf-8', mode='w') as json_file:
    json.dump(corpora, json_file, ensure_ascii=False, indent=4)
