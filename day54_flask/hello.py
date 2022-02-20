import time
# from flask import Flask
# app = Flask(__name__)
#
# Decorator purpose here...
# If someone calls the home page (i.e. /)
# execute the below function
#@app.route('/')
# def hello():
#     return 'Hello World'


def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        # ^^^^
        # useful for doing something before 'function'
        function()
        # or after VVVV
    return wrapper_function

@delay_decorator
def say_hello():
    print("Hello")

@delay_decorator
def say_bye():
    print("Hello")

@delay_decorator
def say_greeting():
    print("How's it going?")

# Decorator as above similar to doing
# decorated_function = delay_decorator(my_function)
# then calling decorated_function()


def time_elapsed(function):
    def wrapper_function():
        start = time.time()
        function()
        print(f"{function.__name__} completed in {time.time() - start:.3f}s")
    return wrapper_function

