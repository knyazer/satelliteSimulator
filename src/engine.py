from src.defaults import *

from src.renderer import Renderer
from src.vec import Vec2
from src.empty import emptyFunc

# Function to get multiplier for parameter
def getCorrectValue(dictionary, key, default):
    if (key in dictionary):
        try:
            value = float(dictionary[key])
            return value
        except:
            return default
    return default

# That engine calculates whole math
class Engine():
    def __init__(self, **kwargs):

        # Load defaults
        self.height = getCorrectValue(kwargs, "height", HEIGHT)
        self.radius = getCorrectValue(kwargs, "radius", RADIUS)
        self.velocity = getCorrectValue(kwargs, "velocity", VELOCITY)
        self.mass = getCorrectValue(kwargs, "mass", MASS)
        self.dt = getCorrectValue(kwargs, "dt", SIMULATION_DELTA)
        self.K = getCorrectValue(kwargs, "k", K)
        self.qualityParam = 1000

        # Init variables
        self.pos = Vec2(self.height, 0)
        self.vel = Vec2(0, self.velocity)

        self.renderer = Renderer(self.radius, self.pos.x, self.pos.y)

        self.drag = self.renderer.drag
        self.zoom = self.renderer.zoom

        # Callback for data sending
        self.dataCallback = emptyFunc

        self.isWorking = True
        self.canBeUpdate = True

    def stop(self):
        self.isWorking = False

    def setQuality(self, quality):
        self.qualityParam = quality

    def start(self):
        self.isWorking = True

    def positiveAccelerate(self):
        self.dt *= 1.3

    def negativeAccelerate(self):
        self.dt = self.dt * 0.5 + 1e-6

    def setDataCallback(self, callback):
        self.dataCallback = callback

    def draw(self, painter, event):
        try:
            if self.isWorking and self.canBeUpdated:
                self.dataCallback(self.pos, self.vel, self.mass, self.dt)

        except:
            self.isWorking = True
            self.canBeUpdated = True
            pass

        self.renderer.draw(painter, event)

    def update(self):
        self.canBeUpdated = False
        if not self.isWorking: return

        # Initalize local variables for faster access
        vel = self.vel
        pos = self.pos
        m = self.mass
        K = self.K
        dt = self.dt / self.qualityParam

        # Border of planet
        sqr = self.radius / 2

        # Setup some precalculated constants
        normPlanetMass = G * PLANET_MASS
        normK = K / m
        halfDt = dt / 2

        iterationsCount = int(self.qualityParam / 1000) + 1
        for j in range(iterationsCount):
            for i in range(int(self.qualityParam / iterationsCount)):

                # Precalculate variables values
                szvel = vel.size()
                szpos = pos.size()

                # Check intersection
                if szpos < sqr:
                    self.pos = pos
                    self.vel = vel
                    self.isWorking = False
                    return

                # Some physics
                acc = -pos * normPlanetMass / (szpos * szpos * szpos) - vel * szvel * normK
                pos += (vel + acc * halfDt) * dt
                vel += acc * dt

            # Set updated coordinate and velocity
            self.pos = pos
            self.vel = vel
            self.dataCallback(self.pos, self.vel, self.mass, self.dt)
            self.renderer.addPoint(self.pos.x, self.pos.y)

        self.canBeUpdated = True
