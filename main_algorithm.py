# -*- coding: utf-8 -*-
from pprint import pprint

from dependency_parsing import stanza_json
from constituency_tree_builder.creator import dependency_tree_to_constituency_tree
from constituency_tree_builder.utils import json_to_dependency_tree


def paths(some_dict, path=()):
    for key, value in some_dict.items():
        key_path = path + (key,)
        yield key_path
        if hasattr(value, "items"):
            yield from paths(value, key_path)


def main_terms_analyzer(sentence):
    list_of_predicates = []
    list_of_subjects = []

    if sentence["_type"] == "homogeneous-predicates":
        sentence_keys = sentence.keys()
        for key in sentence_keys:
            if "predicate" in key:
                predicate = sentence[key]
                if predicate["_type"] == "predicate":
                    while 'predicate' in predicate.keys():
                        predicate = predicate["predicate"]

                    if predicate["_type"] == "predicate":
                        list_of_predicates += [predicate["_token"]["text"]]
                    elif predicate["_type"] == "compound-predicate":
                        keys_of_predicate = predicate.keys()
                        full_predicate = []
                        for predicate_key in keys_of_predicate:
                            if 'verb' in predicate_key:
                                subpredicate = predicate[predicate_key]
                                if subpredicate['_type'] == 'predicate':
                                    full_predicate += [subpredicate["_token"]["text"]]
                                elif subpredicate["_type"] == 'compound-predicate':
                                    full_predicate += [subpredicate['main-nominative']["_token"]["text"]]
                                    full_predicate += [subpredicate['aux-verb']["_token"]["text"]]
                        full_predicate = list(sorted(full_predicate))
                        full_predicate = ' '.join(full_predicate)
                        list_of_predicates += [full_predicate]

    else:
        if "predicate" in sentence.keys():
            temp_dict = sentence

            while "predicate" in temp_dict.keys():
                temp_dict = temp_dict["predicate"]

            if temp_dict["_type"] == "predicate":
                while "predicate" in temp_dict.keys():
                    temp_dict = temp_dict["predicate"]

                list_of_predicates += [temp_dict["_token"]["text"]]

            elif temp_dict["_type"] == "compound-predicate":
                type_of_compound_predicate = list(temp_dict.keys())[1]
                if "verb" not in type_of_compound_predicate:
                    while type_of_compound_predicate in temp_dict.keys():
                        temp_dict = temp_dict[type_of_compound_predicate]

                if "_token" in temp_dict.keys():
                    list_of_predicates += [temp_dict["_token"]["text"]]
                else:
                    predicate = temp_dict
                    if predicate["_type"] == "compound-predicate":
                        predicate_keys = list(predicate.keys())
                        predicate_text = []
                        for key_ind in range(1, len(predicate_keys)):
                            if "_token" in predicate[predicate_keys[key_ind]].keys():
                                predicate_text += [predicate[predicate_keys[key_ind]]["_token"]["text"]]
                            else:
                                temp_predicate = predicate[predicate_keys[key_ind]]
                                temp_predicate_keys = list(temp_predicate.keys())
                                for temp_key_ind in range(1, len(temp_predicate_keys)):
                                    temp_key = temp_predicate_keys[temp_key_ind]

                                    temp_predicate_by_key = temp_predicate[temp_key]

                                    type_of_temp_predicate_by_key = temp_predicate_by_key['_type']
                                    while type_of_temp_predicate_by_key in temp_predicate_by_key.keys():
                                        temp_predicate_by_key = temp_predicate_by_key[type_of_temp_predicate_by_key]
                                        type_of_temp_predicate_by_key = temp_predicate_by_key['_type']

                                    predicate_text += [temp_predicate_by_key["_token"]["text"]]

                        list_of_predicates += [" ".join(predicate_text)]
                    elif predicate["_type"] == "homogeneous-main-nominatives":
                        predicate_keys = list(predicate.keys())
                        for key_ind in range(1, len(predicate_keys)):
                            if "nominative" in predicate_keys[key_ind]:
                                if "_token" in predicate[predicate_keys[key_ind]]:
                                    list_of_predicates += [predicate[predicate_keys[key_ind]]["_token"]["text"]]
                                else:
                                    list_of_predicates += [
                                        predicate[predicate_keys[key_ind]]["main-nominative"]["_token"]["text"]]

            elif temp_dict["_type"] == "homogeneous-predicates":
                temp_dict_keys = list(temp_dict.keys())
                for key in temp_dict_keys:
                    if "predicate" in key:
                        predicate = temp_dict[key]
                        if predicate["_type"] == "predicate":
                            while "predicate" in predicate.keys():
                                predicate = predicate["predicate"]

                            if predicate["_type"] == "predicate":
                                list_of_predicates += [predicate["_token"]["text"]]
                            elif predicate["_type"] == "compound-predicate":
                                type_of_compound_predicate = list(predicate.keys())[1]
                                if "verb" not in type_of_compound_predicate:
                                    while type_of_compound_predicate in predicate.keys():
                                        predicate = predicate[type_of_compound_predicate]

                                if "_token" in predicate.keys():
                                    list_of_predicates += [predicate["_token"]["text"]]
                                else:
                                    predicate_keys = list(predicate.keys())
                                    predicate_text = []
                                    for key_ind in range(1, len(predicate_keys)):
                                        add_predicate = predicate[predicate_keys[key_ind]]

                                        while "predicate" in add_predicate.keys():
                                            add_predicate = add_predicate["predicate"]

                                        predicate_text += [add_predicate["_token"]["text"]]
                                    list_of_predicates += [" ".join(predicate_text)]

                        elif predicate["_type"] == "compound-predicate":
                            type_of_compound_predicate = list(predicate.keys())[1]
                            if "verb" not in type_of_compound_predicate:
                                while type_of_compound_predicate in predicate.keys():
                                    predicate = predicate[type_of_compound_predicate]

                            if "_token" in predicate.keys():
                                list_of_predicates += [predicate["_token"]["text"]]
                            else:
                                predicate_keys = list(predicate.keys())
                                predicate_text = []
                                for key_ind in range(1, len(predicate_keys)):
                                    predicate_text += [predicate[predicate_keys[key_ind]]["_token"]["text"]]
                                list_of_predicates += [" ".join(predicate_text)]

    if "subject" in sentence.keys():
        temp_dict = sentence

        while "subject" in temp_dict.keys():
            temp_dict = temp_dict["subject"]

        if temp_dict["_type"] == "subject":
            try:
                list_of_subjects += [temp_dict["_token"]["text"]]
            except Exception as e:
                print("Error in subject parsing")
                print(e)
                pprint(temp_dict)
                exit()
        elif temp_dict["_type"] == "homogeneous-subjects":
            temp_dict_keys = list(temp_dict.keys())
            for key in temp_dict_keys:
                if "subject" in key:
                    subject = temp_dict[key]
                    while "subject" in subject.keys():
                        subject = subject["subject"]
                    try:
                        if subject['_type'] == 'quoted-group':
                            list_of_subjects += subject['content']["_token"]["text"]

                        elif subject['_type'] == 'subject':
                            list_of_subjects += [subject["_token"]["text"]]
                    except Exception as e:
                        print("Error in subject parsing")
                        print(e)
                        pprint(temp_dict)
                        exit()

    return [sorted(list_of_subjects), sorted(list_of_predicates)]


def syntax_analyzer(sentence):
    syntax_of_sentence = dict()

    dependency_tree = json_to_dependency_tree(stanza_json(sentence))
    constituency_tree = dependency_tree_to_constituency_tree(dependency_tree)

    if "core" in constituency_tree.keys():
        dict_of_core = constituency_tree["core"]
    else:
        dict_of_core = constituency_tree

    while "core" in dict_of_core.keys():
        dict_of_core = dict_of_core["core"]

    if dict_of_core["_type"] in ["core", "predicate", "subject", "sentence", "homogeneous-predicates"]:
        while "core" in dict_of_core.keys():
            dict_of_core = dict_of_core["core"]
        syntax_of_sentence["main-sentence"] = dict()
        sentence_syntax_analyze = main_terms_analyzer(dict_of_core)

        syntax_of_sentence["main-sentence"]["subjects"] = sentence_syntax_analyze[0]
        syntax_of_sentence["main-sentence"]["predicates"] = sentence_syntax_analyze[1]

        ind_of_indirect_object_subsentence = 1

        sentence_paths = paths(dict_of_core)

        for path in sentence_paths:
            if path[-1] == "sentence" and ("indirect-object" in path or "direct-object" in path
                                           or "definition" in path):
                indirect_object_subsentence = dict_of_core
                for key in path:
                    indirect_object_subsentence = indirect_object_subsentence[key]

                if indirect_object_subsentence["_type"] in ["core", "predicate", "subject", "homogeneous-predicates",
                                                            "homogeneous-subjects"]:
                    syntax_of_sentence[f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"] = \
                        dict()
                    indirect_object_subsentence_syntax_analyze = main_terms_analyzer(indirect_object_subsentence)

                    syntax_of_sentence[f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"][
                        "subjects"] \
                        = indirect_object_subsentence_syntax_analyze[0]
                    syntax_of_sentence[f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"][
                        "predicates"] \
                        = indirect_object_subsentence_syntax_analyze[1]
                    ind_of_indirect_object_subsentence += 1
                else:
                    indirect_object_subsentence_keys = indirect_object_subsentence.keys()
                    for key_of_subsentence in indirect_object_subsentence_keys:
                        if "sentence" in key_of_subsentence:
                            temp_subsentence = indirect_object_subsentence[key_of_subsentence]
                            syntax_of_sentence[
                                f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"] = dict()

                            indirect_object_temp_subsentence_syntax_analyze = main_terms_analyzer(temp_subsentence)

                            syntax_of_sentence[f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"][
                                "subjects"] \
                                = indirect_object_temp_subsentence_syntax_analyze[0]
                            syntax_of_sentence[f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"][
                                "predicates"] \
                                = indirect_object_temp_subsentence_syntax_analyze[1]
                            ind_of_indirect_object_subsentence += 1

    elif "sentence" in dict_of_core["_type"]:
        while "core" in dict_of_core.keys():
            dict_of_core = dict_of_core["core"]
        ind_of_indirect_object_subsentence = 1
        for key_of_core in dict_of_core.keys():
            if "sentence" in key_of_core:
                subsentence = dict_of_core[key_of_core]

                syntax_of_sentence[key_of_core] = dict()
                subsentence_syntax_analyze = main_terms_analyzer(subsentence)

                syntax_of_sentence[key_of_core]["subjects"] = subsentence_syntax_analyze[0]
                syntax_of_sentence[key_of_core]["predicates"] = subsentence_syntax_analyze[1]

                sentence_paths = paths(subsentence)
                for path in sentence_paths:
                    if path[-1] == "sentence" and ("indirect-object" in path or "direct-object" in path
                                                   or "definition" in path):
                        indirect_object_subsentence = subsentence
                        for key in path:
                            indirect_object_subsentence = indirect_object_subsentence[key]

                        if indirect_object_subsentence["_type"] in ["core", "predicate", "subject"]:
                            syntax_of_sentence[f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"] = \
                                dict()
                            indirect_object_subsentence_syntax_analyze = main_terms_analyzer(
                                indirect_object_subsentence)

                            syntax_of_sentence[f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"][
                                "subjects"] \
                                = indirect_object_subsentence_syntax_analyze[0]
                            syntax_of_sentence[f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"][
                                "predicates"] \
                                = indirect_object_subsentence_syntax_analyze[1]
                            ind_of_indirect_object_subsentence += 1
                        else:
                            indirect_object_subsentence_keys = indirect_object_subsentence.keys()
                            for key_of_subsentence in indirect_object_subsentence_keys:
                                if "sentence" in key_of_subsentence:
                                    temp_subsentence = indirect_object_subsentence[key_of_subsentence]
                                    syntax_of_sentence[
                                        f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"] = dict()

                                    indirect_object_temp_subsentence_syntax_analyze = main_terms_analyzer(
                                        temp_subsentence)

                                    syntax_of_sentence[
                                        f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"][
                                        "subjects"] \
                                        = indirect_object_temp_subsentence_syntax_analyze[0]
                                    syntax_of_sentence[
                                        f"indirect-object-subsentence-{ind_of_indirect_object_subsentence}"][
                                        "predicates"] \
                                        = indirect_object_temp_subsentence_syntax_analyze[1]
                                    ind_of_indirect_object_subsentence += 1

    return syntax_of_sentence


if __name__ == "__main__":
    print(syntax_analyzer(
        "Командир 4 роты Кавказского ж. д. батальона капитан Зивидзикин прислал в Новороссийский комитет по оказанию помощи пострадавшим от войны героям официальную бумагу, в которой сообщает, что от уполномоченного гор. Новороссийска г-на Криницкого 28 декабря 1914 года им было получено для нижних чинов следующие подарки: 2 мешка по 88 кисетов, ящики № 23, 12, 17 и 50 кусков сала."))
    print(syntax_analyzer(
        "Командир 4 роты Кавказского ж. д. батальона капитан Зивидзикин прислал в Новороссийский комитет по оказанию помощи пострадавшим от войны героям официальную бумагу, в которой сообщает, что от уполномоченного гор."))
    print(syntax_analyzer(
        "Новороссийска г-на Криницкого 28 декабря 1914 года им было получено для нижних чинов следующие подарки: 2 мешка по 88 кисетов, ящики № 23, 12, 17 и 50 кусков сала."))
