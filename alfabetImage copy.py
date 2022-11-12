import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.morphology import erosion
from scipy.ndimage import morphology

def countLakesAndBays(region):
    symbol = ~region.image
    lb = label(symbol)
    lakes = 0
    bays = 0
    for reg in regionprops(lb):
        is_lake = True
        for y, x in reg.coords: 
            if y == 0 or x == 0 or y == region.image.shape[0] - 1 or x == region.image.shape[1] - 1:
                is_lake = False
                break
        lakes += is_lake
        bays += not is_lake             
    return lakes, bays


def has_vline(image): # для нахождения ровного штриха в В
    return 1 in erosion(np.mean(image, 0), [1, 1, 1])

def has_hline(image): # для нахождения вертикального штриха
    return 1 in np.mean(image, 1)

# def centroid(image): #фигня не работает
#     pos = np.where(image)
#     cy = np.mean(pos[0])
#     cx = np.mean(pos[1])
#     if image[cy, cx] > 0:
#         return True
#     else:
#         return False

def recognize(image_region):
    lakes, bays = countLakesAndBays(image_region)
    if lakes == 2: # B or 8
        if has_vline(image_region.image):
            return 'B'
        else:
            return '8'
    elif lakes == 1:
        if bays == 4:
            return '0'
        # elif has_vline(image_region.image):
        #     return 'P'
        elif bays == 3:
            return 'A'
        else:
            y, x = image_region.centroid_local
            x = x / image_region.image.shape[0]
            y = y / image_region.image.shape[1]
            if x > 0.3 and y > 0.3:
                return 'D'
            else:
                return 'P'     
    elif lakes == 0:
        if np.mean(image_region.image) == 1.0:
            return '-'
        elif has_vline(image_region.image):
            return '1'
        elif bays == 2:
            return '/'
        elif has_hline(image_region.image):
            return '*'
        elif bays == 4:
            return 'X'
        else:
            return 'W'
            



image = plt.imread("C:\\progrpython\\img\\symbols\\symbols.png")
image = np.mean(image,2)

image[image > 0] = 1
labeled = label(image)

regions = regionprops(labeled)
result = {}
for reg in regions:
    symbol = recognize(reg)
    # if symbol == 'D':
    #     plt.figure()
    #     plt.imshow(reg.image)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1
print (result)

print(np.max(labeled) == sum(result.values()))

# print(recognize(regions[35]))
# plt.imshow(regions[35].image)
plt.show()
