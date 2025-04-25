# ServellonP12
# Date : 11/26/2024
# Purpose: Demonstrate how to use a database

# imports
from math import sin, cos, sqrt, radians, atan2
import sqlite3
import wx

# database code

# Establish a connection
conn = sqlite3.connect('points.db')
# Instantiate a cursor
curs = conn.cursor()
sqlCmd = 'SELECT * FROM PointsTable'
curs.execute(sqlCmd)
#placeholder variable for database tuple
points = curs.fetchall()


# Define a class to keep track of a point in space, figure out distance from another point.
class Geopoint:

  # init self constructor with two attributes for the locaiton of the point, include a placeholder description 
  def __init__(self, lat=0, lon=0, description='TBD'):
    '''Initialize objects'''
    self.__lat = lat
    self.__lon = lon
    self.__description= description
  

  # set point method, using point property
  def set_point(self,point):
    '''Setting points'''
    self.__lat = point[0]
    self.__lon = point[1]

  # get point method to return tuple or list with lat and lon
  def get_point(self):
    '''Displaying points'''
    return self.__lat, self.__lon

  # point property
  point = property(get_point,set_point)
  

  # description set and get methods
  def set_description(self, description):
    '''Set description'''
    self.__description = description

  def get_description(self):
    '''Display provided description'''
    return self.__description

  # description property
  description = property(get_description, set_description)

  
  # Distance method, using the point property, that will calculate distance between 
  def distance(self, point):
    '''Calculation for the distance between two points, copied from my P6'''
    # import user and city coordinates

    lat_1 = radians(self.__lat)
    lon_1 = radians(self.__lon)

    lat_2 = radians(point.__lat)
    lon_2 = radians(point.__lon)


    t_lat = lat_2 - lat_1
    t_lon = lon_2 - lon_1
  

    # Distance calculation
    R = 6371

    A = sin(t_lat/2)**2 + cos(lat_1) * cos(lat_2) * sin(t_lon/2)**2

    C = 2 * atan2(sqrt(A), sqrt(1 - A))
    
    D = round(R * C, 2)

    return D


# GUI code

# defining calc function
def calculate(event):
  while True:
    # empty the created lists
    display_list = []
    point_list = []

    try:
      # user input point
      user_lat = float(lat_field.GetValue())
      user_lon = float(lon_field.GetValue())
      # pass in values using constructor
      user_point = Geopoint(user_lat, user_lon)
    
    except ValueError:
      display.Value = "Please enter a numeric coordinate and try again."

    # except Exception as exc:
    #   display.Value = f'Error! {exc}'
      
    # read file list, save in empty list created

    for row in points:
      L1 = list(row)
      L1.pop(0)
      display_list.append(L1)

    # loop to create points to add to points list
    for it in range(len(display_list)):

      # create new points, pass in lat lon and description to append the points into list
      new_point = Geopoint(float(display_list[it][0]), float(display_list[it][1]), display_list[it][2])

      # do the distance function, add the result to list
      try:
        new_point_distance = new_point.distance(user_point)
        point_list.append(new_point_distance)
      except UnboundLocalError:
        display.Value = "Please enter a numeric coordinate and try again."
      
    
    # Iterate through the point list and find the closest point
    try:
      lowest = min(point_list)
    except ValueError:
      pass

    # use the point to reference back to the points to display along with the description, use index method
    try:
      lowest_index = point_list.index(lowest)
      display.Value = ((f'You are closest to {display_list[lowest_index][2]}. They are located at {display_list[lowest_index][0]}, {display_list[lowest_index][1]}.'))
    except UnboundLocalError:
      pass
    break
conn.commit()
conn.close()



# GUI set up
app = wx.App() 
win = wx.Frame(None, title="Distance program", size=(600, 400))
bkg = wx.Panel(win)
infobox = wx.MessageBox("Welcome to my which-city-are-you-closest-to program!\nThis program will ask you to provide a set of latitude and longitude, both in decimal degrees.\nThe program will then output which city you are closet to.", 
                        "Program Intro", wx.OK | wx.ICON_INFORMATION)

# button
calcButton = wx.Button(bkg, label= 'Calculate distance')
calcButton.Bind(wx.EVT_BUTTON, calculate)


# Display program calc and info
display = wx.TextCtrl(bkg, style=wx.TE_MULTILINE)


# GUI needs to have two more text boxes where the user can enter their coordinates
lat_field = wx.TextCtrl(bkg)
lat_field.SetHint('Enter your latitude here')
lon_field = wx.TextCtrl(bkg)
lon_field.SetHint('Enter your longitude here')

# boxsizers for displaying
calculatebox = wx.BoxSizer()
calculatebox.Add(lat_field, proportion=1, flag=wx.EXPAND)
calculatebox.Add(lon_field, proportion=1, flag=wx.EXPAND)
calculatebox.Add(calcButton, proportion=1, flag=wx.EXPAND)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(display, proportion=1,
         flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
vbox.Add(calculatebox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

bkg.SetSizer(vbox)
win.Show()
app.MainLoop()
