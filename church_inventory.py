import sqlite3
import qrcode
from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)

# 데이터베이스 파일 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'church_items.db')

# 1. 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (item_id, item_name, manager, department, borrow_date, is_borrowed) VALUES (?, ?, ?, ?, ?, ?)",
                   (item_id, item_name, manager, department, borrow_date, is_borrowed))
    conn.commit()
    conn.close()

# 3. 물품 조회
def get_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE item_id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

# 4. 물품 삭제
def delete_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
    conn.commit()
    conn.close()

# 5. QR 코드 생성 (URL 포함)
def create_qr_code(item_id):
    server_ip = "your-server-ip"
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

# 6. 홈페이지 라우팅
@app.route('/')
def homepage():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <title>교회 물품 관리 시스템</title>
        <style>
            body { padding-top: 50px; }
            .main-container { max-width: 900px; margin: 0 auto; }
            h1 { text-align: center; margin-bottom: 30px; }
            .nav-item { margin-bottom: 15px; }
        </style>
    </head>
    <body>
        <div class="container main-container">
            <h1>교회 물품 관리 시스템</h1>
            <ul class="list-group">
                <li class="list-group-item nav-item">
                    <a href="/add_item" class="btn btn-primary btn-block">물품 추가</a>
                </li>
                <li class="list-group-item nav-item">
                    <a href="/search" class="btn btn-secondary btn-block">물품 검색</a>
                </li>
                <li class="list-group-item nav-item">
                    <a href="/delete_item" class="btn btn-danger btn-block">물품 삭제</a>
                </li>
                <li class="list-group-item nav-item">
                    <a href="/view_items" class="btn btn-info btn-block">모든 물품 조회</a>
                </li>
            </ul>
        </div>
    </body>
    </html>
    ''')

# 7. 물품 추가
@app.route('/add_item', methods=['GET', 'POST'])
def add_item_route():
    if request.method == 'POST':
        item_id = request.form['item_id']
        item_name = request.form['item_name']
        manager = request.form['manager']
        department = request.form['department']
        borrow_date = request.form['borrow_date']
        is_borrowed = int(request.form['is_borrowed'])

        add_item(item_id, item_name, manager, department, borrow_date, is_borrowed)
        qr_image_path = create_qr_code(item_id)

        return render_template_string('''
        <h1>물품이 성공적으로 추가되었습니다!</h1>
        <p>QR 코드:</p>
        <img src="/{{ qr_image_path }}" alt="QR Code" style="max-width: 300px;">
        <br><br>
        <a href="/">홈으로 돌아가기</a>
        ''', qr_image_path=qr_image_path)
    
    return render_template_string('''
    <form method="POST">
        <div class="form-group">
            <label for="item_id">물품 ID</label>
            <input type="text" class="form-control" id="item_id" name="item_id" required>
        </div>
        <div class="form-group">
            <label for="item_name">물품 이름</label>
            <input type="text" class="form-control" id="item_name" name="item_name" required>
        </div>
        <div class="form-group">
            <label for="manager">관리인</label>
            <input type="text" class="form-control" id="manager" name="manager" required>
        </div>
        <div class="form-group">
            <label for="department">부서</label>
            <input type="text" class="form-control" id="department" name="department" required>
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
        <button type="submit" class="btn btn-primary">물품 추가</button>
    </form>
    <a href="/">홈으로 돌아가기</a>
    ''')

# 8. 물품 검색
@app.route('/search', methods=['GET', 'POST'])
def search_item():
    if request.method == 'POST':
        search_term = request.form['search_term']
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE item_id = ? OR item_name LIKE ?", (search_term, f"%{search_term}%"))
        item = cursor.fetchone()
        conn.close()

        if item:
            return render_template_string('''
            <h1>물품 조회 결과</h1>
            <p><strong>물품 ID:</strong> {{ item[0] }}</p>
            <p><strong>물품 이름:</strong> {{ item[1] }}</p>
            <p><strong>관리인:</strong> {{ item[2] }}</p>
            <p><strong>부서:</strong> {{ item[3] }}</p>
            <p><strong>대여 날짜:</strong> {{ item[4] }}</p>
            <p><strong>대여 상태:</strong> {{ '대여 중' if item[5] == 1 else '반납됨' }}</p>
            <a href="/">홈으로 돌아가기</a>
            ''', item=item)
        else:
            return '<h1>해당 물품을 찾을 수 없습니다.</h1><a href="/">홈으로 돌아가기</a>'
    
    return '''
    <form method="POST" action="/search">
        <input type="text" name="search_term" placeholder="물품 ID 또는 이름 입력" required>
        <input type="submit" value="검색">
    </form>
    <a href="/">홈으로 돌아가기</a>
    '''

# 9. 물품 삭제
@app.route('/delete_item', methods=['GET', 'POST'])
def delete_item_route():
    if request.method == 'POST':
        item_id = request.form['item_id']
        delete_item(item_id)
        return f"<h1>물품 {item_id} 삭제 완료</h1><a href='/'>홈으로 돌아가기</a>"
    
    return '''
    <form method="POST" action="/delete_item">
        <input type="text" name="item_id" placeholder="삭제할 물품 ID 입력" required>
        <input type="submit" value="삭제">
    </form>
    <a href="/">홈으로 돌아가기</a>
    '''

# 데이터베이스 초기화 및 서버 실행
if __name__ == '__main__':
    init_db()
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(host='0.0.0.0', port=5000, debug=True)
