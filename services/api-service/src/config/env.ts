import { z } from 'zod';

const envSchema = z.object({
	NODE_ENV: z.enum(['development', 'production', 'staging']).default('development'),
	PORT: z.string().default('3000'),

	CORS_ORIGIN: z.string().default('*'),

	LIVEKIT_URL: z.string().url().optional(),
	LIVEKIT_API_KEY: z.string().optional(),
	LIVEKIT_API_SECRET: z.string().optional(),

	SENTRY_DSN: z.string().optional(),
});

export const ENV_CONFIG = envSchema.parse(process.env);
