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

MAX_HD_VALUE = 1100.0

def calculate_iou(gt_mask, pred_mask):
    intersection = np.logical_and(gt_mask, pred_mask)
    union = np.logical_or(gt_mask, pred_mask)
    iou = np.sum(intersection) / np.sum(union)
    return iou

def calculate_f_score(gt_mask, pred_mask):
    # if pred and groundtruth are empty then return 1.0 instead of nan
    if np.sum(pred_mask) + np.sum(gt_mask) == 0:
        return 1.0
    intersection = np.sum(np.logical_and(gt_mask, pred_mask))
    f_score = 2 * intersection / (np.sum(gt_mask) + np.sum(pred_mask))
    return f_score

def calculate_recall(gt_mask, pred_mask):
    if np.sum(gt_mask) == 0:
        return np.nan
    intersection = np.logical_and(gt_mask, pred_mask)
    recall = np.sum(intersection) / np.sum(gt_mask)
    return recall

def calculate_precision(gt_mask, pred_mask):
    # precision is undefined when prediction is empty 
    # but this returns 0.0 to avoid impact on rankings.
    # returns nan when groundtruth is empty as well
    if np.sum(pred_mask) == 0:
        if np.sum(gt_mask) == 0:
            return np.nan
        else: 
            return 0.0
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
    return hausdorff_distance(find_boundaries(gt_mask), find_boundaries(pred_mask))


metrics_list = []

with open(test_csv_path, 'r') as file:
    reader = csv.reader(file)
    # loop through each row in the CSV file
    for row in reader:
        image_hash = row[0]
        print(f"Evaluating image: {image_hash} ...")
        # read ground truth mask image
        gt_path = os.path.join(groundtruth_masks_path, f"b-{image_hash}.png")
        if not os.path.exists(gt_path):
            continue  # skip if ground truth mask does not exist
        gt = np.array(Image.open(gt_path))
        gt_label = convert_rgb2label(gt, {1: [255, 255, 255]})

        # check if predicted mask exists
        pm_path = os.path.join(predicted_masks_path, f"pred-{image_hash}.png")
        if os.path.exists(pm_path):
            pm = np.array(Image.open(pm_path))
            pm_label = convert_rgb2label(pm, {1: [255, 255, 255]})

            iou = calculate_iou(gt_label == 1, pm_label == 1)
            f_score = calculate_f_score(gt_label == 1, pm_label == 1)
            recall = calculate_recall(gt_label == 1, pm_label == 1)
            precision = calculate_precision(gt_label == 1, pm_label == 1)
            hd = calculate_hd_skimage(gt_label, pm_label, segmentation_type="binary")
            if hd == float('inf'):
                hd = MAX_HD_VALUE
            
            # get names of gt and pm images without extension
            gt_name = f"b-{image_hash}"
            pm_name = f"pred-{image_hash}"
            
            # append the metrics to the metrics_list
            metrics_list.append((gt_name, pm_name, iou, f_score, recall, precision, hd))
        else:
            # if predicted mask does not exist, assign default values of 0 for fail
            metrics_list.append((gt_name, "No_Pred_Mask", 0.0, 0.0, 0.0, 0.0, MAX_HD_VALUE))


full_csv_path = os.path.join(metrics_csv_path, "metrics.csv")

with open(full_csv_path, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Image_gt", "Image_pm", "IOU", "F-Score", "Recall", "Precision", "HD"])  # write header row
    writer.writerows(metrics_list)  