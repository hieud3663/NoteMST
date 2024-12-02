import requests
import time


def getTimeNow():
    utc_time = time.gmtime()
    utc_plus_7_time = time.localtime(time.mktime(utc_time) + 7 * 3600)
    time_now = time.strftime('%d-%m-20%y | %H:%M:%S', utc_plus_7_time)

    return time_now


def getData(): 
    re = requests.get('https://script.google.com/macros/s/AKfycbyq1ebcwlBtjdqO6hy2799SEFHjHzYvy8sJW4NrcSBof_Zi3qzzKqjEIqqE--HSmz1J3Q/exec').json()

    data = []
    for i in re:
        if i['id']:
            id = i['id']
            mst = i['mst']
            name = i['name']
            note = i['note']
            publishAt = i['time']


            data.append([id, mst, name, note, publishAt])
    
    return data
        

def postData(info):
    mst, name, note = info
    data= {'mst': str(mst), 'name': name, 'note': note, 'time': getTimeNow()}
    re2= requests.post('https://script.google.com/macros/s/AKfycbweTROT6fEmQXHw-4d3LtefxqDyNmiLpu2tZHsa8WLFcn13QLwGDoF0dAx420DJaFgPgg/exec', json = data).json()
    print(re2)
    return re2['code']


def editData(info):
    mst, name, note = info
    data= {'mst': str(mst), 'name': name, 'note': note, 'time': getTimeNow()}
    re2= requests.post('https://script.google.com/macros/s/AKfycbwBCnWW21IB5kPttzh_Tng-YzxFg9uX_YpsakTGFPk3llre46qPeCPoCNWX22cwtVkasA/exec', json = data).json()
    print(re2)
    return re2['code']


def getMSTInfo(mst):
    re = requests.get(f'https://api.vietqr.io/v2/business/{mst}').json()
    if re['code'] == '00':
        data = re['data']
        id = data['id']
        name = data['name']

        return id, name
    else:
        return None, None
    

# postData(("01234567890", "ádfgh", "test2324"))
# editData(('101300842', "test1", "hihihi"))
