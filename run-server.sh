# /usr/local/bin/gunicorn app:app
uv run gunicorn app:app --workers 4 --bind 0.0.0.0:5000
