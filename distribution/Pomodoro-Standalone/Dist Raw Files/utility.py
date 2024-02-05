import inspect
import sys


def verbose(debug, observations=None, same_line=False):
    if debug:
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        function_name = caller_frame.f_code.co_name

        verbose_text = f' -> {function_name} '
        if observations:
            verbose_text += f' | {observations}...'
        else:
            verbose_text += '...'

        if same_line:
            print(f'\r{verbose_text}', end='', )
            sys.stdout.flush()
        else:
            print(verbose_text)


def print_selected_attributes(obj, attribute_names=None):
    """
    Prints specified attributes of an object. If attribute_names is None,
    prints all attributes of the object.
    """
    if attribute_names is None:
        # Print all attributes
        for attr in vars(obj):
            print(f"  {attr}: {getattr(obj, attr)}")
    else:
        # Print only specified attributes
        for attr in attribute_names:
            if hasattr(obj, attr):
                print(f"  {attr}: {getattr(obj, attr)}")
            else:
                print(f"  Attribute '{attr}' not found in the object.")
