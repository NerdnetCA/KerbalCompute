#!/usr/bin/python

from kcomp import *

o_start = CONST.KERBIN.get_orbit(CONST.KERBOL)

o_final = Orbit(CONST.KERBOL)
o_final.period = Period(days=295)

print("From Kerbin *** ")
print("Target Orbit Period : ",o_final.period)
print("Target Orbit Apo : ",m(o_final.apoapsis))
print("Target Orbit Peri : ",m(o_final.periapsis))
print("***")

o_transfer = o_start.dup()
o_transfer.periapsis = o_final.periapsis
dv_burn1 = o_start.Vo(o_start.apoapsis) - o_transfer.Vo(o_transfer.apoapsis)
dv_burn2 = o_transfer.Vo(o_transfer.periapsis) - o_final.Vo(o_final.apoapsis)
print("Transfer Orbit Period : ",o_transfer.period)
print("First Burn dV :",dv_burn1)
print("Final Burn dV :",dv_burn2)
print("Total dV: ", dv_burn1 + dv_burn2)
print("Launch Interval for %d satellites : %s"%(nsat, syn/nsat))

syn = o_final.get_synodic(o_start)
nsat = 3
print("***")

rp = o_final.period + o_final.period/3
print("Resonant Orbit period :",rp)
o_resonant = Orbit(CONST.KERBOL,o_final.periapsis+1,o_final.periapsis)
o_resonant.tune_apo(rp)
print("Resonant Apo :", m(o_resonant.apoapsis))
print("Resonant Peri :", m(o_resonant.periapsis))

rdv_burn2 =  o_resonant.Vo(o_resonant.periapsis) - o_transfer.Vo(o_transfer.periapsis)
rdv_burn3 = o_resonant.Vo(o_resonant.periapsis) - o_final.Vo(o_final.apoapsis)
print("Resonant transfer burn :",dv_burn1)
print("Resonant Burn 1 :",rdv_burn2)
print("Resonant Final burn :",rdv_burn3)
print("Total dV :",dv_burn1+rdv_burn2+rdv_burn3)
