# Use the official Node.js runtime as a parent image
FROM node:18-alpine

# Set working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the current directory contents into the container
COPY . .

# Build the app for production
RUN npm run build

# Install a simple http server for serving static content
RUN npm install -g serve

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Serve the app
CMD ["serve", "-s", "build", "-l", "3000"]