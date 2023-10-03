import unittest
from unittest import mock
import time

from mean_decorator import mean


class TestMeanDecorator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mean_time_execution(self):
        with mock.patch("builtins.print") as mock_print:
            with mock.patch("time.time") as mock_time:
                mock_time.side_effect = [0, 1, 1, 2, 2, 3]

                @mean(3)
                def dummy_function():
                    time.sleep(1)

                dummy_function()
                mock_print.assert_called_once_with(
                    "Mean time of executing of dummy_function is 1.0"
                )

    def test_zero_time_execution(self):
        with mock.patch("builtins.print") as mock_print:
            with mock.patch("time.time") as mock_time:
                mock_time.side_effect = [0, 0, 0, 0]

                @mean(2)
                def dummy_function():
                    pass

                dummy_function()
                mock_print.assert_called_once_with(
                    "Mean time of executing of dummy_function is 0.0"
                                                   )

    def test_different_time_execution(self):
        with mock.patch("builtins.print") as mock_print:
            with mock.patch("time.time") as mock_time:
                mock_time.side_effect = [0, 1, 1, 2, 2, 3, 3, 5]

                @mean(4)
                def dummy_function():
                    time.sleep(1)

                dummy_function()
                mock_print.assert_called_once_with(
                    "Mean time of executing of dummy_function is 1.25"
                                                   )

    def test_use_with_error_type(self):
        with self.assertRaises(TypeError):
            @mean("string")
            def dummy_function():
                time.sleep(1)

            dummy_function()


if __name__ == "main":
    unittest.main()
