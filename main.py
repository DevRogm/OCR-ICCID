from tools import ImageProcessor, ICCIDReader, CSVICCIDUpdater

image_processor = ImageProcessor("files/img/")
iccid_reader = ICCIDReader()
csv_updater = CSVICCIDUpdater("files/csv/my_file.csv")

prepared_images =  image_processor.prepare_img

for filename, prepared_img in prepared_images:
    iccid = iccid_reader.get_iccid(prepared_img)
    if iccid:
        csv_updater.update_csv(filename, iccid)
        pass
    else:
        # save a txt file with the name of the file where the ICCID could not be read, create new one with datetime
        csv_updater.log_unread_iccid_files(filename)
    print(filename, iccid)
    # poprawnie odczytane uzupełniać w csv a) wyciagac nazwe z pliku i sklejac tak jak w instrukcji.
    # niepoprawnie odczytane logować w jakimś pliku txt lub excelu

# img_path = "files/img/IS112528000014.jpg"

# img = cv2.imread(img_path)
#
# height, width = img.shape[:2]
#
# top = int(0.39 * height)
# bottom = int(0.60 * height)
# left = int(0.28 * width)
# right = int(0.73 * width)
#
# cropped = img[top:bottom, left:right]
#
# gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
#
# blurred = cv2.GaussianBlur(gray, (0, 0), 3)
# sharpened = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)
#
#
#
# clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
# enhanced = clahe.apply(sharpened)
#
# # Image.fromarray(enhanced).show()
#
# reader = easyocr.Reader(['en'])  # cyfry nie wymagają 'pl'
# results = reader.readtext(enhanced)
#
# # for bbox, text, conf in results:
# #     print(f'Tekst: {text}, Pewność: {conf:.2f}')
#
# iccid = results[0][1]+results[1][1]
#
# print(checksum(iccid))
#
#


