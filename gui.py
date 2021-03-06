import json
import os
import tkinter as tk
from json.decoder import JSONDecodeError
from tkinter import filedialog, messagebox

from PIL import ImageTk, Image

root = tk.Tk()
root.title("Haddock json editor")
root.geometry("500x500")

try:
    root.iconphoto(False, tk.PhotoImage(file='HADDOCK-logo-small.png'))
except:
    pass

class superparent:

    def __init__(self, master):
        """initialize and ask for json file"""
        self.myFrame = tk.Frame(master)
        self.myFrame.place(width=500, height=500)
        self.seconds = 0
        self.changes = []
        self.old_data = []
        self.new_data = []
        self.mbox = tk.messagebox
        self.molecule_image = ImageTk.PhotoImage(Image.open("molecule100.jpg"))
        self.molecule_image_small = ImageTk.PhotoImage(Image.open("molecule25.jpg"))
        self.haddock_image = ImageTk.PhotoImage(Image.open("HADDOCK-logo.png"))


        tk.Button(self.myFrame, text="Click me and and then select a Json file", relief="groove",
                  command=lambda: [self.load_json(), self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.2, relwidth=1, relx=0, rely=0)
        tk.Button(self.myFrame, text="Click me for help", relief="groove",
                  command=lambda: [self.faq()]) \
            .place(relheight=0.2, relwidth=1, relx=0, rely=0.2)
        tk.Label(self.myFrame, image=self.haddock_image).place(relheight=0.4, relwidth=1, relx=0, rely=0.5)

        self.faq()




    def load_json(self):
        """load json into memory"""
        file = tk.filedialog.askopenfile("r", filetypes=[('Json files', '*.json')])
        if not file:
            self.mbox.showinfo(message="I need a json file, exiting")
            exit()
        else:
            try:
                self.name = os.path.basename(file.name)
                self.contents = json.load(file)
                file.close()
            except JSONDecodeError:
                self.mbox.showinfo(message="something is wrong with this file,\
                I cannot load it. Maybe it's empty?")
                self.load_json()

    def helpmessage(self):
        return """Greetings, Here is a quick step by step of how to use this program.\n\nClick the button that says Click me and select a json file.\nClick on the molecule that you want to insert your pdb into.\nClick replace pdb.\nSelect the PDB file you wish to insert\nTo make your changes permanent, click save your edited json file as a new file in the bottom right.\nYour new file will have the updated pdb
        """

    def faq(self):
        self.mbox.showinfo(message=self.helpmessage())

    def clear_window(self):
        """clear the screen so you can create new objects on it"""
        for items in self.myFrame.winfo_children():
            items.destroy()

    def molecule_window(self):
        """display molecule buttons"""
        self.show_options()
        if len(self.contents["partners"]) > 5:
            molecule_button_image = self.molecule_image_small
        else:
            molecule_button_image = self.molecule_image
        x = 0
        for item in self.contents["partners"]:
            tk.Button(self.myFrame, wraplength=130, text=" Molecule " + item + " options",
                      image=molecule_button_image, compound=tk.LEFT, justify=tk.RIGHT, relief="groove",
                      command=lambda item=item: [self.clear_window(), self.molecule_stats(item)]) \
                .place(relheight=1 / len(self.contents["partners"]), relwidth=0.5, relx=0, rely=0 + x)
            x += 1 / len(self.contents["partners"])

    def show_options(self):
        """display option buttons"""
        x = 0
        for item in self.contents:
            if "tblfile" in item:
                tk.Button(self.myFrame, text=f"Click me for options on {item}", relief="groove",
                          command=lambda item=item: [self.clear_window(), self.table_stats(item)]) \
                    .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0 + x)
                x += 0.1

        tk.Button(self.myFrame, text="Click me if you want help text", relief="groove",
                  command=lambda: [self.faq()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.3)
        tk.Button(self.myFrame, text="Click me to see a list of changes made", relief="groove",
                  command=lambda: [self.clear_window(), self.logging()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.4)

        tk.Button(self.myFrame, text="Click me to save your json file", relief="groove",
                  command=lambda: [self.save_json()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.7)
        tk.Button(self.myFrame, text="Click me to load in a new json file", relief="groove",
                  command=lambda: [self.load_json(), self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.8)

    def save_json(self):
        """save json file to disk"""
        files = [('Json Document', '*.json')]
        save_json = tk.filedialog.asksaveasfile(filetypes=files, defaultextension=files)
        if not save_json:
            return
        json.dump(self.contents, save_json, indent=4)
        self.changes.append(f"Json {self.name} saved to disk")
        save_json.close()
        json_update = f"The json file {self.name} file has been updated"
        self.changes.append(json_update)
        self.mbox.showinfo(message="Json succesfully saved")

    def save_table(self, item):
        """save table file to disk"""
        files = [('Text Document', '*.txt')]
        save_table = tk.filedialog.asksaveasfile(filetypes=files, defaultextension=files)
        if not save_table:
            return
        save_table.write(self.contents[item])
        self.changes.append(f"table file of {item} from {self.name} saved to disk")
        save_table.close()
        self.mbox.showinfo(message="Table succesfully saved to disk")

    def replace_table(self, item):
        """replace table from disk"""
        table_file = tk.filedialog.askopenfile("r")
        if not table_file:
            return
        if table_file.name.endswith(".txt"):
            table_update = f"table {item} in the {self.name} file has been updated"
            self.changes.append(table_update)
            self.contents[item] = table_file.read()
            table_file.close()
            self.mbox.showinfo(message="table succesfully replaced")
        else:
            return

    def save_pdb(self, item):
        """save pdb to disk"""

        files = [('PDB Document', '*.pdb')]
        pdb_file = tk.filedialog.asksaveasfile(filetypes=files, defaultextension=files)
        if not pdb_file:
            return
        pdb_file.write(self.contents['partners'][item]['raw_pdb'])
        self.changes.append(f"PDB of molecule {item} in the {self.name} file has been updated")
        pdb_file.close()
        self.mbox.showinfo(message="pdb succesfully saved to disk")






    def replace_pdb(self, index):
        """replace pdb in molecule"""
        pdb_file = tk.filedialog.askopenfile("r")
        if not pdb_file:
            return
        if pdb_file.name.endswith(".pdb"):
            pdb_update = f"PDB of molecule {index} in the {self.name} file has been updated"
            self.changes.append(pdb_update)
            self.contents['partners'][index]['raw_pdb'] = pdb_file.read()
            pdb_file.close()
            self.mbox.showinfo(message="pdb succesfully replaced")
            self.clear_window()
            self.molecule_window()
        else:
            return

    def save_active_residue_list(self, index, entry):
        """save active residue"""
        # weird_user_input_handler
        try:
            json.loads(entry)
        except:
            self.mbox.showinfo(message="Something is wrong with the input, maybe you forgot a bracket or put a letter in or something")
            return
        else:
            residue_update = f"Active residue list of molecule {index} in the {self.name} file has been updated"
            self.changes.append(residue_update)
            self.contents['partners'][index]['activereslist'] = json.loads(entry)
            self.mbox.showinfo(message="residue_list succesfully replaced")
            self.clear_window()
            self.molecule_window()




    def save_passive_residue_list(self, index, entry):
        """save passive residue"""
        #weird_user_input_handler
        try:
            json.loads(entry)
        except:
            self.mbox.showinfo(message="Something is wrong with the input, maybe you forgot a bracket or put a letter in or something")
            return
        else:
            residue_update = f"Passive residue list of molecule {index} in the {self.name} file has been updated"
            self.changes.append(residue_update)
            self.contents['partners'][index]['passivereslist'] = json.loads(entry)
            self.mbox.showinfo(message="residue_list succesfully replaced")
            self.clear_window()
            self.molecule_window()



    def edit_active_residue(self, index):
        """change active residue"""

        tk.Label(self.myFrame, text="Active res list, use the box below for editing") \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0)
        e = tk.Entry(self.myFrame)
        entry = str(self.contents['partners'][index]['activereslist'])
        e.insert(tk.END, f"{entry}")
        e.place(relheight=0.1, relwidth=1, relx=0, rely=0.1)
        tk.Button(self.myFrame, text="Save current input", relief="groove",
                  command=lambda: [self.save_active_residue_list(index, e.get())]) \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0.2)
        tk.Button(self.myFrame, text="Click me to go back to molecule selection", relief="groove",
                  command=lambda: [self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0.9)
        tk.Label(self.myFrame, text=f"Format in these files is really importand, and mistakes are easely made here.\nWhat is currently located in your active/passive reslist is already displayed.\nThe format is square brackets as casing for the numbers which are seperated by a comma.\nFor multiple lists structure wrap square brackets and seperate them with a comma\n\nThis means you can turn example input [1,2,3,4,5,6,7] \n \n Into: \n ----- Single list: [3675756,3,4,56,76,2] \n ----- Multiple lists in list: [[1,2,3,4,654654645,3],[1,1,234,343],[1,4545,4]] \nSeperate the individual lists with a comma and wrap them in brackets\n\nThis means if you have a modified list already-\nYou can just copy paste it in and press save and done", justify="left") \
            .place(relheight=0.6, relwidth=1, relx=0, rely=0.3)

    def edit_passive_residue(self, index):
        """change passive residue"""
        tk.Label(self.myFrame,
                 text="Passive res list, use the box below for editing") \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0)
        e = tk.Entry(self.myFrame)
        entry = self.contents['partners'][index]['passivereslist']
        e.insert(tk.END, f"{entry}")
        e.place(relheight=0.1, relwidth=1, relx=0, rely=0.1)
        tk.Button(self.myFrame, text="Save current input", relief="groove",
                  command=lambda: [self.save_passive_residue_list(index, e.get())]) \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0.2)
        tk.Button(self.myFrame, text="Click me to go back to molecule selection", relief="groove",
                  command=lambda: [self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0.9)
        tk.Label(self.myFrame,
                 text=f"Format in these files is really importand, and mistakes are easely made here.\nWhat is currently located in your active/passive reslist is already displayed.\nThe format is square brackets as casing for the numbers which are seperated by a comma.\nFor multiple lists structure wrap square brackets and seperate them with a comma\n\nThis means you can turn example input [1,2,3,4,5,6,7] \n \n Into: \n ----- Single list: [3675756,3,4,56,76,2] \n ----- Multiple lists in list: [[1,2,3,4,654654645,3],[1,1,234,343],[1,4545,4]] \nSeperate the individual lists with a comma and wrap them in brackets\n\nThis means if you have a modified list already-\nYou can just copy paste it in and press save and done",
                 justify="left") \
            .place(relheight=0.6, relwidth=1, relx=0, rely=0.3)

    def table_stats(self, item):
        """list table options"""
        tk.Label(self.myFrame, text=f"{item}").place(relheight=0.1, relwidth=0.5, relx=0, rely=0)
        tk.Label(self.myFrame, text=f"{item}").place(relheight=0.1, relwidth=0.5, relx=0, rely=0.1)
        tk.Button(self.myFrame, text="save this file to disk", relief="groove",
                  command=lambda: [self.save_table(item)]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0)
        tk.Button(self.myFrame, text="replace with another table", relief="groove",
                  command=lambda: [self.replace_table(item)]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.1)
        tk.Button(self.myFrame, text="Click me to go back to molecule selection", relief="groove",
                  command=lambda: [self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.9)

    def molecule_stats(self, item):
        """list molecule options"""
        tk.Label(self.myFrame, text=f"PDB of molecule {item}").place(relheight=0.1, relwidth=0.5, relx=0, rely=0)
        tk.Button(self.myFrame, text="save PDB as a seperate .pdb file", relief="groove",
                  command=lambda: [self.save_pdb(item)]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0)
        tk.Button(self.myFrame, text="replace PDB", relief="groove",
                  command=lambda: [self.clear_window(), self.replace_pdb(item)]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.1)
        tk.Label(self.myFrame, text="Active res").place(relheight=0.1, relwidth=0.5, relx=0, rely=0.2)
        tk.Button(self.myFrame, text="edit Active res", relief="groove",
                  command=lambda: [self.clear_window(), self.edit_active_residue(item)]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.2)
        tk.Label(self.myFrame, text="Passive res").place(relheight=0.1, relwidth=0.5, relx=0, rely=0.3)
        tk.Button(self.myFrame, text="edit Passive res", relief="groove",
                  command=lambda: [self.clear_window(), self.edit_passive_residue(item)]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.3)
        tk.Button(self.myFrame, text="Click me to go back to molecule selection", relief="groove",
                  command=lambda: [self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.9)

    def save_logfile(self):
        """save logfile to disk"""
        files = [('Text Document', '*.txt')]
        log_file = tk.filedialog.asksaveasfile(filetypes=files, defaultextension=files)
        if not log_file:
            return
        log_file.write("\n".join(self.changes))
        log_file.close()
        self.mbox.showinfo(message="Logfile succesfully saved to disk")



    def logging(self):
        """overview of changes made"""
        tk.Button(self.myFrame, text="Click me to go back to molecule selection", relief="groove",
                  command=lambda: [self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.9)
        tk.Button(self.myFrame, text="Click me to save this list to disk", relief="groove",
                  command=lambda: [self.clear_window(), self.save_logfile()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0, rely=0.9)
        x = 0
        for item in self.changes:
            tk.Label(self.myFrame, text=f"{item}").place(relheight=0.1, relwidth=1, relx=0, rely=0 + x)
            x += 0.1



if __name__ == "__main__":
    e = superparent(root)
    root.mainloop()
