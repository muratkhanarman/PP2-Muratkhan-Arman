class A:
    def method_a(self):
        print("AAAAAAAAAAAAAAAAA")



class B:
    def method_b(self):
        print("BBBBBBBBBBBBBBBB")

class C(A, B):
    pass
obj = C()
obj.method_a()
obj.method_b()