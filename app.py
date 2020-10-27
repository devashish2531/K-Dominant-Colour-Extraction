from flask import Flask,render_template,url_for,redirect,request
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import time

app=Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/home')
def hello2():
    return redirect('/')

@app.route('/submit',methods=['POST'])
def submitdata():
    if request.method == "POST":
        
        k=int(request.form['KValue'])
        
        if request.files:
            image = request.files["image"]
            #print(image)
            image.save(image.filename)
            #******************************************************************
            im=cv2.imread(image.filename)
            original_shape = im.shape
            im=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)

            all_pixels=im.reshape((-1,3))

            dominant_colors=k
            km=KMeans(n_clusters=dominant_colors)
            km.fit(all_pixels)
            centers=km.cluster_centers_
            centers=np.array(centers,dtype='uint8')
            i = 1
            colors = []
            for each_col in centers:
                i+=1
                colors.append(each_col)
             
                
            new_img = np.zeros((original_shape[0]*original_shape[1],3),dtype='uint8')
            for ix in range(new_img.shape[0]):
                new_img[ix] = colors[km.labels_[ix]]
                
            new_img = new_img.reshape((original_shape))
            date_string = time.strftime("%Y-%m-%d-%H:%M")
            print(date_string)
            plt.imsave('static/'+date_string+'.jpg', new_img)
            #*******************************************************************
            print("IMAGE STORED")
            return render_template('ExtractedImage.html',pathe= '/static/'+date_string+'.jpg')
        else :
            print("IMAGE NOT STORED")
            return redirect('/')
    #return redirect('/')


if __name__=='__main__':
    app.run()