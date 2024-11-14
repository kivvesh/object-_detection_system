import cv2
import numpy as np

# Загрузка классов
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Загрузка модели YOLO
net = cv2.dnn.readNetFromDarknet('yolov4.cfg', 'yolov4.weights')

# Функция для обнаружения объектов
def detect_objects(image):
    height, width = image.shape[:2]

    # Подготовка изображения для нейросети
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Получение выходных слоев
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Запуск детекции
    outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    # Обработка результатов
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Порог уверенности
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Рисование рамки вокруг объекта
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Ненужные рамки
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image

# Загрузка изображения
image_path = 'img.png'  # Укажите путь к вашему изображению
image = cv2.imread(image_path)

# Обнаружение объектов
result_image = detect_objects(image)

# Автоматическое определение размера для вывода
max_width = 800  # Максимальная ширина для вывода
aspect_ratio = result_image.shape[1] / result_image.shape[0]  # Соотношение сторон

# Определяем новую высоту на основе максимальной ширины и соотношения сторон
new_width = max_width
new_height = int(max_width / aspect_ratio)

# Изменение размера выходного изображения
resized_image = cv2.resize(result_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

# Отображение результата
cv2.imshow('Detected Objects', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()