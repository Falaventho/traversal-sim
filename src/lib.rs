use pyo3::prelude::*;
use rand::Rng;

/// Generates n random points across a range of start to end inclusive and finds optimal traversal path from starting_position
#[pyfunction]
fn generate_data(start: f64, end: f64, n: usize, starting_position: f64) -> (Vec<f64>, f64) {
    let mut rng = rand::thread_rng();
    let points: Vec<f64> = (0..n).map(|_| rng.gen_range(start..end)).collect();
    let traversal_distance = find_best_path(points.clone(), starting_position);
    (points, traversal_distance)
}

/// Finds the best path given a set of points and a starting position.
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
    m.add_function(wrap_pyfunction!(generate_data, m)?)?;
    Ok(())
}
