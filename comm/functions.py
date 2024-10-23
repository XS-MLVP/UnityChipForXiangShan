#coding=utf8
#***************************************************************************************
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
#**************************************************************************************/
import os
import mlvp

def merge_dict(dict1, dict2):
    """
    Merge two dictionaries
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

def get_out_dir(subdir=""):
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../out', subdir))

def debug(msg):
    mlvp.debug(msg)


def is_full_test():
    return os.getenv("XS_FULL_TEST") == "1" or os.getenv("XS_FULL_TEST") == "true"


def is_short_test():
    return not is_full_test()
