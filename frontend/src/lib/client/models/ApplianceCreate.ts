/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ApplianceTimeWindowCreate } from "./ApplianceTimeWindowCreate";
import type { ApplianceType } from "./ApplianceType";

export type ApplianceCreate = {
  name: ApplianceType;
  power: number;
  duration: number;
  daily_usage: number;
  appliance_windows?: Array<ApplianceTimeWindowCreate>;
};
