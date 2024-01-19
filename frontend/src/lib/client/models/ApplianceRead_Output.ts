/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApplianceTimeWindowRead } from "./ApplianceTimeWindowRead";
import type { ApplianceType } from "./ApplianceType";
export type ApplianceRead_Output = {
  name: ApplianceType;
  power: number;
  duration: number;
  daily_usage: number;
  id: number;
  appliance_windows?: Array<ApplianceTimeWindowRead>;
};
