import json
import os
from spinner import CLI_Spinner
import time


def get_dict(items: list):
    result = {}
    for index, item in enumerate(items, start=1):
        result[str(index)] = item
    return result


def getInput(options: dict, prompt: str):
    s = ""
    os.system('cls')
    promptstr = f"{s:-^40}\n|{prompt:^38}|\n{s:-^40}"
    print(promptstr)
    for key, option in options.items():
        print(f"{key}. {option}")
    print(f"{s:-^40}")
    return input("Select a Option: ")


def get_processes():
    for r, d, f in os.walk("input"):
        if r == "input":
            return d


def getFiles(process):
    for _, _, files in os.walk(f"input\\{process}"):
        for file in files:
            with open(f"input\\{process}\\{file}") as f:
                data = json.load(f)
                yield ((file, data))


def load_data():
    processes = get_processes()
    filedata = {}
    transactiondata = {}
    for process in processes:
        processfiles = []
        for file in getFiles(process):
            processfiles.append(file[0])
            transactiondata[file[0]] = file[1]
        filedata[process] = get_dict(processfiles)
    return (get_dict(processes), filedata, transactiondata)


def main():
    processdata, filedata, transationdata = load_data()
    print(transationdata)
    page = 1
    while True:
        if page == 1:
            processChoice = getInput(processdata, "Select a process")
            processChoice = processdata[processChoice]
            page = 2
        elif page == 2:
            choice = getInput(filedata[processChoice], "Select Transacrion")
            choice = filedata[processChoice][choice]
            # TODO: implement multiple selecction here
            # TODO: implement special options here
            print(transationdata[choice])
            spinner = CLI_Spinner("Adding Transactio to queue", speed=0.1)
            spinner.start()
            time.sleep(5)
            # TODO: implement orchestrator functions here
            spinner.stop()


if __name__ == "__main__":
    main()
