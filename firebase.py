import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# 인증 정보 파일 경로
cred = credentials.Certificate("mosa-352c3-firebase-adminsdk-ejd82-e440f24abb.json")

# 파이어베이스 앱 초기화
firebase_admin.initialize_app(cred, {
    'storageBucket': 'mosa-352c3.appspot.com'
}, name='storage')

# 스토리지 참조
bucket = storage.bucket(app=firebase_admin.get_app(name='storage'))

# 파일 목록 가져오기
files = bucket.list_blobs()

# 파일 이름 출력
for file in files:
    print(file.name)
    
# # 이미지 다운로드
# blob = bucket.blob('user_image/warm1.jpg')
# blob.download_to_filename('user_image/user.jpg')

# # 가져온 사진은 스토리지에서 삭제하기
# def delete_blob():    
#     blob = bucket.blob('pill_img/pill.png')
#     try:
#         blob.delete()
#         print(f"Blob pill.png deleted.")   
#     except:
#         print('404Err')