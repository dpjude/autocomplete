import json
import sys
import uuid
import random
import redis

redishost = '35.194.109.206'
#redishost = '192.168.56.2'
redisport = '6379'
conn0 = redis.StrictRedis(host=redishost, port=redisport, db=0)
conn1 = redis.StrictRedis(host=redishost, port=redisport, db=1)
json_data = './products.json'


def init_db0(json_data):
    with open(json_data, 'r') as f:
        data = json.load(f)
        for product in data:
            product_name = product['name']
            if product_name:
                conn0.zadd('product', 0, product_name.lower())
                for i in range(0,len(product_name)):
                    prefix = product_name[0:i+1].lower()
                    conn0.zadd(prefix, 0, product_name)
            else:
                continue
    return

    
def init_db1(json_data):
    with open(json_data, 'r') as f:
        data = json.load(f)
        for product in data:
            product_name = product['name']
            if product_name:
                conn1.zadd('product', random.randint(0,10000), product_name.lower())
                conn1.zadd('prefix', 0, product_name.lower() + '%')
                for i in range(0,len(product_name)):
                    prefix = product_name[0:i].lower()
                    conn1.zadd('prefix', 0, prefix)
            else:
                continue
    return

	
def complete(prefix):
    count = -1
    records = 0
    results = []
    grab = 42
    id = str(uuid.uuid4())
    print(id)
    
    start = conn1.zrank('prefix',prefix)
    if not start:
        return []
    while (records != count):
        range = conn1.zrange('prefix',start,start+grab-1)
        start += grab
        if not range or len(range) == 0:
            break
        for entry in range:
            entry = entry.decode("utf-8")
            minlen = min(len(entry),len(prefix))
            if entry[0:minlen] != prefix[0:minlen]:
                count = records
                break
            if entry[-1] == "%" and records != count:
                #print(entry)
                records += 1
                conn1.zadd('result' + id, 0, entry[0:-1])
  
    conn1.zinterstore('finalzset' + id, ['product', 'result' + id])
    final_result = conn1.zrevrangebyscore('finalzset' + id, '+inf', '-inf', start=0, num=10)
    
    for final_entry in final_result:
        results.append(final_entry.decode("utf-8"))
        if(len(results) >= 10):
            break
		
    conn1.expire('result' + id, 30)
    conn1.expire('finalzset' + id, 30)
      
    return results
    
	
def autocomplete_on_prefix(prefix):
    zset1 = conn0.zrange(prefix, 0, -1)
    results = []
    for entry in zset1:
        results.append(entry.decode("utf-8"))
    return results

	
def increase_score(product):
    conn0.zincrby('product', 1, product)
    return


def autoComplete():
  print(complete(sys.argv[1]))
  
    
if __name__ == '__main__':
    #init_db0(json_data)
    #init_db1(json_data)
    #autoComplete()