import urllib
from PIL import Image
import imghdr
import error_raise


def image_process(token, img_url, x_start, y_start, x_end, y_end,u_id):
    #store the img_url into the path
    urllib.request.urlretrieve(img_url,f"./static/icon{u_id}.jpg")
    imageObject = Image.open(f"./static/icon{u_id}.jpg")
    width,height = imageObject.size
    #
    if int(x_start)<0 or int(x_end)>width or int(y_start)<0 or int(y_end)>height:
     error_raise.user_profile_image_out_of_dimension()
    #crop and save
    cropped = imageObject.crop((int(x_start),int(y_start),int(x_end),int(y_end)))
    cropped.save(f"./static/icon{u_id}.jpg")
    #check if the type is right
    if imghdr.what(f"./static/icon{u_id}.jpg")!= 'jpeg':
     error_raise.user_profile_wrong_imagetype