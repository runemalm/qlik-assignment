# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . ./

ARG REACT_APP_BACKEND_BASE_URL
ENV REACT_APP_BACKEND_BASE_URL=${REACT_APP_BACKEND_BASE_URL}

RUN npm run build

# Stage 2: Serve static files
FROM nginx:alpine

# Remove default nginx static site
RUN rm -rf /usr/share/nginx/html/*

# Copy built React app to nginx web root
COPY --from=builder /app/build /usr/share/nginx/html

# Optional: Replace default nginx config with custom one
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
