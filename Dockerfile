FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/run/sshd \
    && echo "root:Docker!" | chpasswd

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY sshd_config /etc/ssh/sshd_config

RUN sed -i 's/\r$//' startup.sh \
    && chmod +x startup.sh

EXPOSE 8000
EXPOSE 2222

CMD ["/app/startup.sh"]