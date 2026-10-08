"""Exports reconnaissance findings to JSON or Markdown."""
import json
import os
from datetime import datetime

def export_report(module_name: str, target: str, data: dict, output_dir: str = "reports") -> str:
    """Exports structured reconnaissance data to JSON and Markdown."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    clean_target = "".join(c for c in target if c.isalnum() or c in ("-", "_", ".")).strip()
    base_filename = f"{module_name}_{clean_target}_{timestamp}"

    # JSON export
    json_path = os.path.join(output_dir, f"{base_filename}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"module": module_name, "target": target, "timestamp": timestamp, "data": data}, f, indent=2)

    # Markdown export
    md_path = os.path.join(output_dir, f"{base_filename}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# ZeroTrace Reconnaissance Report\n\n")
        f.write(f"- **Module:** {module_name}\n")
        f.write(f"- **Target:** `{target}`\n")
        f.write(f"- **Timestamp (UTC):** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Findings\n\n")
        if isinstance(data, dict):
            f.write("| Key | Value |\n| :--- | :--- |\n")
            for k, v in data.items():
                f.write(f"| **{k}** | {v} |\n")
        elif isinstance(data, list):
            for item in data:
                f.write(f"- {item}\n")

    return md_path
