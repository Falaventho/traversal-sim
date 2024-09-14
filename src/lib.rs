use pyo3::prelude::*;
use rand::Rng;

#[pyclass]
struct NumberLine {
    start: f64,
    end: f64,
    starting_position: f64,
    number_of_points: usize,
}

#[pymethods]
impl NumberLine {
    #[new]
    fn new(start: f64, end: f64, starting_position: f64, number_of_points: usize) -> Self {
        NumberLine {
            start,
            end,
            starting_position,
            number_of_points,
        }
    }

    fn regenerate_data(&self) -> f64 {
        generate_data(self.start, self.end, self.number_of_points, self.starting_position)
    }

    fn set_starting_position(&mut self, new_starting_position: f64) {
        self.starting_position = new_starting_position;
    }
    fn get_starting_position(&self) -> f64 {
        self.starting_position
    }
    fn get_end(&self) -> f64 {
        self.end
    }
}
/// Generates n random points across a range of start to end inclusive and finds optimal traversal path from starting_position
#[pyfunction]
fn generate_data(start: f64, end: f64, n: usize, starting_position: f64) -> f64 {
    let mut rng = rand::thread_rng();
    let points: Vec<f64> = (0..n).map(|_| rng.gen_range(start..end)).collect();
    let traversal_distance = find_best_path(points.clone(), starting_position);
    traversal_distance
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
    //m.add_function(wrap_pyfunction!(generate_data, m)?)?;
    m.add_class::<NumberLine>()?;
    Ok(())
}
