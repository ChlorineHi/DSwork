from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import json
from typing import Dict, List, Any

# 导入算法类
from algorithms.image_processor import ImageProcessor
from algorithms.path_finder import PathFinder
from algorithms.data_structure import DataStructure

app = Flask(__name__)
CORS(app)

# 初始化算法类实例
image_processor = ImageProcessor()  # 图像处理类实例
path_finder = PathFinder()         # 路径查找类实例
data_structure = DataStructure()   # 数据结构类实例

# ... existing code ...

@app.route('/api/process-image', methods=['POST'])
def process_image():
    """图像处理接口"""
    if 'image' not in request.files:
        return jsonify({
            'status': 'error',
            'message': '没有上传图片'
        }), 400
        
    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({
            'status': 'error',
            'message': '无效的文件类型'
        }), 400

    try:
        # 使用图像处理类的方法
        image = Image.open(file.stream)
        processed_image = image_processor.process(image)
        result = image_processor.analyze(processed_image)
        
        return jsonify({
            'status': 'success',
            'message': '图片处理成功',
            'result': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'处理失败: {str(e)}'
        }), 500

@app.route('/api/shortest-path', methods=['POST'])
def find_shortest_path():
    """最短路径计算接口"""
    try:
        data = request.get_json()
        if not data or 'graph' not in data or 'start' not in data or 'end' not in data:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数'
            }), 400

        # 使用路径查找类的方法
        path = path_finder.find_path(data['graph'], data['start'], data['end'])
        distance = path_finder.calculate_distance(path)
        
        return jsonify({
            'status': 'success',
            'message': '路径计算成功',
            'path': path,
            'distance': distance
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'计算失败: {str(e)}'
        }), 500

@app.route('/api/data', methods=['POST', 'GET', 'DELETE'])
def handle_data():
    """数据结构操作接口"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            # 使用数据结构类的插入方法
            result = data_structure.insert(data)
            return jsonify({
                'status': 'success',
                'message': '数据添加成功',
                'result': result
            })
            
        elif request.method == 'GET':
            key = request.args.get('key')
            # 使用数据结构类的查询方法
            result = data_structure.search(key)
            return jsonify({
                'status': 'success',
                'message': '数据查询成功',
                'data': result
            })
            
        elif request.method == 'DELETE':
            key = request.args.get('key')
            # 使用数据结构类的删除方法
            result = data_structure.delete(key)
            return jsonify({
                'status': 'success',
                'message': '数据删除成功',
                'result': result
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'操作失败: {str(e)}'
        }), 500

# ... existing code ...