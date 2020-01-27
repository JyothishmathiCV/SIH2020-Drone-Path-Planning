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
        return {
"drone_routes":[[[0,5],[0,6],[0,7],[0,8],[0,11],[0,5]],
[[0,12],[1,3],[1,4],[1,5],[1,6],[0,12]],
[[3,5],[3,6],[3,7],[3,8],[3,9],[3,5]],
[[3,12],[3,13],[3,14],[3,15],[3,16],[3,12]]
],
"width":1080,
"height":1080,
"grid_size":[20,23]
}, 200
    


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
            os.system('Rscript grid_division.R '+os.path.abspath("./public/"+diro)+" "+diro+' > output.txt')
            readNcrop(os.path.abspath("./public/"+diro),diro)
            matrix,mapping_points,nrows,ncols=calculate(process("output.txt"))
            f=open("./public/"+diro+"/matrix.json","w")
            f.write(json.dumps({'matrix': matrix, 'mapping_points': mapping_points,'nrows':nrows,'ncols':ncols}))  
            f.close() 
            return {"image" : "public/"+diro+"/"+diro+"real.png"},200
        
        return {"about" : "FILE NOT SAVED"},403

# INPUT JSON FORMAT :

    
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
api.add_resource(AlgorithmCallee,'/call')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=3300)
