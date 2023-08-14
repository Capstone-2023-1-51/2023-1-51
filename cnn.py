import tensorflow as tf
from keras.layers import Input, DepthwiseConv2D, Conv2D, concatenate, GlobalMaxPooling2D, Dense
from keras.preprocessing.image import ImageDataGenerator  # 경로 수정

def build_cnn_model2(input_shape):
    inputs = Input(shape=input_shape)

    # Depthwise Separable Convolution
    dw_conv = DepthwiseConv2D(3, padding='same', activation='relu')(inputs)

    # Convolution 레이어 반복
    conv_layers = []
    for filters in [64, 128, 256]:
        conv = Conv2D(filters, 3, padding='same', activation='relu')(dw_conv)
        conv_layers.append(conv)
        dw_conv = concatenate(conv_layers, axis=-1)

    # Global Max Pooling
    gmp = GlobalMaxPooling2D()(dw_conv)

    # Fully Connected 및 Output 레이어
    fc1 = Dense(128, activation='relu')(gmp)
    output = Dense(1, activation='sigmoid')(fc1)  # 클래스 개수 수정

    model = tf.keras.Model(inputs, output)
    return model


# 모델 구축
input_shape = (10000, 1, 3)  # 이미지의 입력 형태 설정 (예: 224x224 컬러 이미지)
model = build_cnn_model2(input_shape)

# 모델 컴파일
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])  # 손실 함수 변경

# 모델 요약 정보 출력
model.summary()

# 데이터 로딩 및 전처리 설정
train_data_generator = ImageDataGenerator(
    rescale=1.0/255,
    validation_split=0.2
)

# 학습 데이터 로딩
train_generator = train_data_generator.flow_from_directory(
    './images/',
    target_size=(100, 1),
    batch_size=32,
    class_mode='binary',  # 클래스 모드 변경
    subset='training'
)

# 모델 학습
model.fit(train_generator, epochs=10)