set -euo pipefail
cd /root/paperEveryDay

if [ -f ".env" ]; then
  set -a
  . ./.env
  set +a
else
  echo "Missing .env file. Create /root/paperEveryDay/.env with SMTP_* and EMAIL_*." >&2
  exit 1
fi

python run_daily.py