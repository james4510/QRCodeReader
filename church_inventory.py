import sqlite3
import qrcode
from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import os

app = Flask(__name__)

# 1. 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('church_items.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items
                      (item_id TEXT PRIMARY KEY,
                       item_name TEXT,
                       manager TEXT,
                       department TEXT,
                       borrow_date TEXT,
                       is_borrowed INTEGER)''')
    conn.commit()
    conn.close()

# 2. 물품 추가
def add_item(item_id, item_name, manager, department, borrow_date, is_borrowed):
    conn = sqlite3.connect('church_items.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (item_id, item_name, manager, department, borrow_date, is_borrowed) VALUES (?, ?, ?, ?, ?, ?)",
                   (item_id, item_name, manager, department, borrow_date, is_borrowed))
    conn.commit()
    conn.close()

# 3. 물품 조회
def get_item(item_id):
    conn = sqlite3.connect('church_items.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE item_id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

# 4. QR 코드 생성 (URL 포함)
def create_qr_code(item_id):
    # 로컬 네트워크 상의 서버 IP 주소를 사용 (예: 192.168.1.10)
    server_ip = "192.168.0.18"  # 서버 IP 주소를 사용
    url = f"http://{server_ip}:5000/item/{item_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    qr_image_path = f"static/{item_id}_qrcode.png"
    img.save(qr_image_path)
    return qr_image_path


# 5. 기본 페이지 라우팅 (물품 추가 폼)
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <title>교회 물품 관리 시스템</title>
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <h1 class="text-center">교회 물품 추가</h1>
                    <form action="/add_item" method="POST" class="mt-4">
                        <div class="form-group">
                            <label for="item_id">물품 ID</label>
                            <input type="text" class="form-control" id="item_id" name="item_id" placeholder="물품 ID" required>
                        </div>
                        <div class="form-group">
                            <label for="item_name">물품 이름</label>
                            <input type="text" class="form-control" id="item_name" name="item_name" placeholder="물품 이름" required>
                        </div>
                        <div class="form-group">
                            <label for="manager">관리인</label>
                            <input type="text" class="form-control" id="manager" name="manager" placeholder="관리인" required>
                        </div>
                        <div class="form-group">
                            <label for="department">부서</label>
                            <input type="text" class="form-control" id="department" name="department" placeholder="부서" required>
                        </div>
                        <div class="form-group">
                            <label for="borrow_date">대여 날짜</label>
                            <input type="date" class="form-control" id="borrow_date" name="borrow_date" required>
                        </div>
                        <div class="form-group">
                            <label for="is_borrowed">대여 상태</label>
                            <select class="form-control" id="is_borrowed" name="is_borrowed" required>
                                <option value="0">반납됨</option>
                                <option value="1">대여 중</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary btn-block">물품 추가</button>
                    </form>
                </div>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    ''')


# 6. 물품 추가 및 QR 코드 생성
@app.route('/add_item', methods=['POST'])
def add_item_route():
    item_id = request.form['item_id']
    item_name = request.form['item_name']
    manager = request.form['manager']
    department = request.form['department']
    borrow_date = request.form['borrow_date']
    is_borrowed = int(request.form['is_borrowed'])

    # 물품 데이터베이스에 추가
    add_item(item_id, item_name, manager, department, borrow_date, is_borrowed)

    # QR 코드 생성
    qr_image_path = create_qr_code(item_id)

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <title>QR 코드 생성 완료</title>
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header bg-success text-white text-center">
                            <h2 class="card-title">QR 코드 생성 완료</h2>
                        </div>
                        <div class="card-body text-center">
                            <p class="lead">아래의 QR 코드를 스캔하여 물품 정보를 확인하세요.</p>
                            <img src="/{{ qr_image_path }}" alt="QR Code" class="img-fluid mt-4 mb-4" style="max-width: 300px;">
                            <hr>
                            <h4>물품 정보 요약</h4>
                            <p><strong>물품 ID:</strong> {{ item_id }}</p>
                            <p><strong>물품 이름:</strong> {{ item_name }}</p>
                            <p><strong>관리인:</strong> {{ manager }}</p>
                            <p><strong>부서:</strong> {{ department }}</p>
                            <p><strong>대여 날짜:</strong> {{ borrow_date }}</p>
                            <p><strong>대여 상태:</strong> {{ '대여 중' if is_borrowed == 1 else '반납됨' }}</p>
                        </div>
                        <div class="card-footer text-center">
                            <a href="/" class="btn btn-primary">새 물품 추가하기</a>
                            <a href="/item/{{ item_id }}" class="btn btn-secondary">물품 정보 보기</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    ''', qr_image_path=qr_image_path, item_id=item_id, item_name=item_name, manager=manager, department=department, borrow_date=borrow_date, is_borrowed=is_borrowed)

# 7. 물품 정보 페이지 (QR 코드로 접근 시 보여주는 페이지)
@app.route('/item/<item_id>')
def item_info(item_id):
    item = get_item(item_id)

    if item:
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <title>{{ item[1] }} 정보</title>
        </head>
        <body>
            <div class="container mt-5">
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="card">
                            <div class="card-header bg-primary text-white">
                                <h2 class="card-title text-center">{{ item[1] }} 정보</h2>
                            </div>
                            <div class="card-body">
                                <p><strong>물품 ID:</strong> {{ item[0] }}</p>
                                <p><strong>물품 이름:</strong> {{ item[1] }}</p>
                                <p><strong>관리인:</strong> {{ item[2] }}</p>
                                <p><strong>부서:</strong> {{ item[3] }}</p>
                                <p><strong>대여 날짜:</strong> {{ item[4] }}</p>
                                <p><strong>대여 상태:</strong> {{ '대여 중' if item[5] == 1 else '반납됨' }}</p>
                            </div>
                            <div class="card-footer text-center">
                                <a href="/" class="btn btn-secondary">돌아가기</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        ''', item=item)
    else:
        return '<h1>해당 물품을 찾을 수 없습니다.</h1>'

# 데이터베이스 초기화 및 서버 실행
if __name__ == '__main__':
    # 서버 실행 전에 데이터베이스 초기화
    init_db()
    
    # static 폴더가 없으면 생성
    if not os.path.exists('static'):
        os.makedirs('static')

    # Flask 서버 실행
    app.run(host='0.0.0.0', port=5000, debug=True)
