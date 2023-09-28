import json
import logging

def get_motto(key):
    try:
        # 读取JSON文件
        with open('./data/motto.json', 'r',encoding='utf-8') as file:
            data = json.load(file)
            # 查找指定的键
            if key in data:
                return data[key]
            else:
                return False
    except FileNotFoundError:
        logging.info("文件未找到")
        return False
    except json.decoder.JSONDecodeError:
        logging.info("JSON解析错误")
        return False

def add_motto(key,value):
    filename = './data/motto.json'
    try:
        # 读取JSON文件
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 更新或追加键值对
        data[key] = value
        
        # 写入更新后的JSON数据
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        return True
    
    except FileNotFoundError:
        # 如果文件不存在，创建新的JSON文件并写入初始数据
        data = {key: value}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logging.info(f"File '{filename}' 文件不存在，现在已经创建并写入.")
        return True
