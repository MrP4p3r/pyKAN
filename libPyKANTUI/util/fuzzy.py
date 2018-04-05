# -*- coding: utf-8 -*-

import heapq


class _heap_item(object):

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __lt__(self, other):
        return self.key < other.key


def find(query, items, accessor=lambda x: x, threshold=0.3, limit=100):
    """Simple fuzzyfinder.

    :param str query:
        Search string.

    :param iterable[T] items:
        Collection of objects which will be filtered by ``query``.

    :param (T) -> str or list[str] accessor:
        Function used to fetch strings from object yielded from ``items``.

    :param float threshold:
        Float from range 0..1 to filter low-scored items.

    :param int limit:
        Limits the number of suggestions.

    """

    suggestions = []

    for item in items:
        item_strings = accessor(item)
        item_strings = item_strings if isinstance(item_strings, list) else [item_strings]

        suggestion = None
        suggestion_score = threshold

        for search_target in item_strings:
            search_target_score = score(search_target, query)
            if search_target_score > suggestion_score:
                suggestion = item
                suggestion_score = search_target_score

        if suggestion is not None:
            heapq.heappush(suggestions, _heap_item(-suggestion_score, suggestion))
            if limit and len(suggestions) >= limit:
                break

    return (item.value for item in suggestions)


def score(string, query, stripspaces=True, ignorecase=True):
    """Returns factor of how ``query`` is similar to string.

    Based on similar function from https://github.com/atom/fuzzaldrin.

    :param str string:
        Suggestion.

    :param str query:
        Search string.

    :param bool stripspaces:
        Removes spaces from strings.

    :param bool ignorecase:
        Case sensetivity.

    """

    if stripspaces:
        string = string.replace(' ', '')
        query = query.replace(' ', '')

    if ignorecase:
        string = string.lower()
        query = query.lower()

    if string in query:
        return 1

    total_character_score = 0
    query_length = len(query)
    string_length = len(string)

    index_in_string = 0

    for character in query:
        lowercase_index = string.find(character.lower())
        uppercase_index = string.find(character.upper())

        min_index = min(lowercase_index, uppercase_index)
        if min_index == -1:
            min_index = max(lowercase_index, uppercase_index)

        index_in_string = min_index
        if index_in_string == -1:
            break

        character_score = 0.1

        if string[index_in_string] == character:
            character_score += 0.1

        if index_in_string == 0 or string[index_in_string] == character:
            character_score += 0.8
        elif string[index_in_string - 1] in ['-', '_', ' ']:
            character_score += 0.7

        string = string[index_in_string + 1: string_length]

        total_character_score += character_score

    query_score = total_character_score / query_length
    result = (query_score * (query_length / string_length) + query_score) / 2

    return result
