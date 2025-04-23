import requests
import json
import time as sys_time
import logging
import schedule
import pandas as pd
import pymysql
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, time, timedelta

# 禁用SSL警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - Line %(lineno)d - %(message)s',
    filename='data_push.log'
)
logger = logging.getLogger('数据推送服务')

# 接口地址
BASE_URL = "http://127.0.0.1:5000/data/"
API_ENDPOINTS = {
    "ashholdmonitoringdata": BASE_URL + "ashholdmonitoringdata",
    "config": BASE_URL + "config",
    "monitoringdata": BASE_URL + "monitoringdata",
    "monitoringrecorde": BASE_URL + "monitoringrecorde",
    "polycurvedata": BASE_URL + "polycurvedata",
    "sysparaset": BASE_URL + "sysparaset"
}

# 配置字典---数据库连接配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'database': 'baohui_test',
    'port': 3306,
    'charset': 'utf8mb4'
}


def connect_to_db():
    """连接到数据库"""
    try:
        # 关键字参数（kwargs）解包语法
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return None


def get_data_from_table(table_name):
    """从指定表中获取数据"""
    conn = connect_to_db()
    if not conn:
        return []
    try:
        # 使用 DictCursor，表示返回的每条记录是 字典类型，而不是元组
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 这里可以根据需要修改SQL，例如只获取未推送的数据
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Exception as e:
        logger.error(f"从表 {table_name} 获取数据失败: {e}")
        return []
    finally:
        conn.close()



def format_data(table_name, data):
    """根据不同表名格式化数据"""
    formatted_data = []

    # 根据不同的表进行数据格式化
    for record in data:
        if table_name == "ashholdmonitoringdata":
            date_val = record.get("date")  # 类型：datetime.date
            time_val = record.get("curTime")  # 可能是 datetime.time 或 datetime.timedelta

            # 处理 time 类型不一致
            if isinstance(time_val, timedelta):
                # 将 timedelta 转为 time 对象
                total_seconds = int(time_val.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                time_val = time(hour=hours, minute=minutes, second=seconds)

            if date_val and time_val:
                full_datetime = datetime.combine(date_val, time_val)
                # full_datetime是一个datetime.datatime对象，.timestamp()将datetime转换为Unix时间戳，并转化为毫秒
                curtime_ms = int(full_datetime.timestamp() * 1000)
                date_ms = int(datetime.combine(date_val, time.min).timestamp() * 1000)
            else:
                now = datetime.now()
                curtime_ms = int(now.timestamp() * 1000)
                date_ms = int(datetime.combine(now.date(), time.min).timestamp() * 1000)

            formatted = {
                "serialnum": float(record.get("serialNum", 0)),
                "ashholdrate": float(record.get("ashHoldRate", 0)),
                "date": str(date_ms),
                "curtime": str(curtime_ms)
            }
        elif table_name == "config":
            formatted = {
                "channum": record.get("chanNum", ""),
                "suctionmode": record.get("suctionMode", ""),
                "calibrcoef1": float(record.get("calibrCoef1", 0)),
                "calibrcoef2": float(record.get("calibrCoef2", 0)),
                "calibrcoef3": float(record.get("calibrCoef3", 0)),
                "calibrcoef4": float(record.get("calibrCoef4", 0)),
                "calibrcoef5": float(record.get("calibrCoef5", 0)),
                "calibrcoef6": float(record.get("calibrCoef6", 0)),
                "suctiontimes": int(record.get("suctionTimes", 0))
            }
        elif table_name == "monitoringdata":
            date_val = record.get("detectDate")  # 类型：datetime.date
            time_val = record.get("detectTime")  # 可能是 datetime.time 或 datetime.timedelta

            # 处理 time 类型不一致
            if isinstance(time_val, timedelta):
                # 将 timedelta 转为 time 对象
                total_seconds = int(time_val.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                time_val = time(hour=hours, minute=minutes, second=seconds)

            if date_val and time_val:
                full_datetime = datetime.combine(date_val, time_val)
                # full_datetime是一个datetime.datatime对象，.timestamp()将datetime转换为Unix时间戳，并转化为毫秒
                curtime_ms = int(full_datetime.timestamp() * 1000)
                date_ms = int(datetime.combine(date_val, time.min).timestamp() * 1000)
            else:
                now = datetime.now()
                curtime_ms = int(now.timestamp() * 1000)
                date_ms = int(datetime.combine(now.date(), time.min).timestamp() * 1000)

            formatted = {
                "serialnum": int(record.get("serialNum", 0)),
                "gray": int(record.get("gray", 0)),
                "graywithcrack": int(record.get("graywithCrack", 0)),
                "openingrate": float(record.get("openingRate", 0)),
                "ashshrinkagerate": float(record.get("ashshrinkageRate", 0)),
                "ashshrinkagerateforarea": float(record.get("ashshrinkageRateForArea", 0)),
                "carbonlinewidth": float(record.get("carbonlineWidth", 0)),
                "carbonlineuniformity": float(record.get("carbonlineUniformity", 0)),
                "burningrate": float(record.get("burningRate", 0)),
                "burningstatus": record.get("burningStatus", ""),
                "suctiontimes": int(record.get("suctiontimes", 0)),
                "productbrand": record.get("productBrand", ""),
                "detecttime": str(curtime_ms),
                "detectdate": str(date_ms)
            }
        elif table_name == "monitoringrecorde":
            date_val = record.get("detectTime")  # 类型：datetime.date
            time_val = record.get("curDetectTime")  # 可能是 datetime.time 或 datetime.timedelta

            # 处理 time 类型不一致
            if isinstance(time_val, timedelta):
                # 将 timedelta 转为 time 对象
                total_seconds = int(time_val.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                time_val = time(hour=hours, minute=minutes, second=seconds)

            if date_val and time_val:
                full_datetime = datetime.combine(date_val, time_val)
                # full_datetime是一个datetime.datatime对象，.timestamp()将datetime转换为Unix时间戳，并转化为毫秒
                curtime_ms = int(full_datetime.timestamp() * 1000)
                date_ms = int(datetime.combine(date_val, time.min).timestamp() * 1000)
            else:
                now = datetime.now()
                curtime_ms = int(now.timestamp() * 1000)
                date_ms = int(datetime.combine(now.date(), time.min).timestamp() * 1000)

            formatted = {
                "detecttime": str(date_ms),
                "detectperson": record.get("detectPerson", ""),
                "brand;": record.get("brand", ""),  # 注意这里有一个分号
                "detecttype": record.get("detectType", ""),
                "ciglength": int(record.get("cigLength", 0)),
                "burninglength": int(record.get("burningLength", 0)),
                "burningtype": record.get("burningType", ""),
                "suctionmodel": record.get("suctionModel", ""),
                "shootmodel": record.get("shootModel", ""),
                "curdetecttime": str(curtime_ms)
            }
        elif table_name == "polycurvedata":
            date_val = record.get("date")  # 类型：datetime.date
            if date_val:
                date_ms = int(datetime.combine(date_val, time.min).timestamp() * 1000)
            else:
                date_ms = int(datetime.combine(now.date(), time.min).timestamp() * 1000)

            formatted = {
                "date": str(date_ms),
                "productbrand": record.get("productBrand", ""),
                "groupnum": int(record.get("groupNum", 0)),
                "channelnum": int(record.get("channelNum", 0)),
                "scannum": int(record.get("scanNum", 0)),
                "firelength": float(record.get("fireLength", 0)),
                "carbonlinewidth": float(record.get("carbonLineWidth", 0)),
                "carbonlineuniformity": float(record.get("carbonLineUniformity", 0)),
                "burningrate": float(record.get("burningRate", 0))
            }
        elif table_name == "sysparaset":
            formatted = {
                "burningmodel": record.get("burningModel", 0),
                "cigarlength": int(record.get("cigarLength", 0)),
                "suctionpara": int(record.get("suctionPara", 0)),
                "suctioncapcity": int(record.get("suctionCapcity", 0)),
                "suctioninerval": int(record.get("suctionInerval", 0)),
                "suctioncontinus": int(record.get("suctionContinus", 0)),
                "rotateangle": int(record.get("rotateAngle", 0)),
                "swingtime": float(record.get("swingTime", 0)),
                "rotatecycle": float(record.get("rotatecycle", 0)),
                "rotatetime": float(record.get("rotateTime", 0))
            }
        else:
            formatted = record

        formatted_data.append(formatted)

    return formatted_data


def push_data_to_api(table_name, data):
    """将数据推送到API"""
    if not data:
        logger.info(f"表 {table_name} 没有需要推送的数据")
        return

    # 通过表名寻找对应的接口地址
    endpoint = API_ENDPOINTS.get(table_name)
    if not endpoint:
        logger.error(f"未找到表 {table_name} 对应的API端点")
        return

    for record in data:
        try:
            # 发送POST请求，不验证SSL证书
            response = requests.post(
                endpoint,
                json=record,
                verify=False,  # 不验证SSL证书
                timeout=10  # 设置超时时间
            )
            if response.status_code == 200:
                logger.info(f"成功推送数据到 {endpoint}")
            else:
                logger.error(f"推送数据到 {endpoint} 失败, 状态码: {response.status_code}, 响应: {response.text}")

        except Exception as e:
            logger.error(f"推送数据到 {endpoint} 时发生错误: {e}")

def process_table(table_name):
    """处理单个表的数据推送流程"""
    logger.info(f"==========>>> 开始处理表 {table_name} 的数据")
    # 获取数据
    raw_data = get_data_from_table(table_name)
    if not raw_data:
        logger.info(f"表 {table_name} 没有需要推送的数据")
        return
    # 格式化数据
    formatted_data = format_data(table_name, raw_data)
    # 推送数据
    push_data_to_api(table_name, formatted_data)
    logger.info(f"表 {table_name} 的数据处理完成 <<<==========")
    logger.info("")


def run_data_push():
    """运行所有表的数据推送"""
    logger.info("======================>>>>>> 开始数据推送任务 <<<<<<======================")
    for table_name in API_ENDPOINTS.keys():
        try:
            # 推送数据
            process_table(table_name)
        except Exception as e:
            logger.error(f"处理表 {table_name} 时发生错误: {e}")
        # break
    logger.info("======================>>>>>> 数据推送任务完成 <<<<<<======================")


def schedule_jobs():
    """设置定时任务"""
    # 将函数注册为定时任务
    schedule.every(5).seconds.do(run_data_push)
    logger.info("数据推送服务已启动，将每5秒执行一次")
    # 立即执行一次
    run_data_push()
    # 持续运行定时任务
    while True:
        schedule.run_pending()
        sys_time.sleep(1)


if __name__ == "__main__":
    try:
        schedule_jobs()
    except KeyboardInterrupt:
        logger.info("服务被手动中断")
    except Exception as e:
        logger.error(f"服务运行出错: {e}")