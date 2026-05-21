import gradio as gr

def ping(message):
    return f"데스크탑 연결 성공! 받은 메시지: {message}"

demo = gr.Interface(
    fn=ping,
    inputs=gr.Textbox(label="테스트 메시지"),
    outputs=gr.Textbox(label="응답"),
    title="Board Game AI - 연결 테스트"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
