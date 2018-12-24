from headers import *


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
    #--------------------------------------------------
    x_u_0 = (X_u * X_u)[:, [0]] / cov_skin_1[:, [0]]
    x_u_1 = (X_u * X_u)[:, [1]] / cov_skin_1[:, [1]]
    x_u_2 = (X_u * X_u)[:, [2]] / cov_skin_1[:, [2]]

    B = x_u_0 + x_u_1 + x_u_2
    try:
        C = np.vectorize(math.exp)((-1 / 2) * B)
    except OverflowError:
        C= float('inf')
    return np.sum(A*C)

def P_X_no_skin(pixel):
    global iters
    iters += 1
    print(iters)
    X = np.tile(pixel, (16, 1))
    X_u = X - mean_non_skin
    det = np.prod(cov_non_skin_1, axis=1)
    A = w_i_non_skin * (1 / (math.pow(math.pi * 2, 3 / 2) * det))
    cov_inv = np.linalg.inv(cov_non_skin)
    #------------------------------------------------

    x_u_0=(X_u*X_u)[:,[0]]/cov_non_skin_1[:,[0]]
    x_u_1 = (X_u * X_u)[:, [1]]/cov_non_skin_1[:,[1]]
    x_u_2 = (X_u * X_u)[:, [2]]/cov_non_skin_1[:,[2]]

    B = x_u_0+x_u_1+x_u_2
    try:
        C = np.vectorize(math.exp)((-1 / 2) * B)
    except OverflowError:
        C = float('inf')
    return np.sum(A * C)


"""
def P_X_no_skin(pixel):
    global iters
    iters+=1
    print(iters)
    X= np.tile(pixel, (16, 1))
    X_u= X-mean_non_skin
    det= np.linalg.det(cov_non_skin)
    A=  w_i_non_skin*(1/(math.pow(math.pi*2, 3/2)*det))
    #cov_inv= np.linalg.inv(cov_non_skin)
    B= np.dot(X_u * cov_non_skin_1, X_u.transpose())
    C= np.vectorize(exponent)((-1 / 2) * B)

    
    return np.sum(A*C)
 
    try:
        C = np.vectorize(math.exp)((-1 / 2) * B)
    except OverflowError:
        C= float('inf')
    return np.sum(A*C)
"""


def classify(image, phi):
    return image> phi

if __name__ == '__main__':

    path_image= sys.argv[1]
    phi= sys.argv[2]
    image = io.imread(path_image)*1.0
    image2= image.copy()

    P_skin=np.apply_along_axis(P_X_skin, 2, image)
    #P_non_skin= np.apply_along_axis(P_X_no_skin, 2, image2)
    #result= P_skin/P_non_skin
    #print(result)
    print(P_skin)
    skin=classify(P_skin, float(phi))
    imgplot = plt.imshow(skin, cmap='gray')
    plt.show()





