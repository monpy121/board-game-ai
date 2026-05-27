"""
Llama 3.2 Vision 11B LoRA 파인튜닝 (unsloth 사용)
data/processed/dataset.json 기반으로 UNO 카드 인식 특화 학습
"""

import json
from pathlib import Path
from PIL import Image
from torch.utils.data import Dataset as TorchDataset

from unsloth import FastVisionModel
from trl import SFTTrainer, SFTConfig
from unsloth.trainer import UnslothVisionDataCollator

MODEL_ID = "unsloth/Llama-3.2-11B-Vision-Instruct"
OUTPUT_DIR = Path(__file__).parent.parent / "models" / "finetuned"
DATASET_PATH = Path(__file__).parent.parent / "data" / "processed" / "dataset.json"


class CardDataset(TorchDataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        image = Image.open(item["image_path"]).convert("RGB")
        return {
            "images": [image],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {"type": "text", "text": item["question"]},
                    ],
                },
                {
                    "role": "assistant",
                    "content": [{"type": "text", "text": item["answer"]}],
                },
            ],
        }


def load_data():
    with open(DATASET_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return [
        {
            "image_path": item["image"],
            "question": item["question"],
            "answer": item["answer"],
        }
        for item in data
    ]


def train():
    # 모델 로드 (4비트 양자화 + LoRA)
    model, tokenizer = FastVisionModel.from_pretrained(
        MODEL_ID,
        load_in_4bit=True,
        use_gradient_checkpointing="unsloth",
    )

    model = FastVisionModel.get_peft_model(
        model,
        finetune_vision_layers=True,
        finetune_language_layers=True,
        finetune_attention_modules=True,
        finetune_mlp_modules=True,
        r=16,
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        random_state=42,
    )

    dataset = CardDataset(load_data())
    print(f"학습 데이터: {len(dataset)}장")

    FastVisionModel.for_training(model)

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        data_collator=UnslothVisionDataCollator(model, tokenizer),
        train_dataset=dataset,
        args=SFTConfig(
            output_dir=str(OUTPUT_DIR),
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            num_train_epochs=3,
            learning_rate=2e-4,
            warmup_steps=10,
            logging_steps=10,
            save_steps=100,
            fp16=False,
            bf16=True,
            optim="adamw_8bit",
            remove_unused_columns=False,
            dataset_text_field="",
            dataset_kwargs={"skip_prepare_dataset": True},
            report_to="none",
        ),
    )

    trainer.train()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(OUTPUT_DIR))
    tokenizer.save_pretrained(str(OUTPUT_DIR))
    print(f"모델 저장 완료 → {OUTPUT_DIR}")


if __name__ == "__main__":
    train()
