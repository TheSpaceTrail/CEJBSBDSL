"""
MIT License

Copyright (c) 2026 TheSpaceTrail

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Micos - Thank you for reading this code, may god help your soul.
"""

# Built-in Libraries
import argparse
import json
import random
import time
import sys
import operator

CEJBSBDSL_VERSION = "0.0.1"

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", help="path to script")
parser.add_argument("-e", "--entry-point", default="init", required=False, help="program entry point (default: \"init\")")
parser.add_argument("-s", "--seed", default="42", required=False, help="random seed (default: 42, \"random\" for random)")
parser.add_argument("-v", "--version", action="version", version=CEJBSBDSL_VERSION)
parser.add_argument("-dw", "--disable-warnings", action='store_true', help="does not print warnings")
parser.add_argument("-de", "--disable-errors", action='store_true', help="does not print errors and exits quietly and successfully")

args = parser.parse_args()

def error(error_message, code, warning=False):

    global args

    if warning and args.disable_warnings: return
    if not warning and args.disable_errors: sys.exit(0)
    print(f'CEJBSBDSL {CEJBSBDSL_VERSION} {"Error" if not warning else "Warning"} (Code {code}): {error_message}')
    if not warning: sys.exit(1)

try:
    random.seed(int(args.seed) if args.seed!="random" else random.randint(1,999999))
except:
    error("Invalid seed provided.", "4")

comp_operators = {
    ">=": operator.ge,
    "=>": operator.ge,

    "=<": operator.le,
    "<=": operator.le,

    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq,
}

num_operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "**": operator.pow,
}

try:
    origin_sequence = json.load(open(args.file, "r", encoding="utf-8"))

except json.decoder.JSONDecodeError:
    error("JSON decoding error.", "9")

database = {} # Specifically for choice

# Test if some name is in the database; if it is, return the value 
def get_variable(test, database):

    if test[0] == "$":

        if test[1:] in database.keys():

            return database[test[1:]]
        
        else:

            error(f"Variable \"{test}\" not found!", "5")
    
    else:

        return test

def to_float_if_float(value):

    try:
        return float(value)
    except:
        return value

def prompt(text, choices, case_sensitive=False):

    while True:

        i = input(text)
        if not case_sensitive: i = i.lower()

        if i in choices:

            return i

# Run a sequence from storyline.json, run any commands that occur, ignore comments, 
# and auto-print anything that does not start with a special character
def run_sequence(sequence, database):

    idx = 0

    # Loop continuously until broken
    while True:

        if len(sequence) < idx + 1: 
            break # Make sure it does not go forever

        # Split input for parsing
        if " " in sequence[idx]:
            split_sequence = sequence[idx].split(" ")
        else:
            split_sequence = [sequence[idx]]

        # Commands
        try:

            if sequence[idx][0] == "!":

                if split_sequence[0] == "!jump_switch":

                    v = get_variable(split_sequence[1], database)

                    if type(sequence[idx+1]) != dict:
                        
                        error(f"Error in jump switch: type of dictionary invalid.", "7")

                    if not v in sequence[idx+1].keys():

                        if "\n" not in sequence[idx+1].keys():

                            error(f"Error in jump switch: key \"{v}\" not found.", "8")
                        
                        else:

                            return sequence[idx+1]["\n"]

                    return sequence[idx+1][v]
                
                elif split_sequence[0] == "!store":

                    database[get_variable(split_sequence[1], database)] = get_variable(split_sequence[2], database)
                
                elif split_sequence[0] == "!jump":
                    
                    return get_variable(split_sequence[1], database)

                # Ends WHOLE game
                elif split_sequence[0] == "!end":

                    sys.exit(0)

                elif split_sequence[0] == "!modify":

                    try:

                        if split_sequence[1] not in database: database[split_sequence[1]] = ""
                    
                        key = split_sequence[1][1:] if split_sequence[1].startswith("$") else split_sequence[1]
                        op = split_sequence[2]
                        mod_value = to_float_if_float(get_variable(split_sequence[3], database))

                        func = num_operators.get(op)

                        if func: 
                            if type(mod_value) == float:

                                    database[key] = func(to_float_if_float(database[key]) if not database[key] == "" else 0, mod_value)
                            
                            else:

                                    if type(database[split_sequence[1]]) != str: database[split_sequence[1]] = str(database[split_sequence[1]])

                                    database[key] = func(database[key], mod_value)
                                

                        else:
                            error(f"Invalid operator \"{op}\".", "7")

                    except Exception as e:

                        error(f"Operation {split_sequence[1]} {op} to {split_sequence[3]} could not be executed.", "10")

                elif split_sequence[0] == "!random_hop": # Hops randomly

                    return random.choice([get_variable(var, database) for var in split_sequence[1:]])

                elif split_sequence[0] == "!if": # If statement proxy


                    if split_sequence[2] in comp_operators.keys():

                        comp1 = to_float_if_float(get_variable(split_sequence[1], database))
                        comp2 = to_float_if_float(get_variable(split_sequence[3], database))

                        print(comp1, comp2)

                        if comp_operators[split_sequence[2]](comp1, comp2):

                            add_sequence = sequence[idx+1]
                        
                        else:

                            add_sequence = sequence[idx+2]
                        
                        sequence = (sequence[:idx] + add_sequence + sequence[idx + 3:])
                        
                        idx -= 1
                    
                    else:

                        error(f"Comparator \"{split_sequence[2]}\" not found.", "6")

                    
                elif split_sequence[0] == "!sleep":

                    sleep_time = to_float_if_float(get_variable(split_sequence[1], database))
                    if type(sleep_time) != float:
                        error(f"Sleep error; value \"{sleep_time}\" not a float.", "2")
                    time.sleep()

                else:

                    error(f"Command not found \"{split_sequence[0]}\".", "3")

            # Comment; pass
            elif sequence[idx][0] == "#":
                pass

            elif sequence[idx][0] == "$":

                print(get_variable(sequence[idx],database))

            elif sequence[idx][0] == "?":
                
                database["output"] = input(sequence[idx][1:])

            else:

                print(sequence[idx]) 

            idx += 1
        
        except IndexError:

            error(f"Critical command failure command \"{split_sequence[0]}\" given incorrect arguments.", 10)
        
        except Exception as e:

            error(f"Unknown error, likely from Python, \"{e}\".", "?")
    
def check_state(state, origin_sequence):

    if state == None:

        sys.exit(0)

    elif state not in origin_sequence.keys():

            error(f"State \"{state}\" not found.", 1)
    
            exit(1)


# Runs main terminal, loop, iteratively running each sequence until the game is compelte
def execute_parse(origin_sequence, database):

    check_state(args.entry_point, origin_sequence)

    # Run origin sequence, and it continues until the game is done
    state = run_sequence(origin_sequence[args.entry_point], database)

    new_state = None

    while True:

        check_state(state, origin_sequence)

        new_state = run_sequence(origin_sequence[state], database)

        state = new_state


if __name__ == "__main__":

    execute_parse(origin_sequence, database)
