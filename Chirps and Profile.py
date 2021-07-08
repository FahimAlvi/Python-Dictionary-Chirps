from typing import List, Dict, Tuple


def create_profile_dictionary(file_name: str) \
        -> Dict[int, Tuple[str, List[int], List[int]]]:
    """
    Opens the file "file_name" in working directory and reads the content into a
    profile dictionary as defined on Page 2 Functions 1.

    Note, some spacing has been added for human readability.

    >>> create_profile_dictionary("profiles.txt")
    {100: ('Mulan', [300, 500], [200, 400]),
    200: ('Ariel', [100, 500], [500]),
    300: ('Jasmine', [500], [500, 100]),
    400: ('Elsa', [100, 500], []),
    500: ('Belle', [200, 300], [100, 200, 300, 400])}
    """
    profile_dict = {}
    profile_file = open(file_name, "r")

    line_number = 0
    userID = 0
    userName = None
    userFollowers = []
    userFollowed = []

    for line in profile_file:
        if line == "\n" and line_number == 4:
            line_number = 0
            userID = 0
            userName = None
            userFollowers = []
            userFollowed = []
            continue

        if userID == 0 and line_number == 0:  # 0 ache meaning userID akhono read kora hoyni
            userID = int(line)
            line_number += 1
            continue

        if userName is None and line_number == 1:
            userName = line.replace("\n", "")
            line_number += 1
            continue

        if userFollowers == [] and line_number == 2:
            userFollowers = line.replace("\n", "").replace(
                " ", "").split(",") if line != "\n" else []
            line_number += 1
            continue

        if userFollowed == [] and line_number == 3:
            userFollowed = line.replace("\n", "").replace(
                " ", "").split(",") if line != "\n" else []
            line_number += 1

        profile_dict[userID] = (userName, userFollowers, userFollowed)

    return profile_dict


def create_chirp_dictionary(file_name: str) \
        -> Dict[int, Tuple[int, str, List[str], List[int], List[int]]]:
    """
    Opens the file "file_name" in working directory and reads the content into a
    chirp dictionary as defined on Page 2 Functions 2.

    Note, some spacing has been added for human readability.

    >>> create_chirp_dictionary("chirps.txt")
    {100000: (
        400,
        'Does not want to build a %SnowMan %StopAsking',
        ['SnowMan', 'StopAsking'],
        [100, 200, 300],
        [400, 500]),
    100001: (
        200,
        'Make the ocean great again.',
        [''],
        [],
        [400]),
    100002: (
        500,
        "Help I'm being held captive by a beast!  %OhNoes",
        ['OhNoes'],
        [400],
        [100, 200, 300]),
    100003: (
        500,
        "Actually nm. This isn't so bad lolz :P %StockholmeSyndrome",
        ['StockholmeSyndrome'],
        [400, 100],
        []),
    100004: (
        300,
        'If some random dude offers to %ShowYouTheWorld do yourself a favour and %JustSayNo.',
        ['ShowYouTheWorld', 'JustSayNo'],
        [500, 200],
        [400]),
    100005: (
        400,
        'LOLZ BELLE.  %StockholmeSyndrome  %SnowMan',
        ['StockholmeSyndrome', 'SnowMan'],
        [],
        [200, 300, 100, 500])}
    """
    chirp_dict = {}
    chirp_file = open(file_name, "r")

    line_number = 0
    chirpID = 0
    userID = 0
    message = None
    tags = []
    likes = []
    dislikes = []

    for line in chirp_file:
        if line == "\n" and line_number == 6:
            line_number = 0
            chirpID = 0
            userID = 0
            message = None
            tags = []
            likes = []
            dislikes = []
            continue

        if chirpID == 0 and line_number == 0:
            temp = line.replace("\n", "")
            chirpID = int(temp)
            line_number += 1
            continue

        if userID == 0 and line_number == 1:
            temp = line.replace("\n", "")
            userID = int(temp)
            line_number += 1
            continue

        if message is None and line_number == 2:
            message = line.replace("\n", "")
            line_number += 1
            continue

        if tags == [] and line_number == 3:
            tags = line.replace("\n", "").replace(
                " ", "").split(",") if line != "\n" else []
            line_number += 1
            continue

        if likes == [] and line_number == 4:
            likes = line.replace("\n", "").replace(
                " ", "").split(",") if line != "\n" else []
            line_number += 1
            continue

        if dislikes == [] and line_number == 5:
            dislikes = line.replace("\n", "").replace(
                " ", "").split(",") if line != "\n" else []
            line_number += 1

        chirp_dict[chirpID] = (userID, message, tags, likes, dislikes)

    return chirp_dict


def get_top_chirps(
        profile_dictionary: Dict[int, Tuple[str, List[int], List[int]]],
        chirp_dictionary: Dict[int, Tuple[int, str, List[str], List[int], List[int]]],
        user_id: int) \
        -> List[str]:
    """
    Returns a list of the most liked chirp for every user user_id follows.
    See Page 3 Function 3 of th .pdf.
    >>> profile_dictionary = create_profile_dictionary("profiles.txt")
    >>> chirp_dictionary   = create_chirp_dictionary("chirps.txt")
    >>> get_top_chirps(profile_dictionary, chirp_dictionary, 300)
    ["Actually nm. This isn't so bad lolz :P %StockholmeSyndrome"]
    >>> get_top_chirps( profiles, chirps, 500 )
    ['Make the ocean great again.',
    'If some random dude offers to %ShowYouTheWorld do yourself a favour and %JustSayNo.',
    'Does not want to build a %SnowMan %StopAsking']
    """
    if user_id not in profile_dictionary:
        return []

    user_data = profile_dictionary.get(user_id)
    if not user_data:
        return []

    followed = map(int, user_data[2])
    most_liked_chirps = list()

    for f in followed:
        all_chirps = dict()
        for chirpID in chirp_dictionary:
            if chirp_dictionary[chirpID][0] == f:
                all_chirps[chirpID] = chirp_dictionary[chirpID]

        most_likes = -1
        temp_chirp = None

        for cid in all_chirps:
            if len(all_chirps[cid][3]) > most_likes:
                most_likes = len(all_chirps[cid][3])
                temp_chirp = all_chirps[cid][1]

        if temp_chirp is not None:
            most_liked_chirps.append(temp_chirp)

    return most_liked_chirps


def create_tag_dictionary(
        chirp_dictionary: Dict[int, Tuple[int, str, List[str], List[int], List[int]]]) -> Dict[
    str, Dict[int, List[str]]]:
    """
    Creates a dictionary that keys tags to tweets that contain them.

    Note, some spacing has been added for human readability.

    >>> chirp_dictionary = create_chirp_dictionary("chirps.txt")
    >>> create_tag_dictionary(chirp_dictionary)
    {'SnowMan': {
        400: ['Does not want to build a %SnowMan %StopAsking', 'LOLZ BELLE.  %StockholmeSyndrome  %SnowMan']},
    'StopAsking': {
        400: ['Does not want to build a %SnowMan %StopAsking']},
    '': {
        200: ['Make the ocean great again.']},
    'OhNoes': {
        500: ["Help I'm being held captive by a beast!  %OhNoes"]},
    'StockholmeSyndrome': {
        500: ["Actually nm. This isn't so bad lolz :P %StockholmeSyndrome"],
        400: ['LOLZ BELLE.  %StockholmeSyndrome  %SnowMan']},
    'ShowYouTheWorld': {
        300: ['If some random dude offers to %ShowYouTheWorld do yourself a favour and %JustSayNo.']},
    'JustSayNo': {
        300: ['If some random dude offers to %ShowYouTheWorld do yourself a favour and %JustSayNo.']}}
    """

    all_tags = list()
    for cid in chirp_dictionary:
        all_tags.extend(chirp_dictionary[cid][2])
    all_tags = list(set(all_tags))

    tag_dictionary = dict()

    for tag in all_tags:
        if tag not in tag_dictionary:
            tag_dictionary[tag] = dict()

        for cid in chirp_dictionary:
            if tag in chirp_dictionary[cid][2]:
                if chirp_dictionary[cid][0] in tag_dictionary[tag]:
                    tag_dictionary[tag][chirp_dictionary[cid][0]].append(chirp_dictionary[cid][1])
                else:
                    tag_dictionary[tag][chirp_dictionary[cid][0]] = [chirp_dictionary[cid][1]]
    return tag_dictionary


def get_tagged_chirps(
        chirp_dictionary: Dict[int, Tuple[int, str, List[str], List[int], List[int]]],
        tag: str) \
        -> List[str]:
    """
    Returns a list of chirps containing specified tag.
    >>> chirp_dictionary = create_chirp_dictionary("chirps.txt")
    >>> get_tagged_chirps(chirp_dictionary, "SnowMan")
    ['Does not want to build a %SnowMan %StopAsking',
    'LOLZ BELLE.  %StockholmeSyndrome  %SnowMan']
    """
    tagged_chirps = list()

    for cid in chirp_dictionary:
        if tag in chirp_dictionary[cid][2]:
            tagged_chirps.append(chirp_dictionary[cid][1])

    return tagged_chirps


