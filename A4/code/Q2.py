from bnetbase import *


A = Variable('A', [True, False])
B = Variable('B', [True, False])
C = Variable('C', [True, False])
D = Variable('D', [True, False])
E = Variable('E', [True, False])
F = Variable('F', [True, False])
G = Variable('G', [True, False])
H = Variable('H', [True, False])
I = Variable('I', [True, False])


PA = Factor("P(A)", [A])
PA.add_values([[True, 0.9],[False,0.1]])

PBAH = Factor("P(B|A,H)", [B,A,H])
PBAH.add_values([[True,True,True, 1.0],[True,True,False,0.0],\
    [True,False,True,0.5],[True,False,False, 0.6],[False,True,True, 0.0],\
        [False,True,False,1.0],[False,False,True,0.5],[False,False,False,0.4]])

PCBG = Factor("P(C|B,G)", [C,B,G])
PCBG.add_values([[True,True,True, 0.9],[True,True,False,0.9],\
    [True,False,True,0.1],[True,False,False,1.0],[False,True,True,0.1],\
        [False,True,False,0.1],[False,False,True,0.9],[False,False,False,0.0]])

PDCF = Factor("P(D|C,F)", [D,C,F])
PDCF.add_values([[True,True,True, 0.0],[True,True,False,1.0],\
    [True,False,True,0.7],[True,False,False,0.2],[False,True,True,1.0],\
        [False,True,False,0.0],[False,False,True, 0.3],[False,False,False,0.8]])

PEC = Factor("P(E|C)", [E,C])
PEC.add_values([[True,True, 0.2],[True,False,0.4],[False, True,0.8],[False, False,0.6]])

PF = Factor("P(F)", [F])
PF.add_values([[True, 0.1],[False,0.9]])

PG = Factor("P(G)", [G])
PG.add_values([[True, 1.0],[False,0.0]])

PH = Factor("P(H)", [H])
PH.add_values([[True, 0.5],[False,0.5]])

PIB = Factor("P(I|B)", [I,B])
PIB.add_values([[True,True, 0.3],[True,False,0.9],[False,True,0.7],[False,False,0.1]])


Q2_1 = BN('Q2.1', [A,B,C,D,E,F,G,H,I], [PA, PBAH, PCBG, PDCF, PEC, PF, PG, PH, PIB])

print('(a).')
A.set_evidence(True)
probs = VE(Q2_1, B, [A])
print('P(b|a) = {} P(-b|a) = {}'.format(probs[0],probs[1]))

print('(b).')
A.set_evidence(True)
probs = VE(Q2_1, C, [A])
print('P(c|a) = {} P(-c|a) = {}'.format(probs[0],probs[1]))

print('(c).')
A.set_evidence(True)
E.set_evidence(False)
probs = VE(Q2_1, C, [A,E])
print('P(c|a,-e) = {} P(-c|a,-e) = {}'.format(probs[0],probs[1]))

print('(d).')
A.set_evidence(True)
F.set_evidence(False)
probs = VE(Q2_1, C, [A,F])
print('P(c|a,-f) = {} P(-c|a,-f) = {}'.format(probs[0],probs[1]))