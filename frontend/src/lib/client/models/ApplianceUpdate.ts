/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ApplianceTimeWindowUpdate } from "./ApplianceTimeWindowUpdate";
import type { ApplianceType } from "./ApplianceType";

export type ApplianceUpdate = {
  name: ApplianceType;
  power: number;
  duration: number;
  daily_usage: number;
  appliance_windows?: Array<ApplianceTimeWindowUpdate>;
};
