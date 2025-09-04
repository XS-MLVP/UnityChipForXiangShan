# coding=utf8
# ***************************************************************************************
# This project is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#
# See the Mulan PSL v2 for more details.
# **************************************************************************************/

__all__ = [
    "get_root_dir",
    "get_abs_path",
    "time_format",
    "merge_dict",
    "exe_cmd",
    "UT_FCOV",
    "remove_version_tag",
    "module_name_with",
    "is_all_file_exist",
]

import inspect
import os
import time


def get_root_dir(subdir: str = "") -> str:
    """Gets the absolute path to the project's root directory.

    Calculates the root directory based on the location of the current file.

    Args:
        subdir (str, optional): A subdirectory to append to the root path.
            Defaults to "".

    Returns:
        str: The absolute path to the root directory or the specified subdirectory.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../", subdir))


def get_abs_path(path: str, sub: str, cfg) -> str:
    """Constructs an absolute path from a base path and a subdirectory.

    If the `path` is absolute, `sub` is joined to it. If it's relative, it
    is resolved relative to the directory of the configuration file. Placeholders
    in `path` are resolved first.

    Args:
        path (str): The base path, which can be absolute or relative.
        sub (str): The subdirectory to append to the base path.
        cfg: The configuration object, used for variable replacement and as a
            base for resolving relative paths.

    Returns:
        str: The resulting absolute path.
    """
    ret_path = ""
    if path.startswith("/"):
        ret_path = os.path.join(path, sub)
    else:
        ret_path = os.path.abspath(os.path.join(os.path.dirname(cfg.__file__), path, sub))
    if ret_path.endswith("/"):
        ret_path = ret_path[:-1]
    return ret_path


def time_format(seconds: float = None, fmt: str = "%Y%m%d-%H%M%S") -> str:
    """Formats a timestamp into a string.

    Converts a given timestamp (in seconds since the epoch) into a
    string according to the specified format. Uses the current time if no
    timestamp is provided.

    Args:
        seconds (float, optional): Seconds since the epoch. Defaults to `time.time()`.
        fmt (str, optional): The format string for `time.strftime`.
            Defaults to "%Y%m%d-%H%M%S".

    Returns:
        str: The formatted time string.
    """
    if seconds is None:
        seconds = time.time()
    return time.strftime(fmt, time.gmtime(seconds))


def merge_dict(dict1: dict, dict2: dict) -> dict:
    """Recursively merges two dictionaries.

    Merges `dict2` into `dict1` in-place. If a key exists in both and both
    values are dictionaries, they are merged recursively. Otherwise, the
    value from `dict2` overwrites the value in `dict1`.

    Args:
        dict1 (dict): The dictionary to merge into.
        dict2 (dict): The dictionary to merge from.

    Returns:
        dict: The modified `dict1`.
    """
    if not dict1:
        return dict2
    if not dict2:
        return dict1
    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                merge_dict(dict1[key], dict2[key])
            else:
                dict1[key] = dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1


def exe_cmd(cmd, no_log: bool = False) -> tuple[bool, str, str]:
    """Executes a shell command.

    Args:
        cmd (str | list[str]): The command to execute. If a list, it's joined
            into a single string.
        no_log (bool): If True, stdout and stderr are captured and returned.
            If False, they are printed to the console. Defaults to False.

    Returns:
        tuple[bool, str, str]: A tuple containing a success boolean (based on
            return code), the captured stdout, and the captured stderr.
            Stdout/stderr are empty if `no_log` is False.
    """
    import subprocess
    if isinstance(cmd, list):
        cmd = " ".join(cmd)
    if no_log:
        result = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout = result.stdout.decode("utf-8")
        stderr = result.stderr.decode("utf-8")
    else:
        result = subprocess.run(cmd, shell=True)
        stdout = ""
        stderr = ""
    success = result.returncode == 0
    return success, stdout, stderr


def UT_FCOV(group: str, ignore_prefix: str = "ut_") -> str:
    """Generates a hierarchical name for a unit test feature coverage group.

    Constructs a unique group name based on the calling function's module
    path, making it easier to organize coverage results.

    Args:
        group (str): The specific name of the coverage group.
        ignore_prefix (str, optional): A prefix to remove from the final
            generated name. Defaults to "ut_".

    Returns:
        str: A dot-separated string representing the full coverage group path.
    """
    frame = inspect.currentframe()
    caller_frame = frame.f_back
    caller_module = inspect.getmodule(caller_frame)
    if caller_module:
        gname = "/".join(caller_module.__name__.split("UnityChipForXiangShan.")[-1].split("."))
        gname = os.path.normpath(os.path.join(gname, group)).replace("/", ".")
        if gname.startswith(ignore_prefix):
            gname = gname[len(ignore_prefix):]
        return gname
    return "unknown." + os.path.normpath(group)


def remove_version_tag(version_str: str, split_char: str = "-", tag_pos: int = -2) -> str:
    """Removes a specific tag from a version string.

    Splits the string and removes the element at a specified position.
    For example, 'name-tag-number' with default args becomes 'name-number'.

    Args:
        version_str (str): The version string to modify.
        split_char (str, optional): The character to split the string by.
            Defaults to `-`.
        tag_pos (int, optional): The index of the tag to remove after splitting.
            Defaults to -2.

    Returns:
        str: The modified version string.
    """
    if split_char in version_str:
        vlist = version_str.split(split_char)
        vlist.pop(tag_pos)  # name-tag-number => name-tag
        return split_char.join(vlist)
    return version_str


def module_name_with(names, prefix: str = None):
    """Prepends the caller's module path to a name or list of names.

    Useful for creating fully qualified names for tests or other components
    based on their file location.

    Args:
        names (str | list[str]): A name or list of names to qualify.
        prefix (str, optional): A path-like prefix to append to the module
            path before joining with the names.

    Returns:
        str | list[str]: The fully qualified name or list of names.

    Raises:
        ValueError: If `names` is not a string or a list.
    """
    caller_module = inspect.getmodule(inspect.currentframe().f_back)
    assert caller_module, "Failed to get caller module"
    mname = caller_module.__name__
    if prefix:
        mname = os.path.normpath(os.path.join(mname.replace(".", "/"),
                                              prefix)).replace("/", ".")
    if isinstance(names, str):
        return mname + "." + names
    elif isinstance(names, list):
        return [mname + "." + n for n in names]
    raise ValueError("Invalid names type")


def is_all_file_exist(files_to_check: list[str], dir: str):
    """Checks if all files in a list exist within a directory.

    Args:
        files_to_check (list[str]): A list of filenames to check.
        dir (str): The directory where files are expected to be.

    Returns:
        bool | str: Returns `True` if all files exist, otherwise returns the
            filename of the first file that was not found.
    """
    for f in files_to_check:
        if not os.path.exists(os.path.join(dir, f)):
            return f
    return True
