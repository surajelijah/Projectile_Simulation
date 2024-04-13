
# coding: utf-8

# In[1]:


import os
import googlemaps
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

api='AIzaSyAvJ7UO_JSS9gyDwMQGFhYX3B-rGMZBa2M'
gm=googlemaps.Client(key=api)
src=input("Enter the src: ")
dest=input("Enter the destination: ")

geocode_result=gm.geocode(src)[0]
geocode_result1=gm.geocode(dest)[0]
#print (geocode_result)
#print('\n',geocode_result1)

geocode_result.keys()
geocode_result1.keys()
place=geocode_result['geometry']['location']
place2=geocode_result1['geometry']['location']

print ('\n','\n',place,'\n',place2,'\n')


# In[2]:


import gmaps
gmaps.configure(api_key="AIzaSyAvJ7UO_JSS9gyDwMQGFhYX3B-rGMZBa2M")
marker_locations = [
(place['lat'],place['lng']),
(place2['lat'], place2['lng']),
]
fig = gmaps.figure()
markers = gmaps.marker_layer(marker_locations)
fig.add_layer(markers)
fig


# In[3]:


range=haversine(place['lng'],place['lat'],place2['lng'],place2['lat'])
print ('\n\nDistance/Range is: ',range,"\n\n")


# In[4]:


from math import radians, cos, sin,tan, asin,atan,pi, sqrt
from math import sin, cos, radians
from matplotlib import pyplot as plt

class Cannon:
    def __init__(self, x0, y0, v, angle):
        # current x and y coordinates of the missile
        self.x    = x0
        self.y    = y0
    # current value of velocity components
        self.vx  = v*cos(radians(angle))
        self.vy  = v*sin(radians(angle))

    # acceleration by x and y axes
        self.ax   = 0
        self.ay   = -9.8
    # start time
        self.time = 0

    # these list will contain discrete set of missile coordinates
        self.xarr = [self.x]
        self.yarr = [self.y]
    def updateVx(self, dt):
        self.vx = self.vx + self.ax*dt
        return self.vx
    def updateVy(self, dt):
        self.vy = self.vy + self.ay*dt
        return self.vy
    def updateX(self, dt):
        self.x = self.x + 0.5*(self.vx + self.updateVx(dt))*dt
        return self.x
    def updateY(self, dt):
        self.y = self.y + 0.5*(self.vy + self.updateVy(dt))*dt
        return self.y
    def step(self, dt):
        self.xarr.append(self.updateX(dt))
        self.yarr.append(self.updateY(dt))
        self.time = self.time + dt

def makeShoot(x0, y0, velocity, angle):
    """
    Returns a tuple with sequential pairs of x and y coordinates
    """
    cannon = Cannon(x0, y0, velocity, angle)
    dt = 0.05 # time step
    t = 0 # initial time
    cannon.step(dt)

    ###### THE  INTEGRATION ######
    while cannon.y >= 0:
        cannon.step(dt)
        t = t + dt
    ##############################

    return (cannon.xarr, cannon.yarr)
def graph(velocity,angle):
    x0 = 0
    y0 = 0
    #velocity = 10
    x45, y45 = makeShoot(x0, y0, velocity, angle)
    plt.plot(x45, y45, 'bo-',
        [0, 50000], [0, 50], 'k-' # ground
        )
    plt.xlabel('Range/Horizontal distance (miles)')
    plt.ylabel('Height/Vertical distance (miles)')
    plt.show()

g=9.8
def cal_vel(dist,angle):
    return sqrt((g*dist)/sin(radians(angle)))
def cal_height(dist,angle):
    return ((dist*tan(radians(angle)))/(4*g))

def cal_time_of_flight(dist,angle):
    return sqrt((dist*tan(radians(angle)))/(2*g))

index=0
theta=5
print ('\nIndex','\t','Angle','\t','\t','Velocity','\t','\t','\t','\t','Height','\t','\t','\t','Time of Flight','\n')
while theta <= 85:
    velocity=cal_vel(range,theta)
    height=cal_height(range,theta)
    time_of_flight=cal_time_of_flight(range,theta)
    theta+=5
    index+=1
    print (index,'\t',theta,'\t','\t',velocity,'\t','\t','\t',height,'\t','\t',time_of_flight,'\n')
    graph(velocity,theta)
    print('\n')
    
    


# In[5]:


from math import radians, cos, sin,tan, asin,atan,pi, sqrt
def cal_velocity(dist,time):
    return sqrt((g*time)**2+(dist/time)**2)
def cal_theta(dist,time):
    return atan((g*time**2)/dist)*(180/pi)
time=int(input("Enter the desired time to reach the destination: "))
print ('\nVelociy',cal_velocity(range,time),'\n\nAngle of Projection',cal_theta(range,time))


# In[6]:


from math import radians, cos, sin,tan,atan,asin,atan,pi, sqrt
from math import sin, cos, radians
from math import radians, cos, sin, asin, sqrt

Index=0
Velocity=cal_velocity(range,time)
Angle_of_Projection=cal_theta(range,time)
partitions=time/10
iterator=partitions
print("\n\nIndex","\t","Time interval","\t","Height","\t","\t","Range","\t","\t","\t","Velocity at point","\t","Angle_at_Point","\n")
while iterator<=time:
    hdist=Velocity*(cos(radians(Angle_of_Projection)))*iterator
    vdist=(Velocity*(sin(radians(Angle_of_Projection)))*iterator)-((0.5*g)*iterator**2)
    v_at_pt=sqrt((Velocity*(cos(radians(Angle_of_Projection))))**2 +(Velocity*(sin(radians(Angle_of_Projection)))-(g*(iterator)))**2)
    theta_at_pt=atan((Velocity*(sin(radians(Angle_of_Projection)))-(g*(iterator)))/(Velocity*(cos(radians(Angle_of_Projection)))))
    theta_at_pt=theta_at_pt*(180/pi)
    Index+=1 
    print(Index,"\t",iterator,"\t","\t",vdist,"\t",hdist,"\t",v_at_pt,"\t",theta_at_pt,"\n") 
    iterator+=partitions


# In[7]:


from math import radians, cos, sin,tan,atan,asin,atan,pi, sqrt
from math import sin, cos, radians
from math import radians, cos, sin, asin, sqrt

def atan2(y,x):
    return atan((y/x))

lon1=radians(place['lng'])
lon2=radians(place2['lng'])
lat1=radians(place['lat'])
lat2=radians(place['lat'])
ytemp=sin((lon2-lon1))*cos((lat2))
xtemp=cos((lat1))*sin((lat2))-sin((lat1))*cos((lat2))*cos((lon2-lon1))
brng=atan2(ytemp,xtemp)*(180/pi)
print('\nThe Bearing to be considerd is: ',brng,'\n')

