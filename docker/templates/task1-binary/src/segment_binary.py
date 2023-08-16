from skimage.io import imsave, imread
from skimage.color import label2rgb
import numpy as np

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
    # ===============================================

    # dummy predictions - creating predictions using the groundtruth images 
    # please delete this code 
    # ensure that the `pred_labels` variable is populated as per instructions above. 
    gt_rgb = imread(input_image_path.replace("s-", "b-"))
    pred_labels = np.zeros((gt_rgb.shape[0], gt_rgb.shape[1]), dtype=np.uint8)
    pred_labels[gt_rgb[:,:,0] == 255] = 1


    # ================================================
    # End of your code. DO NOT modify the code beyond this point.
    # ================================================

    # convert the numpy array to RGB image and save it to file
    imsave(output_mask_path, (label2rgb(pred_labels, colors=["white"]) * 255.0).astype(np.uint8))
    
    return