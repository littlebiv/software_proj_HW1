import builtins
import contextlib
import importlib.util
import io
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "python" / "kmeans_amir.py"
SPEC = importlib.util.spec_from_file_location("kmeans_amir", MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


@contextlib.contextmanager
def capture_stdout():
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        yield stream


@contextlib.contextmanager
def patched_exit():
    original_exit = builtins.exit

    def fake_exit(code=0):
        raise SystemExit(code)

    builtins.exit = fake_exit
    try:
        yield
    finally:
        builtins.exit = original_exit


class KMeansAmirEdgeTests(unittest.TestCase):
    def test_dist_supports_multidimensional_points(self):
        self.assertAlmostEqual(module.dist([0, 0, 0], [1, 2, 2]), 3.0)

    def test_checks_rejects_invalid_cluster_count(self):
        with capture_stdout() as out, patched_exit():
            with self.assertRaises(SystemExit):
                module.checks(0, 10, [[1, 2], [3, 4]])
        self.assertEqual(out.getvalue().strip(), "Incorrect number of clusters!")

    def test_checks_rejects_invalid_iteration_bound(self):
        with capture_stdout() as out, patched_exit():
            with self.assertRaises(SystemExit):
                module.checks(2, 801, [[1, 2], [3, 4], [5, 6]])
        self.assertEqual(out.getvalue().strip(), "Incorrect number of iterations!")

    def test_checks_rejects_mismatched_dimensions(self):
        with capture_stdout() as out, patched_exit():
            with self.assertRaises(SystemExit):
                module.checks(2, 10, [[1, 2], [3, 4, 5], [6, 7]])
        self.assertEqual(out.getvalue().strip(), "Incorrect number of dimensions!")

    def test_checks_rejects_non_numeric_values(self):
        with capture_stdout() as out, patched_exit():
            with self.assertRaises(SystemExit):
                module.checks(2, 10, [[1, 2], [3, "x"], [5, 6]])
        self.assertEqual(out.getvalue().strip(), "Incorrect data type!")

    def test_main_basic_two_cluster_case(self):
        points = [[1, 2], [1, 4], [1, 0], [4, 2], [4, 4], [4, 0]]
        self.assertEqual(module.main(points, 2), [[2.5, 1.0], [2.5, 4.0]])

    def test_checks_should_reject_k_equal_to_number_of_points(self):
        with capture_stdout() as out, patched_exit():
            with self.assertRaises(SystemExit):
                module.checks(2, 10, [[1, 2], [3, 4]])
        self.assertEqual(out.getvalue().strip(), "Incorrect number of clusters!")

    def test_main_should_handle_empty_cluster_without_zero_division(self):
        points = [[0, 0], [0, 0], [10, 10]]
        result = module.main(points, 2)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(len(centroid) == 2 for centroid in result))


if __name__ == "__main__":
    unittest.main()