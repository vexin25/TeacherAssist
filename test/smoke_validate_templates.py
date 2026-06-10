#!/usr/bin/env python3
"""煙霧測試：驗證所有已登錄的 TemplateStrategy 結構正確性。

執行方式（從專案根目錄）：
    python test/smoke_validate_templates.py

成功時 exit 0，任一策略失敗時 exit 1。
"""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def main() -> int:
    print("=" * 60)
    print("Smoke Test: validate_template_class --all")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", "txt2pptx.utils.validate_template_class", "--all"],
        cwd=PROJECT_ROOT,
    )

    if result.returncode == 0:
        print("\n[PASS] 所有模板策略驗證通過")
    else:
        print("\n[FAIL] 至少一個模板策略驗證失敗")

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
