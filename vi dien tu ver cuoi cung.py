import tkinter as tk
from tkinter.font import Font
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import messagebox
import json
import hashlib
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Lanzim\Downloads\vi dien tu ver8\assets\Chung") #copy duong dan cua folder chung vao day

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class TaiKhoan:
    def __init__(self, username, password, name):
        self.username = username
        self.__password = self.hash_password(password)
        self.name = name
        self.balance = 0
        self.transaction_history = []

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def set_password(self, new_password):
        self.__password = self.hash_password(new_password)

    def check_password(self, password):
        return self.__password == self.hash_password(password)


    def nap_tien(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Nạp tiền: +{amount} VND")

    def rut_tien(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transaction_history.append(f"Rút tiền: -{amount} VND")
        else:
            messagebox.showerror("Lỗi", "Không đủ tiền trong tài khoản.")

class ViTien(TaiKhoan):
    lai_suat = {'1 tháng': 0.05, '3 tháng': 0.07, '6 tháng': 0.1, '1 năm': 0.15}

    def __init__(self, username, password, name):
        super().__init__(username, password, name)

    def tinh_lai(self, ky_han):
        if ky_han in self.lai_suat:
            lai_suat = self.lai_suat[ky_han]
            lai = self.balance * lai_suat
            messagebox.showinfo("Lãi suất", f"Lãi suất dự kiến sau {ky_han} là: {lai} VND")
        else:
            messagebox.showerror("Lỗi", "Không hỗ trợ kỳ hạn này.")

class ViTienDiDong:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ViTienDiDong, cls).__new__(cls, *args, **kwargs)
            cls._instance.users = {}
        return cls._instance


    def dang_ky(self, username, password, name):
        if username not in self.users:
            self.users[username] = ViTien(username, password, name)
            messagebox.showinfo("Thông báo", "Tạo tài khoản thành công.")
        else:
            messagebox.showerror("Lỗi", "Tài khoản đã tồn tại.")

    def dang_nhap(self, username, password):
        if username in self.users:
            user = self.users[username]
            if user.check_password(password):
                messagebox.showinfo("Thông báo", "Đăng nhập thành công.")
                return user
            else:
                messagebox.showerror("Lỗi", "Sai mật khẩu.")
        else:
            messagebox.showerror("Lỗi", "Tài khoản không tồn tại.")

    def serialize_users(self):
        serialized_users = {}
        for username, user in self.users.items():
            serialized_users[username] = {'password': user.get_password(), 'balance': user.balance, 'transaction_history': user.transaction_history}
        
        with open('users.json', 'a') as f:
            json.dump(serialized_users, f)

    def deserialize_users(self, serialized_data):
        deserialized_users = json.loads(serialized_data)
        for username, user_data in deserialized_users.items():
            self.users[username] = ViTien(username, user_data['password'])
            self.users[username].balance = user_data['balance']
            self.users[username].transaction_history = user_data['transaction_history']

class trangdangnhap(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.vi_tien_dien_thoai = ViTienDiDong()
        self.page1()

    def page1(self):
        self.master.geometry("540x960")
        self.master.configure(bg = "#F0F0F0")
        self.master.resizable(False, False)
        font32=Font(family="SF Compact Display", size=28, weight="bold")
        font20=Font(family="SF Compact Display", size=16, weight="bold")
        font12=Font(family="SF Compact Display", size=10, weight="bold") 
        self.canvas = Canvas(
            self.master,
            bg = "#F0F0F0",
            height = 960,
            width = 540,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)

        self.entry_image_1 = PhotoImage(file=relative_to_assets("tendangnhap1.png"))
        self.entry_bg_1 = self.canvas.create_image(268.5, 586.0, image=self.entry_image_1)
        self.entry_password = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
        self.entry_password.place(x=105.0, y=561.0, width=327.0, height=48.0)

        self.entry_image_2 = PhotoImage(file=relative_to_assets("matkhau1.png"))
        self.entry_bg_2 = self.canvas.create_image(269.5, 494.0, image=self.entry_image_2)
        self.entry_username = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_username.place(x=106.0, y=469.0, width=327.0, height=48.0)

        self.button_image_1 = PhotoImage(file=relative_to_assets("dangnhap1.png"))
        self.dangnhap1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.login, relief="flat")
        self.dangnhap1.place(x=106.0, y=670.0, width=330.0, height=45.0)

        self.button_image_2 = PhotoImage(file=relative_to_assets("dangky1.png"))
        self.dangki1 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, command=lambda: self.master.switch_frame(trangdangki), relief="flat")
        self.dangki1.place(x=317.0, y=725.0, width=56.0, height=20.0)

        self.image_image_1 = PhotoImage(file=relative_to_assets("background1.png"))
        self.image_1 = self.canvas.create_image(400.0, 670.0, image=self.image_image_1)

        self.canvas.create_text(54.0, 84.0, anchor="nw", text="Welcome!", fill="#000000", font=font32)
        self.canvas.create_text(54.0, 131.0, anchor="nw", text="Đăng nhập để tiếp tục", fill="#000000", font=font20)
        self.canvas.create_text(106.0, 435.0, anchor="nw", text="Tên đăng nhập :", fill="#000000", font=font20)
        self.canvas.create_text(191.0, 726.0, anchor="nw", text="Không có tài khoản?", fill="#000000", font=font12)
        self.canvas.create_text(107.0, 533.0, anchor="nw", text="Mật khẩu :", fill="#000000", font=font20)

        self.master.mainloop()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username and password:
            user = self.vi_tien_dien_thoai.dang_nhap(username, password)
            if user:
                self.taohome(user)
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên người dùng và mật khẩu.")

    def taohome(self, user):
        self.master.switch_frame(Home, vi_tien_dien_thoai=self.vi_tien_dien_thoai, user=user)

class trangdangki(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.vi_tien_dien_thoai = ViTienDiDong()
        self.page2()

    def page2(self):
        self.master.geometry("540x960")
        self.master.configure(bg = "#F0F0F0")
        self.master.resizable(False, False)
        font32=Font(family="SF Compact Display", size=28, weight="bold")
        font20=Font(family="SF Compact Display", size=16, weight="bold")
        self.canvas = Canvas(
            bg = "#F0F0F0",
            height = 960,
            width = 540,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)

        self.entry_image_3 = PhotoImage(file=relative_to_assets("hovaten2.png"))
        self.entry_bg_3 = self.canvas.create_image(268.5, 470.0, image=self.entry_image_3)
        self.entry_name = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_name.place(x=105.0, y=445.0, width=327.0, height=48.0)
        
        self.entry_image_4 = PhotoImage(file=relative_to_assets("tendangnhap2.png"))
        self.entry_bg_4 = self.canvas.create_image(268.5, 570.0, image=self.entry_image_4)
        self.entry_username = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_username.place(x=106.0, y=545.0, width=327.0, height=48.0)

        self.entry_image_5 = PhotoImage(file=relative_to_assets("matkhau2.png"))
        self.entry_bg_5 = self.canvas.create_image(268.5, 664.0, image=self.entry_image_5)
        self.entry_password = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
        self.entry_password.place(x=105.0, y=639.0, width=327.0, height=48.0)

        self.image_image_2 = PhotoImage(file=relative_to_assets("background1.png"))
        self.image_1 = self.canvas.create_image(400.0, 670.0, image=self.image_image_2)

        self.canvas.create_text(54.0, 84.0, anchor="nw", text="Welcome!", fill="#000000", font=font32)
        self.canvas.create_text(54.0, 131.0, anchor="nw", text="Đăng kí để tiếp tục", fill="#000000", font=font20)
        self.canvas.create_text(106.0, 513.0, anchor="nw", text="Tên đăng nhập :", fill="#000000", font=font20)
        self.canvas.create_text(105.0, 413.0, anchor="nw", text="Họ và tên :", fill="#000000", font=font20)
        self.canvas.create_text(107.0, 611.0, anchor="nw", text="Mật khẩu :", fill="#000000", font=font20)

        self.button_image_3 = PhotoImage(file=relative_to_assets("dangky2.png"))
        self.button_3 = Button(image=self.button_image_3, borderwidth=0, highlightthickness=0, command=self.register, relief="flat")
        self.button_3.place(x=106.0, y=731.0, width=330.0, height=45.0)

        self.master.mainloop()

    def register(self):
        name = self.entry_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username and password:
            self.vi_tien_dien_thoai.dang_ky(username, password, name)
            self.vi_tien_dien_thoai.name = name
            self.master.switch_frame(trangdangnhap)
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên người dùng và mật khẩu.")

class Home(tk.Frame):
    def __init__(self, master=None, vi_tien_dien_thoai=None, user=None, **kwargs):
        self.user = user
        super().__init__(master, **kwargs)
        self.master = master
        self.vi_tien_dien_thoai = vi_tien_dien_thoai
        self.trangchu()

    def trangchu(self):
        self.master.geometry("540x960")
        self.master.configure(bg = "#F0F0F0")
        self.master.resizable(False, False)
        font32=Font(family="SF Compact Display", size=28, weight="bold")
        font25=Font(family="SF Compact Display", size=20, weight="bold")
        font23=Font(family="SF Compact Display", size=18, weight="bold")
        font19=Font(family="SF Compact Display", size=14, weight="bold")
        self.canvas = Canvas(
            self.master,
            bg = "#F0F0F0",
            height = 960,
            width = 540,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)

        counter = 2
        def toggle_balance_display():
            nonlocal counter
            counter += 1

            if hasattr(self, 'text_id2'):
                self.canvas.delete(self.text_id2)

            if counter % 2 == 0:
                self.text_id2 = self.canvas.create_text(67.0, 392.0, anchor="nw", text='{:,}'.format(self.user.balance), fill="#FFFFFF", font=font19)
            else:
                self.text_id2 = self.canvas.create_text(67.0, 392.0, anchor="nw", text="***.***.***.***", fill="#FFFFFF", font=font19)

        self.image_image_1 = PhotoImage(file=relative_to_assets("bachground3.png"))
        self.canvas.create_image(329.0, 582.0, image=self.image_image_1)
        self.image_image_2 = PhotoImage(file=relative_to_assets("the3.png"))
        self.canvas.create_image(268.0, 335.0, image=self.image_image_2)
        self.button_image_10 = PhotoImage(file=relative_to_assets("xem3.png"))
        self.button_10 = Button(image=self.button_image_10, borderwidth=0, highlightthickness=0, command=toggle_balance_display, relief="flat")
        self.button_10.place(x=268.0, y=392.0, width=26.0, height=23.0)
        toggle_balance_display()  


        self.button_image_4 = PhotoImage(file=relative_to_assets("naptien3.png"))
        self.button_4 = Button(image=self.button_image_4, borderwidth=0, highlightthickness=0, command=lambda: self.master.switch_frame(trangnaptien1, vi_tien_dien_thoai=self.vi_tien_dien_thoai, user=self.user), relief="flat")
        self.button_4.place(x=55.0, y=531.0, width=115.0, height=115.0)
        self.button_image_5 = PhotoImage(file=relative_to_assets("chuyentien3.png"))
        self.button_5 = Button(image=self.button_image_5, borderwidth=0, highlightthickness=0, command=lambda: self.master.switch_frame(trangchuyentien, vi_tien_dien_thoai=self.vi_tien_dien_thoai, user=self.user), relief="flat")
        self.button_5.place(x=212.0, y=531.0, width=115.0, height=115.0)
        self.button_image_6 = PhotoImage(file=relative_to_assets("xemlai3.png"))
        self.button_6 = Button(image=self.button_image_6, borderwidth=0, highlightthickness=0, command=lambda: self.master.switch_frame(TienLai, vi_tien_dien_thoai=self.vi_tien_dien_thoai, user=self.user), relief="flat")
        self.button_6.place(x=369.0, y=531.0, width=115.0, height=115.0)
        self.button_image_7 = PhotoImage(file=relative_to_assets("lichsu3.png"))
        self.button_7 = Button(image=self.button_image_7, borderwidth=0, highlightthickness=0, command=lambda: messagebox.showerror("Rất xin lỗi", "Tính năng BETA, sẽ được cập nhật sau."), relief="flat")
        self.button_7.place(x=55.0, y=683.0, width=115.0, height=115.0)
        self.button_image_8 = PhotoImage(file=relative_to_assets("nganhang3.png"))
        self.button_8 = Button(image=self.button_image_8, borderwidth=0, highlightthickness=0, command=lambda: messagebox.showerror("Rất xin lỗi", "Tính năng BETA, sẽ được cập nhật sau."), relief="flat")
        self.button_8.place(x=212.0, y=683.0, width=115.0, height=115.0)
        self.button_image_9 = PhotoImage(file=relative_to_assets("thongtin3.png"))
        self.button_9 = Button(image=self.button_image_9, borderwidth=0, highlightthickness=0, command=lambda: self.master.switch_frame(trangdangnhap), relief="flat")
        self.button_9.place(x=369.0, y=683.0, width=115.0, height=115.0)

        self.canvas.create_rectangle(191.8876953125, 945.0, 346.8876953125, 950.0, fill="#C2C2C2", outline="")
        self.canvas.create_text(67.0, 92.0, anchor="nw", text="Xin chào,", fill="#000000", font=font32)
        self.canvas.create_text(67.0, 132.0, anchor="nw", text=self.vi_tien_dien_thoai.name, fill="#000000", font=font25)
        self.canvas.create_text(218.0, 388.0, anchor="nw", text="VNĐ", fill="#FFFFFF", font=font23)
        self.canvas.create_text(67.0, 338.0, anchor="nw", text="988686831106", fill="#FFFFFF", font=font25)
        self.canvas.create_text(67.0, 249.0, anchor="nw", text="BCSE BANK", fill="#FFFFFF", font=font32)

        self.master.mainloop()

class trangnaptien1(tk.Frame):
    def __init__(self, master=None, vi_tien_dien_thoai=None, user=None, **kwargs):
        self.user = user
        super().__init__(master, **kwargs)
        self.master = master
        self.vi_tien_dien_thoai = vi_tien_dien_thoai
        self.page4()

    def page4(self):
        self.master.geometry("540x960")
        self.master.configure(bg = "#F0F0F0")
        self.master.resizable(False, False)
        font40=Font(family="SF Compact Display", size=30, weight="bold")
        font20=Font(family="SF Compact Display", size=16, weight="bold")

        self.canvas = Canvas(
            self.master,
            bg = "#F0F0F0",
            height = 960,
            width = 540,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)

        self.entry_image_1 = PhotoImage(file=relative_to_assets("sotaikhoan4.png"))
        self.entry_bg_1 = self.canvas.create_image(269.5,522.5,image=self.entry_image_1)
        self.entry_sotien = Entry(bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
        self.entry_sotien.place(x=76.0,y=497.0,width=387.0,height=49.0)

        self.entry_image_2 = PhotoImage(file=relative_to_assets("sotien4.png"))
        self.entry_bg_2 = self.canvas.create_image(268.0,633.5,image=self.entry_image_2)
        self.entry_stk = Entry(bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
        self.entry_stk.place(x=76.0,y=612.0,width=384.0,height=41.0)

        self.button_image_1 = PhotoImage(file=relative_to_assets("home4.png"))
        self.button_1 = Button(image=self.button_image_1,borderwidth=0,highlightthickness=0,command=self.back_to_home,relief="flat")
        self.button_1.place(x=385.0,y=73.0,width=96.0,height=37.0)

        self.button_image_2 = PhotoImage(file=relative_to_assets("xacnhan4.png"))
        self.button_2 = Button(image=self.button_image_2,borderwidth=0,highlightthickness=0,command=self.xacnhannap,relief="flat")
        self.button_2.place(x=105.0,y=706.0,width=330.0,height=45.0)

        self.image_image_1 = PhotoImage(file=relative_to_assets("background4.png"))
        self.image_1 = self.canvas.create_image(361.0,655.0,image=self.image_image_1)

        self.canvas.create_text(182.0,80.0,anchor="nw",text="Nạp Tiền",fill="#000000",font=font40)
        self.canvas.create_text(80.0,458.0,anchor="nw",text="Số tiền nạp",fill="#000000",font=font20)
        self.canvas.create_text(413.0,501.0,anchor="nw",text="VND",fill="#000000",font=font20)
        self.canvas.create_text(77.0,580.0,anchor="nw",text="Số tài ngoản ngân hàng mẹ",fill="#000000",font=font20)

        self.master.mainloop()
    
    def xacnhannap(self):
        
        try:
            amount = float(self.entry_sotien.get())  
            if amount > 0:
                self.user.nap_tien(amount)
                self.master.switch_frame(napthanhcong, vi_tien_dien_thoai=self.vi_tien_dien_thoai, user=self.user)
            else:
                messagebox.showerror("Lỗi", "Số tiền nạp không hợp lệ!")
        except ValueError:
            messagebox.showerror("Lỗi", "Số tiền nạp không hợp lệ!")

    def back_to_home(self):
        self.master.switch_frame(Home, vi_tien_dien_thoai=self.vi_tien_dien_thoai, user=self.user)
      
class napthanhcong(tk.Frame):
    def __init__(self, master=None, vi_tien_dien_thoai=None, user=None, **kwargs):
        self.user = user
        super().__init__(master, **kwargs)
        self.master = master
        self.vi_tien_dien_thoai = vi_tien_dien_thoai
        self.page5()

    def page5(self):
        self.master.geometry("540x960")
        self.master.configure(bg = "#F0F0F0")
        self.master.resizable(False, False)
        font32=Font(family="SF Compact Display", size=28, weight="bold")
        font20=Font(family="SF Compact Display", size=16, weight="bold")

        self.canvas = Canvas(
            self.master,
            bg = "#F0F0F0",
            height = 960,
            width = 540,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)

        self.button_image_1 = PhotoImage(file=relative_to_assets("hoanthanh5.png"))
        self.button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.back_to_home, relief="flat")
        self.button_1.place(x=105.0, y=706.0, width=330.0, height=45.0)

        self.image_image_1 = PhotoImage(file=relative_to_assets("background5.png"))
        self.image_1 = self.canvas.create_image(361.0, 655.0, image=self.image_image_1)

        self.canvas.create_text(123.0,458.0,anchor="nw",text="BẠN ĐÃ NẠP TIỀN ",fill="#000000",font=font32)
        self.canvas.create_text(148.0,500.0,anchor="nw",text=" THÀNH CÔNG",fill="#000000",font=font32)
        self.canvas.create_text(98.0,577.0,anchor="nw",text="Cảm ơn đã sử dụng dịch vụ BCSE Bank\n     Chúc bạn có một ngày tốt lành <3",fill="#000000",font=font20)

        self.master.mainloop()

    def back_to_home(self):
        self.master.switch_frame(Home, vi_tien_dien_thoai=self.vi_tien_dien_thoai, user=self.user)

class trangchuyentien(tk.Frame):
    def __init__(self, master=None, vi_tien_dien_thoai=None, user=None, **kwargs):
        self.user = user
        super().__init__(master, **kwargs)
        self.master = master
        self.vi_tien_dien_thoai = vi_tien_dien_thoai
        self.page6()

    def page6(self):
        self.master.geometry("540x960")
        self.master.configure(bg = "#F0F0F0")
        self.master.resizable(False, False)
        font40=Font(family="SF Compact Display", size=30, weight="bold")
        font20=Font(family="SF Compact Display", size=16, weight="bold")

        self.canvas = Canvas(
            self.master,
            bg = "#F0F0F0",
            height = 960,
            width = 540,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)

        self.entry_image_1 = PhotoImage(file=relative_to_assets("sotaikhoan6.png"))
        self.entry_bg_1 = self.canvas.create_image(269.5,522.5,image=self.entry_image_1)
        self.entry_sotien2 = Entry(bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
        self.entry_sotien2.place(x=76.0,y=497.0,width=387.0,height=49.0)

        self.entry_image_2 = PhotoImage(file=relative_to_assets("sotien6.png"))
        self.entry_bg_2 = self.canvas.create_image(268.0,633.5,image=self.entry_image_2)
        self.entry_stk2 = Entry(bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
        self.entry_stk2.place(x=76.0,y=612.0,width=384.0,height=41.0)

        self.button_image_1 = PhotoImage(file=relative_to_assets("home6.png"))
        self.button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.back_to_home, relief="flat")
        self.button_1.place(x=385.0, y=73.0, width=96.0, height=37.0)

        self.button_image_2 = PhotoImage(file=relative_to_assets("xacnhan6.png"))
        self.button_2 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.xacnhan, relief="flat")
        self.button_2.place(x=105.0, y=706.0, width=330.0, height=45.0)

        self.image_image_1 = PhotoImage(file=relative_to_assets("background6.png"))
        self.image_1 = self.canvas.create_image(361.0, 655.0, image=self.image_image_1)

        self.canvas.create_text(139.0, 80.0, anchor="nw", text="Chuyển Tiền", fill="#000000", font=font40)
        self.canvas.create_text(80.0, 458.0, anchor="nw", text="Số tiền chuyển", fill="#000000", font=font20)
        self.canvas.create_text(413.0, 501.0, anchor="nw", text="VND", fill="#000000", font=font20)
        self.canvas.create_text(77.0, 580.0, anchor="nw", text="Số tài khoản nhận", fill="#000000", font=font20)

        self.master.mainloop()

    def xacnhan(self):
        try:
            amount = float(self.entry_sotien2.get())
            if amount > 0:
                self.user.rut_tien(amount)
                self.master.switch_frame(ChuyenTienThanhCong, vi_tien_dien_thoai=self.vi_tien_dien_thoai, user=self.user)
            else:
                messagebox.showerror("Lỗi", "Số tiền chuyển không hợp lệ!")
        except ValueError:
            messagebox.showerror("Lỗi", "Số tiền chuyển không hợp lệ!")

    def back_to_home(self):
        self.master.switch_frame(Home, vi_tien_dien_thoai=self.vi_tien_dien_thoai, user=self.user)

class ChuyenTienThanhCong(tk.Frame):
    def __init__(self, master=None, vi_tien_dien_thoai=None, user=None, **kwargs):
        self.user = user
        super().__init__(master, **kwargs)
        self.master = master
        self.vi_tien_dien_thoai = vi_tien_dien_thoai
        self.page7()

    def page7(self):
        self.master.geometry("540x960")
        self.master.configure(bg = "#F0F0F0")
        self.master.resizable(False, False)
        font32=Font(family="SF Compact Display", size=28, weight="bold")
        font20=Font(family="SF Compact Display", size=16, weight="bold")

        self.canvas = Canvas(
            self.master,
            bg = "#F0F0F0",
            height = 960,
            width = 540,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)
        
        self.button_image_1 = PhotoImage(file=relative_to_assets("hoanthanh5.png"))
        self.button_1 = Button(image=self.button_image_1,borderwidth=0,highlightthickness=0,command=self.back_to_home,relief="flat")
        self.button_1.place(x=109.0,y=706.0,width=330.0,height=45.0)
        
        self.canvas.create_text(104.0,458.0,anchor="nw",text="BẠN ĐÃ CHUYỂN TIỀN ",fill="#000000",font=font32)
        self.canvas.create_text(148.0,500.0,anchor="nw",text=" THÀNH CÔNG",fill="#000000",font=font32)
        self.canvas.create_text(98.0,577.0,anchor="nw",text="Cảm ơn đã sử dụng dịch vụ BCSE Bank\n     Chúc bạn có một ngày tốt lành <3",fill="#000000",font=font20)
        
        self.image_image_1 = PhotoImage(file=relative_to_assets("background7.png"))
        self.image_1 = self.canvas.create_image(351.0,639.0,image=self.image_image_1)
        self.master.mainloop()
    
    def back_to_home(self):
        self.master.switch_frame(Home, vi_tien_dien_thoai=self.vi_tien_dien_thoai, user=self.user)

class TienLai(tk.Frame):
    def __init__(self, master=None, vi_tien_dien_thoai=None, user=None, **kwargs):
        self.user = user
        super().__init__(master, **kwargs)
        self.master = master
        self.vi_tien_dien_thoai = vi_tien_dien_thoai
        self.page8()

    def page8(self):
        self.master.geometry("540x960")
        self.master.configure(bg = "#F0F0F0")
        self.master.resizable(False, False)
        font20=Font(family="SF Compact Display", size=16, weight="bold")

        self.canvas = Canvas(
            self.master,
            bg = "#F0F0F0",
            height = 960,
            width = 540,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)

        self.button_image_1 = PhotoImage(file=relative_to_assets("home8.png"))
        self.button_1 = Button(self.master, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.back_to_home, relief="flat")
        self.button_1.place(x=385.0, y=73.0, width=96.0, height=37.0)
        
        self.canvas.create_rectangle(71.0,430.0,458.0,466.0,fill="#FFFFFF",outline="")
        self.canvas.create_rectangle(71.0,548.0,458.0,584.0,fill="#FFFFFF",outline="")
        self.canvas.create_rectangle(71.0,665.0,458.0,701.0,fill="#FFFFFF",outline="")
        self.canvas.create_text(72.0,397.0,anchor="nw",text="Tổng tiền lãi 6 tháng",fill="#000000",font=font20)
        self.canvas.create_text(96.0,434.0,anchor="nw",text='{:,}'.format(self.user.balance * (1 + 0.052) * (1 + 0.052)),fill="#000000",font=font20)
        self.canvas.create_text(96.0,552.0,anchor="nw",text='{:,}'.format(self.user.balance * (1 + 0.066) * (1 + 0.066)),fill="#000000",font=font20)
        self.canvas.create_text(96.0,669.0,anchor="nw",text='{:,}'.format(self.user.balance * (1 + 0.08) * (1 + 0.08) * (1 + 0.08)),fill="#000000",font=font20)
        self.canvas.create_text(407.0,434.0,anchor="nw",text="VND",fill="#000000",font=font20)
        self.canvas.create_text(407.0,552.0,anchor="nw",text="VND",fill="#000000",font=font20)
        self.canvas.create_text(407.0,669.0,anchor="nw",text="VND",fill="#000000",font=font20)
        self.canvas.create_text(72.0,515.0,anchor="nw",text="Tổng tiền lãi 1 năm",fill="#000000",font=font20)
        self.canvas.create_text(72.0,632.0,anchor="nw",text="Tổng tiền lãi 3 năm",fill="#000000",font=font20)
        
        self.image_image_1 = PhotoImage(file=relative_to_assets("background8.png"))
        self.image_1 = self.canvas.create_image(395.0,633.0,image=self.image_image_1)
        self.master.mainloop()
    
    def back_to_home(self):
        self.master.switch_frame(Home, vi_tien_dien_thoai=self.vi_tien_dien_thoai, user=self.user)

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frame = None
        self.user = None  
        self.switch_frame(trangdangnhap)

    def switch_frame(self, frame_class, **kwargs):
        user = kwargs.pop('user', self.user)
        vi_tien_dien_thoai = kwargs.pop('vi_tien_dien_thoai', None)  
        new_frame = frame_class(self, vi_tien_dien_thoai=vi_tien_dien_thoai, user=user, **kwargs) # bọn em bị 1 bug khá khó chịu là user không được lưu sau khi đăng nhập nên phải chuyển sang lưu ở đây và lấy user[] và thông tin của vi_tien_dien_thoai[] từ đây # bọn em bị 1 bug khá khó chịu là user không được lưu sau khi đăng nhập nên phải chuyển sang lưu ở đây và lấy user[] và thông tin của vi_tien_dien_thoai[] từ đây 
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()

    def set_user(self, user):
        self.user = user

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()