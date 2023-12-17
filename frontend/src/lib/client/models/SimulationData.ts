/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { AlgorithmRead } from './AlgorithmRead';
import type { CostModelRead } from './CostModelRead';
import type { TwinWorldRead } from './TwinWorldRead';

export type SimulationData = {
  twin_world: Array<TwinWorldRead>;
  cost_model: Array<CostModelRead>;
  algorithm: Array<AlgorithmRead>;
};

