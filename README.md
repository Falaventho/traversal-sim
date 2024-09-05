# Placement Optimization Simulator

This is a small project built to assist in the analysis of an optimization problem in 2d space.

## The Problem

There is a square 2d plane on which n randomly located points will be placed. Before the points are slected, choose a starting point P that will minimize the travel distance required to contact all points.

## The Plan

Define the problem in 1d space, solve the 1d problem, then apply the solution to the 2d space and test for a true or near-true solution.

## The One-Dimensional Problem

There is a line segment of length 2 on which n randomly located points will be placed. Before the points are slected, choose a starting point P that will minimize the travel distance required to contact all points.

## The One-Dimensional Assumptions

At n = 1, the center of the line segment (P = 1) is the optimal solution.

At n = 2, the center of the line segment (P = 1) is still the optimal solution.

At n = 3, the optimal solution is not found at P = 0 || P = 2

As n -> ♾️, the optimal solutions are found closer to each end of the line segment (P = 0 || P = 2).

## Initial Findings

Simulations of n-values from 1-10 generated the following distance-from-center results across a 100,000 iteration-per-step test on a 0.001 width interval step.
![1-10plt](https://github.com/user-attachments/assets/aa4ab966-db75-4401-bd66-9d3c8a5e5bb7)

Below is the same graph with log<sub>10</sub>(x-1) in orange and log<sub>e</sub>(x-1) in black

![1-10plt-log-loge](https://github.com/user-attachments/assets/f26341d9-698d-4b41-a0be-3e5b35c1413e)

### Numerical Findings

A cursory examination of n&nbsp;=&nbsp;100 held true the limit hypothesis with a 100,000 iteration-per-step test on a 0.001 width interval step showing P&nbsp;=&nbsp;1.985 on a segment spanning 0 to 2. From this, a 0.985 distance-from-center value can be extracted.

Below, the distance D from center for optimal traversal distance for n points on a line segment spanning 0 to 2 inclusive where 1<=n<=10:

n = 1, D = 0.000<br>
n = 2, D = 0.000<br>
n = 3, D = 0.515<br>
n = 4, D = 0.660<br>
n = 5, D = 0.727<br>
n = 6, D = 0.776<br>
n = 7, D = 0.800<br>
n = 8, D = 0.827<br>
n = 9, D = 0.847<br>
n = 10, D = 0.863
