mystring = "hello"
myfloat = 10.0
myint = 20

if mystring == "hello":
    print(f"String: {mystring}")
if isinstance(myfloat, float) and myfloat == 10.0:
    print(f"Float {myfloat:f}")
if isinstance(myint, int) and myint == 20:
    print(f"Integer {myint:d}")
