# -*- coding: utf-8 -*-
import json
import time
from segmenter_with_syntax_analysis import text_to_sentences
from razdel import sentenize
from spacy.lang.ru import Russian
import nltk
import stanza

with open('random_corpora.json', encoding='utf-8') as corpora_json_file:
    corpora_json_data = json.load(corpora_json_file)

flag_only_texts_without_quotes = False
if flag_only_texts_without_quotes:
    corpora_json_data = [text for text in corpora_json_data if all([quote not in text['text'] for quote in ['"', '«']])]

list_of_texts = [d["text"] for d in corpora_json_data]
cnt_of_tokens = sum([len(text.split()) for text in list_of_texts])
cnt_of_sentences = sum([len(t['list_of_sentences']) for t in corpora_json_data])

print("Общее количество токенов по корпусу:", cnt_of_tokens)
print("Количество текстов в корпусе:", len(list_of_texts))
print("Количество предложений в корпусе:", cnt_of_sentences)

with open("comparer_time.txt", encoding='utf-8', mode='w') as f:
    pass

iteration_count = 30

for iteration in range(iteration_count):
    list_of_times = []

    cnt_of_wrong_text_segmentations = 0
    cnt_of_mistakes = 0

    total_time = 0

    for text_ind in range(len(corpora_json_data)):
        text = corpora_json_data[text_ind]['text']

        start_time = time.time()
        algorithmic_segmentation = text_to_sentences(text, True, 0, '', False, False, '', False, '', 0, -1)[3][0]
        end_time = time.time()
        total_time += end_time - start_time
        reference_segmentation = corpora_json_data[text_ind]['list_of_sentences']

        if algorithmic_segmentation != reference_segmentation:
            cnt_of_wrong_text_segmentations += 1
            difference = [sent for sent in algorithmic_segmentation if sent not in reference_segmentation]
            cnt_of_mistakes += len(difference)

    print("Наш сегментатор")
    print("Количество ошибочно разделённых текстов по корпусу:", cnt_of_wrong_text_segmentations)
    print("Общее количество ошибок разделения по корпусу:", cnt_of_mistakes)
    print("Количество ошибок на 1000 токенов", cnt_of_mistakes / (cnt_of_tokens // 1000))
    print("Время работы:", total_time, "секунд")

    with open('time.txt', encoding='utf-8', mode='r') as time_file:
        t = time_file.readlines()

    t = sum([float(line.rstrip("\n")) for line in t])
    print("Из них ушло на синтаксический разбор:", t, "секунд")

    list_of_times += [total_time, t]

    with open("time.txt", encoding='utf-8', mode='w') as f:
        pass

    print("\n")

    cnt_of_wrong_text_segmentations = 0
    cnt_of_mistakes = 0

    start_time = time.time()

    for text_ind in range(len(corpora_json_data)):
        text = corpora_json_data[text_ind]['text']

        algorithmic_segmentation = list(sentenize(text))
        algorithmic_segmentation = [sent.text for sent in algorithmic_segmentation]
        reference_segmentation = corpora_json_data[text_ind]['list_of_sentences']

        if algorithmic_segmentation != reference_segmentation:
            cnt_of_wrong_text_segmentations += 1
            difference = [sent for sent in algorithmic_segmentation if sent not in reference_segmentation]
            cnt_of_mistakes += len(difference)

    end_time = time.time()

    print("Natasha - razdel")
    print("Количество ошибочно разделённых текстов по корпусу:", cnt_of_wrong_text_segmentations)
    print("Общее количество ошибок разделения по корпусу:", cnt_of_mistakes)
    print("Количество ошибок на 1000 токенов", cnt_of_mistakes / (cnt_of_tokens // 1000))
    print("Время работы:", end_time - start_time, "секунд")
    list_of_times += [end_time - start_time]
    print("\n")

    cnt_of_wrong_text_segmentations = 0
    cnt_of_mistakes = 0

    start_time = time.time()

    for text_ind in range(len(corpora_json_data)):
        text = corpora_json_data[text_ind]['text']

        algorithmic_segmentation = nltk.tokenize.sent_tokenize(text)
        reference_segmentation = corpora_json_data[text_ind]['list_of_sentences']

        if algorithmic_segmentation != reference_segmentation:
            cnt_of_wrong_text_segmentations += 1
            difference = [sent for sent in algorithmic_segmentation if sent not in reference_segmentation]
            cnt_of_mistakes += len(difference)

    end_time = time.time()

    print("NLTK")
    print("Количество ошибочно разделённых текстов по корпусу:", cnt_of_wrong_text_segmentations)
    print("Общее количество ошибок разделения по корпусу:", cnt_of_mistakes)
    print("Количество ошибок на 1000 токенов", cnt_of_mistakes / (cnt_of_tokens // 1000))
    print("Время работы:", end_time - start_time, "секунд")
    list_of_times += [end_time - start_time]
    print("\n")

    nlp = Russian()
    nlp.add_pipe('sentencizer')

    cnt_of_wrong_text_segmentations = 0
    cnt_of_mistakes = 0

    start_time = time.time()

    for text_ind in range(len(corpora_json_data)):
        text = corpora_json_data[text_ind]['text']

        doc = nlp(text)
        algorithmic_segmentation = [sent.text.strip() for sent in doc.sents]
        reference_segmentation = corpora_json_data[text_ind]['list_of_sentences']

        if algorithmic_segmentation != reference_segmentation:
            cnt_of_wrong_text_segmentations += 1
            difference = [sent for sent in algorithmic_segmentation if sent not in reference_segmentation]
            cnt_of_mistakes += len(difference)

    end_time = time.time()

    print("Spacy")
    print("Количество ошибочно разделённых текстов по корпусу:", cnt_of_wrong_text_segmentations)
    print("Общее количество ошибок разделения по корпусу:", cnt_of_mistakes)
    print("Количество ошибок на 1000 токенов", cnt_of_mistakes / (cnt_of_tokens // 1000))
    print("Время работы:", end_time - start_time, "секунд")
    list_of_times += [end_time - start_time]
    print("\n")

    ppln = stanza.Pipeline('ru', processors='tokenize')

    cnt_of_wrong_text_segmentations = 0
    cnt_of_mistakes = 0

    start_time = time.time()

    for text_ind in range(len(corpora_json_data)):
        text = corpora_json_data[text_ind]['text']

        doc = ppln(text)
        algorithmic_segmentation = [[f'{token.text}' for token in sentence.tokens] for sentence in doc.sentences]

        reference_segmentation = corpora_json_data[text_ind]['list_of_sentences']

        tokenized_reference_segmentation = []
        for sentence in reference_segmentation:
            doc = ppln(sentence)
            tokenized_sentence = [[f'{token.text}' for token in sentence.tokens] for sentence in doc.sentences][0]
            tokenized_reference_segmentation += [tokenized_sentence]

        if algorithmic_segmentation != tokenized_reference_segmentation:
            cnt_of_wrong_text_segmentations += 1
            difference = [sent for sent in algorithmic_segmentation if sent not in tokenized_reference_segmentation]
            cnt_of_mistakes += len(difference)

    end_time = time.time()

    print("Stanza")
    print("Количество ошибочно разделённых текстов по корпусу:", cnt_of_wrong_text_segmentations)
    print("Общее количество ошибок разделения по корпусу:", cnt_of_mistakes)
    print("Количество ошибок на 1000 токенов", cnt_of_mistakes / (cnt_of_tokens // 1000))
    print("Время работы:", end_time - start_time, "секунд")
    list_of_times += [end_time - start_time]

    with open("comparer_time.txt", encoding='utf-8', mode='a') as f:
        f.write(str(list_of_times[0]) + ' ' + str(list_of_times[1]) + ' ' + str(list_of_times[2]) + ' ' +
                str(list_of_times[3]) + ' ' + str(list_of_times[4]) + ' ' + str(list_of_times[5]) + '\n')


with open("comparer_time.txt", encoding='utf-8', mode='r') as f:
    data = [line.rstrip('\n').split() for line in f.readlines()]
    data = [[float(elem) for elem in line] for line in data]
    list_of_summary_time = [0] * len(data[0])
    for line in data:
        for elem_num in range(len(line)):
            list_of_summary_time[elem_num] += line[elem_num]

    list_of_summary_time = [elem / iteration_count for elem in list_of_summary_time]

    print('\n')
    print(f"Усреднённое время работы алгоритмов за {iteration_count} итераций")
    print("Наш сегментатор:", list_of_summary_time[0], "секунд")
    print("Из них на синтаксический разбор:", list_of_summary_time[1], "секунд")
    print("Razdel:", list_of_summary_time[2], "секунд")
    print("NLTK:", list_of_summary_time[3], "секунд")
    print("SpaCy:", list_of_summary_time[4], "секунд")
    print("Stanza:", list_of_summary_time[5], "секунд")