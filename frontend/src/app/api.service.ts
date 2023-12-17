import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from "rxjs";
import { HttpClient } from "@angular/common/http";
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api';
  private simulationResultSource = new BehaviorSubject<any>(null);
  simulationResult$ = this.simulationResultSource.asObservable();
  private simulationCompleted = new BehaviorSubject<boolean>(false);
  private simulationPayload: any;

  constructor(private http: HttpClient) { }

  loadData(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/simulate/load-data`);
  }

  setSimulationPayload(payload: any) {
    this.simulationPayload = payload;
    console.log("Simulation Payload Set:", payload);
  }

  triggerSimulation(): void {
    console.log("Trigger Simulation Called");
    if (this.simulationPayload) {
      this.startSimulation(this.simulationPayload).subscribe();
    } else {
      console.log("No Simulation Payload to Trigger");
    }
  }

  private startSimulation(payload: any): Observable<any> {
    console.log("Starting Simulation with Payload:", payload);
    return this.http.post<any>(`${this.apiUrl}/simulate/start`, payload)
      .pipe(tap(res => {
        console.log("Simulation Result Received:", res);
        this.simulationResultSource.next(res);
        this.simulationCompleted.next(true); // Indicate completion
      }));
  }

  isSimulationCompleted(): Observable<boolean> {
    return this.simulationCompleted.asObservable();
  }

  getCurrentSimulationResult() {
    return this.simulationResultSource.value;
  }
}
