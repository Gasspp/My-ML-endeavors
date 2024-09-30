import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2


# Загрузка предварительно обученной модели InceptionResNetV2
base_model = InceptionResNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Заморозка всех слоев предварительно обученной модели
for layer in base_model.layers:
    layer.trainable = False

# Добавление пользовательского слоя классификации поверх предварительно обученной модели
model = tf.keras.models.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(1, activation='sigmoid')  # Бинарная классификация (есть светофор или нет)
])
checkpoint_callback = ModelCheckpoint(
    'модель_{epoch:02d}.h5', # Формат имени файла, где {epoch:02d} указывает на номер эпохи
    save_weights_only = False, # Сохранение полной модели, а не только весов
    save_best_only = False, # Сохранять модель после каждой эпохи
    monitor = 'val_loss', # Метрика, по которой принимается решение о сохранении модели
    mode = 'min' # Режим, в котором принимается решение о сохранении модели ('min' - минимизация метрики, 'max' - максимизация метрики)
)

# Компиляция модели
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Создание генератора данных для аугментации и загрузки изображений
data_generator = ImageDataGenerator(rescale=1./255, validation_split=0.2)  # Можно применять другие преобразования

# Загрузка обучающих и проверочных данных
train_data = data_generator.flow_from_directory(
    'D:/Programming/TrafficLightRecognitionTrain',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

val_data = data_generator.flow_from_directory(
    'D:/Programming/TrafficLightRecognitionVal',
    target_size = (224, 224),
    batch_size = 32,
    class_mode = 'binary',
    subset = 'validation'
)
#model.load_weights('модель_02.h5')
# Обучение модели
model.fit(
    train_data,
    epochs = 40,
    validation_data = val_data,
    callbacks = [checkpoint_callback]
)

# Сохранение обученной модели
model.save('модель(otchet).h5')