import pygame
import math

pygame.init()

# Constant
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # window size

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLUE_EARTH = (100, 149, 237)
RED_MARS = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans",16)

pygame.display.set_caption("Solar System Simulation")  # window title name


class Planet:
    AU = 149597870700  # m -> AU
    G = 6.67428e-11
    SCALE = (
        250 / AU
    )  # scale the planets and its orbits to screensize - AU = 100 px    - val: 250
    TIMESTEP = 86400  # timelapse of simulation in terms of days 1dy = 86400sec
    MASS = [
        1.98892 * 10 ** 30,
        3.30 * 10 ** 23,
        4.8685 * 10 ** 24,
        5.9742 * 10 ** 24,
        6.39 * 10 ** 23,
        1.899 * 10 ** 27,
        5.685 * 10 ** 26,
        8.682 * 10 ** 25,
        1.024 * 10 ** 26,
    ]
    VELOCITY = [0, -47.4 * 1000, -35.02 * 1000, 29.783 * 1000, 24.077 * 1000]

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        # self.z = z
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []  # represent/track circular orbit of planet travelled

        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = (
            self.x * self.SCALE + WIDTH / 2
        )  # scale the value of m to au & then draw in middle
        y = (
            self.y * self.SCALE + HEIGHT / 2
        )  # scale the value of m to au & then draw in middle

        if len(self.orbit) >= 2:  # dont draw points >=2
            updated_points = []
            for point in self.orbit:  # draw the orbits
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/self.AU, 3)}AU",1,WHITE)
            win.blit(distance_text,(x-distance_text.get_width()/2,y-distance_text.get_height()/2))

    def gravitationalAttraction(self, otherPlanet):
        other_x, other_y = otherPlanet.x, otherPlanet.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if otherPlanet.sun:
            self.distance_to_sun = distance

        force = (
            self.G * self.mass * otherPlanet.mass / distance ** 2
        )  # force done directly

        # force done is x & y direction of planet -> fx & fy - 40:00
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_pos(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.gravitationalAttraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += (
            total_fx / self.mass * self.TIMESTEP
        )  # F=ma -> a=F/m -> v=Ft/m(u=0)
        self.y_vel += (
            total_fy / self.mass * self.TIMESTEP
        )  # F=ma -> a=F/m -> v=Ft/m(u=0)

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True

    clock = pygame.time.Clock()  # run the game at controlled speed, default pc speed

    sun = Planet(0, 0, 30, YELLOW, Planet.MASS[0])
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, Planet.MASS[1])
    mercury.y_vel = Planet.VELOCITY[1]
    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, Planet.MASS[2])
    venus.y_vel = Planet.VELOCITY[2]
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE_EARTH, Planet.MASS[3])
    earth.y_vel = Planet.VELOCITY[3]
    mars = Planet(-1.542 * Planet.AU, 0, 12, RED_MARS, Planet.MASS[4])
    mars.y_vel = Planet.VELOCITY[4]

    planets = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():  # List events occurs in pygame, take action
            if event.type == pygame.QUIT:  # only user event handled, user exit
                run = False

        for planet in planets:
            planet.update_pos(planets)
            planet.draw(WIN)

        pygame.display.update()  # updates in each loop

    pygame.quit()


if __name__ == "__main__":
    main()
