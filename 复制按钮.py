import tkinter,win32clipboard

def copy(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()
    word.set('')

def product(text):
    dic = {
        'C6X': 6,
        'PEW': 8,
        'PE' : 7,
        'S'  : 13,
        'HST': 11,
        'HPT': 10,
        'PF' : 16,
        'PFW': 15,
        'CI5X':14,
        'VSI6X':17,
        'MTM': 28,
        'MTW': 27,
        'MB5X':26,
        'LM':  23,
        'LUM': 22,
        'XZM': 20,
        'SCM': 20,
        'K':40,
        'F5X':34,
        'S5X':51
    }
    text = text.split('/')
    result = ''
    for i in range(len(text)):
        text[i] = str(dic[text[i].upper()])
        result += text[i]+','
    result = result.strip(',')
    copy(result)
    products.set('')

if __name__ == "__main__":
    pic = '/images/materials/'
    content = '''<div class="pt20 pb20">
<div class="relative"><img src="/images/materials/application/aaaaaa.jpg" alt="" />
<div class="wenzi">
<p class="font_sub">Application: bbbbbbbbb</p>
<p>Production fineness: ccccccc</p>
</div>
</div>
<p class="mt20">ddddddddddd</p>
</div>
'''
    window = tkinter.Tk()
    window.wm_attributes("-topmost",1)
    window.wm_geometry("300x300+1260+200")
    # word = tkinter.StringVar()
    # tkinter.Entry(window,textvariable=word,width=30).pack(side=tkinter.TOP)
    # product_button = tkinter.Button(window,text='生成',command=lambda:copy(pic+word.get()+'/big.jpg'),width=30,pady=6)
    # product_button.pack(side=tkinter.TOP)
    url_button = tkinter.Button(window,text='复制',command=lambda:copy(content),width=30,pady=6)
    url_button.pack(side=tkinter.TOP)
    # products = tkinter.StringVar()
    # tkinter.Entry(window,textvariable=products,width=30).pack(side=tkinter.TOP)
    # tkinter.Button(window,text='相关产品',command=lambda:product(products.get()),width=30,pady=6).pack(side=tkinter.TOP)
    window.mainloop()