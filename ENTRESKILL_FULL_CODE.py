  
import os
from pathlib import Path

project_root = Path(__file__).parent / 'entreskill_hub'
output_file = Path(__file__).parent / 'ENTRESKILL_FULL_CODE.py'

exclude_dirs = {'venv', '__pycache__', 'migrations', '.git', 'media', 'staticfiles'}
exclude_exts = {'.pyc', '.png', '.jpg', '.jpeg', '.mp4', '.pdf'}

with open(output_file, 'w', encoding='utf-8') as out:
    out.write("# ENTRESKILL HUB - FULL CODE DUMP\n")
    out.write(f"# Generated on {os.getcwd()}\n\n")
    
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in sorted(files):
            if Path(file).suffix in exclude_exts:
                continue
                
            filepath = Path(root) / file
            rel_path = filepath.relative_to(project_root)
            
            out.write(f"\n\n{'='*80}\n")
            out.write(f"# FILE: {rel_path}\n")
            out.write(f"{'='*80}\n\n")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    out.write(f.read())
            except Exception as e:
                out.write(f"# Error reading file: {e}\n")

print(f"Full code dumped to: {output_file}")