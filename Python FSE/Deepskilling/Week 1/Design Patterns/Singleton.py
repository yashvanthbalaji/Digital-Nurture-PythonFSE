class Singleton:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance


obj1 = Singleton()
obj2 = Singleton()

print(obj1)
print(obj2)

if obj1 == obj2:
    print("Both objects are the same.")
else:
    print("Objects are different.")