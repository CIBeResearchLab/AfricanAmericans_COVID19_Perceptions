from facepplib import FacePP
import json

facepp = FacePP(api_key='', api_secret='')


with open(test_images_no_celeb_path,'rb') as f:
    for line in f:
        line = json.loads(line)
        uid = line['user_id']
        url=str(line['image_url']).split('normal')
        final_url=url[0]+'400x400'+url[1]
        remote_image_url = final_url

        try:

            # Set image_url to the URL of an image that you want to analyze.
            image_url = remote_image_url

            image = facepp.image.get(image_url=image_url,return_attributes=['ethnicity','gender'])

            if len(image.faces) > 0 and image.faces[0].ethnicity['value']!='':
                print(image.faces[0].ethnicity)

        except:
            continue
