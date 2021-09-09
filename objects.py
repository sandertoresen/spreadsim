"""Objects for simple virus spread simmulation"""
import random
import pygame
from config import INFECTED_TIME, IMMUNE_TIME, INFECTED_SURVIVAL_TIME
from config import INFECTION_DEADLYNESS, INFECTION_CHANCE
from config import WIDTH, HEIGHT, BLACK, GREEN, RED, FPS

class Simmulation():
    """Simmulation, run setup() then run()
        to run the simmulation"""

    def __init__(self, n_nodes, nr_infected, n_size, n_speed):
        super().__init__()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.nodes = pygame.sprite.Group()
        self.n_nodes = n_nodes
        self.nr_infected = nr_infected
        self.n_size = n_size
        self.n_speed = n_speed

    def setup(self):
        """Setup pygame and nodes for simmulation"""
        err = ""
        if self.nr_infected > self.n_nodes:
            err = "Error more infected than nodes created"
        if INFECTED_TIME < INFECTED_SURVIVAL_TIME:
            err = "Infection time can't be longer than infection survival time"

        if err != "":
            print(err)
            exit()

        self.add_nodes()

    def add_nodes(self):
        """Add nodes to the simmulation"""

        # Create healthy and infected nodes
        for _ in range(self.n_nodes):
            infected = False

            # Set node to infected
            if self.nr_infected != 0:
                infected = True
                self.nr_infected -= 1

            node = Node(infected, self.n_size,
                        [random.randrange(0, WIDTH - self.n_size),
                         random.randrange(0, HEIGHT - self.n_size)],
                        pygame.Vector2(random.randrange(1, 100),
                                       random.randrange(1, 100)).normalize(),
                        self.n_speed)
            self.nodes.add(node)

    def run(self):
        """Run the simmulation"""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill(BLACK)
            self.nodes.update(self.nodes)
            self.nodes.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)

            stats = [0, 0, 0]
            for i in self.nodes:
                stats[0] += i.infected
                stats[1] += 1
            stats[2] = self.n_nodes - stats[1]
            pygame.display.set_caption(
                f"Infected: {stats[0]} Alive: {stats[1]} Dead: {stats[2]}")


class Node(pygame.sprite.Sprite):
    """Node in the simmulation, sprite object which is
        either infected or healthy"""

    def __init__(self, infected, n_size, pos, dir, speed):
        super().__init__()
        self.image = pygame.Surface((n_size, n_size))
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = dir
        self.speed = speed
        self.size = n_size

        self.infected = False
        self.infection_time = 0  # time node stays infected

        if infected:  # infect node
            self.__change_state()

        self.immune_time = 0

        self.dead = False
        self.survival_time = 0  # Time untill dead if infected

    def update(self, group):
        """Update function ran each tick"""
        self.move()
        self.infect(group)

    def move(self):
        """Move the node"""
        if self.rect.x + self.size >= WIDTH or self.rect.x <= 0:
            self.dir.x *= -1
        if self.rect.y + self.size >= HEIGHT or self.rect.y <= 0:
            self.dir.y *= -1

        self.rect.x += int(self.dir.x * self.speed)
        self.rect.y += int(self.dir.y * self.speed)

    def infect(self, group):
        """check for collition with infected node"""

        # return if immune
        if self.immune_time >= pygame.time.get_ticks():
            return

        #no longer infected
        if self.infected and self.infection_time <= pygame.time.get_ticks():
            self.__change_state()
            return

        if self.dead and self.survival_time <= pygame.time.get_ticks():
            self.kill()
            return

        if self.infected:  # infected but not dead, return
            return

        collition_group = pygame.sprite.spritecollide(self, group, False)
        for i in collition_group:
            if i != self and i.infected:
                #chance of self beeing infected
                self.infected_contact()

    def infected_contact(self):
        """role if close contact leads
        to immunity or infection and if infection is deadly"""

        #if node is infected
        if self.__disease_roll(INFECTION_CHANCE):
            self.__change_state()
        else:
            #if not infected become immune
            self.immune_time = pygame.time.get_ticks() + IMMUNE_TIME

    def __change_state(self):
        """Turn infected to uninfected and turn uninfected to infected"""
        if self.infected:
            self.infected = False
            self.image.fill(GREEN)
            self.immune_time = pygame.time.get_ticks(
            ) + IMMUNE_TIME  # No longer infected, turn immune
            return

        self.infected = True
        self.image.fill(RED)
        self.infection_time = pygame.time.get_ticks(
        ) + INFECTED_TIME  # time untill not infected

        #roll if disease is deadly
        if self.__disease_roll(INFECTION_DEADLYNESS):
            self.dead = True
            self.survival_time = pygame.time.get_ticks(
            ) + INFECTED_SURVIVAL_TIME  # time before dead

    def __disease_roll(self, percentage):
        """roll for if consequence of disease happens"""
        if random.randrange(1, 100) <= percentage:
            return True
        return False
