
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

def start_file():
    pass

def close_file():
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

#옵션 프레임
option_frame = LabelFrame(root, text = '옵션')
option_frame.pack(fill='x', padx = 5, pady = 5)

#1.가로 넓이 옵션
lbl_width = Label(option_frame, text = '가로넓이', width =8)
lbl_width.pack(side = 'left')

#1.가로 넓이 콤보
opt_width = ['원본유지','1024','800','640']
cmb_width = ttk.Combobox(option_frame, state= 'readonly',values = opt_width, width = 10)
cmb_width.current(0)
cmb_width.pack(side = 'left')

#2.간격 옵션
lbl_space = Label(option_frame, text = '간격', width =8)
lbl_space.pack(side = 'left')

#2.간격 콤보
opt_space = ['없음','좁게','보통','넓게']
cmb_space= ttk.Combobox(option_frame, state= 'readonly',values = opt_space, width = 10)
cmb_space.current(0)
cmb_space.pack(side = 'left')

#3.포멧 옵션
lbl_format = Label(option_frame, text = '포멧', width =8)
lbl_format.pack(side = 'left')

#3.포멧 콤보
opt_format = ['PNG','JPG','BMP']
cmb_format= ttk.Combobox(option_frame, state= 'readonly',values = opt_format, width = 10)
cmb_format.current(0)
cmb_format.pack(side = 'left')

#실행 프레임
run_frame = Frame(root)
run_frame.pack(fill='x', padx = 5, pady = 5)

btn_start_file = Button(run_frame, padx = 5, pady = 5, width = 12, text ='닫기', command = start_file)
btn_start_file.pack(side = 'right')
btn_close_file = Button(run_frame, padx = 5, pady = 5, width = 12, text = '시작', command = close_file)
btn_close_file.pack(side = 'right')




root.mainloop()