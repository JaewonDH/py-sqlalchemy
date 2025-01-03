from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 데이터베이스 연결 설정 (예시: SQLite)
engine = create_engine('sqlite:///mydatabase.db',echo=True)
Base = declarative_base()


Session = sessionmaker(bind=engine)
# session = Session()

# # 모든 사용자 조회
# users = session.query(User).all()

# # 조회 결과 출력
# for user in users:
#     print(user.id, user.name, user.email)

# # 세션 종료
# session.close()


def init_db():
# 테이블 생성 (실제로는 한 번만 실행)
    Base.metadata.create_all(engine)
