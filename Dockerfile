ARG RASA_SDK_VERSION=latest
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

WORKDIR /app/actions

RUN apt update \
    && apt get install git \
    && git clone https://github.com/constructorfleet/pyprika.git \
    && cd pyprika \
    && pip install setuptools wheel \
    && python setup.py bdist_wheel \
    && pip install dist/pyprika-0.1.0-py3-none-any.whl

COPY . .

RUN pip install -r requirements.txt

WORKDIR /app

ENTRYPOINT ["./entrypoint.sh"]

CMD ["start", "--actions", "actions.actions"]
