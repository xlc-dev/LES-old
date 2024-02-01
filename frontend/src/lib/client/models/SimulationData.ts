/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AlgorithmRead } from "./AlgorithmRead";
import type { CostModelRead } from "./CostModelRead";
import type { EnergyFlowUploadRead } from "./EnergyFlowUploadRead";
import type { TwinWorldRead } from "./TwinWorldRead";
export type SimulationData = {
  twinworld: Array<TwinWorldRead>;
  costmodel: Array<CostModelRead>;
  algorithm: Array<AlgorithmRead>;
  energyflow: Array<EnergyFlowUploadRead>;
};
