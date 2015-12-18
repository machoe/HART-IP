import redis

class RedisConnector():
    def __init__(self,host,port,db):
        self.host = host
        self.port = port
        self.db   = db
        
    def RedisConnect(self):
        try:
            Predis=redis.StrictRedis(host=self.host, port=self.port, db=self.db)
            Predis.ping()
            return 'Enable'
        except Exception,e:
            i=0
            print("Try connect redis again.\n")
            while(i<3):
                try:
                    Predis=redis.StrictRedis(host=RedisHOST, port=RedisPORT, db=RedisDB)
                    Predis.ping()
                    print("Succeed to re-connect Redis.\n")
                    return 'Enable'
                except Exception,e:
                    print("Error1-2:Faile to re-connect redis:\n%s" %e)
                    i+=1
                    time.sleep(2)
            return 'Unable' 
        
        