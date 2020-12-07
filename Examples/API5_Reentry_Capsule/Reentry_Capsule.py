# IMPORT OPERATIONS
import gp_utilities
import os
import shutil

#Function to copy the given list of files to new directory
def copy_files_to_destination_directory(source, destination, files_list):
    if os.path.isdir(destination):
        os.system('rmdir /S /Q "{}"'.format(destination))
    os.mkdir(destination)
    for j in range(0, len(files_list)):
        shutil.copy(source + "/" + files_list[j], destination)
    os.chdir(destination)

#Function to replace an old text with new text
def find_and_replace(file, find, replace):
    with open(file, 'r') as f:
        text = f.read()
        f.close()
    with open(file, 'w') as f:
        text = text.replace(find, replace)
        f.write(text)

# Main Function
if (__name__ == '__main__'):
    topo = gp_utilities.Topology()

    #Input Parameters
    num_designs = 10
    num_steps = 4
    num_sweeps = 500
    old_surface_file = "reentry_capsule.tria"
    topology_file = "topology.fra"
    directory_name_prefix = "reentry_capsule"

    for i in range(1, num_designs + 1):
        new_surface_file = "{}_{}.tria".format(os.path.splitext(old_surface_file)[0], i)
        source_dir = os.getcwd()
        destination_dir = "{0}_{1}".format(directory_name_prefix, i)

        copy_files_to_destination_directory(source_dir, destination_dir, [new_surface_file, topology_file])
        find_and_replace(topology_file, old_surface_file, new_surface_file)

        topo.write_schedule_file("{}.sch".format(os.path.splitext(topology_file)[0]), num_steps, num_sweeps,
                                 "{}.grd".format(os.path.splitext(new_surface_file)[0]), "dump.tmp")
        Ggrid = "Ggrid {}".format(topology_file)
        os.system(Ggrid)

        os.chdir(source_dir)