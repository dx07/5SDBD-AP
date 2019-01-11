#!/usr/bin/python3

def comment(f, string):
    f.write("c " + string + "\n")

def header(f, variable, clause):
    f.write("p cnf %d " % variable)
    f.write("%d \n" % clause)

#****************************************************************************#
#-------------------------- Encodage domain [a,b]---------------------------#
#****************************************************************************#

def body_domain(f, c):
    for i in range(1, c):
        f.write("-%d" % i)
        f.write(" %d" % (i + 1))
        f.write(" 0\n")

    f.write("%d 0\n" % c)


def encodeDomain(a, b):
    nb_value = b - a + 1
    f = open("encoding_domain.cnf", "w+")
    comment(f, "encoding domain")
    header(f, nb_value, nb_value)
    body_domain(f, nb_value)
    f.close()

#encodeDomain(7, 21)

#**************************************************************************#
#---------------------------- Encodage X <= Y -----------------------------#
#**************************************************************************#
def body_less(f, c):
    for i in range(1, c):
        f.write("-%d" % i)
        f.write(" %d" % (i + 1))
        f.write(" 0\n")

    f.write("%d 0\n" % c)

    for i in range(c+1, c*2):
        f.write("-%d" % i)
        f.write(" %d" % (i + 1))
        f.write(" 0\n")

    f.write("%d 0\n" % (c*2))

    for i in range(1,c+1):
        f.write("-%d" %(c+i))
        f.write(" %d" %(i))
        f.write(" 0\n")

def encode_less(a, b):
    nb_value = b - a + 1
    f=open("encoding_less.cnf", "w+")
    comment(f, "encoding less")
    header(f,nb_value*2, nb_value*3)
    body_less(f,nb_value)
    f.close()

# encode_less(1,5)

#**************************************************************************#
#---------------------------- Encodage X <= Y -----------------------------#
#**************************************************************************#

# Pour les clause communes à X et Y 
# on prend l'intervalle [max(a,c), min(b,d)] (donc verifier que le max est
# plus petit que le min)
# Si a est plus grand que c on va mettre à 0 les valeurs de Y avant l'indice a

def value_x_to_index(x, a):
    return x - a + 1

def value_y_to_index(y, nb_value_x, c):
    return 1 + nb_value_x + y - c 

def body_general_less(f, nb_value_x, nb_value_y, a, b, c, d):
    e = max(a,c)
    g = min(b,d)

    for i in range(1, nb_value_x):
        f.write("-%d" % i)
        f.write(" %d" % (i + 1))
        f.write(" 0\n")

    f.write("%d 0\n" % nb_value_x)

    for i in range(nb_value_x+1, nb_value_x + nb_value_y):
        f.write("-%d" % i)
        f.write(" %d" % (i + 1))
        f.write(" 0\n")

    f.write("%d 0\n" % (nb_value_x + nb_value_y))

    if c < a:
        if d < a :
            gap = 2
        else:
            gap = 1

        for i in range(1, min(d,a) - c + gap):
            f.write("-%d" %(nb_value_x + i))
            f.write(" 0\n")

    if e < g:
        for i in range(e, g+1):
            f.write("-%d" %(value_x_to_index(i, a)))
            f.write(" %d" %(value_y_to_index(i, nb_value_x, c)))
            f.write(" 0\n")

def calcul_variable_clause(a, b, c, d):
    nb_value_x = b - a + 1
    nb_value_y = d - c +1
    e = max(a,c)
    g = min(b,d)
    nb_variable = nb_value_x + nb_value_y
    nb_clause = nb_value_x + nb_value_y

    if  g - e > 0 :
        nb_clause += g - e + 1
    if c < a :
        if d >= a :
            nb_clause += min(d,a) - c
        else:
            nb_clause += min(d,a) - c + 1

    return nb_variable, nb_clause, nb_value_x, nb_value_y

def encodeGeneralLess(a, b, c, d):
    nb_variable, nb_clause, nb_value_x, nb_value_y = calcul_variable_clause(a, b, c, d)

    f = open("encoding_general_less.cnf", "w+")
    comment(f, "encoding general less")
    header(f, nb_variable, nb_clause)
    body_general_less(f, nb_value_x, nb_value_y, a, b, c, d)
    f.close()

# encodeGeneralLess(4, 9, 2, 7)

#**************************************************************************#
#-------------------------- Encodage X + k <= Y ---------------------------#
#**************************************************************************#

def encodePrecedence(a, b, c, d, k):
    new_a = a + k
    new_b = b + k
    nb_variable, nb_clause, nb_value_x, nb_value_y = calcul_variable_clause(new_a, new_b, c, d)

    f = open("encode_precedence.cnf", "w+")
    comment(f, "encoding precedence")
    header(f, nb_variable, nb_clause)
    body_general_less(f, nb_value_x, nb_value_y, new_a, new_b, c, d)
    f.close()

#**************************************************************************#
#---------------------- Encodage Z => (X + k <= Y) ------------------------#
#**************************************************************************#

def value_x_to_index_implies_precedence(x, a):
    return x - a + 2

def value_y_to_index_implies_precedence(y, nb_value_x, c):
    return 2 + nb_value_x + y - c 

def body_implies_precedence(f, nb_value_x, nb_value_y, z, a, b, c, d):
    e = max(a,c)
    g = min(b,d)

    f.write("%d" %int(z))
    f.write(" 0\n")

    for i in range(2, nb_value_x + 1):
        f.write("-%d" % i)
        f.write(" %d" % (i + 1))
        f.write(" 0\n")

    f.write("%d 0\n" % (nb_value_x + 1))

    for i in range(nb_value_x+2, nb_value_x + nb_value_y+1):
        f.write("-%d" % i)
        f.write(" %d" % (i + 1))
        f.write(" 0\n")

    f.write("%d 0\n" % (nb_value_x + nb_value_y + 1))

    if c < a:
        if d < a :
            gap = 2
        else:
            gap = 1

        for i in range(1, min(d,a) - c + gap):
            f.write("-1 -%d" %(nb_value_x + i))
            f.write(" 0\n")

    if e < g:
        for i in range(e, g+1):
            f.write("-1 -%d" %(value_x_to_index_implies_precedence(i, a)))
            f.write(" %d" %(value_y_to_index_implies_precedence(i, nb_value_x, c)))
            f.write(" 0\n")

def calcul_variable_clause_implies_precedence(a, b, c, d):
    nb_value_x = b - a + 1
    nb_value_y = d - c + 1
    e = max(a,c)
    g = min(b,d)
    nb_variable = nb_value_x + nb_value_y + 1
    nb_clause = nb_value_x + nb_value_y + 1

    if  g - e > 0 :
        nb_clause += g - e + 1
    if c < a :
        if d >= a :
            nb_clause += min(d,a) - c
        else:
            nb_clause += min(d,a) - c + 1

    return nb_variable, nb_clause, nb_value_x, nb_value_y

def encodeImpliesPrecedence(z, a, b, c, d, k):
    if z != 1 and z != -1 :
        raise Exception("1 or -1 dude")
    
    new_a = a + k
    new_b = b + k
    nb_variable, nb_clause, nb_value_x, nb_value_y = calcul_variable_clause_implies_precedence(new_a, new_b, c, d)

    f = open("encoding_implies_precedence.cnf", "w+")
    comment(f, "encode Implies Precedence")

    header(f, nb_variable, nb_clause)
    body_implies_precedence(f, nb_value_x, nb_value_y, z, new_a, new_b, c, d)
    f.close()

encodeGeneralLess(2, 4, 7,9)
encodePrecedence(2, 4, 7, 9, 10)
encodeImpliesPrecedence(1, 2, 4, 7, 9, 10)
