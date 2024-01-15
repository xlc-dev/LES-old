/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_start_api_simulate_start_post } from "../models/Body_start_api_simulate_start_post";
import type { HouseholdRead } from "../models/HouseholdRead";
import type { SimulationData } from "../models/SimulationData";

import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";

export class SimulateService {
  /**
   * Get Data
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
   * @param requestBody
   * @returns HouseholdRead Successful Response
   * @throws ApiError
   */
  public static startApiSimulateStartPost(
    requestBody: Body_start_api_simulate_start_post
  ): CancelablePromise<Array<HouseholdRead>> {
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
}
