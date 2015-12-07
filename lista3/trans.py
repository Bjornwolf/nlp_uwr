trans_verbs = {}
with open('../data/tranzytywne', 'r') as trans:
    for line in trans:
        trans_verbs[line[:-1]] = True

print len(trans_verbs)

trans_with_forms = open('../data/trans_form', 'w')
genders = ['m1', 'm2', 'm3', 'f', 'n1', 'n2']
with open('../data/morfeuszNKJP.txt', 'r') as morfeusz:
    for line in morfeusz:
        parts = line[:-1].split(' ')
        word = parts[0]
        base = parts[1]
        tags = parts[2:]
        pos = base.rfind(':')
        if pos != -1:
            base = base[:pos]
        if base in trans_verbs:
            for tag in tags:
                if tag[:5] == 'praet' and tag.split(':')[-2] in genders:
                    trans_with_forms.write(word + ' ' + tag + '\n')
