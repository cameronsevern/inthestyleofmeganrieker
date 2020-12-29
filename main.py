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

st.write('This application allows you to recreate any image in the style of the paintings of Megan Rieker (and a few other examples)')

st.write('Select a painting from the style image dropdown menu then upload a photo below')

st.write('Press the Stylize button to recreate the source image in the style of the style image')

st.write("It's no replacement for the real thing, but I hope it sparks creativity and is fun to play with")

st.write('### Style image:')
style_name = st.selectbox(
    'Select Style',
    ('truck', 'temple','watercolor','watercolor_2','italian_coastal_city', 
    'canal','landscape_1','mountain_range','open_window',
    'renaissance_woman_1','renaissance_woman_2','renaissance_man', 'woman_in_white',
    'candy', 'mosaic', 'rain_princess', 'udnie')
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

