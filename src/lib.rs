use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn find_best_path(points: Vec<f64>, starting_position: f64) -> f64 {
    // render the points down to min and max
    let mut min_point: f64 = points[0];
    let mut max_point: f64 = points[0];
    for point in points.iter() {
        if point > &max_point {
            max_point = *point;
        }
        if point < &min_point {
            min_point = *point;
        }
    }

    let left_dist = (starting_position - min_point).abs();
    let right_dist = (max_point - starting_position).abs();

    let first_traversal = f64::min(left_dist, right_dist);
    let second_traversal = max_point - min_point;

    first_traversal + second_traversal
}

/// A Python module implemented in Rust.
#[pymodule]
fn placement_optimization_sim(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(find_best_path, m)?)?;
    Ok(())
}
