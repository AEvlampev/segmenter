# -*- coding: utf-8 -*-
import json
from random import randint

with open('random_corpora.json', encoding='utf-8') as random_json_file:
    random_json_data = json.load(random_json_file)

with open('razdel_corpora.json', encoding='utf-8') as razdel_json_file:
    razdel_json_data = json.load(razdel_json_file)


for random_text in random_json_data:
    flag_finded = False
    num = ''
    finded_text = ''
    for sentence in random_text['list_of_sentences']:
        for razdel_text in razdel_json_data:
            if sentence in razdel_text['list_of_sentences']:
                if len(random_text['list_of_sentences']) > 1:
                    rnd_sent = random_text['list_of_sentences'][randint(1, len(random_text['list_of_sentences']) - 1)]
                    if rnd_sent in razdel_text['list_of_sentences']:
                        flag_finded = True
                        num = razdel_text['number']
                        finded_text = razdel_text
                        break
                else:
                    flag_finded = True
                    num = razdel_text['number']
                    finded_text = razdel_text
                    break

        if flag_finded:
            break

    if flag_finded:
        print(random_text['number'], '==', num, random_text['text'] == finded_text['text'])
        for random_sentence, razdel_sentence in zip(random_text['list_of_sentences'], finded_text['list_of_sentences']):
            if random_sentence != razdel_sentence:
                print(random_sentence)
                print(razdel_sentence)
                print()
    else:
        print(random_text['number'], '???????????????????????????')