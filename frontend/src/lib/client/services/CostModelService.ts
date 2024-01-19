/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CostModelCreate } from "../models/CostModelCreate";
import type { CostModelRead } from "../models/CostModelRead";
import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";
export class CostModelService {
  /**
   * Get Costmodels
   * @returns CostModelRead Successful Response
   * @throws ApiError
   */
  public static getCostmodelsApiCostmodelGet(): CancelablePromise<Array<CostModelRead>> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/costmodel/",
    });
  }
  /**
   * Post Costmodel
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public static postCostmodelApiCostmodelPost(requestBody: {
    price_network_buy_consumer: any;
    name: any;
    costmodel_algorithm: string;
    description: any;
    price_network_sell_consumer: any;
    fixed_price_ratio: any;
  }): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/costmodel/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Get Costmodel
   * @param id
   * @returns CostModelRead Successful Response
   * @throws ApiError
   */
  public static getCostmodelApiCostmodelIdGet(id: number): CancelablePromise<CostModelRead> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/costmodel/{id}",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Delete Costmodel
   * @param id
   * @returns void
   * @throws ApiError
   */
  public static deleteCostmodelApiCostmodelIdDelete(id: number): CancelablePromise<void> {
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/costmodel/{id}",
      path: {
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
