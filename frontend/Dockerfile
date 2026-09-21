# syntax=docker/dockerfile:1.7
FROM node:20-alpine AS base

ENV NEXT_TELEMETRY_DISABLED=1

WORKDIR /app

# Install deps only (cached layer)
COPY package.json package-lock.json ./
RUN npm ci

# Copy source
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
