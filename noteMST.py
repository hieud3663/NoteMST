from tkinter import *
import tkinter as tk
from tkinter import ttk, font
from data import *

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
        msg.set('✘ MST Công ty đã tồn tại!!!')
        msg_label.config(textvariable=msg, fg='red')

    elif MST_GL and NAME_GL:
        NOTE = text_note.get("1.0", "end-1c").strip()

        info = (MST_GL, NAME_GL, NOTE)

        res = postData(info)
        if res:
            msg.set('✔ Thêm dữ liệu thành công')
            msg_label.config(textvariable=msg, fg='green')
            dataInfo = getInfo()
        else:
            msg.set('✘ Đã xảy ra lỗi!!!')
            msg_label.config(textvariable=msg, fg='red')

    else:
        msg.set('✘ Tên công ty không được để trống!!!')
        msg_label.config(textvariable=msg, fg='red')

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
            msg.set('✔ Cập nhật liệu thành công')
            msg_label.config(textvariable=msg, fg='green')
            dataInfo = getInfo()
        else:
            msg.set('✘ Đã xảy ra lỗi!!!')
            msg_label.config(textvariable=msg, fg='red')

    else:
        msg.set('✘ MST và Tên công ty không được để trống!!!')
        msg_label.config(textvariable=msg, fg='red')

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





# Tạo cửa sổ chính
app = tk.Tk()
app.title(" ♥ Note MST ♥ ")
app.minsize(height=600, width=1000)
app.config(bg = 'lightpink')

tk.Label(app, text=" 🌲💚✲☆ Note MST ☆✲💚🌲", font=('Arial', 20, 'bold'), fg='green', bg='lightpink').grid(row=0, column=1, pady=10)


mst = StringVar()
name_cty = StringVar()
msg = StringVar()


# Bảng hiển thị dữ liệu
columns = ("ID", "MST", "Tên công ty", "Ghi chú", "Thời gian")
tree = ttk.Treeview(app, columns=columns, show="headings")

# Định nghĩa font chữ
set_font = font.Font(family="Arial", size=12)


style = ttk.Style()
style.configure("Treeview", font=("Arial", 10), rowheight=25)  # Font hàng dữ liệu
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))  # Font tiêu đề cột


# Nhập Pincode
tk.Label(app, text="Tìm MST", font=set_font, bg='lightpink').grid(row=1, column=0, pady=5, sticky='e')

pincode_entry = tk.Entry(app, width=30, font=("Arial", 14), textvariable=mst)
pincode_entry.grid(row=1, column=1, padx=1, pady=5)

# Nút Tìm kiếm
dataInfo = getInfo()
search_button = tk.Button(app, text="Search", font=set_font, command=lambda: search(dataInfo, mst.get()))
search_button.grid(row=1, column=2, padx=1, pady=5)


#thêm mst:
tk.Label(app, font=set_font, bg='lightpink').grid(row=2, column=0, padx=20, pady=20)
tk.Label(app, text="Thêm MST", font=set_font, bg='lightpink').grid(row=3, column=0, padx=10, pady=5, sticky='e')
mst_input = StringVar()

mst_input_entry = tk.Entry(app, width=20, font=("Arial", 13), textvariable=mst_input)
mst_input_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

get_mst_btn = tk.Button(app, text="Lấy thông tin", font=set_font, command=lambda: getMSTInfo2(mst_input.get()))
get_mst_btn.grid(row=3, column=2, padx=5, pady=5, sticky='w')

# name cty
tk.Label(app, text="Tên công ty: ", font=("Arial", 13), bg='lightpink').grid(row=4, column=0, padx=5, pady=5, sticky='e')
name_cty.set(NAME_GL)
name_cty_entry = tk.Entry(app, textvariable=name_cty, font=("Arial", 13), width=50, fg=TEXT_COLOR)
name_cty_entry.grid(row=4, column=1, padx=5, pady=5 , sticky='w')

#note
tk.Label(app, text="Ghi chú: ", font=("Arial", 13), bg='lightpink').grid(row=5, column=0, padx=5, pady=5,  sticky='e')
text_note = tk.Text(app, wrap="word", font=("Arial", 12), height=5, width=20)
text_note.grid(row=5, column=1, padx=5, pady=5, sticky='w')

#thêm dữ liệu
msg_label = Label(app, textvariable=msg, font=set_font, bg='lightpink') #thông báo

add_btn = tk.Button(app, text="Thêm dữ liệu", font=set_font, command=lambda: add(dataInfo)) #nut thêm
add_btn.grid(row=6, column=1, padx=5, pady=5, sticky='e')

#sửa dữ liệu
edit_btn = tk.Button(app, text="Sửa dữ liệu", font=set_font, command=lambda: edit(dataInfo))
edit_btn.grid(row=6, column=2, padx=5, pady=5, sticky='w')
msg_label.grid(row=7, column=1, padx=5, pady=5)

#bảng dữ liệu
column_widths = {"ID": 50, "MST": 180, "Tên công ty": 400, "Ghi chú": 180, "Thời gian": 200}
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=column_widths[col])


tree.grid(row=8, column=0, columnspan=len(columns), padx=10, pady=10)
tree.bind("<<TreeviewSelect>>", on_tree_select)


pincode_entry.bind("<KeyRelease>", lambda event: search(dataInfo, mst.get()))
app.mainloop()
