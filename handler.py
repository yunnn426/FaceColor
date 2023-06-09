import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import subprocess

# 인증 정보 파일 경로
cred = credentials.Certificate("mosa-352c3-firebase-adminsdk-ejd82-e440f24abb.json")

# 파이어베이스 앱 초기화
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mosa-352c3-default-rtdb.firebaseio.com/'
})

# Realtime Database 참조
ref = db.reference('/heandler')

def handle_value_added(event):
    print("new")
    value = event.data

    # 다른 파이썬 파일 호출
    subprocess.call(['python3', 'main.py', str(value)])

# 이벤트 감지를 위해 Realtime Database의 경로 모니터링
value_ref = ref

# 값 추가 이벤트 감지
value_ref.listen(handle_value_added)

# 이벤트 감지를 계속하기 위해 프로그램 실행 유지
while True:
    pass