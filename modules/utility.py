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
