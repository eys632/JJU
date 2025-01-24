import os
import glob

class TextSplitter:
    def __init__(self, chunk_size=500, overlap=50):
        """
        Initialize TextSplitter.
        :param chunk_size: Size of each text chunk.
        :param overlap: Number of overlapping characters between chunks.
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text):
        """
        Split text into chunks with optional overlap.
        :param text: Full text to be split.
        :return: List of text chunks.
        """
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk.strip())  # Remove leading/trailing spaces
            start += self.chunk_size - self.overlap

        return chunks

    def process_and_save(self, input_folder, output_folder):
        """
        Process all text files in the input folder and save the split results.
        :param input_folder: Folder containing extracted text files.
        :param output_folder: Folder to save the split text files.
        """
        try:
            # Ensure output directory exists
            os.makedirs(output_folder, exist_ok=True)

            # Find all text files in the input folder
            input_files = glob.glob(os.path.join(input_folder, "*.txt"))

            if not input_files:
                print(f"No text files found in {input_folder}.")
                return

            for input_file in input_files:
                # Read the content of each file
                with open(input_file, 'r', encoding='utf-8') as file:
                    text = file.read()

                # Split the text into chunks
                chunks = self.split_text(text)
                print(f"Processed {len(chunks)} chunks for {input_file}")

                # Save the split chunks to a new file in the output folder
                base_name = os.path.basename(input_file)
                output_file = os.path.join(output_folder, f"split_{base_name}")
                with open(output_file, 'w', encoding='utf-8') as file:
                    for i, chunk in enumerate(chunks):
                        file.write(f"Chunk {i + 1}:\n{chunk}\n\n")
                print(f"Chunks saved to {output_file}")

        except Exception as e:
            print(f"Error processing and saving text: {e}")


if __name__ == "__main__":
    # Input and output folder paths
    input_folder = "C:\\Users\\eys63\\GitHub\\JJU\\01-이연승\\과제\\25_01_22과제_ChromaDB\\output"
    output_folder = "C:\\Users\\eys63\\GitHub\\JJU\\01-이연승\\과제\\25_01_22과제_ChromaDB\\split_output"

    # TextSplitter 객체 생성
    splitter = TextSplitter(chunk_size=500, overlap=50)

    # 모든 텍스트 파일 처리 및 저장
    splitter.process_and_save(input_folder, output_folder)
