import io

import streamlit as st
from rembg import remove
from PIL import Image


# 배경색 적용 함수
def add_background(image, color):
    background = Image.new("RGBA", image.size, color)
    return Image.alpha_composite(background, image)


st.set_page_config(
    page_title="Image Background Remover",
    page_icon="🪄",
    layout="centered"
)

st.title("🪄 Image Background Remover")

st.write(
    "이미지를 업로드하면 배경을 자동으로 제거합니다."
)

uploaded_file = st.file_uploader(
    "이미지를 업로드하세요 (PNG / JPG / JPEG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    input_image = Image.open(uploaded_file).convert("RGBA")
    input_image.thumbnail((1500, 1500))

    with st.spinner("배경 제거 중입니다..."):
        output_image = remove(input_image)

    st.divider()

    bg_option = st.selectbox(
        "배경색 선택",
        ["투명", "흰색", "검정", "하늘색", "핑크색"]
    )

    if bg_option == "투명":
        final_image = output_image
    elif bg_option == "흰색":
        final_image = add_background(output_image, (255, 255, 255, 255))
    elif bg_option == "검정":
        final_image = add_background(output_image, (0, 0, 0, 255))
    elif bg_option == "하늘색":
        final_image = add_background(output_image, (173, 216, 230, 255))
    elif bg_option == "핑크색":
        final_image = add_background(output_image, (255, 192, 203, 255))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("원본")
        st.image(input_image, use_container_width=True)

    with col2:
        st.subheader("결과")
        st.image(final_image, use_container_width=True)

    st.divider()

    original_name = uploaded_file.name.rsplit(".", 1)[0]
    output_filename = f"{original_name}_edited.png"

    buf = io.BytesIO()
    final_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="이미지 다운로드",
        data=byte_im,
        file_name=output_filename,
        mime="image/png"
    )

    st.success("배경 제거가 완료되었습니다!")
