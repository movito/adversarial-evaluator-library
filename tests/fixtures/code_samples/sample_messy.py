"""
Messy Code Quality Module

This code contains INTENTIONAL code quality issues for testing code review evaluators.
It is functionally correct but violates coding standards and best practices.

Expected evaluator verdict: CHANGES_REQUESTED
Expected findings:
- Poor naming conventions
- Missing/outdated documentation
- Code duplication
- Long functions
- Magic numbers
- Dead code
- Inconsistent style
"""

import json
import os
import sys
import time
from datetime import datetime


# TODO: fix this later
# FIXME: this is broken
# XXX: temporary hack
# HACK: need to refactor


x = 10  # QUALITY: Single letter variable name
data = []  # QUALITY: Generic name, no type hint
temp = None  # QUALITY: "temp" is a code smell


def f(a, b, c, d, e, f, g, h):  # QUALITY: Too many parameters, unclear names
    """do stuff"""  # QUALITY: Unhelpful docstring
    return a + b + c + d + e + f + g + h


def processData(userData, processFlag, outputPath, debugMode, verboseMode, strictMode, legacyMode, experimentalMode):  # QUALITY: Too many params, camelCase inconsistent with Python
    # QUALITY: No docstring for complex function
    # QUALITY: Very long function (should be split up)

    result = []

    # QUALITY: Magic numbers throughout
    if len(userData) > 100:
        userData = userData[:100]

    for i in range(0, len(userData)):  # QUALITY: range(0, x) should be range(x)
        item = userData[i]

        # QUALITY: Deep nesting
        if item is not None:
            if isinstance(item, dict):
                if "name" in item:
                    if item["name"] != "":
                        if len(item["name"]) > 0:
                            if processFlag:
                                if not legacyMode:
                                    if experimentalMode:
                                        result.append(item["name"].upper())
                                    else:
                                        result.append(item["name"].lower())
                                else:
                                    result.append(item["name"])

    # QUALITY: Dead code - this block is never executed
    if False:
        print("This never runs")
        for item in result:
            print(item)

    # QUALITY: Commented out code
    # old_result = []
    # for item in userData:
    #     if item and isinstance(item, dict) and "name" in item:
    #         old_result.append(item["name"])
    # return old_result

    # QUALITY: Magic number
    time.sleep(0.5)

    # QUALITY: Duplicate code block 1
    output = []
    for r in result:
        if r is not None:
            if len(r) > 0:
                output.append(r.strip())

    # QUALITY: Duplicate code block 2 (nearly identical to above)
    final_output = []
    for o in output:
        if o is not None:
            if len(o) > 0:
                final_output.append(o.strip())

    # QUALITY: Inconsistent return - sometimes returns, sometimes doesn't
    if debugMode:
        print(f"Debug: {final_output}")

    if verboseMode == True:  # QUALITY: Should be 'if verboseMode:'
        print(f"Verbose output: processed {len(final_output)} items")

    if strictMode != False:  # QUALITY: Confusing double negative
        pass

    return final_output


class DataHandler:  # QUALITY: No docstring
    def __init__(self):
        self.d = []  # QUALITY: Single letter attribute
        self.lst = []  # QUALITY: Abbreviated name
        self.thing = None  # QUALITY: Vague name
        self.data2 = {}  # QUALITY: Numbered variable
        self.temp_data = []  # QUALITY: "temp" prefix
        self._privateStuff = []  # QUALITY: camelCase inconsistent

    def do_stuff(self):  # QUALITY: Vague method name, no docstring
        pass

    def handleData(self, d):  # QUALITY: camelCase inconsistent, single letter param
        self.d = d

    def process(self, a, b, c):  # QUALITY: No docstring, unclear params
        # same as above but different  # QUALITY: Unhelpful comment
        return a * b * c

    def calculate(self, x):  # QUALITY: Generic name
        # calculate the thing
        result = x * 2
        result = result + 10  # QUALITY: Could be result += 10
        result = result - 5
        result = result * 3
        return result

    def get_data(self):
        """
        Gets the data.  # QUALITY: Tautological docstring

        Returns the data that was stored.  # QUALITY: Doesn't add information
        """
        return self.d

    def validate(self, input):  # QUALITY: 'input' shadows builtin
        """validate input"""
        if input == None:  # QUALITY: Should use 'is None'
            return False
        if type(input) == str:  # QUALITY: Should use isinstance()
            return len(input) > 0
        if type(input) == int:
            return input >= 0
        if type(input) == list:
            return len(input) > 0
        return True

    def format_output(self, data, format, type):  # QUALITY: 'format' and 'type' shadow builtins
        """formats the output"""
        if format == "json":
            return json.dumps(data)
        elif format == "csv":
            return ",".join(str(x) for x in data)
        elif format == "text":
            return str(data)
        else:
            return data


def helperFunction():  # QUALITY: camelCase, no params, no return type, no docstring
    """helper"""
    return True


def another_helper():
    # This function does something
    # It was added on 2023-01-15 by John  # QUALITY: Irrelevant comment (use git blame)
    # Updated on 2023-02-20 to fix bug
    # Modified again on 2023-03-01
    pass


def processUserInput(userInput):  # QUALITY: camelCase
    # begin processing  # QUALITY: Obvious comment
    result = userInput  # QUALITY: Pointless assignment

    # check if empty  # QUALITY: Obvious comment
    if result == "":
        return None

    # return result  # QUALITY: Obvious comment
    return result


# QUALITY: Unused imports at top (sys, os)
# QUALITY: Unused function below
def unused_function():
    """This function is never called anywhere."""
    print("I am never used")
    return 42


# Global state  # QUALITY: Comment states the obvious
GLOBAL_COUNTER = 0
GLOBAL_DATA = []
CONFIG = {"a": 1, "b": 2}  # QUALITY: Vague keys


def increment():  # QUALITY: Modifies global state
    global GLOBAL_COUNTER
    GLOBAL_COUNTER += 1


def add_data(item):  # QUALITY: Modifies global state
    global GLOBAL_DATA
    GLOBAL_DATA.append(item)


# QUALITY: Magic numbers in constants without explanation
MAX_SIZE = 1000
MIN_SIZE = 10
TIMEOUT = 30
RETRY_COUNT = 3
BUFFER_SIZE = 4096
THRESHOLD = 0.75


def complex_calculation(a, b, c, d):
    """Does a complex calculation."""
    # QUALITY: Magic numbers
    result = a * 3.14159 + b * 2.71828 - c * 1.41421 + d * 1.61803
    if result > 100:
        result = result * 0.9  # QUALITY: Magic number
    elif result < 0:
        result = result * 1.1  # QUALITY: Magic number
    return result


# QUALITY: Class at bottom of file, inconsistent organization
class Utility:
    @staticmethod
    def method1():
        return 1

    @staticmethod
    def method2():
        return 2

    @staticmethod
    def method3():
        return 3

    # QUALITY: Code duplication
    @staticmethod
    def method4():
        return 4

    @staticmethod
    def method5():
        return 5
