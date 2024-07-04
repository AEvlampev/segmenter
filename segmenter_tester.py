# -*- coding: utf-8 -*-
import json
from segmenter_with_syntax_analysis import text_to_sentences
from pprint import pprint

with open('random_corpora.json', encoding='utf-8') as corpora_json_file:
    corpora_json_data = json.load(corpora_json_file)

# with open('experiment_corpora.json', encoding='cp1251') as corpora_json_file:
#     corpora_json_data = json.load(corpora_json_file)

cnt_of_mistakes = 0
cnt_of_tokens = 0
i = 1

for text_ind in range(len(corpora_json_data)):
    print(f"Текст №{i}")
    i += 1
    text = corpora_json_data[text_ind]['text']
    cnt_of_tokens += len(text.split())

    algorithmic_segmentation = text_to_sentences(text, True, 0, '', False, False, '', False, '', 0, -1)[3][0]
    reference_segmentation = corpora_json_data[text_ind]['list_of_sentences']

    if algorithmic_segmentation != reference_segmentation:
        cnt_of_mistakes += 1
        print("Error!!!")
        difference = [sent for sent in algorithmic_segmentation if sent not in reference_segmentation]
        pprint(difference)

        print()

print(cnt_of_mistakes)
print(cnt_of_tokens)