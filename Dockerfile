# syntax=docker/dockerfile:1
LABEL org.opencontainers.image.description derbynames-microservice-markovify

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install -U pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc git

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install application into container
COPY . .

EXPOSE 5000
# EXPOSE 8000
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD ["gunicorn","-b","0.0.0.0:5000","-w","4","app:app"]
# ENTRYPOINT ["gunicorn","-b","0.0.0.0","-w","4","app:app"]
