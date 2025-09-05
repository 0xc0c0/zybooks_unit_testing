# Name Test "'{function_name}' {print/return} Test"
#Import Statements

import sys, importlib, random, math, inspect
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from types import ModuleType

# ***Adjust this section as needed for the Lab***

# Feedback options, lab_feedback gives a lot of feedback, test_feedback provides minimun feedback

lab_feedback = True
PA_feedback = False

# Testing for a print or return value?

print_check = True

# Create the answer you are looking for based on inputs, *** return must be a list

def actual_answers(length, width, height):
    
    if height == 0:
        dimension  = length * width
    else:
        dimension  = length * width * height
    
    return [dimension]

# set to the name of the variable you are checking
function_name = 'get_shape_property'

# The location of the arguments the function needs in the program inputs
# remeber the stop must be one # passed where you want to stop
fun_arg_start = 0
fun_arg_stop = 3

# How many interations of the test do you want to run?
iterations = 5

#create your inputs all main inputs must be accounted for

test_inputs_raw = []

for i in range(iterations):
    # Create the inputs using random
    
    #random strings
    #name_list = ["Edward", "James", "David", "Tiffany", "Claire", "Sarah"]
    #name = random.choice(name_list)
    
    #random int
    length = random.randint(1, 15)
    width = random.randint(1, 15)
    height = random.randint(0, 2)

    #random float
    #decimal = round(random.random() * 1000, 2)

    # Craft inputs, *** must be in a list
    test_inputs_raw.append([length, width, height])

# ***After this point nothing should need to be changed***

def test_passed(test_feedback):

    test_passed = True

    for raw_inputs in test_inputs_raw:

        sink = StringIO()
        with redirect_stdout(sink):
            with patch("builtins.input", side_effect = raw_inputs) as mock_input:
                main = fresh_import('main', test_feedback)
    
        answer = actual_answers(*raw_inputs)
        
        function_arg = raw_inputs[fun_arg_start:fun_arg_stop]

        if lab_feedback:
            test_feedback.write(f"given the inputs of {raw_inputs} your code was:")

        test_passed = test_function(function_name, answer, main, test_feedback,sink.getvalue(), *function_arg)

        if test_passed:
            test_feedback.write(f"Your program works as intended")
        else:
            test_feedback.write(f"Your program does not works as intended")

    return test_passed
        
# Brings in the student's code, catches the ValueError and EOFError
def fresh_import(module_name: str = 'main', feedback_file = None) -> ModuleType:
    try:
        if module_name in sys.modules:
            del sys.modules[module_name]
    except ValueError as e:
        if feedback_file:
            feedback_file.write(f"Check your input variable data types and conversions")
    except EOFError as e:
        if feedback_file:
            feedback_file.write(f"There are more inputs then expected")
    return importlib.import_module(module_name)

def test_function(fun_name, answers, learner_code, test_feedback, output = '', *args):
    # Verify the function exists in the imported module
    if not hasattr(learner_code, fun_name):
        test_feedback.write(f"The function '{fun_name}' should exist, but it is not present in your program.")
        return False
    else:
        # test_function is now the function we are grading/validating
        test_fun = getattr(learner_code, fun_name)
    
    # Verify the attribute is actually a callable function
    if not callable(test_fun):
        test_feedback.write(f"The function '{fun_name}' is not callable")
        return False
    
    # Verify the function has the correct number of args
    sig = inspect.signature(test_fun)
    num_args = fun_arg_stop - fun_arg_start
    if len(sig) != (num_args):
        test_feedback.write(f"The function '{test_fun}' must take exactly {num_args} parameter(s), but it takes {len(sig.parameters)}.\n")
        return False

    #call the students function
    stu_ans = test_fun(*args)

    #Checking the students function returned the expected answer
    result = True
    for answer in answers:
        if print_check:
            if str(answer) in output:
                if PA_feedback:
                    test_feedback.write(f"Your function works as expected\n")
                elif lab_feedback:
                    test_feedback.write(f"Your function printed the expected value: {answer}\n")
            else:
                if PA_feedback:
                    test_feedback.write(f"Your function does not work as expected\n")
                elif lab_feedback:
                    test_feedback.write(f"Your function did not print the expected value of: {answer}\n")
        else:
            if type(answer) == type(stu_ans):
                if answer == stu_ans or (type(answer) == float and math.isclose(answer, stu_ans)):
                    if PA_feedback:
                        test_feedback.write(f"Your function works as expected\n")
                    elif lab_feedback:
                        test_feedback.write(f"Your function returns the expected value: {answer}\n")
                else:   
                    result = False
                    if PA_feedback:
                        test_feedback.write(f"Your function does not work as expected\n")
                    elif lab_feedback:
                        test_feedback.write(f"Your function returns: {stu_ans}\n The expected return is: {answer}\n")
            else:
                result = False
                test_feedback.write(f"Check your data type\n")
    return result