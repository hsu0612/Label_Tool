import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import glob
import os
import numpy as np
import json
import cv2

# data path
tracking_path = "D:/table_tennis/table_tennis_game_label/human_tracking/"
image_path = "D:/table_tennis/table_tennis_game_img/Fan_Zhendong_vs_Jeoung_Youngsik_2019_ITTF_Korea_14/"
path_w = "D:/table_tennis/"

def draw_one_alphapose(frame, oneResult, format='coco'):
    if format == 'coco':
        l_pair = [(0, 1), (0, 2), (1, 3), (2, 4),  # Head
            (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),(17, 11), (17, 12),  # Body
            (11, 13), (12, 14), (13, 15), (14, 16)]
        p_color = [(0, 255, 255),(0, 191, 255),(0, 255, 102),(0, 77, 255), (0, 255, 0), 
                   #Nose, LEye, REye, LEar, REar
                  (77,255,255),(77, 255, 204), (77,204,255), (191, 255, 77), (77,191,255), (191, 255, 77), 
                   #LShoulder, RShoulder, LElbow, RElbow, LWrist, RWrist
                  (204,77,255),(77,255,204), (191,77,255), (77,255,191), (127,77,255), (77,255,127), (0, 255, 255)] 
                   #LHip, RHip, LKnee, Rknee, LAnkle, RAnkle, Neck
        line_color = [(0, 215, 255), (0, 255, 204), (0, 134, 255), (0, 255, 50), 
                    (77,255,222), (77,196,255), (77,135,255), (191,255,77), (77,255,77), 
                    (77,222,255), (255,156,127), 
                    (0,127,255), (255,127,77), (0,77,255), (255,77,36)]
    img = frame
    part_line = {}
    kp_preds = np.array(oneResult)
    # Draw keypoints
    for n in range(len(kp_preds)):
        cor_x, cor_y = int(kp_preds[n, 0]), int(kp_preds[n, 1])
        part_line[n] = (cor_x, cor_y)
        cv2.circle(img, (cor_x, cor_y), 4, p_color[n], -1)
    # Draw limbs
    for i, (start_p, end_p) in enumerate(l_pair):
        if start_p in part_line and end_p in part_line:
            start_xy = part_line[start_p]
            end_xy = part_line[end_p]
            cv2.line(img, start_xy, end_xy, line_color[i], 1)
    
    return img
        
def action_callback(cateNum, cateName):
    try:
        global data
        global data_count
        global action_output
        
        state = True
        
        hand_num = radioValue.get()
        if hand_num == 1:
            hand = "forehand"
        else:
            hand = "backhand"
        if cateNum == 0:
            for i in action_output:
                if i[5] == data_count:
                    action_output.remove(i)
        else:
            for i in action_output:
                if i[5] == data_count:
                    action_output.remove(i)
                    action_output.append([cateNum, cateName, hand_num, hand, data[data_count], data_count])
                    state=False
                    
            if state:
                action_output.append([cateNum, cateName, hand_num, hand, data[data_count], data_count]) 
            
        photo= next(show)
        imgLabel.configure(image=photo)
        
    except:
        print('end')
        root.quit()
    
def previous_action_callback():
    action_callback(0, 'no action')
    previous_do_no_op()
    previous_do_no_op()
        
def ball_callback(cateNum, cateName):
    try:
        global data
        global data_count
        global ball_output
        
        state = True
        
        if cateNum == 0:
            for i in ball_output:
                if i[3] == data_count:
                    ball_output.remove(i)
        else:
            for i in ball_output:
                if i[3] == data_count:
                    ball_output.remove(i)
                    ball_output.append([cateNum, cateName, data[data_count], data_count])
                    state=False
                    
            if state:
                ball_output.append([cateNum, cateName, data[data_count], data_count])
            
        photo= next(show)
        imgLabel.configure(image=photo)
        
    except:
        print('end')
        root.quit()    
        
def previous_ball_callback():
    ball_callback(0, 'no event')
    previous_do_no_op()
    previous_do_no_op()
        
def previous_do_no_op():
    try: 
        global data
        global data_count
        
        # if image is first frame, then break
        if (data_count == 0):
            print('end')
            root.quit()
        # next will +1, so -2  
        data_count -= 2

        photo= next(show)
        imgLabel.configure(image=photo)
    except:
        print('end')
        root.quit()
                           
def next_do_no_op():
    try:
        photo = next(show)
        imgLabel.configure(image=photo)
    except:
        print('end')
        root.quit()
        
def draw_bounding_box(frame, oneResult, name_1, name_2):
    img=frame
    kp_preds = np.array(oneResult)
    h,w,_=img.shape
    minX, minY =w,h
    maxX, maxY =0,0
    for n in range(len(kp_preds)):
        minX = min(kp_preds[n,0], minX)
        minY = min(kp_preds[n,1], minY)
        maxX = max(kp_preds[n,0], maxX)
        maxY = max(kp_preds[n,1], maxY)
    maxX += 1
    maxY += 1
    assert maxX>minX, print('error : maxX<=minX')
    assert maxY>minY, print('error : maxY<=minY')
    cutW=maxX-minX
    cutH=maxY-minY
    minX = int(max(0,minX-0.3*cutW))
    maxX = int(min(w,maxX+0.3*cutW))
    minY = int(max(0,minY-0.3*cutH))
    maxY = int(min(h,maxY+0.3*cutH))

    bb_color = (0, 0, 255)
    cv2.rectangle(img, (minX, minY), (maxX, maxY), bb_color, 2)

    cv2.rectangle(img, (minX, minY - 30), (minX + 300, minY), (255, 255, 255), -1)
    cv2.putText(img, str(name_1) + ", " + str(name_2), (minX, minY), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    return img

def output_sort(x):
    return(int(x[-1]))

def check():

    global data
    global data_len
    global action_output
    global ball_output

    action_1_name_list = []
    action_2_name_list = []
    action_data_list = []
    action_data_index_list = []
    ball_name_list = []
    ball_data_list = []
    ball_data_index_list = []
    
    action_output.sort(key=output_sort)
    ball_output.sort(key=output_sort)

    for i in action_output:
        action_1_name_list.append(i[1])
        action_2_name_list.append(i[3])
        action_data_list.append(i[4])
        action_data_index_list.append(int(i[5]))
    
    for i in ball_output:
        ball_name_list.append(i[1])
        ball_data_list.append(i[2])
        ball_data_index_list.append(int(i[3]))

    have_action = False
    
    action_index = 0
    ball_index = 0

    for i in range(0, data_len, 1):
        
        speed = 50
        
        image_name = data[i]['image_id']
        while len(image_name) < len(os.listdir(image_path)[0]):
            image_name = "0" + image_name
        img = cv2.imread(image_path+image_name)
        
        if len(action_output) != 0:
            try:
                if action_data_index_list[action_index] == i:
                    have_action = True
                    img = draw_bounding_box(img, data[i]['keypoints'], action_1_name_list[action_index], action_2_name_list[action_index])
                    action_index += 1
            except:
                pass
        if len(ball_output) != 0:
            try:
                if ball_data_index_list[ball_index] == i:
                    have_action = True
                    img = draw_bounding_box(img, data[i]['keypoints'], ball_name_list[ball_index], " ")
                    ball_index += 1
            except:
                pass

        if have_action:
            speed = 5000
        have_action = False
        
        cv2.rectangle(img, (50, 30), (250, 60), (0, 0, 255), -1)
        cv2.putText(img, "Press q: quit", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1, cv2.LINE_AA)
        root.after(5, run_video(img))
        index = i
        if cv2.waitKey(speed) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def save():
    with open(path_w+"action_label.json", 'w') as data_file:
        json.dump(action_output, data_file) 
    with open(path_w+"ball_label.json", 'w') as data_file:
        json.dump(ball_output, data_file) 
        
def run_video(img):
    cv2.imshow('frame', img)

def play():

    global data
    global data_count
    global data_len

    for i in range(data_count, data_len, 1):
        image_name = data[i]['image_id']
        while len(image_name) < len(os.listdir(image_path)[0]):
            image_name = "0" + image_name
        img = cv2.imread(image_path+image_name)
        cv2.rectangle(img, (50, 30), (250, 60), (0, 0, 255), -1)
        cv2.putText(img, "Press q: quit", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1, cv2.LINE_AA)
        root.after(20, run_video(img))
        index = i
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

    data_count = index
    
    photo = next(show)
    imgLabel.configure(image=photo)
    
def play2x():

    global data
    global data_count
    global data_len

    for i in range(data_count, data_len, 1):
        image_name = data[i]['image_id']
        while len(image_name) < len(os.listdir(image_path)[0]):
            image_name = "0" + image_name
        img = cv2.imread(image_path+image_name)
        cv2.rectangle(img, (50, 30), (250, 60), (0, 0, 255), -1)
        cv2.putText(img, "Press q: quit", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1, cv2.LINE_AA)
        root.after(10, run_video(img))
        index = i
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

    data_count = index
    
    photo = next(show)
    imgLabel.configure(image=photo)
    
def play4x():

    global data
    global data_count
    global data_len

    for i in range(data_count, data_len, 1):
        image_name = data[i]['image_id']
        while len(image_name) < len(os.listdir(image_path)[0]):
            image_name = "0" + image_name
        img = cv2.imread(image_path+image_name)
        cv2.rectangle(img, (50, 30), (250, 60), (0, 0, 255), -1)
        cv2.putText(img, "Press q: quit", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1, cv2.LINE_AA)
        root.after(5, run_video(img))
        index = i
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

    data_count = index
    
    photo = next(show)
    imgLabel.configure(image=photo)
    
def back():

    global data
    global data_count
    global data_len

    for i in range(data_count, -1, -1):
        image_name = data[i]['image_id']
        while len(image_name) < len(os.listdir(image_path)[0]):
            image_name = "0" + image_name
        img = cv2.imread(image_path+image_name)
        cv2.rectangle(img, (50, 30), (250, 60), (0, 0, 255), -1)
        cv2.putText(img, "Press q: quit", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1, cv2.LINE_AA)
        root.after(20, run_video(img))
        index = i
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    
    data_count = index
    
    photo = next(show)
    imgLabel.configure(image=photo)
    
def back2x():

    global data
    global data_count
    global data_len

    for i in range(data_count, -1, -1):
        image_name = data[i]['image_id']
        while len(image_name) < len(os.listdir(image_path)[0]):
            image_name = "0" + image_name
        img = cv2.imread(image_path+image_name)
        cv2.rectangle(img, (50, 30), (250, 60), (0, 0, 255), -1)
        cv2.putText(img, "Press q: quit", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1, cv2.LINE_AA)
        root.after(10, run_video(img))
        index = i
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    
    data_count = index
    
    photo = next(show)
    imgLabel.configure(image=photo)

def back4x():

    global data
    global data_count
    global data_len

    for i in range(data_count, -1, -1):
        image_name = data[i]['image_id']
        while len(image_name) < len(os.listdir(image_path)[0]):
            image_name = "0" + image_name
        img = cv2.imread(image_path+image_name)
        cv2.rectangle(img, (50, 30), (250, 60), (0, 0, 255), -1)
        cv2.putText(img, "Press q: quit", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1, cv2.LINE_AA)
        root.after(5, run_video(img))
        index = i
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    
    data_count = index
    
    photo = next(show)
    imgLabel.configure(image=photo)
    
def list_init(action_output, ball_output):
    listbox.delete(0, 'end')
    action_output.sort(key=output_sort)
    ball_output.sort(key=output_sort)
    for i in range(0, len(action_output), 1):
        a = str(action_output[i][4]['image_id'][:-4]) + "_" + str(action_output[i][5]) + "_" + str(action_output[i][1]) + "_" + str(action_output[i][3])
        listbox.insert("end", a)
    for i in range(0, len(ball_output), 1):
        b = str(ball_output[i][2]['image_id'][:-4]) + "_" + str(ball_output[i][3]) + "_" + str(ball_output[i][1])
        listbox.insert("end", b)
    
def list_hashing(event):
    global data_count
    
    a = listbox.get(listbox.curselection())
    b = a.split('_')
    c1 = int(b[0])
    c2 = int(b[1])            
    
    data_count = c2 - 1
    
    photo = next(show)
    imgLabel.configure(image=photo)
    
def show_img(tracking_path, image_path):
    
    # parameter
    global data
    global data_list
    global data_count
    data_count = 0
    # length
    global data_len
    data_len = 0
    # state
    global end_state
    end_state = False
    # output 
    global action_output
    action_output = []
    global ball_output
    ball_output = []
    
    if os.path.isfile(path_w+"action_label.json"):
        with open(path_w+"action_label.json", 'r') as data_file:
            action_output = json.load(data_file)
            
    if os.path.isfile(path_w+"ball_label.json"):
        with open(path_w+"ball_label.json", 'r') as data_file:
            ball_output = json.load(data_file)
      
    # read file
    img_list = os.listdir(image_path)

    # init
    with open(tracking_path+"human_tracking_label.json", 'r') as data_file:
        data = json.load(data_file)
    data_len = len(data)
    # read image index in json
    index = int(data[data_count]['image_id'][:-4])

    while True:
        image_name = data[data_count]['image_id']
        while len(image_name) < len(os.listdir(image_path)[0]):
            image_name = "0" + image_name
        image = cv2.imread(image_path+image_name)
        imgKp = draw_one_alphapose(image, data[data_count]['keypoints'])
        imgKp = cv2.resize(imgKp, (640, 360))
        imgKp = Image.fromarray(cv2.cvtColor(imgKp, cv2.COLOR_BGR2RGB))
        imgKp = ImageTk.PhotoImage(imgKp)
            
        list_init(action_output, ball_output)

        yield imgKp
                      
        data_count += 1
        # end
        if data_len == data_count:
            end_state = True
            break
        index = int(data[data_count]['image_id'][:-4]) 
        
        if end_state:
            break
    root.quit()

class Main(tk.Label):
    def __init__(self, master, image, width, height):
        self.master = master

        tk.Label.__init__(self, master, image=image, width=width, height=height)
        self.rclick = RightClick(self.master)
        self.bind('<Button-3>', self.rclick.popup)

class RightClick():
    def __init__(self, master):
        # create a popup menu
        self.aMenu = tk.Menu(master, tearoff=0)
        self.aMenu.add_command(label='Say Hello', command=self.hello)

    def hello(self):
        pass

    def popup(self, event):
        self.aMenu.post(event.x_root, event.y_root)

root = tk.Tk()
root.title('myLabelTool')

#define vars
imgPathVar = tk.StringVar()
imgCountVar = tk.IntVar()
imgNumVar = tk.IntVar()
humanNumVar = tk.IntVar()
humanCountVar = tk.IntVar()
annPathVar = tk.StringVar()

#radio 
radioValue = tk.IntVar()
radioValue.set(1)

#list box
var = tk.StringVar()

#list
listbox = tk.Listbox(root, listvariable=var, width=50, height=30, selectmode='single')
listbox.pack(side=tk.RIGHT, padx = 10)
listbox.bind("<Double-Button-1>", list_hashing)

#show img
frameImg = tk.Frame(root)
show = show_img(tracking_path, image_path)
photo = next(show)
imgLabel = Main(frameImg, image=photo, width=660, height=380)
imgLabel.pack()

#button action
frameButton_action = ttk.Frame(root, width=150, height=800)
frameButton_action.pack_propagate(0)

#button ball
frameButton_ball = ttk.Frame(root, width=150, height=500)
frameButton_ball.pack_propagate(0)

#button video
frameButton_video = ttk.Frame(root, width=500, height=600)
frameButton_video.pack(side=tk.BOTTOM)

style = ttk.Style()

style.configure('red.TButton', font =('calibri', 12, 'bold'), foreground = 'red') 
style.configure('blue.TButton', font =('calibri', 12, 'bold'), foreground = 'blue') 
style.configure('black.TButton', font =('calibri', 12, 'bold'), foreground = 'black') 
style.configure('red.TLabel', font =('calibri', 18, 'bold'), foreground = 'red')
style.configure('blue.TLabel', font =('calibri', 18, 'bold'), foreground = 'blue') 

label_top  = ttk.Label(frameButton_action, text='Action', style = 'red.TLabel', justify="center")
label_top.pack(padx = 5)

label_bottom  = ttk.Label(frameButton_ball, text='Ball', style = 'blue.TLabel', justify="center")
label_bottom.pack(padx = 5)

action_button1 = ttk.Button(frameButton_action, text="發",  command=lambda:action_callback(1,'Serve'), style = 'black.TButton')
action_button1.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button2 = ttk.Button(frameButton_action, text="擺",  command=lambda:action_callback(2,'Drop'), style = 'black.TButton')
action_button2.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button3 = ttk.Button(frameButton_action, text="切",  command=lambda:action_callback(3,'Cut'), style = 'black.TButton')
action_button3.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button4 = ttk.Button(frameButton_action, text="劈",  command=lambda:action_callback(4,'Hack'), style = 'black.TButton')
action_button4.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button5 = ttk.Button(frameButton_action, text="擰",  command=lambda:action_callback(5,'Twist'), style = 'black.TButton')
action_button5.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button6 = ttk.Button(frameButton_action, text="拉",  command=lambda:action_callback(6,'Spin'), style = 'black.TButton')
action_button6.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button7 = ttk.Button(frameButton_action, text="壓",  command=lambda:action_callback(7,'Push'), style = 'black.TButton')
action_button7.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button8 = ttk.Button(frameButton_action, text="挑",  command=lambda:action_callback(8,'Pick'), style = 'black.TButton')
action_button8.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button9 = ttk.Button(frameButton_action, text="殺",  command=lambda:action_callback(9,'Smash'), style = 'black.TButton')
action_button9.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button10 = ttk.Button(frameButton_action, text="擋",  command=lambda:action_callback(10,'Block'), style = 'black.TButton')
action_button10.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button11 = ttk.Button(frameButton_action, text="削",  command=lambda:action_callback(11,'Chop'), style = 'black.TButton')
action_button11.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button12 = ttk.Button(frameButton_action, text="放高球",  command=lambda:action_callback(12,'Lob'), style = 'black.TButton')
action_button12.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button13 = ttk.Button(frameButton_action, text="往前(無動作)", command=lambda:previous_action_callback(), style = 'black.TButton')
action_button13.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button14 = ttk.Button(frameButton_action, text="往後(無動作)", command=lambda:action_callback(0, 'no action'), style = 'black.TButton')
action_button14.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button15 = ttk.Button(frameButton_action, text="往前", command=lambda:previous_do_no_op(), style = 'black.TButton')
action_button15.pack(fill=tk.BOTH, expand=1, pady = 2)
action_button16 = ttk.Button(frameButton_action, text="往後", command=lambda:next_do_no_op(), style = 'black.TButton')
action_button16.pack(fill=tk.BOTH, expand=1, pady = 2)

ball_button1 = ttk.Button(frameButton_ball, text="反手短",  command=lambda:ball_callback(1,'Short backhand'), style = 'black.TButton')
ball_button1.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button2 = ttk.Button(frameButton_ball, text="中路偏反手短",  command=lambda:ball_callback(2,'Short backhand in the middle'), style = 'black.TButton')
ball_button2.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button3 = ttk.Button(frameButton_ball, text="中路偏正手短",  command=lambda:ball_callback(3,'Short forehand in the middle'), style = 'black.TButton')
ball_button3.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button4 = ttk.Button(frameButton_ball, text="正手短",  command=lambda:ball_callback(4,'Short forehand'), style = 'black.TButton')
ball_button4.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button5 = ttk.Button(frameButton_ball, text="反手長",  command=lambda:ball_callback(5,'Long backhand'), style = 'black.TButton')
ball_button5.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button6 = ttk.Button(frameButton_ball, text="中路長",  command=lambda:ball_callback(6,'Long in the middle'), style = 'black.TButton')
ball_button6.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button7 = ttk.Button(frameButton_ball, text="正手長",  command=lambda:ball_callback(7,'Forehand long'), style = 'black.TButton')
ball_button7.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button8 = ttk.Button(frameButton_ball, text="出界",  command=lambda:ball_callback(8,'Out of bounds'), style = 'black.TButton')
ball_button8.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button9 = ttk.Button(frameButton_ball, text="觸網",  command=lambda:ball_callback(9,'Touch net'), style = 'black.TButton')
ball_button9.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button10 = ttk.Button(frameButton_ball, text="往前(無事件)", command=lambda:previous_ball_callback(), style = 'black.TButton')
ball_button10.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button11 = ttk.Button(frameButton_ball, text="往後(無事件)", command=lambda:ball_callback(0, 'no event'), style = 'black.TButton')
ball_button11.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button12 = ttk.Button(frameButton_ball, text="往前", command=lambda:previous_do_no_op(), style = 'black.TButton')
ball_button12.pack(fill=tk.BOTH, expand=1, pady = 2)
ball_button13 = ttk.Button(frameButton_ball, text="往後", command=lambda:next_do_no_op(), style = 'black.TButton')
ball_button13.pack(fill=tk.BOTH, expand=1, pady = 2)

video_Buttonp1 = ttk.Button(frameButton_video, text="play",  command=lambda:play(), style = 'black.TButton')
video_Buttonp1.pack(side=tk.TOP, expand=1, padx = 10, pady = 10)

video_Buttonp2 = ttk.Button(frameButton_video, text="play2x",  command=lambda:play2x(), style = 'black.TButton')
video_Buttonp2.pack(side=tk.TOP, expand=1, padx = 10, pady = 10)

video_Buttonp3 = ttk.Button(frameButton_video, text="play4x",  command=lambda:play4x(), style = 'black.TButton')
video_Buttonp3.pack(side=tk.TOP, expand=1, padx = 10, pady = 10)

video_Buttonb1 = ttk.Button(frameButton_video, text="back",  command=lambda:back(), style = 'black.TButton')
video_Buttonb1.pack(side=tk.TOP, expand=1, padx = 10, pady = 10)

video_Buttonb2 = ttk.Button(frameButton_video, text="back2x",  command=lambda:back2x(), style = 'black.TButton')
video_Buttonb2.pack(side=tk.TOP, expand=1, padx = 10, pady = 10)

video_Buttonb3 = ttk.Button(frameButton_video, text="back4x",  command=lambda:back4x(), style = 'black.TButton')
video_Buttonb3.pack(side=tk.TOP, expand=1, padx = 10, pady = 10)

video_Buttonb4 = ttk.Button(frameButton_video, text="check",  command=lambda:check(), style = 'black.TButton')
video_Buttonb4.pack(side=tk.TOP, expand=1, padx = 10, pady = 10)

video_Buttonb5 = ttk.Button(frameButton_video, text="save",  command=lambda:save(), style = 'black.TButton')
video_Buttonb5.pack(side=tk.TOP, expand=1, padx = 10, pady = 10)

#radio
frameradio = ttk.Frame(root, width=100, height=100)
frameradio.pack_propagate(0)

rdioOne = tk.Radiobutton(frameradio, text='正手',
                             variable=radioValue, value=1) 
rdioTwo = tk.Radiobutton(frameradio, text='反手',
                             variable=radioValue, value=2) 

rdioOne.pack(side=tk.TOP, padx = 5)
rdioTwo.pack(side=tk.TOP, padx = 5)

frameButton_video.pack(side=tk.LEFT)
frameImg.pack(side=tk.LEFT)
frameButton_ball.pack(side=tk.RIGHT, padx = 5)
frameButton_action.pack(side=tk.RIGHT, padx = 5)
frameradio.pack(side=tk.RIGHT, padx = 5)

#start
root.mainloop()