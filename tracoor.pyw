import pyproj
import csv
import base64
from pyproj import Transformer
from tkinter import *
from tkinter import filedialog, messagebox, PhotoImage
from tkinter import ttk as ttk
import tracoor_text as tx

# * Geographical Coordinate System definitions
WGS84 = pyproj.CRS("EPSG:4326")
CRMT05 = pyproj.CRS(
    "+proj=tmerc +lat_0=0 +lon_0=-84 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs")
CRTM90 = CRTM98 = pyproj.CRS(
    "+proj=tmerc +lat_0=0 +lon_0=-84 +k=0.9996 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs")
LCRN = pyproj.CRS("+proj=lcc +lat_1=10.46666666666667 +lat_0=10.46666666666667 +lon_0=-84.33333333333333 +k_0=0.99995696 +x_0=500000 +y_0=271820.522 +ellps=clrk66 +towgs84=213.11,9.37,-74.95,0,0,0,0 +units=m +no_defs")
LCRS = pyproj.CRS("+proj=lcc +lat_1=9 +lat_0=9 +lon_0=-83.66666666666667 +k_0=0.99995696 +x_0=500000 +y_0=327987.436 +ellps=clrk66 +towgs84=213.11,9.37,-74.95,0,0,0,0 +units=m +no_defs ")

# * Variables
coord_list = [CRMT05, WGS84, CRTM98, CRTM90, LCRN, LCRS]
coord_list_string = ["CRMT05", "WGS84", "CRTM98", "CRTM90", "LCRN", "LCRS"]
file_path = ""
save_path = ""


# * Funtions
# TODO Fine tunning funtions


def do_nothing():
    print("Nothing here!!!!")


def convert_data():
    global coord_from, coord_to, coord_list_string, coord_list
    coord_from = coord_list[coord_list_string.index(from_combo.get())]
    coord_to = coord_list[coord_list_string.index(to_combo.get())]
    transformer = Transformer.from_crs(coord_from, coord_to)
    file = docEntry.get()
    with open(file, newline='') as file:
        CSVFile = csv.reader(file)
        next(CSVFile)
        data = []
        for row in CSVFile:
            Latitude = float(row[0])
            Longitude = float(row[1])
            data.append([Latitude, Longitude])
    transData = []
    for row in data:
        transData.append(list(transformer.transform(row[0], row[1])))
    with open(docSaveEntry.get(), 'w', newline='') as file:
        CSV_File_out = csv.writer(file)
        CSV_File_out.writerow(["Latitud", "Longitud"])
        CSV_File_out.writerows(transData)
    docEntry.delete(0, END)
    docSaveEntry.delete(0, END)
    convert["state"] = DISABLED
    runmenu.entryconfig(0, state=DISABLED)
    messagebox.showinfo(tx.convert_title, tx.convert_text)


def about():
    messagebox.showinfo(tx.about_title, tx.about_text)


def app_use():
    messagebox.showinfo(tx.use_title, tx.use_text)


def open_file():
    global file_path
    root.file_name = filedialog.askopenfilename(
        initialdir=file_path, title=tx.openFile_title, filetypes=[(tx.oFile_csv_text, tx.oFile_csv), (tx.oFile_all_text, tx.oFile_all)])
    docEntry.delete(0, END)
    docEntry.insert(0, root.file_name)
    b_slash = root.file_name.rfind("/")
    if b_slash != -1:
        file_path = root.file_name[0:b_slash+1]
        file_name = root.file_name[b_slash+1:len(root.file_name)]
        file_name = file_name[0:-4]
        docSaveEntry.delete(0, END)
        docSaveEntry.insert(0, file_path + file_name + tx.newFilePrefix)
        convert["state"] = ACTIVE
        runmenu.entryconfig(0, state=ACTIVE)

# * Window propieties


root = Tk()
root.title(tx.appTitle)
root.resizable(width=0, height=0)
img = base64.b64decode(tx.iconBase64)
img = PhotoImage(data=img)
root.iconphoto(True, img)

# * Menu

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Buscar", command=open_file)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(label="Archivo", menu=filemenu)
runmenu = Menu(menubar, tearoff=0)
runmenu.add_command(label="Convertir", command=convert_data, state=DISABLED)
menubar.add_cascade(label="Ejecutar", menu=runmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Acerca", command=about)
helpmenu.add_separator()
helpmenu.add_command(label="Uso", command=app_use)

menubar.add_cascade(label="Ayuda", menu=helpmenu)

# * Aplication elements

mainFrame = Frame(root)
docIn_lb = Label(mainFrame, text="Abrir archivo:")
docEntry = Entry(mainFrame, textvariable=file_path, width=65)
docBrowse = Button(mainFrame, text="Buscar", command=open_file, width=15)
docSave_lb = Label(mainFrame, text="Salvar como:")
docSaveEntry = Entry(mainFrame, textvariable=save_path, width=65)
from_lb = Label(mainFrame, text="Convertir de:")
from_combo = ttk.Combobox(mainFrame, state="readonly",
                          values=coord_list_string, width=10)
from_combo.current(0)
to_lb = Label(mainFrame, text="a:")
to_combo = ttk.Combobox(mainFrame, state="readonly",
                        values=coord_list_string, width=10)
to_combo.current(1)
convert = Button(mainFrame, text="Convertir",
                 state=DISABLED, command=convert_data, width=15, height=2)

# * Aplication elements placement

mainFrame.pack(padx=15, pady=15)
docIn_lb.grid(row=0, column=0, sticky=SW)
docEntry.grid(row=1, column=0, columnspan=3, sticky=W, pady=10)
docBrowse.grid(row=2, column=2, sticky=E)
docSave_lb.grid(row=3, column=0, sticky=SW)
docSaveEntry.grid(row=4, column=0, columnspan=3, sticky=W, pady=10)
from_lb.grid(row=5, column=0, sticky=SW)
from_combo.grid(row=6, column=0, sticky=SW)
to_lb.grid(row=5, column=1, sticky=SW)
to_combo.grid(row=6, column=1, sticky=SW)
convert.grid(row=5, column=2, rowspan=2, sticky=E)

# * Main loop

root.config(menu=menubar)
root.mainloop()
