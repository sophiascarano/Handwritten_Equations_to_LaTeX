from IPython.display import display, Latex

import json
import ast
import base64
import numpy as np
import pandas as pd
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import streamlit as st
import cv2
import matplotlib.pyplot as plt

labels_dict = {0: '\\cdot',
 1: '\\frac',
 2: '\\infty',
 3: '\\left(',
 4: '\\left|',
 5: '\\pi',
 6: '\\right)',
 7: '\\right|',
 8: '\\sqrt',
 9: '\\theta',
 10: '+',
 11: '-',
 12: '.',
 13: '/',
 14: '0',
 15: '1',
 16: '2',
 17: '3',
 18: '4',
 19: '5',
 20: '6',
 21: '7',
 22: '8',
 23: '9',
 24: '=',
 25: 'a',
 26: 'b',
 27: 'c',
 28: 'd',
 29: 'e',
 30: 'g',
 31: 'h',
 32: 'k',
 33: 'n',
 34: 'p',
 35: 'r',
 36: 's',
 37: 't',
 38: 'u',
 39: 'v',
 40: 'w',
 41: 'x',
 42: 'y',
 43: 'z',
 44: '\\lim_',
 45: '\\log',
 46: '\\cot',
 47: '\\csc',
 48: '\\to',
 49: '\\cos',
 50: '\\sec',
 51: '\\sin',
 52: '\\ln',
 53: '\\tan'}

# def create_drawn_box_img(df, img_name, with_bbox_display_yes_no, stroke_color, stroke_width):
#     if with_bbox_display_yes_no == 'yes':
#         filepath = '../all_labeled_img_files/'+img_name
#     elif with_bbox_display_yes_no == 'no':
#         filepath = '../all_img_files/'+img_name
    
#     #generate image of original image with that specific bounding box drawn on it
#     #open the image
#     img = Image.open(filepath)
#     #instantiate new images
#     size1 = img.size
#     size2 = (150, 600) #i think this just crops it. it doesn't rescale
#     newimg1 = Image.new("RGB", size1)
#     newimg1.paste(img)

#     newimg2 = Image.new("RGB", size1)
#     newimg2.paste(img)

#     streamlit_width = 600
#     streamlit_height = 150

#     #img_width, img_height = newimg1.size
#     width = streamlit_width
#     height = streamlit_height
#     dim = (width, height)

#     # resize image
#     dim = (600, 150)
#     resized1 = cv2.resize(np.float32(newimg1), dim, interpolation = cv2.INTER_AREA)
#     resized1 = Image.fromarray((resized1).astype(np.uint8))
    
#     resized2 = cv2.resize(np.float32(newimg2), dim, interpolation = cv2.INTER_AREA)
#     resized2 = Image.fromarray((resized2).astype(np.uint8))

#     #instantiate drawing on first img
#     draw_obj = ImageDraw.Draw(resized1)

#     #get dimensions from df:
#     x = 0
#     this_xmin = df.iloc[x]['left']
#     this_ymax = df.iloc[x]['top']
#     this_width = df.iloc[x]['width']
#     this_height = df.iloc[x]['height']


#     # xmin = this_xmin * (img_width / streamlit_width)
#     # xmax = (this_xmin + this_width) * (img_width / streamlit_width)
#     # ymax = (this_ymax) * (img_height / streamlit_height)
#     # ymin = (this_ymax - this_height) * (img_height / streamlit_height)

#     xmin = this_xmin
#     xmax = (this_xmin + this_width)

#     #########################################
#     ymax_norm_for_plot = this_rect[1] / streamlit_height
#     ymin_norm_for_plot = (this_rect[1] + this_rect[3]) / streamlit_height
    
#     #ymin_norm_for_bbox_calc = (150 - this_rect[1] - this_rect[3]) / streamlit_height
#     #ymax_norm_for_bbox_calc = (150 - this_rect[1]) / streamlit_height
    
#     ymin_norm =ymax_norm_for_plot
#     ymax_norm = ymin_norm_for_plot

#     #############################################

#     ymax = (150  - this_ymax)
#     ymin = (150  - this_ymax - this_height)

#     fill_1 = (255, 165, 0, 0.3)
#     fill_2 = (255, 165, 0, 3)

#     #specify dimensions for each rectangle
#     ####rectangle_dimensions = [xmin, ymin, xmax, ymax]
#     rectangle_dimensions = [xmin, ymin, xmax, ymax]
#     #add this rectangle to drawing
#     draw_obj.rectangle(rectangle_dimensions, fill =fill_2, outline=stroke_color, width=stroke_width)

#     #put the two images together
#     real_img = Image.blend(im1 = resized2, im2 = resized1, alpha = .3)#PIL.Image.blend(im1, im2, alpha)

#     #give path for new image
#     new_img_name = './img_location/'+img_name
#     real_img.save(new_img_name)








def create_drawn_box_img(df, img_name, with_bbox_display_yes_no, stroke_color, stroke_width):
    if with_bbox_display_yes_no == 'yes':
        filepath = '../all_labeled_img_files/'+img_name
    elif with_bbox_display_yes_no == 'no':
        filepath = '../all_img_files/'+img_name
    
    #generate image of original image with that specific bounding box drawn on it
    #open the image
    img = Image.open(filepath)

    img_width, img_height = img.size
    #instantiate new images
    size1 = img.size
    size2 = (150, 600) #i think this just crops it. it doesn't rescale
    newimg1 = Image.new("RGB", size1)
    newimg1.paste(img)

    newimg2 = Image.new("RGB", size1)
    newimg2.paste(img)

    draw_obj = ImageDraw.Draw(newimg1)

    rect_norm_dims = get_chars_in_box(df_rect = df, img_name = img_name)[1]
    
    xmin_real = int(rect_norm_dims[0] * img_width)
    xmax_real = int(rect_norm_dims[1] * img_width)
    ymin_real = int(rect_norm_dims[2] * img_height)
    ymax_real = int(rect_norm_dims[3] * img_height)
    
    rect_real_idms = [xmin_real, xmax_real, ymin_real, ymax_real]
    
    # rectangle_dimensions = [xmin, ymin, xmax, ymaxs]
    rectangle_dimensions = [rect_real_idms[0], rect_real_idms[2], rect_real_idms[1], rect_real_idms[3]]
        
    #add these rectangles to drawing
    fill_2 = (255, 165, 0, 3)
    draw_obj.rectangle(rectangle_dimensions, fill =fill_2, outline=stroke_color, width=stroke_width)
    
    #put the two images together
    real_img = Image.blend(im1 = newimg2, im2 = newimg1, alpha = .3)
    
    #give path for new image
    new_img_name = './img_location/'+img_name
    real_img.save(new_img_name)






def delete_drawn_box_img(img_name):
    os.remove('./img_location/'+img_name)










# see how many boxes (rows) there are:
def how_many_rows(txt_root_name):
    file = open("../all_txt_files/"+txt_root_name+".txt", "r")
    Counter = 0
    Content = file.read() 
    CoList = Content.split("\n") 
    for i in CoList: 
        if i: 
            Counter += 1
    return Counter







def get_dimension_lists(img_root_name):
    
    txt_file = open("../all_txt_files/"+img_root_name+".txt")
    img_file = Image.open(r'../all_img_files/'+img_root_name+'.jpg')

    img_width, img_height = img_file.size

    img_classes = []
    x_center_norms = []
    y_center_norms = []
    width_norms = []
    height_norms = []
    
    num_objects = how_many_rows(img_root_name)
    
    for x in range(num_objects):
        line = txt_file.readline()
        obj_class = line.split(' ', 4)[0]
        x_center_norm = line.split(' ', 4)[1]
        y_center_norm = line.split(' ', 4)[2]
        width_norm = line.split(' ', 4)[3]
        height_norm = line.split(' ', 4)[4]

        img_classes.append(int(obj_class))
        x_center_norms.append(float(x_center_norm))
        y_center_norms.append(float(y_center_norm))
        width_norms.append(float(width_norm))
        height_norms.append(float(height_norm))
    
    #now for the conversion math (did on paper first)
    xcn = x_center_norms
    ycn = y_center_norms
    w = width_norms
    h = height_norms
    W = img_width
    H = img_height
    
    xmins = []
    ymins = []
    xmaxs = []
    ymaxs = []
    for x in range(len(xcn)):
        x_min = int(((2 * xcn[x] * W) - (w[x] * W)) / 2)
        x_max = int(((2 * xcn[x] * W) + (w[x] * W)) / 2)
        y_min = int(((2 * ycn[x] * H) - (h[x] * H)) / 2)
        y_max = int(((2 * ycn[x] * H) + (h[x] * H)) / 2)
        
        xmins.append(x_min)
        xmaxs.append(x_max)
        ymins.append(y_min)
        ymaxs.append(y_max)
        
    num_labels = img_classes
    labels = [labels_dict.get(x) for x in num_labels]
    
    return xmins, ymins, xmaxs, ymaxs, labels




def get_chars_in_box(df_rect, img_name):
    img_root_name = img_name[:-4]
    txt_filepath = '../all_txt_files/'+img_root_name+'.txt'
    
    img_filepath = r'../all_img_files/'+img_root_name+'.jpg'
    img_file = Image.open(img_filepath)
    
    #image dimensions:
    img_width, img_height = img_file.size

    this_txt_file_info = get_dimension_lists(img_root_name)

    #current_object_info = 
    
    bbox_data = []
    for x in range(len(this_txt_file_info[0])):
        this_class = this_txt_file_info[4][x]
        this_xmin = this_txt_file_info[0][x]
        this_xmax = this_txt_file_info[2][x]
        this_ymin = this_txt_file_info[1][x]
        this_ymax = this_txt_file_info[3][x]
        this_tuple = (this_class, this_xmin, this_xmax, this_ymin, this_ymax)
        bbox_data.append(this_tuple)
    
    streamlit_width = 600
    streamlit_height = 150
    
    this_rect = [df_rect.iloc[0]['left'],df_rect.iloc[0]['top'],df_rect.iloc[0]['width'],df_rect.iloc[0]['height']]
    
    xmin_norm = this_rect[0] / streamlit_width
    xmax_norm = (this_rect[0] + this_rect[2]) / streamlit_width
    
    ymax_norm_for_plot = this_rect[1] / streamlit_height
    ymin_norm_for_plot = (this_rect[1] + this_rect[3]) / streamlit_height
    
    #ymin_norm_for_bbox_calc = (150 - this_rect[1] - this_rect[3]) / streamlit_height
    #ymax_norm_for_bbox_calc = (150 - this_rect[1]) / streamlit_height
    
    ymin_norm =ymax_norm_for_plot
    ymax_norm = ymin_norm_for_plot
    
    norms = [xmin_norm, xmax_norm, ymin_norm, ymax_norm]
    
    is_in_rect = []
    for x in range(len(bbox_data)):
        #normalize these values so they're on a comparable scale
        xmin = bbox_data[x][1] / img_width
        xmax = bbox_data[x][2] / img_width
        ymin = bbox_data[x][3] / img_height
        ymax = bbox_data[x][4] / img_height
        if (xmin > xmin_norm) & (ymin > ymin_norm) & (xmax < xmax_norm) & (ymax < ymax_norm):
            is_in_rect.append(bbox_data[x])
    
    order_in_rect = []
    for x in range(len(is_in_rect)):
        x_center = (is_in_rect[x][1] + is_in_rect[x][2]) / 2
        this_tuple = (x_center, is_in_rect[x][0]) #class
        order_in_rect.append(this_tuple)
    
    order_in_rect.sort()
    
    latex_classes_in_order = []
    for x in range(len(order_in_rect)):
        latex_classes_in_order.append(order_in_rect[x][1])
    
    #latex_classes_in_order = [labels_dict.get(x) for x in latex_class_nums_in_order]
    
    return (latex_classes_in_order, norms)





def latex_from_chars_list(list_of_chars):
    full_latex = ''.join(list_of_chars)
    to_display = '\\begin{equation*}'+full_latex+'\\end{equation*}'
    display(Latex(str(to_display)))





def latex_formula_from_char_list(char_list):
    full_latex = ''.join(char_list)
    return full_latex






def render_latex(formula, fontsize=5, dpi=300):
    """Renders LaTeX formula into Streamlit."""
    fig = plt.figure()
    text = fig.text(0, 0, '$%s$' % formula, fontsize=fontsize)

    fig.savefig(BytesIO(), dpi=dpi)  # triggers rendering

    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.05
    fig.set_size_inches((width, height))

    dy = (bbox.ymin / float(dpi)) / height
    text.set_position((0, -dy))

    buffer = BytesIO()
    fig.savefig(buffer, dpi=dpi, format='jpg')
    plt.close(fig)

    st.image(buffer)





def full_frac(numer, denom):
    full_latex = '\\frac{'+numer+'}{'+denom+'}'
    return full_latex





def full_expon(expon, base):
    full_latex = base+'^{'+expon+'}'
    return full_latex




def get_object_order(list_of_object_info):
    this_img = list_of_object_info
    total_num_objects = len(list_of_object_info)
    
    bbox_data = []
    for i in range(len(this_img)):
        this_latex_code = list_of_object_info[i][0]
        this_rect_dim = list_of_object_info[i][1]
        streamlit_width = 600
        streamlit_height = 150

        xmin_norm = this_rect_dim[0] / streamlit_width
        xmax_norm = (this_rect_dim[0] + this_rect_dim[2]) / streamlit_width

        ymax_norm_for_plot = this_rect_dim[1] / streamlit_height
        ymin_norm_for_plot = (this_rect_dim[1] + this_rect_dim[3]) / streamlit_height

        ymin_norm =ymax_norm_for_plot
        ymax_norm = ymin_norm_for_plot

        norms = [xmin_norm, xmax_norm, ymin_norm, ymax_norm]

        x_center = (xmin_norm + xmax_norm) / 2

        info_tuple = (this_latex_code, x_center)

        bbox_data.append(info_tuple)

    #order_in_rect = []
    #for x in range(len(bbox_data)):
        #x_center = (bbox_data[x][1][0] + bbox_data[x][1][1]) / 2
        #this_tuple = (x_center, bbox_data[x][0]) #class
        #order_in_rect.append(this_tuple)

    #return bbox_data.sort()
    #return list_of_object_info[0][0]
    #return order_in_rect.sort()
    sorted_list = sorted(bbox_data, key=lambda x: x[1])
    return sorted_list


def get_full_equation(sorted_list_classes_xcenters):
    latex_chars = []
    for x in range(len(sorted_list_classes_xcenters)):
        latex_chars.append(sorted_list_classes_xcenters[x][0])

    full_latex = ''.join(latex_chars)
    return full_latex
