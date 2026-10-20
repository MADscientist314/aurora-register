"""Regenerate the QR code, print card, social preview image and favicon.

Run from the repository root:  python tools/make_cards.py
Needs: qrcode, Pillow, opencv-python (only to verify the QR decodes).
"""
from pathlib import Path

import cv2
import qrcode
import qrcode.image.svg
from PIL import Image, ImageDraw, ImageFont

URL = "https://madscientist314.github.io/aurora-register/"
ROOT = Path(__file__).resolve().parent.parent

# Brand palette (keep in sync with the :root variables in index.html)
PRIMARY = "#003087"    # BCM logo blue
SECONDARY = "#DA2530"  # Texas Children's red
INK = "#1A1A1A"
INK_3 = "#555555"
SURFACE = "#F5F5F5"

FONTS = Path("C:/Windows/Fonts")
SERIF_B = str(FONTS / "georgiab.ttf")
SANS = str(FONTS / "segoeui.ttf")
SANS_SB = str(FONTS / "seguisb.ttf")
MONO = str(FONTS / "consola.ttf")


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(str(FONTS / "segoeui.ttf"), size)


def make_qr(box):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=box, border=4)
    q.add_data(URL)
    q.make(fit=True)
    return q


def band(draw, width, height):
    split = int(width * 0.6)
    draw.rectangle([0, 0, split, height], fill=PRIMARY)
    draw.rectangle([split, 0, width, height], fill=SECONDARY)


def wrap(draw, text, fnt, max_w):
    words, lines, line = text.split(), [], ""
    for w in words:
        trial = (line + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            line = trial
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines


def print_card(qr_img):
    """Landscape 6 x 4 in card at 300 dpi."""
    W, H = 1800, 1200
    card = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(card)
    band(d, W, 22)
    x, y = 110, 120
    d.text((x, y), "AURORA", font=font(SERIF_B, 120), fill=PRIMARY)
    y += 150
    for line in wrap(d, "AI Ultrasound Risk Assessment for Obstetrical Recognition of Accreta", font(SANS, 34), 860):
        d.text((x, y), line, font=font(SANS, 34), fill=INK_3)
        y += 46
    y += 50
    d.text((x, y), "Register your interest", font=font(SANS_SB, 64), fill=INK)
    y += 100
    for line in ["Research access to AURORA",
                 "Help train AURORA 2.0: centers with",
                 "pathology-confirmed PAS cases"]:
        d.text((x, y), line, font=font(SANS, 40), fill=INK)
        y += 56
    d.line([(x, 960), (x + 860, 960)], fill="#E5E5E5", width=3)
    d.text((x, 990), "Baylor College of Medicine  ·  Texas Children's Hospital", font=font(SANS, 30), fill=INK_3)
    d.text((x, 1040), "Investigational device. Research use only.", font=font(MONO, 26), fill=INK_3)

    qx, qy, qs = 1080, 190, 620
    d.rectangle([qx - 30, qy - 30, qx + qs + 30, qy + qs + 30], outline="#E5E5E5", width=3)
    card.paste(qr_img.resize((qs, qs), Image.NEAREST), (qx, qy))
    d.text((qx + qs // 2, qy + qs + 70), "Scan to register", font=font(SANS_SB, 38), fill=INK, anchor="mm")
    d.text((qx + qs // 2, qy + qs + 125), URL.replace("https://", ""), font=font(MONO, 25), fill=INK_3, anchor="mm")
    card.save(ROOT / "qr" / "aurora-register-card.png", dpi=(300, 300), optimize=True)


def og_card():
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    band(d, W, 14)
    d.rectangle([0, 14, W, H], fill="white")
    d.text((80, 110), "AURORA", font=font(SERIF_B, 110), fill=PRIMARY)
    d.text((80, 250), "AI Ultrasound Risk Assessment for", font=font(SANS, 38), fill=INK_3)
    d.text((80, 298), "Obstetrical Recognition of Accreta", font=font(SANS, 38), fill=INK_3)
    d.text((80, 400), "Register interest: research access", font=font(SANS_SB, 46), fill=INK)
    d.text((80, 458), "and the AURORA 2.0 consortium", font=font(SANS_SB, 46), fill=INK)
    d.text((80, 560), "Baylor College of Medicine  ·  Texas Children's Hospital", font=font(SANS, 28), fill=INK_3)
    im.save(ROOT / "assets" / "og-card.png", optimize=True)


def favicon():
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
        f"<rect width='32' height='32' rx='6' fill='{PRIMARY}'/>"
        "<text x='16' y='23' text-anchor='middle' font-family='Georgia,serif' font-weight='700' "
        "font-size='20' fill='#FFFFFF'>A</text></svg>\n"
    )
    (ROOT / "assets" / "favicon.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    qr_png = make_qr(32).make_image(fill_color=INK, back_color="white").convert("RGB")
    qr_png.save(ROOT / "qr" / "aurora-register-qr.png", optimize=True)
    make_qr(10).make_image(image_factory=qrcode.image.svg.SvgPathImage).save(ROOT / "qr" / "aurora-register-qr.svg")
    print_card(qr_png)
    og_card()
    favicon()
    det = cv2.QRCodeDetector()
    for name in ["aurora-register-qr.png", "aurora-register-card.png"]:
        val, _, _ = det.detectAndDecode(cv2.imread(str(ROOT / "qr" / name)))
        print(name, "decodes OK" if val == URL else f"DECODE MISMATCH: {val!r}")
