ARG RASA_SDK_VERSION=latest
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

WORKDIR /app/actions
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]

CMD ["start", "--actions", "actions.actions"]
