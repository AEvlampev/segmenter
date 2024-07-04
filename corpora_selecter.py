# -*- coding: utf-8 -*-
from random import choices
import json

# Произвольный выбор текстов
# with open('razdel_corpora.json', encoding='utf-8', mode='r') as read_json_file:
#     corpora = json.load(read_json_file)
#
# random_corpora = choices(corpora, k=100)
#
# with open('random_corpora.json', encoding='utf-8', mode='w') as write_json_file:
#     json.dump(random_corpora, write_json_file, ensure_ascii=False, indent=4)

# Исправление нумерования текстов
# with open('random_corpora.json', encoding='utf-8', mode='r') as read_json_file:
#     corpora = json.load(read_json_file)
#
# for i in range(len(corpora)):
#     corpora[i]["number"] = i + 1
#
# with open('random_corpora.json', encoding='utf-8', mode='w') as write_json_file:
#     json.dump(corpora, write_json_file, ensure_ascii=False, indent=4)

# Коррекция знаков препинания
# with open('random_corpora.json', encoding='utf-8', mode='r') as read_json_file:
#     corpora = json.load(read_json_file)
#
#
# for i in range(len(corpora)):
#     raw_text = corpora[i]["text"]
#     raw_list_of_sentences = corpora[i]["list_of_sentences"]
#
#     raw_text = raw_text.replace(" . . .", "...")
#     raw_text = raw_text.replace(" ...", "...")
#     raw_text = raw_text.replace(" .", ".")
#     raw_text = raw_text.replace(" ,", ",")
#     raw_text = raw_text.replace(" !", "!")
#     raw_text = raw_text.replace(" ?", "?")
#     raw_text = raw_text.replace("( ", "(")
#     raw_text = raw_text.replace(" )", ")")
#
#     mod_list_of_sentences = []
#     for sent_ind in range(len(raw_list_of_sentences)):
#         sent = raw_list_of_sentences[sent_ind]
#         sent = sent.replace(" . . .", "...")
#         sent = sent.replace(" ...", "...")
#         sent = sent.replace(" .", ".")
#         sent = sent.replace(" ,", ",")
#         sent = sent.replace(" !", "!")
#         sent = sent.replace(" ?", "?")
#         sent = sent.replace("( ", "(")
#         sent = sent.replace(" )", ")")
#         mod_list_of_sentences += [sent]
#
#     corpora[i]["text"] = raw_text
#     corpora[i]["list_of_sentences"] = mod_list_of_sentences
#
# with open('random_corpora.json', encoding='utf-8', mode='w') as write_json_file:
#     json.dump(corpora, write_json_file, ensure_ascii=False, indent=4)


# Обновление текстов
with open('random_corpora.json', encoding='utf-8', mode='r') as read_json_file:
    corpora = json.load(read_json_file)

for i in range(len(corpora)):
    corpora[i]["text"] = ' '.join(corpora[i]["list_of_sentences"])

with open('random_corpora.json', encoding='utf-8', mode='w') as write_json_file:
    json.dump(corpora, write_json_file, ensure_ascii=False, indent=4)