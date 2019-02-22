from PIL import Image,ImageTk
import tkinter as tk


class Captcha_By_Hand(object):
    """一个手动输入验证码的弹窗，用与少量登录时"""
    def callback(self):
        self.captcha = self.text.get()
        self.input_window.destroy()
        self.input_window.quit()

    def run(self,img):
        self.input_window = tk.Tk()
        self.input_window.title('需要验证码')
        self.input_window.geometry('250x130')
        self.photo = ImageTk.PhotoImage(img)
        tk.Label(self.input_window, image=self.photo).pack()
        tk.Label(self.input_window, text='请输入验证码：').pack()
        self.text = tk.StringVar()
        tk.Entry(self.input_window, textvariable=self.text).pack()
        tk.Button(self.input_window, text='确定', command=self.callback).pack(ipadx=10, ipady=5)
        self.input_window.mainloop()


if __name__ == '__main__':
    s = Captcha_By_Hand()
    s.run(Image.open('C:\\Users\Administrator\Desktop\captcha.jpg'))
    print(s.captcha)
