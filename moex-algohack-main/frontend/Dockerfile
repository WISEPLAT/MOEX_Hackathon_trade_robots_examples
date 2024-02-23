FROM node:18-alpine AS build

WORKDIR /usr/app

COPY ./package*.json ./
RUN npm ci -f

COPY . .

RUN npm run build

FROM nginx:latest AS frontend

RUN rm /usr/share/nginx/html/*
COPY --from=build /usr/app/dist/go.algo_frontned/ /usr/share/nginx/html/
COPY --from=build /usr/app/nginx.conf /etc/nginx/templates/default.conf.template