FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including Next.js)
RUN npm install

# Copy source code
COPY . .

EXPOSE 3000

# Run Next.js dev server
CMD ["npm", "run", "dev"]
