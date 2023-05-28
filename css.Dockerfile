FROM node:20

WORKDIR /code
COPY . /code
RUN npm install

CMD ["npm", "start"]
