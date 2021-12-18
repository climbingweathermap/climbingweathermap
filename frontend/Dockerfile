# build stage
FROM node as build-stage
RUN apk --no-cache add git make python3 g++
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
