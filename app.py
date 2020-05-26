from flask_restful import Resource, Api
from flask import Flask, Response, json, jsonify, request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#ilham akhsani (18090044)
#minal aidin waldfaidzin pak,mohon maaf lahir dan batin
app = Flask(__name__)
api = Api(app)
#koneksi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/remidi'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

#class/model data mahasiswa
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(10), unique=True)
    nama = db.Column(db.String(25))
    kelas = db.Column(db.String(10))
    alamat = db.Column(db.String(52))

    def __init__(self, nim, nama, kelas, alamat):
        self.nim = nim
        self.nama = nama
        self.kelas = kelas
        self.alamat = alamat

    #method mengambil semua data
    @staticmethod
    def get_all_dataSemua():
        return Data.query.all()

#class data schema
class DataSchema(ma.Schema):
    class Meta:
        # Fields
        fields = ('id', 'nim', 'nama', 'kelas', 'alamat')


data_schema = DataSchema()
dataSemua_schema = DataSchema(many=True)

#clas/model data api
class DataApi(Resource):
    #method get
    def get(self, id=None):
        if id is not None:
            data = Data.query.get(id)
            result = data_schema.dump(data)
            return jsonify(result)
        else:
            all_data = Data.get_all_dataSemua()
            result = dataSemua_schema.dump(all_data)
            return jsonify(result)
    #method Post
    def post(self):
        if not request.json or not 'nim ' in request.json and not 'nama' in request.json and not 'kelas' in request.json and not 'alamat' in request.json:
            abort(400)

        data = Data(request.json['nim'], request.json['nama'], request.json['kelas'], request.json['alamat'])
        db.session.add(data)
        db.session.commit()

        result = data_schema.dump(data)
        return jsonify(result)
    #Method put
    def put(self, id):
        if not request.json or not 'nim ' in request.json and not 'nama' in request.json and not 'kelas' in request.json and not 'alamat' in request.json:
            abort(400)

        data = Data.query.get(id)
        data.nim = request.json['nim']
        data.nama = request.json['nama']
        data.kelas = request.json['kelas']
        data.alamat = request.json['alamat']
        db.session.commit()

        result = data_schema.dump(data)
        return jsonify(result)
    #method Delete
    def delete(self, id):
        data = Data.query.get(id)
        db.session.delete(data)
        db.session.commit()

        return jsonify()


api.add_resource(DataApi, '/data/', '/data/<int:id>/', endpoint='data_ep')

# Run Server
if __name__ == '__main__':
    app.run()

#get seluruh data http://127.0.0.1:5000/data
#get data berdasarkan ID http://127.0.0.1:5000/data/4
#post data http://127.0.0.1:5000/data
#put/ubah data berdasarkan id http://127.0.0.1:5000/data/4
#delete data berdasarkan id  http://127.0.0.1:5000/data/4