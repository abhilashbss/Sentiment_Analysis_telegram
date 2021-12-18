import nltk
import collections
import regex as re


def remove_non_english_words(message, all_words):
    return " ".join(w for w in nltk.wordpunct_tokenize(message) if w.lower() in all_words or not w.isalpha())


def flatten(foo):
    for x in foo:
        if isinstance(x, collections.Iterable) and not isinstance(x, str):
            for y in flatten(x):
                yield y
        else:
            yield x


def clean_text(message):
    return re.sub(r"[^a-zA-Z0-9]+", " ", str(message))


def is_topic_filter(sentence, filter_list):
    for filter_word in filter_list:
        if filter_word.lower() in re.findall(r"[\w']+|[.,!?;]", sentence.lower()):
            return True
    return False
