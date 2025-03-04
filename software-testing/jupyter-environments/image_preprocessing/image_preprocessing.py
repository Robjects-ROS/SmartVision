# image_preprocessing.py

import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def resize_image_updated(image, target_size):
    """
    Resize the input image to the target size.
    Works with both older and newer versions of PIL.
    """
    # Check if the input image is a numpy array
    if isinstance(image, np.ndarray):
        # Convert numpy array to PIL Image
        image = Image.fromarray(image)

    # Try to use LANCZOS (newer versions) instead of ANTIALIAS
    try:
        resized_image = image.resize(target_size, Image.LANCZOS)
    except AttributeError:
        try:
            # For PIL 10.0.0+ where we need to use Resampling enum
            resized_image = image.resize(target_size, Image.Resampling.LANCZOS)
        except (ImportError, AttributeError):
            # Last resort: use default resampling
            resized_image = image.resize(target_size)

    # If the original image was a numpy array, convert back
    if isinstance(image, np.ndarray):
        resized_image = np.array(resized_image)

    return resized_image


def normalize_image(image):
    """
    Normalize pixel values to the range [0, 1].

    Parameters:
    image (numpy array): The input image to be normalized.

    Returns:
    normalized_image (numpy array): The normalized image.
    """
    # Check if the input image is a numpy array
    if not isinstance(image, np.ndarray):
        raise TypeError("Input image must be a numpy array")
    
    # Normalize pixel values to the range [0, 1]
    normalized_image = image / 255.0
    return normalized_image
    

def augment_data(images, labels):
    augmented_images = []
    augmented_labels = []
    
    for image, label in zip(images, labels):
        # Perform data augmentation on the image
        augmented_image = apply_augmentation(image)
        
        # Add the original and augmented images to the list
        augmented_images.append(image)
        augmented_images.append(augmented_image)
        
        # Add the corresponding labels
        augmented_labels.append(label)
        augmented_labels.append(label)
    
    return augmented_images, augmented_labels


# Define a function to apply data augmentation
def apply_augmentation(image):
    """
    Apply data augmentation techniques to the input image.
    
    Parameters:
    image (numpy array): The input image to be augmented.
    
    Returns:
    augmented_image (numpy array): The augmented image.
    """
    # Import necessary libraries

    # Flip the image horizontally
    flipped_image = cv2.flip(image, 1)

    # Rotate the image by 90 degrees
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    # Adjust brightness
    brightness_factor = 1.2  # Increase brightness by 20%
    brightness_adjusted = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=10)
    
    # Add random noise
    noise = np.random.normal(0, 15, image.shape).astype(np.uint8)
    noisy_image = cv2.add(image, noise)
    
    # Create a combined augmentation (rotate then adjust brightness)
    combined_augmentation = cv2.convertScaleAbs(rotated_image, alpha=brightness_factor, beta=10)
    
    # Random crop
    h, w = image.shape[:2]
    crop_size = int(min(h, w) * 0.8)  # Crop to 80% of original size
    start_x = np.random.randint(0, w - crop_size + 1)
    start_y = np.random.randint(0, h - crop_size + 1)
    cropped_image = image[start_y:start_y+crop_size, start_x:start_x+crop_size]
    
    # Return the combined augmented image
    return combined_augmentation
