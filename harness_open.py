# Name Test "var '{var_name}' Test"
#Import Statements

import builtins
import sys, importlib, random, math, io
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from types import ModuleType

# ***Adjust this section as needed for the Lab***
INPUT_CSV_FILE = 'amazon.csv'
WHOLE_INPUT_CSV_FILE = 'amazon_complete.csv'
ALTERED_CSV_INPUT_FILE = 'testfile1.csv'
INPUT_CSV_FILE_ACCESSED = False
OUTPUT_TXT_FILE = 'result.txt'
ALTERED_OUTPUT_TXT_FILE = 'testfile1_result.txt'
OUTPUT_TXT_FILE_ACCESSED = False
DATE_LINE_INDEX_IN_OUTPUT = 0
VOLUME_LINE_INDEX_IN_OUTPUT = 1
REAL_OPEN = builtins.open

# Feedback options, lab_feedback gives a lot of feedback, test_feedback provides minimun feedback

lab_feedback = False
PA_feedback = True

# Set one of these to True

check_read_open_only = False
check_var_volume_example = False
check_var_volume_randomized = False
check_var_date_example = False
check_var_date_randomized = False
check_write_open_only = False
check_volume_in_file = False
check_date_in_file = False

if sum([check_read_open_only, check_var_volume_example, check_var_volume_randomized, check_var_date_example, check_var_date_randomized, check_write_open_only, check_volume_in_file, check_date_in_file]) != 1:
    raise ValueError("You must set exactly one of the check_ options to True")

# Create the answer you are looking for based on inputs, *** return must be a list
def create_file_from_list(data, new_file):
    with open(new_file, 'w') as f:
        f.write('\n'.join(data))

def generate_randomized_read_file(original_file, num_rows, new_file):
    open_file = open(original_file)
    contents = open_file.read().strip('\n ').split('\n')
    rand_start = random.randint(0, len(contents)-num_rows)
    rows = contents[rand_start:rand_start + num_rows]
    create_file_from_list(rows, new_file)
    return rows    

def get_correct_answers(filename):
    open_file = open(filename)
    contents = open_file.read().strip('\n ').split('\n')
    date_largest_volume = 0
    largest_volume = 0

    for row in contents:
        cols = row.split(',')
        if(int(cols[5]) > largest_volume):
            largest_volume = int(cols[5])
            date_largest_volume = cols[0]
    return date_largest_volume, largest_volume

def check_answer_in_file(answer, line_num, filename, test_feedback):
    try:
        with open(filename, 'r') as f:
            lines = f.read().strip('\n ').split('\n')
            if len(lines) <= line_num:
                return False
            if str(answer) in lines[line_num]:
                return True
    except FileNotFoundError as e:
        test_feedback.write(f"Your code did not write to this file: {OUTPUT_TXT_FILE}")
    return False


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

def mocked_open(path, mode='r'):
    global INPUT_CSV_FILE_ACCESSED, OUTPUT_TXT_FILE_ACCESSED
    if 'r' == mode and path == INPUT_CSV_FILE:
        path = ALTERED_CSV_INPUT_FILE
        INPUT_CSV_FILE_ACCESSED = True
    elif 'w' == mode and path == OUTPUT_TXT_FILE:
        path = ALTERED_OUTPUT_TXT_FILE
        OUTPUT_TXT_FILE_ACCESSED = True
    return REAL_OPEN(path, mode)

def test_passed(test_feedback):
    test_passed = True
    
    if check_var_date_example or check_var_volume_example:
        generated_lines = open(INPUT_CSV_FILE).read().strip('\n ').split('\n')
        create_file_from_list(generated_lines, ALTERED_CSV_INPUT_FILE)
    else:
        generate_randomized_read_file(WHOLE_INPUT_CSV_FILE, 5, ALTERED_CSV_INPUT_FILE)
        generated_lines = open(ALTERED_CSV_INPUT_FILE).read().strip('\n ').split('\n')
    correct_date, correct_volume = get_correct_answers(ALTERED_CSV_INPUT_FILE)

    try:
        sink = StringIO()
        with redirect_stdout(sink):
            with patch("builtins.open", side_effect=mocked_open):
                student_main = fresh_import('main', test_feedback)
    except FileNotFoundError as e:
        test_feedback.write(f"{e.strerror}: {e.filename}")
        test_passed = False

    for name, obj in vars(student_main).items():
        if isinstance(obj, io.IOBase) and not obj.closed:
            obj.close()
    
    if check_read_open_only:
        test_passed = INPUT_CSV_FILE_ACCESSED
        if test_passed:
            feedback_msg = f"You correctly opened the '{INPUT_CSV_FILE}' file for reading."
        else:
            feedback_msg = f"You did not correctly open the '{INPUT_CSV_FILE}' file for reading."
    elif check_var_volume_example:
        test_feedback.write(f"Using the example data from the problem description:\n{'\n'.join(generated_lines)}\n")
        student_volume = getattr(student_main, 'largest_volume', None)
        test_passed = (student_volume == correct_volume)
        if test_passed:
            feedback_msg = f"Your code correctly set the variable 'largest_volume' to {correct_volume}."
        else:
            if student_volume is None:
                feedback_msg = f"Your code did not set the variable 'largest_volume'."
            elif type(student_volume) is not type(correct_volume):
                feedback_msg = f"Your code did not set the variable 'largest_volume' to the correct data type, it should be an integer."
            else:
                feedback_msg = f"Your code did not correctly set the variable 'largest_volume' to {correct_volume}, your value was {student_volume}."
    elif check_var_volume_randomized:
        test_feedback.write(f"Using an '{INPUT_CSV_FILE}' file containing these lines:\n{'\n'.join(generated_lines)}\n")
        student_volume = getattr(student_main, 'largest_volume', None)
        test_passed = (student_volume == correct_volume)
        if test_passed:
            feedback_msg = f"Your code correctly set the variable 'largest_volume' to {correct_volume}."
        else:
            if student_volume is None:
                feedback_msg = f"Your code did not set the variable 'largest_volume'."
            elif type(student_volume) is not type(correct_volume):
                feedback_msg = f"Your code did not set the variable 'largest_volume' to the correct data type, it should be an integer."
            else:
                feedback_msg = f"Your code did not correctly set the variable 'largest_volume' to {correct_volume}, your value was {student_volume}."
    elif check_var_date_example:
        test_feedback.write(f"Using the example data from the problem description:\n{'\n'.join(generated_lines)}\n")
        student_date = getattr(student_main, 'date_largest_volume', None)
        test_passed = (student_date == correct_date)
        if test_passed:
            feedback_msg = f"Your code correctly set the variable 'date_largest_volume' to {correct_date}."
        else:
            if student_date is None:
                feedback_msg = f"Your code did not set the variable 'date_largest_volume'."
            else:
                feedback_msg = f"Your code did not correctly set the variable 'date_largest_volume' to {correct_date}, your value was {student_date}."
    elif check_var_date_randomized:
        test_feedback.write(f"Using an '{INPUT_CSV_FILE}' file containing these lines:\n{'\n'.join(generated_lines)}\n")
        student_date = getattr(student_main, 'date_largest_volume', None)
        test_passed = (student_date == correct_date)
        if test_passed:
            feedback_msg = f"Your code correctly set the variable 'date_largest_volume' to {correct_date}."
        else:
            if student_date is None:
                feedback_msg = f"Your code did not set the variable 'date_largest_volume'."
            else:
                feedback_msg = f"Your code did not correctly set the variable 'date_largest_volume' to {correct_date}, your value was {student_date}."
    elif check_write_open_only:
        test_passed = OUTPUT_TXT_FILE_ACCESSED
        if test_passed:
            feedback_msg = f"You correctly opened the '{OUTPUT_TXT_FILE}' file for writing."
        else:
            feedback_msg = f"You did not correctly open the '{OUTPUT_TXT_FILE}' file for writing."
    elif check_date_in_file:
        test_passed = check_answer_in_file(student_main.date_largest_volume, DATE_LINE_INDEX_IN_OUTPUT, ALTERED_OUTPUT_TXT_FILE, test_feedback)
        if test_passed:
            feedback_msg = f"You correctly wrote your date with the largest volume on the first line of the '{OUTPUT_TXT_FILE}' file."
        else:
            feedback_msg = f"You did not correctly write your date with the largest volume on the first line of the '{OUTPUT_TXT_FILE}' file."
    elif check_volume_in_file:
        test_passed = check_answer_in_file(student_main.largest_volume, VOLUME_LINE_INDEX_IN_OUTPUT, ALTERED_OUTPUT_TXT_FILE, test_feedback)
        if test_passed:
            feedback_msg = f"You correctly wrote your largest volume on the second line of the '{OUTPUT_TXT_FILE}' file."
        else:
            feedback_msg = f"You did not correctly write your largest volume on the second line of the '{OUTPUT_TXT_FILE}' file."
    

   
    test_feedback.write(f"RESULT: {feedback_msg}\n")

    return test_passed