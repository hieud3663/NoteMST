from pathlib import Path

from tkinter import *
# import tkinter as tk
from data2 import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font, ttk, messagebox
import requests


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")

MST_GL = ''
NAME_GL = ''
NOTE = ''
TEXT_COLOR = 'green'


def getInfo():
    data = getData()

    for row in tree.get_children():
        tree.delete(row)
    for row in data:
        tree.insert("", "end", text = row[1], values=row)

    return data

def getMSTInfo(mst):
    re = requests.get(f'https://api.vietqr.io/v2/business/{mst}').json()
    if re['code'] == '00':
        data = re['data']
        id = data['id']
        name = data['name']

        return id, name
    else:
        return None, None
    
def getMSTInfo2(mst):
    global MST_GL, NAME_GL, TEXT_COLOR, NOTE
    if mst:
        MST_GL, NAME_GL = getMSTInfo(mst)
        if NAME_GL:
            name_cty.set(NAME_GL)
            TEXT_COLOR = 'green'
        else:
            name_cty.set("Không tìm thấy thông tin!!!")
            TEXT_COLOR = 'red'

        name_cty_entry.config(fg=TEXT_COLOR)


def reset_entry():
    mst_input.set('')
    entry_2.config(textvariable=mst_input)

    name_cty.set('')
    name_cty_entry.config(textvariable=name_cty)

    text_note.delete("1.0", "end")  # Xóa nội dung ghi chú cũ


def search(data, mst):


    if mst == "":  # Nếu ô trống, quay lại dữ liệu ban đầu
        filterData = data
    else:
        filterData = [row for row in data if str(row[1]).startswith(str(mst))]

    for row in tree.get_children():
        tree.delete(row)
    for row in filterData:
        tree.insert("", "end", text = row[1], values=row)

def add(data):
    global dataInfo
    list_mst = [str(i[1]) for i in dataInfo]

    if MST_GL in list_mst:
        messagebox.showerror("Lỗi", "✘ MST Công ty đã tồn tại!!!")
    elif MST_GL and NAME_GL:
        NOTE = text_note.get("1.0", "end-1c").strip()

        info = (MST_GL, NAME_GL, NOTE)

        res = postData(info)
        if res:
            messagebox.showinfo("Thành công", "✔ Thêm dữ liệu thành công")
            dataInfo = getInfo()
            reset_entry()
        else:
            messagebox.showerror("Lỗi", "✘ Đã xảy ra lỗi!!!")
    else:
        messagebox.showwarning("Cảnh báo", "✘ Tên công ty không được để trống!!!")

    return 0


def edit(data):
    global dataInfo
    mst = mst_input.get()
    name = name_cty.get()
    note = text_note.get("1.0", "end-1c").strip()

    if mst and name:
        info = (mst, name, note)
        res = editData(info)
        if res:
            messagebox.showinfo("Thành công", "✔ Cập nhật dữ liệu thành công")
            dataInfo = getInfo()
        else:
            messagebox.showerror("Lỗi", "✘ Đã xảy ra lỗi!!!")
    else:
        messagebox.showwarning("Cảnh báo", "✘ MST và Tên công ty không được để trống!!!")

    reset_entry()
    return 0


def on_tree_select(event):
    selected_item = tree.selection()  # Lấy ID của hàng được chọn
    
    if selected_item:
        item = tree.item(selected_item[0])  # Lấy dữ liệu hàng được chọn
        # print(item)
        values = item["values"]  # Lấy danh sách các giá trị trong hàng

        
        # Điền dữ liệu vào các ô nhập liệu
        # mst_input.set(values[1])  # MST
        mst_input.set(item['text']) # MST
        name_cty.set(values[2])   # Tên công ty
        text_note.delete("1.0", "end")  # Xóa nội dung ghi chú cũ
        text_note.insert("1.0", values[3])  # Ghi chú mới


def relative_to_assets(path: str) -> Path:
    return "assets/" + path


window = Tk()

window.geometry("1222x700")
window.title(" ♥ Note MST ♥ ")
window.configure(bg = "#E6FDD9")
window.resizable(True, True)

window.iconbitmap('assets/icon.ico')
mst = StringVar()
name_cty = StringVar()
msg = StringVar()
mst_input = StringVar()

#khai báo bảng dữ liệu
# :

#laays duwx lieuej

# Định nghĩa font chữ
set_font = font.Font(family="Arial", size=12)

canvas = Canvas(
    window,
    bg = "#E6FDD9",
    height = 791,
    width = 1222,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    553.4466094970703,
    131.79474258422852,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=set_font,
    textvariable=mst
)
entry_1.place(
    x=401.0,
    y=111.0,
    width=304.8932189941406,
    height=39.58948516845703
)

canvas.create_text(
    55.0,
    270.54541015625,
    anchor="nw",
    text="Ghi chú\n",
    fill="#000000",
    font=("Poppins Bold", 18 * -1)
)

canvas.create_text(
    582.0272827148438,
    201.570068359375,
    anchor="nw",
    text="Tên công ty",
    fill="#000000",
    font=("Poppins Bold", 20 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("lay_thongtin.png"))
lay_thongtin = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: getMSTInfo2(mst_input.get()),
    relief="flat"
)
lay_thongtin.place(
    x=396.85552978515625,
    y=195.79736328125,
    width=152.1785430908203,
    height=37.11013412475586
)

button_image_2 = PhotoImage(
    file=relative_to_assets("tim_kiem.png"))
tim_kiem = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: search(dataInfo, mst.get()),
    relief="flat"
)
tim_kiem.place(
    x=743.0,
    y=111.0,
    width=89.0,
    height=39.11013412475586
)

button_image_3 = PhotoImage(
    file=relative_to_assets("sua.png"))
sua = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: edit(dataInfo),
    relief="flat"
)
sua.place(
    x=815.796142578125,
    y=307.9524230957031,
    width=154.203857421875,
    height=37.11013412475586
)

button_image_4 = PhotoImage(
    file=relative_to_assets("them.png"))
them = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add(dataInfo),
    relief="flat"
)
them.place(
    x=620.0,
    y=307.9524230957031,
    width=163.11875915527344,
    height=37.11013412475586
)


#Thông báo
# msg_label = Label(window, textvariable=msg, font=set_font, bg='lightpink') #thông báo
# msg_label.place(
#     x = 300,
#     y = 350
# )

# Bảng hiển thị dữ liệu
tree = ttk.Treeview(window)
columns = ("ID", "MST", "Tên công ty", "Ghi chú", "Thời gian")
tree.config(columns=columns, show="headings")
style = ttk.Style()
style.configure("Treeview", font=("Arial", 12), rowheight=25)  # Font hàng dữ liệu
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))  # Font tiêu đề cột


#bảng dữ liệu
column_widths = {"ID": 50, "MST": 180, "Tên công ty": 400, "Ghi chú": 180, "Thời gian": 200}
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=column_widths[col],  anchor='center')

tree.place(
    x=25,
    y=370,
    relwidth= 0.95,
    relheight=0.45
)


#####################3
dataInfo = getInfo()
##############################

canvas.create_text(
    43.0,
    204.0,
    anchor="nw",
    text="Thêm MST",
    fill="#000000",
    font=("Poppins Bold", 18 * -1)
)

canvas.create_text(
    285.0,
    118.56594848632812,
    anchor="nw",
    text="Tìm MST",
    fill="#000000",
    font=("Poppins Bold", 18 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    263.0,
    215.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=set_font,
    textvariable=mst_input
)
entry_2.place(
    x=159.0,
    y=195.0,
    width=208.0,
    height=38.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("note.png"))
entry_bg_3 = canvas.create_image(
    262.5,
    296.0,
    image=entry_image_3
)
text_note = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=set_font
)
text_note.place(
    x=159.0,
    y=258.0,
    width=207.0,
    height=74.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("name_cty.png"))
entry_bg_4 = canvas.create_image(
    948.0,
    215.0,
    image=entry_image_4
)
name_cty.set(NAME_GL)
name_cty_entry = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=set_font,
    textvariable = name_cty
)
name_cty_entry.place(
    x=727.0,
    y=195.0,
    width=442.0,
    height=38.0
)

canvas.create_text(
    451.0,
    14.0,
    anchor="nw",
    text="NOTE MST",
    fill="#000000",
    font=("Poppins Bold", 40 * -1)
)

tree.bind("<<TreeviewSelect>>", on_tree_select)
entry_1.bind("<KeyRelease>", lambda event: search(dataInfo, mst.get()))
window.mainloop()
