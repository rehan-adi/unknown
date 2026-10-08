import * as Sentry from '@sentry/bun';
import { ENV_CONFIG } from '@/config/env';
import { logger as log } from '@/libs/logger';

export const setupSentry = () => {
	if (ENV_CONFIG.NODE_ENV === 'development' || !ENV_CONFIG.SENTRY_DSN) {
		log.info('Sentry is disabled (development mode)');
		return;
	}

	Sentry.init({
		dsn: ENV_CONFIG.SENTRY_DSN,
		environment: ENV_CONFIG.NODE_ENV,
		release: process.env.SENTRY_RELEASE,
	});

	log.info('Sentry initialized successfully');

	process.on('unhandledRejection', (reason) => {
		Sentry.captureException(reason);
	});

	process.on('uncaughtException', (error) => {
		Sentry.captureException(error);
		Sentry.flush(2000).finally(() => process.exit(1));
	});
};

export type SentryContext = {
	tags: {
		controller: string;
		action: string;
		provider?: string;
		userId?: string;
		marketId?: string;
		orderId?: string;
		symbol?: string;
	};
	contexts?: {
		[key: string]: any;
	};
};

export const captureError = (error: unknown, context?: SentryContext | Record<string, any>) => {
	if (ENV_CONFIG.NODE_ENV === 'development' || !ENV_CONFIG.SENTRY_DSN) return;

	Sentry.withScope((scope) => {
		if (context) {
			if ('tags' in context || 'contexts' in context) {
				const ctx = context as SentryContext;
				if (ctx.tags) scope.setTags(ctx.tags);
				if (ctx.contexts) {
					for (const [key, value] of Object.entries(ctx.contexts)) {
						scope.setContext(key, value);
					}
				}
			} else {
				scope.setExtras(context as Record<string, any>);
			}
		}
		Sentry.captureException(error);
	});
};
