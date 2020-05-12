Feature: Basic colorgrade functionality

Scenario: run without arguments
 When I run `seq 5 | colorgrade`
 Then output is colored as follows
        | line | color   |
        | 1    | lime    |
        | 2    | #7fff00 |
        | 3    | yellow  |
        | 4    | #ff8000 |
        | 5    | red     |

Scenario: run with low midpoint
 When I run `seq 3 | colorgrade --mid 1`
 Then output is colored as follows
        | line | color   |
        | 1    | yellow  |
        | 2    | #ff8000 |
        | 3    | red     |

Scenario: run with high midpoint
 When I run `seq 3 | colorgrade --mid 3`
 Then output is colored as follows
        | line | color   |
        | 1    | lime    |
        | 2    | #7fff00 |
        | 3    | yellow  |

Scenario: run with column argument
 When I run `seq 3 | awk '{print "foo", $1}' | colorgrade -c2`
 Then output is colored as follows
        | line  | color  |
        | foo 1 | lime   |
        | foo 2 | yellow |
        | foo 3 | red    |

Scenario: run with separator argument
 When I run `seq 3 | awk 'OFS="," {print $1, "bar"}' | colorgrade -f ','`
 Then output is colored as follows
        | line  | color  |
        | 1,bar | lime   |
        | 2,bar | yellow |
        | 3,bar | red    |

Scenario: run with skip header argument
 When I run `seq 4 | colorgrade -H`
 Then output is colored as follows
        | line | color     |
        | 1    | <nocolor> |
        | 2    | lime      |
        | 3    | yellow    |
        | 4    | red       |
