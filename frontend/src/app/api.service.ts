import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  loadData(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/simulate/load-data`);
  }

  startSimulation(body: any) {
    return this.http.post<any>(`${this.apiUrl}/simulate/start`, body)
  }
}
