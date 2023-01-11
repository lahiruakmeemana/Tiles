import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
import tensorflow.keras as keras
from tensorflow.keras import layers
import np_utils
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,MinMaxScaler

class TilePredictor:
    def __init__(self):
        data = pd.read_csv('data.csv')
        
        self.tile_names = np.sort(data['Tile_Name'].unique())

        price = data.pop('Tile_Price')
        data['Tile_Price'] = price
        self.fields = data.drop(['Tile_Price'],axis=1).columns
        self.uniques = [np.sort(data[i].unique()) for i in self.fields]

        self.encoders = [OneHotEncoder(handle_unknown='ignore') for i in range(7)]

        for i,encoder in enumerate(self.encoders):
            encoder.fit(np.array(self.uniques[i]).reshape((-1,1)))
            
        price = pd.DataFrame(data['Tile_Price'])
        price['Tile_Price'].values.astype(float)         
        self.max_price = data['Tile_Price'].max()
        self.model = keras.models.load_model('trained_model.h5')
        
        
    def predict(self,x):

        x = np.array(x).reshape((-1,1))

        test= [int(x[0])/self.max_price]
        for i in range(1,7):
            encoded = self.encoders[i].transform(np.array(x[i]).reshape((-1,1))).toarray().flatten()
            test.extend(encoded)

        test = np.array(test).reshape((1,175))

        
        res = self.model.predict(test)

        out = self.tile_names[np.argsort(res.flatten())[-1:-4:-1]]
        return out.tolist()
