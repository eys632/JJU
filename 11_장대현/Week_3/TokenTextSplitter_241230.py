# -*- coding: utf-8 -*-
"""07_02_TOKENTEXTSPLITTER.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1h-4Mg-OQ_oPFUzs1HmHc2DbIThk-oTq5
"""

import warnings
from langchain_text_splitters import SpacyTextSplitter

# Load and read the file
with open("/content/appendix-keywords.txt", "r", encoding="utf-8") as f:
    file = f.read()

warnings.filterwarnings("ignore")

# Split the file content into topics manually
topics = file.strip().split("\n\n")  # Topics are assumed to be separated by double newlines

# Initialize the SpacyTextSplitter with the desired settings
text_splitter = SpacyTextSplitter(
    chunk_size = 250,  # Adjusted chunk size
    chunk_overlap = 30  # Adjusted overlap
)

# Define a size threshold for adding separators
SIZE_THRESHOLD = 50  # Only add separators for content larger than this size

# Process each topic separately to avoid splitting mid-topic
result = []
for topic in topics:
    # Split the topic into title and body
    lines = topic.strip().split("\n", 1)  # Split into two parts: title and the rest
    title = lines[0].strip()  # The first line is the title
    body = lines[1].strip() if len(lines) > 1 else ""  # The rest is the body (if exists)

    # Add the title directly without any separator
    result.append(title)

    # Split the body into chunks
    if body:
        chunks = text_splitter.split_text(body)
        for chunk in chunks:
            chunk_text = chunk.strip()
            # Append the chunk
            result.append(chunk_text)
            # Add a separator only if the chunk exceeds the size threshold
            if len(chunk_text) > SIZE_THRESHOLD:
                result.append("=" * 80)

# Save the result to the output file
output_path = "/content/07_02_RESULT_TOKENTEXTSPLITTER.TXT"
with open(output_path, "w", encoding="utf-8") as output_file:
    output_file.write("\n\n".join(result))

print(f"Processed file saved to: {output_path}")
