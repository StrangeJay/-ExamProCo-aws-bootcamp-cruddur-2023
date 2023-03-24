from datetime import datetime, timedelta, timezone
from opentelemetry import trace

# import connection pool
from lib.db import pool 

# import logging  

tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run(cognito_user_id=None):
    # logger.info("HomeActivities")
    with tracer.start_as_current_span("home-activities-mock-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())    
      
      # Connection pool for psycopg 
      sql = """
      SELELECT * FROM activities
      """  
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchall()
      return json[0]
      return results
    
    
   
    