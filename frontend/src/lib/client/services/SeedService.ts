/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";
export class SeedService {
  /**
   * Seed
   * Seeds the database with initial data for the twinworld. Deletes all previous in the database before seeding
   * @param seed
   * @returns null Successful Response
   * @throws ApiError
   */
  public static seedApiSeedPost(seed: number = 0.7358808287447506): CancelablePromise<null> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/seed/",
      query: {
        seed: seed,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
