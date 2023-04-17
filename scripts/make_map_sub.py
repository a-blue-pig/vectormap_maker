#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PointStamped
from std_msgs.msg import String

_CURR_MODE = None
data = []

# Save the point clicked into the array data
def map_callback(msg):
    x = msg.point.x
    y = msg.point.y
    data.append([x,y])
    rospy.loginfo('Data point collected: {}, {}'.format(x,y))

# Change modes, telling the output function how to handle different segments
def mode_callback(msg): 
    _CURR_MODE = msg.data
    if _CURR_MODE == 'c':
        rospy.loginfo("The mode was changed to closed loop")
        data.append('c')
    elif _CURR_MODE == 'l':
        rospy.loginfo("The mode was changed to line")
        data.append('l')
    elif _CURR_MODE == 'e':
        rospy.loginfo("The mode was ended")
        data.append('e')
    elif _CURR_MODE == 's':
        write_file()

def write_file():
    x1,y1 = None, None
    x2,y2 = None, None
    xf,yf = None, None
    with open('make_vector_map/tmp/output.vectormap.txt', 'w') as outfile:
        row = 1
        while row < len(data):
            if data[row] == 'l':
                row += 1
                for point in range(row, len(data)):
                    if data[point+1] != 'e':
                        x1,y1 = data[point]
                        x2,y2 = data[point+1]
                        outfile.write("{}, {}, {}, {}\n".format(x1,y1,x2,y2))
                    else:
                        break
            elif data[row] == 'c':
                row += 1
                xf,yf = data[row]
                for point in range(row, len(data)):
                    if data[point+1] != 'e':
                        x1,y1 = data[point]
                        x2,y2 = data[point+1]
                        outfile.write("{}, {}, {}, {}\n".format(x1,y1,x2,y2))
                    elif data[point+1] == 'e':
                        x1,y1 = data[point]
                        outfile.write("{}, {}, {}, {}\n".format(x1,y1,xf,yf))
                        break
            elif data[row] == 's':
                break
            row += 1
    rospy.loginfo("File is closed")
    sub2.unregister()

if __name__ == '__main__':
    rospy.init_node('map_maker_subscriber')
    sub = rospy.Subscriber('/clicked_point', PointStamped, callback=map_callback)
    sub2 = rospy.Subscriber('/change_mode', String, callback=mode_callback)
    data.append('n')
    rospy.loginfo('Node has started')
    rospy.spin()