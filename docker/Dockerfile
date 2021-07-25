FROM node:16-stretch as NODEBUILD


COPY ./cidash-ui /app/

WORKDIR /app/

RUN npm install; npm run build


FROM nginx

COPY --from=NODEBUILD /app/build /statichtml

COPY ./docker/10-cidash.sh /docker-entrypoint.d/10-cidash.sh

