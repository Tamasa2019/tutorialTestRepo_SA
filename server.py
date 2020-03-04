import bottle
import render

#added
import numpy as np

@bottle.route('/<width:int>/<height:int>')
def image(width, height):

    #check dimensions are same, if not meet in middle 
    if width != height:
        mean_dims = np.int(np.mean([width, height]))
        width = mean_dims
        height = mean_dims 

    #check dimensions are even, if not, add 1
    if not width%2==0: width = width + 1
    if not height%2==0: height = height + 1

    # generate a random [0,255] matrix for each quadrant,
    quadrant = np.random.randint(low=256, size=(np.int(width/2), np.int(width/2)))
    # make the top row: concat the quadrant with a flipped copy of the quadrant
    top_row = np.hstack((quadrant, np.fliplr(quadrant)))
    # bottom row: a mirrored version of the top row sub  
    bottom_row = np.flipud(top_row)
    # whole image: vertically concat both rows
    full_matrix = np.vstack((bottom_row, top_row))
    # return: render.image requires a list of pixel values 
    pixels = np.ndarray.tolist(np.ndarray.flatten(full_matrix))

    return render.image(width, height, pixels)

bottle.run(host='localhost', port=8080)
