import { Routes } from "@angular/router";
import { StepperComponent } from "./stepper/stepper.component";
import { SchedulableLoadComponent } from "./schedulable-load/schedulable-load.component";

export const routes: Routes = [
  { path: "", component: StepperComponent },
  { path: "sl", component: SchedulableLoadComponent },
];
