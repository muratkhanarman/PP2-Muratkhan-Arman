class Adam:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def info(self):
         print(self.name, self.age)

a = Adam("Arman", 19)
a.info()