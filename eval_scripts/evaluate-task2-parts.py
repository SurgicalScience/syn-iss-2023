import numpy as np
import csv
import os
import sys
from PIL import Image
from skimage.measure import label, regionprops
from scipy.spatial.distance import directed_hausdorff
from skimage.segmentation import find_boundaries
from skimage.metrics import hausdorff_distance

test_csv_path = sys.argv[1] 
predicted_masks_path = sys.argv[2] 
groundtruth_masks_path = sys.argv[3] 
metrics_csv_path = sys.argv[4] 

dict_colors = {
    0: (0, 0, 0),     # background
    1: (255, 214, 0), # shaft 
    2: (138, 0, 0),   # wrist
    3: (49, 205, 49), # jaw
}

MAX_HD_VALUE = 1100.0

def calculate_iou(gt_mask, pred_mask):
    union = np.sum(np.logical_or(gt_mask, pred_mask))
    # if pred and groundtruth are empty then return nan
    if union == 0:
        return np.nan
    intersection = np.sum(np.logical_and(gt_mask, pred_mask))
    iou = intersection / union
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
    img_rgb: np-array (uint8), shape (m,n,3)
        RGB image containing masks colored based on label_colors
    dict_colors: dict
        Keys are the label values to be assigned in the output and values are the
        RGB triplets.
    Returns:
    --------
    img_label: np-array (uint8), shape (m,n)
        2-D array of shape (img_rgb.shape[0], img_rgb.shape[1]) containing
        integer values per rgb color specified in dict_colors.
        Background pixels (i.e. pixels not matching specified colors) have a
        value of 0.
    """
    if img_rgb.shape[2] < 3:
        raise(IndexError(f"Supplied RGB image has {img_rgb.shape[2]} dimensions instead of expected 3 dimensions."))
    
    img_label = np.zeros((img_rgb.shape[0], img_rgb.shape[1]), dtype=np.uint8)
    for k, v in dict_colors.items():
        roi = ((img_rgb[:,:,0] == v[0])
                & (img_rgb[:,:,1] == v[1])
                & (img_rgb[:,:,2] == v[2]))
        img_label[roi] = k
    return img_label

def calculate_hd_skimage(gt_mask, pred_mask):
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
    gt_label = np.zeros_like(gt_mask)
    pred_label = np.zeros_like(pred_mask)
    gt_label[gt_mask] = 1
    pred_label[pred_mask] = 1
    return hausdorff_distance(find_boundaries(gt_label), find_boundaries(pred_label))

metrics_list_dict = {
    "class_0": [],   
    "class_1": [],
    "class_2": [],
    "class_3": [],
}

# loop through images in directory
with open(test_csv_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        image_hash = row[0]
        print(f"Evaluating image: {image_hash} ...")
        # read ground truth mask
        gt_path = os.path.join(groundtruth_masks_path, f"p-{image_hash}.png")
        if not os.path.exists(gt_path):
            continue
        gt_img = np.array(Image.open(gt_path))
        # convert the groundtruth rgb image into a label image
        gt = convert_rgb2label(gt_img, dict_colors)
        
        pm_path = os.path.join(predicted_masks_path, f"pred-{image_hash}.png")
        if os.path.exists(pm_path):
            pm_img = np.array(Image.open(pm_path))
            pm = convert_rgb2label(pm_img, dict_colors)
        else:
            pm = None  # set pm to None when there's no predicted mask

        # loop through class labels and calculate metrics
        for class_label in range(1, len(dict_colors)):
            if pm is not None:
                iou = calculate_iou(gt == class_label, pm == class_label)
                f_score = calculate_f_score(gt == class_label, pm == class_label)
                recall = calculate_recall(gt == class_label, pm == class_label)    
                precision = calculate_precision(gt == class_label, pm == class_label)
                hd_distance = calculate_hd_skimage(gt == class_label, pm == class_label)
                if hd_distance == float('inf'):
                    hd_distance = MAX_HD_VALUE
            else:
                iou = 0.0
                f_score = 0.0
                recall = 0.0
                precision = 0.0
                hd_distance = MAX_HD_VALUE
            
            # calculate names for the classes
            gt_name_class = f"p-{image_hash}"
            pm_name_class = f"pred-{image_hash}" if pm is not None else "No_Pred_Mask"
            
            metrics_row = [gt_name_class, pm_name_class, iou, f_score, recall, precision, hd_distance]
            # append the metrics_row to the corresponding metrics list in the dictionary
            metrics_list_dict[f"class_{class_label}"].append(metrics_row)

# write metrics to separate CSV files for each class
for class_label in range(1, len(dict_colors)):
    class_metrics_csv_path = os.path.join(metrics_csv_path, f"class_{class_label}_metrics.csv")
    with open(class_metrics_csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        header_row = ["Image_gt", "Image_pm", "IOU", "DSC", "Recall", "Precision", "HD"]
        writer.writerow(header_row)  
        writer.writerows(metrics_list_dict[f"class_{class_label}"])  