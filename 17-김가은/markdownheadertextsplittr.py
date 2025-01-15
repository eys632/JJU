import re

def markdown_header_text_splitter(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regular expression to match Markdown headers and their content
    pattern = r'(#{1,6}\\s.*?)(?=\\n#{1,6}\\s|\\Z)'
    matches = re.findall(pattern, content, flags=re.S)

    # Process the matches into a dictionary
    sections = {}
    for match in matches:
        lines = match.split('\\n', 1)
        header = lines[0].strip()
        text = lines[1].strip() if len(lines) > 1 else ''
        sections[header] = text

    return sections

# Specify the correct file path
file_path = r'C:\\Users\\PC\\Desktop\\실무인재(겨율특강)\\testResume.md'
sections = markdown_header_text_splitter(file_path)

# Print the split sections
for header, text in sections.items():
    print(f"Header: {header}\\nText: {text}\\n{'-'*40}")
