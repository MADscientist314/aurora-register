# AURORA: register your interest

Registration page for clinicians, scientists and centers interested in **AURORA**, a research model that reads 2D transabdominal ultrasound for signs of placenta accreta spectrum (PAS).

**Live page:** https://madscientist314.github.io/aurora-register/

AURORA is an investigational device. It is not cleared by the FDA and is not for clinical diagnosis or patient management. This repository contains no patient data and no model code or weights.

## What is here

| Path | What it is |
|---|---|
| `index.html` | The registration page (static, no cookies, no analytics). |
| `form.json` | The Google Form link the page's buttons open. Empty until the form exists. |
| `form/build_form.gs` | Google Apps Script that builds the form and its response sheet. |
| `qr/aurora-register-qr.png`, `.svg` | QR code for the live page (error correction H). |
| `qr/aurora-register-card.png` | Print card, 6 x 4 in landscape at 300 dpi, with the QR and the URL. |
| `assets/og-card.png`, `assets/favicon.svg` | Link-preview image and site icon. |
| `tools/make_cards.py` | Regenerates the QR code, print card, preview image and icon. |

The QR code points at the registration page, not at the form, so the form can be replaced later without reprinting any QR codes.

## One-time setup: create the form

1. Sign in to the Google account that should own the responses.
2. Open https://script.google.com, choose **New project**, paste in `form/build_form.gs` and save.
3. Select `buildAuroraForm` and click **Run**. Approve the permissions prompt.
4. In the execution log, copy the **Respondent link**.
5. Paste it into `form.json`:

   ```json
   {
     "form_url": "https://docs.google.com/forms/d/e/.../viewform"
   }
   ```

6. Commit and push. The page's buttons switch from "Registration opens shortly" to the form within a minute or two.

The edit link and the response sheet link in the log stay private. Do not commit them.

## Form fields

Name, email, institution, role, country, interest (use AURORA for research and/or contribute images to train AURORA 2.0), interest in a multicenter collaboration, ultrasound machines used, interpretation or reporting software, approximate PAS cases per year, whether PAS is confirmed by histopathology, and contact consent. The form tells respondents not to enter patient information.

## Citation

Hammerquist AL, Lombaard HA, Sarada S, Mendez Martinez YH, Reed CC, Barrozo ER, Munoz JL, Lee W, Shamshirsaz AA, Belfort MA, Jochum MD. Artificial intelligence-based ultrasound screening for antenatal detection of placenta accreta spectrum. *Am J Obstet Gynecol MFM* 2026;8(10):102079. doi:10.1016/j.ajogmf.2026.102079

## Design

Colors follow the two institutions' web palettes, read from their live sites on 2026-10-20: Baylor College of Medicine logo blue `#003087` and navy `#031A6B` as primary, Texas Children's Hospital red `#DA2530` as accent (`#B70F19` where red is used for text), with Texas Children's neutrals. Type is Noto Serif and Noto Sans (Baylor's web typeface family). The page uses no institutional logos; any logo or joint lockup needs approval from BCM Marketing and Texas Children's Marketing.
