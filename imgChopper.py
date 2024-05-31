import os
from PIL import Image
def cropper(left = 475,right = 1300,top = 500,bottom = 680,img_src= "./static/rating_container.png" , second=False):
    img = Image.open(img_src)
    if second:
        cropped = img.crop((320 , 325 , 1300 , 500))
        print("second")
        
    else:
        cropped = img.crop((670 , 300 , 1650 , 650))
        print("first")
    cropped.show()
    cropped.save("./static/rating_final_2.png")
    
    return "./static/rating_final_2.png"
if __name__=="__main__":
    cropper()