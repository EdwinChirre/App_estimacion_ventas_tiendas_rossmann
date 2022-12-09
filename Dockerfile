FROM python:3.10-slim as base

FROM base as dependencies

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --ignore-pipfile


FROM base as runtime

COPY --from=dependencies /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
#ENV PATH="/.venv/bin/sh"

WORKDIR /app

COPY ./ .

EXPOSE 3000

CMD ["uvicorn","predict_store_sale_api:app","--host","0.0.0.0","--port","3000"]