import sys, io
import random
import importlib

def test_passed(test_feedback):
    # Set the name of the function we are testing
    test_function_name = 'diff_numbers'

    # Set to True if print out is being checked
    check_printing = True
    check_function = False

    test_passed = True
    for i in range(1,5):
        # Set up randomized values for inputs
        x = random.randint(1,50)
        y = random.randint(1,50)

        # Craft inputs
        test_input=f"{x}\n{y}"

        # Set up real answer based on those inputs
        act_ans = abs(x-y)

        # Save off stdin, stdout
        stdin = sys.stdin
        stdout = sys.stdout

        # Initialize test harness stdin and stdout
        sys.stdin = io.StringIO(test_input)
        sys.stdout = io.StringIO()

        # Load or reload the module/script
        if 'main' in sys.modules:
            learner_code = importlib.reload(sys.modules['main'])
        else:
            learner_code = importlib.import_module('main')

        # Collect any outputs
        stu_printed = sys.stdout.getvalue().strip()

        # Give back stdin and stdout control to zybooks
        sys.stdout = stdout
        sys.stdin = stdin

        test_passed = test_function('diff_numbers', act_ans, learner_code, test_feedback, x, y)

    return test_passed

def check_output(answer, output, test_feedback):
    #Checks for the lowercase answer in the lowercase student output
    if answer.lower() in output.lower():
        test_feedback.write(f"Correct, Your answer matches the expected answer: \n\t{answer}")
        return True
    else:
        test_feedback.write(f"Incorrect, the expected answer: '{answer}', which is not in your output")
        return False

def test_variable(var_name, answer, learner_code, test_feedback):

    #checks to see that the varible is in the learner code
    if not hasattr(learner_code, var_name):
        test_feedback.write(f"The variable '{var_name}' should exist, but it is not present in your program.")
        return False
    else:
        test_var = getattr(learner_code, var_name)

    #Checking the students stored value == the expected answer
    if(answer == test_var):
        test_feedback.write(f"Correct, Your answer matches the expected answer: {answer}")
        return True
    else:   
        test_feedback.write(f"Incorrect, Your answer: {test_var}\nExpected answer: {answer}")
        return False
    
def test_function(fun_name, answer, learner_code, test_feedback, *args):
    # Verify the function exists in the imported module
    if not hasattr(learner_code, fun_name):
        test_feedback.write(f"The description the '{fun_name}' function should exist, but it is not present in your program.")
        return False
    else:
        # test_function is now the function we are grading/validating
        test_fun = getattr(learner_code, fun_name)
    
    # Verify the attribute is actually a callable function
        if not callable(test_function):
            test_feedback.write(f"The description the '{fun_name}' function should exist, but it is not present in your program.")
            return False
    
    #call the students function
    stu_ans = test_fun(*args)

    #Checking the students function returned the expected answer
    if(answer == stu_ans):
        test_feedback.write(f"Checking Function --> Success --> '{fun_name}{args}' Returned: {answer} as expected")
        return True
    else:   
        test_feedback.write(f"Checking Function --> Failure --> '{fun_name}{args}' Returned: {stu_ans} instead of {answer}")
        return False