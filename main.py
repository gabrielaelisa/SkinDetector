from headers import *

iters = 0


def P_X_skin(pixel):
    """
    :param pixel: color pixel
    """

    global iters
    iters += 1
    #print(iters)

    X = np.tile(pixel, (16, 1))
    X_u = X - mean_skin
    det = np.prod(cov_skin, axis=1)
    A = w_i_skin * (1 / (math.pow(math.pi * 2, 3 / 2) * det))
    B = np.sum(X_u*X_u/cov_skin, 1)
    C = np.exp((-1 / 2) * B)
    return np.sum(A*C)


def P_X_no_skin(pixel):
    global iters
    iters += 1
    #print(iters)

    X = np.tile(pixel, (16, 1))
    X_u = X - mean_non_skin
    det = np.prod(cov_non_skin, axis=1)
    A = w_i_non_skin * (1 / (math.pow(math.pi * 2, 3 / 2) * det))
    B = np.sum(X_u*X_u/cov_non_skin, 1)
    C = np.exp((-1 / 2) * B)
    return np.sum(A*C)


def classify(image, phi):
    return image > phi


if __name__ == '__main__':
    path_image = sys.argv[1]
    phi = float(sys.argv[2])
    image = io.imread(path_image) * 1.0
    image2 = image.copy()

    P_skin = np.apply_along_axis(P_X_skin, 2, image)
    P_non_skin = np.apply_along_axis(P_X_no_skin, 2, image2)
    result = P_skin / P_non_skin
    skin = classify(result, phi)
    plt.imsave("results/image_"+ path_image[19:21] + "_" + str(phi) + ".png" , skin, cmap ='gray')