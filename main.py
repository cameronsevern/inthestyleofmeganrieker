# python3 -m venv venv
# . venv/bin/activate
# pip install streamlit
# pip install torch torchvision
# streamlit run main.py
import streamlit as st
from PIL import Image
from resizeimage import resizeimage

import style

st.title('In the style of Megan Rieker')

st.write('### Style image:')
style_name = st.selectbox(
    'Select Style',
    ('truck', 'temple','watercolor','italian_coastal_city', 'candy', 'mosaic', 'rain_princess', 'udnie')
)
style_image = "data/images/style-images/" + style_name + ".jpg"
s_image = Image.open(style_image)
st.image(s_image, use_column_width=True) # image: numpy array

st.write('### Source image:')
input_image = st.file_uploader("Upload an image to style")

if input_image is not None:
	img = Image.open(input_image)
	width, height = img.size

	if max(width,height) > 640:
		if width >= height:
			img = resizeimage.resize_width(img, 640)
		else:
			img = resizeimage.resize_height(img, 640)

	img = img.convert("RGB")
	img.save('data/images/content-images/source.jpeg')
	st.image(img, use_column_width=True) # image: numpy array

	model = "data/models/" + style_name + ".pth"
	output_image = "data/images/output-images/" + style_name + input_image.name +".jpg"


clicked = st.button('Stylize')

if clicked:
    model_obj = style.load_model(model)
    style.stylize(model_obj, 'data/images/content-images/source.jpeg', output_image)

    st.write('### Output image:')
    image = Image.open(output_image)
    st.image(image, use_column_width=True)
    del model_obj

