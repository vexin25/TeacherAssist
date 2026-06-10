#!/usr/bin/env python3
"""煙霧測試：端對端驗證 /api/generate 對所有 8 個模板回傳 success=True。

前置條件：伺服器必須已在 http://localhost:8000 執行。
    cd txt2pptx && OLLAMA_MODEL=gpt-oss:20b bash start.sh

執行方式（從專案根目錄）：
    python test/smoke_api.py

成功時 exit 0，任一模板失敗時 exit 1。
"""
import json
import sys
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 900  # Ollama CPU 推理可能需要較長時間

PAYLOAD = {
    "text": (
        "人工智慧（AI）正在革命性地改變各行各業。"
        "從醫療診斷到自動駕駛，AI 的應用無所不在。"
        "本簡報將介紹 AI 的核心技術、主要應用領域及未來發展趨勢。"
    ),
    "num_slides": 5,
    "language": "zh-TW",
    "style": "professional",
}

TEMPLATES = [
    ("ocean_gradient",        "預設版面"),
    ("College_Elegance",      "學院典雅"),
    ("Data_Centric",          "數據導向"),
    ("High_Contrast",         "高調對比"),
    ("Minimalist_Corporate",  "極簡商務"),
    ("Modernist",             "摩登現代"),
    ("Startup_Edge",          "新創活力"),
    ("Zen_Serenity",          "靜謐禪意"),
]


def check_health() -> bool:
    try:
        with urllib.request.urlopen(f"{BASE_URL}/api/health", timeout=5) as r:
            data = json.loads(r.read())
            return data.get("status") == "ok"
    except Exception:
        return False


def generate(template_id: str) -> dict:
    body = dict(PAYLOAD, template=template_id)
    req = urllib.request.Request(
        f"{BASE_URL}/api/generate",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read())


def main() -> int:
    print("=" * 60)
    print("Smoke Test: API /api/generate — 所有模板")
    print("=" * 60)

    if not check_health():
        print("[ERROR] 伺服器未回應，請先啟動：")
        print("  cd txt2pptx && OLLAMA_MODEL=gpt-oss:20b bash start.sh")
        return 1

    print(f"伺服器正常，開始測試 {len(TEMPLATES)} 個模板...\n")

    passed, failed = 0, 0
    for template_id, name in TEMPLATES:
        label = f"[{template_id}] {name}"
        print(f"  測試 {label}...", end=" ", flush=True)
        try:
            data = generate(template_id)
            if data.get("success"):
                print(f"PASS  (file={data.get('filename')})")
                passed += 1
            else:
                print(f"FAIL  (message={data.get('message')})")
                failed += 1
        except urllib.error.HTTPError as e:
            print(f"FAIL  (HTTP {e.code})")
            failed += 1
        except Exception as e:
            print(f"FAIL  ({e})")
            failed += 1

    print()
    print("=" * 60)
    print(f"結果：{passed} 通過 / {failed} 失敗 / {len(TEMPLATES)} 總計")

    if failed == 0:
        print("[PASS] 所有模板 API 煙霧測試通過")
        return 0
    else:
        print("[FAIL] 部分模板失敗，請查看上方輸出")
        return 1


if __name__ == "__main__":
    sys.exit(main())
