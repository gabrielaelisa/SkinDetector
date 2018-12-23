from headers import *
import warnings

warnings.filterwarnings('error')

def suppressWarnings(func):
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            func(*args, **kwargs)

    return wrapper

@suppressWarnings
@np.vectorize
def exponent(num):
    try:
        return math.exp(num)
    except OverflowError:
        return float('inf')

iters= 0
def P_X_skin(pixel):
    """
    :param pixel: color pixel
    """


    global iters
    iters += 1
    print(iters)

    X= np.tile(pixel, (16, 1))
    X_u= X-mean_skin
    det= np.prod(cov_skin_1,axis=1)
    #det= np.linalg.det(cov_skin)
    A=  w_i_skin*(1/(math.pow(math.pi*2, 3/2)*det))
    cov_inv= np.linalg.inv(cov_skin)
    B = np.dot(X_u * np.diagonal(cov_inv, 0, 2, 1), X_u.transpose())
    try:
        C = np.vectorize(math.exp)((-1 / 2) * B)
    except OverflowError:
        C= float('inf')
    return np.sum(A*C)



def P_X_no_skin(pixel):

    X= np.tile(pixel, (16, 1))

    X_u= X-mean_non_skin
    det= np.linalg.det(cov_non_skin)
    A=  w_i_non_skin*(1/(math.pow(math.pi*2, 3/2)*det))
    #cov_inv= np.linalg.inv(cov_non_skin)
    B= np.dot(X_u*np.diagonal(cov_inv, 0,2,1),X_u.transpose())
    C= np.vectorize(exponent)((-1 / 2) * B)
    return np.sum(A*C)



def classify(image, phi):
    return image> phi

if __name__ == '__main__':

    path_image= sys.argv[1]
    phi= sys.argv[2]
    image = io.imread(path_image)*1.0
    image2= image.copy()

    P_skin=np.apply_along_axis(P_X_skin, 2, image)
    P_non_skin= np.apply_along_axis(P_X_no_skin, 2, image2)
    result= P_skin/P_non_skin
    print(P_skin)
    print(P_non_skin)
    print(result)
    skin=classify(result, float(phi))
    imgplot = plt.imshow(skin, cmap='gray')
    plt.show()





