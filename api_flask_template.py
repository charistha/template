from crypt import methods
from distutils.util import execute
from logging import exception
from flask import Flask, request, jsonify, make_response, request_tearing_down
import pymysql

app = Flask(__name__)
mydb = pymysql.connect(
    host= 'localhost',
    user='root',
    passwd='',
    database='db_sekolah'
)

@app.route('/')

@app.route('/index')
def index():
    return 'this is index'

# query to show data
@app.route('get_student_data',methods=['GET'])
def get_student_data():
    query = 'SELECT * FROM tb_siswa WHERE 1=1'
    values = ()
    
    nis = request.args.get('nis')
    nama = request.args.get('nama')
    alamat = request.args.get('alamat')

    if nis:
        query += ' AND nis=%s'
        values += (nis,)
    if nama:
        query += 'AND nama LIKE %s'
        values +=('%'+nama+'%',) 
    if alamat:
        query += 'AND alamat LIKE %s'
        values +=('%'+alamat+'%',) 

    mycursor = mydb.cursor()
    mycursor.execute(query, values)
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    return make_response(jsonify(json_data),200)

#query fill/insert data
@app.route('/insert_student_data', methods=['POST'])
def insert_student_data():
    hasil = {'status':'failed to insert data'}

    try:
        data =  request.json
        query = 'INSERT INTO tb_siswa(nis,nama,alamat) values(%s,%s,%s)'
        values = (data['nis'],data['nama'],data['alamat'],)
        mycursor = mydb.cursor()
        mycursor.execute(query, values)
        mydb.commit()
        hasil = {'status': 'success insert data'}
    except Exception as e:
        print('Error:' + str(e))
    return jsonify(hasil)


#query update data
@app.route('/update_student_data', methods=['PUT'])
def update_student_data():
    hasil =  {'status': 'failed to update data'}

    try:
        data = request.json
        nis_awal = data['nis_awal']

        query ='UPDATE tb_siswa SET nis = %s'
        values = (nis_awal, )

        if "nis_ubah" in data:
            query += ",nis = %s"
            values += (data["nis_ubah"],) 
        
        if "nama" in data:
            query += ",nama = %s"
            values += (data["nama"],) 
        
        if "alamat" in data:
            query += ",alamat = %s"
            values += (data["alamat"],) 

        query += 'WHERE nis = %s'
        values +=(nis_awal,)
        mycursor = mydb.cursor()
        mycursor.execute(query, values)
        mydb.commit()
        hasil = {'status': 'success update data'}
    except Exception as e:
        print('Error:' + str(e))
    return jsonify(hasil)

#query API to delete data
@app.route('/delete_student_data/<nis>', methods=['DELETE'])
def delete_student_data():
    hasil = {'status': 'gagal hapus data siswa'}
    
    try:
        data = request.json
        query = 'DELETE FROM tb_siswa WHERE nis=%s'
        values = (nis,)
        mycursor = mydb.cursor()
        mycursor.execute(query, values)
        mydb.commit()
        hasil = {'status': 'success delete data'}
    except Exception as e:
        print('Error:' + str(e))
    return jsonify(hasil)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)