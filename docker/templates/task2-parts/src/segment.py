from skimage.io import imsave, imread
from skimage.color import label2rgb
import numpy as np

# ===========================================================
# Please include import statements needed for your code here.
# START PARTICIPANT CODE


# END PARTICIPANT CODE
# End of your import statements.
# ===========================================================

def segment(input_image_path, output_mask_path):
    """
    Segment the provided image and save the result in an image file.
    Parameters:
    -----------
    input_image_path: str
        Path to the file that contains the image to be segmented.
    Returns:
    --------
    output_mask_path: str
        Path to the file where the predicted mask should be stored as an image file.
    """
    # ===============================================
    # Place your code below this comment block.
    # Your code must read an image present at the `input_image_path` location. 
    # Your code must generate a numpy array that is the same size as the input image. 
    # The numpy array should be assigned to a variable named `pred_labels`.
    # The numpy array must have a dtype of numpy.uint8 or np.uint8.
    # The array must indicate the class the pixel belongs to by assigning the appropriate class label ID. 
    # Class IDs: shaft = 1, wrist = 2, jaw = 3, background = 0
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
    gt_rgb = imread(input_image_path.replace("s-", "p-"))
    pred_labels = np.zeros((gt_rgb.shape[0], gt_rgb.shape[1]), dtype=np.uint8)
    class_colors = {
        1: [255, 214, 0],
        2: [138, 0, 0],
        3: [49, 205, 49]
    }
    for k, v in class_colors.items():
        roi = (
            (gt_rgb[:,:,0] == v[0]) &
            (gt_rgb[:,:,1] == v[1]) & 
            (gt_rgb[:,:,2] == v[2])
        )
        pred_labels[roi] = k

    # ================================================
    # END PARTICIPANT CODE
    # End of your code. DO NOT modify the code beyond this point.
    # ================================================

    # convert the numpy array to RGB image and save it to file
    imsave(output_mask_path, (label2rgb(pred_labels, colors=["gold", "darkred", "limegreen"]) * 255.0).astype(np.uint8))
    
    return