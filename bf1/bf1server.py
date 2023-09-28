import requests
import logging

server_key=["服务器名", "描述","在线玩家","模式","当前地图","服务器位置","serverId","是否是官服","gameId"]

def  ServerStat(name):
    data = ServerData(name=name)
    if(data==None):
        return False
    servers=data["servers"]
    server_data=[]
    for server in servers:
        server_data.append("服务器名:"+server["prefix"])
        server_data.append("描述:"+server["description"])
        server_data.append("在线玩家:"+server["serverInfo"])
        server_data.append("模式:"+server["mode"])
        server_data.append("当前地图:"+server["currentMap"])
        server_data.append("服务器位置:"+server["country"])
        server_data.append("serverId:"+server["serverId"])
        server_data.append("是否是官服:"+str(server["official"]))
        server_data.append("gameId:"+str(server["gameId"]))
        
    return server_data    

def ServerData(name):
    url = "https://api.gametools.network/bf1/servers/"
    params = {
        "name":name,
        "platform":"pc",
        "limit":10,
       " region":"all",
        "lang":"zh-tw"
    }
     # 发送GET请求
    response = requests.get(url, params=params)
    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应的JSON数据
        data = response.json()
        # 在这里可以处理数据，例如打印它或进行其他操作
        logging.info(f"成功获取服务器{name}的数据")
        return data
    else:
        logging.info("请求失败，状态码:", response.status_code)
        return None
    