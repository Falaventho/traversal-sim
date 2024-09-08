use pyo3::prelude::*;

/// Finds the best path given a set of points and a starting position.
#[pyfunction]
fn find_best_path(points: Vec<f64>, starting_position: f64) -> f64 {
    // Use iterators to find the min and max points
    let min_point = points.iter().cloned().fold(f64::INFINITY, f64::min);
    let max_point = points.iter().cloned().fold(f64::NEG_INFINITY, f64::max);

    let left_dist = (starting_position - min_point).abs();
    let right_dist = (max_point - starting_position).abs();

    let first_traversal = f64::min(left_dist, right_dist);
    let second_traversal = max_point - min_point;

    first_traversal + second_traversal
}

/// A Python module implemented in Rust.
#[pymodule]
fn placement_optimization_sim(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find_best_path, m)?)?;
    Ok(())
}
