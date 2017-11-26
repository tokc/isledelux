import os

IMAGE_DIRECTORY = "./cycles/"
USED_DIRECTORY = "./tweeted/"


def fetch_image():
    image_path = os.path.abspath(IMAGE_DIRECTORY)
    folder = os.listdir(image_path)

    if folder == []:
        return None
    else:
        return os.path.join(image_path, folder[0])


def cleanup_image(path):
    filename = os.path.basename(path)

    os.rename(path, os.path.join(os.path.abspath(USED_DIRECTORY), filename))


if __name__ == "__main__":
    image = fetch_image()
    print(image)
    cleanup_image(image)
