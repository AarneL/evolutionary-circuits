#TTL NAND-gate optimization
#Very slow simulation and usually takes somewhere close to 30-40 generations
#to find a working gate
title = 'scs ccs'

#Put SPICE device models used in the simulations here.
models="""
.model 2N3904   NPN(Is=6.734f Xti=3 Eg=1.11 Vaf=74.03 Bf=416.7 Ne=1.259
+               Ise=6.734f Ikf=66.78m Xtb=1.5 Br=.7371 Nc=2 Isc=0 Ikr=0 Rc=1
+               Cjc=3.638p Mjc=.3085 Vjc=.75 Fc=.5 Cje=4.493p Mje=.2593 Vje=.75
+               Tr=239.5n Tf=301.2p Itf=.4 Vtf=4 Xtf=2 Rb=10, level=1)
"""

#5V power supply with series resistance of 10 ohms.
#Bypass capacitor with series resistance of 0.1 ohms.
#10k ohm and 100pF of load
common="""
vtest Vin1 Vin 0
Rload out 0 100k
"""

inputs = ['Vin']
outputs = ['out']

#List of simulations
#Put SPICE simulation options between.control and .endc lines
spice_commands=[
#Functionality
"""
.control
tran 5n 130u
print i(vtest)
.endc
Vpwl1 Vin1 0 0 PWL(0 15 80u 35 100u 35 130u 15)
"""
]

#Dictionary of the availabe parts
parts = {'R':{'nodes':2,'value':(1,1e6)},#Resistors
         'C':{'nodes':2,'value':(1e-12,1e-7)},#Capacitors
         #'L':{'nodes':2,'value':(1e-10,1e-5)},#Inductors
         'Q':{'nodes':3,'model':('2N3904','2N3906')},#NPN/PNP transistors
	 'D':{'nodes':2,'model':('1N4148')},#Diode
         }

def _goal(f,k,**kwargs):
    """k is the name of measurement. eq. v(out)"""
    #Functionality
    if k=='i(vtest)':
        return 0.1

#def _constraint0(f,x,k,**kwargs):
#    return True

#def _weight(x,**kwargs):
#    """Weighting function for scoring"""
#
#    return 0.1

##TTL npn NAND-gate seed circuit
seed="""
R1 Vin Vbase 10k
R2 Vsense 0 10k
Q3 Vin Vbase Vsense 2N3904
Q4 Vbase Vsense 0 2N3904
"""
seed_copies = 1

#len(sweep_ranges) should be equal to len(sweep_parameters). sweep_ranges[i] contains list of values for the parameter defined in sweep_parameters[i].
sweep_parameters = ['R1', 'R2']
sweep_ranges = [[],[]]
for _i, _trash in enumerate(sweep_parameters):
    #d for decades
    for _d in range (0, 4):
       #get ten values for every decade
        for _x in range(1,10):
            sweep_ranges[_i].append(_x*(10**_d))
#Default timeout is too low
timeout=7
population=1000#Too small population might not converge, but is faster to simulate
max_parts=12#Maximum number of parts
max_mutations = 15
elitism=1#Best circuit is copied straight to next generation, default setting
#constraints = [_constraint0,None,None]

mutation_rate=0.70
crossover_rate=0.10

plot_every_generation = True
fitness_function=[_goal]
#fitness_weight=[{'v(out)':_weight,'i(vc)':3000,'i(vpwl1)':1000,'i(vpwl2)':1000},{'v(in1)':0.05},{'v(in2)':0.05}]
#On state output voltage
#extra_value=[(4.5,5.0)]

plot_yrange={'i(vtest)':(-0.1,0.2)}
