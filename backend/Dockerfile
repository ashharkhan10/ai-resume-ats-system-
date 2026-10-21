# Backend image for Hugging Face Spaces (Docker).
# Spaces expect the app on port 7860 and recommend running as user 1000.

FROM python:3.12-slim

RUN useradd -m -u 1000 user
USER user
ENV PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

WORKDIR /home/user/app

# Install packages first so this layer is cached between deploys
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=user . .

EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
