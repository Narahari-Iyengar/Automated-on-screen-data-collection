# Automated-on-screen-data-collection
This code is written to collect temerature data using FLIR Tools.

The image is of a heated material with a grid on it. The task is to record the temperature at the center of each grid and save the data in a matrix form. Since the picture(at the time of taking) is not a top-view image, selecting the grid points and defining the vector for the cursor movement is important(Done only once at the beginning since every image is taken at the same angle with material fixed). Also, the image box* needs to be defined(only once in the beginning as the box is in a fixed location) - This is done by selecting the 4 corners of the image box. 

*Image box - The temperature reading is displayed in a box by the FLIR Tools software

There are 4 steps involved in this data collection:

    1. Load the images onto the FLIR Tools database
    2. Select grid points and image box points (Done only once at the beginning)
    3. Move cursor to specified grid point
    4. Capture image of temerature shown
    5. Convert image to text using OCR (Optical Character Recognition)
    6. Save data(matrix) as text file
    7. Move to next image

This code automates step 3 through step 7. 

**Packages Required:**

        Pillow
        Numpy
        Pytesseract
        Pyautogui
        cv2
        Pynput
        Imutils
        Time
      


