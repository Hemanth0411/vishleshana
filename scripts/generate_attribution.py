"""
generate_attribution.py — Generates ATTRIBUTION.md for legal compliance.
Scans installed packages and extracts version/license information.
"""

import importlib.metadata
import os

def generate():
    """
    Scans the current environment's packages and writes ATTRIBUTION.md.
    """
    packages = []
    
    # We want to track our primary dependencies
    targets = [
        "networkx", "radon", "pyvis", "openai", "streamlit", 
        "pandas", "GitPython", "python-dotenv", "pytest"
    ]
    
    for name in sorted(targets):
        try:
            dist = importlib.metadata.distribution(name)
            version = dist.version
            # Metadata can be messy, we try to find the license
            meta = dist.metadata
            license_name = meta.get("License", "Unknown")
            # Some packages put license in 'Classifier'
            if license_name == "Unknown":
                classifiers = meta.get_all("Classifier", [])
                for c in classifiers:
                    if c.startswith("License ::"):
                        license_name = c.split(" :: ")[-1]
                        break
            
            packages.append({
                "name": name,
                "version": version,
                "license": license_name
            })
        except importlib.metadata.PackageNotFoundError:
            continue

    # Write the file
    content = "# Open Source Attribution\n\n"
    content += "Vishleshana stands on the shoulders of these incredible open-source projects:\n\n"
    content += "| Package | Version | License |\n"
    content += "| :--- | :--- | :--- |\n"
    
    for p in packages:
        content += f"| {p['name']} | {p['version']} | {p['license']} |\n"
        
    with open("ATTRIBUTION.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✨ Successfully generated ATTRIBUTION.md")

if __name__ == "__main__":
    generate()
