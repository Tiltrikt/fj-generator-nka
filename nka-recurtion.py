def q0(word):
    return q1(word) or q3(word) or False

def q1(word):
    if len(word) > 0:
        match word[0]:
            case '0':
                return q2(word[1:])
            case _:
                return False
    return False

def q2(word):
    if len(word) == 0:
        return True
    return False

def q3(word):
    if len(word) > 0:
        match word[0]:
            case '1':
                return q4(word[1:])
            case _:
                return False
    return False

def q4(word):
    return q5(word) or False

def q5(word):
    if len(word) == 0:
        return True
    return q6(word) or False

def q6(word):
    return q7(word) or q9(word) or False

def q7(word):
    if len(word) > 0:
        match word[0]:
            case '0':
                return q8(word[1:])
            case _:
                return False
    return False

def q8(word):
    if len(word) == 0:
        return True
    return q6(word) or False

def q9(word):
    if len(word) > 0:
        match word[0]:
            case '1':
                return q10(word[1:])
            case _:
                return False
    return False

def q10(word):
    if len(word) == 0:
        return True
    return q6(word) or False

def main():
    word = input("Enter a word: ")
    if q0(word):
        print(f'Word "{word}" accepted')
    else:
        print(f'Word "{word}" rejected')

if __name__=="__main__":
    main()


# _transition_table = {
#     0: {'': {1, 3}, '1': {2, 4}},
#     1: {'0': {2}},
#     2: {},
#     3: {'1': {4}},
#     4: {'': {5}},
#     5: {'': {6}},
#     6: {'': {7, 9}},
#     7: {'0': {8}},
#     8: {'': {6}},
#     9: {'1': {10}},
#     10: {'': {6}}
# }