import glob
import json

verified_ids=[]
with open('/Users/Meghna/Desktop/verified_accounts.json', 'rb') as u:
    for line1 in u:
        data1 = json.loads(line1)
        verified_ids.append(data1['user_id'])


with open('/Users/Meghna/Desktop/celebrities.json', 'rb') as u1,open('/Users/Meghna/Desktop/fake_celebrity_uids.json', 'a') as u2:
    for line in u1:
        data = json.loads(line)
        if data['user_id'] not in verified_ids:
            json.dump(data['user_id'],u2)
            u2.write('\n')
