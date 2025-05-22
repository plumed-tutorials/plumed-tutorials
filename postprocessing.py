# formatted and checked with ruff v0.11
import yaml


def listTodict(input: list):
    output = {}
    for i in input:
        output[i["name"]] = int(i["number"])
    return output


def dictToList(input: dict):
    output = []
    for k in input.keys():
        output.append({"name": k, "number": input[k]})
    return output


def actionCount(nreplicas: int):
    with open("_data/actioncount0.yml", "r") as f:
        actionCounts = listTodict(yaml.load(f, Loader=yaml.BaseLoader))
    total = sum(actionCounts.values())

    for i in range(1, nreplicas):
        with open(f"_data/actioncount{i}.yml", "r") as f:
            actionCounts_i = listTodict(yaml.load(f, Loader=yaml.BaseLoader))
            total += sum(actionCounts_i.values())
            assert actionCounts_i.keys() == actionCounts.keys()
            for k in actionCounts.keys():
                actionCounts[k] += actionCounts_i[k]

    assert total == sum(actionCounts.values())

    with open("_data/actioncount_sum.yml", "w") as f:
        yaml.dump(dictToList(actionCounts), f)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        prog="postprocessing",
        description="""
%(prog)s will prepare some of the files required for the site to work.
""",
    )
    parser.add_argument(
        "-r", "--nreplicas", help="the number of replicas", type=int, required=True
    )
    args = parser.parse_args()
    actionCount(args.nreplicas)
