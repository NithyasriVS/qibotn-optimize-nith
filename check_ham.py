import quimb.tensor as qtn

L = 44

H = qtn.ham_1d_heis(L)

print(H)
print(type(H))