/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApplianceRead_Output } from "./ApplianceRead_Output";
export type HouseholdRead_Output = {
  name: string;
  size?: number;
  energy_usage: number;
  solar_panels?: number;
  solar_yield_yearly: number;
  id: number;
  appliances?: Array<ApplianceRead_Output>;
  twinworld_id: number;
};
