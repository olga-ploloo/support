FROM node:18

WORKDIR /frontend

COPY package*.json ./

RUN npm install

COPY . /frontend

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]