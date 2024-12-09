# Step 1: Use an official minimal image like Alpine
FROM node:22-alpine

# Step 2: Set the working directory inside the container
WORKDIR /usr/src/app

# Step 3: Install pnpm globally
RUN npm install -g pnpm

# Step 4: Copy package.json, pnpm-lock.yaml and install dependencies
COPY package.json ./

# Step 5: Copy the rest of the application source code
COPY . .
RUN rm -rf ./node_modules
RUN pnpm install

# Step 6: Build the Vite project for production
RUN pnpm build

# Add test script for lab3
RUN pnpm test:ci

# Step 7: Run Vite's built-in preview server within a detached session
CMD ["pnpm", "preview", "--host"]

