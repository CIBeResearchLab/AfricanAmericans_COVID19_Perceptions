import gzip
import glob
import json
import emoji
import re

path='/Users/Meghna/Desktop/Twitter_Covid_Data/*.json.gz'
files=glob.glob(path)

users = set()
names=[]
profile_names = {}
c = 0 # Reference for unique users
j = 0 # Reference for duplicate users
count=0

def get_emoji_free_text(text):
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text

def deEmojify(text):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', text)

surname_mappings={
	'YODER':'NON-HISPANIC WHITE',
	'FRIEDMAN':'NON-HISPANIC WHITE',
	'KRUEGER':'NON-HISPANIC WHITE',
	'SCHWARTZ':'NON-HISPANIC WHITE',
	'SCHMITT':'NON-HISPANIC WHITE',
	'MUELLER':'NON-HISPANIC WHITE',
	'WEISS':'NON-HISPANIC WHITE',
	'NOVAK':'NON-HISPANIC WHITE',
	'OCONNELL':'NON-HISPANIC WHITE',
	'KLEIN':'NON-HISPANIC WHITE',
	'LOWERY': 'NON-HISPANIC AMERICAN INDIAN AND ALASKA NATIVE',
	'HUNT': 'NON-HISPANIC AMERICAN INDIAN AND ALASKA NATIVE',
	'SAMPSON': 'NON-HISPANIC AMERICAN INDIAN AND ALASKA NATIVE',
	'JACOBS': 'NON-HISPANIC AMERICAN INDIAN AND ALASKA NATIVE',
	'MOSES': 'NON-HISPANIC AMERICAN INDIAN AND ALASKA NATIVE',
	'LUCERO': 'NON-HISPANIC AMERICAN INDIAN AND ALASKA NATIVE',
	'JAMES': 'NON-HISPANIC AMERICAN INDIAN AND ALASKA NATIVE',
	'PROCTOR': 'NON-HISPANIC AMERICAN INDIAN AND ALASKA NATIVE',
	'ASHLEY': 'NON-HISPANIC AMERICAN INDIAN AND ALASKA NATIVE',
	'CUMMINGS':'NON-HISPANIC AMERICAN INDIAN AND ALASKA NATIVE',
	'WASHINGTON':'NON-HISPANIC BLACK OR AFRICAN AMERICAN',
	'JEFFERSON':'NON-HISPANIC BLACK OR AFRICAN AMERICAN',
	'BOOKER':'NON-HISPANIC BLACK OR AFRICAN AMERICAN',
	'BANKS':'NON-HISPANIC BLACK OR AFRICAN AMERICAN',
	'JOSEPH':'NON-HISPANIC BLACK OR AFRICAN AMERICAN',
	'MOSLEY':'NON-HISPANIC BLACK OR AFRICAN AMERICAN',
	'JACKSON':'NON-HISPANIC BLACK OR AFRICAN AMERICAN',
	'CHARLES': 'NON-HISPANIC BLACK OR AFRICAN AMERICAN',
	'DORSEY': 'NON-HISPANIC BLACK OR AFRICAN AMERICAN',
	'RIVERS':'NON-HISPANIC BLACK OR AFRICAN AMERICAN',
	'ALI':'NON-HISPANIC TWO OR MORE RACES',
	'KHAN':'NON-HISPANIC TWO OR MORE RACES',
	'WONG':'NON-HISPANIC TWO OR MORE RACES',
	'SINGH':'NON-HISPANIC TWO OR MORE RACES',
	'CHANG':'NON-HISPANIC TWO OR MORE RACES',
	'CHUNG':'NON-HISPANIC TWO OR MORE RACES',
	'AHMED': 'NON-HISPANIC TWO OR MORE RACES',
	'WASHINGTON':'NON-HISPANIC TWO OR MORE RACES',
	'BOOKER':'NON-HISPANIC TWO OR MORE RACES',
	'JEFFERSON':'NON-HISPANIC TWO OR MORE RACES',
	'XIONG':'NON-HISPANIC ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'ZHANG':'NON-HISPANIC ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'HUANG':'NON-HISPANIC ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'TRUONG':'NON-HISPANIC ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'YANG':'NON-HISPANIC ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'LI':'NON-HISPANIC ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'VANG':'NON-HISPANIC ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'HUYNH':'NON-HISPANIC ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'VU':'NON-HISPANIC ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'NGUYEN':'NON-HISPANIC ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'BARAJAS':'HISPANIC OR LATINO ORIGIN',
	'ZAVALA':'HISPANIC OR LATINO ORIGIN',
	'VELAZQUEZ':'HISPANIC OR LATINO ORIGIN',
	'AVALOS':'HISPANIC OR LATINO ORIGIN',
	'OROZCO':'HISPANIC OR LATINO ORIGIN',
	'VAZQUEZ':'HISPANIC OR LATINO ORIGIN',
	'JUAREZ':'HISPANIC OR LATINO ORIGIN',
	'MEZA':'HISPANIC OR LATINO ORIGIN',
	'HUERTA':'HISPANIC OR LATINO ORIGIN',
	'IBARRA':'HISPANIC OR LATINO ORIGIN',
	'ZHANG': 'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'LI':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'ALI':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER AND BLACK OR AFRICAN AMERICAN',
	'LIU':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'KHAN':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'VAZQUEZ':'HISPANIC OR LATINO ORIGIN',
	'WANG':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'HUANG':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'LIN':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'SINGH':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'CHEN':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'BAUTISTA':'HISPANIC OR LATINO ORIGIN',
	'VELAZQUEZ':'HISPANIC OR LATINO ORIGIN',
	'PATEL':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'WU':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'SMITH':'WHITE',
	'JOHNSON':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'WILLIAMS':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'BROWN':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'JONES':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'GARCIA':'HISPANIC OR LATINO ORIGIN',
	'MILLER':'WHITE',
	'DAVIS':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'RODRIGUEZ':'HISPANIC OR LATINO ORIGIN',
	'MARTINEZ':'HISPANIC OR LATINO ORIGIN',
	'HERNANDEZ':'HISPANIC OR LATINO ORIGIN',
	'LOPEZ':'HISPANIC OR LATINO ORIGIN',
	'GONZALEZ':'HISPANIC OR LATINO ORIGIN',
	'WILSON':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'ANDERSON':'WHITE',
	'THOMAS':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'TAYLOR':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'MOORE':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'JACKSON':'BLACK OR AFRICAN AMERICAN OR WHITE',
	'MARTIN':'WHITE',
	'LEE':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER OR WHITE',
	'PEREZ':'HISPANIC OR LATINO ORIGIN',
	'THOMPSON':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'WHITE':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'HARRIS':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'SANCHEZ':'HISPANIC OR LATINO ORIGIN',
	'CLARK':'WHITE',
	'RAMIREZ':'HISPANIC OR LATINO ORIGIN',
	'LEWIS':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'ROBINSO':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'WALKER':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'YOUNG':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'ALLEN':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'KING':'WHITE',
	'WRIGHT':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'SCOTT':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'TORRES':'HISPANIC OR LATINO ORIGIN',
	'NGUYEN':'ASIAN AND NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
	'HILL':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'FLORES':'HISPANIC OR LATINO ORIGIN',
	'GREEN':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'ADAMS':'WHITE',
	'NELSON':'WHITE',
	'BAKER':'WHITE',
	'HALL':'WHITE',
	'RIVERA':'HISPANIC OR LATINO ORIGIN',
	'CAMPBELL':'WHITE',
	'MITCHELL':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'CARTER':'WHITE OR BLACK OR AFRICAN AMERICAN',
	'ROBERTS':'WHITE'
}

with open('user_surnames_and_tweets.json','a') as u:
    for i in range(len(files)):
        print("opening file", files[i])
        try:
            with gzip.open(files[i],'rb') as fin:
                for line in fin:
                    tweet=json.loads(line)
                    try:
                        uid = tweet['user']['id_str']
                    except:
                        continue

                    if uid in users:
                        j = j + 1
                        continue

                    users.add(uid)
                    c = c + 1
                    profile_names['user_id'] = uid
                    raw_name=tweet['user']['name'].lower()
                    name=deEmojify(raw_name).split()
                    profile_names['profile_name'] = tweet['user']['name']
                    for pname in range(len(profile_names['profile_name'])):
                        if profile_names['profile_name'][pname] in ([p.lower() for p in list(surname_mappings.keys())]):
                        	profile_names['race']=surname_mappings[profile_names['profile_name'][pname].upper()].lower()
                    if len(profile_names.keys())==2:
                        profile_names['race']='Unknown'
                        count+=1
                    profile_names['tweet_text']=tweet['text']
                    profile_names['hashtags']=tweet['entities']['hashtags']
                    json.dump(profile_names,u)
                    u.write('\n')
                    profile_names.clear()
                    name.clear()
                    print(c)
            print(f"Written for file {files[i]}")
        except:
            print("Faulty file ", files[i])

print("here are duplicates ",j)
print("Surnames with no mappings ",count)
