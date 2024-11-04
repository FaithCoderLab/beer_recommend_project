import gradio as gr
from camera import camera_on as co
from custom_vision import find_drink as fd
import numpy as np


# def show_popup():
#     return gr.update(visible=True), gr.update(visible=True)

# def hide_popup():
#     return gr.update(visible=False), gr.update(visible=False)


with gr.Blocks() as demo:
    #카메라로 사진찍기 클릭 시 카메라 창 띄워주기
    with gr.Column(scale=1, min_width=300): #input related fields
        #이미지 업로드 관련 코드

        image_input = gr.Image(type="pil", label="Upload an Image", height=300)
        img_upload_button = gr.Button("이미지 업로드")
        output_text = gr.Textbox(label="Beer Name")
        img_upload_button.click(fn=fd, inputs=image_input, outputs=output_text)
        recom_button = gr.Button("비슷한 상품 보기")

if __name__ == "__main__":
    demo.launch(debug=True, share=True, inline=False, height=600)