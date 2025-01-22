import os
import numpy as np
from PIL import Image
from datasets import load_dataset
from langchain_experimental.open_clip import OpenCLIPEmbeddings
from langchain_teddynote.models import MultiModal
from langchain_openai import ChatOpenAI
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# pip install -qU open-clip-torch langchain_experimental langchain_teddynote langchain_openai matplotlib

from dotenv import load_dotenv
load_dotenv()

# Set up Korean font for matplotlib
font_path = "C:/Windows/Fonts/malgun.ttf"  # Adjust for your OS
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc("font", family=font_name)

# Step 1: Load Dataset
print("[INFO] Loading dataset...")
dataset = load_dataset(
    path="detection-datasets/coco", name="default", split="train", streaming=True
)

# Step 2: Save image paths from dataset
print("[INFO] Saving images...")
IMAGE_FOLDER = "tmp"
N_IMAGES = 20
os.makedirs(IMAGE_FOLDER, exist_ok=True)

dataset_iter = iter(dataset)
image_uris = []
original_images = []

for i in range(N_IMAGES):
    data = next(dataset_iter)
    image = data["image"]
    image_path = os.path.join(IMAGE_FOLDER, f"image_{i}.jpg")
    image.save(image_path)
    image_uris.append(image_path)
    original_images.append(image)

# Step 3: Initialize OpenCLIP Model
print("[INFO] Initializing OpenCLIP model...")
image_embedding_function = OpenCLIPEmbeddings(
    model_name="ViT-H-14-378-quickgelu", checkpoint="dfn5b"
)

# Step 4: Initialize ChatOpenAI and MultiModal Model
print("[INFO] Initializing LLM and MultiModal model...")
llm = ChatOpenAI(model="gpt-4o")
model = MultiModal(
    model=llm,
    system_prompt="Your mission is to describe the image in detail",
    user_prompt="Description should be written in one sentence (less than 60 characters)",
)

# Step 5: Generate Descriptions for Images
print("[INFO] Generating descriptions...")
descriptions = {}

for image_uri in image_uris:
    descriptions[image_uri] = model.invoke(image_uri, display_image=False)

# Step 6: Visualize Images with Descriptions
print("[INFO] Visualizing images with descriptions...")
plt.figure(figsize=(20, 10))

texts = []
for i, image_uri in enumerate(image_uris):
    image = Image.open(image_uri).convert("RGB")
    texts.append(descriptions[image_uri])
    plt.subplot(4, 5, i + 1)
    plt.imshow(image)
    plt.title(f"{os.path.basename(image_uri)}\n{descriptions[image_uri]}", fontsize=8)
    plt.xticks([])
    plt.yticks([])

plt.tight_layout()
plt.savefig("image_descriptions.png")

# Step 7: Calculate Similarity
print("[INFO] Calculating similarity...")
img_features = image_embedding_function.embed_image(image_uris)
text_features = image_embedding_function.embed_documents(
    ["This is " + desc for desc in descriptions.values()]
)

# Convert to numpy arrays
img_features_np = np.array(img_features)
text_features_np = np.array(text_features)

# Compute similarity
similarity = np.matmul(text_features_np, img_features_np.T)

# Save similarity matrix
np.savetxt("similarity_matrix.csv", similarity, delimiter=",", fmt="%.4f")
print("[INFO] Similarity matrix saved to 'similarity_matrix.csv'")

# Step 8: Visualize Similarity Matrix
print("[INFO] Visualizing similarity matrix...")
count = len(descriptions)
plt.figure(figsize=(20, 14))

# Display similarity as a heatmap
plt.imshow(similarity, vmin=0.1, vmax=0.3, cmap="coolwarm")
plt.colorbar()  # Add color bar

# Add text descriptions to the y-axis
plt.yticks(range(count), texts, fontsize=18)
plt.xticks([])  # Remove x-axis ticks

# Display original images below the x-axis
for i, image in enumerate(original_images):
    plt.imshow(image, extent=(i - 0.5, i + 0.5, -1.6, -0.6), origin="lower")

# Add similarity values as text on the heatmap
for x in range(similarity.shape[1]):
    for y in range(similarity.shape[0]):
        plt.text(x, y, f"{similarity[y, x]:.2f}", ha="center", va="center", size=12)

# Remove plot borders
for side in ["left", "top", "right", "bottom"]:
    plt.gca().spines[side].set_visible(False)

# Set plot range
plt.xlim([-0.5, count - 0.5])
plt.ylim([count + 0.5, -2])

# Add title
plt.title("텍스트와 이미지 특징 간의 코사인 유사도", size=20)
plt.tight_layout()
plt.savefig("similarity_heatmap.png")
print("[INFO] Similarity heatmap saved to 'similarity_heatmap.png'")
