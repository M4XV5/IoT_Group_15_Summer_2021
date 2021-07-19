(define (problem lab_problem) (:domain lab)

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
    (not(is-on fan1))
    (not(is-on alarm1))
    (not(is-on roomled1))
    (not(is-on doorled1))
    (not(is-on emerled1))
    (not(is-true gascrit1))
    (not(is-true tempcrit1))
    (not(is-true lightcrit1))
    (not(is-on btndoor1))
    (not(is-on btnemer1))
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