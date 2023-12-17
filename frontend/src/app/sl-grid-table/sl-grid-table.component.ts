import { Component, OnInit, OnDestroy } from "@angular/core";
import { ApiService } from "../api.service";
import { CommonModule } from "@angular/common";
import { Subscription } from "rxjs";

@Component({
  selector: "app-sl-grid-table",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./sl-grid-table.component.html",
  styleUrl: "./sl-grid-table.component.css",
  providers: [ApiService],
})
export class SlGridTableComponent implements OnInit, OnDestroy {
  simulationData: any;
  private simulationDataSubscription!: Subscription;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.simulationDataSubscription = this.apiService.simulationResult$.subscribe((data) => {
      console.log("Simulation Result Subscription Triggered");
      console.log("data: ", data);
      if (data) {
        this.simulationData = data;
        console.log("Simulation Data:", this.simulationData);
      } else {
        console.log("No Simulation Data Available");
      }
    });
  }

  ngOnDestroy() {
    if (this.simulationDataSubscription) {
      this.simulationDataSubscription.unsubscribe();
    }
  }
}
