class Adam:
    def __init__(self, name):
        self.name = name

class Oqushy(Adam):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

s = Oqushy("Arman", "bes")
print(s.name, s.grade)