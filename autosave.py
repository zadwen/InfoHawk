
import os, json, datetime
def save_case(data, label="case"):
    date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cases/case_{label}_{date}"
    with open(f"{filename}.json", "w") as f: json.dump(data, f, indent=2)
    with open(f"{filename}.md", "w") as f: f.write("## Case Report\n" + json.dumps(data, indent=2))
    return filename
