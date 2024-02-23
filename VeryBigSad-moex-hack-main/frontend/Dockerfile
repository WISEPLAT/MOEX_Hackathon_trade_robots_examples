FROM node:18-alpine as build

WORKDIR /
COPY package.json .
COPY package-lock.json .
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine as prod

WORKDIR /
EXPOSE 3000
ENV NODE_ENV=production

COPY --from=build ./build ./build
COPY package.json .
COPY package-lock.json .
RUN npm ci --omit dev

ENTRYPOINT ["node", "./build"]
