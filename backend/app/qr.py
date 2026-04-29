import os
import re

try:
    import qrcode
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "qrcode is required for QR generation. Install backend requirements first."
    ) from exc


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DEFAULT_QR_DIR = os.path.join(PROJECT_ROOT, "assets", "qrcodes")
DEFAULT_VERIFICATION_BASE_URL = os.getenv(
    "VERIFICATION_BASE_URL",
    "https://mathcodelab.de/verify/?id=",
)


def _safe_filename_part(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return cleaned.strip("._-") or "certificate"


def build_verification_url(certificate_id: str, base_url: str | None = None) -> str:
    base = (base_url or DEFAULT_VERIFICATION_BASE_URL).rstrip()
    if not base.endswith("="):
        base = base.rstrip("/") + "/"
    return f"{base}{certificate_id}"


def generate_certificate_qr(
    certificate_id: str,
    student_id: str | None = None,
    verification_url: str | None = None,
    output_dir: str | None = None,
) -> str:
    """Generate a QR image for the certificate verification URL and return its file path."""
    target_url = verification_url or build_verification_url(certificate_id)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    pixels = image.getdata()
    transparent_pixels = []
    for red, green, blue, alpha in pixels:
        if red >= 250 and green >= 250 and blue >= 250:
            transparent_pixels.append((255, 255, 255, 0))
        else:
            transparent_pixels.append((red, green, blue, 255))
    image.putdata(transparent_pixels)

    target_dir = output_dir or DEFAULT_QR_DIR
    os.makedirs(target_dir, exist_ok=True)
    filename_parts = []
    if student_id:
        filename_parts.append(_safe_filename_part(student_id))
    filename_parts.append(_safe_filename_part(certificate_id))
    file_path = os.path.join(target_dir, "_".join(filename_parts) + ".png")
    image.save(file_path)
    return file_path