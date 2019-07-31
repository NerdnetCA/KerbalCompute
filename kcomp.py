
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
        
##################################################################



##################################################################
# Celestial Body Parameters
#

CONST = {
    "KERBOL": {
            "Req": 261600000,
            "SGP": 1.1723328E+18,
            "Gs": 17.1
            
        },    
    "MOHO": {
            "Asm": 5263138304,
            "Req": 250000,
            "SGP": 1.6860938E+11,
            "Gs": 2.7,
            "SRP": 1210000
        },
    "EVE": {
            "Asm": 9832684544,
            "Req": 700000,
            "SGP": 8.1717302E+12,
            "Gs": 16.7,
            "SRP": 80500
        },
    "KERBIN": {
            "Req": 600000,
            "SGP": 3.5316E+12,
            "Asm": 13599840256,
            "Gs": 9.81,
            "SRP": 21549.425
        },
    "MUN": {
            "Req": 200000,
            "SGP": 6.5138398E+10,
            "Asm": 12000000,
            "Gs": 1.63,
            "SRP": 138984.38
        },
    "MINMUS": {
            "Req": 60000,
            "SGP": 1.7658E+9,
            "Asm": 47000000,
            "Gs": 0.491,
            "SRP": 40400
        },
    "DUNA": {
            "Req": 320000,
            "SGP": 3.0136321E+11,
            "Asm": 20726155264,
            "Gs": 2.94,
            "SRP": 65517.859
        },
    "DRES": {
            "Asm": 40839348203,
            "Req": 138000,
            "SGP": 2.1484489E+10,
            "Gs": 1.13,
            "SRP": 34800
        },
    "JOOL": {
            "Req": 6000000,
            "SGP": 2.82528E+14,
            "Asm": 68773560320,
            "Gs": 7.85,
            "SRP": 36000
        },
    "EELOO": {
            "Asm": 90118820000,
            "Req": 210000,
            "SGP": 7.4410815E+10,
            "Gs": 1.69,
            "SRP": 19460
        },
    "GILLY": {
            "Asm": 31500000,
            "Req": 13000,
            "SGP": 8289449.8,
            "Gs": 0.049,
            "SRP": 28255
        },
    "IKE": {
            "Req": 130000,
            "SGP": 1.8568369E+10,
            "Asm": 3200000,
            "Gs": 1.10,
            "SRP": 65517.862
        },
    "LAYTHE": {
            "Asm": 27184000,
            "Req": 500000,
            "SGP": 1.962E+12,
            "Gs": 7.85,
            "SRP": 52980.879
        },
    "VALL": {
            "Asm": 43152000,
            "Req": 300000,
            "SGP": 2.074815E+11,
            "Gs": 2.31,
            "SRP": 105962.09
        },
    "TYLO": {
            "Asm": 68500000,
            "Req": 600000,
            "SGP": 2.82528E+12,
            "Gs": 7.85,
            "SRP": 211926.36
        },
    "BOP": {
            "Asm": 128500000,
            "Req": 65000,
            "SGP": 2.4868349E+9,
            "Gs": 0.589,
            "SRP": 544507.43
        },
    "POL": {
            "Asm": 179890000,
            "Req": 44000,
            "SGP": 7.2170208E+8,
            "Gs": 0.373,
            "SRP": 901902.62
        }
    
    }
##################################################################


##################################################################
# Conversion utils
def km(v):
    return v*1000

def Mm(v):
    return v*1000000

def kerbintime(days=0,hours=0,mins=0,secs=0):
    hours += days*6
    mins += hours*60
    secs += mins*60
    return secs

def oxyfor(fuel):
    return fuel * (OXYTOFUEL)

def massfor(fuel):
    ox = oxyfor(fuel)
    return 0.005*(ox+fuel)

def parameter(bodyname,param):
    return CONST[bodyname][param]

##################################################################



##################################################################
# Decorators
#
def withparam(func):
    def wrapper(bodyname, *args, **kws):
        params = CONST[bodyname]
        params.update(kws)
        p = PBundle(params)
        return func(p)
    return wrapper

##################################################################



##################################################################
# Orbital Mechanics functions
#
@withparam
def calc_Vesc(p):
    if 'radius' in dir(p):
        r = p.radius
    elif 'altitude' in dir(p):
        r = p.Req + p.altitude
    else:
        r = p.Req
    mu = p.SGP
    rv = math.sqrt((2*mu)/r)
    return rv

@withparam
def calc_Vo(p):
    r = p.Req + p.altitude
    if 'semimajor' in dir(p):
        a = p.semimajor
    elif 'apoapsis' in dir(p):
        a = (2*p.Req + p.apoapsis + p.periapsis)/2
    else:
        a = r
    return math.sqrt(p.SGP*((2/r)-(1/a)))

@withparam
def calc_Po(p):
    """ Calculate orbital period, given semimajor axis or
        both apses (from surface of parent body) or
        altitude (from surface) assuming 0 eccentricity or
        radius from centre of parent body assuming 0 eccentricity
        """
    if 'semimajor' in dir(p):
        a = p.semimajor
    elif 'apoapsis' in dir(p):
        a = (2*p.Req + p.apoapsis + p.periapsis)/2
    elif 'altitude' in dir(p):
        a = p.altitude + p.Req
    else:
        a = p.radius
    return Interval(secs=2*math.pi*math.sqrt(a**3/p.SGP))

@withparam
def calc_Asm(p):
    """ Calculate semimajor axis, given orbital period
    """
    t = p.period.seconds if isinstance(p.period, Interval) else p.period
    return math.pow((p.SGP*t**2)/(4*math.pi**2), 1./3.)

##################################################################



