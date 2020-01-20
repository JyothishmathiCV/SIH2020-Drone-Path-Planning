from flask import Flask, request
from flask_restful import Resource, Api
import os,json
from distance import calculate
from raw2json import process
import algorithm
from cvman import readNcrop

app = Flask(__name__,static_folder="public")
api = Api(app)  



class HelloWorld(Resource):
    def get(self):
        return {"about" : "Hello World!"}
    def post(self):
        some_json = request.get_json()
        return {"you sent" : some_json}, 201
    


class UploadMultiple(Resource):
    def post(self):
        if request.files:
            files = request.files.getlist("files")
            print(files)
            print("Got it!!")
            for afile in files:
                diro=afile.filename.split(".")[0]
                if(not(os.path.isdir("./public/"+diro))):
                    os.mkdir("./public/"+diro)
                if(not(os.path.isfile("./public/"+diro+"/"+afile.filename))):
                    afile.save(os.path.join("public",diro,afile.filename))
            #os.system('Rscript grid_division.R '+os.path.abspath("./public/"+diro)+" "+diro+' > output.txt')
            readNcrop(os.path.abspath("./public/"+diro),diro)
            matrix,mapping_points,nrows,ncols=calculate(process("output.txt"))
            f=open("./public/"+diro+"/matrix.json","w")
            f.write(json.dumps({'matrix': matrix, 'mapping_points': mapping_points,'nrows':nrows,'ncols':ncols}))  
            f.close() 
            return {"image" : "public/"+diro+"/"+diro+"real.png"},200
        
        return {"about" : "FILE NOT SAVED"},403

# INPUT JSON FORMAT :
# {
#     speed : "",
#     life : "", //range
#     filename : "",
#     no_of_drones: xx,
#     charging_points: [[row,column,cellno],....],
# }
    
class AlgorithmCallee(Resource):
    def post(self):
        data_json = request.get_json()
        with open("public/"+data_json["filename"]+"/matrix.json","r") as f:
            data = json.loads(f.read())
        data_json['mapping_points'] = data['mapping_points']
        data_json["distance_matrix"] = data['matrix']
        data_json["nrows"] = data['nrows']
        data_json["ncols"] = data['ncols']
        routing_path = algorithm.main(data_json)
        # TODO
        # Modify the return according to the image parameters
        return {"drone_routes" : routing_path, "width": 'xx', "height" : 'xx', "grid_size": 'xx',"image" : 'xx'}, 200


api.add_resource(HelloWorld,'/')
api.add_resource(UploadMultiple,'/upload')
api.add_resource(AlgorithmCallee,'/call/<string:path>')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
