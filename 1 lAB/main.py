
a, b, c = [int(i) for i in input().split()]
D = b**2 - (4*a*c)
if D == 0:
    x = -1 * b / 2 / a
    print(f'x = {x}')
elif D > 0:
    x1 = (-1 * b + D**0.5) / (2*a)
    x2 = (-1 * b - D**0.5) / (2*a)
    print(f'x1 = {x1} , x2 = {x2}')
else:
    print("Корней нет")
