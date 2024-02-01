/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AlgorithmRead } from "./AlgorithmRead";
import type { CostModelRead } from "./CostModelRead";
import type { EnergyFlowUploadRead } from "./EnergyFlowUploadRead";
import type { HouseholdRead_Output } from "./HouseholdRead_Output";
import type { TwinWorldRead } from "./TwinWorldRead";
export type SelectedOptions = {
  twinworld: TwinWorldRead;
  costmodel: CostModelRead;
  algorithm: AlgorithmRead;
  energyflow: EnergyFlowUploadRead;
  households: Array<HouseholdRead_Output>;
};
