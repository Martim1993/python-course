def log_function_call(func):
    def wrapper(a, b, c=None):

        print(f"Calling function: {func.__name__}")

        if c is not None:
            result = func(a, b, c)
            print(f"Arguments: {a, b, c}")
        else:
            result = func(a, b)
            print(f"Arguments: {a, b}")

        print(f"Result: {result}\n")
        return result
    return wrapper


@log_function_call
def add(a, b):
    return a + b


@log_function_call
def multiply(a, b, c):
    return a * b * c


add(2,3)
multiply(1, 2, 3)


def main():
    add(2, 3)
    multiply(1, 2, 3)


main()
