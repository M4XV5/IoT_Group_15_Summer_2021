# read planner console output and parse it into usable code
def readPlan(plan):
    #print('\n---------------------------------------------------\nplan: \n',
    #plan,
    #'\n---------------------------------------------------\n')
    # plan begins after "step" and ends before "time spent"
    steps_start = plan.find("step")
    steps_end = plan.find("time spent")

    # handle if no string is found
    if steps_start == -1 or steps_end == -1:
        print("Plan is not valid!")
        print('\n---------------------------------------------------\nplan: \n', 
        plan, '\n---------------------------------------------------\n')
    else:
        # string starts after "step", ends before"time spent:"
        all_steps = plan[steps_start + 4:steps_end]
        # split string at linebreaks
        single_steps = all_steps.split("\n")
        # remove whitespaces around strings
        single_steps = list(map(str.strip, single_steps))
        # remove list entries with empty strings
        single_steps = list(filter(None, single_steps))
        # cut off "x: " at beginning of strings (x being step number)
        single_steps = [x[3:] for x in single_steps]
        # only keep first token in strings before space (which is the action name)
        single_steps = [x.split(' ', 1)[0] for x in single_steps]

        print('single_steps:\n', single_steps)
    
    return single_steps


#if __name__ == '__main__':

    #f = open('plan_example.txt', "r")
   # readPlan(f.read())