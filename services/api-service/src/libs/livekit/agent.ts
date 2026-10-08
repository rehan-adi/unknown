import { logger } from '@/libs/logger';

export default async function agent(ctx: any) {
	logger.info(`Agent started for room: ${ctx.room.name}`);
	await ctx.connect();
	logger.info('Agent successfully connected to room.');
}
