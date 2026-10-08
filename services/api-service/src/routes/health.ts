import { Hono } from 'hono';
import { getHealth } from '@/controllers/health';

export const healthRouter = new Hono();

healthRouter.get('/', getHealth);
