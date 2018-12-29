from headers import *
def compare(mask_image, result_image):
    total= len(result_image)*len(result_image[0])
    #print(mask_image)
    #print(total)
    C= mask_image==result_image
    D=C< result_image
    E= C< mask_image
    print(np.sum(D))
    false_positive=np.sum(D)/total
    false_negative= np.sum(E)/ total
    print("false positive=%.3f" %false_positive)

if __name__ == '__main__':
    path_mask_image = sys.argv[1]
    path_result_image = sys.argv[2]
    mask_image = io.imread(path_mask_image)
    result_image= io.imread(path_result_image)
    compare(mask_image, result_image)