from jinja2 import Template

problem_template = Template("""(define (problem lab_problem) (:domain lab)

(:objects
    fan1 - fan
    alarm1 - alarm
    roomled1 - room-led
    doorled1 - door-led
    emerled1 - emer-led
    gascrit1 - gas-crit
    tempcrit1 - temp-crit
    lightcrit1 - light-crit
    btndoor1 - btn-door
    btnemer1 - btn-emer
    emergencyflag1 - emergencyflag
    tempflag1 - tempflag
    lightflag1 - lightflag
    doorflag1 - doorflag
)

; init everything thats true, otherwise it is false by default
(:init
    ; un-set flags
    (not(is-set emergencyflag1))
    (not(is-set tempflag1))
    (not(is-set lightflag1))
    (not(is-set doorflag1))
    ; variables here
    {{ fan1 }}
    {{ alarm1 }}
    {{ roomled1 }}
    {{ doorled1 }}
    {{ emerled1 }}
    {{ gascrit1 }}
    {{ tempcrit1 }}
    {{ lightcrit1 }}
    {{ btndoor1 }}
    {{ btnemer1 }}
)

(:goal
    (and
        (is-set emergencyflag1)
        (is-set tempflag1)
        (is-set lightflag1)
        (is-set doorflag1)
    )
)
)
""")

def make_problem(fanOn, alarmOn, rlOn, dlOn, elOn, gasCrit, tempCrit, lightCrit, btnDoor, btnEmer):
    output = problem_template.render(fan1=fanOn,
    alarm1=alarmOn, 
    roomled1=rlOn, 
    doorled1=dlOn, 
    emerled1=elOn, 
    gascrit1=gasCrit, 
    tempcrit1=tempCrit, 
    lightcrit1=lightCrit, 
    btndoor1=btnDoor, 
    btnemer1=btnEmer)
    with open("problem_lab_gen.pddl", "w") as text_file:
        text_file.write(output)