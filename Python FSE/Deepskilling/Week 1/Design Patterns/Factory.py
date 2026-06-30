class Dog:
    def sound(self):
        print("Dog says: Bark")


class Cat:
    def sound(self):
        print("Cat says: Meow")


class AnimalFactory:
    def get_animal(self, animal):
        if animal == "dog":
            return Dog()
        elif animal == "cat":
            return Cat()
        else:
            return None


factory = AnimalFactory()

animal = factory.get_animal("dog")

if animal:
    animal.sound()
else:
    print("Invalid Animal")