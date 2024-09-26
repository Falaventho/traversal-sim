# Refactoring Plan/Log

Notes on the refactoring sub-project.

## Data Handling

Data handling is tightly coupled to the user interface. Create new class that handles data (import, export, replot, etc.) and accepts a user interface as an instantiation paramaeter. A dataset 'setter' and other appropriate mutators need to be developed, but the user interface should have little reason to touch the data itself, it being better for the data handler to reach for user interface methods as needed.

## User Interface

With an expansion on the horizon, the user interface class may need an abstract superclass that models the form that different UI implementations may take.

## Simulation

The simulation class should be reformed into one capable of handling geometric shapes. The number-line class in rsmod may be superceded by an abstract 'field' or 'geometry' superclass to allow for shape-based expansion in the near-future.
