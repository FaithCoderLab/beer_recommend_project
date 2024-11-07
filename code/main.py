import gradio as gr
#from camera import camera_on as co
from custom_vision import find_drink as fd
from beer_recommend import find_beer_and_recommend as fbr

custom_css = """
.gradio-container {
    font-family: 'Arial', sans-serif;
}
.feedback textarea {
    font-size: 18px !important;
    border-radius: 10px;
}"""

custom_js = """
function addWelcomeAnimation() {
    const welcome = document.createElement('div');
    welcome.textContent = 'Welcome to Machulin Guide!';
    welcome.style.fontSize = '24px';
    welcome.style.textAlign = 'center';
    welcome.style.marginBottom = '20px';
    document.querySelector('.gradio-container').prepend(welcome);
}"""

with gr.Blocks(theme=gr.themes.Citrus()) as demo:
    #카메라로 사진찍기 클릭 시 카메라 창 띄워주기
    with gr.Column(scale=1, min_width=300):
        
        #이미지 업로드 관련 코드
        image_input = gr.Image(type="pil", label="Upload an Image", height=300)
        img_upload_button = gr.Button("이미지 업로드")
        beer_info_text = gr.Textbox(label="Beer Information")
        img_upload_button.click(fn=fd, inputs=image_input, outputs=beer_info_text)
        recom_button = gr.Button("비슷한 상품 보기")
        beer_rec_text = gr.Textbox(label="Beer Recommendation")
        recom_button.click(fn=fbr, inputs=beer_info_text, outputs=beer_rec_text)

if __name__ == "__main__":
    demo.launch(debug=True, share=True, inline=False, height=600)
