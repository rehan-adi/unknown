import app from './app';
import { logger } from '@/libs/logger';
import { ENV_CONFIG } from '@/config/env';
import { setupSentry } from '@/libs/sentry';
import { startVoiceAgent } from '@/libs/livekit/livekit';

setupSentry();

startVoiceAgent();

export default {
	port: parseInt(ENV_CONFIG.PORT),
	fetch: app.fetch,
};

logger.info(
	{ port: ENV_CONFIG.PORT, env: ENV_CONFIG.NODE_ENV },
	'API service is running on port {port} in {env} mode',
);
