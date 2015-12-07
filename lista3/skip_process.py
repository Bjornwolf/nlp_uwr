f = open('../data/skipgramy', 'r')

skipgrams = {}
for line in f:
    line = line[:-1].split(' ')
    number = float(line[0])
    w1 = line[1]
    w2 = line[2]
    if number > 20.:
        if w1 in skipgrams:
            skipgrams[w1].append( (w2, number) )
        else:
            skipgrams[w1] = [(w2, number)]

        
