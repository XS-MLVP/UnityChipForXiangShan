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

class consts():
    Width = 3
    nRespDups = 1

class BaseConstant(int):
    """特殊常量基类"""
    __slots__ = ()
    _name = ""
    _value = None
    
    def __new__(cls):
        return int.__new__(cls, cls._value)
    
    def __repr__(self):
        return f"<{self._name}>"
    
    def __str__(self):
        return self._name
    
    def __eq__(self, other):
        return other == self._value or other is self

class DontCareType(BaseConstant):
    _name = "DONTCARE"
    _value = 0

class Unused0Type(BaseConstant):
    _name = "UNUSED_0"
    _value = 0

class Unused1Type(BaseConstant):
    _name = "UNUSED_1"
    _value = 1

DONTCARE = DontCareType()
UNUSED0 = Unused0Type()
UNUSED1 = Unused1Type()