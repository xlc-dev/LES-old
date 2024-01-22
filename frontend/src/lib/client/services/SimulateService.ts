/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApplianceTime } from "../models/ApplianceTime";
import type { Body_start_api_simulate_start_post } from "../models/Body_start_api_simulate_start_post";
import type { HouseholdRead_Input } from "../models/HouseholdRead_Input";
import type { HouseholdRead_Output } from "../models/HouseholdRead_Output";
import type { SimulationData } from "../models/SimulationData";
import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";
export class SimulateService {
  /**
   * Get Data
   * Get all possible options for the simulation
   * @returns SimulationData Successful Response
   * @throws ApiError
   */
  public static getDataApiSimulateLoadDataGet(): CancelablePromise<SimulationData> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/simulate/load-data",
    });
  }
  /**
   * Start
   * Start the simulation with the given parameters from /get-data
   * @param requestBody
   * @returns HouseholdRead_Output Successful Response
   * @throws ApiError
   */
  public static startApiSimulateStartPost(
    requestBody: Body_start_api_simulate_start_post
  ): CancelablePromise<Array<HouseholdRead_Output>> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/simulate/start",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Reset
   * @returns null Successful Response
   * @throws ApiError
   */
  public static resetApiSimulateResetPost(): CancelablePromise<null> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/simulate/reset",
    });
  }
  /**
   * Stop
   * @returns any Successful Response
   * @throws ApiError
   */
  public static stopApiSimulateStopPost(): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/simulate/stop",
    });
  }
  /**
   * Plan Simulated Annealing
   * @param requestBody
   * @returns ApplianceTime Successful Response
   * @throws ApiError
   */
  public static planSimulatedAnnealingApiSimulatePlanSimulatedAnnealingPost(
    requestBody: Array<HouseholdRead_Input>
  ): CancelablePromise<ApplianceTime> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/simulate/plan_simulated_annealing",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Plan
   * @param requestBody
   * @returns ApplianceTime Successful Response
   * @throws ApiError
   */
  public static planApiSimulatePlanPost(
    requestBody: Array<HouseholdRead_Input>
  ): CancelablePromise<ApplianceTime> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/simulate/plan",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
