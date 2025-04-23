from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# 模拟API端点：接收数据并写入本地文件
@app.route('/data/ashholdmonitoringdata', methods=['POST'])
def receive_ashholdmonitoringdata():
        # 获取请求体中的 JSON 数据
        data = request.get_json()
        return save_data(data, "ashholdmonitoringdata.json")

@app.route('/data/config', methods=['POST'])
def receive_config():
    # 获取请求体中的 JSON 数据
    data = request.get_json()
    return save_data(data, "config.json")

@app.route('/data/monitoringdata', methods=['POST'])
def receive_monitoringdata():
    # 获取请求体中的 JSON 数据
    data = request.get_json()
    return save_data(data, "monitoringdata.json")

@app.route('/data/monitoringrecorde', methods=['POST'])
def receive_monitoringrecorde():
    # 获取请求体中的 JSON 数据
    data = request.get_json()
    return save_data(data, "monitoringrecorde.json")

@app.route('/data/polycurvedata', methods=['POST'])
def receive_polycurvedata():
    # 获取请求体中的 JSON 数据
    data = request.get_json()
    return save_data(data, "polycurvedata.json")

@app.route('/data/sysparaset', methods=['POST'])
def receive_sysparaset():
    # 获取请求体中的 JSON 数据
    data = request.get_json()
    return save_data(data, "sysparaset.json")

def save_data(data, filename):
    try:
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        with open(filename, 'a') as f:
            json.dump(data, f)
            f.write("\n")
            # 返回成功响应
        return jsonify({"status": "success", "message": "Data received and saved"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # 运行 Flask Web 服务器，监听本地 5000 端口
    app.run(debug=True, host='0.0.0.0', port=5000)
