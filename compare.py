from headers import *
def compare(mask_image, result_image):
    #binarization
    result_image=np.where(result_image > 254, 1, 0)
    mask_image = np.where(mask_image > 254, 1, 0)

    total= len(result_image)*len(result_image[0])
    total_skin= np.sum(mask_image)
    total_no_skin= total-total_skin

    C= mask_image==result_image
    D=C< result_image
    E= np.logical_and(C, mask_image)

    false_positive=np.sum(D)/total_no_skin
    true_positive= np.sum(E)/ total_skin

    print("false positive=%.3f" %false_positive)
    print("true_positive=%.3f" %true_positive)

if __name__ == '__main__':
    path_mask_image = sys.argv[1]
    path_result_image = sys.argv[2]
    mask_image = io.imread(path_mask_image)[:,:,0]
    result_image= io.imread(path_result_image)[:,:,0]
    compare(mask_image, result_image)