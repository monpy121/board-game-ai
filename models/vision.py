import cv2
import numpy as np
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor

MODEL_ID = "meta-llama/Llama-3.2-11B-Vision-Instruct"

_model = None
_processor = None


def load_model():
    global _model, _processor
    if _model is not None:
        return

    print("Llama 3.2 Vision 모델 로딩 중...")
    _processor = AutoProcessor.from_pretrained(MODEL_ID)
    _model = MllamaForConditionalGeneration.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        load_in_4bit=True,
    )
    print("모델 로딩 완료")


def _order_points(pts):
    """사각형 꼭짓점을 좌상-우상-우하-좌하 순으로 정렬"""
    pts = pts.reshape(4, 2).astype("float32")
    ordered = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    ordered[0] = pts[np.argmin(s)]  # 좌상
    ordered[2] = pts[np.argmax(s)]  # 우하
    diff = np.diff(pts, axis=1)
    ordered[1] = pts[np.argmin(diff)]  # 우상
    ordered[3] = pts[np.argmax(diff)]  # 좌하
    return ordered


def detect_card(frame):
    """
    프레임에서 가장 가까운 카드 1장을 감지해 정면으로 crop한 이미지 반환.
    카드를 찾지 못하면 None 반환.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_contour = None
    best_area = 0

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) != 4:
            continue

        area = cv2.contourArea(approx)
        if area < 5000:  # 너무 작은 사각형 무시
            continue

        if area > best_area:
            best_area = area
            best_contour = approx

    if best_contour is None:
        return None

    # 원근 변환으로 카드 정면 펼치기
    ordered = _order_points(best_contour)
    tl, tr, br, bl = ordered

    width = int(max(
        np.linalg.norm(br - bl),
        np.linalg.norm(tr - tl)
    ))
    height = int(max(
        np.linalg.norm(tr - br),
        np.linalg.norm(tl - bl)
    ))

    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1],
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(ordered, dst)
    warped = cv2.warpPerspective(frame, matrix, (width, height))

    return warped


def identify_card(frame, game_name="UNO"):
    """
    프레임에서 카드를 감지하고 Llama로 카드 종류를 식별.
    반환: (카드 이름 문자열, crop된 카드 이미지) 또는 (None, None)
    """
    load_model()

    card_img = detect_card(frame)
    if card_img is None:
        return None, None

    pil_image = Image.fromarray(cv2.cvtColor(card_img, cv2.COLOR_BGR2RGB))

    prompt = (
        f"<|image|>\n"
        f"이것은 {game_name} 카드야. "
        f"카드의 색상과 종류를 간결하게 알려줘. "
        f"예시: '빨간 7', '파란 스킵', '와일드 드로우 포'"
    )

    inputs = _processor(
        text=prompt,
        images=pil_image,
        return_tensors="pt",
    ).to(_model.device)

    with torch.no_grad():
        output = _model.generate(**inputs, max_new_tokens=30)

    result = _processor.decode(output[0], skip_special_tokens=True)
    result = result.split("알려줘")[-1].strip()

    return result, card_img
