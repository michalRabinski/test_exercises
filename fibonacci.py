"""
Created on Wed Aug 14 11:17:48 2019

Author: Michał Rabiński

Description:
    TBD
"""

from datetime import datetime 
import sys

##Input data
# Fibonacci list length
_FIBONACCI_LENGTH = 10000
# Print last element from Fibonacci list? 1 - yes, 0 - no
_PRINT_LAST_FLAG = 1
# Print the size of Fibonacci list? 1 - yes, 0 - no
_PRINT_SIZE_FLAG = 1

def fibonacciFunction(fibLen):    
    # Initialize list with 2 first elements (0,1)
    fibOut = [0] * fibLen
    fibOut[1] = 1  
    # Iterate through list creating following Fibonacci values
    for i in range(2,fibLen):
        fibOut[i] = fibOut[i-1] + fibOut[i-2]
    return fibOut

def fibonacciGenerator(num):
    # Initialize separate variables with 2 first elements (0,1)
    fibPrev, fibNext= 0, 1
    # Generate following items
    for _ in range(num):
        yield fibPrev
        fibPrev, fibNext = fibNext, fibPrev + fibNext   
        
def main():
    
    ##Check a performance of created function called "fibonacciFunction"
    t0_1 = datetime.now()
    # Call fibonacciFunction
    fib_func = fibonacciFunction(_FIBONACCI_LENGTH)
    # Print last element output and/or list size depending on flags states
    if _PRINT_LAST_FLAG == 1: 
        print("Fibonacci function last element output: {}".format(fib_func[-1]))
    if _PRINT_SIZE_FLAG == 1: 
        print("Size of full output: {} bytes".format(sys.getsizeof(fib_func)))
    # Evaluate performance
    t1_1 = datetime.now()
    print("Calling Fibonacci function takes {} microseconds".format((t1_1-t0_1).microseconds))
    
    
    ##Check a performance of created function called "fibonacciGenerator"
    t0_2 = datetime.now()
    # Call fibonacciGenerator
    fib_gen = fibonacciGenerator(_FIBONACCI_LENGTH)
    # Print last element output depending on flag state
    if _PRINT_SIZE_FLAG == 1: 
        print("Size of the generator object: {} bytes".format(sys.getsizeof(fib_gen))) 
    # Extract the list from generator
    fib_gen = [next(fib_gen) for _ in range(_FIBONACCI_LENGTH)]
    # Print last element output and/or list size depending on flags states
    if _PRINT_SIZE_FLAG == 1: 
        print("Size of full output (using generator): {} bytes".format(sys.getsizeof(fib_gen))) 
    if _PRINT_LAST_FLAG == 1: 
        print("Fibonacci generator last element output: {}".format(fib_gen[-1]))
    # Evaluate performance   
    t1_2 = datetime.now()
    print("Calling Fibonacci generator takes {} microseconds".format((t1_2-t0_2).microseconds))         
    
if __name__ == '__main__':
    main()