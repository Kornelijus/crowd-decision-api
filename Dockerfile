FROM python:3.10-alpine as base

ARG POETRY_VERSION=1.1.13
ARG APP_NAME=crowd_decision
ARG APP_PATH=/opt/$APP_NAME

FROM base as staging

ENV PYTHONDONTWRITEBYTECODE=1       \
    PYTHONFAULTHANDLER=1            \
    PYTHONUNBUFFERED=1              \
    PIP_NO_CACHE_DIR=1              \
    PIP_DISABLE_PIP_VERSION_CHECK=1

ENV POETRY_HOME=/opt/poetry         \
    POETRY_VERSION=$POETRY_VERSION  \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

RUN apk --no-cache add curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"


FROM staging as development

ARG APP_NAME
ARG APP_PATH

WORKDIR $APP_PATH
COPY ./poetry.lock ./pyproject.toml ./
COPY ./$APP_NAME ./$APP_NAME

RUN poetry install --no-root --no-dev

ENTRYPOINT [ "poetry", "run" ]
CMD ["uvicorn", "$APP_NAME.main:app", "--reload"]
