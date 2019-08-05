
import math


##################################################################
# Variable naming
#

"""

Req - Equatorial Radius (m)
SGP - Standard Gravitational Parameter (m^3/s^2) 
Gs - Surface Gravity (m/s^2)
Asm - Semi-major axis
SRP - Sidereal rotational period
Psid - Sidereal orbital period

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
        
class Vessel(object):
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
    
class Period(object):
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
        
    def __add__(self, interval):
        return Period(secs=self.__seconds + interval.seconds)
        
    def __mul__(self, scalar):
        return Period(secs=self.__seconds * scalar)
        
    def __sub__(self, other):
        return Period(secs=self.__seconds - interval.seconds)
        
    def __truediv__(self, scalar):
        return Period(secs=math.floor(self.__seconds / scalar))
        
    def __lt__(self, other):
        return self.__seconds < other.__seconds
    
    def __le__(self, other):
        return self.__seconds <= other.__seconds
    
    def __eq__(self, other):
        return self.__seconds == other.__seconds
    
    def __ne__(self, other):
        return self.__seconds != other.__seconds
    
    def __gt__(self, other):
        return self.__seconds > other.__seconds
    
    def __ge__(self, other):
        return self.__seconds >= other.__seconds
    
    
        
class CelestialBody(object):
    def __init__(self, asm, apo, peri, req, sgp, gs, srp, incl, aperi, lan, psid):
        self.Asm = asm
        self.Apo = apo
        self.Peri = peri
        self.Req = req
        self.SGP = sgp
        self.μ = sgp
        self.Gs = gs
        self.SRP = srp
        self.Incl = incl
        self.APeri = aperi
        self.LAN = lan
        self.Psid = psid
        
    def Vesc(self, altitude=None, radius=None):
        if radius is not None:
            r=radius
        elif altitude is not None:
            r = altitude + self.Req
        else:
            r=self.Req
        return math.sqrt((2*self.SGP)/r)
    
    def get_orbit(self, parent):
        return Orbit(parent, self.Apo, self.Peri, True)

class Orbit(object):
    def __init__(self, body, apoapsis=100000, periapsis=100000, fromcentre=False):
        self.body = body
        if apoapsis < periapsis:
            apoapsis, periapsis = periapsis, apoapsis
        if fromcentre:
            self.__apoapsis = apoapsis
            self.__periapsis = periapsis
        else:
            self.__apoapsis = apoapsis + body.Req
            self.__periapsis = periapsis + body.Req
    
    def dup(self):
        o = Orbit(self.body, self.__apoapsis, self.__periapsis, True)
        return o
    
    @property
    def apoapsis(self):
        return self.__apoapsis - self.body.Req
    
    @property
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
        if self.__apoapsis < self.__periapsis:
            self.__apoapsis, self.__periapsis = self.__periapsis, self.__apoapsis
        
    @periapsis.setter
    def periapsis(self, v):
        self.__periapsis = v+self.body.Req
        if self.__apoapsis < self.__periapsis:
            self.__apoapsis, self.__periapsis = self.__periapsis, self.__apoapsis

    @property
    def Asm(self):
        return (self.__apoapsis + self.__periapsis)/2
    
    @Asm.setter
    def Asm(self, value):
        self.__apoapsis = self.__periapsis = value/2
        return
    
    @property
    def eccentricity(self):
        return 1-(2/(self.__apoapsis/self.__periapsis + 1))
        
    @property
    def period(self):
        return Period(secs=2*math.pi*math.sqrt(self.Asm**3/self.body.SGP))
        
    @period.setter
    def period(self, interval):
        t = interval.seconds if isinstance(interval, Period) else interval
        a = math.pow((self.body.SGP*t**2)/(4*math.pi**2), 1./3.)
        self.__apoapsis = a
        self.__periapsis = a

    def get_synodic(self, orbit):
        p1 = self.period.seconds
        p2 = orbit.period.seconds
        if p1 > p2:
            p1, p2 = p2, p1
        return Period(secs=1/((1/p1)-(1/p2)))
    
    def tune_peri(self, interval):
        t = interval.seconds if isinstance(interval, Period) else interval
        a = math.pow((self.body.SGP*t**2)/(4*math.pi**2), 1./3.)
        self.__periapsis = (2*a) - self.__apoapsis
        if self.__apoapsis < self.__periapsis:
            self.__apoapsis, self.__periapsis = self.__periapsis, self.__apoapsis
        
    def tune_apo(self, interval):
        t = interval.seconds if isinstance(interval, Period) else interval
        a = math.pow((self.body.SGP*t**2)/(4*math.pi**2), 1./3.)
        self.__apoapsis = (2*a) - self.__periapsis
        if self.__apoapsis < self.__periapsis:
            self.__apoapsis, self.__periapsis = self.__periapsis, self.__apoapsis

    def Vo(self, altitude):
        r = self.body.Req + altitude
        return math.sqrt(self.body.SGP*((2/r)-(1/self.Asm)))
 
    
##################################################################



##################################################################
# Celestial Body Parameters
#

CONST = PBundle({
    "KERBOL": CelestialBody (0,0,0,261600000,1.1723328E+18,17.1,432000,0,0,0,0),
    "MOHO": CelestialBody(5263138304, 6315765981, 4210510628, 250000, 1.6860938E+11, 2.7, 1210000, 7, 15, 70, 2215754),
    "EVE": CelestialBody(9832684544, 9931011387, 9734357701, 700000, 8.1717302E+12, 16.7, 80500, 2.1, 0, 15, 5657995),
    "KERBIN": CelestialBody(13599840256, 13599840256, 13599840256, 600000, 3.5316E+12, 9.81, 21549.425, 0, 0, 0, 9203545),
    "MUN": CelestialBody(12000000, 12000000, 12000000, 200000, 6.5138398E+10, 1.63, 138984.38, 0, 0, 0, 138984),
    "MINMUS": CelestialBody(47000000, 47000000, 47000000, 60000, 1.7658E+9, 0.491, 40400, 6, 38, 78, 1077311),
    "DUNA": CelestialBody(20726155264, 21783189163, 19669121365, 320000, 3.0136321E+11, 2.94, 65517.859, 0.06, 0, 135.5, 17315400),
    "DRES": CelestialBody(40839348203, 46761053692, 34917642714, 138000, 2.1484489E+10, 1.13, 34800, 5, 90, 280, 47893063),
    "JOOL": CelestialBody(68773560320, 72212238387, 65334882253, 6000000, 2.82528E+14, 7.85, 36000, 1.304, 0, 52, 104661432),
    "EELOO": CelestialBody(90118820000, 113549713200, 66687926800, 210000, 7.4410815E+10, 1.69,19460, 6.15, 260, 50, 156992048),
    "GILLY": CelestialBody(31500000, 48825000, 14175000, 13000, 8289449.8, 0.049, 28255, 2.1, 0, 15, 388587),
    "IKE": CelestialBody(3200000, 3296000, 3104000, 130000, 1.8568369E+10, 1.10, 65517.862, 0.2, 0, 0, 65518),
    "LAYTHE": CelestialBody(27184000, 27184000, 27184000, 500000, 1.962E+12, 7.85, 52980.879, 0, 0, 0, 52981),
    "VALL": CelestialBody(43152000, 43152000, 43152000, 300000, 2.074815E+11, 2.31, 105962.09, 0, 0, 0, 105962),
    "TYLO": CelestialBody(68500000, 68500000, 68500000, 600000, 2.82528E+12, 7.85, 211926.36, 0.025, 0, 0, 211926),
    "BOP": CelestialBody(128500000, 158697500, 98302500, 65000, 2.4868349E+9, 0.589, 544507.43, 15, 25, 10, 544507),
    "POL": CelestialBody(179890000, 210624207, 149155794, 44000, 7.2170208E+8, 0.373, 901902.62, 4.25, 15, 2, 901903)
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



