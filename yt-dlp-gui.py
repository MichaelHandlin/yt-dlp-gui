import subprocess
import tkinter as tk
import os
import json
from pathlib import Path

class YtdlpGUI():
    objects = {}
    default_dir = ""
    default_param = ""
    current_dir = os.getcwd()

    def __init__(self) -> None:
        self.construct_gui()
        self.load_defaults()
        self.objects['master'].mainloop()

    def new_config_file(self):
        write = {
            "defaultDir": "",
            "defaultParam": ""
        }
        json_object = json.dumps(write, indent=4)
        f = open("config.json", 'w')
        f.write(json_object)
        f.close()

    def load_defaults(self):
        print("load called")
        #Check if config exists
        path = self.current_dir + "\\config.json"
        config = Path(path)
        if not config.exists():
            self.new_config_file()
        else:
            f = open(path, 'r')
            file = json.load(f)
            self.objects['odir_entry'].delete(0, "end")
            self.objects['odir_entry'].insert(0, file['defaultDir'])
            self.objects['param_entry'].delete(0, "end")
            self.objects['param_entry'].insert(0, file['defaultParam'])
            f.close()
        #Gather values

    def save_defaults(self):
        print("save called")
        config = {
            "defaultDir": self.objects['odir_entry'].get(),
            "defaultParam": self.objects['param_entry'].get()
        }
        path = self.current_dir + "\\config.json"
        json_object = json.dumps(config, indent=4)
        f = open("config.json", 'w')
        f.write(json_object)
        f.close()

    def construct_gui(self):
        #item Declarations
        master = tk.Tk()
        self.objects['master'] = master
        url_label = tk.Label(master, text="URL:")
        odir_label = tk.Label(master, text="Output Folder:")
        param_label = tk.Label(master, text="Parameters")

        url_entry = tk.Entry(master, width=50)
        self.objects['url_entry'] = url_entry
        odir_entry = tk.Entry(master, width=50)
        self.objects['odir_entry'] = odir_entry
        param_entry = tk.Entry(master, width=50)
        self.objects['param_entry'] = param_entry

        text = tk.Text(master, padx=2, pady=2, state="disabled", height=15)
        self.objects['text'] = text
        gobutton = tk.Button(master, text="Go", width=10, command=self.execute)
        savebutton = tk.Button(master, text="Save", width=10, command=self.save_defaults)
        resetbutton = tk.Button(master, text="Reset", width=10, command=self.load_defaults)

        #Grid Alignment
        url_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        url_entry.grid(row=0, column=1, sticky=tk.W, pady=2)
        resetbutton.grid(row=0, column=2, pady=2)
        odir_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        odir_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        savebutton.grid(row=1, column=2, pady=2)
        param_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        param_entry.grid(row=2, column=1, sticky=tk.W, pady=2)
        gobutton.grid(row=2, column=2, pady=2)
        text.grid(row=3, column=0, columnspan=3)

    def execute(self):
        self.output_progress()

    def output_progress(self):
        textbox = self.objects['text']
        textbox.configure(state='normal')
        textbox.delete(1.0, 'end')
        outfile = self.objects['odir_entry'].get() + "\\%(title)s.%(ext)s"
        url = self.objects['url_entry'].get()
        params = self.objects['param_entry'].get()
        params = params.split()
        command = ['yt-dlp']
        command = command + params
        command = command + ['-o', outfile]
        command.append(url)
        print(command)
        #process = subprocess.Popen(['ping', 'python.org'],
        process = subprocess.Popen(command, 
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
        while True:
            output = process.stdout.readline()
            outstr = ""
            if output != "":
                outstr = output.strip() + "\n"
            else:
                outstr = output.strip()
            textbox.insert('1.0', outstr)
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                #('RETURN CODE', return_code)
                # Process has finished, read rest of the output 
                for output in process.stdout.readlines():
                    #textbox.insert('1.0', output.strip())
                    print(output.strip())
                break
        textbox.configure(state='disabled')

if __name__ == "__main__":
    main = YtdlpGUI()