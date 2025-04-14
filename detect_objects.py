import cv2
import numpy as np
import os

YOLO_DIR = os.path.join(os.path.dirname(__file__), "ai", "yolo")

def load_yolo():
    weights = os.path.join(YOLO_DIR, "yolov3.weights")
    cfg = os.path.join(YOLO_DIR, "yolov3.cfg")
    net = cv2.dnn.readNet(weights, cfg)
    classes = []
    with open(os.path.join(YOLO_DIR, "coco.names"), "r") as f:
        classes = f.read().splitlines()
    return net, classes

def detect_with_camera():
    net, classes = load_yolo()
    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()
        height, width, _ = img.shape

        blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)

        output_layers = net.getUnconnectedOutLayersNames()
        outputs = net.forward(output_layers)

        boxes, confidences, class_ids = [], [], []

        for output in outputs:
            for detect in output:
                scores = detect[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x, center_y, w, h = [int(val * width if i % 2 == 0 else val * height) for i, val in enumerate(detect[:4])]
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = f"{classes[class_ids[i]]}: {int(confidences[i] * 100)}%"
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("YOLO Object Detection", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
