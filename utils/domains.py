import numpy as np
import graphlearning as gl

class domain:
    def __init__(self):
        pass
    
    def boundary(self):
        pass
    
    def sample(self):
        pass
     
class square(domain):
    def __init__(self):
        super().__init__()
    
    def sample(self, n, usegrid):
        if not usegrid:
            X = gl.rand(n, 2)
        else:
            m = int(np.sqrt(n))
            x,y = np.mgrid[0:m,0:m]/(m-1) 
            x,y = x.flatten(),y.flatten()
            X = np.vstack((x,y)).T
        return X
    
    def boundary(self, X, h):
        return np.where((X[:,0] > 1-h) | (X[:,1] > 1-h))[0]
    

class neumann_triangle(domain):
    def __init__(self, r = 0.1):
        super().__init__()
    
    def sample(self, n, usegrid):
        if not usegrid:
            X = gl.rand(n, 2)
        else:
            m = int(np.sqrt(n))
            x,y = np.mgrid[0:m,0:m]/(m-1) 
            x,y = x.flatten(),y.flatten()
            X = np.vstack((x,y)).T
        return self.winnow(X)
    
    def boundary(self, X, h):
        dist1 = np.sqrt(X[:,0]**2 + (X[:,1]-1)**2)
        dist2 = np.sqrt((X[:,0]-1)**2 + X[:,1]**2)
        if h == 0:
            bdy_idx = np.array([np.argmin(dist1),np.argmin(dist2)])
        else:
            bdy_idx = np.where((dist1 <= h) | (dist2 <= h))[0]
        return bdy_idx
    
    def winnow(self, X):
        return X[self.domain_function(X[:,0],X[:,1]) <= 1, :]
    
    def domain_function(self, x, y):
        return np.absolute(x)**(2/3) + np.absolute(y)**(2/3)
    
    
class neumann_star(domain):
    def __init__(self, r = 0.1):
        super().__init__()
    
    def sample(self, n, usegrid):
        if not usegrid:
            X = 2*gl.rand(4*n, 2) - np.ones((1,2))
        else:
            m = int(np.sqrt(4*n))
            x,y = np.mgrid[-(m-1):m,-(m-1):m]/(m-1) 
            x,y = x.flatten(),y.flatten()
            X = np.vstack((x,y)).T
        return self.winnow(X)
    
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
        return X[self.domain_function(X[:,0],X[:,1]) <= 1, :]
    
    def domain_function(self, x, y):
        return np.absolute(x)**(2/3) + np.absolute(y)**(2/3)
    
    
    

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
