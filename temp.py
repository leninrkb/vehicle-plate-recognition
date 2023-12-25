from numba import cuda
import numpy as np
from timeit import default_timer as timer

def func(a):
    for i in range(10000000):
        a[i] += 1
    
@cuda.jit
def func2(a):
    idx = cuda.blockIdx.x * cuda.blockDim.x + cuda.threadIdx.x
    

if __name__=="__main__":
    n = 10000000
    a = np.ones(n, dtype=np.float64)
    
    start = timer()
    func(a)
    print("sin GPU:", timer()-start)
    
    start = timer()
    func2(a), n  # Aquí está la corrección
    print("con GPU:", timer()-start)
