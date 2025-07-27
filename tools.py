import os
import cv2
import easyocr
from PIL import Image
import csv

class ImageProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.prepare_img = self._prepare_img()

    def _prepare_img(self):
        for img_path in self._get_image_paths():
            loaded_img = self._read_img(img_path)
            cropped_img = self._crop_img(loaded_img)
            gray_img = self._convert_to_gray(cropped_img)
            blurred_img = self._gaussian_blur(gray_img)
            sharpened_img = self._add_weighted(gray_img, blurred_img)
            enhaced_img = self._enhace_img(sharpened_img)
            Image.fromarray(enhaced_img).show()
            yield (os.path.basename(img_path), enhaced_img)

    def _get_image_paths(self):
        with os.scandir(self.folder_path) as entries:
            for entry in sorted(entries, key=lambda e: e.name):
                yield entry.path

    def _read_img(self, img_path):
        read_img = cv2.imread(img_path)
        return read_img

    def _crop_img(self, loaded_img):
        height, width = loaded_img.shape[:2]
        top = int(0.39 * height)
        bottom = int(0.60 * height)
        left = int(0.28 * width)
        right = int(0.73 * width)
        cropped_img = loaded_img[top:bottom, left:right]
        return cropped_img

    def _convert_to_gray(self, cropped_img):
        return cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

    def _gaussian_blur(self, gray_img):
        return cv2.GaussianBlur(gray_img, (1, 1), 3)

    def _add_weighted(self, gray_img, blurred_img):
        return cv2.addWeighted(gray_img, 2, blurred_img, -0.5, 0)

    def _enhace_img(self, sharpened_img):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(sharpened_img)


class ICCIDReader:

    def get_iccid(self, img):
        reader = easyocr.Reader(['en'])
        results = reader.readtext(img)
        iccid = results[0][1]+results[1][1]
        if self._checksum(iccid):
            return iccid

    def _checksum(self, iccid):
        if not iccid.isdigit() or len(iccid) != 19:
            raise ValueError("ICCID musi zawierać dokładnie 19 cyfr.")

        digits = [int(d) for d in iccid[:-1]]  # Bez ostatniej cyfry (checksum)
        check_digit = int(iccid[-1])

        # Algorytm Luhna – od prawej do lewej, parzyste pozycje * 2
        total = 0
        reverse_digits = digits[::-1]

        for i, digit in enumerate(reverse_digits):
            if i % 2 == 0:
                doubled = digit * 2
                total += doubled if doubled < 10 else doubled - 9
            else:
                total += digit

        calculated_checksum = (10 - (total % 10)) % 10
        return calculated_checksum == check_digit


class CSVICCIDUpdater:
    def __init__(self, full_folder_path):
        self.full_folder_path = full_folder_path

    def update_csv(self, filename, iccid):
        with open(self.full_folder_path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print(', '.join(row))

    @staticmethod
    def log_unread_iccid_files(filename):
        pass