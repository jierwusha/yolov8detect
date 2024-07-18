import datetime
import mimetypes
from flask import Flask, request, send_from_directory, make_response, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
import os
import shutil
from datetime import timedelta
from core.config.config import BaseConfig
from core.img_process import img_process
from core.video.video_process import mainProcess

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
    # 获取JSON数据
    data = request.files
    # 获取特定参数
    mode = data.get('mode')
    print(mode)
    conf = data.get('conf')
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

        src_path = os.path.join(folder, file.filename)
        save_path = os.path.join(app.config['SAVE_FOLDER'], file.filename)
        if mode == 1:
            model_path = os.path.join(app.config['MODEL_PATH'], 'code.pt')
        elif mode == 2:
            model_path = os.path.join(app.config['MODEL_PATH'], 'car.pt')
        else:
            model_path = os.path.join(app.config['MODEL_PATH'], 'code.pt')
        file.save(src_path)

        # 调用核心处理功能
        image_info = img_process.img_process(conf, model_path, src_path, save_path)

        return jsonify({'status': 1,
                        'image_url': f'http://127.0.0.1:5000/{src_path}',
                        'draw_url': f'http://127.0.0.1:5000/{save_path}',
                        'image_info': image_info})

    return jsonify({'status': 0, 'error': 'File type not allowed'})


@app.route('/upload_video', methods=['POST'])
def upload_video():
    # 获取JSON数据
    data = request.json
    # 获取特定参数
    mode = data.get('mode')
    conf = data.get('conf')
    if 'file' not in request.files:
        return jsonify({'status': 0,
                        'error': 'No file part'})

    file = request.files['file']

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

        src_path = os.path.join(folder, file.filename)
        save_path = os.path.join(app.config['SAVE_FOLDER'], file.filename)
        if mode == 'code':
            model_path = os.path.join(app.config['MODEL_PATH'], 'code.pt')
        elif mode == 'car':
            # 调用核心处理功能
            YOLOmodelPath = os.path.join(app.config['MODEL_PATH'], 'video.pt')
            LPRNetModelPath = os.path.join(app.config['MODEL_PATH'], 'lprnet_best.pth')
            mainProcess.mainProcess(YOLOmodelPath, LPRNetModelPath, src_path, save_path)
        else:
            model_path = os.path.join(app.config['MODEL_PATH'], 'yolo.pt')

        return jsonify({'status': 1,
                        'video_url': f'http://127.0.0.1:5000/{src_path}',
                        'draw_url': f'http://127.0.0.1:5000/{save_path}',
                        })

    return jsonify({'status': 0, 'error': 'File type not allowed'})


@app.route("/download", methods=['GET'])
def download_file():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    return send_from_directory('data', 'testfile.zip', as_attachment=True)


# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if not file is None:
            image_data = open(f'tmp/{file}', "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response


if __name__ == '__main__':
    app.run()
