import numpy as np

#%%% PART ONE vvvvv
eq1 = [2,3,0,1]
print(np.poly1d(eq1))
print(np.polyval(eq1,x=2))


eq2 = [2,0,1]
dereq = np.polyder(eq2)
print(np.polyval(dereq, x=1))

#%%% PART TWO vvvvv
import numpy as np

def nm(arr, x, prev_x=None):
    xn1 = x - (np.polyval(arr, x) / np.polyval(np.polyder(arr), x))
    print(xn1)  
    
    if prev_x is not None and round(x, 3) == round(prev_x, 3):
        return round(x, 3)
    else:
        return nm(arr, xn1, x)

def main():
    ask = input('Please enter the coefficients of your polynomial separated by commas, with no spaces, EXAMPLE ::: 2x**3 + 3x**2 + 1 == 2,3,0,1: ')
    eq = [int(num) for num in ask.split(',')]
    x = float(input('Please enter an initial guess: '))

    root = nm(eq, x)
    
    print(f"The root found by Newton's Method is: {root:.3f}")
    
    polynomial_roots = np.roots(eq)
    print(f"The roots of the polynomial are: {polynomial_roots}")


main()

#%%% EXAMPLES vvvvv

# x = 2


# eq = np.poly1d([2,3,0,1])
# der = np.polyder([2,3,0,1])
# dereq = np.poly1d(der)

# y1 = np.polyval(eq, x)
# y2 = np.polyval(dereq, x)


# r1 = np.roots([2,3,0,1])
# r2 = np.roots([6,6,0])


# print(eq)
# print(' ')
# print(der)
# print(' ')
# print(dereq)
# print(' ')
# print(y1)
# print(' ')
# print(y2)
# print(' ')
# print(r1)
# print(' ')
# print(r2)