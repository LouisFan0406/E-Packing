from pywebio import start_server
from pywebio.input import input, FLOAT
from pywebio.output import put_text,put_image
from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()


def E_Packing():
    put_text("歡迎使用易包貨！")
    while True:
        n = int(input("商品共有幾項："))
        list1 = []
        list_max=[]
        total_v = 0
        for j in range(n):
            list1.append([])
        for i in range(n):
            width = float(input("商品寬度:"))
            length = float(input("商品長度:"))
            height = float(input("商品高度:"))
            qaulity = float(input("商品個數:"))
            volume = width * length * height
            list1[i].append(width)
            list1[i].append(length)
            list1[i].append(height)
            list1[i].append(volume)
            list1[i].append(qaulity)
            total_v = total_v+volume
            list_max.append(max(tuple(list1[i][0:3])))

        list_color = ['red','blue','orange','lawngreen','purple','lawngreen','yellow','gray','pink','brown','cyan','olive','darkgreen','orange']

        #判別要用什麼箱子

        if total_v<4500:
            if max(list_max)<25:
                put_text("使用一號箱")
                box_size = (25, 18, 10)
            elif max(list_max)<32:
                put_text("使用二號箱")
                box_size = (32, 25, 15)
            elif max(list_max) < 35:
                put_text("使用三號箱")
                box_size = (35, 26, 16)
            elif max(list_max) < 50:
                put_text("使用五號箱")
                box_size = (50, 35, 35)
            else:
                put_text("使用特規箱")
                box_size = (100, 100, 100)
        elif 4500 < total_v < 12000:
            if max(list_max)<32:
                put_text("使用二號箱")
                box_size = (32, 25, 15)
            elif max(list_max) < 35:
                put_text("使用三號箱")
                box_size = (35, 26, 16)
            elif max(list_max) < 50:
                put_text("使用五號箱")
                box_size = (50, 35, 35)
            else:
                put_text("使用特規箱")
                box_size = (100, 100, 100)
        elif 12000 < total_v < 14560 :
            if max(list_max) < 35:
                put_text("使用三號箱")
                box_size = (35, 26, 16)
            elif max(list_max) < 50:
                put_text("使用五號箱")
                box_size = (50, 35, 35)
            else:
                put_text("使用特規箱")
                box_size = (100, 100, 100)
        elif 14560 < total_v < 36750:
            if max(list_max) < 35:
                put_text("使用四號箱")
                box_size = (35, 30, 35)
            elif max(list_max) < 50:
                put_text("使用五號箱")
                box_size = (50, 35, 35)
            else:
                put_text("使用特規箱")
                box_size = (100, 100, 100)
        elif 36750 < total_v < 61250:
            if max(list_max) < 50:
                put_text("使用五號箱")
                box_size = (50, 35, 35)
            else:
                put_text("使用特規箱")
                box_size = (100, 100, 100)
        else:
            put_text("請使用特殊規格箱")
            box_size = (100,100,100)
        # init packing function
        packer = Packer()
        #  init bin
        # box_ = (box_length, box_winth, box_height)
        box = Bin('example1', box_size, 70.0, 0, 0)

        packer.addBin(box)
        #  add item

        for i in range(n):
            packer.addItem(Item(i, i, 'cube', tuple(list1[i][0:3]), 1, 1, 100, True,list_color[i] ))
            if list1[i][-1] > 1:
                for j in range(int(list1[i][-1]) -1):
                    packer.addItem(Item(i, i, 'cube', tuple(list1[i][0:3]), 1, 1, 100, True,list_color[i] ))


        # calculate packing
        packer.pack(bigger_first=True,distribute_items=False,fix_point=True,number_of_decimals=0)

        # put_text result
        b = packer.bins[0]
        volume = b.width * b.height * b.depth
        put_text(":::::::::::", b.string())

        # put_text("FITTED ITEMS:")
        volume_t = 0
        volume_f = 0
        unfitted_name = ''
        for item in b.items:
            volume_t += float(item.width) * float(item.height) * float(item.depth)
        for item in b.unfitted_items:
            volume_f += float(item.width) * float(item.height) * float(item.depth)
            unfitted_name += '{},'.format(item.partno)
        put_text("***************************************************")
        put_text('空間利用率 : {}%'.format(round(volume_t / float(volume) * 100 ,2)))
        put_text('空間剩餘量 : ', float(volume) - volume_t )
        put_text('沒裝進的貨物 : ',unfitted_name)
        put_text('沒裝進的貨物體積 : ',volume_f)
        put_text("重力分布 : ",b.gravity)
        stop = time.time()
        put_text('使用時間 : ',stop - start)

        # draw results
        painter = Painter(b)
        result = painter.plotBoxAndItems()
        put_image(result, width='50px')
        answer = input("要輸入下個商品嗎:?(Y/N)")
        if answer == "Y":
            continue
        if answer == "N":
            put_text("感謝您的使用，下次再見")
            break

if __name__ == '__main__':
    start_server(E_Packing, port=80)