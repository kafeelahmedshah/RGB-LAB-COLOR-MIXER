# 🎨 RGB + LAB Color Mixer

A professional interactive **Python + Streamlit** application for creating and exploring digital colors using **RGB** and **CIELAB** values.

## Features

- RGB sliders: R, G, B from 0–255
- CIELAB sliders: L* 0–100, a* -128 to +127, b* -128 to +127
- Live color preview with HEX code
- RGB → XYZ → CIELAB conversion
- CIELAB → XYZ → RGB conversion
- Standard sRGB / D65 reference
- Current RGB, LAB, and HEX values
- Save and clear color history
- Responsive Streamlit tabs and layout
- No external API for conversion
- GitHub and Streamlit Community Cloud ready

## Files

```text
rgb-lab-color-mixer/
├── app.py
├── requirements.txt
└── README.md
```

## Run Locally

```bash
git clone https://github.com/YOUR-USERNAME/rgb-lab-color-mixer.git
cd rgb-lab-color-mixer
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in your terminal, normally `http://localhost:8501`.

## Upload to GitHub

Create a GitHub repository named `rgb-lab-color-mixer` and upload `app.py`, `requirements.txt`, and `README.md`.

Or use Git:

```bash
git init
git add app.py requirements.txt README.md
git commit -m "Create RGB LAB Color Mixer"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/rgb-lab-color-mixer.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## Deploy on Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud.
2. Connect your GitHub account.
3. Select the `rgb-lab-color-mixer` repository.
4. Select the `main` branch.
5. Set `app.py` as the main file.
6. Deploy.

Streamlit will install the packages listed in `requirements.txt`.

## Color Conversion

RGB conversion follows:

```text
RGB → Linear sRGB → XYZ (D65) → CIELAB
```

The reverse conversion is:

```text
CIELAB → XYZ (D65) → Linear sRGB → RGB
```

The app implements these calculations directly in Python using standard sRGB transfer functions, D65 reference white, and the standard sRGB/XYZ matrices.

## Gamut Note

CIELAB covers colors that are not always displayable in sRGB. When a LAB value converts outside the RGB 0–255 range, the displayed RGB channels are clipped to the valid range.

## License

Suitable for educational, portfolio, and personal projects. Add an open-source license if you plan to distribute the project publicly.
