# build stage
FROM node:lts-alpine as build-stage
RUN apk --no-cache add git
WORKDIR /app
COPY package*.json ./
RUN npm install --production=false
COPY . .

RUN npm run compile:sass
RUN npm run build
RUN export VUE_APP_BACKEND_ADDRESS=$(echo "$(cut -d'=' -f2 <<< $(grep VUE_APP_BACKEND_ADDRESS .env))")

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
