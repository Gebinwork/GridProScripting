# Import libraries
import sys
import fileinput

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

    # Input Parameters
    step_count = 5
    sweep_count = 300
    skewness = 0.8
    output_file_prefix = "volute"

    # Evaluate fold count and skewness value from qcheck output files
    folds,skew = evaluate_fold_count_from_qcheck_output()

    # Checking the desired quality condition
    count = step_count-1
    is_good_enough = (folds == 0 and skew == 0)
    for line in fileinput.input(schedule_file_name, inplace=1):
        count += 1
        if count > 50:
            break
        elif line.startswith('write'):
            if is_good_enough:
                print ("step {}: -c all 1.0 0 -C all 1.0 24 -r -S {} -w\n" + line.rstrip()).format(count, sweep_count)
            else:
                print ("step {}: -c all 1.0 0 -C all 1.0 24 -r -S {} -w "
                       "\nstep {}: -sys 'ws qchk {}.grd 11 10000 {} 120' "
                       "\nstep {}: -sys 'python Quality.py {}'\n"
                       + line.rstrip()).format(count, sweep_count, count + 1, output_file_prefix, skewness, count + 2, schedule_file_name)
        else:
            print line.rstrip()
    
# Main Function
if (__name__ == '__main__'):
    extend_schedule_file(sys.argv[1])
