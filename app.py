from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
client = MongoClient('mongodb://localhost', 27017)

db = client.project

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test', methods=['GET'])
def test_get():
    id = request.args.get('id')
    data_list = list(db.metadata.find({"id":id}, {'_id': False}))
    return jsonify({'metadata': data_list})


@app.route('/test', methods=['POST'])
def test_post():
    id = request.form['id']
    created_datetime = request.form['created_datetime']
    inference_result = request.form['inference_result']
    file_path = request.form['file_path']
    type = request.form['type']
    doc = {'id': id, 'created_datetime' : created_datetime, 'inference_result' : inference_result, 'file_path' : file_path, 'type' : type}
    db.metadata.insert_one(doc)
    return jsonify({'msg': '저장 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)