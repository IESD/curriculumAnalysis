import os, time, tkinter as tk
from tkinter import filedialog
from pathlib import Path
from extract import extractKeywords, extractProgrammes, extractModules


def extract():
    try:
        programmesPath = Path(stringVars[0].get()[12:])
        modulesPath = Path(stringVars[1].get()[9:])
        outputPath = Path(stringVars[2].get()[8:])
        keywordsPath = Path(stringVars[3].get()[10:])
        keywords = [kw for kw in extractKeywords(keywordsPath)]
        for file in os.scandir(programmesPath):
            if not file.name.endswith('txt'):
                continue
            for p in extractProgrammes(Path(file.path), outputPath, keywords):
                programmes.append(p)

        for file in os.scandir(modulesPath):
            if not file.name.endswith('txt'):
                continue
            for m in extractModules(Path(file.path), outputPath, keywords):
                modules.append(m)
        stringVars[4].set('Completed.')
    except FileNotFoundError:
        stringVars[4].set('FileNotFoundError.')
    except PermissionError:
        stringVars[4].set('PermissionError.')
    except AssertionError:
        stringVars[4].set('AssertionError.')
    window.update()
    time.sleep(1)
    stringVars[4].set('Ready.')


def browseDirectory(name, stringVar):
    directory = filedialog.askdirectory(initialdir='/', title=f'Select {name} Directory')
    stringVar.set(f'{name}: {directory}')


def browseFile(stringVar):
    filename = filedialog.askopenfilename(initialdir='/', title=f'Select Keywords File',
                                          filetypes=(('Text files', '*.txt'), ('all files', '*.*')))
    stringVar.set(f'Keywords: {filename}')


def createStringVar(string):
    stringVar = tk.StringVar()
    stringVar.set(string)
    stringVars.append(stringVar)


def createWindow():
    window = tk.Tk()
    window.title('File Explorer')
    # window.geometry("500x400")
    window.config(background="#D3D3D3")
    names = ['Programmes', 'Modules', 'Output']
    for name in names:
        createStringVar(f'Select {name} Directory')
        label = tk.Label(window, textvariable=stringVars[-1], width=50, height=3, fg='blue')
        button = tk.Button(window, text='BrowseDirectories',
                           command=lambda n=name, s=stringVars[-1]: browseDirectory(n, s))
        label.grid(column=1, row=names.index(name), columnspan=3, padx=10, pady=10)
        button.grid(column=4, row=names.index(name))
    createStringVar('Select Keywords File')
    keywordLabel = tk.Label(window, textvariable=stringVars[-1], width=50, height=3, fg="blue")
    keywordBtn = tk.Button(window, text="Browse Files", command=lambda s=stringVars[-1]: browseFile(s))
    keywordLabel.grid(column=1, row=4, columnspan=3, pady=10)
    keywordBtn.grid(column=4, row=4, sticky="w", padx=10)

    startBtn = tk.Button(window, text="Start", command=extract)
    startBtn.grid(column=2, row=5, sticky="e", padx=10, pady=40)
    createStringVar('Ready.')
    debugLabel = tk.Label(window, textvariable=stringVars[-1], width=20, fg="green", bg='#D3D3D3')
    debugLabel.grid(column=3, row=5, sticky="w", pady=40)
    return window


if __name__ == '__main__':
    stringVars = []
    programmes = modules = []
    window = createWindow()
    window.mainloop()
