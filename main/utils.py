import math
import string
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def formatIt(sentence):
    whitelist = string.ascii_lowercase + string.digits + ' '
    new_s = ''
    for char in sentence:
        if char in whitelist:
            new_s += char
        else:
            new_s += ' '
    return new_s


def vectorize(sentence):
    sentence = sentence.lower()
    ignore = set(stopwords.words('english'))
    stemmer = WordNetLemmatizer()
    text = []
    words = word_tokenize(sentence)
    stemmed = []
    for word in words:
        if word not in ignore:
            stemmed.append(stemmer.lemmatize(word))
    text.append(' '.join(stemmed))
    return formatIt(" ".join(text))


def cosine_similarity(v1, v2):
    v1 = vectorize(v1)
    v2 = vectorize(v2)
    v1 = Counter(v1.split())
    v2 = Counter(v2.split())
    common = set(v1.keys()) & set(v2.keys())
    numerator = sum([v1[x] * v2[x] for x in common])
    sum1 = sum([v1[x] ** 2 for x in v1.keys()])
    sum2 = sum([v2[x] ** 2 for x in v2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


print(cosine_similarity("One Piece", "One Piece"))
