from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>' - bad practice
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)

Base = declarative_base()

#responsible for talking to the databases
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''      
while True:
        
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres',password='postgres',
                                cursor_factory=RealDictCursor)#to add the column name)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to the data base failed")
        print("Error: ", error)
        time.sleep(2)
'''