import json
import os
import tkinter as tk
from json.decoder import JSONDecodeError
from tkinter import filedialog, messagebox

from PIL import ImageTk, Image

root = tk.Tk()
root.title("Haddock gui")
root.geometry("500x500")
root.iconphoto(False, tk.PhotoImage(file='HADDOCK-logo.png'))


class superparent:

    def __init__(self, master):
        """initialize and ask for json file"""
        self.myFrame = tk.Frame(master)
        self.myFrame.place(width=500, height=500)
        self.molecule_image = ImageTk.PhotoImage(Image.open("molecule100.jpg"))
        self.molecule_image_small = ImageTk.PhotoImage(Image.open("molecule25.jpg"))
        self.seconds = 0
        self.changes = []
        self.old_data = []
        self.new_data = []
        self.mbox = tk.messagebox
        tk.Button(self.myFrame, text="Click me and and then select a Json file", relief="groove",
                  command=lambda: [self.load_json(), self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.2, relwidth=1, relx=0, rely=0)
        tk.Button(self.myFrame, text="Click me for help", relief="groove",
                  command=lambda: [self.faq()]) \
            .place(relheight=0.2, relwidth=1, relx=0, rely=0.2)
        self.faq()
        self.protoshape = {"activereslist": '[]',
                           "auto_passive": 'true',
                           "auto_passive_radius": 6.5,
                           "cg": 'false',
                           "chain": "All",
                           "charged_cter": 'false',
                           "charged_nter": 'false',
                           "cyclic": 'false',
                           "dna": 'false',
                           "fix_origin": 'false',
                           "fully_flex": '{}',
                           "his_patch": '{}',
                           "link_file": "protein-allhdg5-4-noter.link",
                           "moleculetype": "",
                           "par_file": "protein-allhdg5-4.param",
                           "partnerlist": '[]',
                           "passivereslist": '[]',
                           'raw_pdb': '',
                           "pdb_file": "protein1.pdb",
                           "psf_file": "protein1.psf",
                           "root": "protein1",
                           "semi_flex": '{}',
                           "segid": "A",
                           "shape": 'false',
                           "top_file": "protein-allhdg5-4.top"

                           }

    def load_json(self):
        """load json into memory"""
        file = tk.filedialog.askopenfile("r", filetypes=[('Json files', '*.json')])
        if not file:
            self.mbox.showinfo(message="I need a json file")
            if not hasattr(self, "contents"):
                self.mbox.showinfo(message="Sorry I really need a json file to begin working,\
                please run the program again and select one. exiting.")
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
        return """Greetings, Here is an explanation of how to use this program.\n\nClicking the button will open up a file browser, use this to navigate to where you downloaded your json file from the haddock website, and select that json file.\n\nThe gui will list all the molecules in the json on the left side, click on these picture for options on how to edit them.\n\nOn the right you will have various options\n\nYou can export/insert the table(s) to/from a seperate txt file\nYou can show this text again with the help text button\nYou can click to see a list of changes you have made incase you forgot which part of which molecule you edited\nYou can implement a new molecule, this will ask you for a pdb file. select your choice and a new molecule will be added\nyou can delete a molecule incase you uploaded a new molecule with the wrong file\nyou can save your edited json as a new file, just type in the name. The json file extension is added automaticly\nyou can switch to a different json file without needing to reboot the program, don't forget to save your previous json.\n\nWhen you click on a molecule you will be taken to the option screen of your selected choice.\n\nYou can save the pdb of the molecule as a seperate pdb file by clicking on the save pdb button.\nyou can switch the current pdb with a pdb on your hard drive by clicking the replace pdb button.\nYou can edit the active residue of the molecule by clicking the edit active residue button.\nIn the active residue editing screen, simply copy paste your active residue list in the white box.\nIt should look something like this: 50,23,23,12\nClick the save button when you are done.\nIn the passive residue editing screen, simply copy paste your passive residue list in the white box.\nIt should look something like this: 50,23,23,12\nClick the save button when you are done
        
        """

    def faq(self):
        self.mbox.showinfo(message=self.helpmessage())

    def clear_window(self):
        """clear the screen so you can create new objects on it"""
        for items in self.myFrame.winfo_children():
            items.destroy()

    def molecule_window(self):
        """display molecule buttons"""
        self.show_tables()
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

    def show_tables(self):
        """display table buttons"""
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
        tk.Button(self.myFrame, text="Click me to implement a new molecule", relief="groove",
                  command=lambda: [self.clear_window(), self.choose_molecule_type()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.5)
        tk.Button(self.myFrame, text="Click me to delete a molecule", relief="groove",
                  command=lambda: [self.clear_window(), self.delete_molecule_window()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.6)
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
        else:
            return

    def save_active_residue_list(self, index, entry):
        """save active residue"""
        residue_update = f"Active residue list of molecule {index} in the {self.name} file has been updated"
        self.changes.append(residue_update)
        if "[" and "]" not in entry:
            entry = "[" + entry + "]"
        self.contents['partners'][index]['activereslist'] = entry
        self.mbox.showinfo(message="residue_list succesfully replaced")
        self.clear_window()
        self.molecule_window()

    def save_passive_residue_list(self, index, entry):
        """save passive residue"""
        residue_update = f"Passive residue list of molecule {index} in the {self.name} file has been updated"
        self.changes.append(residue_update)
        if "[" and "]" not in entry:
            entry = "[" + entry + "]"
        self.contents['partners'][index]['passivereslist'] = entry
        self.mbox.showinfo(message="residue_list succesfully replaced")
        self.clear_window()
        self.molecule_window()

    def edit_active_residue(self, index):
        """change active residue"""
        tk.Label(self.myFrame, text="Active res list, use the box below for editing") \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0)
        e = tk.Entry(self.myFrame)
        monkeyproof = str(self.contents['partners'][index]['activereslist'])[1:-1]
        e.insert(tk.END, f"{monkeyproof}")
        e.place(relheight=0.1, relwidth=1, relx=0, rely=0.1)
        tk.Button(self.myFrame, text="Save current input", relief="groove",
                  command=lambda: [self.save_active_residue_list(index, e.get())]) \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0.2)
        tk.Button(self.myFrame, text="Click me to go back to molecule selection", relief="groove",
                  command=lambda: [self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0.9)

    def edit_passive_residue(self, index):
        """change passive residue"""
        tk.Label(self.myFrame,
                 text="Passive res list, use the box below for editing") \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0)
        e = tk.Entry(self.myFrame)
        monkeyproof = str(self.contents['partners'][index]['passivereslist'])[1:-1]
        e.insert(tk.END, f"{monkeyproof}")
        e.place(relheight=0.1, relwidth=1, relx=0, rely=0.1)
        tk.Button(self.myFrame, text="Save current input", relief="groove",
                  command=lambda: [self.save_passive_residue_list(index, e.get())]) \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0.2)
        tk.Button(self.myFrame, text="Click me to go back to molecule selection", relief="groove",
                  command=lambda: [self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.1, relwidth=1, relx=0, rely=0.9)

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
        # tk.Button(self.myFrame, text="save json",
        #          command=lambda: [self.save_json()]) \
        #    .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.6)
        # tk.Button(self.myFrame, text="new json",
        #          command=lambda: [self.load_json()]) \
        #    .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.7)
        # tk.Button(self.myFrame, text="Click to see changes",
        #          command=lambda: [self.clear_window(), self.logging()]) \
        #    .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.8)

    def molecule_stats(self, item):
        """list molecule options"""
        tk.Label(self.myFrame, text=f"PDB of molecule {item}").place(relheight=0.1, relwidth=0.5, relx=0, rely=0)
        tk.Button(self.myFrame, text="save PDB as a seperate .pdb file", relief="groove",
                  command=lambda: [self.save_pdb(item)]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0)
        tk.Button(self.myFrame, text="replace PDB", relief="groove",
                  command=lambda: [self.replace_pdb(item)]) \
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
        # tk.Button(self.myFrame, text="save json",
        #          command=lambda: [self.save_json()]) \
        #    .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.6)
        # tk.Button(self.myFrame, text="new json",
        #          command=lambda: [self.load_json()]) \
        #    .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.7)
        # tk.Button(self.myFrame, text="Click to see changes",
        #          command=lambda: [self.clear_window(), self.logging()]) \
        #    .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.8)

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
    def choose_molecule_type(self):
        self.moleculetypes = ['Protein', 'Ligand', 'Peptide', 'Glycan', 'Nucleic', 'Shape', 'Dummy']


        tk.Button(self.myFrame, text="Click me to go back to molecule selection", relief="groove",
                  command=lambda: [self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.9)

        for index, item in enumerate(self.moleculetypes):
            tk.Button(self.myFrame, wraplength=150, text="Type of molecule: " + item,
                      compound=tk.LEFT, justify=tk.RIGHT, relief="groove",
                      command=lambda item=item: [self.clear_window(), self.new_molecule(item), self.molecule_window()]) \
                .place(relheight=1 / len(self.moleculetypes), relwidth=0.5, relx=0, rely=0+(0.1*index))


    def new_molecule(self, item):
        """modify the template and insert new molecule"""

        if item == "Shape":
            print("Shape modified")
            self.protoshape['top_file'] = "shape.top"
            self.protoshape['link_file'] = "shape.link"
            self.protoshape['par_file'] = "shape.param"

        if item == "Nucleic":
            self.protoshape['top_file'] = "dna-rna-allatom-hj-opls-1.3.top"
            self.protoshape['link_file'] = "dna-rna-1.3.link"
            self.protoshape['par_file'] = "dna-rna-allatom-hj-opls-1.3.param"
            self.protoshape['dna'] = True

        if item == "Protein-Nucleic":
            self.protoshape['dna'] = True

        pdb_file = tk.filedialog.askopenfile("r")
        if not pdb_file:
            return
        if pdb_file.name.endswith(".pdb"):
            pdb_update = f"New molecule in the {self.name} file has been added"
            molecule_list = self.contents['partners']
            self.protoshape["moleculetype"] = item
            self.protoshape["raw_pdb"] = pdb_file.read()
            print(self.protoshape)
            new_molecule = self.protoshape
            last_molecule = max([int(i) for i in molecule_list])
            molecule_list[f"{int(last_molecule) + 1}"] = new_molecule
            pdb_file.close()
            self.changes.append(pdb_update)
            self.mbox.showinfo(message=f"pdb succesfully inserted, new molecule created with name Molecule {last_molecule+1}")

        else:
            return

    def delete_molecule(self, item):
        """delete molecule"""
        del self.contents['partners'][f'{item}']

    def delete_molecule_window(self):
        """screen to delete molecules"""
        tk.Button(self.myFrame, text="Click me to go back to molecule selection", relief="groove",
                  command=lambda: [self.clear_window(), self.molecule_window()]) \
            .place(relheight=0.1, relwidth=0.5, relx=0.5, rely=0.9)
        if len(self.contents["partners"]) > 5:
            molecule_button_image = self.molecule_image_small
        else:
            molecule_button_image = self.molecule_image
        x = 0
        for item in self.contents["partners"]:
            tk.Button(self.myFrame, wraplength=130, text=" Molecule " + item + " options",
                image=molecule_button_image, compound=tk.LEFT, justify=tk.RIGHT, relief="groove",
                command=lambda item=item: [self.delete_molecule(item), self.clear_window(), self.molecule_window()]) \
                .place(relheight=1 / len(self.contents["partners"]), relwidth=0.5, relx=0, rely=0 + x)
            x += 1 / len(self.contents["partners"])


if __name__ == "__main__":
    e = superparent(root)
    root.mainloop()
