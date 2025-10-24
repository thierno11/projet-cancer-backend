from fastapi import UploadFile, HTTPException
import shutil
from pathlib import Path
import cv2
import numpy as np
import base64
import torch
from .charger_model import model, device

async def effectuer_analyse(image: UploadFile):
    """
    Analyse une image mammographique
    """
    # Vérifier le type de fichier
    allowed_extensions = {".jpg", ".jpeg", ".png", ".dcm"}
    file_ext = Path(image.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Format de fichier non supporté. Formats acceptés: {', '.join(allowed_extensions)}"
        )

    # Créer un dossier temporaire pour stocker l'image
    upload_dir = Path("temp_uploads")
    upload_dir.mkdir(exist_ok=True)

    # Sauvegarder temporairement l'image
    file_path = upload_dir / image.filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        img_original, img_with_boxes, mask_bin, num_detections = predict_and_draw_boxes(str(file_path), model, device)

        # Encoder l'image originale en base64
        _, buffer_original = cv2.imencode('.jpg', img_original)
        img_original_base64 = base64.b64encode(buffer_original).decode('utf-8')

        # Encoder l'image avec les boîtes en base64
        _, buffer_boxes = cv2.imencode('.jpg', img_with_boxes)
        img_boxes_base64 = base64.b64encode(buffer_boxes).decode('utf-8')

        # Convertir le masque binaire en image visualisable (0-255) puis encoder
        mask_visual = (mask_bin * 255).astype(np.uint8)
        _, buffer_mask = cv2.imencode('.png', mask_visual)
        mask_base64 = base64.b64encode(buffer_mask).decode('utf-8')

        return {
            "status": "success",
            "message": f"Analyse terminée - {num_detections} zone(s) suspecte(s) détectée(s)",
            "num_detections": num_detections,
            "image_original": f"data:image/jpeg;base64,{img_original_base64}",
            "image_with_boxes": f"data:image/jpeg;base64,{img_boxes_base64}",
            "mask": f"data:image/png;base64,{mask_base64}",
            "filename": image.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}")

    finally:
        # Nettoyer le fichier temporaire
        if file_path.exists():
            file_path.unlink()





def predict_and_draw_boxes(img_path, model, device, threshold=0.5, min_area=50):
    """
    Effectue la prédiction sur une image mammographique et dessine les boîtes de détection

    Args:
        img_path: Chemin vers l'image à analyser
        model: Modèle PyTorch chargé
        device: Device PyTorch (cpu ou cuda)
        threshold: Seuil de confiance pour la détection (0-1)
        min_area: Aire minimale pour considérer une détection valide

    Returns:
        img_original: Image originale en couleur
        img_with_boxes: Image avec les boîtes de détection
        mask_bin: Masque binaire de segmentation
        num_detections: Nombre de zones détectées
    """
    model.eval()

    # Charger l'image en niveaux de gris
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Impossible de charger l'image: {img_path}")

    original_shape = img.shape
    print(f"Image chargée - Dimensions: {original_shape}")

    # Normalisation (0-1)
    img_normalized = img.astype(np.float32) / 255.0

    # Préparation du tensor pour le modèle (B, C, H, W)
    img_tensor = torch.from_numpy(img_normalized).unsqueeze(0).unsqueeze(0).to(device)
    print(f"Tensor shape: {img_tensor.shape}")

    # Inférence
    with torch.no_grad():
        mask_pred = model(img_tensor)

        # Appliquer sigmoid si le modèle ne le fait pas déjà
        if mask_pred.max() > 1.0 or mask_pred.min() < 0:
            mask_pred = torch.sigmoid(mask_pred)
            print("Sigmoid appliqué au masque de prédiction")

        mask_pred = mask_pred.squeeze().cpu().numpy()

    print(f"Masque prédit - Min: {mask_pred.min():.4f}, Max: {mask_pred.max():.4f}, Mean: {mask_pred.mean():.4f}")

    # Recherche du meilleur seuil
    thresholds_to_try = [threshold, 0.3, 0.5, 0.7, mask_pred.mean()]
    best_threshold = threshold
    max_detections = 0

    for t in thresholds_to_try:
        mask_temp = (mask_pred > t).astype(np.uint8)
        contours_temp, _ = cv2.findContours(mask_temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        num_valid = sum(1 for cnt in contours_temp if cv2.contourArea(cnt) > min_area)

        if num_valid > max_detections:
            max_detections = num_valid
            best_threshold = t

    print(f"Meilleur seuil trouvé: {best_threshold:.4f} avec {max_detections} détection(s)")

    # Binariser le masque avec le meilleur threshold
    mask_bin = (mask_pred > best_threshold).astype(np.uint8)

    # Trouver les contours
    contours, _ = cv2.findContours(mask_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Convertir l'image en couleur
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img_original = img_color.copy()
    img_with_boxes = img_color.copy()

    # Dessiner les rectangles de détection
    num_detections = 0
    detections_info = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(cnt)

            # Dessiner le rectangle JAUNE
            cv2.rectangle(img_with_boxes, (x, y), (x+w, y+h), (0, 255, 255), 4)

            # Ajouter un label avec le numéro
            num_detections += 1
            label = f"#{num_detections}"
            cv2.putText(img_with_boxes, label, (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

            detections_info.append({
                "id": num_detections,
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h),
                "area": float(area)
            })

            print(f"Zone {num_detections}: x={x}, y={y}, w={w}, h={h}, area={area:.0f}")

    print(f"✓ {num_detections} zone(s) suspecte(s) détectée(s)\n")

    return img_original, img_with_boxes, mask_bin, num_detections