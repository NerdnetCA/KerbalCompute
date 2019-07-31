#!/usr/bin/python

import kcomp

asm = kcomp.calc_Asm(kcomp.CONST.MOHO, kcomp.Interval(hours=4,mins=30) )

print(asm)
