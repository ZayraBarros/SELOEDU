# utils/uploads.py
import os
from uuid import uuid4
from pathlib import Path
from hashlib import md5

from flask import current_app
from werkzeug.utils import secure_filename

# Pillow é opcional (usamos se disponível)
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


# -------- auxiliares --------

def _initials_from_name(name, max_chars=2):
    if not name:
        return "?"
    parts = [p for p in name.strip().split() if p]
    if len(parts) == 1:
        return (parts[0][:2].upper()).ljust(max_chars)[:max_chars]
    return (parts[0][0] + parts[-1][0]).upper()[:max_chars]

def _color_from_name(name):
    h = md5((name or "").encode("utf-8")).hexdigest()
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    def clamp(x, lo=40, hi=220):
        return max(lo, min(hi, x))
    return clamp(r), clamp(g), clamp(b)

def _load_font(size):
    if not PIL_AVAILABLE:
        return None
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(str(p), size=size)
            except Exception:
                pass
    return ImageFont.load_default()


# -------- API que a sua view importa --------

def remove_file_safe(filename: str | None):
    """Remove um arquivo de dentro do UPLOAD_FOLDER, se existir."""
    if not filename:
        return
    try:
        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    except Exception:
        return
    file_path = upload_folder / filename
    try:
        if file_path.exists() and upload_folder in file_path.parents:
            file_path.unlink()
    except Exception:
        current_app.logger.exception("Erro removendo arquivo %s", filename)


def save_image(file_storage=None, user_name: str | None = None):
    """
    Salva a imagem enviada (se houver) e cria thumbnail.
    Se não houver arquivo e houver user_name, tenta gerar avatar de iniciais (thumb).
    Retorna (filename_original, filename_thumb)
    """
    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    # Caso com upload
    if file_storage:
        try:
            ext = secure_filename(file_storage.filename).rsplit(".", 1)[-1].lower()
        except Exception:
            ext = "png"
        filename = f"{uuid4().hex}.{ext}"
        filepath = upload_folder / filename

        # salva original
        file_storage.save(filepath)

        # cria thumb (se Pillow disponível)
        thumb_name = None
        if PIL_AVAILABLE:
            try:
                img = Image.open(filepath).convert("RGB")
                img.thumbnail(current_app.config.get("THUMBNAIL_SIZE", (200, 200)))
                thumb_name = f"thumb_{filename}"
                img.save(upload_folder / thumb_name, optimize=True)
            except Exception:
                thumb_name = None

        return filename, thumb_name

    # Caso sem upload: gerar avatar de iniciais (thumb) se possível
    if user_name and PIL_AVAILABLE:
        w, h = current_app.config.get("THUMBNAIL_SIZE", (200, 200))
        initials = _initials_from_name(user_name)
        bg = _color_from_name(user_name)
        img = Image.new("RGBA", (w, h), color=bg + (255,))
        draw = ImageDraw.Draw(img)

        font_size = int(h * 0.5)
        font = _load_font(font_size) or ImageFont.load_default()
        tw, th = draw.textsize(initials, font=font)
        x = (w - tw) / 2
        y = (h - th) / 2 - int(0.05 * h)
        draw.text((x+1, y+1), initials, font=font, fill=(0, 0, 0, 100))
        draw.text((x, y), initials, font=font, fill=(255, 255, 255, 255))

        thumb_name = f"initials_{uuid4().hex}.png"
        img.convert("RGB").save(upload_folder / thumb_name, format="PNG", optimize=True)
        return None, thumb_name

    return None, None
