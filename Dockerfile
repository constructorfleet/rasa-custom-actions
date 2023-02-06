ARG RASA_SDK_VERSION=latest
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

WORKDIR /app/actions

COPY . .

RUN pip install -r requirements.txt

#RUN apt-get update \
#    && apt-get install -y git vim \
#    && cd /tmp \
#    && git clone https://github.com/constructorfleet/pyprika.git \
#    && cd pyprika \
#    && pip install setuptools wheel \
#    && python setup.py bdist_wheel \
#    && pip install dist/pyprika_client_client-0.1.0-py3-none-any.whl

WORKDIR /app

ENTRYPOINT ["./entrypoint.sh"]

CMD ["start", "--actions", "actions.actions"]
