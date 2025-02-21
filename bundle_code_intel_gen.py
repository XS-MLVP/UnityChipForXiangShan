import json
import argparse
import os

# calculate hash of a number set, so as to distinct between two sets
def set_hash(set_in):
    str_res = "_"
    for num in set_in:
        str_res = f"{str_res}_{num}"
    return hash(str_res)

class MProxy():
    stored = ''
    leaf = None

    def print(self, str_in=''):
        self.stored += str_in + '\n'

    def get(self):
        return self.stored

    def get_leave_hash(self, ob):
        if self.leaf is None:
            self.leaf = hash(ob)
        return self.leaf 

# dfs function
# node: the current node to be visit
# logs: stores the name and some other might be useful attrs(now some of them are useless though)
# insides: stores all the nodes' full name of the same kind. For bundles, also stores the index of the unique bundle
# prefix: prefix str of current node
# bundle_names_counter: store the bundle name, which might be useful in the future
def visit(node, logs, insides, prefix, bundle_names_counter, rp:MProxy):
    leaf = 0
    sons = set()
    for son_name in node:
        
        if type(node[son_name]) == dict:
            leaf |= 2 # node type
            whole_name = f"{prefix}{son_name}"
            grandsons, son_leaf = visit(node[son_name], logs, insides, f"{whole_name}_", bundle_names_counter, rp)
            inside_hash = set_hash(grandsons)
            cur_hashes = set()
            cur_hashes.add(son_name)
            cur_hashes.add(inside_hash)
            # to distinguish between leaf and both and node
            cur_hashes.add(son_leaf)
            son_hash = set_hash(cur_hashes)
            if son_hash not in logs.keys():
                # if son_leaf & 1:
                    # son hash as outsiders with name added to hash
                logs[son_hash] = (son_leaf, inside_hash, son_name, whole_name, grandsons, [])
                # else:
                    # logs[son_hash] = (False, inside_hash, son_name, whole_name, grandsons)  
            if inside_hash not in insides.keys():
                insides[inside_hash] = [son_leaf, [], "", []]
                if son_leaf & 2:
                    # new bundle appears
                    insides[inside_hash][2] = bundle_names_counter[0]
                    bundle_names_counter[1].append(f"_{bundle_names_counter[0]}Bundle")
                    rp.print(f"class {bundle_names_counter[1][bundle_names_counter[0]]}(Bundle):")

                    son_bundles = {}
                    boths = {}
                    for grandson in grandsons:
                        name = logs[grandson][2]
                        boths[name] = False
                        leaf_res = logs[grandson][0]

                        if leaf_res & 2:
                            grandson_inside = logs[grandson][1]
                            if grandson_inside not in son_bundles:
                                son_bundles[grandson_inside] = []
                            son_bundles[grandson_inside].append(name)
                        
                        if leaf_res & 1:
                            # out of the frustrating compilation optimization, we have to take a look at the "same name" of leaf and node
                            if leaf_res & 2:
                                boths[name] = True
                            if prefix != "":
                                name = f"_{name}"
                            insides[inside_hash][3].append(f"{name}")

                    for bundle_hash in son_bundles.keys():
                        bundle_cls = bundle_names_counter[1][insides[bundle_hash][2]]
                        for prefix_name in son_bundles[bundle_hash]:
                            tprefix_name = prefix_name
                            if len(prefix) > 0:
                                tprefix_name = f"_{tprefix_name}"
                            if boths[prefix_name]:
                                son_leaves = insides[bundle_hash][3]
                                for _son_leaf in son_leaves:
                                    leaf_name = f"{tprefix_name}{_son_leaf}"
                                    insides[inside_hash][3].append(leaf_name)
                            else:
                                rp.print(f"\t{tprefix_name} = {bundle_cls}.from_prefix(\"{tprefix_name}\")")

                    if len(insides[inside_hash][3]) > 0:
                        leaves_str = ', '.join(insides[inside_hash][3])
                        after_str = f"Signals({len(insides[inside_hash][3])})" if len(insides[inside_hash][3]) > 1 else "Signal()"
                        rp.print(f"\t{leaves_str} = {after_str}")

                    rp.print()

                    bundle_names_counter[0] += 1

            insides[inside_hash][1].append(whole_name)
            sons.add(son_hash)
        else:
            
            leaf |= 1 # leaf
            # son_hash = rp.get_leave_hash(node[son_name]) # for all leaves, ways to deal in toffee are same, they are all signals, so get a staic value equal to

    return sons, leaf

def main(signals_path, target_path):
    with open(signals_path, "r", encoding="utf-8") as sig_file:
        data = json.load(sig_file)

    notes = {}
    insides = {}
    module_name = "PredCheckerAll"
    rpr = MProxy()
    rpr.print("from toffee import Bundle, Signals, Signal\n")
    data = {module_name: data}
    sons, _ = visit(data, notes, insides, "", [0, []], rpr)

    with open(target_path, "w", encoding="utf-8") as tgt_f:
        tgt_f.write(rpr.get())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('signal', type=str, default='')
    parser.add_argument('target', type=str, default='')
    args = parser.parse_args()
    main(args.signal, args.target)