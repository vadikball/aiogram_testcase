import json


def words_to_json(file_name: str):
    words = []

    with open(file_name, encoding='utf-8') as file:
        for row in file:
            word = row.lower().split('\n')[0]
            if word:
                words.append(word)

    with open(
            '{0}.json'.format(file_name.split('.')[0]),
        'w'
    ) as file:
        json.dump(words, file)


words_to_json('cenz.txt')
