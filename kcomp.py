
import math


##################################################################
# Variable naming
#

"""

Req - Equatorial Radius (m)
SGP - Standard Gravitational Parameter (m^3/s^2)
Gs - Surface Gravity (m/s^2)
Asm - Semi-major axis

Vesc - Escape Velocity
Vo - Orbital Velocity
Po - Orbital Period

"""
##################################################################



##################################################################
# Constants
FUELTOOXY = 9.0/11.0
OXYTOFUEL = 11.0/9.0
G0 = 9.80665

##################################################################



##################################################################
# Classes

# Utility class
class PBundle(object):
    def __init__(self, values):
        self.__dict__.update(values)
        
class Ship(object):
    def __init__(self, isp, drymass, fuelcapacity):
        self.isp = isp
        self.drymass = drymass
        self.fuelcapacity = fuelcapacity
        self.oxycapacity = oxyfor(fuelcapacity)
        self.__fuel = 0
        self.__oxy = 0
        
    def refuel(self):
        self.__fuel = self.fuelcapacity
        self.__oxy = self.oxycapacity
        
    @property
    def fuel(self):
        return (self.__fuel, self.__oxy)
    
    @fuel.setter
    def fuel(self, fuel):
        self.__fuel = fuel
        self.__oxy = oxyfor(fuel)
        
    @property
    def totalmass(self):
        return self.drymass + massfor(self.fuel[0])

    @property
    def delta_v(self):
        return self.isp * G0 * math.log(self.totalmass/self.drymass)
    
class Interval(object):
    def __init__(self, days=0, hours=0, mins=0, secs=0):
        hours += days*6
        mins += hours*60
        secs += mins*60        
        self.__seconds = secs
        
    @property
    def seconds(self):
        return self.__seconds
    
    @property
    def time(self):
        mins, secs = divmod(math.floor(self.__seconds), 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 6)
        return (days,hours,mins,secs)
        
    @time.setter
    def time(self, t):
        self.__seconds = t[0]*21600 + t[1]*3600 + t[2]*60 + t[3]        
        
    @seconds.setter
    def seconds(self, s):
        self.__seconds = s
        
    def __repr__(self):
        return str(self.time)
    
    def add(self, days=0, hours=0, mins=0, secs=0):
        hours += days*6
        mins += hours*60
        secs += mins*60
        self.__seconds += secs
        
    def add_interval(self, interval):
        self.__seconds += interval.seconds
        
class CelestialBody(object):
    def __init__(self, asm, req, sgp, gs, srp):
        self.Asm = asm
        self.Req = req
        self.SGP = sgp
        self.Gs = gs
        self.SRP = srp
        
    def Vesc(self, altitude=None, radius=None):
        if radius is not None:
            r=radius
        elif altitude is not None:
            r = altitude + self.Req
        else:
            r=self.Req
        return math.sqrt((2*self.SGP)/r)

class Orbit(object):
    def __init__(self, body, apoapsis=100000, periapsis=100000, fromcentre=False):
        self.body = body
        if fromcentre:
            self.__apoapsis = apoapsis
            self.__periapsis = periapsis
        else:
            self.__apoapsis = apoapsis + body.Req
            self.__periapsis = periapsis + body.Req
    
    @property
    def apoapsis(self):
        return self.__apoapsis - self.body.Req
    
    def apoapsis_f(self):
        return self.__apoapsis
    
    @property
    def periapsis(self):
        return self.__periapsis - self.body.Req
    
    @property
    def periapsis_f(self):
        return self.__periapsis
    
    @apoapsis.setter
    def apoapsis(self, v):
        self.__apoapsis = v+self.body.Req
        
    @periapsis.setter
    def periapsis(self, v):
        self.__periapsis = v+self.body.Req
        
    @property
    def Asm(self):
        return (self.__apoapsis + self.__periapsis)/2
    
    @property
    def eccentricity(self):
        return 1-(2/(self.__apoapsis/self.__periapsis + 1))
        
    @property
    def period(self):
        return Interval(secs=2*math.pi*math.sqrt(self.Asm**3/self.body.SGP))
        
    @period.setter
    def period(self, interval):
        t = interval.seconds if isinstance(interval, Interval) else interval
        a = math.pow((self.body.SGP*t**2)/(4*math.pi**2), 1./3.)
        self.__apoapsis = a
        self.__periapsis = a

    def tune_peri(self, interval):
        t = interval.seconds if isinstance(interval, Interval) else interval
        a = math.pow((self.body.SGP*t**2)/(4*math.pi**2), 1./3.)
        self.__periapsis = (2*a) - self.__apoapsis
        
    def tune_apo(self, interval):
        t = interval.seconds if isinstance(interval, Interval) else interval
        a = math.pow((self.body.SGP*t**2)/(4*math.pi**2), 1./3.)
        self.__apoapsis = (2*a) - self.__periapsis

    def Vo(self, altitude):
        r = self.body.Req + altitude
        return math.sqrt(self.body.SGP*((2/r)-(1/self.Asm)))
 
    
##################################################################



##################################################################
# Celestial Body Parameters
#

CONST = PBundle({
    "KERBOL": CelestialBody (0,261600000,1.1723328E+18,17.1,432000),
    "MOHO": CelestialBody(5263138304, 250000, 1.6860938E+11, 2.7, 1210000),
    "EVE": CelestialBody(9832684544, 700000, 8.1717302E+12, 16.7, 80500),
    "KERBIN": CelestialBody(13599840256, 600000, 3.5316E+12, 9.81, 21549.425),
    "MUN": CelestialBody(12000000, 200000, 6.5138398E+10, 1.63, 138984.38),
    "MINMUS": CelestialBody(47000000, 60000, 1.7658E+9, 0.491, 40400),
    "DUNA": CelestialBody(20726155264, 320000, 3.0136321E+11, 2.94, 65517.859),
    "DRES": CelestialBody(40839348203, 138000, 2.1484489E+10, 1.13, 34800),
    "JOOL": CelestialBody(68773560320, 6000000, 2.82528E+14, 7.85, 36000),
    "EELOO": CelestialBody(90118820000, 210000, 7.4410815E+10, 1.69,19460),
    "GILLY": CelestialBody(31500000, 13000, 8289449.8, 0.049, 28255),
    "IKE": CelestialBody(3200000, 130000, 1.8568369E+10, 1.10, 65517.862),
    "LAYTHE": CelestialBody(27184000, 500000, 1.962E+12, 7.85, 52980.879),
    "VALL": CelestialBody(43152000, 300000, 2.074815E+11, 2.31, 105962.09),
    "TYLO": CelestialBody(68500000, 600000, 2.82528E+12, 7.85, 211926.36),
    "BOP": CelestialBody(128500000, 65000, 2.4868349E+9, 0.589, 544507.43),
    "POL": CelestialBody(179890000, 44000, 7.2170208E+8, 0.373, 901902.62)
    })
##################################################################


##################################################################
# Conversion utils
def km(v):
    return v*1000

def Mm(v):
    return v*1000000

def oxyfor(fuel):
    return fuel * (OXYTOFUEL)

def massfor(fuel):
    ox = oxyfor(fuel)
    return 0.005*(ox+fuel)

##################################################################



