import numpy as np

class kernel:
    def __init__(self):
        pass
    

class singular(kernel):
    def __init__(self):
        super().__init__()
    
    def __call__(self, x):
        if type(x) == int:
            return 1
        else:
            return 1/np.sqrt(x)

