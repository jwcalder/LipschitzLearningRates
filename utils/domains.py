import numpy as np
import graphlearning as gl

class domain:
    def __init__(self, fixed_verts=np.zeros((0,2))):
        self.fixed_verts = fixed_verts
    
    def boundary(self):
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
    
    def boundary(self, X, delta=0.1):
        bdy_mask = np.where((X[:,0] > 1-delta) | (X[:,1] > 1-delta))
        return bdy_mask[0]
    
    def winnow(self, X):
        idx = np.where((X[:,0]-0.5)**2+(X[:,1]-0.5)**2 > self.r**2)
        return X[idx[0], :], idx[0]
    

class neumann_triangle(domain):
    def __init__(self, r = 0.1, **kwargs):
        super().__init__(**kwargs)
        self.r = r
    
    
    def boundary(self, X, h):
        dist1 = np.sqrt(X[:,0]**2 + (X[:,1]-1)**2)
        dist2 = np.sqrt((X[:,0]-1)**2 + X[:,1]**2)
        if h == 0:
            bdy_idx = np.array([np.argmin(dist1),np.argmin(dist2)])
        else:
            bdy_idx = np.where((dist1 <= h) | (dist2 <= h))[0]
        return bdy_idx
    
    def winnow(self, X):
        idx = np.where(self.domain_function(X[:,0],X[:,1]) <= 1)[0]
        return X[idx, :], idx
    
    def domain_function(self, x, y):
        return np.absolute(x)**(2/3) + np.absolute(y)**(2/3)
    
    
class neumann_star(domain):
    def __init__(self, r = 0.1, **kwargs):
        super().__init__(**kwargs)
    
    def sample(self, n, usegrid):
        if not usegrid:
            X = 2*gl.rand(4*n, 2) - np.ones((1,2))
        else:
            m = int(np.sqrt(n))
            x,y = np.mgrid[-(m-1):m,-(m-1):m]/(m-1) 
            x,y = x.flatten(),y.flatten()
            X = np.vstack((x,y)).T
        
        X, _ = self.winnow(X)
        return np.vstack((X, self.fixed_verts))
    
    def boundary(self, X, h):
        dist1 = np.sqrt(X[:,0]**2 + (X[:,1]-1)**2)
        dist2 = np.sqrt((X[:,0]-1)**2 + X[:,1]**2)
        dist3 = np.sqrt(X[:,0]**2 + (X[:,1]+1)**2)
        dist4 = np.sqrt((X[:,0]+1)**2 + X[:,1]**2)
        if h == 0:
            bdy_idx = np.array([np.argmin(dist1),np.argmin(dist2),np.argmin(dist3),np.argmin(dist4)])
        else:
            bdy_idx = np.where((dist1 <= h) | (dist2 <= h) | (dist3 <= h) | (dist4 <= h))[0]
        return bdy_idx
    
    def winnow(self, X):
        idx = np.where(self.domain_function(X[:,0],X[:,1]) <= 1)[0]
        return X[idx, :], idx
    
    def domain_function(self, x, y):
        return np.absolute(x)**(2/3) + np.absolute(y)**(2/3)
    
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
