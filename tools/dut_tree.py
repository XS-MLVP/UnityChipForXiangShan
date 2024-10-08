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

import json
import copy

node_default_meta_data = {
    "cases":     {"total": 0, "pass": 0, "fail": 0, "skip": 0},
    "functions": {"total": 0, "cover": 0},
    "lines":     {"total": 0, "cover": 0},
    "paths":     "",
    "value":     1,
    "light":     False,
}

node_defaut_extern = {
    "itemStyle": {
        "colorAlpha": 0.1,
    }
}

priority_critical = 0
priority_high = 1
priority_low = 2

dut_priority_low = {
    "priority": priority_low
}

dut_priority_high = {
    "priority": priority_high
}

dut_priority_critical = {
    "priority": priority_critical
}

def update_dut_tree_node_meta(tree_data):
    def _update_node_meta(node, parent_name):
        if "children" in node:
            meta = copy.deepcopy(node_default_meta_data)
            meta["paths"] = parent_name + "/" + node["name"]
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
                meta["value"] += child_meta["value"]
            node["meta"] = meta
            node["value"] = node["meta"]["value"]
        else:
            node["meta"]["paths"] = parent_name + "/" + node["name"]
        return node["meta"]
    _update_node_meta(tree_data, "")
    return tree_data


def init_dut_tree(tree_data):
    def _append_meta_to_leaf(node):
        if "children" not in node:
            node["meta"] = copy.deepcopy(node_default_meta_data)
            node["value"] = node["meta"]["value"]
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
            assert path in leaf_map, "Path not found: %s" % path
            leaf_map[path]["meta"] = {**leaf_map[path]["meta"], **meta}
            leaf_map[path]["value"] = leaf_map[path]["meta"]["value"]
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
                   ("line-coverage-rate(%)","", lambda x: 100*x["lines"]["cover"]/x["lines"]["total"] if x["lines"]["total"] > 0 else 0)]:
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
        return json.dumps({
            "list": list_data,
            "tree": self.tree
        }, indent=4)
