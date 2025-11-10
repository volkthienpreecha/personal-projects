import numpy as np 
import hashlib
import cv2 
import os

def image_hash_computation(image_path):

    if isinstance(image_path, (bytes,bytearray)):
        img_array = np.frombuffer(image_path, np.uint8)
        img = cv2.imdecode(img_array,cv2.IMREAD_COLOR)
    elif isinstance(image_path, str) and os.path.exists(image_path):
        img = cv2.imread(image_path)
    else:
        raise ValueError("Invalid image input: must be bytes or a valid file path.")
    
    if img is None:
        raise ValueError("Failed to load image. Make sure it's a valid PNG/JPEG.")

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #Sobel gradients

    gx = cv2.Sobel(gray, cv2.CV_64F, 1,0,ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F,0,1,ksize=3)

    #Sobel gradient magnitude

    grad_mag = np.sqrt(gx**2 + gy**2)
    grad_mag = np.uint8(255*grad_mag / np.max(grad_mag))

    # Resize to 32x32
    small = cv2.resize(grad_mag, (32,32), interpolation=cv2.INTER_AREA)
    flat = small.flatten().astype(np.float32)
    flat /= 255.0
    byte_repr = flat.tobytes()

    return hashlib.sha256(byte_repr).hexdigest()

def hamming_distance(hash1, hash2):
    b1 = bytes.fromhex(hash1)
    b2 = bytes.fromhex(hash2)

    return sum((x ^ y).bit_count() for x,y in zip(b1, b2))

if __name__ == "__main__":
    path1 = r"C:\Users\volko\Downloads\image_for_provenance.png"
    path2 = r"C:\Users\volko\Downloads\image_for_provenance.png"
    hash1 = image_hash_computation(path1)
    hash2 = image_hash_computation(path2)
    print("Hamming distance:", hamming_distance(hash1, hash2))