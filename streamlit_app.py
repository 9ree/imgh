import streamlit as st
from google.cloud import storage
import io

def upload_to_gcs(save_image_serviece, source_file, destination_blob_name):
    """Uploads a file to the Google Cloud Storage bucket."""
    
    # 스트림 위치를 시작으로 이동
    source_file.seek(0)
    
    # Google Cloud Storage 클라이언트 생성
    storage_client = storage.Client.from_service_account_json('/path/to/your-service-account-key.json')
    bucket = storage_client.bucket(save_image_serviece)
    blob = bucket.blob(destination_blob_name)
    
    # 파일 업로드
    blob.upload_from_file(source_file, content_type=source_file.type)
    
    # 공개 URL 반환
    return blob.public_url

# Streamlit 앱
st.title('이미지를 잠깐 보관해드릴게요!')

# 이미지 업로드
uploaded_file = st.file_uploader("이미지를 선택해주세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 이미지 표시
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    
    # 업로드할 파일의 이름
    file_name = uploaded_file.name

    # 업로드할 버킷 이름
    bucket_name = 'save_image_serviece'

    # Google Cloud Storage에 업로드할 파일의 경로
    destination_blob_name = f"images/{file_name}"

    # Google Cloud Storage에 업로드
    public_url = upload_to_gcs(save_image_serviece, uploaded_file, destination_blob_name)
    
    # 업로드 성공 메시지와 이미지 URL 표시
    st.write("Image uploaded successfully.")
    st.write(f"Image URL: {public_url}")
