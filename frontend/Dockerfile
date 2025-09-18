FROM node:20-alpine
WORKDIR /usr/src/app
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN yarn install
COPY . .
EXPOSE 5173
CMD ["yarn", "dev", "--", "--host", "0.0.0.0"]


