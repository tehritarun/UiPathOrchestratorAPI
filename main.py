import json
import os
from spinner import CLI_Spinner
import time
import orchestratorApi
import subprocess


def get_dict(items: list):
    result = {}
    for index, item in enumerate(items, start=1):
        result[str(index)] = item
    return result


def getInput(options: dict, prompt: str, page: int):
    s = ""
    subprocess.run("clear")
    promptstr = f"{s:-^40}\n|{prompt:^38}|\n{s:-^40}"
    print(promptstr)
    for key, option in options.items():
        print(f"{key}. {option}")
    if page == 2:
        print("a. add all items")
        print("b. back")
    print("q. quit")
    print(f"{s:-^40}")
    return input("Select a Option: ")


def get_processes():
    for r, d, f in os.walk("input"):
        if r == "input":
            return d


def getFiles(process):
    for _, _, files in os.walk(os.path.join("input", process)):
        for file in files:
            if not file.lower().endswith(".json"):
                continue
            filename = os.path.join("input", process, file)

            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                process(e)
                continue
            payloaddata = {"itemData": {
                "Name": process,
                "Reference": file.upper().replace(".JSON", "").strip(),
                "SpecificContent": data,
                "Priority": "Normal",
            }}
            yield ((file, payloaddata))


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


def handle_input(choice: str, data: dict):
    validinput = True
    selections = []
    if choice.lower().strip() == "a":
        choice = ",".join(data.keys())
    for c in choice.split(","):
        if c.isnumeric() and c in data.keys():
            selections.append(data[c])
        else:
            validinput = False
    if validinput:
        return selections
    elif choice.lower().strip() == "q":
        quit()
    elif choice.lower().strip() == "b":
        return "back"
    else:
        return "invalid input"


def main():
    folderId = select_folder()
    processdata, filedata, transationdata = load_data()
    page = 1
    message = "Select a process/queue"
    while True:
        if page == 1:
            processChoice = getInput(processdata, message, page)
            if processChoice in processdata.keys():
                processChoice = processdata[processChoice]
                page = 2
                message = "Select Transaction"
            elif processChoice.lower().strip() == "q":
                quit()
            else:
                message = "Invalid input"
        elif page == 2:
            choice = getInput(filedata[processChoice], message, page)
            # choice = filedata[processChoice][choice]
            selections = handle_input(choice, filedata[processChoice])
            if type(selections) is list:
                spinner = CLI_Spinner("Adding Transaction to queue", speed=0.1)
                spinner.start()
                for selection in selections:
                    payloadstr = json.dumps(transationdata[selection])
                    orchestratorApi.add_transaction(payloadstr, folderId)
                    time.sleep(2)
                spinner.stop()
            elif selections == "back":
                page = 1
            else:
                message = selections


def select_folder():
    folders = orchestratorApi.get_folders()
    foldernames = {}
    folderIds = {}
    for index, folder in enumerate(folders, start=1):
        foldernames[str(index)] = folder['DisplayName']
        folderIds[folder['DisplayName']] = folder['Id']
    folderchoice = getInput(foldernames, "Select Folder", 0)
    if folderchoice in foldernames.keys():
        return str(folderIds[foldernames[folderchoice]])
    else:
        print("invalid input. please try again")
        exit(1)


if __name__ == "__main__":
    main()
