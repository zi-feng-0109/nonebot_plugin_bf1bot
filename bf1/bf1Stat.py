from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import random
import os
import json
import logging


    ##设置text_key
text_key = ["ID","等级","代表战排","KD","KPM","SPM","胜率",
            "最佳兵种","命中率","爆头率",
            "爆头数","游戏时长(h)",
            "击杀","死亡","胜利",
            "失败","最远爆头","最高连杀",
            "复仇击杀","救援击杀","治疗","修复","协助击杀"]

weapon_key = ["","种类：","使用时长(h)：","击杀：","KPM：","命中率：","爆头率：","效率："]
vehicle_key = ["","种类：","击杀：","KPM：","摧毁：","驾龄(h)："]

def Stats(name):
    data = PlayerStats(name=name)
    if data == None:
        return False
    isHacker = CheckBan(names=name)
    #获取前五武器数据
    top_5_weapons=[]
    data["weapons"]=sorted(data["weapons"], key=lambda x: x["kills"], reverse=True)
    top_5_weapons = data["weapons"][:5]
    #获取前五载具数据
    top_5_vehicles=[]
    data["vehicles"]=sorted(data["vehicles"], key=lambda x: x["kills"], reverse=True)
    top_5_vehicles = data["vehicles"][:5]
    ImageStats(data,top_5_weapons,top_5_vehicles)
    logging.info(isHacker)
    if isHacker:
        KillMother(name=name)



#制作hacker图标
def KillMother(name):
    hacker_url = "https://img1.imgtp.com/2023/09/28/MiyOJBGY.png"
    response = requests.get(hacker_url)
    image1 = Image.open(BytesIO(response.content))
    image2 = Image.open(f'{name}.png')
    image1.resize((400,400))
    image1 = image1.convert(image2.mode)

    opacity = 0.6
    x_range = (100, 600)
    y_range = (50, 175)
    x_position = random.randint(x_range[0], x_range[1])
    y_position = random.randint(y_range[0], y_range[1])
    image2.paste(image1, (x_position, y_position), image1)
    #image2.putalpha(int(80 * opacity))
    os.remove(f'{name}.png')
    image2.save(f'{name}.png')
    image1.close()
    image2.close()


#请求获得玩家全部基础数据信息
def PlayerStats(name):
    url="https://api.gametools.network/bf1/all/"
    params = {
        "format_values":"true",
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
        logging.info(f"成功获取玩家{name}的数据")
        return data
    else:
        logging.info("请求失败，状态码:", response.status_code)
        return None

#查是否是hacker
def CheckBan(names):
    # 发起API请求
    url = "https://api.gametools.network/bfban/checkban"
    params = {
        "names": names
    }
    response = requests.get(url, params=params)

    # 提取"hacker"属性的值
    data = response.json()
    names = names.lower()
    if data["names"][names]["hacker"]:
        hacker_value = data["names"][names]["hacker"];
        return hacker_value
    else:
        return None

#制作Stat图像
def ImageStats(data,top_5_weapons,top_5_vehicles):
    big_image_url = "https://moe.jitsu.top/img/?sort=1080p&size=mw1024"
    response = requests.get(big_image_url)
    big_image = Image.open(BytesIO(response.content))

    #放置灰色head框
    rectangle = Image.new('RGBA', (big_image.width, big_image.height), (128, 128, 128, 0))
    # 创建绘图对象
    draw = ImageDraw.Draw(rectangle)
    # 在新图像上绘制矩形
    rectangle_width = big_image.width - 2 * 15
    rectangle_left = 15
    rectangle_top = 10
    #head的矩形
    draw.rectangle([rectangle_left, rectangle_top, rectangle_left + rectangle_width, rectangle_top + 124],
                fill=(128, 128, 128, 179))  
    #下放左边矩形
    rectangle2_width = (rectangle_width-10)/2
    rectangle2_top = 144
    draw.rectangle([rectangle_left, rectangle2_top, rectangle_left + rectangle2_width, rectangle_top + 520],
                fill=(128, 128, 128, 179)) 
    #下方右边矩形
    draw.rectangle([rectangle_left+rectangle2_width+10, rectangle2_top, big_image.width-15, rectangle_top + 520],
                fill=(128, 128, 128, 179))  
    #最下方矩形
    draw.rectangle([rectangle_left,big_image.height-5-30,big_image.width-15,big_image.height-5],
                fill=(128, 128, 128, 179))
    # 将新图像粘贴到底图上
    result_image = Image.alpha_composite(big_image.convert('RGBA'), rectangle)

    #获取战队头像并拼接
    if data["activePlatoon"]["emblem"]:
        avatar_url = data["activePlatoon"]["emblem"]
    else:
        avatar_url = data["avatar"]
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content))
    avatar = avatar.resize((104,104))

    #avatar.save("test.png")
    # 将头像粘贴到header框上
    avatar_left = 25
    avatar_top = 20
    try:
        result_image.paste(avatar,(avatar_left,avatar_top),avatar)
    except Exception as e:
        logging.info(f"抛出异常{e}")
        result_image.paste(avatar,(avatar_left,avatar_top))

    #书写玩家数据信息
    draw = ImageDraw.Draw(result_image)
    ##设置字体格式
    font = ImageFont.truetype("./data/text.ttf",size=20)
    text_color = (0,0,0)


    text_value=StatsText(data)
    for i in range(23):
        text = text_key[i]+":"+"\t"+str(text_value[i])
        if i==0:
            position = (147,22)
        elif i==1:
            position = (487,22)
        elif i==2:
            position = (657,22)
        elif i<8:
            position = (147+170*(i-3),41)
            if (i==3 or i==4):
                text_color = (255,255,255)
        elif i<13:
            position = (147+170*(i-8),61)
        elif i<18:
            position = (147+170*(i-13),80)
        else:
            position = (147+170*(i-18),98)
        #logging.info(f"成功写入{i}:{text}")
        draw.text(position, text=text, fill=text_color, font=font)
        text_color = (0, 0, 0)


    rectangle_coordinates = (140, 20, 1002, 124)
    # 绘制矩形框
    border_width = 2  # 框的宽度
    border_color = (0, 0, 0)  # 框的颜色，这里为黑色
    draw.rectangle(rectangle_coordinates, outline=border_color, width=border_width)

    #拼接前五武器
    for i in range(5):

        weapon_image_url = top_5_weapons[i]["image"]
        vehicle_image_url = top_5_vehicles[i]["image"]
        response = requests.get(weapon_image_url)
        response1 = requests.get(vehicle_image_url)
        weapon_image = Image.open(BytesIO(response.content))
        vehicle_image = Image.open(BytesIO(response1.content))
        weapon_image = weapon_image.resize((204,51))
        vehicle_image = vehicle_image.resize((204,51))
        weapon_left = 20
        vehicle_left = rectangle_left+rectangle2_width+15
        top = 154+i*78
        result_image.paste(weapon_image,(int(weapon_left),top),weapon_image)
        result_image.paste(vehicle_image,(int(vehicle_left),top),vehicle_image)
    #武器数据文本

    ##武器数据基础设定
    #书写玩家数据信息
    ##设置字体格式
    weapon_font = ImageFont.truetype("./data/text2.ttf",size=11)
    text_color = (0,0,0)

    #武器数据遍历
    for i in range(5):
        weapon_value = []
        vehicle_value = []
        weapon_value = StatsWeaponValue(top_5_weapons[i])
        vehicle_value = StatsVehicleValue(top_5_vehicles[i])
        #武器用
        position_map = {0: (232, 158),
                        1: (423, 158),
                        2: (232, 173),
                        3: (320, 173),
                        4: (423, 173),
                        5: (232, 188),
                        6: (320, 188),
                        7: (423, 188),}
        #载具用
        position_map1 = {0: (730, 158),
                        1: (917, 158),
                        2: (730, 173),
                        3: (814, 173),
                        4: (917, 173),
                        5: (730, 188),}
        ##填充武器文本
        for j in range(8):
            weapon_text=weapon_key[j]+str(weapon_value[j])
            if j in position_map:
                x, y = position_map[j]
                position = (x, y + i * 78)
            else:
                position = (0, 0)
            if j==3 or j==4:
                text_color = (255,255,255)
            draw.text(position, text=weapon_text, fill=text_color, font=weapon_font)
            text_color = (0,0,0)
        ##填充载具文本
        for k in range(6):
            vehicle_text= vehicle_key[k]+str(vehicle_value[k])
            if k in position_map1:
                x, y = position_map1[k]
                position = (x, y + i * 78)
            else:
                position = (0, 0)  
            if k==2 or k==3:
                text_color = (255,255,255)
            draw.text(position, text= vehicle_text, fill=text_color, font=weapon_font)
            text_color = (0,0,0)         

    #感谢
    thanks_font = ImageFont.truetype("./data/text2.ttf",size=16)
    text_color = (255,255,255)
    thanks_text = "感谢gametools.network提供的API支持"
    draw.text((360,545), text=thanks_text, fill=text_color, font=thanks_font)
    # 保存修改后的图像
    result_image.save(f'{data["userName"]}.png')
    

def StatsText(data):
    # 创建一个空列表来存储数据的值
    text_value = []
    # 添加数据的值到列表中
    if data["activePlatoon"]["tag"]:
        text_value.append("["+data["activePlatoon"]["tag"]+"]"+data["userName"])
    else:
        text_value.append(data["userName"])  # 用户名字
    text_value.append(data["rank"])  # 用户等级
    if data["activePlatoon"]["name"]:
        text_value.append(data["activePlatoon"]["name"])
    else:
        text_value.append("无")  # 代表战排
    text_value.append(data["killDeath"])      # 击杀/死亡比率
    text_value.append(data["killsPerMinute"])  # 每分钟击杀数
    text_value.append(data["scorePerMinute"])  # 每分钟得分
    text_value.append(data["winPercent"])  # 胜率
    text_value.append(data["bestClass"])  # 最佳职业
    text_value.append(data["accuracy"])  # 击中率
    text_value.append(data["headshots"])  # 爆头率
    text_value.append(data["headShots"])  # 爆头数
    text_value.append((data["secondsPlayed"]//60)//60)  # 游戏时间（小时）
    text_value.append(data["kills"])  # 击杀数
    text_value.append(data["deaths"])  # 死亡数
    text_value.append(data["wins"])  # 胜利数
    text_value.append(data["loses"])  # 失败数
    text_value.append(data["longestHeadShot"])  # 最远爆头距离
    text_value.append(data["highestKillStreak"])  # 最高连杀数
    text_value.append(data["avengerKills"])  # 复仇击杀数
    text_value.append(data["saviorKills"])  # 救援击杀数
    text_value.append(data["heals"])  # 治疗次数
    text_value.append(data["repairs"])  # 修复次数
    text_value.append(data["killAssists"])  # 击杀协助次数 

    return text_value

#weapon_key = ["","种类","使用时长(h)","击杀","KPM","命中率","爆头率","效率"]
def StatsWeaponValue(data):
    weapon_value = []
    weapon_value.append(data["weaponName"])
    weapon_value.append(data["type"])
    weapon_value.append(int(data["timeEquipped"])//60//60)
    weapon_value.append(data["kills"])
    weapon_value.append(data["killsPerMinute"])
    weapon_value.append(data["accuracy"])
    weapon_value.append(data["headshots"])
    weapon_value.append(data["hitVKills"])

    return weapon_value

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

#搜索绑定
def search_value_in_bfbd(search_key):

    bfbd_file = os.path.join("./data", "bfbd.json")  # bfbd.json文件路径
    # 检查bfbd.json文件是否存在
    if os.path.exists(bfbd_file):
        # 读取现有数据
        with open(bfbd_file, "r") as file:
            existing_data = json.load(file)

        # 搜索对应的值
        if search_key in existing_data:
            value = existing_data[search_key]
            return value
        else:
            return False
    else:
        # 如果文件不存在，创建文件并写入初始内容
        with open(bfbd_file, "w") as file:
            file.write("{}")  # 写入初始内容，如空的JSON对象 {}

        return None

#绑定ID
def append_to_bfbd(key, value):
    
    bfbd_file = os.path.join("./data", "bfbd.json")  # bfbd.json文件路径
    # 检查bfbd.json文件是否存在
    if os.path.exists(bfbd_file):
        # 读取现有数据
        with open(bfbd_file, "r") as file:
            existing_data = json.load(file)
        # 添加新的键值对
        existing_data[key] = value
        # 写入更新后的数据回到文件中
        with open(bfbd_file, "w") as file:
            json.dump(existing_data, file, indent=4)
    else:
        # 如果文件不存在，创建文件并写入初始内容，包含新的键值对
        with open(bfbd_file, "w") as file:
            data = {key: value}
            json.dump(data, file, indent=4)
    return True




    

