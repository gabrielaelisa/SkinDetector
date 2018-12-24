from headers import *

iters=0

@np.vectorize
def P_X(pixel, mean, covariance):


    X_u= pixel-mean
    det= np.prod(covariance)
    A= (1/(math.pow(math.pi*2, 3/2)*det))
    B = (np.array(X_u).transpose()/covariance)* X_u
    C=math.exp((-1 / 2) * B)
    return (A*C)


def probability_skin(pixel):
    global iters
    iters += 1
    print(iters)
    X=np.tile(pixel, (16,1))
    result= np.vectorize(P_X)(X,mean_skin, cov_skin)
    return np.sum(np.dot(w_i_skin,result))

def classify(image, phi):
    return image> phi

if __name__ == '__main__':

    path_image= sys.argv[1]
    phi= sys.argv[2]
    image = io.imread(path_image)*1.0
    image2= image.copy()

    P_skin=np.apply_along_axis(probability_skin, 2, image)
    print(P_skin)
    skin=classify(P_skin, float(phi))
    imgplot = plt.imshow(skin, cmap='gray')
    plt.show()



