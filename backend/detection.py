import cv2
import os
from ultralytics import YOLO

# =========================
# 配置部分（你只要改这里）
# =========================
MODEL_PATH = "best.pt"              # 模型路径
SOURCE_PATH = "evaluation.mp4"      # 输入图片或视频路径

PERSON_CLASS_ID = 0                 # 0: 人
WEAPON_CLASS_IDS = {1}              # 1: 武器

# 输出路径配置
OUTPUT_DIR = "output"               # 所有结果放在这个文件夹
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_IMAGE_PATH = os.path.join(OUTPUT_DIR, "result_image.jpg")
OUTPUT_VIDEO_PATH = os.path.join(OUTPUT_DIR, "result_video.mp4")


def get_safety_status(person_count: int, has_weapon: bool):
    """
    根据当前画面的人数 + 是否检测到武器给出安全状态和颜色。
      - 如果检测到武器 => UNSAFE（红色）
      - 否则如果无人 => SAFE（绿色）
      - 否则 => REVIEW（黄色）
    """
    if has_weapon:
        return "UNSAFE (weapon detected)", (0, 0, 255)        # 红色
    if person_count == 0:
        return "SAFE (no people)", (0, 255, 0)                # 绿色
    else:
        return "REVIEW (people present)", (0, 255, 255)       # 黄色


def process_frame(frame, model):
    """
    对单帧做检测、画框、统计人数和武器数量，并标注安全状态。
    返回：处理后的 frame、人数、武器数、安全状态文字
    """
    results = model(frame, verbose=False)[0]

    person_count = 0
    weapon_count = 0
    has_weapon = False

    # 遍历检测结果
    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        label = results.names.get(cls_id, str(cls_id))

        # 默认框颜色：白色
        color = (255, 255, 255)

        # 人
        if cls_id == PERSON_CLASS_ID:
            person_count += 1
            color = (255, 0, 0)   # 红/蓝色框标人
            label = f"person {conf:.2f}"

        # 武器 / weapon-like
        if cls_id in WEAPON_CLASS_IDS:
            weapon_count += 1
            has_weapon = True
            color = (0, 0, 255)   # 红色框标武器
            label = f"weapon {conf:.2f}"

        # 只对人和武器画框
        if cls_id == PERSON_CLASS_ID or cls_id in WEAPON_CLASS_IDS:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(
                frame,
                label,
                (int(x1), int(y1) - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1,
                cv2.LINE_AA,
            )

    # 计算安全状态
    safety_text, safety_color = get_safety_status(person_count, has_weapon)

    # 顶部画一条半透明条用于显示文字
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], 60), (0, 0, 0), -1)
    alpha = 0.4
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    # 左上角：安全状态
    cv2.putText(
        frame,
        f"Safety: {safety_text}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        safety_color,
        2,
        cv2.LINE_AA,
    )

    # 左下角：人数 + 武器数
    info_text = f"Persons: {person_count}  Weapons: {weapon_count}"
    cv2.putText(
        frame,
        info_text,
        (20, frame.shape[0] - 20),  # 左下角
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    return frame, person_count, weapon_count, safety_text


def is_image_file(path: str):
    ext = os.path.splitext(path)[1].lower()
    return ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]


def main():
    if not os.path.exists(SOURCE_PATH):
        print(f"Error: {SOURCE_PATH} does not exist.")
        return

    print("Loading YOLO model...")
    model = YOLO(MODEL_PATH)
    print("Model loaded.")

    # ========= 图片模式 =========
    if is_image_file(SOURCE_PATH):
        print("Running in IMAGE mode.")
        img = cv2.imread(SOURCE_PATH)
        if img is None:
            print("Error: cannot read image.")
            return

        processed, person_count, weapon_count, safety_text = process_frame(img, model)
        print(f"[Result] Safety: {safety_text}, Persons: {person_count}, Weapons: {weapon_count}")

        # 显示结果
        cv2.imshow("VenueShield AI - Image", processed)
        print(f"Saving result image to: {OUTPUT_IMAGE_PATH}")
        cv2.imwrite(OUTPUT_IMAGE_PATH, processed)  # ✅ 导出标注后的图片

        print("Press any key in the window to exit.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

    # ========= 视频模式 =========
    print("Running in VIDEO mode.")
    cap = cv2.VideoCapture(SOURCE_PATH)
    if not cap.isOpened():
        print("Error: cannot open video.")
        return

    # 获取视频参数，用于保存输出视频
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25  # 兜底
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, fps, (width, height))

    window_name = "VenueShield AI - Video"
    print("Press 'q' in the window to quit.")
    print(f"Saving annotated video to: {OUTPUT_VIDEO_PATH}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed, person_count, weapon_count, safety_text = process_frame(frame, model)

        # 显示
        cv2.imshow(window_name, processed)
        # ✅ 写入输出视频
        out.write(processed)

        # 按 q 退出
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Done.")


if __name__ == "__main__":
    main()
