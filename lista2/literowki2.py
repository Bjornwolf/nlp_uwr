
keyboard = ['###qwertyuiop###','###asdfghjkl###', '###zxcvbnm###']
latin = 'qwertyuiopasdfghjklzxcvbnm'
polish = 'ęóąśłżźćń'
unpolish = 'eoaslzxcn'
chars = set(latin + polish)


def build_grams():
    f = open('../data/1grams', 'r')
    words = {}
    for line in f:
        number, word = line[:-1].split(' ')[-2:]
        if len(set(word) - chars) == 0:
            words[word] = int(number)
    return words

def build_dictionary():
    dictionary = {}
    for line in open('../data/slownik', 'r'):
        word = line[:-1]
        dictionary[word] = True
    return dictionary

def near_signs(sign):
    if sign in keyboard[0]:
        i = keyboard[0].find(sign)
        options = [keyboard[0][j] for j in [i-1, i, i+1]]
        options += [keyboard[1][j] for j in [i-1, i]]
    elif sign in keyboard[1]:
        i = keyboard[1].find(sign)
        options = [keyboard[0][j] for j in [i, i+1]]
        options += [keyboard[1][j] for j in [i-1, i, i+1]] 
        options += [keyboard[2][j] for j in [i-1, i]] 
    else:
        i = keyboard[2].find(sign)
        options = [keyboard[1][j] for j in [i, i+1]]
        options += [keyboard[2][j] for j in [i-1, i, i+1]]
    return ''.join(options).replace('#', '')

def generate_typos(word, dictionary):
    def build_ins(word, i):
        if len(word) == 1:
            return None
        if i == 0:
            adj = [1]
        elif i == len(word) - 1:
            adj = [len(word) - 2]
        else:
            adj = [i - 1, i + 1]
        if word[i] in near_signs(word[adj[0]]) + near_signs(word[adj[-1]]):
            return word[:i] + word[i+1:]
        return None

    def build_del(word, i):
        if i == 0:
            adj = [0]
        elif i == word_length:
            adj = [word_length - 1]
        else:
            adj = [i - 1, i]
        results = []
        for letter in near_signs(word[adj[0]]) + near_signs(word[adj[-1]]):
            results.append(word[:i] + letter + word[i:])
        return results

    def build_trans(word, i):
        return word[:i] + word[i+1] + word[i] + word[i+2:], word[i], word[i+1]

    def build_repl(word, i):
        results = []
        for letter in near_signs(word[i]):
            if letter != word[i]:
                results.append( (word[:i] + letter + word[i+1:], word[i], letter) )
        return results

    def build_altplus(word, i):
        opt = polish.find(word[i])
        if opt == -1:
            return None
        return word[:i] + unpolish[opt] + word[i+1:]

    def build_altminus(word, i):
        opt = unpolish.find(word[i])
        if opt == -1:
            return None
        return word[:i] + polish[opt] + word[i+1:]
    
    word_length = len(word)
    built = []
    for i in range(word_length):
        ins_opt = build_ins(word, i)
        try:
            _ = dictionary[ins_opt]
            built.append( (ins_opt, 'ins', None) )
        except KeyError:
            pass

        apl_opt = build_altplus(word, i)
        try:
            _ = dictionary[apl_opt]
            built.append( (apl_opt, 'alt+', None) )
        except KeyError:
            pass 

        amn_opt = build_altminus(word, i)
        try:
            _ = dictionary[amn_opt]
            built.append( (amn_opt, 'alt-', None) )
        except KeyError:
            pass

        for repl_opt, s1, s2 in build_repl(word, i):
            try:
                _ = dictionary[repl_opt]
                built.append( (repl_opt, 'repl', (s1, s2)) )
            except KeyError:
                pass

    for i in range(word_length + 1):
        for del_opt in build_del(word, i):
            try:
                _ = dictionary[del_opt]
                built.append( (del_opt, 'del', None) )
            except KeyError:
                pass

    for i in range(word_length - 1):
        trans_opt, s1, s2 = build_trans(word, i)
        if s1 != s2:
            try:
                _ = dictionary[trans_opt]
                built.append( (trans_opt, 'trans', (s1, s2)) )
            except KeyError:
                pass

    return built

def save_table_to_csv(table, filename):
    charlist = sorted(latin)
    out = open('../data/' + filename, 'w+')
    total = sum(table.values())
    out.write(';')
    for k in charlist:
        out.write(k + ';')
    out.write('\n')
    for k in charlist:
        out.write(k + ';')
        for l in charlist:
            out.write(str(float(table[(k, l)]) / total) + ';')
        out.write('\n')


dictionary = build_dictionary()
words = build_grams()
print(generate_typos('dookoła', dictionary))
lw = len(words)
stats = {}
repl = {}
trans = {}
for l in sorted(latin):
    for k in sorted(latin):
        repl[ (l, k) ] = 0
        trans[ (l, k) ] = 0

for (i, word) in enumerate(words):
    if i % 100000 == 0:
        print(i, ' of ', lw)
    word_cnt = words[word]
    possible_corrections = generate_typos(word, dictionary)
    for correction, error_type, error_details in possible_corrections:
        try:
            c = words[correction]
            if word_cnt < c:
                try:
                    stats[correction][error_type] += word_cnt
                except KeyError:
                    stats[correction] = {'ins': 0, 'del': 0, 'repl': 0, 'trans': 0, 'alt+': 0, 'alt-': 0}
                    stats[correction][error_type] += word_cnt
                if error_type == 'repl':
                    repl[error_details] += word_cnt
                if error_type == 'trans':
                    trans[error_details] += word_cnt
        except KeyError:
            pass
p = {'ins': 0., 'del': 0., 'repl': 0., 'trans': 0., 'alt+': 0., 'alt-': 0.}
N = len(stats)
for key in stats:
    total_row = sum(stats[key].values())
    for error_type in p.keys():
        p[error_type] += float(stats[key][error_type]) / total_row

for error_type in p.keys():
    p[error_type] /= N
print(p)
# mam słownik stats :: {POPRAWNE_SŁOWO -> {RODZAJ_BŁĘDU -> SUMA}}
save_table_to_csv(repl, 'repl.csv')
save_table_to_csv(trans, 'trans.csv')



















