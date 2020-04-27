import random

determiners = ['a', 'an', 'all', 'any', 'both', 'each', 'either', 'enough', 'every', 'half', 'her', 'his', 'its', 'least', 'less', 'many', 'more', 'most', 'much', 'my', 'my', 'neither', 'no', 'one', 'two', 'three', 'four', 'five', 'our', 'several', 'some', 'such', 'that', 'the', 'their', 'these', 'this', 'those', 'what', 'which', 'whose', 'your']


def grab_sentences(nSen, fname):
    lines = open(fname, encoding='utf8').read().splitlines()
    x = random.choices(lines, k=nSen)
    return(x)

senList = grab_sentences(1, 'generalchat.txt')
#print(senList)
wordStr = str.senList()
wordL = senStr.split()
print(wordL)
# x = max(wordL, key=len)

# i = random.choices(determiners)
# print('{} {}'.format(i, x))
