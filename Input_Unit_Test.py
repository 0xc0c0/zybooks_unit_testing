# Name test "Input Test"
# Import Statements
import sys, importlib, random
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from types import ModuleType

num_expected_inputs = 1

def craft_inputs(num = 5):
    test_inputs = []

    for i in range(num):

        test_input = []

        for i in range(num_expected_inputs)

            x = random.randint(1,50)
            test_input.append[x]

        test_inputs.append([test_input])
        
    return test_inputs


def test_passed(test_feedback):
    test_passed = True
    test_inputs = craft_inputs()

    for test_input in test_inputs:
        text_input = '\n'.join([str(x) for x in test_input])

        try:

            sink = StringIO()
            with redirect_stdout(sink):
                with patch("builtins.input", side_effect=text_input) as mock_input:
                    fresh_import()

            if mock_input.call_count != len(test_input):
                test_passed = False
                test_feedback.write("Did not capture the correct number of inputs")

        except StopIteration as e:
            test_feedback.write("Too many calls to input() in your program")

    return test_passed

def fresh_import(module_name: str = 'main', feedback_file = None) -> ModuleType:
    """Import the student's main module fresh"""
    try:
        if module_name in sys.modules:
            del sys.modules[module_name]
    except ValueError as e:
        if feedback_file:
            feedback_file.write(f"Check your input variable data types and conversions")
    return importlib.import_module(module_name)