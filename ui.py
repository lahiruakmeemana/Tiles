import sys
import json
from PyQt5.QtWidgets import QGridLayout,QApplication, QWidget, QLabel, QPushButton, QMessageBox,QComboBox,QFormLayout,QLineEdit
from predict import TilePredictor

with open("fields.json") as file:
    fields = json.load(file)
columns = ['Tile_Color', 'Tile_Size', 'Room_Type', 'Room_Color', 'Tile_type', 'Finish_Type']

tile_sizes= {'300 x 300 mm':(0.3,0.3), 
             '600 x 300 mm':(0.6,0.3), 
             '550 x 300 mm':(0.55,0.3), 
             '500 x 500 mm':(0.5,0.5),
             '400 x 400 mm':(0.4,0.4), 
             '200 x 200 mm':(0.2,0.2)}

def dialog():
    inputs= [txtbox.text()]
    if txtbox.text()=='' or int(txtbox.text())>1200:
        rec.setText("Enter price lower than Rs:1200")
        return 
    rec.setText('Recommend Tiles:')
        
    for i in range(6):
        inputs.append(str(qcb[i].currentText()))
    outputs = predictor.predict(inputs)
    for i in range(3):
        labels[i].setText(' '+str(outputs[i]))
    
    #labels.show()
    
    print(outputs)
    
def calculate():
    count = 0
    try:
        floor_height,floor_width,skirting_height, door_width = [float(i.text()) for i in count_details]
    except:
        rec_tiles.setText('Enter values in meters')
        return
    tile_height,tile_width = tile_sizes[qcb[1].currentText()]
    
    area = floor_height * floor_width
    tile_area = tile_height * tile_width
    count += area/tile_area
    
    skirting_len = 2*(floor_height+floor_width)-door_width
    if skirting_height>0:
        len_per_tile = tile_area/ skirting_height
        count += skirting_len/len_per_tile
    
    count = int(count * 1.05)    
    
    rec_tiles.setText('Required Tiles:')
    tile_count.setText(str(count))
    return
      
if __name__ == "__main__":
    
    predictor = TilePredictor()
    #first = True
    
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(500,400)
    w.setWindowTitle('Tile Recommender')
    labels = [QLabel(w) for i in range(3)]
    
    label = QLabel()
    label.setText('Input Tile Details:')
    
    btn = QPushButton()
    btn.setText('Recommend')
    btn.clicked.connect(dialog)
    
    calc = QPushButton()
    calc.setText('Calculate')
    calc.clicked.connect(calculate)
    
    
    qcb = []
    for i in range(6):
        cb = QComboBox()
        cb.setFixedWidth(180)
        cb.addItems(fields[columns[i]])
        qcb.append(cb)
    txtbox = QLineEdit()
    qcb.append(txtbox)
    
    rec = QLabel()
    rec_tiles = QLabel()
    
    layout = QGridLayout()

    layout.addWidget(label,0,0)
    
    arr = [' Tile Color:',' Tile Size:',' Room Type:',' Room Color:',' Finish Type:',' Tile Type:',' Tile Price:']
    for i,field in enumerate(arr):
        layout.addWidget(QLabel(field),i+1,0)
        layout.addWidget(qcb[i],i+1,1)
    
    layout.addWidget(btn,9,0,1,2)
    layout.addWidget(calc,9,2,1,2)
    
    layout.addWidget(rec,10,0,1,2)
    layout.addWidget(rec_tiles,10,2,1,2)
    for i,name in enumerate(labels):
        layout.addWidget(name,11+i,0,1,2)
    
    
    count_details = []
    arr = ['Floor Height','Floor Width','Skirting Height', 'Door Width']
    for i,field in enumerate(arr):
        temp = QLineEdit()
        count_details.append(temp)
        layout.addWidget(QLabel(' '+field+':'),i+1,2)
        layout.addWidget(temp,i+1,3)
      
    
    tile_count = QLabel()

    layout.addWidget(tile_count,11,2,1,2)
    
    w.setLayout(layout)
    w.show()
    sys.exit(app.exec_())
    
