# HuyenTranAUTO

Prototype **Automation + Recognition System** cho TFT AutoBuy.

## Những gì đã có trong bản này

- Data-driven Champion Database từ JSON (`config/champions.sample.json`).
- Shop Recognition interface (`ShopRecognitionEngine`) để plug-in template matching / feature matching.
- Decision Engine có logic ưu tiên:
  - Core/Carry
  - Gần lên sao (2⭐/3⭐)
  - Econ (gold thấp/cao)
  - Strategy mode (slow roll / fast 8 / reroll / flex)
  - Roll timing level 7 cho 3-cost
  - Contested penalty
- AutoClick Engine có:
  - Click tọa độ trung tâm icon
  - Human-like random delay
  - Fail-safe theo screen bounds
  - `dry_run` mode để test an toàn
- Controller + stats cho scan loop.

## Chạy demo

```bash
python3 main.py --strategy slow_roll --gold 34 --level 7
```

## Test

```bash
python3 -m pytest -q
```

## Gợi ý mở rộng tiếp theo

- Tích hợp OpenCV pipeline thực tế trong `autobuy/recognition.py`.
- OCR gold/level để bật Smart Econ tự động.
- Board + item recognition để nâng cấp decision engine thành bản pro.
