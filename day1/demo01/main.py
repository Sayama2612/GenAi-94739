import calculator as calc
from calculator import sub
import geometry as geo
import greeting

greeting.greet("Chase")

num1 = int(input("Enter num1 :"))
num2 = int(input("Enter num2 :"))

calc.add(num1, num2)
sub(num1,num2)

len = int(input("Enter Length :"))
br = int(input("Enter Breadth :"))

geo.calc_rect_area(len, br)
geo.calc_rect_peri(len, br)