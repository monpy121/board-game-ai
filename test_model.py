"""
파인튜닝된 LoRA 모델 테스트 — 이미지 업로드 -> 카드 인식 결과 출력
실행: (board-game-ai 환경) python test_model.py
접속: http://localhost:7860
"""

from pathlib import Path
import torch
import gradio as gr
from unsloth import FastVisionModel

ADAPTER_PATH = str(Path(__file__).parent / "models" / "finetuned")
QUESTION = "이 UNO 카드는 무슨 카드야?"

model = None
tokenizer = None


def load_model():
    global model, tokenizer
    if model is not None:
        return

    print("모델 로딩 중...")
    model, tokenizer = FastVisionModel.from_pretrained(
        ADAPTER_PATH,
        load_in_4bit=True,
    )
    FastVisionModel.for_inference(model)
    print("모델 로딩 완료")


def predict(image):
    load_model()

    if image is None:
        return "이미지를 업로드해주세요."

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": QUESTION},
            ],
        }
    ]

    input_text = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
    inputs = tokenizer(
        image,
        input_text,
        add_special_tokens=False,
        return_tensors="pt",
    ).to("cuda")

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=32,
            temperature=1.0,
            do_sample=False,
        )

    # 입력 토큰 제거 후 응답만 디코딩
    input_len = inputs["input_ids"].shape[1]
    answer = tokenizer.decode(output_ids[0][input_len:], skip_special_tokens=True).strip()
    return answer


demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil", label="UNO 카드 이미지"),
    outputs=gr.Textbox(label="인식 결과"),
    title="UNO 카드 인식 테스트",
    description="파인튜닝된 Llama 3.2 Vision LoRA 모델 테스트. 초록 카드만 학습되어 있음.",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
