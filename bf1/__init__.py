from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Message,GroupMessageEvent
import re
from .bf1Stat import search_value_in_bfbd,Stats,append_to_bfbd
from .bf1Vehicle import VehicleStat
from .bf1Weapon import WeaponStat
from .bf1motto import add_motto
from .bf1server import ServerStat
from pathlib import Path
import logging

current_dir = Path.cwd()
logging.basicConfig(filename='bf1bot.log', level=logging.INFO)

stat = on_command("stat", priority=10, block=True)
bd = on_command("bd",priority=10, block=True)
weapon = on_command("weapon",priority=10,aliases={'武器','w'},block=True)
vehicle = on_command("vehicle",priority=10,aliases={'载具','v'},block=True)
weapon = on_command("weapon",priority=10,aliases={'武器','w'},block=True)
motto = on_command("座右铭",priority=10,aliases={'motto'},block=True)
server = on_command("服务器",priority=10,aliases={"server","f"},block=True)
bf1help = on_command("bfhelp",priority=10,aliases={"战地1帮助","机器人帮助"},block=True)

@stat.handle()
async def stat_handle(foo: GroupMessageEvent):
    name=foo.get_message()
    user_id = foo.get_user_id()
    key_id=str(user_id)
    name=str(name)
    if(name=="/stat"):
        result = search_value_in_bfbd(key_id)
        if result ==None:
            await stat.finish(Message("本地绑定文件不存在，已创建，请先绑定"))
        elif result == False:
            await stat.finish(Message("请先绑定id，指令/bd+\" \"+ID"))
        else:
            name = result
    else:
        name = re.sub(r'^/stat\s*', '', name)
    StatsResult = Stats(name)
    if StatsResult == False:
        await stat.finish(Message("未查找到此ID"))
    image_path = current_dir / f"{name}.png"
    message1=MessageSegment.image(image_path.as_uri())
    message2=MessageSegment.at(user_id=user_id)
    message_all=message1+message2
    await stat.send(message_all)

    file_name = f"{name}.png"
    # 创建文件路径对象
    file_path = Path("./", file_name)
    # 使用unlink()方法删除文件
    try:
        file_path.unlink()
        logging.info(f"文件 '{file_path}' 删除成功")
    except FileNotFoundError:
        logging.info(f"文件 '{file_path}' 不存在")
    except Exception as e:
        logging.info(f"删除文件时出现错误: {str(e)}")

@bd.handle()
async def bd_handle(foo: GroupMessageEvent):
    name = foo.get_message()
    name = str(name)
    name = re.sub(r'^/bd\s*', '', name)
    user_id = foo.get_user_id()
    user_id = str(user_id)
    result = append_to_bfbd(user_id,name)
    if result == True:
        await bd.finish(Message("绑定成功"))
    else:
        await bd.finish(Message("绑定失败，请联系bot作者"))

@vehicle.handle()
async def vehicle_handle(foo: GroupMessageEvent):
    name=foo.get_message()
    user_id = foo.get_user_id()
    key_id=str(user_id)
    name=str(name)
    if name=="/v" or name=='/载具' or name=='/vehicle':
        result = search_value_in_bfbd(key_id)
        if result ==None:
            await vehicle.finish(Message("本地绑定文件不存在，已创建，请先绑定"))
        elif result == False:
            await vehicle.finish(Message("请先绑定id，指令/bd+\" \"+ID"))
        else:
            name = result
    else:
        name = name.split()[1]
    VehicleResult = VehicleStat(name=name,user_id=key_id)
    if VehicleResult == False:
        await vehicle.finish(Message("请求失败，请重新查询，可能是此ID有误"))
    image_path = current_dir / f"{name}_vehicle.png"
    message1=MessageSegment.image(image_path.as_uri())
    message2=MessageSegment.at(user_id=user_id)
    message_all=message1+message2
    await vehicle.send(message_all)

    file_name = f"{name}_vehicle.png"
    # 创建文件路径对象
    file_path = Path("./", file_name)
    try:
        file_path.unlink()
        logging.info(f"文件 '{file_path}' 删除成功")
    except FileNotFoundError:
        logging.info(f"文件 '{file_path}' 不存在")
    except Exception as e:
        logging.info(f"删除文件时出现错误: {str(e)}")

@weapon.handle()
async def weapon_handle(foo: GroupMessageEvent):
    name=foo.get_message()
    user_id = foo.get_user_id()
    key_id=str(user_id)
    name=str(name)
    if name=="/w" or name=='/武器' or name=='/weapon':
        result = search_value_in_bfbd(key_id)
        if result ==None:
            await weapon.finish(Message("本地绑定文件不存在，已创建，请先绑定"))
        elif result == False:
            await weapon.finish(Message("请先绑定id，指令/bd+\" \"+ID"))
        else:
            name = result
    else:
        name = name.split()[1]
    WeaponResult = WeaponStat(name=name,user_id=key_id)
    if WeaponResult == False:
        await weapon.finish(Message("请求失败，请重新查询，可能是此ID有误"))
    image_path = current_dir / f"{name}_weapon.png"
    message1=MessageSegment.image(image_path.as_uri())
    message2=MessageSegment.at(user_id=user_id)
    message_all=message1+message2
    await weapon.send(message_all)
    file_name = f"{name}_weapon.png"
    # 创建文件路径对象
    file_path = Path("./", file_name)
    try:
        file_path.unlink()
        logging.info(f"文件 '{file_path}' 删除成功")
    except FileNotFoundError:
        logging.info(f"文件 '{file_path}' 不存在")
    except Exception as e:
        logging.info(f"删除文件时出现错误: {str(e)}")

@motto.handle()
async def motto_handle(foo: GroupMessageEvent):
    text = str(foo.get_message())
    text = text.split()[1]
    user_id = str(foo.get_user_id())
    result=add_motto(key=user_id,value=text)
    if result ==True:
        await motto.finish(Message(f"座右铭'{text}'已经成功绑定！\n注：座右铭不能包含空格，如果有误，重新绑定座右铭即可直接修改。"))
    else:
        await motto.finish(Message("绑定座右铭失败，请重新绑定或者联系bot作者。"))
    
@server.handle()
async def server_handle(foo: GroupMessageEvent):
    name = str(foo.get_message())
    name = name.split()[1]
    user_id = str(foo.get_user_id())
    message=""
    Server_list = ServerStat(name=name)
    index = 0
    if Server_list == False:
        await server.finish(Message("请求失败，可能是网络问题或服务器ID错误，肯定不是程序问题！"))
    else:
        for servers in Server_list:
            message = message + servers + "\n"
            index +=1
            if index % 9 == 0:
                message = message + "\n"
        await server.finish(Message(message))
    
@bf1help.handle()
async def  bf1help_handle():
    await bf1help.finish(MessageSegment.image("https://img1.imgtp.com/2023/09/28/USZQG8hH.png"))
