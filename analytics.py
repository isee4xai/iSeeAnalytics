import json


def get_node_counts(execs, node_types=None):
    node_counts = {}
    for exe in execs:
        if node_types and exe["https://www.w3id.org/iSeeOnto/BehaviourTree#enacted"]["class"] not in node_types:
            continue
        if exe["https://www.w3id.org/iSeeOnto/BehaviourTree#enacted"]["instance"] in node_counts:
            node_counts[exe["https://www.w3id.org/iSeeOnto/BehaviourTree#enacted"]["instance"]
                        ] = node_counts[exe["https://www.w3id.org/iSeeOnto/BehaviourTree#enacted"]["instance"]] + 1
        else:
            node_counts[exe["https://www.w3id.org/iSeeOnto/BehaviourTree#enacted"]["instance"]] = 1
    return node_counts


def bt_exec_eval_question(data):
    node_counts = {}
    for key in data:
        content = data[key]
        nodes = content["interaction"]["nodes"]
        execs = content["interaction"]["executions"]
        eval_execs = [exe for exe in execs if exe["https://www.w3id.org/iSeeOnto/BehaviourTree#enacted"]
                      ["class"] == "https://www.w3id.org/iSeeOnto/BehaviourTree#EvaluationQuestionNode"]
        for ev in eval_execs:
            gen = ev["http://www.w3.org/ns/prov#generated"]["https://www.w3id.org/iSeeOnto/BehaviourTree#properties"]["https://www.w3id.org/iSeeOnto/BehaviourTree#hasDictionaryMember"]
            q = [g["https://www.w3id.org/iSeeOnto/BehaviourTree#pair_value_object"]["content"]
                 for g in gen if g["https://www.w3id.org/iSeeOnto/BehaviourTree#pairKey"] == "question"]
            v = [g["https://www.w3id.org/iSeeOnto/BehaviourTree#pair_value_object"]["content"]
                 for g in gen if g["https://www.w3id.org/iSeeOnto/BehaviourTree#pairKey"] == "variable"]
            if q and v:
                if q[0] in node_counts:
                    temp = node_counts[q[0]]
                    temp.append(v[0])
                    node_counts[q[0]] = temp
                else:
                    node_counts[q[0]] = [v[0]]
    return node_counts


def bt_execution(data, node_types=None):
    agg_node_counts = {}
    ind_node_counts = {}
    for key in data:
        content = data[key]
        nodes = content["interaction"]["nodes"]
        executions = content["interaction"]["executions"]
        node_counts = get_node_counts(executions, node_types)
        for k in node_counts:
            agg_node_counts[k] = agg_node_counts[k] + \
                node_counts[k] if k in agg_node_counts else node_counts[k]
        ind_node_counts[key] = node_counts
    return agg_node_counts, ind_node_counts
