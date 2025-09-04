__all__ = ['TemplateString']

import os
import re
from collections.abc import Callable

from pydantic import AfterValidator
from typing_extensions import Annotated


def replace_default_vars(input_str: str) -> str:
    """Replaces predefined placeholder variables in a string.

    Substitutes placeholders like `%{time}`, `%{pid}`, `%{host}`, `%{root}`,
    `%{gitag}`, and `%{giturl}` with their corresponding dynamic values.

    Args:
        input_str (str): The string containing placeholder variables.

    Returns:
        str: The string with placeholders replaced.
    """
    from ..functions.git import get_git_tag, get_git_url_with_commit
    from ..functions.utils import get_root_dir, time_format

    # Define variable mapping table with lazy evaluation
    variable_resolvers: dict[str, Callable[[], str]] = {
        'time': lambda: time_format(fmt="%Y%m%d%H%M%S"),
        'pid': lambda: str(os.getpid()),
        'host': lambda: os.uname().nodename,
        'root': lambda: get_root_dir(),
        'gitag': lambda: get_git_tag(),
        'giturl': lambda: get_git_url_with_commit(),
    }

    # Use regex to find all placeholders at once
    def replace_match(match):
        var_name = match.group(1)
        if var_name in variable_resolvers:
            return variable_resolvers[var_name]()
        return match.group(0)  # Keep original if variable doesn't exist

    # Use regex to replace all matching placeholders
    return re.sub(r'%\{([^}]+)}', replace_match, input_str)


TemplateString: type[str] = Annotated[str, AfterValidator(replace_default_vars)]
