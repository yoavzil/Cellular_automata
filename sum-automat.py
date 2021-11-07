from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from time import time,sleep
import string
digs = string.digits + string.ascii_letters

root = Tk()
root.title("sum-automaton")
flag = False

def num2array(num):
    array = [int(i) for i in int2base(num,3)]
    array.reverse()
    x  = 7-len(array)
    while x > 0:
        array.append(0)
        x = x-1
    # array.reverse()
    return array


def entering_array(win, width):
    win.delete(ALL)
    rule = simpledialog.askstring("Input", "enter a rule number between 0-2186", parent=win)
    gen = simpledialog.askstring("Input", "enter number of generations(to get classification more than 99)", parent=win)

    user_run(num2array(int(rule)), width, win, int(gen))

def on_closing():
    global flag
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        flag = True
        root.destroy()


def sum_digits(digit):
    return sum(int(x) for x in digit if x.isdigit())

    
def clear(win):
    list = win.grid_slaves()
    for item in win.grid_slaves():
        item.destroy()

def draw_cells(cells, i, width, win):
    j = width/2 - 5*i
    if flag:
        return
    linenum = win.create_text(j-15, 60+5*i, anchor = "nw")
    win.itemconfig(linenum, text= str(i),font = ("courier", 4))
    for cell in cells:
        if flag:
            return
        if cell == '0':
            a = win.create_rectangle(j,60+5*i,j+5,65+5*i, fill = "blue")
            win.pack()
        if cell == '1':
            a = win.create_rectangle(j,60+5*i,j+5,65+5*i, fill = "cyan")
            win.pack()
        if cell == '2':
            a = win.create_rectangle(j,60+5*i,j+5,65+5*i, fill = "lime green")
            win.pack()
        j = j+5
        
def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)


def automat_calc(array, width, win, gen):
    extra_flag = False
    classer = []
    cells = '010'
    draw_cells('1',0,width,win)
    if flag:
        return
    lawLable = Label(win, text = "current law:" + str(array),font = ("courier", 8))
    lawLable.place(x= 0, y= 0)
    for i in range(gen):
        cells = '0' + cells + '0'
        sums = [cells[n:n+3] for n in range(len(cells)-2)]
        calc = [sum_digits(k) for k in sums ]
        transformed = [array[j] for j in calc]
        cells = ''.join(map(str, transformed))
        draw_cells(cells,i+1,width,win)
        if flag:
            return
        cells = '0' + cells + '0'
        win.update()
        sleep(0.01)
        if i >= 36 and i <= 99:
            classer.append(cells)
        if i == 99:
            if flag:
                return
            lable = classify_automaton(classer, win)
            extra_flag = True
    if extra_flag:
        if flag:
            return
        win.update()
        mylable = lable.cget("text")
        win.after(1000,lable.destroy())
        return mylable

def auto_run(win, width):
    kind_counter = {"boring":0,"interesting":0,"chaotic":0}
    for j in range(0,2187):
        array = [int(i) for i in int2base(j,3)]
        array.reverse()
        x  = 7-len(array)
        while x > 0:
            array.append(0)
            x = x-1
        # array.reverse()
        kind = automat_calc(array,width,win, 100)
        if kind:
            kind_counter[kind] +=1
        if flag:
            return
        win.after(0,win.update())
        if flag:
            return
        win.delete(ALL)
        if flag:
            return
        win.update()
        win.after(200,win.update())
        array.clear()
    print(kind_counter)

def user_run(array,width,win, gen):
    automat_calc(array,width,win, gen)

def classify_automaton(classes, win):
    sign = False
    if flag:
            return
    classified = ""
    sub_arr = []
    for cells in classes:
        sub_arr += [(cells)[:(int(len(cells)/2)+10)-15]]
    first = sub_arr[0]
    sub_arr.remove(sub_arr[0])
    
    for k in range(len(sub_arr)-1):
        if first in sub_arr[k] and k < 7:
            classified =("boring")
            sign = True
            break
        elif first in sub_arr[k] and k>=7:
            classified =("interesting")
            sign = True
            break
    if not sign:
        classified =("chaotic")
    if flag:
        return
    label = Label(win, text = classified,font = ("courier", 32))
    label.place(x=25,y=100)
    return label

def main():
    global root
    width = 1280
    height = 720
    win = Canvas(root ,width = width,height = height)
    win.pack()
    win.configure(background = "white")

    autoB = Button(win, text = "automatic mode", command = lambda: auto_run(win, width))
    autoB.place(x = width/2 -150, y = 0)
   
    manualB = Button(win, text = "manual mode", command = lambda: entering_array(win, width))
    manualB.place(x = width/2 +50, y = 0)

    
main()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()