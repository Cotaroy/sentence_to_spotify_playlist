"""
Contains methods that manipulate words
"""

from thefuzz import fuzz
FILLER_WORDS = {'THE', 'A', 'AN', 'LIKE', 'LIKES', 'BUT',
                'HE', 'HIM', 'HIS', 'SHE', 'HER', 'HERS'
                'I', 'YOU', 'US', 'WE', 'OURS', 'YOURS'}


def merge_filler(words: list[str]) -> list[str]:
    """
    merges filler into next word

    >>> merge_filler(['the', 'ball', 'likes', 'turtles'])
    ['the ball', 'likes turtles']
    >>> merge_filler(['the', 'a', 'her', 'mom'])
    ['the a her mom']
    """
    if len(words) < 2:
        return words

    for j in range(len(words)):
        word = words[j].split(' ')
        if not any([x.upper() not in FILLER_WORDS for x in word]):
            break
        return words

    i = 0
    new = []
    while i < len(words):
        if all([word in FILLER_WORDS for word in words[i].upper().split(' ')]) and i < len(words) - 1:
            new.append(words[i] + ' ' + words[i + 1])
            i += 1
        elif all([word in FILLER_WORDS for word in words[i].upper().split(' ')]) and i == len(words) - 1:
            new[-1] += ' ' + new[i]
        else:
            new.append(words[i])
        i += 1
    return merge_filler(new)


def return_closest(target: str, matches: list[str]) -> int:
    """return the index of the string closest to target from matches"""
    max_so_far = fuzz.ratio(target, matches[0])
    index = 0
    for i in range(1, len(matches)):
        ratio = fuzz.ratio(target, matches[i])
        if ratio > max_so_far:
            max_so_far = ratio
            index = i
    return index
