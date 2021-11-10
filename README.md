# README

# haddock-json-editor

A simple gui to help you change your molecule json files.

# about

This is meant as an offline/intermediary solution to editing molecule json files. This will be made available via web interface in an upcoming haddock update hopefully soon. You can use this to change the PDB and/or active/passive residue.

# requirements:

- A working python 3 environment with pip. 
- The haddock-logo and molecule images are required to be in the same map as the gui.py script.

 
# for windows users:

open cmd, navigate to your map of choice. If you already have git you can skip the first step

Just copy pasta the commands below into your terminal. Say Y if it asks you a Y/n question. 


```
pip install git
```

```
git clone https://github.com/haddocking/haddock24-json-editor
```

```
pip install -r requirements.txt
```

```
gui.py 
```

# For linux users:

open terminal, navigate to your map of choice. If you already have git you can skip the first step

Just copy pasta the commands below into your terminal. Say Y if it asks you a Y/n question.

```
sudo apt-get install git
```

```
git clone https://github.com/haddocking/haddock24-json-editor
```

```
pip3 install -r requirements.txt
```

```
python3 gui.py 
```

# Usage for editing your json file

Once you have executed the script you should be presented with the following gui.

![ExplainPicture1](https://user-images.githubusercontent.com/39408360/140933003-5df5a5a4-5993-4975-be4c-c0b7c6e6fcbb.png)

By clicking on the top button a file opener will appear and you can navigate to the folder where the json file is you wish to edit.

![ExplainPicture3](https://user-images.githubusercontent.com/39408360/140933013-0f11fbe0-fdde-4a99-b104-ba2a608f1e2a.png)

Upon succesfully finding and opening your json file you should be prompted with the following screen. For each molecule a button will be generated.

![ExplainPicture4](https://user-images.githubusercontent.com/39408360/140933015-ce99d1d0-719e-44b4-ac12-b22397b6ab09.png)

Click on the molecule of your choice you wish to edit. You will then be taken to the following screen. For now we will replace a pdb.

![ExplainPicture5](https://user-images.githubusercontent.com/39408360/140933017-a761ef3b-1f0c-48d5-9ac1-cc06868cae7a.png)

Clicking on replace pdb will open up a file browser again, use this to open up your .pdb file.

![ExplainPicture6](https://user-images.githubusercontent.com/39408360/140933019-be82f155-9f9d-422b-98ef-0efeb2fb79a1.png)

If all went well, you should recieve the following popup.

![ExplainPicture7](https://user-images.githubusercontent.com/39408360/140933020-7f8663b6-69ea-480b-812e-a4b77203e1a5.png)

Afterwards you have replaced your pdb file you will automaticly be taken back to the molecule selection screen

![ExplainPicture8](https://user-images.githubusercontent.com/39408360/140933022-b582112b-c987-4543-b81d-039174aea3e8.png)

For editing a residue of a molecule, select the molecule. But this time click edit active/passive residue (they work the same).
You will be presented with the following screen

![ExplainPicture9](https://user-images.githubusercontent.com/39408360/140933024-3831f988-009b-4891-b144-3cdcb0aad1a0.png)

Editing a residue you can do by clicking on the text box and using your keyboard.
If the residue for some reason is very large and you need to change it with another very large residue, you can use doubleclick on the textbox and then ctrl-c ctrl-v (copy paste) your new residue in. 

![ExplainPicture10](https://user-images.githubusercontent.com/39408360/140936507-3916a13d-8570-466d-a26d-8c5b5a5ae006.png)

You will then be taken back to the molecule selection screen, having done our changes we now save the new file.

![ExplainPicture11](https://user-images.githubusercontent.com/39408360/140937729-5b6215d8-f92a-4be9-b602-fa198b071041.png)

Save your file and done!

# Updates/desires/requests

If you would like more, maybe different options, feel free to add requests below 
