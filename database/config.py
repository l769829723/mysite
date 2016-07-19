from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import os
DATABASE = os.path.join(os.path.dirname(__file__), 'mysite.db')

engine = create_engine('mysql://qiubai:qiubai@192.168.1.254:3306/qiubai?charset=utf8', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    import database.models
    Base.metadata.create_all(bind=engine)
