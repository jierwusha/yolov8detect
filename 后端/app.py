import datetime
import mimetypes
import re
import uuid

from flask import Flask, request, send_from_directory, make_response, jsonify, current_app, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import shutil
from datetime import timedelta

from core.config.config import BaseConfig
from core.img_process.img_process import img_process
from core.video.code_video.code_video import video_process
from core.video.video_process.mainProcess import countCar
from core.camera.camera import track_cam
from core.camera.screen_low import capture
from core.camera.modify import capture_and_detect


# app是Flask构建的实例
app = Flask(__name__)
# 添加配置文件
app.config.from_object(BaseConfig)
# 文件存储路径
TMP_CT_FOLDER = './tmp/ct'
TMP_DRAW_FOLDER = './tmp/draw'
MODEL_PATH = './weights'
app.config['UPLOAD_FOLDER'] = TMP_CT_FOLDER
app.config['SAVE_FOLDER'] = TMP_DRAW_FOLDER
app.config['MODEL_PATH'] = MODEL_PATH
# 允许的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}
# 模型存储路径

# 确保目标目录存在
if not os.path.exists(TMP_CT_FOLDER):
    os.makedirs(TMP_CT_FOLDER)
if not os.path.exists(TMP_DRAW_FOLDER):
    os.makedirs(TMP_DRAW_FOLDER)
# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
# 初始化扩展，传入app 创建db
db = SQLAlchemy(app)


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


# 测试数据库连接
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("select 1"))
#         print(rs.fetchone())
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return f"Current working directory: {os.getcwd()}"


@app.route('/upload', methods=['POST'])
def upload_file():
    # 获取特定参数
    mode = request.form.get('mode')
    conf = float(request.form.get('conf'))
    if 'file' not in request.files:
        return jsonify({'status': 0,
                        'error': 'No file part'})

    file = request.files.get('file')

    if file and allowed_file(file.filename):
        mime_type, _ = mimetypes.guess_type(file.filename)
        if mime_type is None:
            return jsonify({'status': 0,
                            'error': 'Unknown file type'})
        if mime_type.startswith('image'):
            folder = app.config['UPLOAD_FOLDER']
        else:
            return jsonify({'status': 0,
                            'error': 'Unsupported file type'})

        unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}"
        src_path = os.path.join(folder, unique_filename)
        src_path = src_path.replace('\\', '/')
        save_path = os.path.join(app.config['SAVE_FOLDER'], unique_filename)
        save_path = save_path.replace('\\', '/')
        file.save(src_path)
        if mode == 'code':
            model_path = os.path.join(app.config['MODEL_PATH'], 'code.pt')
        elif mode == 'car':
            model_path = os.path.join(app.config['MODEL_PATH'], 'car.pt')
        else:
            model_path = os.path.join(app.config['MODEL_PATH'], 'yolo.pt')

        # 调用核心处理功能
        image_info = img_process(conf, model_path, src_path, save_path)

        return jsonify({'status': 1,
                        'image_url': f'http://127.0.0.1:5000/{src_path}',
                        'draw_url': f'http://127.0.0.1:5000/{save_path}',
                        'image_info': image_info})

    return jsonify({'status': 0, 'error': 'File type not allowed'})


@app.route('/upload_video', methods=['POST'])
def upload_video():
    # 获取特定参数
    mode = request.form.get('mode')
    conf = float(request.form.get('conf'))
    if 'file' not in request.files:
        return jsonify({'status': 0,
                        'error': 'No file part'})

    file = request.files.get('file')

    if file and allowed_file(file.filename):
        mime_type, _ = mimetypes.guess_type(file.filename)
        if mime_type is None:
            return jsonify({'status': 0,
                            'error': 'Unknown file type'})

        if mime_type.startswith('video'):
            folder = app.config['UPLOAD_FOLDER']
        else:
            return jsonify({'status': 0,
                            'error': 'Unsupported file type'})

        unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}"
        src_path = os.path.join(folder, unique_filename)
        src_path = src_path.replace('\\', '/')
        save_path = os.path.join(app.config['SAVE_FOLDER'], unique_filename)
        save_path = save_path.replace('\\', '/')
        file.save(src_path)
        if mode == 'code':
            model_path = os.path.join(app.config['MODEL_PATH'], 'code.pt')
            result_list = video_process(conf, model_path, src_path, save_path)
            return jsonify({'status': 1,
                            'video_url': f'http://127.0.0.1:5000/{src_path}',
                            'draw_url': f'http://127.0.0.1:5000/{save_path}',
                            'result_info': result_list
                            })
        elif mode == 'car':
            # 调用核心处理功能
            YOLOmodelPath = os.path.join(app.config['MODEL_PATH'], 'video.pt')
            LPRNetModelPath = os.path.join(app.config['MODEL_PATH'], 'lprnet_best.pth')
            car_list, car_count = countCar(YOLOmodelPath, LPRNetModelPath, src_path, save_path)
            return jsonify({'status': 1,
                            'video_url': f'http://127.0.0.1:5000/{src_path}',
                            'draw_url': f'http://127.0.0.1:5000/{save_path}',
                            'result_info': car_list,
                            'result_count': car_count
                            })
        else:
            model_path = os.path.join(app.config['MODEL_PATH'], 'yolo.pt')
            result_list = video_process(conf, model_path, src_path, save_path)
            return jsonify({'status': 1,
                            'video_url': f'http://127.0.0.1:5000/{src_path}',
                            'draw_url': f'http://127.0.0.1:5000/{save_path}',
                            'result_info': result_list
                            })

    return jsonify({'status': 0, 'error': 'File type not allowed'})


@app.route("/download", methods=['GET'])
def download_file():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    return send_from_directory('data', 'testfile.zip', as_attachment=True)


# show photo
# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if file is not None:
            file_path = f'tmp/{file}'
            if file.endswith('.jpg') or file.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif file.endswith('.png'):
                content_type = 'image/png'
            elif file.endswith('.mp4'):
                content_type = 'video/mp4'
            else:
                return "Unsupported file format", 415  # Unsupported Media Type

            if os.path.exists(file_path):
                if content_type.startswith('image'):
                    return send_file(file_path, mimetype=content_type)
                elif content_type == 'video/mp4':
                    return send_file(file_path, mimetype=content_type, as_attachment=True)
            else:
                return "File not found", 404  # Not Found

    return "Invalid request", 400  # Bad Request



@app.route("/camera", methods=['POST'])
def camera():
    data = request.json
    if data:
        key1 = data.get('key1', '')
        key2 = data.get('key2', '')
        key3 = data.get('key3', '')
        concatenated = f"{key1}{key2}{key3}"
        if concatenated == '000':
            model_path = os.path.join(app.config['MODEL_PATH'], 'code.pt')
            track_cam(0, model_path)
            return "Processed successfully"
        elif concatenated == '001':
            model_path = os.path.join(app.config['MODEL_PATH'], 'car.pt')
            track_cam(0, model_path)
            return "Processed successfully"
        elif concatenated == '010':
            model_path = os.path.join(app.config['MODEL_PATH'], 'code.pt')
            track_cam(1, model_path)
            return "Processed successfully"
        elif concatenated == '011':
            model_path = os.path.join(app.config['MODEL_PATH'], 'car.pt')
            track_cam(1, model_path)
            return "Processed successfully"
        elif re.match(r'10\d', concatenated):
            model_path = os.path.join(app.config['MODEL_PATH'], 'camera.pt')
            capture(model_path)
            return "Processed successfully"
        elif re.match(r'11\d', concatenated):
            model_path = os.path.join(app.config['MODEL_PATH'], 'camera.pt')
            capture_and_detect(model_path)
            return "Processed successfully"
        else:
            return "fail"
    else:
        return "fail"


if __name__ == '__main__':
    app.run()
