"""增加任务锁机制"""
import sys
import requests
import json
import time as sys_time
import logging
from logging.handlers import TimedRotatingFileHandler
import schedule
import pandas as pd
import pymysql
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, time, timedelta
import os
import re
import threading

# 禁用SSL警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 日志文件目录（可选）
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 当前日期命名日志文件
log_filename = datetime.now().strftime("%Y-%m-%d.log")
log_path = os.path.join(log_dir, log_filename)

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - Line %(lineno)d - %(message)s',
    filename=log_path
)

logger = logging.getLogger('数据推送服务')

# 设置任务锁
task_lock = threading.Lock()
is_task_running = False

# 加载配置
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        # 返回默认配置
        return {
            "database": DB_CONFIG,
            "api": {"base_url": BASE_URL, "timeout": 10},
            "schedule": {"interval_seconds": 5}
        }

# 使用配置
config = load_config()
DB_CONFIG = config['database']
BASE_URL = config['api']['base_url']
API_TIMEOUT = config['api']['timeout']
SCHEDULE_INTERVAL = config['schedule']['interval_time']

API_ENDPOINTS = {
    "ashholdmonitoringdata": BASE_URL + "ashholdmonitoringdata",
    "config": BASE_URL + "config",
    "monitoringdata": BASE_URL + "monitoringdata",
    "monitoringrecorde": BASE_URL + "monitoringrecorde",
    "polycurvedata": BASE_URL + "polycurvedata",
    "sysparaset": BASE_URL + "sysparaset"
}

# 记录最后处理的记录ID
LAST_PROCESSED = {
    "ashholdmonitoringdata": 0,
    "config": 0,
    "monitoringdata": 0,
    "monitoringrecorde": 0,
    "polycurvedata": 0,
    "sysparaset": 0
}

# 加载上次处理的记录
def load_last_processed():
    try:
        with open("last_processed.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.info(f"加载上次处理记录失败: {e}")
        #
        save_last_processed()
        # 返回默认值
        return LAST_PROCESSED

# 保存最后处理的记录
def save_last_processed():
    try:
        with open("last_processed.json", "w", encoding='utf-8') as f:
            json.dump(LAST_PROCESSED, f)
    except Exception as e:
        logger.error(f"保存处理记录失败: {e}")


def connect_to_db(max_retries=3, retry_interval=5):
    """ 连接到数据库,带重连机制 """
    retry_count = 0
    while retry_count < max_retries:
        try:
            # 关键字参数（kwargs）解包语法
            connection = pymysql.connect(**DB_CONFIG)
            return connection
        except Exception as e:
            retry_count += 1
            logger.error(f"数据库连接失败(尝试{retry_count}/{max_retries}):{e}")
            if retry_count < max_retries:
                logger.info(f"等待{retry_interval}秒后重试...")
                sys_time.sleep(retry_interval)
    return None

def get_id_field_for_table(table_name):
    """根据表名返回唯一标识字段名"""
    id_mapping = {
        "ashholdmonitoringdata": "id",
        "config": "id",
        "monitoringdata": "id",
        "monitoringrecorde": "id",
        "polycurvedata": "id",
        "sysparaset": "burningModel"
    }
    return id_mapping.get(table_name, "id")

def get_data_from_table(table_name):
    """ 从指定表中获取增量数据 """
    conn = connect_to_db()
    if not conn:
        return []
    try:
        # 使用 DictCursor，表示返回的每条记录是 字典类型，而不是元组
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 获取表的唯一标识字段
        id_field = get_id_field_for_table(table_name)
        last_id = LAST_PROCESSED.get(table_name, 0)

        # 构建查询，只获取上次处理后的新数据
        query = f"SELECT * FROM `{table_name}` WHERE {id_field} > {last_id} ORDER BY {id_field} ASC"
        cursor.execute(query)
        data = cursor.fetchall()
        # 更新最后处理的ID
        if data:
            max_id = max(record[id_field] for record in data)
            LAST_PROCESSED[table_name] = max_id
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
                # 输出: 2025-05-08 14:30:00
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
    """ 将数据推送到API """
    if not data:
        logger.info(f"表 {table_name} 没有需要推送的数据")
        return True

    # 通过表名寻找对应的接口地址
    endpoint = API_ENDPOINTS.get(table_name)
    if not endpoint:
        logger.error(f"未找到表 {table_name} 对应的API端点")
        return False

    success_count = 0
    total_count = len(data)
    failed_records = []
    for record in data:
        try:
            # 发送POST请求，不验证SSL证书
            response = requests.post(
                endpoint,
                json=record,
                verify=False,  # 不验证SSL证书
                timeout=API_TIMEOUT  # 设置超时时间
            )
            if response.status_code == 200:
                success_count += 1
                logger.info(f"成功推送数据到 {endpoint}")
            else:
                logger.error(f"推送数据到 {endpoint} 失败, 状态码: {response.status_code}, 响应: {response.text}")
                failed_records.append(record)
        except Exception as e:
            logger.error(f"推送数据到 {endpoint} 时发生错误: {e}")
            failed_records.append(record)
    # 所有记录都推送成功，返回True
    if success_count == total_count:
        logger.info(f"所有记录都推送完毕")
        return True
    else:
        logger.warning(f"表 {table_name} 数据推送: 成功 {success_count}/{total_count}")
        return False

def process_table(table_name):
    """处理单个表的数据推送流程"""
    logger.info(f"==========>>> 开始处理表 【{table_name}】 的数据")
    # 获取增量数据
    raw_data = get_data_from_table(table_name)
    if not raw_data:
        logger.info(f"表 {table_name} 没有需要推送的数据")
        return True

    # 记录数据条数
    data_count = len(raw_data)
    logger.info(f"表 {table_name} 获取到 {data_count} 条新数据")

    # 格式化数据
    formatted_data = format_data(table_name, raw_data)
    # 推送数据
    success = push_data_to_api(table_name, formatted_data)
    logger.info(f"表 【{table_name}】 的数据处理完成 <<<==========")
    logger.info("")
    return success


def run_data_push():
    """运行所有表的数据推送"""
    global is_task_running
    # 检查是否已有任务在运行
    with task_lock:
        if is_task_running:
            logger.info("上一次数据推送任务尚未完成，跳过此次执行")
            return
        is_task_running = True
    try:
        logger.info("======================>>>>>> 开始数据推送任务 <<<<<<======================")
        # 加载上次推送的最后记录
        global LAST_PROCESSED
        LAST_PROCESSED = load_last_processed()
        all_success = True

        for table_name in API_ENDPOINTS.keys():
            try:
                # 推送数据
                success = process_table(table_name)
                if not success:
                    all_success = False
            except Exception as e:
                logger.error(f"处理表 {table_name} 时发生错误: {e}")
                all_success = False
            # 如果所有表都成功推送，保存处理记录
            if all_success:
                save_last_processed()
        logger.info("======================>>>>>> 数据推送任务完成 <<<<<<======================")
    finally:
        with task_lock:
            # 无论是否成功完成，都要释放锁
            is_task_running = False

def schedule_jobs():
    """ 设置定时任务 """
    # 将函数注册为定时任务 schedule.every(10).minutes.do(job)
    # schedule.every(SCHEDULE_INTERVAL).seconds.do(run_data_push)
    schedule.every(SCHEDULE_INTERVAL).minutes.do(run_data_push)
    logger.info(f"数据推送服务已启动，将{SCHEDULE_INTERVAL}分钟执行一次")
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