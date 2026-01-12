#set page(width: auto, height: auto, margin: 5pt)
#show math.equation: set text(size: 15pt, weight: "semibold")
#import "@preview/intextual:0.1.1": *

// intertext-rule show rule is required for elements to display properly.
#show: intertext-rule

$
c space v arrow delta(c, v) #tag[(delta)]\
(lambda x.e) v arrow e[x arrow.r.bar v] #tag[(beta_v)] \
"let" x "be" v "in" e arrow e[x arrow.r.bar v] #tag[(let)] \
"Y"v arrow v(lambda x. ("Y" v) x) #tag[(Y)]
$
