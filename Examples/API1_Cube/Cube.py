# IMPORT OPERATIONS
import gp_utilities
from gp_utilities import vector3d as vec

#Main Function
if(__name__ == '__main__'):
    topo = gp_utilities.Topology()      #Assign Topology Class

#Creating surface for each face of the cube
    s0 = topo.add_plane(vec(0, 0.5, 0.5), vec(-0.5,0,0))
    s1 = topo.add_plane(vec(1, 0.5, 0.5), vec( 0.5,0,0))
    s2 = topo.add_plane(vec(0.5, 0, 0.5), vec(0,-0.5,0))
    s3 = topo.add_plane(vec(0.5, 1, 0.5), vec(0, 0.5,0))
    s4 = topo.add_plane(vec(0.5, 0.5, 0), vec(0,0,-0.5))
    s5 = topo.add_plane(vec(0.5, 0.5, 1), vec(0,0, 0.5))

#Corner Creation
    c0 = topo.add_corner(0, 0, 0)     #Corner id 0
    c1 = topo.add_corner(1, 0, 0)     #Corner id 1
    c2 = topo.add_corner(0, 1, 0)     #Corner id 2
    c3 = topo.add_corner(1, 1, 0)     #Corner id 3
    c4 = topo.add_corner(0, 0, 1)     #Corner id 4
    c5 = topo.add_corner(1, 0, 1)     #Corner id 5
    c6 = topo.add_corner(0, 1, 1)     #Corner id 6
    c7 = topo.add_corner(1, 1, 1)     #Corner id 7

#Linking the corners
    topo.link([(c0,c1), (c0,c2), (c2,c3), (c1,c3),
               (c4,c5), (c4,c6), (c6,c7), (c5,c7),
               (c0,c4), (c1,c5), (c2,c6), (c3,c7)])

#Assigning the corners to each of the surface
    c0.assign(s4)
    c0.assign(s2)    #c0.assign_multiple([s4,s2,s0])
    c0.assign(s0)

    c1.assign(s4)
    c1.assign(s2)
    c1.assign(s1)

    c2.assign(s4)
    c2.assign(s3)
    c2.assign(s0)

    c3.assign(s4)
    c3.assign(s3)
    c3.assign(s1)

    c4.assign_multiple([s5,s2,s0])

    c5.assign_multiple([s5,s2,s1])

    c6.assign_multiple([s5,s3,s0])

    c7.assign_multiple([s5,s3,s1])

#Checking validity of the Topology
    topo.is_valid( )

#Writing the fra file
    topo.write_topology("cube.fra")
