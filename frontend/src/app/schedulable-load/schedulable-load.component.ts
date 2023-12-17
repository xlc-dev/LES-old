import { Component } from "@angular/core";
import { SidebarComponent } from "../sidebar/sidebar.component";
import { SlGridTableComponent } from "../sl-grid-table/sl-grid-table.component";
import { ApiService } from "../api.service";
import { HttpClient, HttpClientModule } from "@angular/common/http";
import { CommonModule } from "@angular/common";

@Component({
  selector: "app-schedulable-load",
  standalone: true,
  imports: [SidebarComponent, SlGridTableComponent, CommonModule, HttpClientModule],
  templateUrl: "./schedulable-load.component.html",
  styleUrl: "./schedulable-load.component.css",
  providers: [ApiService],
})
export class SchedulableLoadComponent {}
