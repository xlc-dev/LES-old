/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_start_api_simulate_start_post } from "../models/Body_start_api_simulate_start_post";
import type { SelectedModelsInput } from "../models/SelectedModelsInput";
import type { SelectedModelsOutput } from "../models/SelectedModelsOutput";
import type { SelectedOptions } from "../models/SelectedOptions";
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
   * @returns SelectedOptions Successful Response
   * @throws ApiError
   */
  public static startApiSimulateStartPost(
    requestBody: Body_start_api_simulate_start_post
  ): CancelablePromise<SelectedOptions> {
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
   * Plan
   * @param requestBody
   * @returns SelectedModelsOutput Successful Response
   * @throws ApiError
   */
  public static planApiSimulatePlanPost(
    requestBody: SelectedModelsInput
  ): CancelablePromise<SelectedModelsOutput> {
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
