# 定义了一个Profile类，用于获取图像文件的路径。


from pathlib import Path


class Profile:
    __images_path = None

    @staticmethod
    def get_images_path():
        home_path = Path(__file__).parent.parent

        images_path = home_path.joinpath("data/images")
        if not images_path.exists():
            images_path.mkdir(parents=True)

        return images_path
