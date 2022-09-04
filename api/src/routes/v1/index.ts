import express from 'express';

import ping from './endpoints/ping';
import teapot from './endpoints/teapot';

const v1route = express.Router();

v1route.use('/ping', ping);
v1route.use('/teapot', teapot);

export default v1route;
