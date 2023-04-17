#!/usr/bin/env python
import rospy
from std_msgs.msg import String
    
# Publisher to change the 'mode'
def change_mode():
    rospy.init_node('map_maker_pub')
    rospy.loginfo('Node has started')

    pub = rospy.Publisher("change_mode", String)

    current = 'None'

    rate = rospy.Rate(2)

    while not rospy.is_shutdown():
        mode_to_change = raw_input("\nCurrently: {}\n Mode to switch? (c,l,e,s):  ".format(current))
        if mode_to_change not in ['c','l','e','s']:
            print('\ninvalid input\n')
            pass
        else:
            pub.publish(mode_to_change)
            current = mode_to_change
        rate.sleep()

if __name__ == '__main__':
    try:
        change_mode()
    except rospy.ROSInterruptException:
        pass
