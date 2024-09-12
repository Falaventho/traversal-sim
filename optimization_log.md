# Optimization Log

A record of moves and their percent gain at implementation time

## Rust Functions

- Rebuilt pathfinding function, including min and max, using rust. 3% runtime improvement across 50 n-values at 3sf, 3rep, 1000iter
- Migrated number line point generation to rust module, traversal calculation now bundled and handled entirely rust-side. 75% runtime improvement across 50 n-values at 3sf, 3rep, 1000iter