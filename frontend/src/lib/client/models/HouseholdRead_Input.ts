/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApplianceRead_Input } from './ApplianceRead_Input';
export type HouseholdRead_Input = {
  name: string;
  size?: number;
  energy_usage: number;
  solar_panels?: number;
  solar_yield_yearly: number;
  id: number;
  appliances?: Array<ApplianceRead_Input>;
  twinworld_id: number;
};

