# KerbalCompute
Orbital Mechanics tools for Kerbal Space Program


```
>>> CONST.MUN.Apo
12000000
>>> CONST.MOHO.Incl
7
>>> CONST.TYLO.get_orbit(CONST.JOOL).period.seconds
211926.35960020457
>>> o = CONST.LAYTHE.get_orbit(CONST.JOOL)
>>> o.apoapsis
21184000
>>> o.periapsis
21184000
>>> o.apoapsis = 20000000
>>> o.apoapsis
21184000
>>> o.periapsis
20000000
>>> o.eccentricity
0.022262334536702677
>>> o.period
(2, 2, 14, 19)
>>> o.period.seconds
51259.648517710055


```


