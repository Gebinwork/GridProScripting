# IMPORT OPERATIONS
import gp_utilities
from gp_utilities import vector3d as vec
import os
import variables

def topo_modify(corners_along_sphere, sphere_surface_group, corners_around_sphere, translation_for_sphere,
                translation_around_sphere, density_between_spheres, density_after_spheres):
    #Topology_Modification
    topo.execute("transform_topo -g {} -sg {} -t1 {} {} {}".format(corners_along_sphere, sphere_surface_group,
                                                                                   translation_for_sphere.get_component(0),translation_for_sphere.get_component(1),
                                                                                   translation_for_sphere.get_component(2)))
    topo.execute("transform_topo -g {} -t1 {} {} {}".format(corners_around_sphere, translation_around_sphere.get_component(0),
                                                                            translation_around_sphere.get_component(1), translation_around_sphere.get_component(2)))

    #Density_Modification_between_spheres
    den = topo.den()
    den.set_density(topo.corner(variables.corners_between_spheres[0]), topo.corner(variables.corners_between_spheres[1]), density_between_spheres)
    den.set_density(topo.corner(variables.corners_between_spheres[1]), topo.corner(variables.corners_between_spheres[2]), density_between_spheres)

    #Density_Modification_after_spheres
    den.set_density(topo.corner(variables.corners_after_spheres[0]), topo.corner(variables.corners_after_spheres[1]), density_after_spheres)
    den.set_density(topo.corner(variables.corners_after_spheres[1]), topo.corner(variables.corners_after_spheres[2]), density_after_spheres)
    return topo

def write_schedule_file():
    #Write_schedule_file
    file = open("{}.sch".format(output_file_prefix), "w+")
    file.writelines("step {}: -c all 1.0 0 -C all 1.0 24 -r -S {} -w "
                    "\nstep {}: -sys 'ws qchk {}.grd 11 10000 {} 120' "
                    "\nstep {}: -sys 'python Quality.py {}.sch'"
                    "\nwrite -f {}.grd".format(variables.step_count, variables.sweep_count, variables.step_count+1,
                                               output_file_prefix, variables.skewness, variables.step_count+2,
                                               output_file_prefix, output_file_prefix))
    file.close()


#Main Function
if(__name__ == '__main__'):
    topo = gp_utilities.Topology()

    #Input_Parameters
    input_file_prefix = "template"
    initial_distance = float(10)
    den_between_spheres = 13
    den_after_spheres = 13
    corner_grp_along_sphere = 1
    corner_grp_around_sphere = 2
    sphere_surface_grp = 1

    #Topology Modification and Run Ggrid
    for i in range(10, 4, -1):
        topo.read("{}.fra".format(input_file_prefix))
        translation_for_grp_along_sphere = vec(-(initial_distance-i), 0, 0)
        translation_for_grp_around_sphere = vec(-((initial_distance - i) / 2), 0, 0)
        den_between_spheres = den_between_spheres-1
        den_after_spheres = den_after_spheres+1
        topo_modify(corner_grp_along_sphere, sphere_surface_grp, corner_grp_around_sphere, translation_for_grp_along_sphere,
                    translation_for_grp_around_sphere, den_between_spheres, den_after_spheres)
        output_file_prefix = "distance_{}units".format(i)
        topo.write_topology("{}.fra".format(output_file_prefix))
        write_schedule_file()
        Ggrid = "Ggrid {}.fra".format(output_file_prefix)
        os.system(Ggrid)