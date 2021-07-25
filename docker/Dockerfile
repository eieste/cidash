FROM node:16-stretch as NODEBUILD


COPY ./cidash-ui /app/

WORKDIR /app/

RUN npm install; npm run build


FROM nginx

COPY --from=NODEBUILD /app/build /statichtml

COPY ./docker/entrypoint.bash /entrypoint.bash

ENTRYPOINT /entrypoint.bash

EXPOSE 80

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]
