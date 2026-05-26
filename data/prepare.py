"""
data/raw/ 폴더 구조를 읽어 파인튜닝용 데이터셋을 생성.
폴더명 = 카드 라벨 (예: red_7, blue_skip, wild_draw_four)
"""

import os
import json
import cv2
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from models.vision import detect_card

RAW_DIR = Path(__file__).parent / "raw"
OUT_DIR = Path(__file__).parent / "processed"

LABEL_MAP = {
    # 빨강
    "red_0": "빨간 0",       "red_1": "빨간 1",       "red_2": "빨간 2",
    "red_3": "빨간 3",       "red_4": "빨간 4",       "red_5": "빨간 5",
    "red_6": "빨간 6",       "red_7": "빨간 7",       "red_8": "빨간 8",
    "red_9": "빨간 9",       "red_skip": "빨간 스킵", "red_reverse": "빨간 리버스",
    "red_draw_two": "빨간 드로우 투",
    # 파랑
    "blue_0": "파란 0",      "blue_1": "파란 1",      "blue_2": "파란 2",
    "blue_3": "파란 3",      "blue_4": "파란 4",      "blue_5": "파란 5",
    "blue_6": "파란 6",      "blue_7": "파란 7",      "blue_8": "파란 8",
    "blue_9": "파란 9",      "blue_skip": "파란 스킵","blue_reverse": "파란 리버스",
    "blue_draw_two": "파란 드로우 투",
    # 초록
    "green_0": "초록 0",     "green_1": "초록 1",     "green_2": "초록 2",
    "green_3": "초록 3",     "green_4": "초록 4",     "green_5": "초록 5",
    "green_6": "초록 6",     "green_7": "초록 7",     "green_8": "초록 8",
    "green_9": "초록 9",     "green_skip": "초록 스킵","green_reverse": "초록 리버스",
    "green_draw_two": "초록 드로우 투",
    # 노랑
    "yellow_0": "노란 0",    "yellow_1": "노란 1",    "yellow_2": "노란 2",
    "yellow_3": "노란 3",    "yellow_4": "노란 4",    "yellow_5": "노란 5",
    "yellow_6": "노란 6",    "yellow_7": "노란 7",    "yellow_8": "노란 8",
    "yellow_9": "노란 9",    "yellow_skip": "노란 스킵","yellow_reverse": "노란 리버스",
    "yellow_draw_two": "노란 드로우 투",
    # 와일드
    "wild": "와일드",
    "wild_draw_four": "와일드 드로우 포",
}


def process_image(img_path):
    """이미지 로드 후 카드 감지 시도. 실패하면 원본 그대로 사용."""
    frame = cv2.imread(str(img_path))
    if frame is None:
        return None

    cropped = detect_card(frame)
    return cropped if cropped is not None else frame


def prepare():
    OUT_DIR.mkdir(exist_ok=True)
    dataset = []
    skipped = []

    for folder in sorted(RAW_DIR.iterdir()):
        if not folder.is_dir():
            continue

        label_key = folder.name.lower()
        if label_key not in LABEL_MAP:
            print(f"[경고] 알 수 없는 폴더명 건너뜀: {folder.name}")
            skipped.append(folder.name)
            continue

        answer = LABEL_MAP[label_key]
        out_folder = OUT_DIR / label_key
        out_folder.mkdir(exist_ok=True)

        images = [f for f in folder.iterdir()
                  if f.suffix.lower() in (".jpg", ".jpeg", ".png")]

        for i, img_path in enumerate(images):
            processed = process_image(img_path)
            if processed is None:
                continue

            out_path = out_folder / f"{i:04d}.jpg"
            cv2.imwrite(str(out_path), processed)

            dataset.append({
                "image": str(out_path),
                "question": "이 UNO 카드는 무슨 카드야?",
                "answer": answer,
            })

        print(f"[완료] {folder.name} ({label_key}) → {len(images)}장")

    out_json = OUT_DIR / "dataset.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"\n총 {len(dataset)}장 처리 완료 → {out_json}")
    if skipped:
        print(f"건너뛴 폴더: {skipped}")


if __name__ == "__main__":
    prepare()
