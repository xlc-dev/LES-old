/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AlgorithmRead } from "./AlgorithmRead";
import type { CostModelRead } from "./CostModelRead";
import type { HouseholdRead_Input } from "./HouseholdRead_Input";
import type { TwinWorldRead } from "./TwinWorldRead";
export type SelectedModelsInput = {
  chunkoffset: number;
  households: Array<HouseholdRead_Input>;
  costmodel: CostModelRead;
  algorithm: AlgorithmRead;
  twinworld: TwinWorldRead;
};
