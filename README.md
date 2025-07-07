# DESP-AAS Moderation Handling


## Table of Contents

- [Introduction](#Introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [Deployment](#deployment)
- [License](#license)
- [Support](#support)

## Introduction

### What is the Moderation-handling microservice?

The Moderation-handling microservice is a specialized component within architecture. It is responsible for redirecting moderation events in real-time, providing automated content moderation capabilities for distributed systems.

**Key Features:**
- **Event Processing**: Handles incoming moderation events from various sources
- **Real-time Processing**: Provides low-latency event handling for time-sensitive operations
- **Scalable Architecture**: Built to handle high-volume event streams efficiently

**Use Cases:**
- Real-time event monitoring and alerting
- Policy enforcement across distributed systems


## Prerequisites

Before you begin, ensure you have the following installed:
- **Git** 
- **Docker** Docker is mainly used for the test suite, but can also be used to deploy the project via docker compose

## Installation

1. Clone the repository:
```bash
git clone https://github.com/acri-st/moderation.git moderation
cd moderation
```

## Development

## Development Mode

### Standard local development

Setup environment
```bash
make setup
```

Start the development server:
```bash
make start
```

To clean the project and remove node_modules and other generated files, use:
```bash
make clean
```

## Contributing

Check out the **CONTRIBUTING.md** for more details on how to contribute.