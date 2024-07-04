# -*- coding: utf-8 -*-
from main_algorithm import syntax_analyzer
from time import time
from pprint import pprint
import json
import re

file = open('list_of_unambiguously_interpreted_abbreviations.txt', mode='r', encoding='cp1251')
list_of_abbreviations = [i.rstrip('\n') for i in file.readlines()]
file.close()

with open("time.txt", encoding='utf-8', mode='w') as f:
    pass

with open('list_of_exceptions.json', encoding='utf-8') as list_of_exceptions_file:
    list_of_exceptions = json.load(list_of_exceptions_file)


def exception_checker(text: str, i: int) -> bool:
    punctuation_sign = text[i]

    current_word = ""
    current_word_index = i - 1

    while True:
        if not text[current_word_index].isalpha():
            break
        else:
            current_word = text[current_word_index] + current_word
        current_word_index -= 1

        if current_word_index < 0:
            break

    if current_word not in list_of_exceptions[punctuation_sign].keys():
        return False

    next_word = ""
    next_word_index = i + 2
    while True:
        if not text[next_word_index].isalpha():
            break
        else:
            next_word += text[next_word_index]
        next_word_index += 1

        if next_word_index > len(text) - 1:
            break

    if next_word in list_of_exceptions[punctuation_sign][current_word]:
        return True
    else:
        return False


def counter_of_full_subsentences_in_variant_of_segmentation(segmentation: list[str]):
    cnt_of_full_subsentences_in_variant_of_segmentation = 0
    for sentence in segmentation:
        start = time()
        syntax_of_sentence = syntax_analyzer(sentence)
        end = time()

        with open("time.txt", encoding='utf-8', mode='a') as f:
            f.write(str(end - start) + '\n')

        cnt_of_full_subsentences_in_sentence = 0
        syntax_of_sentence_keys = syntax_of_sentence.keys()

        for subsentence_key in syntax_of_sentence_keys:
            if syntax_of_sentence[subsentence_key]["subjects"] and syntax_of_sentence[subsentence_key]["predicates"]:
                cnt_of_full_subsentences_in_sentence += 1

        cnt_of_full_subsentences_in_variant_of_segmentation += cnt_of_full_subsentences_in_sentence

    return cnt_of_full_subsentences_in_variant_of_segmentation


def selecter_of_segmentation_variants(segmentation_variants):
    dict_of_segmentation_variants = dict()

    for segmentation_variant in segmentation_variants:
        cnt_of_full_subsentences_in_segmentation_variant = \
            counter_of_full_subsentences_in_variant_of_segmentation(segmentation_variant)

        if cnt_of_full_subsentences_in_segmentation_variant not in dict_of_segmentation_variants.keys():
            dict_of_segmentation_variants[cnt_of_full_subsentences_in_segmentation_variant] = [segmentation_variant]
        else:
            dict_of_segmentation_variants[cnt_of_full_subsentences_in_segmentation_variant] += [segmentation_variant]

    # pprint(dict_of_segmentation_variants)

    # Оптимальным будем называть вариант сегментации, при котором
    # образуется наибольшее количество полных простых предложений
    optimal_segmentation_variants = dict_of_segmentation_variants[max(dict_of_segmentation_variants.keys())]

    # Выберем из оптимальных тот вариант разбиения, при котором образуется наименьшее количество предложений

    max_cnt_of_sent = min([len(variant) for variant in optimal_segmentation_variants])

    for segmentation_variant in optimal_segmentation_variants:
        if len(segmentation_variant) == max_cnt_of_sent:
            return segmentation_variant


def text_to_sentences(raw_text: str, is_master: bool, start_index: int,
                      master_sentence: str, flag_sentence_is_started: bool,
                      flag_is_under_quotes: bool, type_of_opening_quote: str,
                      flag_is_under_bracket: bool, type_of_opening_bracket: str,
                      cnt_of_additional_bracket_of_the_same_type: int, last_concatenated_index: int) -> list:
    if not raw_text:
        return []

    text = raw_text

    list_of_sentences = list()
    list_of_segmentation_variants = list()

    sentence = ''
    len_of_text = len(text)
    last_splited_index = -1

    flag_sentence_with_fragment = False
    fragment = ''

    flag_is_in_numbered_list = False
    order_number_of_numbered_list = 0

    i = start_index
    while i <= (len_of_text - 1):
        # print(i, text[i])
        if text[i] == ' ' and flag_sentence_is_started is False:
            i += 1
            continue

        # Постановку кавычек регламентируем следующим образом: "..." или «...» или «..."..."...»

        if text[i] == '"':
            if type_of_opening_quote == '':
                if flag_is_under_quotes is False:
                    flag_is_under_quotes = True
                    if flag_sentence_is_started is False:
                        flag_sentence_is_started = True
                type_of_opening_quote = '"'
            elif type_of_opening_quote == '"':
                flag_is_under_quotes = False
                type_of_opening_quote = ''

        if text[i] == '«':
            if type_of_opening_quote == '':
                if flag_is_under_quotes is False:
                    flag_is_under_quotes = True
                    if flag_sentence_is_started is False:
                        flag_sentence_is_started = True
                type_of_opening_quote = '«'
        elif text[i] == '»':
            if type_of_opening_quote == '«':
                type_of_opening_quote = ''
                flag_is_under_quotes = False

        if flag_sentence_is_started is True:
            if flag_is_under_bracket is True:
                if text[i] == ')' and type_of_opening_bracket == '(':
                    if cnt_of_additional_bracket_of_the_same_type == 0:
                        flag_is_under_bracket = False
                        type_of_opening_bracket = ''
                    else:
                        cnt_of_additional_bracket_of_the_same_type -= 1
                elif text[i] == '}' and type_of_opening_bracket == '{':
                    if cnt_of_additional_bracket_of_the_same_type == 0:
                        flag_is_under_bracket = False
                        type_of_opening_bracket = ''
                    else:
                        cnt_of_additional_bracket_of_the_same_type -= 1
                elif text[i] == ']' and type_of_opening_bracket == '[':
                    if cnt_of_additional_bracket_of_the_same_type == 0:
                        flag_is_under_bracket = False
                        type_of_opening_bracket = ''
                    else:
                        cnt_of_additional_bracket_of_the_same_type -= 1
                elif text[i] == '(' and type_of_opening_bracket == '(':
                    cnt_of_additional_bracket_of_the_same_type += 1
                elif text[i] == '{' and type_of_opening_bracket == '{':
                    cnt_of_additional_bracket_of_the_same_type += 1
                elif text[i] == '[' and type_of_opening_bracket == '[':
                    cnt_of_additional_bracket_of_the_same_type += 1
            else:
                if text[i] == '(':
                    type_of_opening_bracket = '('
                    flag_is_under_bracket = True
                elif text[i] == '{':
                    type_of_opening_bracket = '{'
                    flag_is_under_bracket = True
                elif text[i] == '[':
                    type_of_opening_bracket = '['
                    flag_is_under_bracket = True
                elif text[i] in ')}]':
                    pass

        if (text[i].isupper() is True or text[i].isdigit() is True or text[
            i] in '"—«-(') and flag_sentence_is_started is False:
            flag_sentence_is_started = True

        if flag_sentence_is_started:
            if i > last_concatenated_index:
                # print(text[i], i)
                last_concatenated_index = i
                sentence += text[i]
        else:
            recurring_symbol = text[i]
            if recurring_symbol in '.!?':
                if list_of_sentences:
                    last_sentence = list_of_sentences[len(list_of_sentences) - 1]
                    if last_sentence[-1] == recurring_symbol:
                        last_sentence += text[i]
                        del list_of_sentences[len(list_of_sentences) - 1]
                        list_of_sentences += [last_sentence]

                        updated_list_of_segmentation_variants = list_of_segmentation_variants

                        for segmentation_variant in list_of_segmentation_variants:
                            last_sentence_from_segmentation = segmentation_variant[-1]
                            last_sentence_from_updated_segmentation = last_sentence_from_segmentation + recurring_symbol

                            updated_segmentation_variant = segmentation_variant
                            updated_segmentation_variant[-1] = last_sentence_from_updated_segmentation

                            updated_list_of_segmentation_variants += [updated_segmentation_variant]

                        list_of_segmentation_variants = updated_list_of_segmentation_variants
                i += 1
                continue
            else:
                pass

        if flag_sentence_is_started:
            if flag_is_under_quotes is False and flag_is_under_bracket is False:
                if text[i] == '.':
                    if sentence[:len(sentence) - 1].isdigit():
                        number = sentence[:len(sentence) - 1]

                        if flag_is_in_numbered_list:
                            if int(number) == order_number_of_numbered_list + 1:
                                order_number_of_numbered_list += 1
                                i += 1
                                continue
                            else:
                                text_substring = text[i + 1:]
                                compiler = re.compile(" [0-9]+[.] ")
                                result = list(compiler.finditer(text_substring))
                                indices_of_numbers = [[r.start(0), r.end(0)] for r in result]

                                numbers = [text_substring[n[0] + 1 : n[1] - 2] for n in indices_of_numbers]
                                if numbers:
                                    next_number = int(numbers[0])
                                    if next_number == int(number) + 1:
                                        order_number_of_numbered_list = int(number)
                                        i += 1
                                        continue
                                    else:
                                        flag_is_in_numbered_list = False
                                        order_number_of_numbered_list = 0
                                else:
                                    flag_is_in_numbered_list = False
                                    order_number_of_numbered_list = 0
                        else:
                            if int(number) == 0:
                                flag_is_in_numbered_list = True
                                order_number_of_numbered_list = 0
                                i += 1
                                continue
                            elif int(number) == 1:
                                flag_is_in_numbered_list = True
                                order_number_of_numbered_list = 1
                                i += 1
                                continue
                            else:
                                pass

                    if (i + 1) <= (len_of_text - 1):
                        if text[i + 1] != ' ':
                            i += 1
                            continue
                        else:
                            if (i + 2) <= (len_of_text - 1):
                                if text[i + 2].islower() is True:
                                    i += 1
                                    continue
                                else:
                                    pass
                            else:
                                if is_master is True:
                                    if i != last_splited_index:
                                        if flag_sentence_with_fragment:
                                            sentence = sentence.replace(fragment + ' ', '', 1)
                                            fragment = ''
                                            flag_sentence_with_fragment = False

                                        if list_of_segmentation_variants:
                                            updated_list_of_segmentation_variants = list()
                                            for segmentation_variant in list_of_segmentation_variants:
                                                updated_list_of_segmentation_variants += [
                                                    segmentation_variant + [sentence]]
                                            list_of_segmentation_variants = updated_list_of_segmentation_variants
                                        else:
                                            list_of_segmentation_variants += [[sentence]]

                                        list_of_sentences += [sentence]
                                        sentence = ''
                                        flag_sentence_is_started = False
                                        last_splited_index = i

                                    i += 1
                                    continue
                                else:
                                    list_of_sentences += [sentence]
                                    return [list_of_sentences, i,
                                            last_concatenated_index, list_of_segmentation_variants]
                    else:
                        if is_master is True:
                            if i != last_splited_index:
                                if flag_sentence_with_fragment:
                                    sentence = sentence.replace(fragment + ' ', '', 1)
                                    fragment = ''
                                    flag_sentence_with_fragment = False

                                if list_of_segmentation_variants:
                                    updated_list_of_segmentation_variants = list()
                                    for segmentation_variant in list_of_segmentation_variants:
                                        updated_list_of_segmentation_variants += [
                                            segmentation_variant + [sentence]]
                                    list_of_segmentation_variants = updated_list_of_segmentation_variants
                                else:
                                    list_of_segmentation_variants += [[sentence]]

                                list_of_sentences += [sentence]
                                sentence = ''
                                flag_sentence_is_started = False
                                last_splited_index = i

                            i += 1
                            continue
                        else:
                            list_of_sentences += [sentence]
                            return [list_of_sentences, i, last_concatenated_index, list_of_segmentation_variants]

                    splited_sentence = sentence.split()
                    last_word = splited_sentence[-1].replace('.', '')

                    if last_word in list_of_abbreviations:
                        if len(splited_sentence) == 1:
                            i += 1
                            continue
                        else:
                            if is_master:
                                list_with_slave_sentence, last_index, last_concatenated_index, \
                                    list_of_segmentation_variants_recursive = text_to_sentences(raw_text, False, i + 1,
                                                                                                sentence, False,
                                                                                                flag_is_under_quotes,
                                                                                                type_of_opening_quote,
                                                                                                flag_is_under_bracket,
                                                                                                type_of_opening_bracket,
                                                                                                cnt_of_additional_bracket_of_the_same_type,
                                                                                                last_concatenated_index)

                                slave_sentence = list_with_slave_sentence[0]
                                print('Candidate:', slave_sentence)

                                if flag_sentence_with_fragment:
                                    sentence = sentence.replace(fragment + ' ', '', 1)
                                    fragment = ''
                                    flag_sentence_with_fragment = False

                                master_with_slave_sentence = sentence + ' ' + slave_sentence

                                if i != last_splited_index:
                                    # Создаём все возможные случаи сегментации предложения по инициалам
                                    master_with_slave_sentence_splited = master_with_slave_sentence.rstrip('.').split()
                                    variants_with_initial_segmentation = list()
                                    for word_index in range(len(master_with_slave_sentence_splited)):
                                        word_splited = master_with_slave_sentence_splited[word_index]
                                        if word_splited[-1] == '.':
                                            if len(word_splited) - 1 == 1:
                                                if len(master_with_slave_sentence_splited) > 1:
                                                    penultimate_word_splited = \
                                                        master_with_slave_sentence_splited[word_index - 1]
                                                    if penultimate_word_splited[0].isupper():
                                                        if len(master_with_slave_sentence_splited) > 2:
                                                            word_before_penultimate_splited = \
                                                                master_with_slave_sentence_splited[word_index - 2]
                                                            if word_before_penultimate_splited[0].isupper() and \
                                                                    word_before_penultimate_splited[-1] != ".":
                                                                first_sentence_splited = \
                                                                    [master_with_slave_sentence_splited[
                                                                         index]
                                                                     for index in range(word_index + 1)]
                                                                second_sentence_splited = \
                                                                    [master_with_slave_sentence_splited[
                                                                         index]
                                                                     for index in range(word_index + 1,
                                                                                        len(master_with_slave_sentence_splited))]

                                                                first_sentence = ' '.join(
                                                                    first_sentence_splited)
                                                                second_sentence = ' '.join(
                                                                    second_sentence_splited) + '.'
                                                                if first_sentence != sentence:
                                                                    variants_with_initial_segmentation += \
                                                                        [[first_sentence,
                                                                          second_sentence]]

                                    new_segmentation_variants = variants_with_initial_segmentation
                                    new_segmentation_variants += [[sentence, slave_sentence]]
                                    new_segmentation_variants += [[master_with_slave_sentence]]

                                    optimal_segmentation_variant = \
                                        selecter_of_segmentation_variants(new_segmentation_variants)

                                    # print('11111111111', optimal_segmentation_variant)

                                    if list_of_segmentation_variants:
                                        updated_list_of_segmentation_variants = list()
                                        for segmentation_variant in list_of_segmentation_variants:
                                            updated_list_of_segmentation_variants += [
                                                segmentation_variant + optimal_segmentation_variant]
                                        list_of_segmentation_variants = updated_list_of_segmentation_variants
                                    else:
                                        list_of_segmentation_variants += [optimal_segmentation_variant]

                                    last_splited_index = last_index

                                list_of_sentences += [sentence]
                                sentence = slave_sentence

                                flag_sentence_with_fragment = True
                                fragment = slave_sentence

                                i = last_index
                                continue
                            else:
                                list_of_sentences += [sentence]
                                return [list_of_sentences, i, last_concatenated_index, list_of_segmentation_variants]
                    else:
                        # Проверяем, окончилось ли предложение оканчивается инициалом
                        if len(last_word) == 1 and last_word[0].isupper():
                            # Проверяем, есть ли ещё слова в накопленном предложении
                            if len(splited_sentence) > 1:
                                # Берём предпоследнее слово и проверяем, чем оно является
                                penultimate_word = splited_sentence[-2]

                                # Если предпоследнее слово - инициал
                                if len(penultimate_word) == 2 and penultimate_word[0].isupper() and penultimate_word[
                                    -1] == '.':
                                    if (i + 3) <= (len_of_text - 1):
                                        if text[i + 3] == '.':
                                            if is_master:
                                                if i != last_splited_index:
                                                    if flag_sentence_with_fragment:
                                                        sentence = sentence.replace(fragment + ' ', '', 1)
                                                        fragment = ''
                                                        flag_sentence_with_fragment = False

                                                    if list_of_segmentation_variants:
                                                        updated_list_of_segmentation_variants = list()
                                                        for segmentation_variant in list_of_segmentation_variants:
                                                            updated_list_of_segmentation_variants += [
                                                                segmentation_variant + [sentence]]
                                                        list_of_segmentation_variants = \
                                                            updated_list_of_segmentation_variants
                                                    else:
                                                        list_of_segmentation_variants += [[sentence]]

                                                    last_splited_index = i

                                                    list_of_sentences += [sentence]
                                                    sentence = ''
                                                    flag_sentence_is_started = False

                                                i += 1
                                                continue
                                            else:
                                                list_of_sentences += [sentence]
                                                return [list_of_sentences, i, last_concatenated_index,
                                                        list_of_segmentation_variants]
                                        else:
                                            if len(splited_sentence) > 2:
                                                word_before_penultimate = splited_sentence[-3]
                                                if word_before_penultimate[0].isupper() is True:
                                                    if is_master:
                                                        list_with_slave_sentence, last_index, last_concatenated_index, \
                                                            list_of_segmentation_variants_recursive = text_to_sentences(
                                                            raw_text, False, i + 1, sentence, False,
                                                            flag_is_under_quotes, type_of_opening_quote,
                                                            flag_is_under_bracket,
                                                            type_of_opening_bracket,
                                                            cnt_of_additional_bracket_of_the_same_type,
                                                            last_concatenated_index)

                                                        slave_sentence = list_with_slave_sentence[0]
                                                        print('Candidate:', slave_sentence)

                                                        if flag_sentence_with_fragment:
                                                            sentence = sentence.replace(fragment + ' ', '', 1)
                                                            fragment = ''
                                                            flag_sentence_with_fragment = False

                                                        master_with_slave_sentence = sentence + ' ' + slave_sentence

                                                        if i != last_splited_index:
                                                            # Создаём все возможные случаи сегментации предложения
                                                            # по инициалам
                                                            master_with_slave_sentence_splited = master_with_slave_sentence.rstrip(
                                                                '.').split()
                                                            variants_with_initial_segmentation = list()
                                                            for word_index in range(
                                                                    len(master_with_slave_sentence_splited)):
                                                                word_splited = master_with_slave_sentence_splited[
                                                                    word_index]
                                                                if word_splited[-1] == '.':
                                                                    if len(word_splited) - 1 == 1:
                                                                        if len(master_with_slave_sentence_splited) > 1:
                                                                            penultimate_word_splited = \
                                                                                master_with_slave_sentence_splited[
                                                                                    word_index - 1]
                                                                            if penultimate_word_splited[0].isupper():
                                                                                if len(master_with_slave_sentence_splited) > 2:
                                                                                    word_before_penultimate_splited = \
                                                                                        master_with_slave_sentence_splited[
                                                                                            word_index - 2]
                                                                                    if word_before_penultimate_splited[
                                                                                        0].isupper() and \
                                                                                            word_before_penultimate_splited[
                                                                                                -1] != ".":
                                                                                        first_sentence_splited = \
                                                                                            [
                                                                                                master_with_slave_sentence_splited[
                                                                                                    index]
                                                                                                for index in
                                                                                                range(word_index + 1)]
                                                                                        second_sentence_splited = \
                                                                                            [
                                                                                                master_with_slave_sentence_splited[
                                                                                                    index]
                                                                                                for index in
                                                                                                range(word_index + 1,
                                                                                                      len(master_with_slave_sentence_splited))]

                                                                                        first_sentence = ' '.join(
                                                                                            first_sentence_splited)
                                                                                        second_sentence = ' '.join(
                                                                                            second_sentence_splited) + '.'
                                                                                        if first_sentence != sentence:
                                                                                            variants_with_initial_segmentation += \
                                                                                                [[first_sentence,
                                                                                                  second_sentence]]

                                                            new_segmentation_variants = \
                                                                variants_with_initial_segmentation
                                                            new_segmentation_variants += [[sentence, slave_sentence]]
                                                            new_segmentation_variants += [[master_with_slave_sentence]]

                                                            optimal_segmentation_variant = \
                                                                selecter_of_segmentation_variants(
                                                                    new_segmentation_variants)

                                                            # print('11111111111', optimal_segmentation_variant)

                                                            if list_of_segmentation_variants:
                                                                updated_list_of_segmentation_variants = list()
                                                                for segmentation_variant in list_of_segmentation_variants:
                                                                    updated_list_of_segmentation_variants += [
                                                                        segmentation_variant + optimal_segmentation_variant]
                                                                list_of_segmentation_variants = updated_list_of_segmentation_variants
                                                            else:
                                                                list_of_segmentation_variants += [
                                                                    optimal_segmentation_variant]

                                                            last_splited_index = last_index

                                                        list_of_sentences += [sentence]
                                                        sentence = slave_sentence

                                                        flag_sentence_with_fragment = True
                                                        fragment = slave_sentence

                                                        i = last_index
                                                        continue
                                                    else:
                                                        list_of_sentences += [sentence]
                                                        return [list_of_sentences, i, last_concatenated_index,
                                                                list_of_segmentation_variants]
                                                else:
                                                    i += 1
                                                    continue
                                            else:
                                                i += 1
                                                continue

                                elif len(penultimate_word) != 1 and penultimate_word[0].isupper() is True:
                                    if (i + 3) <= (len_of_text - 1):
                                        if text[i + 3] == '.':
                                            i += 1
                                            continue
                                        else:
                                            if is_master:
                                                list_with_slave_sentence, last_index, last_concatenated_index, \
                                                    list_of_segmentation_variants_recursive = text_to_sentences(
                                                    raw_text, False, i + 1, sentence, False,
                                                    flag_is_under_quotes, type_of_opening_quote, flag_is_under_bracket,
                                                    type_of_opening_bracket,
                                                    cnt_of_additional_bracket_of_the_same_type, last_concatenated_index)

                                                slave_sentence = list_with_slave_sentence[0]
                                                print('Candidate:', slave_sentence)

                                                if flag_sentence_with_fragment:
                                                    sentence = sentence.replace(fragment + ' ', '', 1)
                                                    fragment = ''
                                                    flag_sentence_with_fragment = False

                                                master_with_slave_sentence = sentence + ' ' + slave_sentence

                                                if i != last_splited_index:
                                                    # Создаём все возможные случаи сегментации предложения по инициалам
                                                    master_with_slave_sentence_splited = master_with_slave_sentence.rstrip(
                                                        '.').split()
                                                    variants_with_initial_segmentation = list()
                                                    for word_index in range(len(master_with_slave_sentence_splited)):
                                                        word_splited = master_with_slave_sentence_splited[word_index]
                                                        if word_splited[-1] == '.':
                                                            if len(word_splited) - 1 == 1:
                                                                if len(master_with_slave_sentence_splited) > 1:
                                                                    penultimate_word_splited = \
                                                                        master_with_slave_sentence_splited[
                                                                            word_index - 1]
                                                                    if penultimate_word_splited[0].isupper():
                                                                        if len(master_with_slave_sentence_splited) > 2:
                                                                            word_before_penultimate_splited = \
                                                                                master_with_slave_sentence_splited[
                                                                                    word_index - 2]
                                                                            if word_before_penultimate_splited[
                                                                                0].isupper() and \
                                                                                    word_before_penultimate_splited[
                                                                                        -1] != ".":
                                                                                first_sentence_splited = \
                                                                                    [master_with_slave_sentence_splited[
                                                                                         index]
                                                                                     for index in range(word_index + 1)]
                                                                                second_sentence_splited = \
                                                                                    [master_with_slave_sentence_splited[
                                                                                         index]
                                                                                     for index in range(word_index + 1,
                                                                                                        len(master_with_slave_sentence_splited))]

                                                                                first_sentence = ' '.join(
                                                                                    first_sentence_splited)
                                                                                second_sentence = ' '.join(
                                                                                    second_sentence_splited) + '.'
                                                                                if first_sentence != sentence:
                                                                                    variants_with_initial_segmentation += \
                                                                                        [[first_sentence,
                                                                                          second_sentence]]

                                                    new_segmentation_variants = variants_with_initial_segmentation
                                                    new_segmentation_variants += [[sentence, slave_sentence]]
                                                    new_segmentation_variants += [[master_with_slave_sentence]]

                                                    optimal_segmentation_variant = \
                                                        selecter_of_segmentation_variants(new_segmentation_variants)

                                                    # print('11111111111', optimal_segmentation_variant)

                                                    if list_of_segmentation_variants:
                                                        updated_list_of_segmentation_variants = list()
                                                        for segmentation_variant in list_of_segmentation_variants:
                                                            updated_list_of_segmentation_variants += [
                                                                segmentation_variant + optimal_segmentation_variant]
                                                        list_of_segmentation_variants = updated_list_of_segmentation_variants
                                                    else:
                                                        list_of_segmentation_variants += [optimal_segmentation_variant]

                                                    last_splited_index = last_index

                                                list_of_sentences += [sentence]
                                                sentence = slave_sentence

                                                flag_sentence_with_fragment = True
                                                fragment = slave_sentence

                                                i = last_index
                                                continue
                                            else:
                                                list_of_sentences += [sentence]
                                                return [list_of_sentences, i, last_concatenated_index,
                                                        list_of_segmentation_variants]
                                else:
                                    i += 1
                                    continue
                            else:
                                i += 1
                                continue
                        else:
                            if is_master:
                                if i != last_splited_index:
                                    if list_of_segmentation_variants:
                                        if flag_sentence_with_fragment:
                                            sentence = sentence.replace(fragment + ' ', '', 1)
                                            fragment = ''
                                            flag_sentence_with_fragment = False

                                        updated_list_of_segmentation_variants = list()
                                        for segmentation_variant in list_of_segmentation_variants:
                                            updated_list_of_segmentation_variants += [segmentation_variant + [sentence]]
                                        list_of_segmentation_variants = updated_list_of_segmentation_variants
                                    else:
                                        list_of_segmentation_variants += [[sentence]]

                                    last_splited_index = i

                                    list_of_sentences += [sentence]
                                    sentence = ''
                                    flag_sentence_is_started = False

                                i += 1
                                continue
                            else:
                                list_of_sentences += [sentence]
                                return [list_of_sentences, i, last_concatenated_index, list_of_segmentation_variants]
                elif text[i] == '!':
                    if (i + 1) <= (len_of_text - 1):
                        if text[i + 1] != ' ':
                            i += 1
                            continue
                        else:
                            if (i + 2) <= (len_of_text - 1):
                                if text[i + 2].islower() is True:
                                    i += 1
                                    continue
                                # TODO Околокостыльное решение, либо формализовать, либо переделать
                                elif text[i + 2] == "-":
                                    if (i + 3) <= (len_of_text - 1):
                                        if not text[i + 3].isupper():
                                            if (i + 4) <= (len_of_text - 1):
                                                if text[i + 4].islower():
                                                    i += 1
                                                    continue
                                else:
                                    # TODO Распространить проверку исключений на все терминальные знаки препинания
                                    if exception_checker(text, i):
                                        i += 1
                                        continue

                                    if is_master is True:
                                        if i != last_splited_index:
                                            if flag_sentence_with_fragment:
                                                sentence = sentence.replace(fragment + ' ', '', 1)
                                                fragment = ''
                                                flag_sentence_with_fragment = False

                                            if list_of_segmentation_variants:
                                                updated_list_of_segmentation_variants = list()
                                                for segmentation_variant in list_of_segmentation_variants:
                                                    updated_list_of_segmentation_variants += [
                                                        segmentation_variant + [sentence]]
                                                list_of_segmentation_variants = updated_list_of_segmentation_variants
                                            else:
                                                list_of_segmentation_variants += [[sentence]]

                                            list_of_sentences += [sentence]
                                            sentence = ''
                                            flag_sentence_is_started = False
                                            last_splited_index = i

                                        i += 1
                                        continue
                                    else:
                                        list_of_sentences += [sentence]
                                        return [list_of_sentences, i,
                                                last_concatenated_index, list_of_segmentation_variants]
                            else:
                                if is_master is True:
                                    if i != last_splited_index:
                                        if flag_sentence_with_fragment:
                                            sentence = sentence.replace(fragment + ' ', '', 1)
                                            fragment = ''
                                            flag_sentence_with_fragment = False

                                        if list_of_segmentation_variants:
                                            updated_list_of_segmentation_variants = list()
                                            for segmentation_variant in list_of_segmentation_variants:
                                                updated_list_of_segmentation_variants += [
                                                    segmentation_variant + [sentence]]
                                            list_of_segmentation_variants = updated_list_of_segmentation_variants
                                        else:
                                            list_of_segmentation_variants += [[sentence]]

                                        list_of_sentences += [sentence]
                                        sentence = ''
                                        flag_sentence_is_started = False
                                        last_splited_index = i

                                    i += 1
                                    continue
                                else:
                                    list_of_sentences += [sentence]
                                    return [list_of_sentences, i,
                                            last_concatenated_index, list_of_segmentation_variants]
                    else:
                        if is_master is True:
                            if i != last_splited_index:
                                if flag_sentence_with_fragment:
                                    sentence = sentence.replace(fragment + ' ', '', 1)
                                    fragment = ''
                                    flag_sentence_with_fragment = False

                                if list_of_segmentation_variants:
                                    updated_list_of_segmentation_variants = list()
                                    for segmentation_variant in list_of_segmentation_variants:
                                        updated_list_of_segmentation_variants += [
                                            segmentation_variant + [sentence]]
                                    list_of_segmentation_variants = updated_list_of_segmentation_variants
                                else:
                                    list_of_segmentation_variants += [[sentence]]

                                list_of_sentences += [sentence]
                                sentence = ''
                                flag_sentence_is_started = False
                                last_splited_index = i

                            i += 1
                            continue
                        else:
                            list_of_sentences += [sentence]
                            return [list_of_sentences, i, last_concatenated_index, list_of_segmentation_variants]

                elif text[i] == '?':
                    if (i + 1) <= (len_of_text - 1):
                        if text[i + 1] != ' ':
                            i += 1
                            continue
                        else:
                            if (i + 2) <= (len_of_text - 1):
                                if text[i + 2].islower() is True:
                                    i += 1
                                    continue
                                else:
                                    if is_master is True:
                                        if i != last_splited_index:
                                            if flag_sentence_with_fragment:
                                                sentence = sentence.replace(fragment + ' ', '', 1)
                                                fragment = ''
                                                flag_sentence_with_fragment = False

                                            if list_of_segmentation_variants:
                                                updated_list_of_segmentation_variants = list()
                                                for segmentation_variant in list_of_segmentation_variants:
                                                    updated_list_of_segmentation_variants += [
                                                        segmentation_variant + [sentence]]
                                                list_of_segmentation_variants = updated_list_of_segmentation_variants
                                            else:
                                                list_of_segmentation_variants += [[sentence]]

                                            list_of_sentences += [sentence]
                                            sentence = ''
                                            flag_sentence_is_started = False
                                            last_splited_index = i

                                        i += 1
                                        continue
                                    else:
                                        list_of_sentences += [sentence]
                                        return [list_of_sentences, i,
                                                last_concatenated_index, list_of_segmentation_variants]
                            else:
                                if is_master is True:
                                    if i != last_splited_index:
                                        if flag_sentence_with_fragment:
                                            sentence = sentence.replace(fragment + ' ', '', 1)
                                            fragment = ''
                                            flag_sentence_with_fragment = False

                                        if list_of_segmentation_variants:
                                            updated_list_of_segmentation_variants = list()
                                            for segmentation_variant in list_of_segmentation_variants:
                                                updated_list_of_segmentation_variants += [
                                                    segmentation_variant + [sentence]]
                                            list_of_segmentation_variants = updated_list_of_segmentation_variants
                                        else:
                                            list_of_segmentation_variants += [[sentence]]

                                        list_of_sentences += [sentence]
                                        sentence = ''
                                        flag_sentence_is_started = False
                                        last_splited_index = i

                                    i += 1
                                    continue
                                else:
                                    list_of_sentences += [sentence]
                                    return [list_of_sentences, i,
                                            last_concatenated_index, list_of_segmentation_variants]
                    else:
                        if is_master is True:
                            if i != last_splited_index:
                                if flag_sentence_with_fragment:
                                    sentence = sentence.replace(fragment + ' ', '', 1)
                                    fragment = ''
                                    flag_sentence_with_fragment = False

                                if list_of_segmentation_variants:
                                    updated_list_of_segmentation_variants = list()
                                    for segmentation_variant in list_of_segmentation_variants:
                                        updated_list_of_segmentation_variants += [
                                            segmentation_variant + [sentence]]
                                    list_of_segmentation_variants = updated_list_of_segmentation_variants
                                else:
                                    list_of_segmentation_variants += [[sentence]]

                                list_of_sentences += [sentence]
                                sentence = ''
                                flag_sentence_is_started = False
                                last_splited_index = i

                            i += 1
                            continue
                        else:
                            list_of_sentences += [sentence]
                            return [list_of_sentences, i, last_concatenated_index, list_of_segmentation_variants]

                elif text[i] == '…':
                    if (i + 1) <= (len_of_text - 1):
                        if text[i + 1] != ' ':
                            i += 1
                            continue
                        else:
                            if (i + 2) <= (len_of_text - 1):
                                if text[i + 2].islower() is True:
                                    i += 1
                                    continue
                                else:
                                    if is_master is True:
                                        if i != last_splited_index:
                                            if flag_sentence_with_fragment:
                                                sentence = sentence.replace(fragment + ' ', '', 1)
                                                fragment = ''
                                                flag_sentence_with_fragment = False

                                            if list_of_segmentation_variants:
                                                updated_list_of_segmentation_variants = list()
                                                for segmentation_variant in list_of_segmentation_variants:
                                                    updated_list_of_segmentation_variants += [
                                                        segmentation_variant + [sentence]]
                                                list_of_segmentation_variants = updated_list_of_segmentation_variants
                                            else:
                                                list_of_segmentation_variants += [[sentence]]

                                            list_of_sentences += [sentence]
                                            sentence = ''
                                            flag_sentence_is_started = False
                                            last_splited_index = i

                                        i += 1
                                        continue
                                    else:
                                        list_of_sentences += [sentence]
                                        return [list_of_sentences, i,
                                                last_concatenated_index, list_of_segmentation_variants]
                            else:
                                if is_master is True:
                                    if i != last_splited_index:
                                        if flag_sentence_with_fragment:
                                            sentence = sentence.replace(fragment + ' ', '', 1)
                                            fragment = ''
                                            flag_sentence_with_fragment = False

                                        if list_of_segmentation_variants:
                                            updated_list_of_segmentation_variants = list()
                                            for segmentation_variant in list_of_segmentation_variants:
                                                updated_list_of_segmentation_variants += [
                                                    segmentation_variant + [sentence]]
                                            list_of_segmentation_variants = updated_list_of_segmentation_variants
                                        else:
                                            list_of_segmentation_variants += [[sentence]]

                                        list_of_sentences += [sentence]
                                        sentence = ''
                                        flag_sentence_is_started = False
                                        last_splited_index = i

                                    i += 1
                                    continue
                                else:
                                    list_of_sentences += [sentence]
                                    return [list_of_sentences, i,
                                            last_concatenated_index, list_of_segmentation_variants]
                    else:
                        if is_master is True:
                            if i != last_splited_index:
                                if flag_sentence_with_fragment:
                                    sentence = sentence.replace(fragment + ' ', '', 1)
                                    fragment = ''
                                    flag_sentence_with_fragment = False

                                if list_of_segmentation_variants:
                                    updated_list_of_segmentation_variants = list()
                                    for segmentation_variant in list_of_segmentation_variants:
                                        updated_list_of_segmentation_variants += [
                                            segmentation_variant + [sentence]]
                                    list_of_segmentation_variants = updated_list_of_segmentation_variants
                                else:
                                    list_of_segmentation_variants += [[sentence]]

                                list_of_sentences += [sentence]
                                sentence = ''
                                flag_sentence_is_started = False
                                last_splited_index = i

                            i += 1
                            continue
                        else:
                            list_of_sentences += [sentence]
                            return [list_of_sentences, i, last_concatenated_index, list_of_segmentation_variants]

        i += 1

    if sentence:
        if is_master:
            if i != last_splited_index:
                flag_sentence_is_not_fragment = True
                if flag_sentence_with_fragment:
                    if sentence != fragment:
                        sentence = sentence.replace(fragment + ' ', '', 1)
                        fragment = ''
                        flag_sentence_with_fragment = False
                    else:
                        flag_sentence_is_not_fragment = False

                if flag_sentence_is_not_fragment:
                    if sentence != list_of_segmentation_variants[0][-1]:
                        if list_of_segmentation_variants:
                            updated_list_of_segmentation_variants = list()
                            for segmentation_variant in list_of_segmentation_variants:
                                updated_list_of_segmentation_variants += [
                                    segmentation_variant + [sentence]]
                            list_of_segmentation_variants = updated_list_of_segmentation_variants
                        else:
                            list_of_segmentation_variants += [[sentence]]

                        list_of_sentences += [sentence]

                    sentence = ''
                    flag_sentence_is_started = False
                    last_splited_index = i
        else:
            list_of_sentences += [sentence]
            return [list_of_sentences, i, last_concatenated_index, list_of_segmentation_variants]

    if raw_text and not list_of_sentences and is_master:
        raise Exception

    return [list_of_sentences, i, last_concatenated_index, list_of_segmentation_variants]


if __name__ == "__main__":
    raw_text = "Термин «черная дыра» введен Дж. Уилером в 1968 г."

    list_of_segmentation_variants = text_to_sentences(raw_text, True, 0, '', False, False, '', False, '', 0, -1)[3]

    pprint(list_of_segmentation_variants[0])
