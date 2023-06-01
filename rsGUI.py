import tkinter as tk
from tkinter.ttk import *
import myvariant
from pandastable import Table

class TableWindow(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)

         #NEW WINDOW POSITON
        w = 1200 # width for the Tk root
        h = 600 # height for the Tk root
        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.title("Results")

        self.parent = parent
        # icon
        #icon = tk.PhotoImage(file="icon.png")
        #self.iconphoto(True, icon)
        self.table = Table(self, dataframe=data, showstatusbar=True, showtoolbar=True)
        self.table.show()
        self.protocol("WM_DELETE_WINDOW", self.destroy_window)

    def destroy_window(self,):
        print("ENTERED CLOSING STATE")
        self.parent.text_box["state"] = tk.NORMAL
        self.parent.btn["state"] = tk.NORMAL
        self.parent.hg19_button["state"] = tk.NORMAL
        self.parent.hg38_button["state"] = tk.NORMAL
        self.parent.label_info_text.set("Enter rsIDs")
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("rsGUI")

        #NEW WINDOW POSITON
        w = 400 # width for the Tk root
        h = 300 # height for the Tk root
        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.label = tk.Label(self, text="Enter one rs number per line")
        self.label.pack()

        # a button widget which will
        # open a new window on button click
        self.btn = Button(self,
                    text ="Search",
                    command= lambda: self.get_text_content())
        
        # Create a Text widget
        self.text_box = tk.Text(self)
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar widget
        self.scrollbar = tk.Scrollbar(self.text_box)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Attach the Scrollbar to the Text widget
        self.text_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_box.yview)

        # icon
        # icon
        #icon = tk.PhotoImage(file="icon.png")
        #self.iconphoto(True, icon)

        
        # Following line will bind click event
        # On any click left / right button
        # of mouse a new window will be opened
        # self.btn.bind("<Button>",
        #         lambda e: get_text_content(self))
        self.btn.pack(pady = 10)

        # label under the button
        self.label_info_text = tk.StringVar()
        self.label_info_text.set("Enter rsIDs")
        self.label_info = tk.Label(self, textvariable = self.label_info_text)
        self.label_info.pack() 

        # assembly Checkbutton 
        self.hg19_value = tk.IntVar()
        self.hg19_button = tk.Checkbutton ( self, text = "hg19" , justify = tk.LEFT, variable = self.hg19_value, command = self.select_hg19)
        self.hg19_button.select()
        self.hg19_button.pack()
        self.hg38_value = tk.IntVar()
        self.hg38_button = tk.Checkbutton ( self, text = "hg38", justify = tk.LEFT, variable= self.hg38_value, command = self.select_hg38)
        self.hg38_button.pack()

    def select_hg19(self):
        self.hg19_value.set(1) 
        self.hg38_value.set(0)
    def select_hg38(self):
        self.hg19_value.set(0) 
        self.hg38_value.set(1)
    
    def get_text_content(self):
        # GET CONTENT OF TEXT BOX
        content = self.text_box.get("1.0", tk.END)
        content = content.strip()
        print(content)
        if content == "":
            self.label_info_text.set("Please enter at\nleast one rsID")
        else:
            # PROCESS STUFF
            self.label_info_text.set("Processing rsIDs...")
            mv = myvariant.MyVariantInfo()
            all_rsids = content.split("\n")
            if self.hg19_value.get() == 1:
                assembly = "hg19"
            elif self.hg38_value.get() == 1:
                assembly = "hg38"
            else:
                print("PICNIC")
            print(assembly)
            res = mv.querymany(all_rsids, scopes='dbsnp.rsid', fields='all', as_dataframe=True, assembly=assembly)
            res.insert(0, "rsID" ,res.index)
            print(res)
            # LAUNCH NEW WINDOW
            # DISABLE MAIN WINDOW STUFF
            self.text_box["state"] = tk.DISABLED
            self.btn["state"] = tk.DISABLED
            self.hg19_button["state"] = tk.DISABLED
            self.hg38_button["state"] = tk.DISABLED
            self.label_info_text.set("Check other window for results")
            self.resultWindow = TableWindow(self, res)

if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()
