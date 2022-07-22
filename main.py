import math
import sys
import time
import torch
import win32api
import win32con
import win32gui
from PyQt5.QtWidgets import QApplication
from pynput.mouse import Controller
import mouse


class Point():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Line(Point):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)

    def getlen(self):
        changdu = math.sqrt(math.pow((self.x1 - self.x2), 2) +
                            math.pow((self.y1 - self.y2), 2))
        return changdu


# 获取窗口句柄
hwnd = 3084854
print(hwnd)
# hwnd = win32gui.FindWindow(None, "csgo")
#hwnd = win32gui.GetDesktopWindow()

# 截图完毕后保存在根目录的cfbg.bmp文件
def screen_record():
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save("cfbg.bmp")


device = torch.device("cuda")
model = torch.hub.load('yolov5', 'custom', 'yolov5/exp/weights/last.pt',source='local', force_reload=False)  # 加载本地模型
l2, t2, r2, b2 = win32gui.GetClientRect(3084854)
game_width =b2-t2  
game_height =r2-l2
print(game_width,game_height) 

while True:
    # 截取屏幕
    screen_record()
    # 使用模型
    model = model.to(device)
    img = 'cfbg.bmp'
    # 开始推理
    results = model(img)
    # results.show()
    # 过滤模型
    xmins = results.pandas().xyxy[0]['xmin']
    ymins = results.pandas().xyxy[0]['ymin']
    xmaxs = results.pandas().xyxy[0]['xmax']
    ymaxs = results.pandas().xyxy[0]['ymax']
    class_list = results.pandas().xyxy[0]['class']
    confidences = results.pandas().xyxy[0]['confidence']
    newlist = []
    for xmin, ymin, xmax, ymax, class_item, conf in zip(xmins, ymins, xmaxs, ymaxs, class_list, confidences):
        if class_item == 0 and conf > 0.5:
            newlist.append([int(xmin), int(ymin), int(xmax), int(ymax), conf])
    # 循环遍历每个敌人的坐标信息传入距离计算方法获取每个敌人距离鼠标的距离
    if len(newlist) > 0:
        # 存放距离数据
        cdList = []
        xyList = []
        for listItem in newlist:
            # 当前遍历的人物中心坐标
            # xindex = int((listItem[2]+listItem[0])/2)
            # yindex = int((listItem[3]+listItem[1])/2)
            xindex = int(listItem[2] - (listItem[2] - listItem[0]) / 2)
            yindex = int(listItem[3] - (listItem[3] - listItem[1]) / 2)
            print(xindex, yindex)
            mouseModal = Controller()
            x, y = mouseModal.position
            # print("x,y:",x,y)
            # print("width,height:",int(game_width/2),(game_height/2))
            # print(xindex,yindex)
            # mouseModal.move=(xindex-x,yindex-y)
            L1 = Line(x, y, xindex, yindex)
            mouseModal.position=(xindex,yindex)
            # 获取到距离并且存放在cdList集合中
            cdList.append(int(L1.getlen()))
            xyList.append([xindex, yindex, listItem[0],listItem[1], listItem[2], listItem[3]])
        # 这里就得到了距离最近的敌人位置了
        minCD = min(cdList)
        if minCD < 150000:
            for cdItem, xyItem in zip(cdList, xyList):
                if cdItem == minCD:
                    # 按下一次鼠标左键，程序移动鼠标
                    if win32api.GetAsyncKeyState(0x01):
                        #  win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(xyItem[0] - game_width // 2),int(xyItem[1] - (game_height - (xyItem[3] - xyItem[5])) // 2), 0, 0)
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(xyItem[0] - x),int(xyItem[1]-y), 0, 0)
                        x,y=mouseModal.position
	                    # win32api.SetCursorPos((int(xyItem[0]-x), int(xyItem[1]-y)))
                    break
#句柄扫描
# import win32gui
# hwnd_title = dict() 
# def get_all_hwnd(hwnd,mouse):
#     if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
#         hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
# win32gui.EnumWindows(get_all_hwnd, 0)

# for h,t in hwnd_title.items():
#     if t is not "":
#         print(([h], [t]))
