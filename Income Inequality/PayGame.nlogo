turtles-own [level level-next alpha beta gamma class payoff loss]
globals [count-levels-list count-levels-combined num-bars count-num-agents count-num-agents-old index-list switch-list N-list alpha-list beta-list gamma-list turtle-count]

;; Basic functions

to setup
  clear-all

  set num-bars num-levels;;100
  set count-num-agents n-values num-levels [0]
  set count-num-agents-old n-values num-levels [0]

  set index-list [0 1 2 3 4]
  set N-list (list N-0 N-1 N-2 N-3 N-4)
  set alpha-list (list alpha-0 alpha-1 alpha-2 alpha-3 alpha-4)
  set beta-list (list beta-0 beta-1 beta-2 beta-3 beta-4)
  set gamma-list (list gamma-0 gamma-1 gamma-2 gamma-3 gamma-4)
  set turtle-count 0

  set count-levels-combined []

  set count-levels-list (list [] [] [] [] [])
  foreach index-list
  [ ?1 ->
    let fraction-arg (item ?1 N-list)
    let alpha-arg (item ?1 alpha-list)
    let beta-arg (item ?1 beta-list)
    let gamma-arg (item ?1 gamma-list)
    set count-levels-list (replace-item ?1 count-levels-list (update-log-normal-n fraction-arg alpha-arg beta-arg gamma-arg))
    set count-levels-combined (sentence count-levels-combined (item ?1 count-levels-list))
  ]

  setup-patches


  foreach index-list
  [ ?1 ->
    create-turtles round (num-agents * (item ?1 N-list))
    [
      set shape "dot"
      set level mean-level
      enter-level
      set class ?1
      set alpha (item ?1 alpha-list)
      set beta (item ?1 beta-list)
      set gamma (item ?1 gamma-list)
      let deg random 360
      let r level / num-levels * 10
      setxy (r * cos(deg)) (r * sin(deg))
    ]

  ]


  reset-ticks
  tick
end


to setup-patches
  ask patches [ set pcolor black ]
end



to default
  set num-agents 1e4
  set num-levels 100
  set s-min 20000
  set s-max 3000000
  set go-until 100

  set N-0 0.95
  set N-1 0.05
  set N-2 0
  set N-3 0
  set N-4 0

  set alpha-0 93.4
  set alpha-1 95.8
  set alpha-2 100
  set alpha-3 100
  set alpha-4 100

  set beta-0 3.87
  set beta-1 3.67
  set beta-2 4
  set beta-3 4
  set beta-4 4

  set gamma-0 2.17
  set gamma-1 4.34
  set gamma-2 5
  set gamma-3 5
  set gamma-4 5

end

to go
  ifelse ticks < go-until [
  imitate
  move-turtles
  tick][stop]
end

to move-turtles
  ask turtles [
      let deg who / num-agents * 360
      let r level / num-levels * 10
      setxy (r * cos(deg)) (r * sin(deg))
      ]
end

;; New functions

to imitate
  ask turtles[
    set turtle-count (turtle-count + 1)

    ;; pick a random salary level
    let level-target 1 + random num-levels
    let level-self level

    ;; target salary and self salary
    let s-target level-to-salary level-target;; s-min + (level-target - 1) * s-delta
    let s-self level-to-salary level-self;;s-min + (level-self - 1) * s-delta




    ;; target population and self population
    let num-target item (level-target - 1) count-num-agents;;count turtles with [level = level-target]
    let num-self item (level-self - 1) count-num-agents ;;count turtles with [level = level-self]


    ;; compare, if target has a higher payoff, switch
    let payoff-target alpha * (ln s-target) - beta * (ln s-target) ^ 2 - gamma * (ln (num-target + 1 / num-agents))
    let payoff-self alpha * (ln s-self) - beta * (ln s-self) ^ 2 - gamma * (ln num-self)
    set payoff payoff-self

    ;; using a smooth curve for decision making
    let diff (payoff-target - payoff-self)
    let exp_s 2.0
    let exp_mu 5.0
    let cdf ((1.0 / (1.0 + exp((exp_mu - diff) / exp_s))) * 100000)
    let exp_random random 100000

    if diff > 0 [
    ;;if cdf > exp_random and diff > 0 [
      leave-level
      set level level-target
      enter-level
      set payoff payoff-target
    ]

    ;; check periodically for convergence rate
    let turtle-count-interval 10000
    if turtle-count mod turtle-count-interval = 0 [
      set loss 0
      let indexer ( range 0 length count-num-agents )

      foreach indexer [ ind ->
        let cur1 item ind count-num-agents
        let cur2 item ind count-num-agents-old
        set loss (loss + (cur1 - cur2) ^ 2)
      ]
      show loss

      set count-num-agents-old count-num-agents
    ]
  ]
end

to leave-level
  let tmp item (level - 1) count-num-agents
  set count-num-agents replace-item (level - 1) count-num-agents (tmp - 1)
end

to enter-level
  let tmp item (level - 1) count-num-agents
  set count-num-agents replace-item (level - 1) count-num-agents (tmp + 1)
end

to output-data
  set-current-directory "D:/Research Columbia/Github/income-game-theory/src/simulation"
  let rand-int random 99
  export-plot "histogram-levels" (word rand-int "-data.csv")
  export-interface (word rand-int "-pars.png")

end

to-report mean-level
  report round(num-levels / 2) - 1
end

to-report level-to-salary [x]
  report s-min + (s-max - s-min) / (num-levels - 1) * (x - 1)
end

to-report update-log-normal-n [fraction-arg alpha-arg beta-arg gamma-arg]
  let num-list replicator-dynamics fraction-arg alpha-arg beta-arg gamma-arg
  report make-bins num-list
end

to-report replicator-dynamics [fraction-arg alpha-arg beta-arg gamma-arg]
  let mu (alpha-arg + gamma-arg) / (2 * beta-arg)
  let sigma sqrt (gamma-arg / (2 * beta-arg))
  let s-list map level-to-salary n-values num-levels [ ?1 -> ?1 + 1 ] ;; salary list

  let x-list-unnormalized map [ ?1 -> e ^ (alpha-arg / gamma-arg * (ln ?1) - beta-arg / gamma-arg * (ln ?1) ^ 2) ] s-list

  let normalization sum x-list-unnormalized
  let x-list map [ ?1 -> ?1 * fraction-arg / normalization ] x-list-unnormalized
  let num-list map [ ?1 -> round(?1 * num-agents) ] x-list ;; num-list = x-list * num-agents
  report num-list
end

to-report make-bins [num-list]
  ;; create a pseudo distribution based on num-list
  let count-levels-0 []
  let level-now 1
  foreach num-list [ ?1 ->
    let num-now round ?1
    if num-now > 0 [
      foreach n-values num-now [level-now] [ ??1 ->
      set count-levels-0 lput ??1 count-levels-0 ]]
    set level-now level-now + 1 ]
  report count-levels-0
end
@#$#@#$#@
GRAPHICS-WINDOW
474
10
655
192
-1
-1
8.24
1
10
1
1
1
0
1
1
1
-10
10
-10
10
1
1
1
ticks
30.0

BUTTON
7
10
73
43
Setup
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
201
10
264
43
Go
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
0

BUTTON
268
10
363
43
Go once
go
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
0

INPUTBOX
10
64
87
124
num-agents
10000.0
1
0
Number

INPUTBOX
205
65
283
125
s-min
20000.0
1
0
Number

INPUTBOX
286
66
365
126
s-max
3000000.0
1
0
Number

INPUTBOX
90
64
167
124
num-levels
100.0
1
0
Number

PLOT
666
10
1226
382
histogram-levels
levels
turtles
0.0
10.0
0.0
10.0
true
false
"set-plot-x-range 0 num-levels\nset-plot-y-range 0 count turtles\nset-histogram-num-bars num-levels;;num-bars" "set-plot-y-range 0 10;;(0.1 * (count turtles))"
PENS
"Class 0 est." 1.0 0 -13791810 true "set-histogram-num-bars num-bars" "histogram (item 0 count-levels-list)"
"Class 1 est." 1.0 0 -1184463 true "set-histogram-num-bars num-bars" "histogram (item 1 count-levels-list)"
"Class 2 est." 1.0 0 -2674135 true "" "histogram (item 2 count-levels-list)"
"Class 3 est." 1.0 0 -13840069 true "" "histogram (item 3 count-levels-list)"
"Class 4 est." 1.0 0 -5825686 true "" "histogram (item 4 count-levels-list)"
"Class 0 sim." 1.0 1 -13791810 true "" "histogram [level] of turtles with [class = 0]"
"Class 1 sim." 1.0 1 -1184463 true "" "histogram [level] of turtles with [class = 1]"
"Class 2 sim." 1.0 1 -2674135 true "" "histogram [level] of turtles with [class = 2]"
"Class 3 sim." 1.0 1 -13840069 true "" "histogram [level] of turtles with [class = 3]"
"Class 4 sim." 1.0 1 -5825686 true "" "histogram [level] of turtles with [class = 4]"
"Combined est." 1.0 0 -16777216 true "" "histogram count-levels-combined"

BUTTON
75
10
171
43
Set default
default
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
584
219
659
252
Output
output-data
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
0

INPUTBOX
399
64
468
124
go-until
100.0
1
0
Number

INPUTBOX
9
133
98
193
N-0
0.95
1
0
Number

INPUTBOX
101
134
189
194
N-1
0.05
1
0
Number

INPUTBOX
194
135
284
195
N-2
0.0
1
0
Number

INPUTBOX
287
136
377
196
N-3
0.0
1
0
Number

INPUTBOX
379
137
470
197
N-4
0.0
1
0
Number

INPUTBOX
9
195
98
255
alpha-0
93.4
1
0
Number

INPUTBOX
101
195
188
255
alpha-1
95.8
1
0
Number

INPUTBOX
193
197
283
257
alpha-2
100.0
1
0
Number

INPUTBOX
286
198
376
258
alpha-3
100.0
1
0
Number

INPUTBOX
379
200
469
260
alpha-4
100.0
1
0
Number

INPUTBOX
9
258
98
318
beta-0
3.87
1
0
Number

INPUTBOX
101
258
187
318
beta-1
3.67
1
0
Number

INPUTBOX
193
259
281
319
beta-2
4.0
1
0
Number

INPUTBOX
285
261
376
321
beta-3
4.0
1
0
Number

INPUTBOX
378
263
468
323
beta-4
4.0
1
0
Number

INPUTBOX
8
320
99
380
gamma-0
2.17
1
0
Number

INPUTBOX
102
320
187
380
gamma-1
4.34
1
0
Number

INPUTBOX
193
322
279
382
gamma-2
5.0
1
0
Number

INPUTBOX
283
323
374
383
gamma-3
5.0
1
0
Number

INPUTBOX
379
325
470
385
gamma-4
5.0
1
0
Number

@#$#@#$#@
## VERSIONS

Version 1.2 (4/19/15)
- Natural log

Version 1.1 (11/11/2014)
- Nothing new

Version 1.0 (10/21/2014)
- 5 populations

Version 0.10.lite (08/25/2014)
- Much faster
- 10^ instead of exp, FIXED!!!!!!

Version 0.10 (08/19/2014)
- Added payoff attribute
- Payoff histogram (removed on 8/20)

Version 0.9 (08/16/2014)
- The data and prediction still have a slight mismatch. Can we fix this?
- Export data and parameters to MATLAB
- Simplified the formula to get the distribution (use replicator instead of lognormal)

Version 0.8 (08/11/2014)
- A more realistic alpha, beta, gamma for population 2
- Added empirical histograms for individual populations

Version 0.7 (08/08/2014)
- Added a monitor for the top 10%'s fraction of total money
- Data output: Salaries

Version 0.6 (06/10/2014)
- Fixed agent's radial degree
- New histogram of combined analytical curve

Version 0.5 (06/09/2014)
- Introduced polarized agents with two sets of alpha/beta/gamma
- Introduced distribution of parameters
- Introduced separated analytical curves
- Known issue: You have to hit "setup" every time when a parameter is changed

Version 0.4 (06/09/2014)
- Introduced budget: only transactions that result in a new money sum <= budget are allowed
- Known issue: When money-now > budget, it takes a long time for the system to reach budget.

Version 0.3 (05/30/2014)
- Added a delta to keep money never exceeding the budget
- Known issue: You have to click setup every time after changing alpha/beta/gamma because technically, money can't exceed the original budget from the last time you click setup

Version 0.2 (05/29/2014)
- Fixed level representation inconsistency. Changed from 0 ... 99 to 1 ... 100 
- Added an empirical adjustment parameter to make money budget closer to equilirbium money sum

Version 0.1 (05/28/2014)
- Fixed money budget conservation problem

## WHAT IS IT?

This program simulates the log-normal pay distribution.

## HOW IT WORKS

All agents initially have the same salary between s-min and s-max. Each agent then starts searching by randomly choosing a salary level i from 0 to (num-level - 1). If the payoff of that level i (i.e., h_i = alpha*log(S_i) - beta*(log(S_i))^2 - gamma*log(N_i)) is greater than the agent's own payoff at level j, he switches to level i. 

## HOW TO USE IT

Press Setup (to use default parameters, press Default then press Setup) and then press GO.

num-agents: Number of agents (1000 maximum due to performance concerns)
num-levels: Number of salary levels
s-min: Minimum wage
s-max: Salary upper bound

## THINGS TO NOTICE

Map: The closer the agents to the center, the lower salary level they are in.
Plot: Histogram and expected log-normal reference.

## THINGS TO TRY

Change alpha, beta, and gamma values to see the shift of distribution.

## EXTENDING THE MODEL

Different payoff functions and revision protocols. 

## NETLOGO FEATURES

N/A

## RELATED MODELS

Histogram Example

## CREDITS AND REFERENCES

http://www.columbia.edu/~yl2750/PayGame.html
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.0.4
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
