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
import json


def process_doc_result(report_dir, report_name, cfg):
    toffee_result = os.path.join(report_dir, os.path.dirname(report_name), "toffee_report.json")
    assert os.path.exists(toffee_result), f"{toffee_result} not found, please check the toffee report"
    report_data = json.loads(open(toffee_result).read())
    # 0. get all the test cases
    # 1. get all functions coverage
    # 2. get all lines coverage
    # 3. save result to docutment
