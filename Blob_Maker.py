import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from mpl_toolkits import mplot3d



def mk_blob(**kwargs):
    '''Makes a blob by generating a circle/sphere with a variable radius based
       on a set distribution function and applying Gaussian filter to smooth
       through the data

       **kwargs include:
         dim: dimension options 2d or 3d
         dist: the distribution functions include vonmises, wald, and normal
         value: integer value for the 1st component of each numpy function
         scale: integer value for the 2st component of each numpy function
         size: array size
         sigma: sigma value for the Gaussian filter
         plot: Boolean plot setting

        returns x,y and z(3d only) array values
    '''

    #list of defaults
    dim = '2d'
    dist = 'normal'
    val = 1
    scale = 0
    size = 100
    sigma = 2
    plot = 'False'

    for key, component in kwargs.items():
        if key == 'dim':
            dim = component
        if key == 'dist':
            dist = component
        if key == 'value':
            val = component
        if key == 'size':
            size = component
        if key == 'scale':
            scale = component
        if key == 'sigma':
            sigma = component
        if key == 'plot':
            plot = component

    if ((dist == 'wald') or (dist == 'vonmises')) & (scale == 0):
        scale = 100
    elif scale == 0:
        scale = 0.15
        
    if dim=='3d':    
        if dist=='wald':
            r = np.random.wald(val, scale, size=[size,size])
        elif dist=='vonmises':
            r = np.random.vonmises(val, scale, size=[size,size])
        else:
            r = np.random.normal(val, scale, size=[size,size])
    else:
        if dist=='wald':
            r = np.random.wald(val, scale, size=size)
        elif dist=='vonmises':
            r = np.random.vonmises(val, scale, size=size)
        else:
            r = np.random.normal(val, scale, size=size)

    if dim=='3d':
        
        old_size = size
        size = complex(0, size)
        theta, phi = np.mgrid[0:2*np.pi:size, 0:np.pi:size]

        x = r*np.cos(theta)*np.sin(phi)
        y = r*np.sin(theta)*np.sin(phi)
        z = r*np.cos(phi)

        xx = np.ndarray(shape=(old_size,old_size+1))
        yy = np.ndarray(shape=(old_size,old_size+1))
        zz = np.ndarray(shape=(old_size,old_size+1))

        for i in range(old_size):

            xx[i] = np.append(x[i],x[i,0])
            yy[i] = np.append(y[i],y[i,0])
            zz[i] = np.append(z[i],z[i,-15])


        x = gaussian_filter(xx, sigma=sigma)
        y = gaussian_filter(yy, sigma=sigma)
        z = gaussian_filter(zz, sigma=sigma)


        for i in range(old_size):

            x[i,old_size] = x[i,0]
            y[i,old_size] = y[i,0]
            x[old_size-1,i] = x[0,i]
            y[old_size-1,i] = y[0,i]

    else:
        theta = np.linspace(np.pi/2, 5*np.pi/2, size)

        x = r*np.cos(theta)
        y = r*np.sin(theta)

        x = np.append(x,x[0])
        y = np.append(y,y[0])

        x = gaussian_filter(x, sigma=sigma)
        y = gaussian_filter(y, sigma=sigma)
        x[size] = x[0]
        y[size] = y[0]
    
    if plot:

        if dim=='3d':
            fig = plt.figure(1)
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_wireframe(x,y,z)
            plt.show()
        else:
            fig = plt.figure(2)
            ax = fig.add_subplot(111)
            ax.plot(x,y)
            plt.show()
            
    if dim=='3d':
        return x,y,z
    else:
        return x,y


