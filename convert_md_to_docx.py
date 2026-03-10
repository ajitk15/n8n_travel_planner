import pypandoc
import os

try:
    print("Downloading pandoc...")
    pypandoc.download_pandoc()
except Exception as e:
    print(f"Error downloading: {e}")

print("Converting file...")
input_file = r"c:\Workspace\n8n\n8n_agent_guide.md"
output_file = r"c:\Workspace\n8n\n8n_agent_guide.docx"

pypandoc.convert_file(
    input_file,
    'docx',
    outputfile=output_file
)
print(f"Successfully converted to {output_file}")
