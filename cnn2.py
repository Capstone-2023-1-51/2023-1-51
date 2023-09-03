import tensorflow as tf
from keras.layers import Input, DepthwiseConv2D, Conv2D, concatenate, GlobalMaxPooling2D, Dense, Flatten
from keras.preprocessing.image import ImageDataGenerator


def depthwise_separable_conv_block(input_layer, kernel_size):
    x = DepthwiseConv2D(kernel_size, padding='same', activation='relu')(input_layer)
    x = Conv2D(10, 1, activation='relu')(x)
    return x


def build_cnn_model(input_shape):
    input_layer = Input(shape=input_shape)

    # 크기별 Depthwise Convolution 연산 수행
    x = depthwise_separable_conv_block(input_layer, (1, 1))
    conv_blocks = [x]
    for kernel_size in range(2, 11):
        x = depthwise_separable_conv_block(x, (1, kernel_size))
        conv_blocks.append(x)

    # 연산 결과 합치기
    concatenated = concatenate(conv_blocks, axis=-1)
    conv = Conv2D(64, (1, 3), padding='same', activation='relu')(concatenated)

    gmp = GlobalMaxPooling2D()(conv)
    # Fully Connected 및 Output 레이어
    #fc = Flatten()(gmp)
    fc1 = Dense(256, activation='relu')(gmp)
    output = Dense(1, activation='sigmoid')(fc1)

    # 모델 생성
    model = tf.keras.Model(inputs=input_layer, outputs=output)
    return model


# 모델 구축
input_shape = (1, 10000, 3)  # 이미지의 입력 형태 설정
model = build_cnn_model(input_shape)

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
    target_size=(1, 10000),
    batch_size=32,
    class_mode='binary',  # 클래스 모드 변경
    subset='training'
)
print(train_generator.labels)
# 모델 학습
model.fit(train_generator, epochs=10)

# 모델 저장
model.save('my_model2.h5')
