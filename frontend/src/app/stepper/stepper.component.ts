import { Component, OnInit, ElementRef } from '@angular/core';
import { Router } from '@angular/router';
import {CommonModule} from "@angular/common";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {ApiService} from "../api.service";

@Component({
  selector: 'app-stepper',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './stepper.component.html',
  styleUrl: './stepper.component.css',
  providers: [ApiService]
})
export class StepperComponent implements OnInit {
  algorithms: any[] = [];

  pricingmodels: any[] = [];

  twinworlds: any[] = [];

  activeStep: number = 1;
  currentDescription: string = '';
  pinnedDescription: string | null = null;

  selectedAlgorithms: any[] = [];
  selectedPricingModels: any[] = [];
  selectedTwinWorlds: any[] = [];

  constructor(private apiService: ApiService, private elementRef: ElementRef, private router: Router) { }

  ngOnInit(): void {
    this.elementRef.nativeElement.ownerDocument.body.style.backgroundColor = '#1e1e2d';

    this.apiService.loadData().subscribe((res) => {
      this.algorithms =res.algorithm;
      this.pricingmodels =res.cost_model;
      this.twinworlds =res.twin_world;
    })
  }


  setActiveStep(step: number): void {
    this.activeStep = step;
    this.resetDescriptions();
  }

  getLineProgressWidth(): string {
    switch (this.activeStep) {
      case 1: return '12%';
      case 2: return '52%';
      case 3: return '100%';
      default: return '0%';
    }
  }

  pinDescription(description: string, step: number) {
    this.pinnedDescription = description;
    this.currentDescription = description;

    if (step < 3) {
      this.setActiveStep(step + 1);
    } else {
      this.navigateToSchedulableLoad();
    }
  }

  private navigateToSchedulableLoad() {
    this.router.navigate(['/sl']);
  }

  changeDescription(description: string) {
      this.currentDescription = description;
  }

  resetDescriptions() {
    this.currentDescription = '';
  }

  onAlgorithmSelected(algorithm: any) {
    this.selectedAlgorithms.push(algorithm);
  }

  onPricingModelSelected(model: any) {
    this.selectedPricingModels.push(model);
  }

  onTwinWorldSelected(world: any) {
    this.selectedTwinWorlds.push(world);
  }

  completeSelection() {
    const payload: any = {
      algorithm_id: this.selectedAlgorithms[0].id,
      twinworld_id: this.selectedTwinWorlds[0].id,
      costmodel_id: this.selectedPricingModels[0].id
    }
    this.apiService.startSimulation(payload).subscribe((res) => {
      console.log(res)
      this.navigateToSchedulableLoad()
    });
  }
}
