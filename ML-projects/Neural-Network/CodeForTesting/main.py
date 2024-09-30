import tensorflow as tf

# Загрузка обученной модели из файла .h5
model = tf.keras.models.load_model('D:/Programming/CodeForRecognition/100с_0нс.h5')

# Предсказания на новых данных
image_folder = 'D:/Programming/TrafficLightRecognitionVal/Светофоры/'
image_paths = [image_folder + f'{i}.jpg' for i in range (1, 66)]

# Загрузка и предобработка изображения
for i, image_path in enumerate(image_paths, start=1):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = image / 255.0  # Нормализация значений пикселей

    # Добавление размерности пакета (batch dimension) для предсказания
    image = tf.expand_dims(image, axis=0)

    # Получение предсказаний
    predictions = model.predict(image)

    # Печать результатов предсказаний
    print("изображение№",i)
    if predictions[0][0] > 0.5:
        print("Светофор присутствует на изображении")
    else:
        print("Светофор отсутствует на изображении")
    similarity = predictions[0][0] * 100
    similarity_formatted = "{:.2f}".format(similarity)
    print("Сходство со светофором на {}%".format(similarity_formatted))