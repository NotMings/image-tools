import os
import tempfile
import shutil
import PIL.Image as Image
from pathlib import Path


class ImageTools:
    def __init__(self, **kwargs):
        self.input_image_dir = Path(kwargs['input_image_dir']) if 'input_image_dir' in kwargs else None
        self.output_image_dir = Path(kwargs['output_image_dir']) if 'output_image_dir' in kwargs else None
        # self.image_path = kwargs['image_path'] if 'image_path' in kwargs else None

        self.image_quality = 90
        self.image_step = 1

        self.image_path_list = self.__get_image_path_list(self.input_image_dir)
        self.temp_dir = tempfile.mkdtemp()

    
    def __del__(self):
        image_path_list = os.listdir(self.temp_dir)
        for image in image_path_list:
            shutil.move(os.path.join(self.temp_dir, image), os.path.join(self.temp_dir, image))

        shutil.rmtree(self.temp_dir)


    def __reset_dir(self):
        self.input_image_dir = self.temp_dir
        self.image_path_list = self.__get_image_path_list(self.temp_dir)


    def __get_image_path_list(self, image_dir):
        image_path_list = []

        if isinstance(image_dir, Path) is False:
            image_dir = Path(image_dir)

        for i in list(image_dir.rglob('*')):
            if i.suffix in ['.jpg', '.jpeg', '.png', '.webp']:
                image_path_list.append(str(i))
        return image_path_list


    def image_to_jpg(self):
        for i in range(len(self.image_path_list)):
            image = Image.open(self.image_path_list[i]).convert('RGB')
            image_stem = Path(self.image_path_list[i]).stem
            image_path = os.path.join(self.temp_dir, image_stem + '.jpg')
            image.save(image_path, quality=self.image_quality)

        self.__reset_dir()


    def image_to_jpeg(self):
        for i in range(len(self.image_path_list)):
            image = Image.open(self.image_path_list[i]).convert('RGB')
            image_stem = Path(self.image_path_list[i]).stem
            image_path = os.path.join(self.temp_dir, image_stem + '.jpeg')
            image.save(image_path, quality=self.image_quality)

        self.__reset_dir()


    def image_to_png(self):
        for i in range(len(self.image_path_list)):
            image = Image.open(self.image_path_list[i]).convert('RGB')
            image_stem = Path(self.image_path_list[i]).stem
            image_path = os.path.join(self.temp_dir, image_stem + '.png')
            image.save(image_path, quality=self.image_quality)

        self.__reset_dir()


    def image_to_webp(self):
        for i in range(len(self.image_path_list)):
            image = Image.open(self.image_path_list[i]).convert('RGB')
            image_stem = Path(self.image_path_list[i]).stem
            image_path = os.path.join(self.temp_dir, image_stem + '.webp')
            image.save(image_path, quality=self.image_quality)
        
        self.__reset_dir()


    def compress_image(self, max_size):
        for i in range(len(self.image_path_list)):
            image_size = os.path.getsize(self.image_path_list[i])
            image_stem = Path(self.image_path_list[i]).stem
            image_path = os.path.join(str(self.output_image_dir), image_stem + Path(self.image_path_list[i]).suffix)
            image = Image.open(self.image_path_list[i]).convert('RGB')
            
            if image_size > (max_size * 1024):
                while image_size > (max_size * 1024):
                    # compression_ratio = max_size * 1024 / image_size
                    compression_ratio = 0.9

                    new_image = image.resize((int(image.size[0] * compression_ratio), int(image.size[1] * compression_ratio)))

                    if self.image_quality - self.image_step <= 30:
                        new_image.save(image_path, quality=self.image_quality)
                        break

                    self.image_quality = self.image_quality - self.image_step
                    new_image.save(image_path, quality=self.image_quality)
                    image_size = os.path.getsize(image_path)
                    image = Image.open(image_path).convert('RGB')
            else:
                image.save(image_path, quality=self.image_quality)

        self.__reset_dir()
