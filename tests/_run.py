import os
import time

start = time.time()

test_res = ""
warns = 0
errors = 0

def check_file(filename: str):
    global test_res
    global warns
    global errors

    module = __import__(filename[:-3])

    result = module.main()

    if result [0] != 0:
        if result[0] == 1:
            error_type = "Warning"
            warns += 1

        elif result[0] == 2:
            error_type = "Error"
            errors += 1

            test_res += f"Test {module.__name__} has failed with code {result[0]} ({error_type}), {result[1]}\n"
    
    return

def main():
    global test_res
    global warns
    global errors

    for filename in (os.listdir(os.path.dirname(__file__))):
        if filename.endswith(".py") and filename[0] != "_":
            check_file(filename)


    if test_res == "":
        test_res = "All tests passed successfully"
    else:
        test_res = f"Tests failed with a total of {warns} warnings and {errors} errors\n\n{test_res}"

    end = time.time()

    test_res = f"{test_res}\nTook {round(end - start, 2)} seconds"
    print(test_res)

if __name__ == "__main__":
    main()