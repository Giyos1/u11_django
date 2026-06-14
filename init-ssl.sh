#!/bin/sh
# ============================================================
#  SSL sertifikatni BIR MARTA olish uchun skript (serverda ishlaydi).
#  Ishlatish:  sh init-ssl.sh
#  Keyin certbot konteyneri o'zi avtomatik yangilab turadi.
# ============================================================
set -e

# ---- FAQAT SHU 3 QATORNI O'ZGARTIRASIZ ----
DOMAIN="booking.giyosdev.uz"  # asosiy domen
WWW=""                        # www versiyasi yo'q (kerak bo'lsa "www.booking.giyosdev.uz")
EMAIL="ibroximovs1998@gmail.com"
# -------------------------------------------

COMPOSE="sudo docker compose -f docker-compose.yml"
CERT_DIR="/etc/letsencrypt/live/$DOMAIN"

# www bo'sh bo'lmasa, "-d www..." qo'shamiz
WWW_ARG=""
[ -n "$WWW" ] && WWW_ARG="-d $WWW"

echo "### 1/6  db va web ko'tarilyapti..."
$COMPOSE up -d db web

echo "### 2/6  Vaqtinchalik (dummy) sertifikat yaratilyapti — nginx ishga tushishi uchun..."
$COMPOSE run --rm --entrypoint "sh -c 'mkdir -p $CERT_DIR && openssl req -x509 -nodes -newkey rsa:2048 -days 1 -keyout $CERT_DIR/privkey.pem -out $CERT_DIR/fullchain.pem -subj /CN=localhost'" certbot

echo "### 3/6  Nginx ishga tushirilyapti..."
$COMPOSE up -d nginx

echo "### 4/6  Dummy sertifikat o'chirilyapti..."
$COMPOSE run --rm --entrypoint "rm -Rf /etc/letsencrypt/live/$DOMAIN /etc/letsencrypt/archive/$DOMAIN /etc/letsencrypt/renewal/$DOMAIN.conf" certbot

echo "### 5/6  Let's Encrypt'dan haqiqiy sertifikat so'ralyapti..."
$COMPOSE run --rm --entrypoint certbot certbot \
  certonly --webroot -w /var/www/certbot \
  -d "$DOMAIN" $WWW_ARG \
  --email "$EMAIL" --agree-tos --no-eff-email

echo "### 6/6  Nginx qayta yuklanyapti..."
$COMPOSE exec nginx nginx -s reload

echo ""
echo "### TAYYOR!  https://$DOMAIN endi ishlashi kerak."