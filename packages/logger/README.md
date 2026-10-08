# Logger Package

A shared structured logging library powered by [Pino](https://github.com/pinojs/pino).

It provides a unified `createLogger` utility for all microservices in the workspace. During development, it automatically uses `pino-pretty` to format logs into easily readable output. In production, it writes highly optimized JSON logs.

## Usage

This package is designed to be imported by other services:

```typescript
import { createLogger } from '@unknown/logger';

const logger = createLogger('my-service-name');

// Log a simple message
logger.info('Service started successfully!');

// Log with parameters
logger.info({ port: 3000 }, 'Service started successfully on port {port}');

// Log with an error
logger.error({ err }, 'An error occurred');
```
