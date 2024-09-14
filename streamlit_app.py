import streamlit as st
from google.cloud import storage
import io

def upload_to_gcs(bucket_name, source_file, destination_blob_name, service_account_key):
    """Uploads a file to the Google Cloud Storage bucket."""
    
    # 스트림 위치를 시작으로 이동
    source_file.seek(0)
    
    # Google Cloud Storage 클라이언트 생성
    storage_client = storage.Client.from_service_account_info(service_account_key)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    # 파일 업로드
    blob.upload_from_file(source_file, content_type=source_file.type)
    
    # 공개 URL 반환
    return blob.public_url

# Streamlit 앱
st.title('이미지를 호스팅해드립니다!')

# 서비스 계정 키 파일 업로드
service_account_key_file = st.file_uploader("서비스 계정 키 파일을 업로드하세요 (JSON)", type=["json"])

# 이미지 업로드
uploaded_file = st.file_uploader("이미지를 선택해주세요", type=["jpg", "jpeg", "png"])

if service_account_key_file is not None and uploaded_file is not None:
    # 이미지 표시
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    
    # 업로드할 파일의 이름
    file_name = uploaded_file.name

    # Google Cloud Storage에 업로드할 파일의 경로
    destination_blob_name = f"images/{file_name}"

    # Google Cloud Storage에 업로드
    bucket_name = 'save_image_serviece'  # 버킷 이름을 정확히 입력
    
    # 서비스 계정 키 파일 로드
    service_account_key = service_account_key_file.read()

    # 업로드
    public_url = upload_to_gcs(bucket_name, uploaded_file, destination_blob_name, service_account_key)
    
    # 업로드 성공 메시지와 이미지 URL 표시
    st.write("Image uploaded successfully.")
    st.write(f"Image URL: {public_url}")
