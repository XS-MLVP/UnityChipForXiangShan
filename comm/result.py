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
import yaml
import copy
import re
import fnmatch
from .logger import warning


def process_doc_result(report_dir, report_name, cfg):
    if cfg.doc_result.disable:
        return
    from .functions import get_abs_path, time_format
    extend_info = {"time": time_format(fmt="%Y-%m-%d %H:%M:%S")}
    toffee_result = os.path.join(report_dir, os.path.dirname(report_name), "toffee_report.json")
    assert os.path.exists(toffee_result), f"{toffee_result} not found, please check the toffee report"
    report_data = json.loads(open(toffee_result).read())
    extend_info["raw_report"] = report_data
    # 0. load dut tree
    tree_yaml = get_abs_path(cfg.doc_result.dutree, "", cfg)
    # 1. get all the test cases
    dut_tree = DutTree(yaml.load(open(tree_yaml).read(), Loader=yaml.FullLoader))
    dut_data = dut_tree.as_dict()
    leaf_meta = {}
    for case in report_data["tests"]:
        case_path = case["phases"][0]["report"].split(" ")[1].split("::")[0].replace("'", "")
        case_status = case["status"]
        path = parse_dut_path(case_path, dut_data, "ut_")
        if path not in leaf_meta:
            leaf_meta[path] = copy.deepcopy(node_default_meta_data)
        leaf_meta[path]["cases"]["total"] += 1
        if case_status["category"] == "passed":
            leaf_meta[path]["cases"]["pass"] += 1
        elif case_status["category"] == "skipped":
            leaf_meta[path]["cases"]["skip"] += 1
        else:
            leaf_meta[path]["cases"]["fail"] += 1
        if case_status["category"] == "skipped":
            # find skip reason
            for phase in case["phases"]:
                if phase["status"]["category"] == "skipped":
                    leaf_meta[path]["cases"]["reason"] = parse_case_exception_reson(phase["call"])
                    break
        if path not in extend_info:
            extend_info[path] = {"target_line_coverage_files": [],
                                 "matched_line_coverage_files":[],
                                 }
    # 2. get all functions coverage
    for group in report_data["coverages"]["functional"]["groups"]:
        path = get_leaf_path_by_group(leaf_meta, group["name"], dut_data, "ut_")
        if path is not None:
            leaf_meta[path]["functions"]["total"] += group["bin_num_total"]
            leaf_meta[path]["functions"]["cover"] += group["bin_num_hints"]
    # 3. get all lines coverage
    for path in leaf_meta.keys():
        line_files = get_line_coverage_files(path, cfg, dut_data, "build_ut_")
        if(len(line_files) == 0):
            continue
        line_hint, line_total = search_line_coverage(line_files, os.path.join(report_dir,
                                                     os.path.dirname(report_name), "line_dat"), path, extend_info)
        leaf_meta[path]["lines"]["total"] += line_total
        leaf_meta[path]["lines"]["cover"] += line_hint
    # 4. save result to docutment
    dut_tree.update_leaf_meta(leaf_meta)
    result = dut_tree.export_echart_jsondata(dut_data.get("dut_block", []))
    result["extend"] = extend_info
    result["config"] = dut_data.get("config",{})
    result_file = os.path.join(os.path.dirname(toffee_result), cfg.doc_result.result_name)
    with open(result_file, "w+") as file:
        json.dump(result, file, indent=4)
    # 5. link report dir to doc report dir
    link_path = get_abs_path(cfg.doc_result.report_link, "", cfg)
    if not os.path.exists(link_path):
        os.symlink(report_dir, link_path, target_is_directory=True)


def search_line_coverage(lc_files, target_dir, path, extend_info):
    all_files = []
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if not file.endswith(".gcov.html"):
                continue
            all_files.append(os.path.join(root, file))
    target_file = []
    for f in lc_files:
        matched = False
        if "*" in f or "?" in f:
            mfiles = fnmatch.filter(all_files, f)
            target_file.extend(mfiles)
            if len(mfiles) == 0:
                warning(f"target line coverage file '{f}' not found for: {path}")
            else:
                matched = True
        else:
            find = False
            for file in all_files:
                file_name = os.path.basename(file)
                if "/" not in f and f in file_name:
                    target_file.append(file)
                    find = True
                elif f in file:
                    target_file.append(file)
                    find = True
            if not find:
                warning(f"target line coverage file '{f}' not found for: {path[1:].replace('/', '.')}")
            else:
                matched = True
        extend_info[path]["target_line_coverage_files"].append(f if matched else f + " (not found)")
    # search line coverage in html files
    line_hint = 0
    line_total = 0
    for f in target_file:
        find = 0
        with open(f, "r") as file:
            for ln in file.readlines():
                if find  == 0 and '<td class="headerItem">Lines:</td>' in ln:
                    find = 1
                    continue
                if find == 1:
                    line_hint = int(re.search(r'class="headerCovTableEntry">(\d+)</td>', ln).group(1))
                    find = 2
                elif find == 2:
                    line_total = int(re.search(r'class="headerCovTableEntry">(\d+)</td>', ln).group(1))
                    break
        if find != 2:
            warning(f"Failed to get line coverage from {f}")
            line_total = 0
            line_hint = 0
        extend_info[path]["matched_line_coverage_files"].append((f.replace(os.path.abspath(
            os.path.join(target_dir, "..")), ""), line_hint, line_total))
    return line_hint, line_total


def get_line_coverage_files(path, cfg, dut_data, prefix):
    from .functions import get_root_dir
    import importlib
    mname = path.replace("/%s/"%dut_data["name"], prefix).replace("/", "_")
    script_python = get_root_dir("scripts/%s.py" % mname)
    if not os.path.exists(script_python):
        warning("Script not found: %s, please check your script" % script_python)
        return []
    try:
        module = importlib.import_module("scripts.%s" % mname)
        line_conver_file = module.line_coverage_files(cfg)
        if len(line_conver_file) == 0:
            warning("No line coverage files found in %s" % script_python)
        return line_conver_file
    except Exception as e:
        warning("Failed to get line coverage files from %s, you need to implement 'line_coverage_files' correctly, error: %s" % (script_python, e))
        return []


def get_leaf_path_by_group(leaf_meta, group_name, dut_data, prefix):
    path = group_name.replace(".", "/")
    if path.startswith(prefix):
        path = path[len(prefix):]
    path = "/%s/" % dut_data["name"] + path
    for p in leaf_meta.keys():
        if path.startswith(p):
            return p
    warning("DUT path not found: %s, please check your function coverage group name format" % path)
    return None


def parse_case_exception_reson(call_info):
    match = re.search(r"excinfo=<ExceptionInfo\s+(.*?)\s+tblen=", call_info)
    if match:
        return match.group(1)
    return ""


def parse_dut_path(path, dut_tree, prefix):
    module_name = os.path.dirname(path)
    if module_name.startswith(prefix):
        module_name = module_name[len(prefix):]
    return "/" + dut_tree["name"] + "/" + module_name


node_default_meta_data = {
    "cases":     {"total": 0, "pass": 0, "fail": 0, "skip": 0},
    "functions": {"total": 0, "cover": 0},
    "lines":     {"total": 0, "cover": 0},
    "paths":     "",
    "light":     False,
    "light_count": 0,
    "doc_url":   "",
}


node_defaut_extern = {
    "itemStyle": {
        "colorAlpha": 0.1,
    }
}


def update_dut_tree_node_meta(tree_data):
    def _update_node_meta(node, parent_name):
        if "children" in node:
            meta = copy.deepcopy(node_default_meta_data)
            meta["paths"] = parent_name + "/" + node["name"]
            value = 0
            for child in node["children"]:
                child_meta = _update_node_meta(child, meta["paths"])
                meta["cases"]["total"] += child_meta["cases"]["total"]
                meta["cases"]["pass"] += child_meta["cases"]["pass"]
                meta["cases"]["fail"] += child_meta["cases"]["fail"]
                meta["cases"]["skip"] += child_meta["cases"]["skip"]
                meta["functions"]["total"] += child_meta["functions"]["total"]
                meta["functions"]["cover"] += child_meta["functions"]["cover"]
                meta["lines"]["total"] += child_meta["lines"]["total"]
                meta["lines"]["cover"] += child_meta["lines"]["cover"]
                meta["lines"]["text"] = "%d/%d (%.2f %%)" % (meta["lines"]["cover"], meta["lines"]["total"],
                                                             float(meta["lines"]["cover"])/meta["lines"]["total"]*100) if meta["lines"]["total"] > 0 else "0/0 (0.00 %)"
                meta["light_count"] += child_meta["light_count"]
                value += child.get("value", 1)
            node["meta"] = meta
            node["value"] = value
        else:
            node["meta"]["paths"] = parent_name + "/" + node["name"]
            node["meta"]["light_count"] = 1 if node["meta"]["light"] else 0
        return node["meta"]
    _update_node_meta(tree_data, "")
    return tree_data


def init_dut_tree(tree_data):
    def _append_meta_to_leaf(node):
        if "children" not in node:
            meta = copy.deepcopy(node_default_meta_data)
            meta.update(node.get("meta",{}))
            node["meta"] = meta
            node["value"] = 1
            node.update(copy.deepcopy(node_defaut_extern))
        else:
            for child in node["children"]:
                _append_meta_to_leaf(child)
    _append_meta_to_leaf(tree_data)
    return tree_data


class DutTree(object):
    def __init__(self, tree):
        self.tree = init_dut_tree(copy.deepcopy(tree))

    def as_json(self):
        update_dut_tree_node_meta(self.tree)
        return json.dumps(self.tree, indent=4)

    def as_dict(self):
        update_dut_tree_node_meta(self.tree)
        return self.tree

    def from_json(self, json_str):
        self.tree = json.loads(json_str)

    def update_leaf_meta(self, meta_path_values: dict, update=True):
        # get all nodes mapping to meta_path_values
        if update:
            update_dut_tree_node_meta(self.tree)
        leaf_map = {}
        def seek_leaf_node(node):
            if "children" not in node:
                key = node["meta"]["paths"]
                assert key not in leaf_map, "Duplicate key: %s" % key
                leaf_map[key] = node
            else:
                for child in node["children"]:
                    seek_leaf_node(child)
        seek_leaf_node(self.tree)
        for path, meta in meta_path_values.items():
            if not path in leaf_map:
                warning("Path not found: %s, please check your dut module struct" % path)
                continue
            leaf_map[path]["meta"] = {**leaf_map[path]["meta"], **meta}
            total = leaf_map[path]["meta"]["cases"]["total"]
            if total > 0:
                leaf_map[path]["itemStyle"]["colorAlpha"] = min(1.0, float(total)/10.0)
                leaf_map[path]["meta"]["light"] = total >= 10

    def export_nodes_as_list(self, node_names=[], update=True):
        if update:
            update_dut_tree_node_meta(self.tree)
        info_list = []
        def seek_leaf_node(node):
            if node["name"] in node_names or "children" not in node:
                # get info: name, cases(total, pass, fail, skip), functions (covered/total), lines (covered/total)
                info_list.append({
                    "name": node["name"] + ("-*" if "children" in node else ""),
                    "cases": node["meta"]["cases"],
                    "functions": node["meta"]["functions"],
                    "lines": node["meta"]["lines"],
                })
            else:
                for child in node["children"]:
                    seek_leaf_node(child)
        seek_leaf_node(self.tree)
        return info_list

    def export_echart_jsondata(self, node_names=[]):
        update_dut_tree_node_meta(self.tree)
        node_list = self.export_nodes_as_list(node_names, False)
        list_data = {
            "names": [],
            "series": [],
        }
        for se in [("passed cases", "cases", lambda x:x["cases"]["pass"]),
                   ("failed cases", "cases", lambda x:x["cases"]["fail"]),
                   ("skiped cases", "cases", lambda x:x["cases"]["skip"]),
                   ("function covered", "function", lambda x:x["functions"]["cover"]),
                   ("function un-covered", "function", lambda x:x["functions"]["total"]-x["functions"]["cover"]),
                   ("line-coverage-rate","", lambda x: "%d/%d (%.2f %%)" %(x["lines"]["cover"], x["lines"]["total"],
                                                                       100*x["lines"]["cover"] /x["lines"]["total"])
                                                                        if x["lines"]["total"] > 0 else "0/0 (0.00 %)")]:
            data = {
                "name": se[0],
                "type": "bar",
                "data": []
            }
            if se[1]:
                data["stack"] = se[1]
            name_empty = list_data["names"] == []
            for node in node_list:
                data["data"].append(se[2](node))
                if name_empty:
                    list_data["names"].append(node["name"])
            list_data["series"].append(data)
        return {
            "list": list_data,
            "tree": self.tree
        }
