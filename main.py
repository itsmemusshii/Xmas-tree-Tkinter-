from tkinter import*
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Inventory System")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("1300x600")
root.resizable(0, 0)
root.iconbitmap('icon.ico')
#==================================VARIABLES==========================================
PRODUCTNAME = StringVar()
STOCKQTY = StringVar()
PACKAGINGKG= StringVar()
INOUT = StringVar()
SRP = StringVar()
ROLLNo = StringVar()
DELIVERY = StringVar()
PRODUCTNO = StringVar()

SEARCH=StringVar()
temp=StringVar()

#==================================METHODS============================================
def Database():
    global conn, cursor
    conn = sqlite3.connect('DatabaseFile(DONOTDELETE).db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS member (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, ProductName TEXT, StockQty TEXT, PackagingKg TEXT,InOut TEXT, Srp TEXT,Delivery TEXT,ProductNo TEXT)")

def Create():
    if  STOCKQTY.get() == "" or PRODUCTNAME.get() == "":
        txt_result.config(text="Please complete the fields!", fg="red")
    else:
        Database()
        cursor.execute("INSERT INTO member (ProductNo,ProductName, StockQty,PackagingKg,InOut, Srp,Delivery) VALUES(?, ?, ?, ?, ?,?,?)", (str(PRODUCTNO.get()),str(STOCKQTY.get()), str(PRODUCTNAME.get()),str(PACKAGINGKG.get()) ,str(INOUT.get()), str(SRP.get()),str(DELIVERY.get())))
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM member ORDER BY ProductName ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        conn.commit()
        PRODUCTNO.set("")
        PRODUCTNAME.set("")
        STOCKQTY.set("")
        PACKAGINGKG.set("")
        INOUT.set("")
        SRP.set("")
        DELIVERY.set("")
        cursor.close()
        conn.close()
        txt_result.config(text="Created a data!", fg="green")

def Read():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute("SELECT * FROM member ORDER BY ProductName ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    txt_result.config(text="Successfully read the data from database", fg="black")

def Update():
    Database()
    if INOUT.get() == "":
        txt_result.config(text="Please select a choice", fg="red")
    else:
        tree.delete(*tree.get_children())
        cursor = conn.cursor()
        cursor.execute("UPDATE member SET ProductNo = ?,ProductName = ?, 'StockQty' = ?,'PackagingKg'=? ,`InOut` =?,  `Srp` = ?,  `Delivery` = ? WHERE mem_id = ?", (str(PRODUCTNO.get()),str(STOCKQTY.get()), str(PACKAGINGKG.get()),str(PRODUCTNAME.get()) ,str(INOUT.get()), str(SRP.get()),str(DELIVERY.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM member ORDER BY ProductName ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
        cursor.close()
        conn.close()
        PRODUCTNO.set("")
        PRODUCTNAME.set("")
        STOCKQTY.set("")
        PACKAGINGKG.set("")
        INOUT.set("")
        SRP.set("")
        DELIVERY.set("")
        btn_create.config(state=NORMAL)
        btn_read.config(state=NORMAL)
        btn_update.config(state=DISABLED)
        btn_delete.config(state=NORMAL)
        txt_result.config(text="Successfully updated the data", fg="black")
def Reset():
    PRODUCTNO.set("")
    PRODUCTNAME.set("")
    STOCKQTY.set("")
    PACKAGINGKG.set("")
    INOUT.set("")
    SRP.set("")
    DELIVERY.set("")
def searchdb():
    tree.delete(*tree.get_children())
    Database()
    if(temp.get()=="ProductNo"):
      cursor.execute("SELECT * FROM 'member' WHERE ProductNo LIKE '%s' ORDER BY '' ASC" %SEARCH.get())
    else:
      cursor.execute("SELECT * FROM 'member' WHERE InOut LIKE '%s' ORDER BY '' ASC" %SEARCH.get())
    fetch=cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    txt_result.config(text="Successfully searched for the data",fg="black")


def OnSelected(event):
    global mem_id;
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    PRODUCTNO.set("")
    PRODUCTNAME.set("")
    STOCKQTY.set("")
    PACKAGINGKG.set("")
    INOUT.set("")
    SRP.set("")
    DELIVERY.set("")

    PRODUCTNO.set(selecteditem[1])
    PRODUCTNAME.set(selecteditem[3])
    STOCKQTY.set(selecteditem[2])
    PACKAGINGKG.set(selecteditem[4])
    SRP.set(selecteditem[6])
    DELIVERY.set(selecteditem[7])


    btn_create.config(state=DISABLED)
    btn_read.config(state=DISABLED)
    btn_update.config(state=NORMAL)
    btn_delete.config(state=DISABLED)

def Delete():
    if not tree.selection():
       txt_result.config(text="Please select an item first", fg="red")
    else:
        result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM member WHERE mem_id = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
            txt_result.config(text="Successfully deleted the data", fg="black")


def Exit():
    result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()



#================================FRAME=========================
title=Frame(root,height=60,width=1300,bd=5,relief="groove")
title.pack(side=TOP)
left=Frame(root,width=400,height=1240,bd=5,relief="flat")
left.pack(side=LEFT)
right=Frame(root,width=900,height=1232, bd=8, relief="raise")
right.pack(side=LEFT)
#--------------search frame------------------
searchframe=Frame(left,bd=8,width=392,height=500,relief="groove")
searchframe.pack(side=TOP)
form=Frame(left,height=400,width=300,bd=20)
form.pack(side=TOP)
buttonf=Frame(left,bd=8,relief="groove",width=100,height=250)
buttonf.pack(side=BOTTOM)
RadioGroup = Frame(form)
In = Radiobutton(RadioGroup, text="In", variable=INOUT, value="In", font=('arial', 16)).pack(side=LEFT)
Out = Radiobutton(RadioGroup, text="Out", variable=INOUT, value="Out", font=('arial', 16)).pack(side=LEFT)


#==================================LABEL WIDGET=======================================
temp.set("Choices")
searchoptions=OptionMenu(searchframe,temp,"ProductNo","InOut")
searchoptions.pack(side=LEFT)
txt_Search=Label(searchframe,text="Search by",font=('arial',12))
txt_Search.pack(side=TOP)
txt_title = Label(title, width=900, font=('arial', 24), text = "JABBY'S POULTRY STORE INVENTORY SYSTEM")
txt_title.pack()
txt_ProductName = Label(form, text="ProductName:", font=('arial', 16), bd=8)
txt_ProductName.grid(row=2, sticky="e")
txt_StockQty = Label(form, text="Stock Quantity:", font=('arial', 16), bd=8)
txt_StockQty.grid(row=3, sticky="e")
txt_PackagingKg=Label(form, text="Packaging/Kg:", font=('arial', 16), bd=8)
txt_PackagingKg.grid(row=4,sticky='e')
txt_InOut = Label(form, text="InOut:", font=('arial', 16), bd=8)
txt_InOut.grid(row=0, sticky="e")
txt_Srp = Label(form, text="Srp:", font=('arial', 16), bd=8)
txt_Srp.grid(row=5, sticky="e")
txt_Delivery = Label(form, text="Delivery:", font=('arial', 16), bd=8)
txt_Delivery.grid(row=6, sticky="e")
txt_ProductNo = Label(form, text="Product No:", font=('arial', 16), bd=8)
txt_ProductNo.grid(row=1, sticky="e")

txt_result = Label(buttonf)
txt_result.pack(side=TOP)
#==================================ENTRY WIDGET=======================================
Searchtext=Entry(searchframe,textvariable=SEARCH,width=50)
Searchtext.pack(side=TOP)
ProductName = Entry(form, textvariable=PRODUCTNAME, width=40)
ProductName.grid(row=4, column=1)
StockQty = Entry(form, textvariable=STOCKQTY, width=40)
StockQty.grid(row=2, column=1)
PackagingKg = Entry(form,textvariable=PACKAGINGKG,width=40)
PackagingKg.grid(row=3,column=1)
RadioGroup.grid(row=0, column=1)
Srp = Entry(form, textvariable=SRP, width=40)
Srp.grid(row=5, column=1)
Delivery = Entry(form, textvariable=DELIVERY, width=40)
Delivery.grid(row=6, column=1)
ProductNo = Entry(form, textvariable=PRODUCTNO, width=40)
ProductNo.grid(row=1, column=1)

#==================================BUTTONS WIDGET=====================================
btn_create = Button(buttonf, width=10, text="Create", command=Create)
btn_create.pack(side=LEFT)
btn_read = Button(buttonf, width=10, text="Show", command=Read )
btn_read.pack(side=LEFT)
btn_update = Button(buttonf, width=10, text="Update", command=Update, state=DISABLED)
btn_update.pack(side=LEFT)
btn_reset = Button(buttonf, width=10, text="Reset", command=Reset)
btn_reset.pack(side=LEFT)
btn_delete = Button(buttonf, width=10, text="Delete", command=Delete)
btn_delete.pack(side=LEFT)
btn_exit = Button(buttonf, width=10, text="Exit", command=Exit)
btn_exit.pack(side=LEFT)
btn_search = Button(searchframe,width=10,text="Search",command=searchdb)
btn_search.pack(side=BOTTOM)



#==================================LIST WIDGET========================================
scrollbary = Scrollbar(right, orient=VERTICAL)
scrollbarx = Scrollbar(right, orient=HORIZONTAL)
tree = ttk.Treeview(right, columns=("MemberID","Product No", "ProductName", "StockQty","PackagingKg" ,"InOut", "Srp","Delivery"), height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="none", anchor=W)
tree.heading('ProductName', text="ProductName", anchor=W)
tree.heading('StockQty', text="Stock Quantity", anchor=W)
tree.heading('PackagingKg',text="Packaging/Kg",anchor=W)
tree.heading('InOut', text="In/Out", anchor=W)
tree.heading('Srp', text="Srp", anchor=W)
tree.heading('Delivery', text="Delivery", anchor=W)
tree.heading('Product No', text="Product No", anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=125)
tree.column('#3', stretch=NO, minwidth=0, width=125)
tree.column('#4',stretch=NO,minwidth=0,width=125)
tree.column('#4', stretch=NO, minwidth=0, width=125)
tree.column('#5', stretch=NO, minwidth=0, width=125)

tree.pack()
tree.bind('<Double-Button-1>', OnSelected)
#==================================INITIALIZATION=====================================
if __name__ == '__main__':
    root.mainloop()