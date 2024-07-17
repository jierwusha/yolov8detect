import datetime
import mimetypes
from flask import Flask, request, send_from_directory, make_response, jsonify, current_app
from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
import os
import shutil
from datetime import timedelta
from processor.AIDetector_pytorch import Detector

# app是Flask构建的实例
app = Flask(__name__)
# 添加配置文件
app.config.from_object(BaseConfig)
# 文件存储路径
IMAGE_UPLOAD_FOLDER = 'uploads/image'
VIDIO_UPLOAD_FOLDER = 'uploads/vidio'
TMP_CT_FOLDER = './tmp/ct'
TMP_DRAW_FOLDER = './tmp/draw'
app.config['UPLOAD_FOLDER_IMAGES'] = IMAGE_UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_VIDEOS'] = VIDIO_UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}
# 确保目标目录存在
if not os.path.exists(IMAGE_UPLOAD_FOLDER):
    os.makedirs(IMAGE_UPLOAD_FOLDER)
if not os.path.exists(VIDIO_UPLOAD_FOLDER):
    os.makedirs(VIDIO_UPLOAD_FOLDER)
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
    with app.app_context():
        current_app.model = Detector('code.pt')
    if 'file' not in request.files:
        return jsonify({'status': 0,
                        'error': 'No file part'})

    file = request.files['file']
    print(datetime.datetime.now(), file.filename)

    if file and allowed_file(file.filename):
        mime_type, _ = mimetypes.guess_type(file.filename)
        if mime_type is None:
            return jsonify({'status': 0,
                            'error': 'Unknown file type'})

        if mime_type.startswith('image'):
            folder = app.config['UPLOAD_FOLDER_IMAGES']
        elif mime_type.startswith('video'):
            folder = app.config['UPLOAD_FOLDER_VIDEOS']
        else:
            return jsonify({'status': 0,
                            'error': 'Unsupported file type'})

        src_path = os.path.join(folder, file.filename)
        file.save(src_path)

        # 将文件复制到临时目录
        shutil.copy(src_path, TMP_CT_FOLDER)
        image_path = os.path.join(TMP_CT_FOLDER, file.filename)

        # 调用核心处理功能

        output_image_path = os.path.join(TMP_DRAW_FOLDER, 'results.jpg')
        image_info = current_app.model.detect(image_path, output_image_path)

        return jsonify({'status': 1,
                        'image_url': f'http://127.0.0.1:5000/tmp/ct/test1.jpg',
                        'draw_url': f'http://127.0.0.1:5000/tmp/draw/results.jpg',
                        'image_info': image_info})

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
