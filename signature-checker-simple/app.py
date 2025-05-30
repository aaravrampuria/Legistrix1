import streamlit as st
import cv2
import numpy as np

st.title("Legistrix - Signature Forgery Detection")

st.write("Upload two signature images to compare their similarity.")

img1 = st.file_uploader("Upload Original Signature", type=["png", "jpg", "jpeg"])
img2 = st.file_uploader("Upload Signature to Verify", type=["png", "jpg", "jpeg"])

threshold = 85  # similarity threshold in %

if img1 and img2:
    # Read uploaded files once
    file_bytes1 = np.asarray(bytearray(img1.read()), dtype=np.uint8)
    file_bytes2 = np.asarray(bytearray(img2.read()), dtype=np.uint8)

    # Decode images as grayscale
    image1 = cv2.imdecode(file_bytes1, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imdecode(file_bytes2, cv2.IMREAD_GRAYSCALE)

    # Resize second image to first image's size
    image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

    # Calculate absolute difference
    diff = cv2.absdiff(image1, image2)

    non_zero_count = np.count_nonzero(diff)
    total_pixels = diff.size
    similarity = (1 - non_zero_count / total_pixels) * 100

    st.write(f"Similarity: {similarity:.2f}%")

    if similarity >= threshold:
        st.success("Result: Genuine Signature ✅")
    else:
        st.error("Result: Forged Signature ❌")
