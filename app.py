# app.py
# Flask后端程序
# UTF-8编码, 无BOM

from flask import Flask, request, jsonify, send_from_directory
import os
from cube_solver import solve
import validator

app = Flask(__name__, static_folder='static')

# 将 app.py 目录下或 static 目录下的 index.html 作为首页
@app.route('/')
def index():
    # 兼容直接放在根目录或static目录
    if os.path.exists(os.path.join('static', 'index.html')):
         return send_from_directory('static', 'index.html')
    # 假设代码结构是 app.py 和 index.html 同级，则需要读取文件内容返回
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "Error: index.html not found"

def convert_unfolded_to_solver_format(unfolded_str):
    if len(unfolded_str) != 24:
        return ""
    # UFL, UBL, UBR, UFR, DFL, DBL, DBR, DFR
    indices = [2, 8, 5, 0, 17, 4, 1, 16, 13, 3, 9, 12, 22, 10, 7, 20, 19, 6, 21, 18, 15, 23, 11, 14]
    return "".join(unfolded_str[i] for i in indices)

# 目标状态: YRBYOBYOGYRGWRBWOBWOGWRG
target_state = 'YRBYOBYOGYRGWRBWOBWOGWRG'

@app.route('/solve', methods=['POST'])
def api_solve():
    try:
        data = request.get_json()
        unfolded_cube_state = data.get('cube', '')
        if len(unfolded_cube_state) != 24:
            return jsonify({'error': '魔方状态必须为长度24的字符串'}), 400

        solver_cube_state = convert_unfolded_to_solver_format(unfolded_cube_state)
        
        # 1. 验证魔方是否合法
        is_valid, msg = validator.validate_cube(solver_cube_state)
        if not is_valid:
            return jsonify({'error': '填色状态不可解: ' + msg}), 200

        # 2. 求解
        steps = solve(solver_cube_state, target_state)
        return jsonify({'steps': steps})
    except Exception as e:
        app.logger.error(f"Solve API error: {e}")
        return jsonify({'error': '服务器内部错误: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
