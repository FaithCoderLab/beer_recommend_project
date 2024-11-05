# main.py
import gradio as gr
from camera import camera_on as co
from custom_vision import find_drink as fd
from beer_recommendation import recommend_beers
import numpy as np

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

def format_recommendations(recommendations):
    formatted = ""
    for beer in recommendations:
        formatted += f"이름: {beer['name']}\n"
        formatted += f"스타일: {beer['style']}\n"
        formatted += f"주요 맛: {beer['main_flavor']}\n"
        formatted += f"도수: {beer['abv']}%\n\n"
    return formatted

with gr.Blocks(theme=gr.themes.Citrus()) as demo:
    gr.HTML("<h1 style='text-align: center; margin-bottom: 1rem;'>Machulin Guide</h1>")
    
    with gr.Tabs():
        with gr.TabItem("이미지 인식 맥주 추천"):
            with gr.Column(scale=1, min_width=300):
                image_input = gr.Image(type="pil", label="Upload an Image", height=300)
                img_upload_button = gr.Button("이미지 업로드")
                output_text = gr.Textbox(label="인식된 맥주")
                img_upload_button.click(fn=fd, inputs=image_input, outputs=output_text)
                
                gr.Markdown("### 인식된 맥주와 유사한 맥주 추천")
                similar_beer_output = gr.Textbox(label="유사한 맥주 추천 결과")
                recommend_similar_button = gr.Button("유사한 맥주 추천")
                recommend_similar_button.click(
                    fn=lambda x: "유사한 맥주 추천 기능은 아직 구현되지 않았습니다.",
                    inputs=output_text,
                    outputs=similar_beer_output
                )

        with gr.TabItem("특성별 맥주 추천"):
            with gr.Column():
                alcohol_tolerance = gr.Radio(
                    ["a", "b", "c"], 
                    label="알코올 수용도", 
                    info="a: 알코올을 전혀 섭취하지 못해요\nb: 알코올에 예민하지만, 낮은 수준의 알코올 섭취는 좋아요\nc: 알코올에 크게 영향 받지 않아요"
                )
                bitter_rating = gr.Slider(0, 5, step=1, label="쓴맛 (Bitter)")
                sweet_rating = gr.Slider(0, 5, step=1, label="단맛 (Sweet)")
                sour_rating = gr.Slider(0, 5, step=1, label="신맛 (Sour)")
                fruity_rating = gr.Slider(0, 5, step=1, label="과일향 (Fruity)")
                hoppy_rating = gr.Slider(0, 5, step=1, label="홉향 (Hoppy)")
                spicy_rating = gr.Slider(0, 5, step=1, label="향신료향 (Spicy)")
                malty_rating = gr.Slider(0, 5, step=1, label="맥아향 (Malty)")
            
            recom_button = gr.Button("맥주 추천받기")
            recommendation_output = gr.Textbox(label="추천 맥주")
            
            recom_button.click(
                fn=lambda *args: format_recommendations(recommend_beers(*args)),
                inputs=[alcohol_tolerance, bitter_rating, sweet_rating, sour_rating,
                        fruity_rating, hoppy_rating, spicy_rating, malty_rating],
                outputs=recommendation_output
            )

if __name__ == "__main__":
    demo.launch(debug=True, share=True, inline=False, height=600)
