FROM node:9.1.0-slim

ENV ENV ${env:-dev}

EXPOSE 4200

RUN npm install -g yarn;
RUN mkdir /app
WORKDIR /app
COPY ./microblog/package.json ./
COPY ./microblog/yarn.lock ./
RUN yarn install;

# add in our code and build
ADD ./microblog /app/
RUN yarn build;
