import os
import requests

def save_image(url: str, title: str, save_dir=os.getenv('IMAGES_FOLDER')) -> str:
    
    # Ensure the directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Full path to save the image
    image_path = os.path.join(save_dir, f"{title}.jpg")
    full_image_path = os.path.abspath(image_path)  # Get the absolute path
    
    # Download and save the image
    response = requests.get(url)
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download image: {url}")

    return full_image_path
