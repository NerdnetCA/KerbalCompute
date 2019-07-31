# KerbalCompute
Orbital Mechanics tools for Kerbal Space Program

Examples:

```
Create ship instance with Isp=290s, Dry Mass=20t, Fuel Capacity=360
ship = Ship(290, 20, 360)

Refuel to capacity, implicitly adding oxidizer
ship.refuel()

Set fuel to 300, implicitly setting oxidizer to proper ratio
ship.fuel = 300

Get delta v based on current fuel load
ship.delta_v



```


