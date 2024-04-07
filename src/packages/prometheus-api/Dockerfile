FROM python:3.12 as build

COPY packages /tmp/packages

WORKDIR /tmp/packages/prometheus-api

RUN bin/build.sh

FROM python:3.12

RUN mkdir -p /usr/local/lib/papi
RUN mkdir -p /app/packages/api

ENV PYTHONPATH="/usr/local/lib/papi:$PYTHONPATH"

COPY --from=build /tmp/packages/prometheus-api/dist /tmp/dist

RUN cp -r /tmp/dist/libs/* /usr/local/lib/papi

RUN cp -r /tmp/dist/prometheus_api /app/packages/api

WORKDIR /app/packages/api

COPY packages/prometheus-api/docker /app/docker
RUN chmod +x /app/docker/*.sh

CMD ["/app/docker/entrypoint.sh", "run:uvicorn"]