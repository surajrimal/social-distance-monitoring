# import necessary libraries 
import cv2 
import numpy as np 


pts1 = np.float32([[786, 117], [1067, 149], [634, 615], [183, 487]]) 
pts2 = np.float32([[400, 100], [600, 100], [600, 900], [400, 900]]) 
# Apply Perspective Transform Algorithm 
matrix = cv2.getPerspectiveTransform(pts1, pts2) 
mpixel = 10000 #minimum pixel that we need to compare


def draw_points_in_vicinity(points, image):
    image = np.hstack((image,transform_perspective(image.copy())))
    transformed_points = []
    for p in points:
        px = (matrix[0][0]*p[0] + matrix[0][1]*p[1] + matrix[0][2]) / ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2]))
        py = (matrix[1][0]*p[0] + matrix[1][1]*p[1] + matrix[1][2]) / ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2]))
        transformed_points.append([px, py])

    total_people_at_risk = 0
    for i in range(len(transformed_points)):
        for j in range(i+1, len(transformed_points)):
            x1,x2 = int(transformed_points[i][0]), int(transformed_points[j][0])
            y1,y2 = int(transformed_points[i][1]), int(transformed_points[j][1])
            dist = ((x1-x2)**2)+((y1-y2)**2)
            if(dist<=mpixel):
                x1,x2 = int(points[i][0]), int(points[j][0])
                y1,y2 = int(points[i][1]), int(points[j][1])
                cv2.line(image,(x1, y1-50),(x2, y2-50),(50,50,255),2)
                total_people_at_risk = total_people_at_risk + 1

    image = cv2.rectangle(image, (5, 5), (240,50), (50, 50, 50), -1)             
    cv2.putText(image,"Total People: " + str(len(points)), (15,20), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255) )
    cv2.putText(image,"Total transmission paths: " + str(total_people_at_risk), (15,40), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255) )
    return image

def transform_perspective(image):
    transform = cv2.warpPerspective(image, matrix, (750, 1000))
    return  cv2.resize(transform, (500, 720), interpolation = cv2.INTER_AREA)