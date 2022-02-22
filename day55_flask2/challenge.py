# Create the logging_decorator() function 👇
def logging_decorator(function):
    def wrapper(*args, **kwargs):
        value = function(args[0], args[1], args[2])
        print(
            f"You called {function.__name__}({args[0]}, {args[1]}, {args[2]})\n"
            f"It returned: {value}"
        )
    return wrapper


# Use the decorator 👇
@logging_decorator
def a_function(param1, param2, param3):
    return sum((param1, param2, param3))

a_function(1,2,3)
