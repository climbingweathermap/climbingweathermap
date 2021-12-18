# build stage
FROM node:lts-alpine as build-stage
RUN apk add --no-cache python3 build-base # build base includes g++ and gcc and Make
WORKDIR /app
COPY package*.json ./
RUN npm install --production=false
COPY . .

RUN npm run compile:sass
# RUN npm run builddev 
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
