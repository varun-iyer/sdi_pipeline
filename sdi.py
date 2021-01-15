from functools import update_wrapper
import click
import inspect

@click.group(chain=True)
def cli():
    """
    asdfkajsdfh
    """

@cli.resultcallback()
def run_pipeline(operators):
    """
    Callback is invoked with an iterable of all subcommands
    """
    # a list of fitsfiles passed through the whole pipeline
    hduls = ()
    print(operators)
    for operator in operators:
        hduls = operator(hduls)
        print(hduls)

    for _ in hduls:
        # do necessary things on overall outputs
        pass

def operator(func):
    """
    Decorator which wraps commands so that they return functions after being
    run by click.
    All of the returned functions are passed as an iterable
    into run_pipeline.
    """
    def new_func(*args, **kwargs):
        def operator(hduls):
            # args and kwargs are subcommand-specific
            return func(hduls, *args, **kwargs)
        return operator

    # basically return new_func, but better
    return update_wrapper(new_func, func)

def generator(func):
    """
    Does what operator does, but for the first thing in the series, like
    opening the hduls.
    Works with sub-funcs that do not have 'hduls' as the first argument.
    """
    @operator
    def new_func(hduls, *args, **kwargs):
        yield from hduls
        yield from func(*args, **kwargs)
    return update_wrapper(new_func, func)

@cli.command("start")
@generator
def start():
    print("start")
    return "begin"

@cli.command("hello")
@operator
def hello(hduls):
    return "hello"

@cli.command("goodbye")
@operator
def hello(hduls):
    return "goodbye"
