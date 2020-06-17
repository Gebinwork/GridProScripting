# Import libraries
import sys
import fileinput
import variables

# Evaluate fold count and skewness value from qcheck output files
def evaluate_fold_count_from_qcheck_output():
    # Calculating number of folds and skew
    folds = open('bad_folds.hex').readline()
    folds = int(folds)
    skew = open('bad_skewness.hex').readline()
    skew = int(skew)
    return [folds,skew]

# Extend schedule file if the grid quality is not good enough
def extend_schedule_file(schedule_file_name):

    # Evaluate fold count and skewness value from qcheck output files
    folds,skew = evaluate_fold_count_from_qcheck_output()

    # Checking the desired quality condition
    count = variables.step_count-1
    desired_quality = (folds == 0 and skew == 0)
    for line in fileinput.input(schedule_file_name, inplace=1):
        count += 1
        if count > 100:
            break
        elif line.startswith('write'):
            if desired_quality:
                print ("step {}: -c all 1.0 0 -C all 1.0 24 -r -S {} -w\n" + line.rstrip()).format(count, variables.sweep_count)
            else:
                print ("step {}: -c all 1.0 0 -C all 1.0 24 -r -S {} -w"
                       "\nstep {}: -sys 'ws qchk {}.grd 11 10000 {} 120' "
                       "\nstep {}: -sys 'python Quality.py {}'\n"
                       + line.rstrip()).format(count, variables.sweep_count, count + 1, schedule_file_name[:-4], variables.skewness,
                                               count + 2, schedule_file_name)
        else:
            print line.rstrip()
    
# Main Function
if (__name__ == '__main__'):
    extend_schedule_file(sys.argv[1])
