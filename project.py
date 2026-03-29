import random
import abc

# --- 1. ABSTRACT BASE CLASS ---
class Entity(abc.ABC):
    @abc.abstractmethod
    def update(self):
        pass

# --- 2. THE ORGANISM HIERARCHY ---
class Organism(Entity):
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.alive = True

    def __str__(self):
        return self.__class__.__name__[0] # Returns 'A' for Animal, 'P' for Plant

class Plant(Organism):
    def update(self):
        # Plants grow energy over time
        self.energy += 2 
        if self.energy > 20: # Reproduction logic
            return "reproduce"

class Animal(Organism):
    def __init__(self, x, y, energy, speed=1):
        super().__init__(x, y, energy)
        self.speed = speed

    def move(self, width, height):
        self.x = max(0, min(width - 1, self.x + random.randint(-1, 1)))
        self.y = max(0, min(height - 1, self.y + random.randint(-1, 1)))
        self.energy -= 1 # Moving costs energy

    def update(self):
        if self.energy <= 0:
            self.alive = False
            return "dead"
        
        if self.energy > 30:
            self.energy /= 2 # Split energy with offspring
            return "reproduce"
        
        return "move"

# --- 3. THE WORLD ENGINE ---
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entities = []

    def spawn(self, entity):
        self.entities.append(entity)

    def run_turn(self):
        new_life = []
        for e in self.entities:
            action = e.update()
            
            if action == "move" and isinstance(e, Animal):
                e.move(self.width, self.height)
            
            elif action == "reproduce":
                # Logic to spawn a new entity of the same type nearby
                child = type(e)(e.x, e.y, e.energy) 
                new_life.append(child)
        
        self.entities.extend(new_life)
        # Professional cleanup: Remove dead organisms
        self.entities = [e for e in self.entities if e.alive]

    def display(self):
        # Create a visual grid
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]
        for e in self.entities:
            grid[e.y][e.x] = str(e)
        
        for row in grid:
            print(" ".join(row))
        print(f"Population: {len(self.entities)}\n" + "-"*20)

# --- 4. EXECUTION ---
if __name__ == "__main__":
    sim_world = World(10, 5)
    
    # Initial Population
    sim_world.spawn(Animal(2, 2, 15))
    sim_world.spawn(Plant(5, 4, 10))

    for turn in range(5):
        print(f"Turn {turn + 1}")
        sim_world.run_turn()
        sim_world.display()




        