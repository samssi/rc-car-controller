clean:
	@find . -name '*.py?' -delete
	@find . -name '.cache' -type d | xargs rm -rf
	@find . -name '__pycache__' -type d | xargs rm -rf
	@rm -rf .venv

.venv/bin/activate: requirements.txt
	@test -d .venv || python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install --no-cache-dir -Ur requirements.txt || exit -1
	touch .venv/bin/activate

env: .venv/bin/activate

start:
	FLASK_APP=main.py flask run --host=0.0.0.0

start-local:
	FLASK_APP=main.py flask run