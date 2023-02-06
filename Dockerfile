ARG RASA_SDK_VERSION=latest
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

WORKDIR /app/actions

# Change back to root user to install dependencies
USER root

# To install system dependencies
RUN apt-get update -qq && \
    apt-get install -y <NAME_OF_REQUIRED_PACKAGE> && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

#RUN apt-get update \
#    && apt-get install -y git vim \
#    && cd /tmp \
#    && git clone https://github.com/constructorfleet/pyprika.git \
#    && cd pyprika \
#    && pip install setuptools wheel \
#    && python setup.py bdist_wheel \
#    && pip install dist/pyprika_client_client-0.1.0-py3-none-any.whl

# Switch back to non-root to run code
USER 1001

COPY . .

WORKDIR /app

ENTRYPOINT ["./entrypoint.sh"]

CMD ["start", "--actions", "actions.actions"]
