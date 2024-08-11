import json
import os


def get_dict(items: list):
    result = {}
    for index, item in enumerate(items, start=1):
        result[index] = item
    return result


def getInput(options: dict, prompt: str):
    s = ''
    promptstr = f'{s:-^40}\n|{prompt:^38}|\n{s:-^40}'
    print(promptstr)


def get_processes():
    for r, d, f in os.walk('input'):
        if r == 'input':
            # print(f"{d=}")
            return d


def getFiles(process):
    for _, _, files in os.walk(f'input\\{process}'):
        for file in files:
            yield (file)


def main():
    processes = get_processes()
    for process in processes:
        for file in getFiles(process):
            print(file)
    print(get_dict(processes))
    getInput(get_dict(processes), "test prompt")


if __name__ == "__main__":
    main()
