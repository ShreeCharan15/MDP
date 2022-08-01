from flask import Flask, jsonify, request
from nst import NST
import os
import datetime
nst=NST()
# creating a Flask app
app = Flask(__name__)
@app.route('/', methods = ['POST'])
def home():
    styles={'Kandinsky':'kandinsky.jpg',
      'Scream':'scream.jpg',
      'Starry Night':'starrynight.jpg',
      'Sunset':'tree.jpg',
      'Waves':'waves.png',
      'Edtaonisl':'edtaonisl.jpg',
      'Build':'build.jpg',
      'Candy':'candy.jpg',
      'Cubist':'cubist.jpg',
      'Fur':'fur.jpg',
      'Hundertwasser':'hundertwasser.jpg',}
    content_path=request.get_json()['path']
    
    locs={}
    fold=request.get_json()['fold']
    print("path",content_path, "fold",fold)
    directory = fold
    parent_dir = "C:/Users/Shree Charan/NSTIMAGES/"
    path = os.path.join(parent_dir, directory)
    if not os.path.exists(path):
      os.mkdir(path)
    for key,value in styles.items():
        loc=nst.convertImage(content_path,style_path='./styles/'+value,save_path=path)
        locs[key]=loc
    
    return jsonify(locs)
  
# driver function
if __name__ == '__main__':
    app.run(debug = True)