import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore

cred = "None"
text_list = "None"
user_name = "None"
user_list = "None"
user = "None"

def start():
    # 인증 정보 파일 경로
    global cred
    cred = credentials.Certificate("mosa-352c3-firebase-adminsdk-ejd82-e440f24abb.json")

    # 파이어베이스 앱 초기화
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'mosa-352c3.appspot.com'
    }, name='storage')


    # 스토리지 참조
    bucket = storage.bucket(app=firebase_admin.get_app(name='storage'))

    # 스토리지에서 파일 리스트 가져오기
    # bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix='user_image/')
    # blobs는 해당 폴더 내 모든 파일 리스트를 가지고 있습니다.

    # 가장 최근 파일 찾기
    latest_time = None
    latest_blob = None
    for blob in blobs:
        if not latest_time or blob.time_created > latest_time:
            latest_time = blob.time_created
            latest_blob = blob

    # 가장 최근 파일 다운로드
    if latest_blob:
        latest_blob.download_to_filename('user_image/user.jpg')
        
    ## 최근 파일 이름 가져오기 위한 코드
    # 파일 목록 가져오기
    files = bucket.list_blobs(prefix='user_image/')

    # 파일 목록 정렬하기
    files = sorted(files, key=lambda x: x.time_created, reverse=True)

    # 가장 최근 파일 이름 출력
    if files:
        file_name = files[0].name
    else:
        print('폴더에 파일이 없습니다.')
        
    global text_list, user_name, user_list, user
    text_list = file_name.split("/", 1) 
    user_name = text_list[1]
    user_list = user_name.split("_",1)
    user = user_list[0]
    # user가 최근파일을 올린 아이디입니당.


def result(color):
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    #결과값 가져오기
    color_result = color
    face_result = "b"

    # 추가할 데이터 생성
    data = {
        'file_name' : user_name,
        'color_result': color_result,
        'face_result' : "b"
    }

    # 사용자별 컬렉션에 데이터 추가
    db.collection(f"{user}_color_result").add(data)