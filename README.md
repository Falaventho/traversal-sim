# Placement Optimization Simulator

This is a small project built to assist in the analysis of an optimization problem in 2d space.

## The Problem

There is a square 2d plane on which n randomly located points will be placed. Before the points are slected, choose a starting point P that will minimize the travel distance required to contact all points.

## The Plan

Define the problem in 1d space, solve the 1d problem, then apply the solution to the 2d space and test for a true or near-true solution.


## The One-Dimensional Problem

There is a line segment of length 2 (spanning -1 to 1 inclusive) on which n points will be randomly placed with uniform probability. Before the points are slected, choose a starting point P that will minimize the travel distance required to contact all points.

<details>
<summary>
More on the one-dimensional problem
</summary>

<br/>

### The One-Dimensional Assumptions

At n = 1, the center of the line segment (P = 0) is the optimal solution.

At n = 2, the center of the line segment (P = 0) is still the optimal solution.

As n increases, the optimal solutions are found closer and closer to the ends of the line segment.

As n approaches infinity, the optimal solutions are found at the ends of the line segment (P = -1 or P = 1).

<br/>

### One-Dimensional Findings

Simulations of n-values from 1-10 generated the following distance-from-center (d) results across a 100,000 iteration-per-step test on a 0.001 width interval step. Each n-value simulation was repeated 10 times, to assist in analyzing the program's precision.

![1-10plt-5-100k-10](https://github.com/user-attachments/assets/c7d45f31-ab1d-4bcd-95eb-dca30071a3f8)

Associated mean and standard deviation for each n-value in sample above.

![1-10stats-5-100k-10-5-5](https://github.com/user-attachments/assets/91fd9519-0509-4d98-9c21-c7989219ceb5)

<br/>

### One-Dimensional Analysis

The one-dimensional simulation produces expected results, with the relatively large standard deviation for n=2 effectively explaining the apparent drift from d=0. There may be an effective description of this curve in the form  $1-\frac{a}{bx-1}$  for  $x\ge2$.
</details>
