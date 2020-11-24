import pandas as pd
from PIL import Image, ImageDraw
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2

from IPython.display import display, Latex

from app_functions import get_full_equation, get_object_order, full_expon, full_frac, create_drawn_box_img, delete_drawn_box_img, get_chars_in_box, latex_from_chars_list, render_latex, latex_formula_from_char_list

st.title("Image to LaTeX Converter")
st.subheader("Welcome! This is an app where you can put in an image of a handwritten equation, and after following a few prompts, receive the output of the equation in LaTeX format.")
st.subheader("To start: upload an image to the left and follow the prompts.")
#######################
# Specify canvas parameters in application

filename = st.sidebar.text_input('Enter the uploaded file name: ')
show_boxes = st.sidebar.checkbox("Do you want to see the bounding boxes?")
if show_boxes:
    filepath = '../all_labeled_img_files/'+filename
    img = filepath
    with_display = 'yes'
else:
    filepath = '../all_img_files/'+filename
    img = filepath
    with_display = 'no'
    #img = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
    #to prevent the warnign from showing
    st.set_option('deprecation.showfileUploaderEncoding', False)

st.image(img, width=600)

fractions = st.sidebar.checkbox("Do you have any fractions in your equation?")
exponents = st.sidebar.checkbox("Do you have any exponents in your equation?")
limits = st.sidebar.checkbox("Do you have any limits in your equation?")

latex_show = st.sidebar.checkbox("Would you like to see the latex code?")
#nothing = st.sidebar.checkbox("I have none of the above")

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
stroke_color = st.sidebar.beta_color_picker("Stroke color hex: ")
bg_color = st.sidebar.beta_color_picker("Background color hex: ", "#eee")
bg_image = img
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform")
)
realtime_update = st.sidebar.checkbox("Update in realtime", True)
#############################


total_new_objects = []
#object_order = []
#############################
#begin with fractions
if fractions:
    st.header("Please draw boxes around all fraction expressions")
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="" if bg_image else bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=150,
        drawing_mode=drawing_mode,
        key="canvas_frac",
    )
    all_done = st.checkbox("Check this box when you are finished creating fraction boxes")
    if all_done:
        # Do something interesting with the image data and paths
        if canvas_result.image_data is not None:
            #st.image(canvas_result.image_data)
            img_data = canvas_result.image_data
        if canvas_result.json_data is not None:
            df = pd.json_normalize(canvas_result.json_data["objects"])
            #for each box, make an object that has those coordinate dimensions
            object_coords = []
            latex_code = [] #for later
            for x in range(len(df.index)):
                left = int(df.iloc[x]['left'])
                top = int(df.iloc[x]['top'])
                width = int(df.iloc[x]['width'])
                height = int(df.iloc[x]['height'])
                these_coords = (left, top, width, height)
                object_coords.append(these_coords)
            #df2 = pd.DataFrame(canvas_result.json_data["objects"])
            #show dataframe once all done making boxes
            #st.dataframe(df)##############
            #st.dataframe(df2)
            len_df = len(df.index)
            is_correct = st.selectbox(f'We have detected {len_df} fraction expression(s). Is this correct?', ("yes", "no"))
            if is_correct == "no":
                st.write("Please redraw your boxes.")
            else:
                #for each rectangle that was drawn:
                for x in range(len_df):
                    this_df = df.iloc[[x]]
                    #this_rect_dimensions =
                    create_drawn_box_img(df=this_df, img_name=filename, with_bbox_display_yes_no=with_display, stroke_color = stroke_color, stroke_width = stroke_width)
                    created_img = './img_location/'+filename

                    ##### DENOMINATOR
                    st.header("Please draw a box around the denominator in this fraction")
                    # Create a canvas component
                    canvas_result2 = st_canvas(
                        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                        stroke_width=stroke_width,
                        stroke_color=stroke_color,
                        background_color="" if bg_image else bg_color,
                        background_image=Image.open(created_img) if created_img else None,
                        update_streamlit=realtime_update,
                        height=150,
                        drawing_mode=drawing_mode,
                        key="canvas_fract_denom"+str(x),
                    )
                    # Do something interesting with the image data and paths
                    if canvas_result2.image_data is not None:
                        #st.image(canvas_result.image_data)
                        img_data = canvas_result.image_data
                    if canvas_result2.json_data is not None:
                        df_this = pd.json_normalize(canvas_result2.json_data["objects"])
                        #st.dataframe(df_this)

                    all_done_2 = st.checkbox("Check this box when you are finished circling the denominator for box "+str(x+1))
                    if all_done_2:
                        get_chars = get_chars_in_box(df_rect = df_this, img_name = filename)[0]
                        #st.dataframe(pd.DataFrame(get_chars))
                        char_formula_denom = latex_formula_from_char_list(get_chars)
                        st.write("detected denominator: ")
                        render_latex(formula = char_formula_denom)

                        #delete image
                        #delete_drawn_box_img(img_name = filename)
                    
                    ######## NUMERATOR
                    st.header("Please draw a box around the numerator in this fraction")
                    # Create a canvas component
                    canvas_result2 = st_canvas(
                        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                        stroke_width=stroke_width,
                        stroke_color=stroke_color,
                        background_color="" if bg_image else bg_color,
                        background_image=Image.open(created_img) if created_img else None,
                        update_streamlit=realtime_update,
                        height=150,
                        drawing_mode=drawing_mode,
                        key="canvas_fract_numer"+str(x),
                    )
                    # Do something interesting with the image data and paths
                    if canvas_result2.image_data is not None:
                        #st.image(canvas_result.image_data)
                        img_data = canvas_result.image_data
                    if canvas_result2.json_data is not None:
                        df_this = pd.json_normalize(canvas_result2.json_data["objects"])
                        #st.dataframe(df_this)

                    all_done_3 = st.checkbox("Check this box when you are finished circling the numerator for box "+str(x+1))
                    if all_done_3:
                        get_chars = get_chars_in_box(df_rect = df_this, img_name = filename)[0]
                        #st.dataframe(pd.DataFrame(get_chars))
                        char_formula_numer = latex_formula_from_char_list(get_chars)
                        st.write("detected numerator: ")
                        render_latex(formula = char_formula_numer)

                        full_frac_expression = full_frac(char_formula_numer, char_formula_denom)
                        st.write("full fraction equation: ")
                        render_latex(formula = full_frac_expression)
                        all_done_4 = st.checkbox("Does this fraction expression for box "+str(x)+" look correct?")
                        if all_done_4:
                            #put this full latex expression into the list of latex_code for each rectangle
                            latex_code.append(full_frac_expression)
                            #delete image
                            delete_drawn_box_img(img_name = filename)
                
                total_object_info =[]
                for x in range(len(latex_code)):
                    this_tuple = (latex_code[x], object_coords[x])
                    total_object_info.append(this_tuple)
                for x in total_object_info:
                    total_new_objects.append(x)

    #st.write(total_new_objects)

    if len(total_new_objects)> 0:
        object_order = get_object_order(total_new_objects)
        full_latex = get_full_equation(sorted_list_classes_xcenters = object_order)
        st.write("full equation so far: ")
        render_latex(formula = full_latex)
        if latex_show:
            st.write(full_latex)
    else:
        object_order = []
    #st.write(object_order)




##########################
if exponents:
    st.header("Please draw boxes around all exponent expressions")
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="" if bg_image else bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=150,
        drawing_mode=drawing_mode,
        key="canvas_expon",
    )
    all_done = st.checkbox("Check this box when you are finished with creating exponential boxes")
    if all_done:
        # Do something interesting with the image data and paths
        if canvas_result.image_data is not None:
            #st.image(canvas_result.image_data)
            img_data = canvas_result.image_data
        if canvas_result.json_data is not None:
            df = pd.json_normalize(canvas_result.json_data["objects"])
            #for each box, make an object that has those coordinate dimensions
            object_coords = []
            latex_code = [] #for later
            for x in range(len(df.index)):
                left = int(df.iloc[x]['left'])
                top = int(df.iloc[x]['top'])
                width = int(df.iloc[x]['width'])
                height = int(df.iloc[x]['height'])
                these_coords = (left, top, width, height)
                object_coords.append(these_coords)
            #df2 = pd.DataFrame(canvas_result.json_data["objects"])
            #show dataframe once all done making boxes
            #st.dataframe(df)##############
            #st.dataframe(df2)
            len_df = len(df.index)
            is_correct = st.selectbox(f'We have detected {len_df} exponent expression(s). Is this correct?', ("yes", "no"))
            if is_correct == "no":
                st.write("Please redraw your boxes.")
            else:
                #for each rectangle that was drawn:
                for x in range(len_df):
                    this_df = df.iloc[[x]]
                    create_drawn_box_img(df=this_df, img_name=filename, with_bbox_display_yes_no=with_display, stroke_color = stroke_color, stroke_width = stroke_width)
                    created_img = './img_location/'+filename

                    ##### BASE
                    st.header("Please draw a box around the base of this exponential expression")
                    # Create a canvas component
                    canvas_result2 = st_canvas(
                        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                        stroke_width=stroke_width,
                        stroke_color=stroke_color,
                        background_color="" if bg_image else bg_color,
                        background_image=Image.open(created_img) if created_img else None,
                        update_streamlit=realtime_update,
                        height=150,
                        drawing_mode=drawing_mode,
                        key="canvas_expon_base"+str(x),
                    )
                    # Do something interesting with the image data and paths
                    if canvas_result2.image_data is not None:
                        #st.image(canvas_result.image_data)
                        img_data = canvas_result.image_data
                    if canvas_result2.json_data is not None:
                        df_this = pd.json_normalize(canvas_result2.json_data["objects"])
                        #st.dataframe(df_this)

                    all_done_2 = st.checkbox("Check this box when you are finished circling the base for box "+str(x+1))
                    if all_done_2:
                        get_chars = get_chars_in_box(df_rect = df_this, img_name = filename)[0]
                        #st.dataframe(pd.DataFrame(get_chars))
                        char_formula_base = latex_formula_from_char_list(get_chars)
                        st.write("detected base: ")
                        render_latex(formula = char_formula_base)

                    ######## NUMERATOR
                    st.header("Please draw a box around the exponent in this exponential expression")
                    # Create a canvas component
                    canvas_result2 = st_canvas(
                        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                        stroke_width=stroke_width,
                        stroke_color=stroke_color,
                        background_color="" if bg_image else bg_color,
                        background_image=Image.open(created_img) if created_img else None,
                        update_streamlit=realtime_update,
                        height=150,
                        drawing_mode=drawing_mode,
                        key="canvas_expon_exponent"+str(x),
                    )
                    # Do something interesting with the image data and paths
                    if canvas_result2.image_data is not None:
                        #st.image(canvas_result.image_data)
                        img_data = canvas_result.image_data
                    if canvas_result2.json_data is not None:
                        df_this = pd.json_normalize(canvas_result2.json_data["objects"])
                        #st.dataframe(df_this)

                    all_done_3 = st.checkbox("Check this box when you are finished circling the exponent for box "+str(x+1))
                    if all_done_3:
                        get_chars = get_chars_in_box(df_rect = df_this, img_name = filename)[0]
                        #st.dataframe(pd.DataFrame(get_chars))
                        char_formula_expon = latex_formula_from_char_list(get_chars)
                        st.write("detected exponent: ")
                        render_latex(formula = char_formula_expon)

                        full_expon_expression = full_expon(char_formula_expon, char_formula_base)
                        st.write("full exponential equation: ")
                        render_latex(formula = full_expon_expression)
                        all_done_4 = st.checkbox("Does this fraction expression for box "+str(x+1)+" look correct?")
                        if all_done_4:
                            latex_code.append(full_expon_expression)
                            #delete image
                            delete_drawn_box_img(img_name = filename)

                total_object_info =[]
                for x in range(len(latex_code)):
                    this_tuple = (latex_code[x], object_coords[x])
                    total_object_info.append(this_tuple)
                for x in total_object_info:
                    total_new_objects.append(x)

    #st.write(total_new_objects)

    if len(total_new_objects)> 0:
        object_order = get_object_order(total_new_objects)
        full_latex = get_full_equation(sorted_list_classes_xcenters = object_order)
        st.write("full equation so far: ")
        render_latex(formula = full_latex)
        if latex_show:
            st.write(full_latex)

    else:
        object_order = []
    #st.write(object_order)


if limits:
    st.header("Please draw boxes around all limit expressions")
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="" if bg_image else bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=150,
        drawing_mode=drawing_mode,
        key="canvas_lim",
    )
    all_done = st.checkbox("Check this box when you are finished creating limit boxes")
    if all_done:
        # Do something interesting with the image data and paths
        if canvas_result.image_data is not None:
            #st.image(canvas_result.image_data)
            img_data = canvas_result.image_data
        if canvas_result.json_data is not None:
            df = pd.json_normalize(canvas_result.json_data["objects"])
            #for each box, make an object that has those coordinate dimensions
            object_coords = []
            latex_code = [] #for later
            for x in range(len(df.index)):
                left = int(df.iloc[x]['left'])
                top = int(df.iloc[x]['top'])
                width = int(df.iloc[x]['width'])
                height = int(df.iloc[x]['height'])
                these_coords = (left, top, width, height)
                object_coords.append(these_coords)
            #df2 = pd.DataFrame(canvas_result.json_data["objects"])
            #show dataframe once all done making boxes
            #st.dataframe(df)##############
            #st.dataframe(df2)
            len_df = len(df.index)
            is_correct = st.selectbox(f'We have detected {len_df} limit expression(s). Is this correct?', ("yes", "no"))
            if is_correct == "no":
                st.write("Please redraw your boxes.")
            else:
                #for each rectangle that was drawn:
                for x in range(len_df):
                    this_df = df.iloc[[x]]
                    #this_rect_dimensions =
                    create_drawn_box_img(df=this_df, img_name=filename, with_bbox_display_yes_no=with_display, stroke_color = stroke_color, stroke_width = stroke_width)
                    created_img = './img_location/'+filename

                    ##### LIM base
                    st.header("Please draw a box around the limit information in this expression")
                    # Create a canvas component
                    canvas_result2 = st_canvas(
                        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                        stroke_width=stroke_width,
                        stroke_color=stroke_color,
                        background_color="" if bg_image else bg_color,
                        background_image=Image.open(created_img) if created_img else None,
                        update_streamlit=realtime_update,
                        height=150,
                        drawing_mode=drawing_mode,
                        key="canvas_lim_base"+str(x),
                    )
                    # Do something interesting with the image data and paths
                    if canvas_result2.image_data is not None:
                        #st.image(canvas_result.image_data)
                        img_data = canvas_result.image_data
                    if canvas_result2.json_data is not None:
                        df_this = pd.json_normalize(canvas_result2.json_data["objects"])
                        #st.dataframe(df_this)
                    all_done_2 = st.checkbox("Check this box when you are finished circling the limit information for box "+str(x+1))
                    if all_done_2:
                        get_chars = get_chars_in_box(df_rect = df_this, img_name = filename)[0]
                        #st.write(get_chars)
                        #st.dataframe(pd.DataFrame(get_chars))
                        char_formula_lim_base = latex_formula_from_char_list(get_chars)
                        #st.write(char_formula_lim_base)
                        char_formula_full_lim = '\\lim_{'+char_formula_lim_base+'}'
                        #st.write(char_formula_full_lim)
                        st.write("detected limit expression: ")
                        render_latex(formula = char_formula_full_lim)

                        all_done_4 = st.checkbox("Does this limit expression for box "+str(x)+" look correct?")
                        if all_done_4:
                            #put this full latex expression into the list of latex_code for each rectangle
                            latex_code.append(char_formula_full_lim)
                            #delete image
                            delete_drawn_box_img(img_name = filename)
                
                total_object_info =[]
                for x in range(len(latex_code)):
                    this_tuple = (latex_code[x], object_coords[x])
                    total_object_info.append(this_tuple)
                for x in total_object_info:
                    total_new_objects.append(x)

    #st.write(total_new_objects)

    if len(total_new_objects)> 0:
        object_order = get_object_order(total_new_objects)
        full_latex = get_full_equation(sorted_list_classes_xcenters = object_order)
        st.write("full equation so far: ")
        render_latex(formula = full_latex)
        if latex_show:
            st.write(full_latex)
    else:
        object_order = []
    #st.write(object_order)


