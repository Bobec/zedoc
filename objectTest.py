# CLASA OBIECT
class Obiect():
    b = ""
    d = ""

a = Obiect()
a.b = "c"
a.d = "e"

for property, value in vars(a).items():
    print(property, ":", value)