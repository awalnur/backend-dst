# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 25/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================

import redis

def create_redis():
  return redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
  )

pool = create_redis()
def get_redis():
  # Here, we re-use our connection pool
  # not creating a new one
  return redis.Redis(connection_pool=pool)
