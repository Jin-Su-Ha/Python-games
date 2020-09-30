
import tkinter.ttk as ttk
from tkinter import*


root = Tk()
root.title("Image Merge")

#파일 프레임(파일 추가, 선택 삭제)
file_frame = Frame(root)
file_frame.pack(fill='x', padx = 5, pady = 5)

def add_file():
    pass

def del_file():
    pass

def list_file():
    pass

def search_file():
    pass


btn_add_file = Button(file_frame, padx = 5, pady = 5, width = 12, text ='파일추가', command = add_file)
btn_add_file.pack(side = 'left')
btn_del_file = Button(file_frame, padx = 5, pady = 5, width = 12, text = '선택삭제', command = del_file)
btn_del_file.pack(side = 'right')


#리스트 프레임
list_frame = Frame(root)
list_frame.pack(fill = 'both')

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side = 'right', fill = 'y')

list_file = Listbox(list_frame, selectmode = 'extended', height = 15, yscrollcommand = scrollbar.set)
list_file.pack(side = 'left', fill = 'both', expand = True)
scrollbar.config(command = list_file.yview)

#저장 경로 프레임
path_frame = LabelFrame(root, text = '저장경로')
path_frame.pack(fill='x', padx = 5, pady = 5)

save_path = Entry(path_frame)
save_path.pack(side = 'left', fill = 'x', expand = True, padx = 5, pady = 5)

btn_search_file = Button(path_frame, padx = 5, pady = 2, width = 6,text ='찾아보기', command = search_file)
btn_search_file.pack(side = 'right')




root.mainloop()