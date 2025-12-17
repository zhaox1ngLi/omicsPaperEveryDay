set -euo pipefail
cd /home/lizhaoxing/omicsPaperEveryDay

if [ -f ".env" ]; then
  set -a
  . ./.env
  set +a
else
  echo "Missing .env file. Create /home/lizhaoxing/omicsPaperEveryDay/.env with SMTP_* and EMAIL_*." >&2
  exit 1
fi

PYTHON="/home/gpu/anaconda3/bin/python"
if [ ! -x "$PYTHON" ]; then
  echo "Python not found or not executable: $PYTHON" >&2
  exit 1
fi

"$PYTHON" run_daily.py