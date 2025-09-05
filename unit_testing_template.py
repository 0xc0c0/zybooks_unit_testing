import sys, io
import random
import importlib

# Define correct functions here
# Correct functions may apply to any of: function testing, variable testing, output/print testing
# Function parameters should generally be from their natural form (int, float, str) and not "stringified"
# Ask Coco for assistance if this is confusing
# UPDATE FOR EACH PROBLEM
def correct_sum_numbers(x, y):
    return x + y

# If checking functions, setup function checking dictionary here
# keys are the string names of the functions that should exist in student code
# values are the names of the functions with the correct implementations of those functions
# UPDATE FOR EACH PROBLEM
test_function_answers = {
    'sum_numbers': correct_sum_numbers
}

# If you need to customize your output checking for a particular function or variable,
#   modify this or create additional functions here
# UPDATE FOR EACH PROBLEM (maybe)
def default_output_checker(answer, student_stdout, feedback_output=None):
    search_str = str(answer)
    found_offset = search_str.lower() in student_stdout.lower()
    success = (found_offset != -1)
    if feedback_output:
        feedback_output.write(f"{LOG_SUCCESS[success]} --> Expected to find {search_str} (case insensitive) in the output")
    return success


# Adding an output checker for a named function here will enable output checking for that function
# UPDATE FOR EACH PROBLEM
test_function_answer_formatters = {
    'sum_numbers': default_output_checker
}

# Saved strings to build printouts in the testfeedback box
LOG_SUCCESS = {
    True: 'SUCCESS',
    False: 'FAILURE'
}

# Boilerplate to enable multiple runs of the main.py the students are writing
# returns the loaded 'main' module as 'student_main'
# returns a string with all the stdout from student code 'stu_printed'
def handle_run_test_main(test_input):
    # Save off stdin, stdout
    stdin = sys.stdin
    stdout = sys.stdout

    # Initialize test harness stdin and stdout
    sys.stdin = io.StringIO(test_input)
    sys.stdout = io.StringIO()

    # Load or reload the module/script
    if 'main' in sys.modules:
        student_main = importlib.reload(sys.modules['main'])
    else:
        student_main = importlib.import_module('main')

    # Collect any outputs
    stu_printed = sys.stdout.getvalue().strip()

    # Give back stdin and stdout control to zybooks
    sys.stdout = stdout
    sys.stdin = stdin

    return student_main, stu_printed

def test_passed(test_feedback):
    # Should not need to update this function
    def check_function_return_value(student_main, function_name, function_inputs):
        # Verify the function exists in the imported module
        if not hasattr(student_main, function_name):
            test_feedback.write(f"The description the '{function_name}' function should exist, but it is not present in your program.")
            return False
        else:
            # test_function is now the function we are grading/validating
            test_function = getattr(student_main, function_name)
        
        # Verify the attribute is actually a callable function
        if not callable(test_function):
            test_feedback.write(f"The description the '{function_name}' function should exist, but it is not present in your program.")
            return False

        # Call the student's function
        stu_ans = test_function(*function_inputs)

        # Call the correct function (solution) defined above
        act_ans = test_function_answers[function_name](*function_inputs)

        success = stu_ans == act_ans
        test_feedback.write(f"Test {i} --> Checking Function --> {LOG_SUCCESS[success]} --> '{function_name}({x}, {y})' Returned: {stu_ans}, Expected: {act_ans}")
        return success

    # Create a list of test run arguments
    # If only running main a single time, then just use the following line instead
    # test_run_stdin_inputs = [(value1, value2)]
    # UPDATE FOR EACH PROBLEM
    test_run_inputs = []
    for i in range(1,5):
        # Randomization approach for problem
        # UPDATE FOR EACH PROBLEM
        x = random.randint(1,50)
        y = random.randint(1,50)
        inputs = (x,y)
        test_run_inputs.append(inputs)



    # Setup randomized grading test passes here
    test_passed = True
    test_num = 0
    for test_run_input in test_run_inputs:
        # Craft inputs
        test_stdin = '\n'.join((str(x) for x in test_run_input))

        # Set up real answer based on those inputs
        act_ans = correct_sum_numbers(*test_run_input)

        # Perform test run and collect any output
        student_main, stu_outputs = handle_run_test_main(test_stdin)

        # If we're grading print statements, ensure correct output is somewhere in student's prints (implementation may vary)
        if check_printing:
            success = output_formatter(act_ans) in stu_outputs
            if success:
                test_feedback.write(f"Test {i} --> Checking Output --> Using Inputs '{x}' and '{y}' --> {LOG_SUCCESS[success]} --> Found '{act_ans}' in output, as expected")
            else:
                test_feedback.write(f"Test {i} --> Checking Output --> Using Inputs '{x}' and '{y}' --> {LOG_SUCCESS[success]} --> Did not find '{act_ans}' in output!")
                test_passed = False

    return test_passed
