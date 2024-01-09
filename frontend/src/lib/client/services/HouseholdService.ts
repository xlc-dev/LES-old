import type { HouseholdRead } from "../models/HouseholdRead";
import type { HouseholdCreate } from "../models/HouseholdCreate";
import type { HouseholdUpdate } from "../models/HouseholdUpdate";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";

export class HouseholdService {
  /**
   * Get Households for a specific Twin World
   * @param twinWorldId The ID of the Twin World
   * @returns HouseholdRead[] List of households
   */
  public static async getHouseholds(twinWorldId: number): Promise<HouseholdRead[]> {
    const result = await __request<{ body: HouseholdRead[] }>(OpenAPI, {
      method: 'GET',
      url: `/api/twinworld/${twinWorldId}/households/`,
    });
    return result.body;
  }

  /**
   * Create a new Household in a Twin World
   * @param twinWorldId The ID of the Twin World
   * @param data Household creation data
   * @returns HouseholdRead The created household
   */
  public static async createHousehold(twinWorldId: number, data: HouseholdCreate): Promise<HouseholdRead> {
    const result = await __request<{ body: HouseholdRead }>(OpenAPI, {
      method: 'POST',
      url: `/api/twinworld/${twinWorldId}/households/`,
      body: data,
    });
    return result.body;
  }

  /**
   * Update a Household in a Twin World
   * @param twinWorldId The ID of the Twin World
   * @param householdId The ID of the Household to update
   * @param data Household update data
   * @returns HouseholdRead The updated household
   */
  public static async updateHousehold(twinWorldId: number, householdId: number, data: HouseholdUpdate): Promise<HouseholdRead> {
    const result = await __request<{ body: HouseholdRead }>(OpenAPI, {
      method: 'PUT',
      url: `/api/twinworld/${twinWorldId}/households/${householdId}`,
      body: data,
    });
    return result.body;
  }

  /**
   * Delete a Household from a Twin World
   * @param twinWorldId The ID of the Twin World
   * @param householdId The ID of the Household to delete
   */
  public static async deleteHousehold(twinWorldId: number, householdId: number): Promise<void> {
    await __request<{ body: void }>(OpenAPI, {
      method: 'DELETE',
      url: `/api/twinworld/${twinWorldId}/households/${householdId}`,
    });
  }
}
