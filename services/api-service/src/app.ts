import { Hono } from 'hono';
import { cors } from 'hono/cors';
import * as Sentry from '@sentry/bun';
import { ENV_CONFIG } from '@/config/env';
import { logger as log } from '@/libs/logger';
import { healthRouter } from '@/routes/health';
import { secureHeaders } from 'hono/secure-headers';
import { logger as honoLogger } from 'hono/logger';

const app = new Hono();

app.use(honoLogger());
app.use(
	cors({
		origin: ENV_CONFIG.CORS_ORIGIN.split(',').map((o) => o.trim()),
		allowHeaders: ['Content-Type', 'Authorization', 'X-Custom-Header'],
		allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
		exposeHeaders: ['Content-Length', 'X-Custom-Header'],
		maxAge: 86400,
		credentials: true,
	}),
);
app.use(secureHeaders());

app.use('*', async (_c, next) => {
	await Sentry.withScope(async (scope) => {
		await next();
	});
});

app.route('/api/v1/health', healthRouter);

app.onError((err, c) => {
	if (ENV_CONFIG.NODE_ENV !== 'development' && ENV_CONFIG.SENTRY_DSN) {
		const status = 'status' in err ? (err as any).status : 500;
		if (status >= 500) {
			Sentry.captureException(err);
		}
	}

	log.error({ err }, `[Error] ${err.message}`);

	const status = 'status' in err ? (err as any).status : 500;
	return c.json(
		{
			success: false,
			message: status >= 500 ? 'Internal Server Error' : err.message,
		},
		status as any,
	);
});

export default app;
