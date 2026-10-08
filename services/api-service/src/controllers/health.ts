import type { Context } from 'hono';

export const getHealth = (c: Context) => {
	return c.json({
		success: true,
		message: 'API Service is up running',
	});
};
