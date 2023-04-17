# Vector Map Maker

This package helps you create a vectormap from a gmapping based slam map in rviz. This is based on the "publish point" plugin. The package has both a publisher and a subscriber. The publisher changes the mode:
* 'c' - Closed loop, the shape you are making is intended to be closed
* 'l' - Line, the shape you are making is an open shape composed of lines
* 'e' - End the chain for both closed loop and lines
* 's' - Stop, creates the vectormap file and saves it in tmp/

The publisher is just there to help you see what points it is saving, and get the X,Y coordinates from '\clicked_point'.

## Getting Started
To get started you will need to have a minimum of 5 terminals open:
1. roscore
2. gazebo simulation
3. navigation with slam map
    a. You will need to add the publish point tool in rviz in order for /clicked_point to show up in `rostopic list`
4. make map publisher
5. make map subscriber

You will only interact with the `make_map_pub` window when you need to change modes.
