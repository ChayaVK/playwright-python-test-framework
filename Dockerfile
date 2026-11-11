# Official Playwright image for Python: Chromium, Firefox and WebKit are already installed.
# Keep this tag the same as the playwright version in requirements.txt.
FROM mcr.microsoft.com/playwright/python:v1.63.0-noble

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default: the whole suite in Chromium. Override the command to run something else, for example:
#   docker run --rm pw-python-tests pytest -m smoke --browser firefox
CMD ["pytest", "-n", "auto"]
