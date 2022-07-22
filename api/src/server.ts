/* eslint-disable @typescript-eslint/no-var-requires */
require('dotenv').config();

import express from 'express';
import helmet from 'helmet';

import v1route from './routes/v1';

export const app = express();

app.use(helmet());
app.use(express.json());

app.use('/v1', v1route);
