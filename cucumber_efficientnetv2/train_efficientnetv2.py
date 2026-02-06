import argparse
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import (ConfusionMatrixDisplay, classification_report,
                             confusion_matrix, roc_auc_score, roc_curve)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize


def parse_args():
    parser = argparse.ArgumentParser(description="Train EfficientNetV2 on cucumber dataset.")
    parser.add_argument("--data_dir", type=str, default="/datasets", help="Path to dataset root.")
    parser.add_argument("--output_dir", type=str, default="./outputs", help="Output directory.")
    parser.add_argument("--image_size", type=int, default=128, help="Image size (square).")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size.")
    parser.add_argument("--epochs", type=int, default=20, help="Number of epochs.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def configure_environment():
    tf.keras.mixed_precision.set_global_policy("mixed_float16")
    gpus = tf.config.list_physical_devices("GPU")
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)


def discover_dataset(data_dir):
    data_path = Path(data_dir)
    train_dir = data_path / "train"
    val_dir = data_path / "val"
    test_dir = data_path / "test"
    if train_dir.exists() and val_dir.exists() and test_dir.exists():
        return "split", train_dir, val_dir, test_dir
    return "single", data_path, None, None


def build_datasets_from_split(train_dir, val_dir, test_dir, image_size, batch_size, seed):
    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        image_size=(image_size, image_size),
        batch_size=batch_size,
        shuffle=True,
        seed=seed,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        image_size=(image_size, image_size),
        batch_size=batch_size,
        shuffle=False,
        seed=seed,
    )
    test_ds = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        image_size=(image_size, image_size),
        batch_size=batch_size,
        shuffle=False,
        seed=seed,
    )
    class_names = train_ds.class_names
    return train_ds, val_ds, test_ds, class_names


def build_datasets_from_single(data_path, image_size, batch_size, seed):
    file_paths = []
    labels = []
    class_names = sorted([p.name for p in data_path.iterdir() if p.is_dir()])
    class_to_idx = {name: idx for idx, name in enumerate(class_names)}

    for class_name in class_names:
        for img_path in (data_path / class_name).rglob("*"):
            if img_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}:
                file_paths.append(str(img_path))
                labels.append(class_to_idx[class_name])

    train_paths, temp_paths, train_labels, temp_labels = train_test_split(
        file_paths,
        labels,
        test_size=0.2,
        random_state=seed,
        stratify=labels,
    )
    val_paths, test_paths, val_labels, test_labels = train_test_split(
        temp_paths,
        temp_labels,
        test_size=0.5,
        random_state=seed,
        stratify=temp_labels,
    )

    def build_dataset(paths, labels, shuffle):
        path_ds = tf.data.Dataset.from_tensor_slices(paths)
        label_ds = tf.data.Dataset.from_tensor_slices(labels)
        ds = tf.data.Dataset.zip((path_ds, label_ds))
        if shuffle:
            ds = ds.shuffle(buffer_size=len(paths), seed=seed)

        def load_image(path, label):
            image = tf.io.read_file(path)
            image = tf.image.decode_image(image, channels=3, expand_animations=False)
            image = tf.image.resize(image, (image_size, image_size))
            image = tf.cast(image, tf.float32)
            return image, label

        ds = ds.map(load_image, num_parallel_calls=tf.data.AUTOTUNE)
        ds = ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)
        return ds

    train_ds = build_dataset(train_paths, train_labels, True)
    val_ds = build_dataset(val_paths, val_labels, False)
    test_ds = build_dataset(test_paths, test_labels, False)
    return train_ds, val_ds, test_ds, class_names


def build_model(num_classes, image_size):
    data_augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
            tf.keras.layers.RandomContrast(0.1),
        ],
        name="augmentation",
    )
    inputs = tf.keras.Input(shape=(image_size, image_size, 3))
    x = data_augmentation(inputs)
    x = tf.keras.applications.efficientnet_v2.preprocess_input(x)

    base_model = tf.keras.applications.EfficientNetV2B0(
        include_top=False,
        weights=None,
        input_tensor=x,
    )
    x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(
        num_classes,
        activation="softmax",
        dtype="float32",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4),
    )(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model


def get_last_conv_layer(model):
    for layer in reversed(model.layers):
        if len(layer.output_shape) == 4:
            return layer.name
    raise ValueError("No 4D layer found for Grad-CAM.")


def plot_training_curves(history, output_dir):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(history.history["loss"], label="train")
    axes[0].plot(history.history["val_loss"], label="val")
    axes[0].set_title("Loss")
    axes[0].legend()

    axes[1].plot(history.history["sparse_categorical_accuracy"], label="train")
    axes[1].plot(history.history["val_sparse_categorical_accuracy"], label="val")
    axes[1].set_title("Accuracy")
    axes[1].legend()

    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "training_curves.png"))
    plt.close(fig)


def evaluate_and_plot(model, test_ds, class_names, output_dir):
    y_true = []
    y_pred = []
    y_prob = []
    for images, labels in test_ds:
        probs = model.predict(images, verbose=0)
        preds = np.argmax(probs, axis=1)
        y_true.extend(labels.numpy())
        y_pred.extend(preds)
        y_prob.extend(probs)

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    y_prob = np.array(y_prob)

    report = classification_report(y_true, y_pred, target_names=class_names)
    with open(os.path.join(output_dir, "classification_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
    fig, ax = plt.subplots(figsize=(8, 8))
    disp.plot(ax=ax, cmap="Blues", xticks_rotation=45)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "confusion_matrix.png"))
    plt.close(fig)

    y_true_bin = label_binarize(y_true, classes=list(range(len(class_names))))
    fig, ax = plt.subplots(figsize=(8, 6))
    for idx, class_name in enumerate(class_names):
        fpr, tpr, _ = roc_curve(y_true_bin[:, idx], y_prob[:, idx])
        auc_score = roc_auc_score(y_true_bin[:, idx], y_prob[:, idx])
        ax.plot(fpr, tpr, label=f"{class_name} (AUC={auc_score:.2f})")
    ax.plot([0, 1], [0, 1], "k--", linewidth=1)
    ax.set_title("One-vs-Rest ROC Curves")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "roc_curves.png"))
    plt.close(fig)


def make_gradcam_heatmap(model, image, last_conv_layer_name, pred_index=None):
    grad_model = tf.keras.Model(
        [model.inputs],
        [model.get_layer(last_conv_layer_name).output, model.output],
    )
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(image)
        if pred_index is None:
            pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]
    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.reduce_max(heatmap)
    return heatmap.numpy()


def save_gradcam_examples(model, test_ds, class_names, output_dir):
    last_conv_layer_name = get_last_conv_layer(model)
    images, labels = next(iter(test_ds))
    images = images[:6]
    labels = labels[:6]

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.flatten()

    for idx, (img, label) in enumerate(zip(images, labels)):
        input_img = tf.expand_dims(img, axis=0)
        heatmap = make_gradcam_heatmap(model, input_img, last_conv_layer_name)
        heatmap = tf.image.resize(heatmap[..., np.newaxis], (img.shape[0], img.shape[1]))
        heatmap = tf.squeeze(heatmap).numpy()
        heatmap = np.uint8(255 * heatmap)
        heatmap = plt.cm.jet(heatmap)[:, :, :3]
        overlay = 0.4 * heatmap + (img.numpy() / 255.0)
        axes[idx].imshow(np.clip(overlay, 0, 1))
        axes[idx].set_title(f"True: {class_names[label.numpy()]}")
        axes[idx].axis("off")

    fig.suptitle("Grad-CAM Examples", fontsize=14)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "gradcam_examples.png"))
    plt.close(fig)


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    configure_environment()

    mode, train_dir, val_dir, test_dir = discover_dataset(args.data_dir)
    if mode == "split":
        train_ds, val_ds, test_ds, class_names = build_datasets_from_split(
            train_dir,
            val_dir,
            test_dir,
            args.image_size,
            args.batch_size,
            args.seed,
        )
    else:
        train_ds, val_ds, test_ds, class_names = build_datasets_from_single(
            train_dir,
            args.image_size,
            args.batch_size,
            args.seed,
        )

    train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(tf.data.AUTOTUNE)
    test_ds = test_ds.prefetch(tf.data.AUTOTUNE)

    model = build_model(len(class_names), args.image_size)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    checkpoint_path = os.path.join(args.output_dir, "best_model.keras")
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            checkpoint_path,
            monitor="val_sparse_categorical_accuracy",
            save_best_only=True,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
        ),
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
        callbacks=callbacks,
    )

    plot_training_curves(history, args.output_dir)
    evaluate_and_plot(model, test_ds, class_names, args.output_dir)
    save_gradcam_examples(model, test_ds, class_names, args.output_dir)


if __name__ == "__main__":
    main()
