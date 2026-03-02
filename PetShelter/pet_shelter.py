# pet_shelter.py - Pet Shelter Management System
# Starter code for e005-exercise-oop

# Imports
import json
import random
import pickle


r"""
Pet Shelter Management System
-----------------------------
A system to manage animals in a pet shelter using OOP principles.

Class Hierarchy:
        Animal (Base Class)
       /       \
    Dog         Cat
   /   \          \
Puppy  ServiceDog  Kitten

Complete the TODO sections to finish the implementation.
"""


# =============================================================================
# Task 1: Base Animal Class
# =============================================================================

class Animal:
    """Base class for all animals in the shelter."""
    
    def __init__(self, name, age, species):
        """
        Initialize an animal.
        
        Args:
            name: The animal's name
            age: Age in years
            species: Type of animal
        """
        self.name = name
        self.age = age
        self.species = species
        self._adopted = False  # Protected attribute
    
    def speak(self):
        """Make a sound. To be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement speak()")
    
    def describe(self):
        """Return a description of the animal."""
        status = "adopted" if self._adopted else "available"
        return f"{self.name} is a {self.age}-year-old {self.species} ({status})"
    
    def adopt(self):
        """Mark the animal as adopted."""
        if self._adopted:
            return f"{self.name} has already been adopted!"
        self._adopted = True
        return f"Congratulations! You adopted {self.name}!"
    
    def is_adopted(self):
        """Check if animal is adopted."""
        return self._adopted

    
    def __str__(self):
        """String representation."""
        return f"{self.species}: {self.name} (Age: {self.age})"


# =============================================================================
# Task 2: Dog and Cat Classes
# =============================================================================

class Dog(Animal):
    """A dog in the shelter."""
    
    def __init__(self, name, age, breed, is_trained=False):
        """
        Initialize a dog.
        
        Args:
            name: Dog's name
            age: Age in years
            breed: Dog breed (e.g., "Golden Retriever")
            is_trained: Whether the dog is house-trained
        """
        super().__init__(name, age, "Dog")
        self.breed = breed
        self.is_trained = is_trained
    
    def speak(self):
        """Dogs bark."""
        return f"{self.name} says Woof! Woof!"
    
    def fetch(self):
        """Dogs can fetch."""
        return f"{self.name} fetches the ball!"
    
    def describe(self):
        """Override to include breed and training."""
        base = super().describe()
        trained = "trained" if self.is_trained else "not trained"
        return f"{base} - {self.breed}, {trained}"
    
    def __repr__(self) -> str:
        return f"{self.name=}, {self.age=}, {self.breed=}, {self.is_trained=}"


class Cat(Animal):
    """A cat in the shelter."""
    
    def __init__(self, name: str, age: int, color: str, is_indoor: bool=True):
        """
        Initialize a cat.
        
        Args:
            name: Cat's name
            age: Age in years
            color: Cat's color/pattern
            is_indoor: Whether the cat is indoor-only
        """
        # Call parent constructor with species="Cat"
        super().__init__(name, age, "Cat")
        # Set self.color
        self.color = color
        # Set self.is_indoor
        self.is_indoor = is_indoor
    
    def speak(self):
        """Cats meow."""
        # Return "{name} says Meow!"
        return f"{self.name} says Meow!"
    
    def scratch(self):
        """Cats scratch."""
        return f"{self.name} scratches the furniture!"
    
    def describe(self):
        """Override to include color and indoor status."""
        # Get base description from parent
        base: str = super().describe()
        # Add color and indoor/outdoor status
        indoor_status: str = "indoor" if self.is_indoor else "outdoor"
        return f"{base} - {self.color}, {indoor_status}"
    
    def __repr__(self) -> str:
        return f"Cat({self.name=}, {self.age=}, {self.color=}, {self.is_indoor=})"


# =============================================================================
# Task 3: Specialized Classes
# =============================================================================

class Puppy(Dog):
    """A puppy (dog under 1 year old)."""
    
    def __init__(self, name, age_months, breed):
        """
        Initialize a puppy.
        
        Args:
            name: Puppy's name
            age_months: Age in months (not years!)
            breed: Puppy breed
        """
        # Convert months to years for parent
        age_years = round(age_months / 12, 1)
        super().__init__(name, age_years, breed, is_trained=False)
        self.age_months = age_months
    
    def speak(self):
        """Puppies yip."""
        return f"{self.name} says Yip! Yip!"
    
    def describe(self):
        """Show age in months for puppies."""
        status = "adopted" if self._adopted else "available"
        return f"{self.name} is a {self.age_months}-month-old {self.breed} puppy ({status})"
    
    def __repr__(self) -> str:
        return f"Puppy({self.name=}, {self.age_months=}, {self.breed=})"


class ServiceDog(Dog):
    """A trained service dog."""
    
    def __init__(self, name: str, age: int, breed: str, service_type: str):
        """
        Initialize a service dog.
        
        Args:
            name: Dog's name
            age: Age in years
            breed: Dog breed
            service_type: Type of service (e.g., "guide", "therapy", "search")
        """
        # Call parent constructor with is_trained=True
        super().__init__(name, age, breed, is_trained=True)
        # Set self.service_type
        self.service_type = service_type
    
    def perform_service(self):
        """Perform the dog's service."""
        # Return "{name} performs {service_type} duties."
        return f"{self.name} performs {self.service_type} duties."
    
    def describe(self):
        """Include service type in description."""
        # Get base description and add service type
        base: str = super().describe()
        return f"{base} - Service Type: {self.service_type}"
    
    def __repr__(self) -> str:
        return f"{self.name=}, {self.age=}, {self.breed=}, {self.service_type=}"


class Kitten(Cat):
    """A kitten (cat under 1 year old)."""
    
    def __init__(self, name: str, age_months: int, color: str):
        """
        Initialize a kitten.
        
        Args:
            name: Kitten's name
            age_months: Age in months
            color: Kitten's color/pattern
        """
        # Convert months to years
        age_years: float = round(age_months/12, 1) 
        # Call parent constructor
        super().__init__(name, age_years, color)
        # Store age_months
        self.age_months = age_months
    
    def speak(self):
        """Kittens mew."""
        # Return "{name} says Mew! Mew!"
        return f"{self.name} says Mew! Mew!"
    
    def describe(self):
        """Show age in months for kittens."""
        # Similar to Puppy.describe()
        status = "adopted" if self._adopted else "available"
        return f"{self.name} is a {self.age_months}-month-old kitten ({status})"
    
    def __repr__(self) -> str:
        return f"{self.name=}, {self.age_months=}, {self.color=}"


# =============================================================================
# Task 4: The Shelter Class
# =============================================================================

# Shelter class helpers
def get_random_dog_name() -> str:
    """Return random dog name"""

    # not tracking animal gender so use random name list for each
    file: str = random.choice(("male-dog-names.json", "female-dog-names.json"))

    # retrieve list of pet names from file
    with open(file, 'r') as f:
        dog_names = json.load(f)

    return random.choice(dog_names)

def get_random_cat_name() -> str:
    """Return random cat name"""

    # retrieve list of pet names from file
    with open("cat-names.json", 'r') as f:
        dog_names = json.load(f)

    return random.choice(dog_names)



class Shelter:
    """Manages the pet shelter."""
    
    def __init__(self, name):
        """Initialize the shelter."""
        self.name = name
        self.animals = []
    
    def add_animal(self, animal):
        """Add an animal to the shelter."""
        self.animals.append(animal)
        return f"{animal.name} has been added to {self.name}"
    

    def load_from_file(self):
        with open("animals.pickle", "rb") as f:
            self.animals = pickle.load(f)

    def save_to_file(self):
        with open("animals.pickle", "wb") as f:
            pickle.dump(self.animals, f)                


    def generate_random_animal(self) -> Animal:
        """
        Generate `num` amount of animals and add them to the shelter.
        """

        # generate randomized attributes to be used
        age: int = random.randint(1, 13)
        age_months: int = random.randint(0, 12)

        breed: str = random.choice(("German Shepherd", "Bulldog", "Labrador Retriever", "Golden Retriever", "French Bulldog", "Husky", "Beagle", "Poodle", "Chihuahua", "Dachshund", "Pug", "Border Collie"))
        color: str = random.choice(("Black", "White", "Brown", "Golden", "Gray"))
        service_type: str = random.choice(("guide", "therapy", "search"))

        is_trained: bool = random.choice((True, False))
        is_indoor: bool = random.choice((True, False))

        animal_types: list[str] = ["Dog", "Cat", "Puppy", "ServiceDog", "Kitten"]

        # Choose random animal type, then create and return instance with appropriate attributes
        match random.choice(animal_types):
            case "Dog":
                # name, age, breed, is_trained
                return Dog(get_random_dog_name(), age, breed, is_trained)
            case "Cat":
                # name, age, color, is_indoor
                return Cat(get_random_cat_name(), age, color, is_indoor)
            case "Puppy":
                # name, age_months, breed
                return Puppy(get_random_dog_name(), age_months, breed)
            case "ServiceDog":
                # name, age, breed, service_type
                return ServiceDog(get_random_dog_name(), age, breed, service_type)
            case "Kitten":
                # name, age_months, color
                return Kitten(get_random_cat_name(), age_months, color)

    
    def find_by_name(self, name: str):
        """Find an animal by name."""
        # Loop through animals and return one with matching name
        matches: list = [animal for animal in self.animals if animal.name == name]
        if len(matches) == 0:
            # Return None if animal not found
            return None
        return matches[0]
        
    
    def list_available(self):
        """List all animals available for adoption."""
        # Return list of animals where is_adopted() is False
        return list(filter(lambda x: not x.is_adopted(), self.animals))
    
    def list_by_species(self, species: str):
        """List all animals of a specific species."""
        # Filter self.animals by species
        return list(filter(lambda x: x.species == species, self.animals))
    
    def adopt_animal(self, name):
        """Adopt an animal by name."""
        animal = self.find_by_name(name)
        if animal:
            return animal.adopt()
        return f"No animal named {name} found."
    
    def make_all_speak(self):
        """Demonstrate polymorphism - all animals speak."""
        print(f"\n--- {self.name} Choir ---")
        for animal in self.animals:
            print(f"  {animal.speak()}")
    
    def get_statistics(self):
        """Return shelter statistics."""
        total = len(self.animals)
        adopted = sum(1 for a in self.animals if a.is_adopted())
        available = total - adopted
        
        species_count = {}
        for animal in self.animals:
            species = animal.species
            species_count[species] = species_count.get(species, 0) + 1
        
        return {
            "total": total,
            "adopted": adopted,
            "available": available,
            "by_species": species_count
        }
    
    def display_all(self):
        """Display all animals."""
        print(f"\n{'='*50}")
        print(f"  {self.name} - Current Residents")
        print(f"{'='*50}")
        for i, animal in enumerate(self.animals, 1):
            print(f"{i}. {animal.describe()}")
        print(f"{'='*50}")


# =============================================================================
# Task 5: Demonstration
# =============================================================================

def demonstrate_functionality(shelter: Shelter) -> None:
    """Demonstrate the Shelter classes functionality"""

    # Add various animals (using completed classes)
    shelter.add_animal(Dog("Buddy", 3, "Golden Retriever", True))
    # Add a Cat
    shelter.add_animal(Cat("Rihanna Kitty", 1, "White"))
    # Add a Puppy
    shelter.add_animal(Puppy("Oreo", 7, "Border Collie"))
    # Add a ServiceDog
    shelter.add_animal(ServiceDog("Corey", 6, "German Shepherd", "search"))
    # Add a Kitten
    shelter.add_animal(Kitten("Snowball", 3, "Yellow"))


    print(shelter.list_available())
    
    # Display all animals
    shelter.display_all()
    
    # Demonstrate polymorphism
    shelter.make_all_speak()
    
    # Adopt an animal
    print("\n--- Adoption ---")
    print(shelter.adopt_animal("Buddy"))
    
    # Try to adopt again
    print(shelter.adopt_animal("Buddy"))
    
    # Show statistics
    stats = shelter.get_statistics()
    print(f"\n--- Shelter Statistics ---")
    print(f"  Total: {stats['total']}")
    print(f"  Available: {stats['available']}")
    print(f"  Adopted: {stats['adopted']}")
    print(f"  By Species: {stats['by_species']}")


def main():
    """Driver function"""
    
    # Create shelter
    shelter = Shelter("Happy Paws Rescue")

    # demonstrate_functionality(shelter)

    # Add 10 generated animals to shelter
    # for _ in range(10):
    #    shelter.add_animal(shelter.generate_random_animal())

    shelter.load_from_file()
    shelter.display_all()
    # shelter.save_to_file()


    
    


if __name__ == "__main__":
    main()
