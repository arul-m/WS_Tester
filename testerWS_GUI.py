#!/usr/bin/python
import tkinter as tk
from tkinter import filedialog
import subprocess, sys
import WSTester as tester


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.configure(borderwidth='2', relief='groove', width='500', height='150')

    def create_widgets(self):
        self.load_firmwarefile = tk.Button(self, text="LOAD FIRMWARE", command=self.openfirmwarefile, fg="blue",
                                           bg="white", width=50)
        self.load_firmwarefile.pack(side="top")

        self.label_variable = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.label_variable, anchor="w", fg="white", bg="red", justify='left')
        self.label.pack()
        self.label_variable.set(u"LOAD FIRMWARE FILE!")

        self.flash_test = tk.Button(self, text="TEST & PROGRAM", state="disabled", command=self.test, fg="green",
                                    bg="white", width=50)
        self.flash_test.pack()

        self.flash_production = tk.Button(self, text="PROGRAM", state="disabled", command=self.flashproduction,
                                          fg="purple",
                                          bg="white",
                                          width=50)
        self.flash_production.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy, width=50)
        self.quit.pack()

        self.textwindow = tk.Text(self, wrap='word')
        self.textwindow.pack(side='bottom', fill='both', expand=True)
        self.textwindow.tag_configure("stderr", foreground="#b22222")

        sys.stdout = TextRedirector(self.textwindow, "stdout")
        sys.stderr = TextRedirector(self.textwindow, "stderr")

    def openfirmwarefile(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("elf files", "*.elf"), ("elf files", "")))
        if self.filename:
            self.label_variable.set(self.filename)
            self.label.configure(bg="green")
            self.flash_production.configure(state="active")
            self.flash_test.configure(state="active")
        else:
            self.load_firmwarefile.flash()

    def test(self):

        command_line = ['START',
                        'C:/Program Files (x86)/Atmel/Studio/7.0/Extensions/Application/StudioCommandPrompt.exe',
                        'atprogram', '-v', '-t', 'atmelice', '-i', 'isp', '-d', 'atmega328pb', 'chiperase',
                        'program', '-f', "test.elf"]
        with subprocess.Popen(command_line, bufsize=-1, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) as cli:
            print(cli.stderr.readline())
            print(cli.stdout.readline())
            cli.wait()
            cli.kill()
        # Run test
        tester.ws_test()
        # Program with the Application Firmware
        self.flashproduction()
        # Confirm the loaded application firmware is working
        tester.ws_testerapp()

    def flashproduction(self):
        self.textwindow.delete(index1="1.0", index2="end")
        command_line = ['START',
                        'C:/Program Files (x86)/Atmel/Studio/7.0/Extensions/Application/StudioCommandPrompt.exe',
                        'atprogram', '-v', '-t', 'atmelice', '-i', 'isp', '-d', 'atmega328pb',
                        'chiperase',
                        'program', '-f', self.filename]
        with subprocess.Popen(command_line, bufsize=-1, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) as cli:
            print(cli.stderr.readline())
            print(cli.stdout.readline())

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        #self.widget.configure(state="disabled")


# create the application
root = tk.Tk()
app = Application(master=root)

#
# here are method calls to the window manager class
#
app.master.title("Whitesands Test and Flash firmware Application")
app.master.minsize(500, 150)
app.master.maxsize(1000, 400)
app.master.resizable(False, False)
app.master.attributes('-topmost', True)
app.mainloop()
