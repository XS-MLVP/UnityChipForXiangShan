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
    "get_git_commit",
    "is_git_dirty",
    "get_git_branch",
    "get_git_tag",
    "get_git_remote_url",
    "get_git_url_with_commit",
]

import subprocess

from ..logger import warning


def get_git_commit() -> str:
    """Gets the current git commit hash.

    Returns:
        str: The full commit hash, or "none" if an error occurs.
    """
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
        return commit
    except subprocess.CalledProcessError as e:
        warning(f"Error getting git commit: {e}")
        return "none"


def is_git_dirty() -> bool:
    """Checks if the git working directory is dirty (has uncommitted changes).

    Returns:
        bool: True if there are uncommitted changes, False otherwise.
    """
    try:
        status = subprocess.check_output(["git", "status", "--porcelain"]).strip().decode("utf-8")
        return len(status) > 0
    except subprocess.CalledProcessError as e:
        warning(f"Error checking if git is dirty: {e}")
        return False


def get_git_branch() -> str:
    """Gets the current git branch name.

    Returns:
        str: The current branch name, or "none" if an error occurs.
    """
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode("utf-8")
        return branch
    except subprocess.CalledProcessError as e:
        warning(f"Error getting git branch: {e}")
        return "none"


def get_git_tag() -> str:
    """Generates a descriptive tag for the current git state.

    The format is 'branch-commit[-dirty]'.

    Returns:
        str: A string representing the complete git state tag.
    """
    return get_git_branch() + "-" + get_git_commit() + ("-dirty" if is_git_dirty() else "")


def get_git_remote_url() -> str:
    """Gets the remote 'origin' URL of the git repository.

    Returns:
        str: The remote URL, or "none" if not found or an error occurs.
    """
    try:
        url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).strip().decode("utf-8")
        return url
    except subprocess.CalledProcessError as e:
        return "none"


def get_git_url_with_commit() -> str:
    """Constructs a web URL for the current commit.

    This function formats the remote git URL into a browseable HTTPS link
    pointing to the specific commit tree.

    Returns:
        str: The full URL to the commit, or "none" if an error occurs.
    """
    url = get_git_remote_url()
    commit = get_git_commit()
    if url != "none" and commit != "none":
        return f"{url}/tree/{commit}".replace(".git/", "/").replace(
            "git@github.com:", "https://github.com/").strip() + (" (dirty)" if is_git_dirty() else "")
    return "none"
