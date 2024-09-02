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
