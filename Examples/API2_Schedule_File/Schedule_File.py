# IMPORT OPERATIONS
import gp_utilities
import os

#Main Function
if(__name__ == '__main__'):
    topo = gp_utilities.Topology()      #Assign Topology Class

    input_topo_prefix = "step5.final_topo"
    step_count = 5
    sweep_count = 300

    topo.write_schedule_file("{0}.sch".format(input_topo_prefix), step_count, sweep_count, "blk.tmp", "dump.tmp")
    Ggrid = "Ggrid {0}.fra".format(input_topo_prefix)
    os.system(Ggrid)
