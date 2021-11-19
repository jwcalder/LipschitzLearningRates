import numpy as np
import graphlearning as gl

class domain:
    def __init__(self):
        pass
    
    def boundary_mask(self):
        pass
    
    
class square(domain):
    def __init__(self, r = 0.1):
        super().__init__()
        self.r = r
    
    def sample(self, n):
        X = gl.rand(n, 2)
        return self.winnow(X)
    
    def boundary_mask(self, X, delta=0.1):
        bdy_mask = np.where((X[:,0] > 1-delta) | (X[:,1] > 1-delta))
        return bdy_mask[0]
    
    def winnow(self, X):
        idx = np.where((X[:,0]-0.5)**2+(X[:,1]-0.5)**2 > self.r**2)
        return X[idx[0], :]
    

class neumann_triangle(domain):
    def __init__(self, r = 0.1):
        super().__init__()
        self.r = r
    
    def sample(self, n, usegrid = False):
        if not usegrid:
            X = gl.rand(n, 2)
        else:
            m = int(np.sqrt(n))
            x,y = np.mgrid[0:m,0:m]/(m-1) 
            x,y = x.flatten(),y.flatten()
            X = np.vstack((x,y)).T
        return self.winnow(X)
    
    def boundary_mask(self, X, delta=0.1):
        dist1 = np.sqrt(X[:,0]**2 + (X[:,1]-1)**2)
        dist2 = np.sqrt((X[:,0]-1)**2 + X[:,1]**2)
        bdy_mask = np.where((dist1 <= delta) | (dist2 <= delta))
        #
        return bdy_mask[0]
    
    def winnow(self, X):
        idx = np.where(X[:,1]<=self.domain_function(X[:,0]))
        return X[idx[0], :]
    
    def domain_function(self, x):
        return (1-x**(2/3))**(3/2)
    
    
    
    

# class circle(domain):
#     def __init__(self, r=1):
#         super().__init__()
#         self.r = r
        

#     def sample_points(self, n):
#         X = np.random.uniform(low=-self.r,high=self.r, size=(n,2))
#         r_ind = np.where((X[:,0]**2 + X[:,1]**2)<=self.r)
#         return np.squeeze(X[r_ind,:])  
    
#     def sample_boundary(self, m):
#         alpha =  np.random.uniform(low=-np.pi,high=np.pi, size=(m,))
#         return self.r * np.stack([np.sin(alpha), np.cos(alpha)],axis=1)
    
#     def boundary_idx(self, X):
#         return np.argsort((X[:,0]**2 + X[:,1]**2))
    
#     def grid(self, n):
#         x = np.linspace(0, 1, n)
#         y = np.linspace(0, 1, n)
#         r_ind = np.where((x**2 + y**2)<=self.r)
        
#         xv, yv = np.meshgrid(x, y)