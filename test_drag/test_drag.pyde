
source = None
clicked = False

def setup():
    size(1280, 720)

def draw():
    global source
    global clicked
    
    background(255)
    fill(255)
    rect(5, 5, 1270, 710)
    
    if mousePressed:
        if clicked == False:
            clicked = True
            source = (mouseX, mouseY)
            
            if 20 < source[0] < 120 and 20 < source[1] < 120:
                print("clicked")
        
        if 20 < source[0] < 120 and 20 < source[1] < 120 \
            and 20 < mouseX < 120 and 20 < mouseY < 120:
            fill(255, 0, 0)
        else:
            fill(255)
    else:
        clicked = False
            
    rect(20, 20, 100, 100)
    
    fill(0)

    text(mouseX, 1000, 20)
    text(mouseY, 1000, 30)
    if source:
        text(source[0], 500, 500)
        text(source[1], 500, 600)
