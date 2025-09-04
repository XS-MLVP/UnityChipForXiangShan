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
    "base64_encode",
    "base64_decode",
]

import base64


def base64_encode(input_str: str) -> str:
    """Encodes a string into a Base64 representation.

    This function takes a standard string, encodes it into UTF-8 bytes,
    and then returns the Base64 encoded string.

    Args:
        input_str: The string to be encoded.

    Returns:
        The Base64 encoded string.
    """
    input_bytes = input_str.encode('utf-8')
    base64_bytes = base64.b64encode(input_bytes)
    base64_str = base64_bytes.decode('utf-8')
    return base64_str


def base64_decode(base64_str: str) -> str:
    """Decodes a Base64 encoded string into a UTF-8 string.

    Args:
        base64_str: The Base64 encoded string.

    Returns:
        The decoded UTF-8 string.

    Raises:
        binascii.Error: If the input `base64_str` is incorrectly padded or
            contains non-alphabet characters.
        UnicodeDecodeError: If the decoded bytes cannot be interpreted as
            valid UTF-8.
    """
    base64_bytes = base64_str.encode('utf-8')
    input_bytes = base64.b64decode(base64_bytes)
    return input_bytes.decode('utf-8')
