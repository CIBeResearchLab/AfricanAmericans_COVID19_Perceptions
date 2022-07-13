import requests
import json

def sendRequest(url):
    try:
        page = requests.get(url)

    except Exception as e:
        print("error:", e)
        return False

    # check status code
    if (page.status_code != 200):
        return False

    return page

count=0
with open('unique_user_imageURL.json','rb') as f, open('modified_urls.json','a') as f1:
    for line in f:
        line = json.loads(line)
        url = str(line['image_url'])
		#print(sendRequest(url))
        if sendRequest(url)!=False:
            json.dump(line,f1)
            f1.write('\n')
        else:
            count+=1
print(f"No images for {count} URLs")
