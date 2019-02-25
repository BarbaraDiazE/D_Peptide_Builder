# --------------------------------------------------------------
# Generators
# --------------------------------------------------------------

def generate_sequence(data_first, data, peptide_length):
    letters = list(map(lambda x: x[2], data))
    names = list(map(lambda y: y[1], data))
    types = list(map(lambda z: z[0], data))
    A = list(map(lambda w: w[2], data_first))
    num = peptide_length
    if num == '2':
        peps = list(map(lambda pep: f'{A[0]}{pep}', letters))
        return peps
    if num == '3':
        peps = []
        string = list(map(lambda pep: f'{A[0]}{pep}', letters))
        for x0, x1 in [(x0, x1) for x0 in string for x1 in letters]:
            peps.append(x0 + x1)
        return peps
    if num == '4':
        peps = []
        string_2 = []
        string_1 = list(map(lambda pep: f'{A[0]}{pep}', letters))
        for x0, x1 in [(x0, x1) for x0 in string_1 for x1 in letters]:
            string_2.append(x0 + x1)
        for x0, x1 in [(x0, x1) for x0 in string_2 for x1 in letters]:
            peps.append(x0 + x1)
        return peps
    if num == '5':
        peps = []
        string_3 = []
        string_2 = []
        string_1 = list(map(lambda pep: f'{A[0]}{pep}', letters))
        for x0, x1 in [(x0, x1) for x0 in string_1 for x1 in letters]:
            string_2.append(x0 + x1)
        for x0, x1 in [(x0, x1) for x0 in string_2 for x1 in letters]:
            string_3.append(x0 + x1)
        for x0, x1 in [(x0, x1) for x0 in string_3 for x1 in letters]:
            peps.append(x0 + x1)
        return peps
    if num == '6':
        peps = []
        string_4 = []
        string_3 = []
        string_2 = []
        string_1 = list(map(lambda pep: f'{A[0]}{pep}', letters))
        for x0, x1 in [(x0, x1) for x0 in string_1 for x1 in letters]:
            string_2.append(x0 + x1)
        for x0, x1 in [(x0, x1) for x0 in string_2 for x1 in letters]:
            string_3.append(x0 + x1)
        for x0, x1 in [(x0, x1) for x0 in string_3 for x1 in letters]:
            string_4.append(x0 + x1)
        for x0, x1 in [(x0, x1) for x0 in string_4 for x1 in letters]:
            peps.append(x0 + x1) 
        return peps

def generate_names(data_first, data, peptide_length):
    names = list(map(lambda y: y[1], data))
    A = list(map(lambda z: z[1], data_first))
    num = peptide_length
    if num == '2':
        peps = list(map(lambda pep: f'{A[0]} {pep}', names))
        return peps
    if num == '3':
        peps = []
        string = list(map(lambda pep: f'{A[0]} {pep}', names))
        for x0, x1 in [(x0, x1) for x0 in string for x1 in names]:
            peps.append(x0 +" "+ x1)
        return peps
    if num == '4':
        peps = []
        string_2 = []
        string_1 = list(map(lambda pep: f'{A[0]} {pep}', names))
        for x0, x1 in [(x0, x1) for x0 in string_1 for x1 in names]:
            string_2.append(x0 +" "+ x1)
        for x0, x1 in [(x0, x1) for x0 in string_2 for x1 in names]:
            peps.append(x0 +" "+ x1)
        return peps
    if num == '5':
        peps = []
        string_3 = []
        string_2 = []
        string_1 = list(map(lambda pep: f'{A[0]} {pep}', names))
        for x0, x1 in [(x0, x1) for x0 in string_1 for x1 in names]:
            string_2.append(x0 +" "+ x1)
        for x0, x1 in [(x0, x1) for x0 in string_2 for x1 in names]:
            string_3.append(x0 +" "+ x1)
        for x0, x1 in [(x0, x1) for x0 in string_3 for x1 in names]:
            peps.append(x0 +" "+ x1)
        return peps
    if num == '6':
        peps = []
        string_4 = []
        string_3 = []
        string_2 = []
        string_1 = list(map(lambda pep: f'{A[0]} {pep}', names))
        for x0, x1 in [(x0, x1) for x0 in string_1 for x1 in names]:
            string_2.append(x0 +" "+ x1)
        for x0, x1 in [(x0, x1) for x0 in string_2 for x1 in names]:
            string_3.append(x0 +" "+ x1)
        for x0, x1 in [(x0, x1) for x0 in string_3 for x1 in names]:
            string_4.append(x0 +" "+ x1)
        for x0, x1 in [(x0, x1) for x0 in string_4 for x1 in names]:
            peps.append(x0 +" "+ x1)
        return peps
        