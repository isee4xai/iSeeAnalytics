import json
import requests
import analytics

API_BASE = "<api-base>"
TOKEN = "<test-token>"


def request(url, _params):
    _headers = {
        "Content-Type": "application/json",
        "x-access-token": TOKEN
    }
    response = requests.get(url, params=_params, headers=_headers)
    json_res = json.loads(response.text)

    return json_res


def get_interaction_content(usecase_id):
    url = API_BASE + "interaction/usecase/" + usecase_id
    interactions = request(url, {})
    contents = {}
    for item in interactions:
        url = API_BASE + "interaction/usecase/" + \
            usecase_id + "/json/"+item["_id"]
        content = request(url, {})
        contents[item["_id"]] = content
    return contents


def main():
    usecase_id = "<usecase-id>"
    version = 10  # need to include in the query
    contents = get_interaction_content(usecase_id)
    # bt_exec = analytics.bt_execution(contents)
    # agg_counts, ind_counts = analytics.bt_execution(contents, node_types=["https://www.w3id.org/iSeeOnto/BehaviourTree#ExplainerNode"])
    eval_counts = analytics.bt_exec_eval_question(contents)
    print(json.dumps(eval_counts))


if __name__ == "__main__":
    main()
