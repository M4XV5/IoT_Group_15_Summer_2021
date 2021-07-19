(define (domain lab)

    (:requirements
        ;:durative-actions
        ;:equality
        :negative-preconditions
        ;:numeric-fluents
        ;:object-fluents
        :typing
        :disjunctive-preconditions)

    (:types
        ; instances of objects possible
        fan alarm crit led button flag - object
        gas-crit temp-crit light-crit - crit
        emergencyflag tempflag lightflag doorflag - flag
        room-led door-led emer-led - led
        btn-door btn-emer - button
    )

    (:predicates
        ; to get opposite, do (not(...))
        (is-on ?o - object)
        (is-true ?c - crit)
        (is-set ?f - flag)
    )
    
    (:action light-on
        :parameters (?lc - light-crit ?rl - room-led ?lf - lightflag)
        :precondition (and 
                        ;light is off
                        (not(is-on ?rl))
                        ;light value bool is true
                        (is-true ?lc)
                        ;flag not set
                        (not(is-set ?lf))
                        )
        :effect (and 
                    ;light is on
                    (is-on ?rl) 
                    ;flag set
                    (is-set ?lf)
                    )
    )

    (:action light-keep-on
        :parameters (?lc - light-crit ?rl - room-led ?lf - lightflag)
        :precondition (and 
                        ;light is on
                        (is-on ?rl)
                        ;light value bool is true
                        (is-true ?lc)
                        ;flag not set
                        (not(is-set ?lf))
                        )
        :effect (and 
                    ;light is on
                    ;(is-on ?rl) 
                    ;flag set
                    (is-set ?lf)
                    )
    )
    
    (:action light-neutral-off
        :parameters (?lc - light-crit ?rl - room-led ?lf - lightflag)
        :precondition (and 
                        ;light is on
                        ;(is-on ?rl) 
                        ;on or off --> so there is always a way to achieve goal
                        ;light value bool is false
                        (not(is-true ?lc))
                        ;flag not set
                        (not(is-set ?lf))
                        )
        :effect (and 
                    ;light is off
                    (not(is-on ?rl))
                    ;flag set
                    (is-set ?lf)
                    )
    )
    
    (:action emergency-on
        :parameters (?gc - gas-crit ?bc - btn-emer ?ef - emergencyflag ?el - emer-led ?a - alarm)
        :precondition (and
                        ;alarm is off
                        (not(is-on ?a))
                        ;emergency light off
                        (not(is-on ?el))                        
                        (or
                            ;gas value critical
                            (is-true ?gc)
                            ;emergency button is on
                            (is-on ?bc)
                        )
                        ;flag not set
                        (not(is-set ?ef))
                        )
        :effect (and 
                    ;alarm is on
                    (is-on ?a) 
                    ;emergency light on
                    (is-on ?el)
                    ;flag is set
                    (is-set ?ef)
                    )
    )

    (:action emergency-keep-on
        :parameters (?gc - gas-crit ?bc - btn-emer ?ef - emergencyflag ?el - emer-led ?a - alarm)
        :precondition (and
                        ;alarm is on
                        (is-on ?a)
                        ;emergency light on
                        (is-on ?el)
                        (or
                            ;gas value critical
                            (is-true ?gc)
                            ;emergency button is on
                            (is-on ?bc)
                        )
                        ;flag not set
                        (not(is-set ?ef))
                        )
        :effect (and 
                    ;alarm is on
                    ;(is-on ?a) 
                    ;emergency light on
                    ;(is-on ?el)
                    ;flag is set
                    (is-set ?ef)
                    )
    )

    (:action emergency-neutral-off
        :parameters (?gc - gas-crit ?bc - btn-emer ?ef - emergencyflag ?el - emer-led ?a - alarm)
        :precondition (and
                        ;alarm is on
                        ;(is-on ?a) 
                        ;on or off --> so there is always a way to achieve goal
                        ;emergency light
                        ;(is-on ?el)
                        ;on or off --> so there is always a way to achieve goal
                        ;gas value not critical
                        (not(is-true ?gc))
                        ;emergency button is off
                        (not(is-on ?bc))
                        ;flag not set
                        (not(is-set ?ef))
                        )
        :effect (and 
                    ;alarm is off
                    (not(is-on ?a))
                    ;emergency light off
                    (not(is-on ?el))
                    ;flag is set
                    (is-set ?ef)
                    )
    )
    
    (:action fan-on
        :parameters (?tc - temp-crit ?tf - tempflag ?f - fan)
        :precondition (and
                        ;fan is off
                        (not(is-on ?f))
                        ;temperature value critical
                        (is-true ?tc)
                        ;flag not set
                        (not(is-set ?tf))
                    )
        :effect (and 
                    ;fan is on
                    (is-on ?f)
                    ;flag set
                    (is-set ?tf)
                    )
    )
    
    (:action fan-keep-on
        :parameters (?tc - temp-crit ?tf - tempflag ?f - fan)
        :precondition (and
                        ;fan is on
                        (is-on ?f)
                        ;temperature value critical
                        (is-true ?tc)
                        ;flag not set
                        (not(is-set ?tf))
                    )
        :effect (and 
                    ;fan is on
                    ;(is-on ?f) 
                    ;flag set
                    (is-set ?tf)
                    )
    )
    
    (:action fan-neutral-off
        :parameters (?tc - temp-crit ?tf - tempflag ?f - fan)
        :precondition (and
                        ;fan is on
                        ;(is-on ?f)
                        ;on or off --> so there is always a way to achieve goal
                        ;temperature value not critical
                        (not(is-true ?tc))
                        ;flag not set
                        (not(is-set ?tf))
                    )
        :effect (and 
                    ;fan is off
                    (not(is-on ?f))
                    ;temperature value not critical
                    (not(is-true ?tc))
                    ;flag is set
                    (is-set ?tf)
                    )
    )
    
    (:action door-open
        :parameters (?bd - btn-door ?dl - door-led ?df - doorflag)
        :precondition (and
                        ;rfid button is activated
                        (is-on ?bd)
                        ;rfid led is off  (simulates door)
                        (not(is-on ?dl))
                        ;flag not set
                        (not(is-set ?df))
                    )
        :effect (and 
                    ;door unlocks
                    (is-on ?dl)
                    ;flag is set
                    (is-set ?df)
                    )
    )

    (:action door-keep-open
        :parameters (?bd - btn-door ?dl - door-led ?df - doorflag)
        :precondition (and
                        ;rfid button is activated
                        (is-on ?bd)
                        ;rfid led is on  (simulates door)
                        (is-on ?dl)
                        ;flag not set
                        (not(is-set ?df))
                    )
        :effect (and 
                    ;door unlocks
                    ;(is-on ?dl)
                    ;flag is set
                    (is-set ?df)
                    )
    )

    (:action door-neutral-close
        :parameters (?bd - btn-door ?dl - door-led ?df - doorflag)
        :precondition (and
                        ;rfid button is not activated
                        (not(is-on ?bd))
                        ;rfid led is on  (simulates door)
                        ;(is-on ?dl)
                        ;on or off --> so there is always a way to achieve goal
                        ;flag not set
                        (not(is-set ?df))
                    )
        :effect (and 
                    ;door locked
                    (not(is-on ?dl))
                    ;flag set
                    (is-set ?df)
                    )
    )  
)