# IMPORT OPERATIONS
import os
import gp_utilities

#Find the List of corner IDs in a given corner group
def corner_group_to_id_list(dimension, corner_group):
    id_list = []
    corners = topo.corner_group(corner_group).get_all()
    num_corners = topo.get_num_corners_in_corner_group(corner_group)
    print num_corners
    if dimension == 2:
        for number in range(num_corners/2):
            id_list.append(corners[number].get_id())
    else:
        for number in range(num_corners):
            id_list.append(corners[number].get_id())
    return id_list

#Main Function
if(__name__ == '__main__'):

    topo = gp_utilities.Topology()
#Input Parameters
    cg_to_be_rotated = 1
    sg_to_be_rotated = 1
    inner_group = 2
    outer_group = 3
    center_of_rotation = [0.5, 0, 0]
    axis_of_rotation = [0, 0, -1]

    current_AOA = 0
    final_AOA = 90
    increment = 2

    num_steps = 8
    num_sweeps = 500

#Transform Topology
    while current_AOA <= final_AOA:
        topo.read_topo_file("topology.fra")
        inner_list = corner_group_to_id_list(2, inner_group)
        outer_list = corner_group_to_id_list(2, outer_group)

        # Detach Corner Groups
        for corners in inner_list:
            linked_corners_inner_list = topo.corner(corners).get_links()
            for links in range(len(linked_corners_inner_list)):
                linked_id = linked_corners_inner_list[links].get_id()
                if linked_id in outer_list:
                    topo.unlink([(topo.corner(corners), topo.corner(linked_id))])

        topo.execute("transform_topo -g {} -sg {} -ax {} {} {} {} {} {} -a {}".format(cg_to_be_rotated,
                                 sg_to_be_rotated, center_of_rotation[0], center_of_rotation[1], center_of_rotation[2],
                                 axis_of_rotation[0], axis_of_rotation[1], axis_of_rotation[2], current_AOA))
        cg = topo.get_corner_group(4)
        cg.append(topo.corner_group(inner_group))
        cg.append(topo.corner_group(outer_group))
        cg.rlink()
        topo.write_topology("topology.@{}.fra".format(current_AOA))

# Run Ggrid
        topo.write_schedule_file("topology.@{}.sch".format(current_AOA), num_steps, num_sweeps,
                                 "grid.@{}.grd".format(current_AOA), "dump.tmp")
        Ggrid = "Ggrid topology.@{}.fra".format(current_AOA)
        os.system(Ggrid)

        current_AOA = current_AOA + increment
