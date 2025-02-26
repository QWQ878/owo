from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# 假設有一些借用的電腦資料，並且每台電腦有獨立的紀錄
computers = {i: {'status': '充電', 'records': []} for i in range(1, 13)}

def manage_records(computer_id):
    """管理紀錄，如果紀錄超過20條，刪除前10條"""
    records = computers[computer_id]['records']
    if len(records) > 20:
        computers[computer_id]['records'] = records[10:]  # 刪除前10條

@app.route('/')
def index():
    return render_template('index.html', computers=computers)

@app.route('/borrow/<int:computer_id>', methods=['POST'])
def borrow(computer_id):
    name = request.form.get('name')
    seat_number = request.form.get('seat_number')

    if computers[computer_id]['status'] == '充電':
        computers[computer_id]['status'] = '借用'
        record = f"{name}（座號: {seat_number}）借用電腦 {computer_id}，時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        computers[computer_id]['records'].append(record)
        manage_records(computer_id)  # 管理紀錄
    return redirect(url_for('index'))

@app.route('/return/<int:computer_id>', methods=['POST'])
def return_computer(computer_id):
    name = request.form.get('name')
    seat_number = request.form.get('seat_number')

    if computers[computer_id]['status'] == '借用':
        computers[computer_id]['status'] = '充電'
        record = f"{name}（座號: {seat_number}）歸還電腦 {computer_id}，時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        computers[computer_id]['records'].append(record)
        manage_records(computer_id)  # 管理紀錄
    return redirect(url_for('index'))

@app.route('/records/<int:computer_id>')
def view_records(computer_id):
    return render_template('records.html', computer_id=computer_id, records=computers[computer_id]['records'])

if __name__ == '__main__':
    app.run(debug=True)
