import { fileURLToPath } from 'node:url';
import { ENV_CONFIG } from '@/config/env';
import { logger as log } from '@/libs/logger';
import { AgentServer, WorkerOptions } from '@livekit/agents';

export async function startVoiceAgent() {
	if (!ENV_CONFIG.LIVEKIT_URL || !ENV_CONFIG.LIVEKIT_API_KEY || !ENV_CONFIG.LIVEKIT_API_SECRET) {
		log.warn('LiveKit credentials not found in environment. Skipping Voice Agent initialization.');
		return;
	}

	try {
		const server = new AgentServer(
			new WorkerOptions({
				agent: fileURLToPath(new URL('./agent.ts', import.meta.url)),
				wsURL: ENV_CONFIG.LIVEKIT_URL,
				apiKey: ENV_CONFIG.LIVEKIT_API_KEY,
				apiSecret: ENV_CONFIG.LIVEKIT_API_SECRET,
			}),
		);

		await server.run();
		log.info('LiveKit Voice Agent server initialized successfully.');
	} catch (error) {
		log.error({ err: error }, 'Failed to start LiveKit Voice Agent server');
	}
}
