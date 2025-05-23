import requests

def upload_to_r2(file_path, file_name):
    url = f"https://pub-e9b60722b96746639438295f50602ef5.r2.dev/videos/{file_name}"

    headers = {
        "Content-Type": "video/mp4",
    }

    with open(file_path, 'rb') as f:
        response = requests.put(url, headers=headers, data=f)

    if response.status_code in [200, 201]:
        return url  # Ссылка на видео
    else:
        raise Exception(f"Upload failed: {response.status_code} {response.text}")
        