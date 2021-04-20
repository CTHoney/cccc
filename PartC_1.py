import csv
from tkinter import *

import cv2
from PIL import ImageTk,Image
from pandas import np
from matplotlib import pyplot as plt


class Part_C:
    def __init__(self,master):
        self.frame = Frame(master,bg="black",height=100)
        self.frame.pack(expand=1, side=LEFT,fill=X, anchor=NW)

        self.fun_fram=Frame(self.frame)
        self.fun_fram.pack(side=LEFT,anchor=NW)
        # ---------------------Menu Creation ------------------------
        self.mbar = Frame(self.fun_fram, relief='raised', width=20, bd=2)
        self.mbar.pack(expand=0, fill=X, side=TOP)

        # Create forground menu ------------------------------------------
        self.fgbutton = Menubutton(self.mbar, text='Adjust')
        self.fgbutton.pack(side=LEFT)
        self.fgmenu = Menu(self.fgbutton, tearoff=0)
        self.fgbutton['menu'] = self.fgmenu

        # Populate Forground menu
        self.fgmenu.add('command', label='greyscale', command=self.greyscale)
        self.fgmenu.add('command', label='zoom', command=self.Zoom)
        self.fgmenu.add('command', label='red', command=self.Red)
        self.fgmenu.add('command',label='blue',command=self.Blue)
        self.fgmenu.add('command', label='pixelinvert', command=self.PixelInvert)
        self.fgmenu.add('command', label='Draw', command=self.draw)

        self.bbar = Frame(self.fun_fram, relief='raised', width=20, bd=2)
        self.bbar.pack(expand = 1, fill = BOTH, side = BOTTOM, pady = 5, before = self.mbar)
        # -------------------- entry box frame ---------------------
        self.t = StringVar()
        self.lb2 = Label(self.bbar, text='File:')
        self.lb2.pack(side=LEFT)
        self.entry = Entry(self.bbar, textvariable=self.t, bg='white')
        self.bt = Button(self.bbar, text='Load', command=self.load)
        self.entry.pack(side=LEFT, padx=5)
        self.bt.pack(side=LEFT, padx=5)

        # --------------------- listbox frame ------------------------
        self.lf = Frame(self.fun_fram, bd=2, relief='groove')
        self.lb = Label(self.lf, text='Past Events:')
        self.bt1 = Button(self.lf, text='Clear', command=self.clear)
        self.bt2=Button(self.lf, text='Draw', command=self.draw)
        self.listbox = Listbox(self.lf,height=20)
        self.sbl = Scrollbar(self.listbox, orient=VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.sbl.set)
        self.lb.pack(expand=1,side=TOP, padx=5,anchor=NW)
        self.bt1.pack(side=BOTTOM)
        self.bt2.pack(side=BOTTOM)
        self.listbox.pack(padx=5, fill=X)
        self.sbl.pack(side=RIGHT, fill=Y)
        self.lf.pack(expand=0, fill=X, pady=5, before=self.bbar, side=BOTTOM)



        self.showImage=Frame(master,bg="black")
        self.label_img=Label(self.showImage,bg="black")
        self.label_img.pack(side=TOP,fill=BOTH)
        self.showImage.pack(anchor=NW,pady=50,padx=50,after=self.fun_fram)

        #part_C
        self.file = "US_Census_2018_Poverty.csv"



    def clear(self):
        self.listbox.delete(0, END)
        self.label_img.config(image='')
    def load(self):
        try:
            img = cv2.imread(self.t.get())  # opencv读取图片
            res = cv2.resize(img, (800, 600), interpolation=cv2.INTER_CUBIC)  # 用cv2.resize设置图片大小
            img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
            current_image = Image.fromarray(img2)  # 将图像转换成Image对象
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.label_img.imgtk = imgtk
            self.label_img.config(image=imgtk)
            self.listbox.insert(END, 'Loaded file ' + self.t.get())
        except Exception as e:
            print(e)
            self.listbox.insert(END, 'Error loading file ' + self.t.get())


    # def save(self):
    #     try:
    #        img=cv2.imread(self.t.get())
    #        cv2.imwrite("temp1.jpg",img)
    #        self.listbox.insert(END,'Save successfully!')
    #     except:
    #         self.listbox.insert(END, 'Save filed ' + self.t.get())

    #灰度处理
    def greyscale(self):
        try:
            self.clear()
            img = cv2.imread(self.t.get())  # opencv读取图片
            # 将图片从 BGR 空间转换到 HSV 空间
            res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            current_image = Image.fromarray(res)  # 将图像转换成Image对象
            cv2.imwrite("grey_temp.jpg", res)
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.label_img.imgtk = imgtk
            self.label_img.config(image=imgtk)
            self.listbox.insert(END, 'Loaded file ' + self.t.get())
        except Exception as e:
            print(e)
            self.listbox.insert(END, 'Error loading file ' + self.t.get())



    def Zoom(self):
        try:
            self.clear()
            img = cv2.imread(self.t.get())  # opencv读取图片
            # 获取图片信息
            x, y = img.shape[0:2]
            dst = cv2.resize(img, (int(y / 2), int(x / 2)))
            current_image = Image.fromarray(dst)  # 将图像转换成Image对象
            cv2.imwrite("zoom_temp.jpg", dst)
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.label_img.imgtk = imgtk
            self.label_img.config(image=imgtk)
            self.listbox.insert(END, 'Loaded file ' + self.t.get())
        except Exception as e:
            print(e)
            self.listbox.insert(END, 'Error loading file ' + self.t.get())



    def Red(self):
        try:
            self.clear()
            img = cv2.imread(self.t.get())
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            img_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
            # Plot the converted images
            current_image = Image.fromarray(img_hls)  # 将图像转换成Image对象
            cv2.imwrite("red_temp.jpg", img_hls)
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.label_img.imgtk = imgtk
            self.label_img.config(image=imgtk)
            self.listbox.insert(END, 'Loaded file ' + self.t.get())
        except Exception as e:
            print(e)
            self.listbox.insert(END, 'Error loading file ' + self.t.get())



    #像素取反
    def PixelInvert(self):
        try:
            self.clear()
            img = cv2.imread(self.t.get())  # opencv读取图片
            res = cv2.bitwise_not(img)
            current_image = Image.fromarray(res)  # 将图像转换成Image对象
            cv2.imwrite("PixelInvert_temp.jpg", res)
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.label_img.imgtk = imgtk
            self.label_img.config(image=imgtk)
            self.listbox.insert(END, 'Loaded file ' + self.t.get())
        except Exception as e:
            print(e)
            self.listbox.insert(END, 'Error loading file ' + self.t.get())


    def Blue(self):
        try:
            self.clear()
            img = cv2.imread(self.t.get())  # opencv读取图片
            # 将图片从 BGR 空间转换到 HSV 空间
            HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            H, S, V = cv2.split(HSV)
            LowerBlue = np.array([100, 100, 50])
            UpperBlue = np.array([130, 255, 255])
            mask = cv2.inRange(HSV, LowerBlue, UpperBlue)
            res = cv2.bitwise_and(img, img, mask=mask)
            current_image = Image.fromarray(res)  # 将图像转换成Image对象
            cv2.imwrite("Blue_temp.jpg", res)
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.label_img.imgtk = imgtk
            self.label_img.config(image=imgtk)
            self.listbox.insert(END, 'Loaded file ' + self.t.get())
        except Exception as e:
            print(e)
            self.listbox.insert(END, 'Error loading file ' + self.t.get())



    #读数据绘制表
    def draw(self):
        self.clear()
        white_p=[]
        Black_p = []
        Hispanic_p = []
        Asian_p = []
        n_x=['white','Black','Hispanic','Asian']
        with open(self.file, 'r') as f:
            reader = csv.reader(f)
            row=0
            for var in reader:
                if row==0:
                    pass
                else:
                    white_p.append(int(var[2])/int(var[1])*100)
                    Black_p.append(int(var[4])/int(var[3])*100)
                    Hispanic_p.append(int(var[6])/int(var[5])*100)
                    Asian_p.append(int(var[8])/int(var[7])*100)
                row+=1
        white_p_sum=0
        for n in white_p:
            white_p_sum+=n
        Black_p_sum = 0
        for n in Black_p:
            Black_p_sum += n
        Hispanic_p_sum = 0
        for n in Hispanic_p:
            Hispanic_p_sum += n
        Asian_p_sum = 0
        for n in Asian_p:
            Asian_p_sum += n
        result = [int(white_p_sum / len(white_p)), int(Black_p_sum / len(Black_p)),
                  int(Hispanic_p_sum / len(Hispanic_p)), int(Asian_p_sum / len(Asian_p))]
        # 绘制直方图
        plt.bar(n_x,result , color='blue')

        # 设置图表参数
        plt.xlabel('Ethnicity', fontsize=15, color='black')  # 设置x轴标签
        plt.ylabel('Percent of Ethnicity Group', fontsize=15, color='green')  # 设置y轴标签
        plt.title('100% Below Poverty Level in 2018', fontsize=20)  # 设置标题
        plt.savefig("draw.png", bbox_inches='tight')
        img = cv2.imread("draw.png")  # opencv读取图片
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        current_image = Image.fromarray(img2)  # 将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        self.label_img.imgtk = imgtk
        self.label_img.config(image=imgtk)
        #plt.show()  # 显示图表


if __name__ == '__main__':
    # 初始化Tk()
    root = Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.config(bg="black")
    all=Part_C(root)
    root.geometry("%dx%d" % (w, h))
    # 设置标题
    root.title('Python GUI Learning')
    root.pack_propagate(0)
    # 进入消息循环
    root.mainloop()