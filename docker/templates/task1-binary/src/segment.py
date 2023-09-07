from skimage.io import imsave, imread
import numpy as np

# ===========================================================
# Please include import statements needed for your code here.
# START PARTICIPANT CODE


# END PARTICIPANT CODE
# End of your import statements.
# ===========================================================

def convert_label2rgb(img_label, label_colors):
    """Convert label image to a 3-channel RGB image.

    Create a 3-channel RGB image filled with the specified colors in the corresponding pixels of the label image.
    Parameters:
    -----------
    img_label: numpy.ndarray (m,n)
        The label array that identified each pixel with its corresponding class label.
    label_colors: dict
        The mapping between class labels and the RGB colors that the resulting image would assign for each class
        label. The keys are integers specifying class labels that are present in img_label. They values are lists
        of RGB triplets in uint8 type (e.g., [240, 224, 200]).
    Returns:
    --------
    img_rgb: numpy.ndarray (m,n,3)
        The RGB image wherein pixels corresponding to the label image have been assigned their respective colors.
    """
    # check how many unique labels are present and if there are corresponding colors specified
    label_ids = np.unique(img_label)
    if len(label_ids) > len(label_colors.keys()):
        raise KeyError(
            f"There are more unique labels ({len(label_ids)}) present in label image then provided label colors ({len(label_colors.keys())})."
        )
    # check that each label has a corresponding color
    for id in label_ids:
        if id not in label_colors.keys():
            raise KeyError(f"There is no color specified for the label {id}.")
    # generate the RGB image
    img_rgb = np.zeros(img_label.shape + (3,), dtype=np.uint8)
    for id in label_ids:
        rr, cc = np.where(img_label == id)
        img_rgb[rr, cc, :] = label_colors[id]
    return img_rgb


def segment(input_image_path, output_mask_path):
    """
    Segment the provided image and save the result in an image file.
    Parameters:
    -----------

    Returns:
    --------

    """
    # ===============================================
    # Place your code below this comment block.
    # Your code must read an image present at the `input_image_path` location. 
    # Your code must generate a numpy array that is the same size as the input image. 
    # The numpy array should be assigned to a variable named `pred_labels`.
    # The numpy array must have a dtype of numpy.uint8 or np.uint8.
    # The array must indicate the class the pixel belongs to by assigning the appropriate class label ID. 
    # 
    # Example:
    # --------
    # The code below is to ensure that the scripts function and produce output in desired format. 
    # The code is simply creating a copy of sample groundtruth masks. 
    # The test data will NOT contain such groundtruth masks. 
    # 
    # START PARTICIPANT CODE
    # ===============================================

    # dummy predictions - creating predictions using the groundtruth images 
    # please delete this code 
    # ensure that the `pred_labels` variable is populated as per instructions above. 
    gt_rgb = imread(input_image_path.replace("s-", "b-"))
    pred_labels = np.zeros((gt_rgb.shape[0], gt_rgb.shape[1]), dtype=np.uint8)
    pred_labels[gt_rgb[:,:,0] == 255] = 1


    # ================================================
    # END PARTICIPANT CODE
    # End of your code. DO NOT modify the code beyond this point.
    # ================================================

    # convert the numpy array to RGB image and save it to file
    imsave(output_mask_path, convert_label2rgb(pred_labels, label_colors={0: [0, 0, 0], 1: [255, 255, 255]}))
    
    return