from PIL import Image
from doctr.models import ocr_predictor
from doctr.io import DocumentFile

model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def preprocess_image(image):
    min_width = min_height = 500
    width, height = image.size
    if width > min_width:
        min_width = 0
    if height > min_height:
        min_height = 0
    im_new = add_margin(image, 0, min_width, min_height, 0, (0, 0, 0))
    return im_new

def do_ocr():
    image = Image.open(r"snips\to_ocr.png")
    image = preprocess_image(image)
    image.save('snips/ocr_image.png')

    single_img_doc = DocumentFile.from_images("snips/ocr_image.png")
    result = model(single_img_doc)
    json_output = result.export()
    result_string = extract_sentences(json_output)
    return "".join(result_string)

def extract_sentences(json_output):
    blocks = json_output["pages"][0]["blocks"]
    full_text = []
    for block in blocks:
        for line in block["lines"]:
            words = [word["value"] for word in line["words"]]
            sentence = " ".join(words + ["\n"])
            full_text.append(sentence)
        full_text.append("\n")
    return full_text