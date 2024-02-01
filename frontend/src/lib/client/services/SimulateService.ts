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
   * Plan
   * The plan function executing all the different subfunctions.
   *
   * The plan function is done in the following 8 steps:
   * 1. All the relevant data is gathered in setup_planning
   * 2. For each day, relevant data is gathered in loop_helpers
   * 3. The greedy algorithm is executed with plan_greedy, resulting in a base
   * planning
   * 4. The framework for the results is created in create_results
   * 5. The results of greedy algorithm are documented in write_results
   * 6. If selected, the simulated annealing is performed, resulting in an
   * improved planning
   * 7. The results, and any improvements, are recorded again in write_results
   * 8. The results and planned in data is send back to the frontend
   *
   * The reason for performing write_results twice is in case the random nature
   * of simulated annealing causes a worse result during simulated annealing.
   * While this is unlikely, it technically is possible.
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
