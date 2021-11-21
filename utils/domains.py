import numpy as np
import graphlearning as gl

class domain:
    def __init__(self, fixed_verts=np.zeros((0,2))):
        self.fixed_verts = fixed_verts
    
    def boundary_mask(self):
        pass
    
    def sample(self, n, usegrid=False):
        if not usegrid:
            X = gl.rand(n, 2)
        else:
            m = int(np.sqrt(n))
            x,y = np.mgrid[0:m,0:m]/(m-1) 
            x,y = x.flatten(),y.flatten()
            X = np.vstack((x,y)).T
        
        X, _ = self.winnow(X)
        return np.vstack((X, self.fixed_verts))
    
    def winnow(self, X):
        return X, np.arange(X.shape[0])
    
    
class square(domain):
    def __init__(self, r = 0.0, **kwargs):
        super().__init__(**kwargs)
        self.r = r
    
    def boundary_mask(self, X, delta=0.1):
        bdy_mask = np.where((X[:,0] > 1-delta) | (X[:,1] > 1-delta))
        return bdy_mask[0]
    
    def winnow(self, X):
        idx = np.where((X[:,0]-0.5)**2+(X[:,1]-0.5)**2 > self.r**2)
        return X[idx[0], :], idx[0]
    

class neumann_triangle(domain):
    def __init__(self, r = 0.1, **kwargs):
        super().__init__(**kwargs)
        self.r = r
    
    
    def boundary_mask(self, X, delta=0.1):
        dist1 = np.sqrt(X[:,0]**2 + (X[:,1]-1)**2)
        dist2 = np.sqrt((X[:,0]-1)**2 + X[:,1]**2)
        bdy_mask = np.where((dist1 <= delta) | (dist2 <= delta))
        #
        return bdy_mask[0]
    
    def winnow(self, X):
        idx = np.where(X[:,1]<=self.domain_function(X[:,0]))
        return X[idx[0], :], idx[0]
    
    def domain_function(self, x):
        return (1-x**(2/3))**(3/2)
    
    
class circle(domain):
    def __init__(self, r=1.0, m = [0,0], **kwargs):
        super().__init__(**kwargs)
        self.r = r
        self.m = m
    
    def boundary_mask(self, X, delta=0.1):
        bdy_mask = np.where(((X[:,0]-self.m[0])**2 + (X[:,1]-self.m[1])**2) > (self.r - delta)**2)

        return bdy_mask[0]
        
    def winnow(self, X):
        idx = np.where(((X[:,0]-self.m[0])**2 + (X[:,1]-self.m[1])**2)<=self.r**2)
        return X[idx[0], :], idx[0]