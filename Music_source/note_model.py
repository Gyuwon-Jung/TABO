import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical

# 데이터 폴더 경로
data_folder = 'note_data'
classes = ['whole', 'half', 'quarter', 'eight', 'sixteen']

# 데이터 로딩 및 전처리
data = []
labels = []

for i, class_name in enumerate(classes):
    class_path = os.path.join(data_folder, class_name)
    for image_name in os.listdir(class_path):
        image_path = os.path.join(class_path, image_name)
        image = load_img(image_path, target_size=(64, 64))
        image_array = img_to_array(image)
        data.append(image_array)
        labels.append(i)

data = np.array(data) / 255.0
labels = np.array(labels)

# 데이터를 훈련용과 테스트용으로 분할
train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2, random_state=42)

# 레이블을 One-Hot 인코딩으로 변환
train_labels_onehot = to_categorical(train_labels, num_classes=len(classes))
test_labels_onehot = to_categorical(test_labels, num_classes=len(classes))

# CNN 모델 생성
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(len(classes), activation='softmax')
])

# 모델 컴파일
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 모델 훈련
model.fit(train_data, train_labels_onehot, epochs=10, batch_size=32, validation_data=(test_data, test_labels_onehot))
