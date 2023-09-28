from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from .bf1motto import get_motto
import logging

vehicle_key = ["","种类：","击杀：","KPM：","摧毁：","驾龄(h)："]

def VehicleStat(name,user_id):
    data = Vehicle(name=name)
    if(data==None):
        return False
    #头像
    avatar_url = data["avatar"]
    top_14_vehicles=[]
    data["vehicles"]=sorted(data["vehicles"], key=lambda x: x["kills"], reverse=True)
    top_14_vehicles = data["vehicles"][:14]
    ImageVehicle(name,top_14_vehicles,avatar_url,user_id=user_id)

def Vehicle(name):
    url = "https://api.gametools.network/bf1/vehicles/"
    params = {
        "lang":"zh-tw",
        "platform": "pc",
        "name": name
    }
     # 发送GET请求
    response = requests.get(url, params=params)
    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应的JSON数据
        data = response.json()
        # 在这里可以处理数据，例如打印它或进行其他操作
        logging.info(f"成功获取玩家{name}的载具数据")
        return data
    else:
        logging.info("请求失败，状态码:", response.status_code)
        return None

def ImageVehicle(name,data,avatar_url,user_id):
    big_image_url = "https://moe.jitsu.top/img/?sort=1080p&size=mw1024"
    response = requests.get(big_image_url)
    big_image = Image.open(BytesIO(response.content))

    ##头像
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content))
    avatar = avatar.resize((104,104))

    #放置灰色head框
    rectangle = Image.new('RGBA', (big_image.width, big_image.height), (128, 128, 128, 0))
    # 创建绘图对象
    draw = ImageDraw.Draw(rectangle)
    # 在新图像上绘制矩形
    rectangle_width = big_image.width - 2 * 15
    rectangle_left = 15
    rectangle_top = 10
    #head的矩形
    draw.rectangle([rectangle_left, rectangle_top, rectangle_left + rectangle_width-169, rectangle_top + 520],
                fill=(128, 128, 128, 179)) 
    #右边矩形
    draw.rectangle([rectangle_left + rectangle_width-154, rectangle_top, big_image.width-20, rectangle_top + 520],
                fill=(128, 128, 128, 179)) 
    #底部的矩形
    draw.rectangle([rectangle_left,big_image.height-5-30,big_image.width-20,big_image.height-5],
                fill=(128, 128, 128, 179))
    
    result_image = Image.alpha_composite(big_image.convert('RGBA'), rectangle)
    

    # 将头像粘贴到header框上
    avatar_left = rectangle_left + rectangle_width-149
    avatar_top = 15
    result_image.paste(avatar,(avatar_left,avatar_top))
    #书写ID 
    draw = ImageDraw.Draw(result_image)
    vehicle_font = ImageFont.truetype("./data/text.ttf",size=16)
    text_color = (255,255,255)
    nmaePosition=(rectangle_left + rectangle_width-149,122)
    nameText = "ID:"+name
    draw.text(nmaePosition, text=nameText, fill=text_color, font=vehicle_font)
    #感谢
    thanks_font = ImageFont.truetype("./data/text.ttf",size=16)
    thanks_text = "感谢gametools.network提供的API支持"
    draw.text((360,545), text=thanks_text, fill=text_color, font=thanks_font)
    #书写座右铭
    motto_text = get_motto(user_id)
    if motto_text != False:
        motto_font = ImageFont.truetype('./data/text2.ttf',size=22)
        text_len = len(motto_text)
        x = big_image.width-90
        y = 150
        index = 0
        if text_len>=12:
            for char in motto_text:
                if char == '，' or char == '。':
                    y-=10
                if (char > 'a' and char < 'z') or (char > 'A' and char <'Z'):
                    x+=4
                if index >= text_len/2:
                    x = big_image.width-122
                    y = 194 + (index-text_len/2)*26
                draw.text((x,y),text=char,fill=(255,255,255),font=motto_font)
                if (char >= 'a' and char <= 'z') or (char >= 'A' and char <='Z'):
                    x-=4
                y+=26
                index = index + 1
        else:
            for char in motto_text:
                x = big_image.width-105
                if char == '，' or char == '。':
                    y-=10
                if (char >= 'a' and char <= 'z') or (char >= 'A' and char <='Z'):
                    x+=4
                draw.text((x,y),text=char,fill=(255,255,255),font=motto_font)
                if (char >= 'a' and char <= 'z') or (char > 'A' and char <='Z'):
                    x-=4
                y+=26
            
    
    #载具图片遍历
    for i in range(14):
        vehicle_image_url = data[i]["image"]
        response = requests.get(vehicle_image_url)
        vehicle_image = Image.open(BytesIO(response.content))
        vehicle_image = vehicle_image.resize((163,41))
        vehicle_left = 20
        top = 25+i*72
        if i>=7:
            vehicle_left = 420
            top = 30+(i-7)*72
        result_image.paste(vehicle_image,(int(vehicle_left),top),vehicle_image)

    #书写载具数据   
    ##设置字体格式
    vehicle_font = ImageFont.truetype("./data/text2.ttf",size=10)
    text_color = (255,255,255)
    #载具数据遍历
    for i in range(14):
        vehicle_value = []
        vehicle_value = StatsVehicleValue(data[i])
        #载具数据基础位置
        position_map = {0: (185, 28),
                        1: (320, 28),
                        2: (185, 42),
                        3: (320, 42),
                        4: (185, 56),
                        5: (320, 56),}
        
        for j in range(6):
            text = vehicle_key[j]+":"+str(vehicle_value[j])
            if j in position_map:
                x,y=position_map[j]
                if i>=7:
                    x = x+400
                    position = (x,y+(i-7)*72)
                else:
                    position = (x,y+i*72)
            draw.text(position, text=text, fill=text_color, font=vehicle_font)
    result_image.save(f"{name}_vehicle.png")

#vehicle_key = ["","种类","击杀","KPM","摧毁","驾龄"]
def StatsVehicleValue(data):
    vehicle_value = []
    vehicle_value.append(data["vehicleName"])
    vehicle_value.append(data["type"])
    vehicle_value.append(data["kills"])
    vehicle_value.append(data["killsPerMinute"])
    vehicle_value.append(data["destroyed"])
    vehicle_value.append(data["timeIn"]//60//60)

    return vehicle_value


# names=["anshaos","zi_feng_0109","IJN-Shokaku","LMCYI"]
# names1=["zi_feng_0109"]
# for name in names1:
#     VehicleStat(name=name,user_id='669667780')