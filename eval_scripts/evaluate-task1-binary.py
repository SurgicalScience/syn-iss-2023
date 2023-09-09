import numpy as np
import csv
import os
import sys
from PIL import Image
from skimage.measure import label, regionprops
from scipy.spatial.distance import directed_hausdorff
from skimage.segmentation import find_boundaries 
from skimage.metrics import hausdorff_distance

# the below 4 lines are the arguments that are passed using the command line
test_csv_path = sys.argv[1] 
predicted_masks_path = sys.argv[2] 
groundtruth_masks_path = sys.argv[3] 
metrics_csv_path = sys.argv[4] 

def calculate_iou(gt_mask, pred_mask):
    intersection = np.logical_and(gt_mask, pred_mask)
    union = np.logical_or(gt_mask, pred_mask)
    iou = np.sum(intersection) / np.sum(union)
    return iou

def calculate_f_score(gt_mask, pred_mask):
    intersection = np.logical_and(gt_mask, pred_mask)
    precision = np.sum(intersection) / np.sum(pred_mask)
    recall = np.sum(intersection) / np.sum(gt_mask)
    f_score = 2 * (precision * recall) / (precision + recall)
    return f_score

def calculate_recall(gt_mask, pred_mask):
    intersection = np.logical_and(gt_mask, pred_mask)
    recall = np.sum(intersection) / np.sum(gt_mask)
    return recall

def calculate_precision(gt_mask, pred_mask):
    intersection = np.logical_and(gt_mask, pred_mask)
    precision = np.sum(intersection) / np.sum(pred_mask)
    return precision

def convert_rgb2label(img_rgb, dict_colors):
    """
    Reverse of skimage.color.label2rgb

    Parameters:
    -----------
    img_rgb: np-array (uint8)
        RGB image containing masks colored based on label_colors
    dict_colors: dict
        Keys are the label values to be assigned in the output and values are the
        RGB triplets, e.g., {1: [234,155,136], 2: [139,139,240]}
        Keys should be positive non-zero integers, Values should be valid integer
        RGB triplets [0,255]
    Returns:
    --------
    img_label: np-array (uint8)
        2-D array of shape (img_rgb.shape[0], img_rgb.shape[1]) containing
        integer values per rgb color specifiec in dict_colors.
        Background pixels (i.e. pixels don't matching specified colors) have a
        value of 0.
    """
    img_label = np.zeros((img_rgb.shape[0], img_rgb.shape[1]), dtype=np.uint8)
    for k, v in dict_colors.items():
        roi = ((img_rgb[:,:,0] == v[0])
                & (img_rgb[:,:,1] == v[1])
                & (img_rgb[:,:,2] == v[2]))
        img_label[roi] = k
    return img_label
        
def calculate_hd_skimage(gt_mask, pred_mask, segmentation_type):
    """
    Parameters:
    -----------
    gt_mask, pred_mask: nd-array (type: uint8)
        RGB image showing the mask.
    Returns:
    --------
    distance: float
        The hausdorff distance between the boundaries generated 
    """
    if segmentation_type == "binary":
        dict_colors = {
            1: (255, 255, 255)
        }
    elif segmentation_type == "parts":
        dict_colors = {
            1: (255,214,0),
            2: (138,0,0),
            3: (49,205,49)
        }
    else:
        RuntimeError(f"Incorrect segmentation type specified. Should be one of \"binary\" or \"parts\", user specified: {segmentation_type}.")
        return
    # convert images into a label image
    gt_label = convert_rgb2label(gt_mask, dict_colors)
    pred_label = convert_rgb2label(pred_mask, dict_colors)
    return hausdorff_distance(find_boundaries(gt_label), find_boundaries(pred_label))


metrics_list = []

with open(test_csv_path, 'r') as file:
    reader = csv.reader(file)
    # loop through each row in the CSV file
    for row in reader:
        image_name = row[0]  
        image_hash = image_name 
        
        print(image_hash) 

        # read ground truth mask image
        gt_path = os.path.join(groundtruth_masks_path, f"b-{image_hash}.png")
        if not os.path.exists(gt_path):
            continue  # skip if ground truth mask does not exist
        gt = np.array(Image.open(gt_path))

        # check if predicted mask exists
        pm_path = os.path.join(predicted_masks_path, f"pred-{image_hash}.png")
        if os.path.exists(pm_path):
            pm = np.array(Image.open(pm_path))

            iou = calculate_iou(gt, pm)
            f_score = calculate_f_score(gt, pm)
            recall = calculate_recall(gt, pm)
            precision = calculate_precision(gt, pm)
            hd = calculate_hd_skimage(gt, pm, segmentation_type="binary")
            
            # get names of gt and pm images without extension
            gt_name = os.path.splitext(os.path.basename(gt_path))[0]
            pm_name = os.path.splitext(os.path.basename(pm_path))[0]
            
            # append the metrics to the metrics_list
            metrics_list.append((gt_name, pm_name, iou, f_score, recall, precision, hd))
        else:
            # if predicted mask does not exist, assign default values of 0 for fail
            metrics_list.append((gt_name, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        
        # print metrics: CAN COMMENT OUT
        print("Image_gt:", gt_name)
        print("Image_pm:", pm_name)
        print("IOU:", iou)
        print("F-Score:", f_score)
        print("Recall:", recall)
        print("Precision:", precision)
        print("HD:", hd)

full_csv_path = os.path.join(metrics_csv_path, "metrics.csv")

with open(full_csv_path, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Image_gt", "Image_pm", "IOU", "F-Score", "Recall", "Precision", "HD"])  # write header row
    writer.writerows(metrics_list)  