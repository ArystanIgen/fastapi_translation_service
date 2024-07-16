FROM node:14

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install express google-translate-extended-api

COPY . .

EXPOSE 3000

CMD [ "node", "index.js" ]
