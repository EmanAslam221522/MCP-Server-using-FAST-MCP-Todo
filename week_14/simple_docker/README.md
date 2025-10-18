# Hello World Express App

A simple Express.js application that displays "Hello World" on the root route.

## Prerequisites

- Docker installed on your machine

## Building the Docker Image

Build the Docker image with the following command:

```bash
docker build -t hello-world-app .
```

## Running the Docker Container

Run the container with:

```bash
docker run -p 3000:3000 hello-world-app
```

The application will be accessible at http://localhost:3000

## Alternative: Run with Docker in detached mode

To run the container in the background:

```bash
docker run -d -p 3000:3000 hello-world-app
```

## Stopping the Container

If running in detached mode, first find the container ID:

```bash
docker ps
```

Then stop it:

```bash
docker stop <container-id>
```

## Running without Docker

If you prefer to run without Docker:

```bash
npm install
npm start
```