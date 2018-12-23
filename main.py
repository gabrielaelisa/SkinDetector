from headers import *



def P_X_skin(pixel):
    """
    :param pixel: color pixel
    """
    X= np.tile(pixel, (16, 1))
    """
    X_u= X-mean_skin
    det= np.linalg.det(cov_skin)
    A=  w_i_skin*(1/(math.pow(math.pi*2, 3/2)*det))
    cov_inv= np.linalg.inv(cov_skin)
    B= X_u*cov_inv*X_u
    C =np.vectorize(math.exp)(B)
    """
    norm = []
    for i in range(16):
        norm.append(multivariate_normal.pdf(X[i], mean_skin[i], cov_skin[i]))
    return np.sum(np.array(norm) * w_i_skin)

def P_X_no_skin(pixel):
    X = np.tile(pixel, (16, 1))
    """
    X_u= X-mean_skin
    det= np.linalg.det(cov_skin)
    A=  w_i_skin*(1/(math.pow(math.pi*2, 3/2)*det))
    B=
    """
    norm= []
    for i in range(16):
        norm.append(multivariate_normal.pdf(X[i], mean_non_skin[i], cov_non_skin[i]))
    return np.sum(np.array(norm) * w_i_non_skin)

def classify(image, phi):
    return image< phi

if __name__ == '__main__':

    path_image= sys.argv[1]
    phi= sys.argv[2]
    image = io.imread(path_image)
    image2= image.copy()
    P_skin=np.apply_along_axis(P_X_skin, 2, image)
    P_non_skin= np.apply_along_axis(P_X_no_skin, 2, image2)
    result= image/image2
    skin=classify(result, phi)
    plt.show(skin)




