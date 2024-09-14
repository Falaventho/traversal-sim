# Optimization Log

A record of moves and their percent gain at implementation time

## Rust Rebuilds

- Rebuilt pathfinding function, including min and max, using rust. 3% runtime improvement across standard test.
- Migrated number line point generation to rust module, traversal calculation now bundled and handled entirely rust-side. 75% runtime reduction across standard test.
- Migrated number line class to rust module, now a struct with method implementations. 27% runtime reduction across standard test.

### Standard Test

- n value range 1 to 50
- 3 significant figures
- 1000 iterations
- 3 repetitions
