import json
import re
import time
import subprocess
import requests

import os


SPACING = 25


def frameToText(frame, color: bool):
    newFrm = []
    constr = ""

    for i in range(SPACING):
        constr += ' '

    pattern = re.compile(r'<span style="([^"]+)">(.+?)</span>', re.DOTALL)

    x = 0

    newLine = []
    preClr = (-1,-1,-1)

    for match in pattern.finditer(frame):
        x += 1
        rawClr = match.group(1)
        
        matchClr = re.search(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', rawClr)
        if not matchClr:
            continue
        r, g, b = map(int, matchClr.groups())

        c = match.group(0)[match.group(0).index(">")+1]

        if color:
            if preClr != (r,g,b):
                constr += f"\x1b[38;2;{r};{g};{b}m"
                preClr = (r,g,b)
        constr += c

        obj = {
            "c": c,
            "r": r,
            "g": g,
            "b": b
        }

        newLine.append(obj)

        #print(f'\x1b[38;2;{r};{g};{b}m', end="")
        #print(c, end="")
        if x == 50:
            x = 0
            newFrm.append(newLine)
            constr += '\n'
            for i in range(SPACING):
                constr += ' '
            newLine = []
            #print()

    newFrm.append(newLine)
    constr += '\n'

    return constr

def showAnimation(file):
    with open(file) as fp:
        frames = json.load(fp)

        for frame in frames:
            print('\x1bc'+frame)
            time.sleep(0.1)

def runProgram():
    print('\x1bc')
    link = input("Download link: ")
    name = input("Name: ")

    rawAsciiFile = f"tmp/{name}_tmp.json"
    outFileWColor = f"animations/{name}-color.json"
    outFileNoColor = f"animations/{name}.json"
    rawGifFile = f"tmp/{name}.gif"

    # Send a GET request to the server to fetch the file
    response = requests.get(link)

    if response.status_code != 200:
        print(f"Failed to download. Status: f{response.status_code}")
        return
    # Open a file (in binary mode) to write the content
    with open(rawGifFile, "wb") as file:
        file.write(response.content)

    print("File downloaded!")
    

    process = subprocess.Popen(f"./image-to-ascii -w 50 -a symbols.txt {rawGifFile} -o {rawAsciiFile}", shell=True)
    process.wait()

    with open(rawAsciiFile) as fp:
        raw = json.load(fp)

        clrFrames = []
        noClrFrames = []

        for frame in raw:
            noColor = frameToText(frame, False)
            withColor = frameToText(frame, True)
            clrFrames.append(withColor)
            noClrFrames.append(noColor)

        with open(outFileWColor, "w", encoding="utf-8") as fp:
            json.dump(clrFrames, fp)
        
        with open(outFileNoColor, "w", encoding="utf-8") as fp:
            json.dump(noClrFrames, fp)
    
    print("Cleanup")
    os.remove(rawGifFile)
    os.remove(rawAsciiFile)

    if input("Want to display once (Y/N): ").lower() == "y":
        showAnimation(outFileWColor)
        showAnimation(outFileNoColor)


while True:
    runProgram()