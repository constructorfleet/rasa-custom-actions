ARG RASA_SDK_VERSION=latest
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

WORKDIR /app/actions
COPY . .

RUN pip install -r requirements.txt \
    && pip install pyprika-0.1.0-py3-none-any.whl

WORKDIR /app

ENTRYPOINT ["./entrypoint.sh"]

CMD ["start", "--actions", "actions.actions"]
