#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PointStamped
from std_msgs.msg import String

_FILENAME = 'output.vectormap.txt'
data = []

# Save the point clicked into the array 'data'
def map_callback(msg):
    x = msg.point.x
    y = msg.point.y
    data.append([x,y])
    rospy.loginfo('Data point collected: {}, {}'.format(x,y))

# Change modes, telling the output function how to handle different segments of points.
def mode_callback(msg): 
    mode = msg.data
    if mode == 'c':
        rospy.loginfo("The mode was changed to closed loop")
        data.append('c')
    elif mode == 'l':
        rospy.loginfo("The mode was changed to line")
        data.append('l')
    elif mode == 'e':
        rospy.loginfo("The mode was ended")
        data.append('e')
    elif mode == 's':     # Stop saving data points and create the vectormap file
        write_file()

# Iterate through the collected data and save each segment correctly with a start and end point
# for each line.
def write_file():
    x1,y1 = None, None      # Start point
    x2,y2 = None, None      # End point
    xf,yf = None, None      # First point (closed loop only)
    with open('make_vector_map/tmp/'+_FILENAME, 'w') as outfile:
        # Skip the first line with 'n'
        row = 1
        while row < len(data):
            # Treat the following points as a connected line chain
            if data[row] == 'l':
                row += 1
                for point in range(row, len(data)):
                    if data[point+1] != 'e':
                        x1,y1 = data[point]
                        x2,y2 = data[point+1]
                        outfile.write("{}, {}, {}, {}\n".format(x1,y1,x2,y2))
                    else:
                        break

            # Treat the following points as a closed loop chain
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

            # End of the file
            elif data[row] == 's':
                break
            row += 1
    # Clean up/Notify that file is ready
    rospy.loginfo("File is closed")
    sub2.unregister()

if __name__ == '__main__':
    # Subscribe to the publish point tool in rviz and the change mode publisher
    rospy.init_node('map_maker_subscriber')
    sub = rospy.Subscriber('/clicked_point', PointStamped, callback=map_callback)
    sub2 = rospy.Subscriber('/change_mode', String, callback=mode_callback)

    # Initialize the data and notify that the node is running
    data.append('n')
    rospy.loginfo('Node has started')
    rospy.spin()
