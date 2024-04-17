from qibo import gates, Circuit, hamiltonians

g = gates.X(0)

print(g.matrix())

ham = hamiltonians.XXZ(nqubits=3)
print(type(ham))
#print(ham.matrix())
print(ham.circuit(dt=1e-2))

